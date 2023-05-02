import sys

sys.path.insert(0, "../../")

from pathlib import Path
from tbx import gk, work_remote
from tbx.load import ensemble

prod_folder = (
    work_remote
    / "runs/snse/"
)


# settings
freq = 1.00
maxsteps = 250000
n_atoms = 864

def get_dataset(L):
    return gk.combine(
        ensemble(
            prod_folder / f"production_models_train_default_L{L}/gk_2_fk_lattice/300/n_{n_atoms}",
            "maxsteps",
            f"gk.to_{maxsteps}.freq_{freq:.2f}.nc",
            n=11,
        ),
        maxtime=1e5
    )
    
for L in [1, 2, 3]:
    data = get_dataset(L)
    data.to_netcdf(f"sokrates_L{L}_prod.nc")
