import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from tbx.load import ensemble
from tbx import gk, get_and_concatenate

from pathlib import Path

basedir = Path("/talos/scratch/mlang/glp-work/runs/snse")

models = [
    "production_models_train_default_L1",
    "production_models_train_default_L2",
    "production_models_train_default_L3",
]
workflow = "gk_2_fk_lattice"


def filename(maxsteps, freq=1.0):
    return f"gk.to_{maxsteps}.freq_{freq:.2f}.nc"


def get_dataset(model, n, maxsteps):
    if maxsteps <= 250000:
        maxtime=5e4
    else:
        maxtime=0.5e6

    return gk.combine(
        ensemble(
            ((basedir / model) / workflow) / f"300/n_{n}",
            "maxsteps",
            filename(maxsteps, freq=1.0),
        ),
        maxtime=maxtime,
    )


def get_kappa(model, n, maxsteps):
    data = get_dataset(model, n, maxsteps)
    return gk.get_kappa(data, a=None, eps=0)


n_atomss = {
    "production_models_train_default_L1": [864],
    "production_models_train_default_L2": [256, 864, 2048, 4000],
    "production_models_train_default_L3": [864],
}
maxstepss = range(25000, 1000001, 25000)

for model in models:
    outfile = Path(f"{model}.nc")
    if outfile.is_file():
        print(f"{outfile} exists, skip")
        continue

    print(f"working on {outfile.stem}")

    def get_maxsteps(n, maxsteps):
        k, e = get_kappa(model, n, maxsteps)
        k = xr.DataArray(k, name="kappa_mean")
        e = xr.DataArray(e, name="kappa_stderr")

        d = xr.Dataset({"kappa_mean": k, "kappa_stderr": e})

        return d

    def get_maxstepss(n):
        return get_and_concatenate(
            lambda maxsteps: get_maxsteps(n, maxsteps), maxstepss, "maxsteps"
        )

    def get_n_atomss():
        return get_and_concatenate(lambda n: get_maxstepss(n), n_atomss[model], "n_atoms")

    data = get_n_atomss()
    data.to_netcdf(outfile)
