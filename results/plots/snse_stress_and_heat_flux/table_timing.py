from shared import *
from tbx.tables import *

from shared import *
from tbx.tables import *

settings = {
    "32": {
        "fd": 1e-3,
        "dtype": np.float32,
    },
    "64": {
        "fd": 1e-4,
        "dtype": np.float64,
    },
}


names = {
    # "atom_pair_textbook_mic": "",
    "fd": "F.d.",
    "strain_system": r"\ref{eq:glp_stress_strain_direct}",
    "strain_graph": r"\ref{eq:glp_stress_strain_edges}",
    "unfolded_strain_unfolded": r"\ref{eq:glp_stress_strain_unf}",
    "strain_direct": r"\ref{eq:glp_stress_sc_basis}",
    "atom_pair_direct": r"\ref{eq:glp_stress_edges}",
    "unfolded_direct_unfolded": r"\ref{eq:glp_stress_bulk}",
}

explicit_names = {
    "fd": "F.d.",
    "strain_system": r"10",
    "strain_graph": r"11",
    "unfolded_strain_unfolded": r"12",
    "strain_direct": r"13",
    "atom_pair_direct": r"14",
    "unfolded_direct_unfolded": r"15",
}


titles = [
    "Eq.",
    r"$N{=}864$",
    r"$N{=}2048$",
    r"$N{=}4000$",
    r"$N{=}864$",
    r"$N{=}2048$",
    r"$N{=}4000$",
]

formatter = rounder(1, typ="e")

for L in [1, 2, 3]:
    stress = []
    for key, name in names.items():
        if L == 2:
            row = [name]
        else:
            row = [explicit_names[key]]
        for suffix in ["32", "64"]:
            for size in [864, 2048, 4000]:
                if L == 3 and size == 4000:
                    row += ["--"]
                    continue

                times = get_time("stress", suffix, size=size, key=key, L=L)
                row += [to_num(formatter(times))]

        stress.append(row)

    heading = (
        r"\multicolumn{1}{c}{}&\multicolumn{3}{c}{\textbf{Single}}&\multicolumn{3}{c}{\textbf{Double}}\\"
        r"\multicolumn{1}{c}{}&\multicolumn{3}{c}{Time per atom (s)}&\multicolumn{3}{c}{Time per atom (s)}\\"
        + "\n"
    )

    tab = make_tabular(titles, stress, layout="l | rrr | rrr", heading=heading)
    savetab(tab, tables / f"snse_stress_times_M{L}.tex")
    print(tab)
