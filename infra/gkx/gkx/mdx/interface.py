# run a GK NVE

from jax import lax, jit

import numpy as np
import xarray as xr
from pathlib import Path

from ase.units import fs
from vibes import keys, dimensions

from glp.instantiate import get_dynamics
from glp.dynamics import atoms_to_input

from gkx import comms
from gkx.utils import open_trajectory

from .nve import run

defaults = {
    "files": {
        "geometry": "geometry.in",
        "supercell": "geometry.in.supercell",
        "primitive": "geometry.in.primitive",
    },
    "batch_size": 25,
    "chunk_size": 2500,
    "outfolder": Path("trajectory/"),
    "maxsteps": 25000,
}


def run_from_yaml(file):
    from specable.inout import read_yaml

    run_from_dict(read_yaml(file))


def run_from_dict(dct):
    from ase import io
    from ase import units

    dct = {**defaults, **dct}

    potential = dct.pop("potential")
    calculator = dct.pop("calculator")

    # todo: make exception for recompute?
    maxsteps = dct.pop("maxsteps")
    batch_size = dct.pop("batch_size")
    chunk_size = dct.pop("chunk_size")

    if maxsteps % chunk_size != 0:
        maxsteps = (maxsteps // chunk_size + 1) * chunk_size
        comms.warn(
            f"rounding up maxsteps to {maxsteps} (must be divisible by chunk_size)"
        )

    files = dct.pop("files")
    initial_atoms = io.read(files.pop("geometry"), format="aims")

    if "supercell" in files:
        supercell_atoms = io.read(files.pop("supercell"), format="aims")
    else:
        supercell_atoms = None

    if "primitive" in files:
        primitive_atoms = io.read(files.pop("primitive"), format="aims")
    else:
        primitive_atoms = None

    outfolder = Path(dct.pop("outfolder"))

    if outfolder.is_dir():
        if "recompute" not in dct:
            if (outfolder / "TMP").is_file():
                comms.warn("found TMP file; deleting. (did a job shut down hard?)")
                (outfolder / "TMP").unlink()

            n_chunks = len(list(outfolder.glob("*.nc")))
            if n_chunks > 0:
                traj = open_trajectory(outfolder)
                initial_step = len(traj.time)
                if initial_step >= maxsteps:
                    comms.talk("already done, quitting")
                    return None

                initial_atoms = traj.get_atoms(-1)
                initial_chunk = n_chunks
                comms.talk(
                    f"restarting from step {initial_step}, chunk {initial_chunk}"
                )
            else:
                initial_step = 0
                initial_chunk = 0

    else:
        outfolder.mkdir()
        initial_step = 0
        initial_chunk = 0

    if "nve" in dct:
        from .nve import run

        dt = dct["nve"]["dt"]

        run(
            maxsteps,
            potential,
            calculator,
            dt,
            initial_atoms,
            supercell_atoms=supercell_atoms,
            primitive_atoms=primitive_atoms,
            outfolder=outfolder,
            batch_size=batch_size,
            chunk_size=chunk_size,
            initial_step=initial_step,
            initial_chunk=initial_chunk,
        )

    elif "nvt" in dct or "npt" in dct:
        from .nvt_npt import run

        run(
            maxsteps,
            potential,
            calculator,
            dct,
            initial_atoms,
            supercell_atoms=supercell_atoms,
            primitive_atoms=primitive_atoms,
            outfolder=outfolder,
            chunk_size=chunk_size,
            initial_step=initial_step,
            initial_chunk=initial_chunk,
        )

    elif "recompute" in dct:
        from .recompute import run

        assert str(dct["recompute"]["trajectory"]) != str(outfolder)

        trajectory = open_trajectory(dct["recompute"]["trajectory"])
        step_size = dct["recompute"]["step_size"]
        devices = dct["recompute"].get("devices", 1)

        if outfolder.is_dir():
            if (outfolder / "TMP").is_file():
                comms.warn("found TMP file; deleting. (did a job shut down hard?)")
                (outfolder / "TMP").unlink()

            n_chunks = len(list(outfolder.glob("*.nc")))
            if n_chunks > 0:
                traj = open_trajectory(outfolder)
                initial_step = len(traj)

                if (initial_step * step_size) >= len(trajectory.time):
                    comms.talk("already done, quitting")
                    return None

                initial_chunk = n_chunks
                initial_atoms = trajectory.get_atoms(initial_step * step_size)
                comms.talk(
                    f"restarting from (recompute) step {initial_step}, chunk {initial_chunk}"
                )
            else:
                initial_step = 0
                initial_chunk = 0

        run(
            trajectory,
            potential,
            calculator,
            step_size,
            initial_atoms,
            supercell_atoms=supercell_atoms,
            primitive_atoms=primitive_atoms,
            outfolder=outfolder,
            chunk_size=chunk_size,
            batch_size=batch_size,
            initial_step=initial_step,
            initial_chunk=initial_chunk,
            devices=devices,
        )
