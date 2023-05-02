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
    # "fd": "Fin. diff.",
    "strain_system": r"\ref{eq:glp_stress_strain_direct}",
    "strain_graph": r"\ref{eq:glp_stress_strain_edges}",
    "unfolded_strain_unfolded": r"\ref{eq:glp_stress_strain_unf}",
    "strain_direct": r"\ref{eq:glp_stress_sc_basis}",
    "atom_pair_direct": r"\ref{eq:glp_stress_edges}",
    "unfolded_direct_unfolded": r"\ref{eq:glp_stress_bulk}",
}

titles = [
    "Equation",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
]

for L in ["1", "2", "3"]:
    stress = []

    for key, name in names.items():
        row = [name]
        for suffix in ["32", "64"]:
            true, pred = get(suffix, key, prop="stress", L=L)

            formatter = rounder(2, typ="e")
            losses = [
                r"\num{X}".replace("X", formatter(mae(true, pred))),
                # r"\num{X}".replace("X", formatter(r2(true, pred))),
                # r"\num{X}".replace("X", formatter(maxae(true, pred))),
                r"\num{X}".replace("X", formatter(mape(true, pred))),
                # r"\num{X}".replace("X", formatter(maxape(true, pred))),
            ]
            row += losses

        stress.append(row)

    heading = (
        r"\multicolumn{1}{c}{}&\multicolumn{2}{c}{\textbf{Single}}&\multicolumn{2}{c}{\textbf{Double}}\\" + "\n"
    )

    tab = make_tabular(titles, stress, layout="l | r r | r r", heading=heading)
    if L == "2":
        savetab(tab, tables / f"snse_stress_error.tex")
    else:
        for i, name in enumerate(names.values()):
            tab = tab.replace(name, str(10+i))

        savetab(tab, tables / f"si-snse_stress_error_m{L}.tex")
    print(tab)


names = {
    # "atom_pair_textbook_mic": "",
    "atom_pair_direct": r"\ref{eq:j_virials}",
    "hf_unfolded": r"\ref{eq:j_unf}",
    # "hf_hardy": r"\ref{eq:hf_jfull}",
}

titles = [
    "Eq.",
    r"$\interactions$",
    r"\acs{mae} (\unit{eV \angstrom \per fs})",
    # r"\acs{maxae} in \unit{eV}",
    r"\acs{mape} (\unit{\percent})",
    # r"\acs{maxape} in \unit{\percent}",
    r"\acs{mae} (\unit{eV \angstrom \per fs})",
    r"\acs{mape} (\unit{\percent})",
]

tables_hf = []
for L in ["1", "2", "3"]:
    heat_flux = []
    for key, name in names.items():
        row = [name, r"$X$".replace("X", L)]
        for suffix in ["32", "64"]:
            true, pred = get(suffix, key, prop="heat_flux", L=L)

            formatter = rounder(2, typ="e")
            losses = [
                r"\num{X}".replace("X", formatter(mae(true, pred))),
                # r"\num{X}".replace("X", formatter(maxae(true, pred))),
                r"\num{X}".replace("X", formatter(mape(true, pred))),
                # r"\num{X}".replace("X", formatter(maxape(true, pred))),
            ]

            row += losses

        heat_flux.append(row)
    tables_hf.append(heat_flux)

heading = (
    r"\multicolumn{2}{c}{}&\multicolumn{2}{c}{\textbf{Single}}&\multicolumn{2}{c}{\textbf{Double}}\\" + "\n"
)

tab = make_tabular(titles, None, layout="l l | r r | r r", heading=heading, tables=tables_hf)
savetab(tab, tables / f"snse_heat_flux_error.tex")
print(tab)
