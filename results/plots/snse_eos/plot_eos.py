#! /usr/bin/env python3

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import typer
from ase.units import GPa
from matplotlib import pyplot as plt
from rich import print as echo

warnings.simplefilter("ignore")

plt.style.use("glp.mplstyle")


def vinet(V, E0, B0, BP, V0):
    "Vinet equation from PRB 70, 224107"

    X = (V / V0) ** (1 / 3)
    eta = 3 / 2 * (BP - 1)

    E = E0 + 2 * B0 * V0 / (BP - 1) ** 2 * (
        2 - (5 + 3 * BP * (X - 1) - 3 * X) * np.exp(-eta * (X - 1))
    )
    return E


def vinet_pressure(V, B0, BP, V0):
    """Eq. (4.1) in P. Vinet et al., Phys Rev B 35, 1945 (1987)."""
    X = (V / V0) ** (1 / 3)
    eta = 3 / 2 * (BP - 1)
    P = 3 * B0 * (1 - X) / X ** 2 * np.exp(eta * (1 - X))
    return P


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(
    folder: Path,
    file_data: Path = "eos.csv",
    file_fit_e: Path = "eos_e.json",
    file_fit_p: Path = "eos_p.json",
    outfile: Path = None,
):

    fig, ax = plt.subplots(figsize=(6, 3))

    echo(folder)
    df = pd.read_csv(folder / file_data, comment="#", index_col="volume")

    x = df.index / df.N  # np.linspace(df.index.min(), df.index.max(), 51)
    y = df.energy / df.N

    popt_e = json.load(open(folder / file_fit_e))
    popt_p = json.load(open(folder / file_fit_p))

    # baseline energy
    E0 = popt_e["E0"]

    kw_p = {"lw": 1, "c": "#313131"}
    kw_e = {"lw": 2, "ls": (0, (5, 4)), "c": "C3"}
    kw_calc = {"marker": "o", "c": "k", "lw": 0, "ms": 4}
    kw_all = {"clip_on": False}

    # create volume space
    _x = np.linspace(x.min(), x.max(), 51)

    # plot EOS created from pressure fit
    _y = 1e3 * (vinet(_x, *popt_p.values()) - E0)
    ax.plot(_x, _y, **kw_p, **kw_all)
    # plot EOS created from energy fit
    _y = 1e3 * (vinet(_x, *popt_e.values()) - E0)
    ax.plot(_x, _y, **kw_e, **kw_all)
    # plot calculated data points
    _y = 1e3 * (y - E0)
    ax.plot(x, _y, **kw_calc, **kw_all)

    # labels
    ax.set_xlabel(r"Volume per atom (${\rm \AA}^3$)")
    ax.set_ylabel("Energy per atom (meV)")

    kw = {"loc": 9, "frameon": False, "markerfirst": False}
    ax.legend(["EOS fit to pressure", "EOS fit to energy", "Calculation"], **kw)

    # pressure on separete axes
    tax = ax.twinx()

    # plot EOS created from pressure fit
    _y = vinet_pressure(_x, *list(popt_p.values())[1:]) / GPa
    tax.plot(_x, _y, **kw_p, **kw_all)
    # plot EOS created from energy fit
    _y = vinet_pressure(_x, *list(popt_e.values())[1:]) / GPa
    tax.plot(_x, _y, **kw_e, **kw_all)
    # calculated pressures
    tax.plot(x, df.pressure / GPa, **kw_calc, **kw_all)

    # labels
    tax.set_ylabel("Pressure (GPa)")

    # arrows
    kw_arrow = dict(head_width=0.3, head_length=0.1, fc="k", ec="k", lw=1)
    ax.arrow(25, 8, -0.125, 0, **kw_arrow)
    ax.arrow(28, 2.5, 0.125, 0, **kw_arrow)

    # limits
    ax.set_ylim(0, 12)
    tax.set_ylim(-2.5, 2.5)

    # save plot
    if outfile is None:
        outfile = f"plot_{folder}_eos.pdf"
    echo(f"... save figure to {outfile}")
    fig.savefig(outfile, bbox_inches="tight")


if __name__ == "__main__":
    app()
