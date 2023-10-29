"""Recompute a trajectory that already ran."""


from jax import lax, jit, pmap

import numpy as np
from ase.units import fs
from pathlib import Path
from collections import namedtuple

from glp.instantiate import get_calculator
from glp.dynamics import atoms_to_input

from gkx import comms
from gkx.utils.trees import (
    tree_slice,
    tree_concatenate,
    tree_unsqueeze,
    tree_split_first_dim,
    tree_merge_first_dim,
)

from .dataset import *
from .batcher import to_batch, fake_batch
from .chunker import Chunker
from .utils import get_length

Input = namedtuple("Input", ("system", "velocities", "masses"))


def run(
    trajectory,
    potential,
    calculator,
    step_size,
    initial_atoms,
    supercell_atoms=None,
    primitive_atoms=None,
    outfolder=Path("recompute/"),
    batch_size=25,
    chunk_size=2500,
    initial_step=0,
    initial_chunk=0,
    devices=1,
):
    maxsteps = len(trajectory.time)
    parallel = devices > 1

    # todo: be more forgiving
    assert maxsteps % chunk_size == 0
    assert maxsteps % step_size == 0
    assert maxsteps > 1  # otherwise we won't save anything

    if parallel:
        assert batch_size % devices == 0
        comms.talk(
            f"will parallelise across {devices} devices in batches of {int(batch_size/devices)}",
            full=True,
        )

    reporter = comms.reporter()
    reporter.start("running recompute")
    reporter.step("setup")

    calculator_fn = get_calculator(potential, calculator)

    update = lambda atoms, batch_size, devices, parallel: get_scan(
        calculator_fn, atoms, batch_size, devices, parallel
    )

    scanner, state = update(initial_atoms, batch_size, devices, parallel)

    chunker = Chunker(chunk_size)

    reporter.step(f"re ", spin=False)
    n_step = initial_step
    n_chunk = initial_chunk
    state_str = "starting"

    # we generally count in steps of recomputation, not trajectory steps
    # chunker.count: number of steps we've successfully computed
    # n_step: starting step of chunk currently being assembled

    while n_step * step_size < maxsteps:
        reporter.tick("🚀 " + state_str)

        batch_start = (chunker.count + initial_step) * step_size  # index in trajectory
        batch_end = batch_start + batch_size * step_size
        if batch_end > maxsteps:
            # todo: do more clever things
            if parallel:
                comms.talk("finishing final steps in serial mode")
                parallel = False
                devices = 1

            reporter.tick("finishing up")
            batch_end = maxsteps
            batch_size = int((batch_end - batch_start) / step_size)
            scanner, state = update(
                trajectory.get_atoms(batch_start), batch_size, devices, parallel
            )

        input_batch = tree_concatenate(
            [
                tree_unsqueeze(get_input(trajectory, i))
                for i in range(batch_start, batch_end, step_size)
            ]
        )

        if parallel:
            input_states = tree_concatenate([tree_unsqueeze(state)] * devices)

            input_batches = tree_split_first_dim(input_batch, devices)

            new_state, out = scanner(
                input_states, input_batches
            )  # -> (results, state) w/ devices, batch_size/devices leading axes

            out = tree_merge_first_dim(out)
            overflow = out[1].any()

        else:
            new_state, out = scanner(state, input_batch)  # -> out = (results, overflow)
            overflow = new_state.overflow

        if overflow:
            comms.talk("overflow!")
            good_until = np.argmax(out[1] == True)  # find first overflow
            if good_until == 0:
                comms.warn("overflow occured immediately")
                comms.warn(
                    "if this occurs repeatedly, skin+cutoff may be too small for cell"
                )
                scanner, state = update(
                    trajectory.get_atoms(batch_start), batch_size, devices, parallel
                )
                results = None
            else:
                # salvage non-overflow parts of batch
                scanner, state = update(
                    trajectory.get_atoms(batch_start + (good_until - 1) * step_size),
                    batch_size,
                    devices,
                    parallel,
                )
                results = tree_slice(out[0], slice(0, good_until))

        else:
            if parallel:
                state = tree_slice(new_state, -1)
            else:
                state = new_state
            results = out[0]

        if results is not None:
            chunk = chunker.submit(results)

        time_per_step = reporter.timer_step() / chunker.count
        current_steps = chunker.count + initial_step
        remaining_steps = maxsteps / step_size - current_steps
        remaining_time = time_per_step * remaining_steps

        state_str = f"{current_steps*step_size}/{maxsteps} (ETA: {(remaining_time/60):.1f}min) ({time_per_step*1000:.0f}ms/step)"

        if chunk is None:
            continue
        else:
            reporter.tick("🔧 " + state_str)

            dataset = chunk_to_dataset(
                trajectory,
                chunk,
                n_step,
                step_size,
            )

            reporter.tick("💾 " + state_str)
            # attempt at atomic write -- does this work?
            tmpfile = outfolder / "TMP"
            dataset.to_netcdf(tmpfile)
            tmpfile.replace(outfolder / f"{n_chunk:06d}.nc")

            comms.talk(
                f"completed chunk {n_chunk} "
                + f"(ETA: {(remaining_time/60):.1f}min) ({time_per_step*1000:.0f}ms/step)",
                full=True,
            )

            n_step += chunk_size
            n_chunk += 1

    reporter.tick("(✨) " + state_str)
    reporter.done(f"done at {(reporter.timer_step() / chunker.count)*1000:.0f}ms/step")


def get_scan(calculator_fn, atoms, batch_size, devices, parallel):
    system, velocities, masses = atoms_to_input(atoms)
    calculator, state = calculator_fn(system)

    if parallel:
        scan_size = int(batch_size / devices)
    else:
        scan_size = batch_size

    @jit
    def calculate(prior_state, inputs):
        results, new_state = calculator.calculate(
            inputs.system,
            prior_state,
            velocities=inputs.velocities,
            masses=inputs.masses,
        )

        return new_state, (results, new_state.overflow)

    def scanner(state, input_batch):
        return lax.scan(calculate, state, input_batch, length=scan_size)

    if parallel:
        scanner = pmap(scanner)

    return scanner, state


def get_input(trajectory, index):
    atoms = trajectory.get_atoms(index)
    return Input(*atoms_to_input(atoms))


def chunk_to_dataset(trajectory, chunk, start_idx, step_size):
    from vibes import keys

    length = get_length(chunk)

    dt = trajectory.data.attrs["timestep"] * step_size

    time = dt * np.arange(start_idx, start_idx + length, dtype=float)
    time = {keys.time: time}

    final_data = {}
    for key, value in chunk.items():
        k, d = data_to_array(key, value, time, trajectory.reference_atoms, length)
        final_data[k] = d

    data = xr.Dataset(final_data, coords=time)

    data.attrs = trajectory.data.attrs

    return data
