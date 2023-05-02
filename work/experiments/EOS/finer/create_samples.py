#! /usr/bin/env python3

import shutil
from pathlib import Path

import numpy as np
import typer
from ase.io import read
from rich import print as echo

app = typer.Typer(pretty_exceptions_show_locals=False)

strains = np.linspace(0.99, 1.01, 21)


@app.command()
def main(
    file_geometry: str = "geometry.in",
    file_relaxation: Path = "relaxation.in",
    replicas: int = 1,
    base_folder: Path = "eos",
    format: str = "aims",
):

    echo(f"... use {replicas} replicas")

    atoms = read(file_geometry, format=format) * [replicas, replicas, replicas]

    base_folder.mkdir(exist_ok=True)

    for ii, strain in enumerate(strains):
        echo(f"... strain: {strain}")
        cell = atoms.cell * strain
        watoms = atoms.copy()
        watoms.set_cell(cell, scale_atoms=True)

        folder = base_folder / f"{ii:03d}"
        folder.mkdir(exist_ok=True)

        outfile = folder / file_geometry

        echo(f"... write file to {outfile}")
        watoms.write(outfile, format=format)

        outfile = folder / file_relaxation

        echo(f"... copy {file_relaxation} to {outfile}")
        shutil.copyfile(file_relaxation, outfile)

    echo("done.")


if __name__ == "__main__":
    app()
