#! /usr/bin/env python3

import json
import warnings
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import typer
from matplotlib import pyplot as plt
from rich import print as echo

warnings.simplefilter("ignore")


plt.style.use("glp.mplstyle")

colors = ["#313131", "teal", "C0", "C3"]
linestyles = ["-", "--", "--", "-"]
markers = ["o", "s", "d", "D"]
linewidths = [2, 1, 1, 1.5]


def vinet(V, E0, B0, BP, V0):
    "Vinet equation from PRB 70, 224107"

    X = (V / V0) ** (1 / 3)
    eta = 3 / 2 * (BP - 1)

    E = E0 + 2 * B0 * V0 / (BP - 1) ** 2 * (
        2 - (5 + 3 * BP * (X - 1) - 3 * X) * np.exp(-eta * (X - 1))
    )
    return E


def no_ticks(ax, direction="x"):
    if direction == "x":
        ax.xaxis.set_major_locator(plt.NullLocator())
    else:
        ax.yaxis.set_major_locator(plt.NullLocator())


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(
    folders: List[Path],
    file_data: Path = "eos.csv",
    file_fit: Path = "eos_e.json",
    outfile: Path = "plot_eos_comparison.pdf",
):
    # create canvas
    fig, ax = plt.subplots(figsize=(6, 4))

    kw = {"color": "#313131", "lw": 1, "ls": ":"}
    x1, x2 = 26.478425, 27.002756  # training volumes
    ax.axvline(x1, **kw)
    ax.axvline(x2, **kw)
    ax.fill_betweenx([0, 100], x1, x2, color="#D3D3D3")
    ax.text((x1 + x2) / 2, 12.3, "Training", ha="center", va="bottom")

    ax.set_ylim(0, 12.2)
    ax.set_xlim(24.75, 28.5)
    ax.set_xlabel(r"Volume per atom (${\rm \AA}^3$)")
    ax.set_ylabel(r"Energy per atom (meV)")

    # inset
    axins = ax.inset_axes([0.2, 0.475, 0.5, 0.5])
    axins.set_xlim(x1, x2)
    axins.set_ylim(0, 1.5)
    axins.set_xlabel(None)
    axins.set_ylabel(None)
    no_ticks(axins, direction="x")
    no_ticks(axins, direction="y")
    ax.indicate_inset_zoom(axins, edgecolor="k", alpha=1, linewidth=2)
    axins.fill_betweenx([0, 100], x1, x2, color="#D3D3D3")
    for spine in axins.spines:
        axins.spines[spine].set_color("k")

    # main plot
    for ii, folder in enumerate(folders):

        file = folder / file_data

        echo(f"... read {file}")
        df = pd.read_csv(file, comment="#", index_col="volume")

        # read EOS parameters
        popt_e = json.load(open(folder / file_fit))

        x = df.index / df.N
        y = df.energy / df.N

        E0 = popt_e["E0"]

        c = colors[ii]
        ls = linestyles[ii]
        _x = np.linspace(x.min(), x.max(), 51)
        # energy via EOS
        _y = 1e3 * (vinet(_x, *popt_e.values()) - E0)
        ax.plot(_x, _y, lw=linewidths[ii], c=c, ls=ls, clip_on=False)
        axins.plot(_x, _y, lw=linewidths[ii], c=c, ls=ls, clip_on=True)
        # calculated values
        _y = 1e3 * (y - E0)
        marker = markers[ii]
        ax.plot(x, _y, marker=marker, c=c, lw=0, ms=5, clip_on=False)
        axins.plot(x, _y, marker=marker, c=c, lw=0, ms=6, clip_on=True)

    # legend
    kw = {"loc": 4, "frameon": False, "markerfirst": False}
    legend = 9 * [
        "_",
    ]
    legend += ["DFT", "_", "$M=1$", "_", "$M=2$", "_", "$M=3$"]
    ax.legend(legend, **kw)

    echo(f"... save figure to {outfile}")
    fig.savefig(outfile)


if __name__ == "__main__":
    app()
