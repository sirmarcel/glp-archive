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

titles = [
    "Eq.",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
    r"Time (\unit{\second\per atom})",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
    r"Time (\unit{\second\per atom})",
]


stress = []

for key, name in names.items():
    row = [name]
    for suffix in ["32", "64"]:
        true, pred = get(suffix, key, prop="stress")
        times = get_time("stress", suffix)

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            # r"\num{X}".replace("X", formatter(r2(true, pred))),
            # r"\num{X}".replace("X", formatter(maxae(true, pred))),
            r"\num{X}".replace("X", formatter(mape(true, pred))),
            # r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]
        row += losses
        if key != "fd":
            row += [r"\num{X}".replace("X", formatter(times[key]))]
        else:
            row += ["--"]

    stress.append(row)

heading = (
    r"\multicolumn{1}{c}{}&\multicolumn{3}{c}{\textbf{Single}}&\multicolumn{3}{c}{\textbf{Double}}\\" + "\n"
)

tab = make_tabular(titles, stress, layout="l | r r r | r r r", heading=heading)
savetab(tab, tables / f"lj_stress_error.tex")
print(tab)


names = {
    # "atom_pair_textbook_mic": "",
    "hf_hardy": r"\ref{eq:J_mic}",
    "atom_pair_direct": r"\ref{eq:j_virials}",
    "hf_unfolded": r"\ref{eq:j_unf}",
}

titles = [
    "Eq.",
    r"\acs{mae} (\unit{eV \angstrom \per fs})",
    # r"\acs{maxae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
    # r"\acs{maxape} (\unit{\percent})",
    r"\acs{mae} (\unit{eV \angstrom \per fs})",
    r"\acs{mape} (\unit{\percent})",
]


heat_flux = []

for key, name in names.items():
    row = [name]
    for suffix in ["32", "64"]:
        true, pred = get(suffix, key, prop="heat_flux")

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            # r"\num{X}".replace("X", formatter(maxae(true, pred))),
            r"\num{X}".replace("X", formatter(mape(true, pred))),
            # r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]

        row += losses

    heat_flux.append(row)

heading = (
    r"\multicolumn{1}{c}{}&\multicolumn{2}{c}{\textbf{Single}}&\multicolumn{2}{c}{\textbf{Double}}\\" + "\n"
)

tab = make_tabular(titles, heat_flux, layout="l | r r | r r", heading=heading)
savetab(tab, tables / f"lj_heat_flux_error.tex")
print(tab)
