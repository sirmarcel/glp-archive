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

for suffix, s in settings.items():
    print(f"#### {suffix} bits")

    data = get_data(suffix=suffix)

    fd = s["fd"]

    names = {
        # "atom_pair_textbook_mic": "",
        f"finite_differences_{fd:.0e}": "Fin. diff.",
        "direct_strain_system": r"\ref{eq:glp_stress_strain_direct}",
        "direct_strain_graph": r"\ref{eq:glp_stress_strain_edges}",
        "unfolded_system": r"\ref{eq:glp_stress_strain_unf}",
        "direct_strain_direct": r"\ref{eq:glp_stress_sc_basis}",
        "atom_pair_fractional_mic": r"\ref{eq:glp_stress_edges}",
        "unfolded_unfolded": r"\ref{eq:glp_stress_bulk}",
    }

    titles = [
        "Equation",
        r"\acs{mae} in \unit{eV}",
        r"\acs{mape} in \unit{\percent}",
        # r"\acs{cod} in \unit{\percent}",
        # r"\acs{maxape} in \unit{\percent}",
    ]


    stress = []

    for key, name in names.items():
        true, pred = get(data, key, prop="stress")
        if "finite_differences" not in key:
            assert pred.dtype == s["dtype"]

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            # r"\num{X}".replace("X", formatter(r2(true, pred))),
            # r"\num{X}".replace("X", formatter(maxae(true, pred))),
            r"\num{X}".replace("X", formatter(mape(true, pred))),
            # r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]

        stress.append([name, *losses])

    tab = make_tabular(titles, stress, layout="l | r r ")
    savetab(tab, tables / f"lj_stress_error_{suffix}.tex")
    print(tab)


    names = {
        # "atom_pair_textbook_mic": "",
        "atom_pair_fractional_mic": "atom_pair_fractional_mic",
        "atom_pair_textbook_mic": "atom_pair_textbook_mic",
        "hf_unfolded": "hf_unfolded",
        "hf_hardy": "hf_hardy",
    }

    titles = [
        "Equation",
        r"\acs{mae} in \unit{eV}",
        # r"\acs{maxae} in \unit{eV}",
        r"\acs{mape} in \unit{\percent}",
        # r"\acs{maxape} in \unit{\percent}",
    ]


    heat_flux = []

    for key, name in names.items():
        true, pred = get(data, key, prop="heat_flux")
        if "finite_differences" not in key:
            assert pred.dtype == s["dtype"]

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            # r"\num{X}".replace("X", formatter(maxae(true, pred))),
            r"\num{X}".replace("X", formatter(mape(true, pred))),
            # r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]

        heat_flux.append([name, *losses])

    tab = make_tabular(titles, heat_flux, layout="l | r r ")
    savetab(tab, tables / f"lj_heat_flux_error_{suffix}.tex")
    print(tab)
