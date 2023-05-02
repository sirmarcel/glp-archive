#! /usr/bin/env python3

import warnings
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import typer
from matplotlib import pyplot as plt
from rich import print as echo
from scipy.optimize import curve_fit


# Vinet EOS


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


# Reasonable bounds


colors = ["#313131", "teal", "C0", "C3"]
linestyles = ["-", "--", "--", "-"]
markers = ["o", "s", "d", "D"]
linewidths = [3, 1.5, 1.5, 2]


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(
    files: List[Path],
    outfile: Path = "plot_eos_comparison_zoom.pdf",
):

    fig, ax = plt.subplots(figsize=(6, 4))

    for ii, file in enumerate(files):
        echo(file)
        df = pd.read_csv(file, comment="#", index_col="volume")

        x = df.index  # np.linspace(df.index.min(), df.index.max(), 51)
        y = df.energy
        y0 = y.min()

        bounds = ([-1, 0, -10, 0], [1, 5, 10, 1000])

        popt_e, _ = curve_fit(vinet, x, y - y0, bounds=bounds)
        echo(popt_e)

        bounds = ([0, -10, 0], [5, 10, 1000])
        popt_p, _ = curve_fit(vinet_pressure, df.index, df.pressure, bounds=bounds)
        # echo(popt_p)

        E0 = popt_e[0]

        c = colors[ii]
        ls = linestyles[ii]
        x = np.linspace(df.index.min(), df.index.max(), 51)
        y = vinet(x, *popt_e) / df.N.mean()
        ax.plot(x / df.N.mean(), 1e3 * y, lw=linewidths[ii], c=c, ls=ls, clip_on=True)
        # y = vinet(x, -E0, *popt_p)
        # ax.plot(x / df.N.mean(), 1e3 * y, lw=linewidths[ii]/2, c=c, ls='-', clip_on=True)
        # y = vinet(x, E0, *popt_p)
        # ax.plot(
        #     x / df.N.mean(), 1e3 * y, lw=1, c="k", ls='-', clip_on=True
        # )
        # ax.plot(x, vinet(x, E0, *popt_p), lw=4, ls="--", c=c)
        x = df.index
        y = (df.energy - df.energy.min() + E0) / df.N.mean()
        marker = markers[ii]
        ax.plot(x / df.N, 1e3 * y, marker=marker, c=c, lw=0, ms=7, clip_on=True)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        kw = {"loc": 4, "frameon": False, "markerfirst": False}
        legend = ["_", "DFT", "_", "L=1", "_", "L=2", "_", "L=3"]
        # legend = []
        # for file in files:
        #     legend.extend([file.parent, "_"])
        ax.legend(legend, **kw)

    # ax.legend(["EOS fit to energy", "EOS fit to pressure", "calculation", "DFT"])

    # training
    kw = {"color": "#313131", "lw": 1, "ls": ":"}
    # xlim = 10
    x1, x2 = 26.478425, 27.002756
    ax.axvline(x1, **kw)
    ax.axvline(x2, **kw)
    ax.fill_betweenx([0, 100], x1, x2, alpha=0.3, color="#313131")
    # ax.text(x1, 101.0, "Training", ha="left", va="bottom")

    # ax.set_ylim(0, 100)
    # ax.set_xlim(24.75, 28.5)

    ax.set_ylim(0, 1.5)
    ax.set_xlim(x1, x2)

    ax.set_xlabel(r"Volume per atom (${\rm \AA}^3$)")
    ax.set_ylabel(r"Energy per atom (meV)")

    echo(f"... save figure to {outfile}")
    fig.savefig(outfile)


if __name__ == "__main__":
    app()
