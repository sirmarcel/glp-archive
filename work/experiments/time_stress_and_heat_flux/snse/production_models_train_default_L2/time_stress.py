from shared import *
from glp.ase import Calculator


calculator_configs = {
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
            "heat_flux": False,
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
}


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



for size in [864, 2048, 4000]:
    for x64 in [True, False]:
        size, initial, inputs, atomss, outfile, dtype = prepare(size, x64=x64)
        system = initial[0]

        potential_config = {
            "mlff": {
                "folder": "model/",
                "dtype": dtype,
            }
        }

        things = {}

        for key, config in calculator_configs.items():
            print(f"setup {key}")
            fn = get_calculator(potential_config, config)

            calc, state = fn(system)
            calc_fn = jit(calc.calculate)
            _, state = calc_fn(system, state)

            things[key] = (calc_fn, state)

        results = {k: [] for k in things.keys()}

        for _ in range(3):
            for key, thing in things.items():
                print(f"time {key}")
                calc, state = thing
                start = monotonic()
                for inp in inputs:
                    system = inp[0]
                    res, state = calc(system, state)
                    assert not state.overflow
                    np.array(res["stress"])

                end = monotonic()
                results[key].append((end - start) / (n_samples * size))

        if not x64:
            d = 1e-3
        else:
            d = 1e-4

        key = f"finite_differences_{d:.0e}"
        results[key] = []
        ase_calculator = Calculator(
            get_calculator(potential_config, {"atom_pair": {"skin": skin}}), dtype=dtype
        )
        atoms = atomss[0].copy()
        atoms.calc = ase_calculator
        atoms.get_forces()

        for _ in range(3):
            start = monotonic()
            for atoms in atomss:
                atoms.calc = ase_calculator
                calculate_numerical_stress(atoms, d=d)

            end = monotonic()
            results[key].append((end - start) / (n_samples * size))

        for key, value in results.items():
            s = [f"{v*1e6:.1f}" for v in value]
            print(f"{key}: {s} µs/atom")

        with open("stress_" + outfile, "w") as f:
            f.write(yaml.dump(results))
