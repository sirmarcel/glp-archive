from jax.config import config

config.update("jax_enable_x64", True)

import jax.numpy as jnp

import numpy as np
from jax import jit

from ase.io import read
from ase.stress import voigt_6_to_full_3x3_stress
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution

from glp import atoms_to_system, comms
from glp.instantiate import get_calculator
from glp.ase import Calculator
from glp.dynamics import atoms_to_input

n_samples = 10
skin = 1.0
skin_unfolder = 2.0

primitive = read("geometry.in.primitive", format="aims")

reporter = comms.reporter()


def calculate_numerical_stress(atoms, d=1e-6, voigt=True):
    """Calculate numerical stress using finite difference."""

    stress = np.zeros((3, 3), dtype=float)

    cell = atoms.cell.copy()
    V = atoms.get_volume()
    for i in range(3):
        x = np.eye(3)
        x[i, i] += d
        atoms.set_cell(np.dot(cell, x), scale_atoms=True)
        eplus = atoms.get_potential_energy()

        x[i, i] -= 2 * d
        atoms.set_cell(np.dot(cell, x), scale_atoms=True)
        eminus = atoms.get_potential_energy()

        stress[i, i] = (eplus - eminus) / (2 * d * V)
        x[i, i] += d

        j = i - 2
        x[i, j] = d
        x[j, i] = d
        atoms.set_cell(np.dot(cell, x), scale_atoms=True)
        eplus = atoms.get_potential_energy()

        x[i, j] = -d
        x[j, i] = -d
        atoms.set_cell(np.dot(cell, x), scale_atoms=True)
        eminus = atoms.get_potential_energy()

        stress[i, j] = (eplus - eminus) / (4 * d * V)
        stress[j, i] = stress[i, j]

    atoms.set_cell(cell, scale_atoms=True)

    if voigt:
        return stress.flat[[0, 4, 8, 5, 2, 1]]
    else:
        return stress


for x64 in [True, False]:
    reporter.start(f"test with 64bit={x64}")

    if x64:
        dtype = jnp.float64
        outfile = "results_64.npz"
    else:
        dtype = jnp.float32
        outfile = "results_32.npz"

    initial_atoms = primitive * [4, 8, 8]
    initial_system = atoms_to_system(initial_atoms, dtype=dtype)

    def get_atoms(seed):
        atoms = initial_atoms.copy()
        atoms.rattle(stdev=0.01, seed=seed)

        rng = np.random.default_rng(seed)
        strain = 0.01 * rng.uniform(low=-1.0, high=1.0, size=(3, 3))
        strain = 0.5 * (strain + strain.T)
        strain += np.eye(3)

        cell = atoms.get_cell().array

        strained_cell = np.einsum("Ba,Aa->AB", strain, cell)

        atoms.set_cell(strained_cell, scale_atoms=True)

        MaxwellBoltzmannDistribution(
            atoms, temperature_K=10, rng=np.random.default_rng(seed)
        )

        return atoms

    potential_config = {
        "mlff": {
            "folder": "model/",
            "dtype": dtype,
        }
    }

    calculator_configs = {
        "atom_pair_fractional_mic": {
            "variations_atom_pair": {
                "skin": skin,
                "fractional_mic": True,
                "heat_flux": True,
                "convective": False,
            }
        },
        "atom_pair_textbook_mic": {
            "variations_atom_pair": {
                "skin": skin,
                "fractional_mic": False,
                "heat_flux": True,
                "convective": False,
            }
        },
        # eq. 15
        "strain_system": {
            "variations_end_to_end": {
                "skin": skin,
                "stress_mode": "strain_system",
            }
        },
        # eq. 16
        "strain_graph": {
            "variations_end_to_end": {
                "skin": skin,
                "stress_mode": "strain_graph",
            }
        },
        # eq. 17
        "unfolded_strain_unfolded": {
            "variations_unfolded": {
                "skin": skin,
                "skin_unfolder": skin_unfolder,
                "stress_mode": "strain_unfolded",
            }
        },
        # eq. 18
        "strain_direct": {
            "variations_end_to_end": {
                "skin": skin,
                "stress_mode": "direct",
            }
        },
        # eq. 19
        "atom_pair_direct": {
            "atom_pair": {
                "skin": skin,
                "heat_flux": True,
                "convective": False,
            }
        },
        # eq. 20
        "unfolded_direct_unfolded": {
            "variations_unfolded": {
                "skin": skin,
                "skin_unfolder": skin_unfolder,
                "stress_mode": "direct_unfolded",
            }
        },
        "hf_unfolded": {
            "heat_flux_unfolded": {
                "skin": skin,
                "skin_unfolder": skin_unfolder,
                "convective": False,
            }
        },
        "hf_hardy": {
            "heat_flux_hardy": {
                "skin": skin,
                "convective": False,
            }
        },
    }
    ase_calculator = Calculator(
        get_calculator(potential_config, {"atom_pair": {"skin": skin}}), dtype=dtype
    )

    reporter.step("setup")

    samples = [get_atoms(i) for i in range(n_samples)]
    inputs = [atoms_to_input(atoms, dtype=dtype) for atoms in samples]

    calculators = {}

    for name, config in calculator_configs.items():
        calculators[name] = Calculator(
            get_calculator(potential_config, config), dtype=dtype, raw=True
        )

    results = {}
    for name, calc in calculators.items():
        reporter.step(f"calc {name}", spin=False)

        for i, atoms in enumerate(samples):
            reporter.tick(f"{i}")
            res = calc.calculate(atoms)

            for key, value in res.items():
                fullkey = f"{key}_{name}"
                if fullkey in results:
                    results[fullkey].append(value)
                else:
                    results[fullkey] = [value]

    ds = np.logspace(-6, -2, num=5 + 2 * 4, base=10)
    for d in ds:
        name = f"finite_differences_{d:.0e}"
        reporter.step(name)
        stress = []
        for atoms in samples:
            atoms.calc = ase_calculator
            stress.append(
                calculate_numerical_stress(atoms, voigt=False, d=d) * atoms.get_volume()
            )

        results["stress_" + name] = stress

    reporter.step("write")

    np.savez_compressed(outfile, **results)

    reporter.done()
