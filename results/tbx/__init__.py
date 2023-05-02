import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import xarray as xr

from .literals import *

plt.style.use(Path(__file__).parent / "../plots/glp.mplstyle")

results = Path(__file__).parent / "../../glp-results/data"

work = Path(__file__).parent / "../../glp-work"
work_remote = Path("/talos/scratch/mlang/glp-work")

img = Path(__file__).parent / "../../glp-paper/img/"
tables = Path(__file__).parent / "../../glp-paper/tables/"


def load(file):
    file = Path(file)
    if file.suffix == ".nc":
        return xr.open_dataset(file)
    elif file.suffix == ".npz":
        return np.load(file, allow_pickle=True)
    else:
        raise IOError(f"cannot open file {file}")


def get_and_concatenate(getter, quantity, name):
    import xarray as xr

    data = [getter(q) for q in quantity]
    data = xr.concat(data, dim=xr.DataArray(data=quantity, name=name, dims=(name)))

    return data


def savefig(fig, file):
    fig.savefig(file, bbox_inches="tight", pad_inches=0.05)


def savetab(tab, file):
    with open(file, "w") as f:
        f.write(tab)


def fig_and_ax(figsize=None):
    if figsize:
        fig = plt.figure(figsize=figsize, dpi=200)
    else:
        fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = plt.axes()
    return fig, ax


def minor_ticks_every(ax, spacing, direction="x"):
    from matplotlib.ticker import MultipleLocator

    if direction == "x":
        ax.xaxis.set_minor_locator(MultipleLocator(spacing))
    else:
        ax.yaxis.set_minor_locator(MultipleLocator(spacing))


def major_ticks_every(ax, spacing, direction="x"):
    from matplotlib.ticker import MultipleLocator

    if direction == "x":
        ax.xaxis.set_major_locator(MultipleLocator(spacing))
    else:
        ax.yaxis.set_major_locator(MultipleLocator(spacing))


def scale_labels(ax, scale, direction="x"):
    from matplotlib.ticker import FuncFormatter

    ticks = FuncFormatter(lambda x, pos: "{0:g}".format(x / scale))

    if direction == "x":
        ax.xaxis.set_major_formatter(ticks)
    else:
        ax.yaxis.set_major_formatter(ticks)


colwidth = 2 * 3.375


def round_up_to_digits(x, digits=2):
    return np.ceil(x * 10**digits) / 10**digits

