from shared import *
from tbx.tables import *

names = {
    # "atom_pair_textbook_mic": "",
    "strain_system": "10",
    "strain_graph": "11",
    "unfolded_strain_unfolded": "12",
    "strain_direct": "13",
    "atom_pair_direct": "14",
    "unfolded_direct_unfolded": "15",
}

titles = [
    "Equation",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
    r"\acs{mae} (\unit{eV})",
    r"\acs{mape} (\unit{\percent})",
]

idx_to_name = ["x", "y", "z"]

for L in [1, 2, 3]:
    for suffix in ["32", "64"]:
        overall = []

        for x in [0, 1, 2]:
            stress = []
            comps = [[x, 0], [x, 1], [x, 2]]

            for key, name in names.items():
                row = [name]
                for component in comps:
                    # for suffix in ["32", "64"]:
                    true, pred = get(suffix, key, prop="stress", component=component)

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

            # heading = (
            #     r"\multicolumn{1}{c}{}&\multicolumn{2}{c}{\textbf{Single}}&\multicolumn{2}{c}{\textbf{Double}}\\"
            #     + "\n"
            # )

            heading = (
                r""
                r"\multicolumn{1}{c}{}&\multicolumn{2}{c}{$\sigma_{XX}$}&\multicolumn{2}{c}{$\sigma_{YY}$}&\multicolumn{2}{c}{$\sigma_{ZZ}$}\\".replace(
                    "XX", f"{idx_to_name[x]}x"
                )
                .replace("YY", f"{idx_to_name[x]}y")
                .replace("ZZ", f"{idx_to_name[x]}z")
                + "\n"
            )

            tab = make_tabular(
                titles, stress, layout="l | r r | r r | r r ", heading=heading
            )
            overall.append(tab)
        savetab(
            "\n".join(overall),
            tables / f"snse_stress_error_components_M{L}_{suffix}.tex",
        )
        # print(tab)
