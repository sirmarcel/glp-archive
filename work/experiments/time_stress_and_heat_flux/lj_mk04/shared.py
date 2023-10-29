from jax.config import config

config.update("jax_enable_x64", True)

import jax.numpy as jnp

import numpy as np
from time import monotonic
import yaml

from jax import jit

from ase.build import bulk
from ase.calculators.lj import LennardJones
from ase.stress import voigt_6_to_full_3x3_stress
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution

from glp import atoms_to_system, comms
from glp.instantiate import get_calculator
from glp.ase import Calculator
from glp.dynamics import atoms_to_input

n_samples = 1000
skin = 1.0
skin_unfolder = 2.0


def prepare(size, x64=False):
    if x64:
        dtype = jnp.float64
        outfile = f"results_n{size}_64.yaml"
    else:
        dtype = jnp.float32
        outfile = f"results_n{size}_32.yaml"

    if size == 864:
        initial_atoms = bulk("Ar", cubic=True) * [6, 6, 6]
    elif size == 2048:
        initial_atoms = bulk("Ar", cubic=True) * [8, 8, 8]
    elif size == 4000:
        initial_atoms = bulk("Ar", cubic=True) * [10, 10, 10]

    assert len(initial_atoms) == size

    initial_inputs = atoms_to_input(initial_atoms, dtype=dtype)

    def get_atoms(seed):
        atoms = initial_atoms.copy()
        atoms.rattle(stdev=0.01, seed=seed)

        # rng = np.random.default_rng(seed)
        # strain = 0.01 * rng.uniform(low=-1.0, high=1.0, size=(3, 3))
        # strain = 0.5 * (strain + strain.T)
        # strain += np.eye(3)

        # cell = atoms.get_cell().array

        # strained_cell = np.einsum("Ba,Aa->AB", strain, cell)

        # atoms.set_cell(strained_cell, scale_atoms=True)

        MaxwellBoltzmannDistribution(
            atoms, temperature_K=10, rng=np.random.default_rng(seed)
        )

        return atoms

    atomss = [get_atoms(i) for i in range(n_samples)]
    inputs = [atoms_to_input(atoms, dtype=dtype) for atoms in atomss]

    return size, initial_inputs, inputs, atomss, outfile, dtype
