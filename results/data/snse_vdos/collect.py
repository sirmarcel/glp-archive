import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path
from stepson import Trajectory

sokrates_L1 = Path(
    "/talos/scratch/mlang/glp-work/runs/snse/production_models_train_default_L1"
)
sokrates_L2 = Path(
    "/talos/scratch/mlang/glp-work/runs/snse/production_models_train_default_L2"
)
sokrates_L3 = Path(
    "/talos/scratch/mlang/glp-work/runs/snse/production_models_train_default_L3"
)
reference = Path("/talos/scratch/mlang/gkx-md/experiments/snse/reference/nve.1.nc")
maxfreq = 30
npad = 10000
window = 25


def vibes_get_vdos(velocities, masses, hann=False, npad=10000):
    # borrowed from https://gitlab.com/vibes-developers/vibes/-/merge_requests/57/
    from vibes.correlation import get_autocorrelationNd
    from vibes.fourier import get_fourier_transformed

    n_atoms = velocities.shape[1]

    assert len(masses) == n_atoms, (len(masses), n_atoms)

    # mass-scale the velocities
    velocities *= masses**0.5

    v_corr = get_autocorrelationNd(velocities, normalize=True, hann=hann)
    df_vdos = get_fourier_transformed(v_corr, npad=npad)

    return df_vdos


def get_reference():
    return Trajectory(reference)


def get_rerun(folder):
    return Trajectory(folder / "vdos/trajectory/")


def get_single_vdos(dataset):
    velocities = dataset.velocities.compute()
    masses = dataset.masses
    vdos = vibes_get_vdos(velocities=velocities, masses=masses, hann=False, npad=npad)
    df = vdos.real.sum(axis=(1, 2)).to_series()[:maxfreq].rolling(window=window).mean()
    return df.to_xarray()


sokrates = get_single_vdos(get_rerun(sokrates_L1))
sokrates.to_netcdf("default_L1.nc")


sokrates = get_single_vdos(get_rerun(sokrates_L2))
sokrates.to_netcdf("default_L2.nc")

sokrates = get_single_vdos(get_rerun(sokrates_L3))
sokrates.to_netcdf("default_L3.nc")

aims = get_single_vdos(get_reference())
aims.to_netcdf("aims.nc")
