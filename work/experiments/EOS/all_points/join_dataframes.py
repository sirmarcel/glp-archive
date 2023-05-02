#! /usr/bin/env python3

from pathlib import Path
from typing import List

import pandas as pd
import typer
from rich import print as echo


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(
    files: List[Path],
    outfile: Path = "eos.csv",
):

    dfs = [pd.read_csv(file, comment="#", index_col="volume") for file in files]

    df = pd.concat(dfs).sort_index().drop_duplicates()

    echo(df)

    echo(f'... write to {outfile}')
    df.to_csv(outfile)




if __name__ == "__main__":
    app()
