from ase.io import read
from unfolder_engine import get_unfolding

from tbx import *
from tbx.tables import *

primitive = read("geometry.in.primitive", format="aims")

t = []
for multiplier in range(2, 15):
    atoms = primitive * [multiplier, multiplier * 2, multiplier * 2]
    row = []
    for m in [1, 2, 3]:

        idx, directions = get_unfolding(
            atoms.get_positions(), atoms.get_cell().array, m * 5.0
        )

        N = len(atoms)
        Nextra = len(idx)
        Nunf = N + Nextra

        print(f"{N:6d}: {Nextra:6d} {Nunf/N:.1f}")
        row += [to_num(N), to_num(Nextra), to_num(Nunf), to_num(rounder(1)(Nunf / N)) + r"$\times$"]
    t.append(row)

header = (
    r"\multicolumn{4}{c}{$\interactions = 1\quad \effcutoff = \qty{5}{\angstrom}$}&\multicolumn{4}{c}{$\interactions = 2\quad \effcutoff = \qty{10}{\angstrom}$}&\multicolumn{4}{c}{$\interactions = 3\quad \effcutoff = \qty{15}{\angstrom}$}\\"
    + "\n"
)
title = [r"$N$", r"$+\,\,\, N_{\text{add}}$", r"$=\,\, N_{\text{unf}}$", "Factor"] * 3

tab = make_tabular(title, t, layout="r r r r | r r r r | r r r r", heading=header)
savetab(tab, tables / f"snse_additional_positions.tex")
print(tab)
