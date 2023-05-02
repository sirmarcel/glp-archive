from shared import *
from ase.stress import full_3x3_to_voigt_6_stress


for suffix in ["32", "64"]:
    fig, ax = fig_and_ax(figsize=(0.95 * colwidth, 4))

    ds = np.logspace(-6, -2, num=5 + 2 * 4, base=10)

    y = [mae(*get(suffix, f"finite_differences_{d:.0e}", prop="stress")) for d in ds]

    ax.plot(ds, y, marker=star, color=black, markersize=15)

    ax.set_ylabel("MAE in eV")
    ax.set_xlabel(r"Step size in \unit{\angstrom}")

    ax.set_xscale("log", base=10)

    ax.set_xticks(ds)
    ax.set_xticklabels([f"{d:.0e}" for d in ds])

    ax.set_yscale("log", base=10)
    ax.set_xlim(0.9e-6, 1.1e-2)

    m = np.argmin(y)
    ax.plot(ds[m], y[m], color=red, marker=star, markersize=18)
    savefig(fig, f"fd/convergence_{suffix}_vs_error.png")
    # savefig(fig, img / f"gk/si-lj_stress_fd_convergence_{suffix}.pdf")

for suffix in ["32", "64"]:
    fig, ax = fig_and_ax(figsize=(0.95 * colwidth, 4))

    ds = np.logspace(-6, -2, num=5 + 2 * 4, base=10)

    y = [
        full_3x3_to_voigt_6_stress(
            get_data(suffix=suffix)[f"stress_finite_differences_{d:.0e}"]
        )[0]
        for d in ds
    ]
    y = np.array(y)

    from IPython import embed
    
    # embed()

    for i in range(6):
        ax.plot(ds, y[:, i], marker=star, color=black, markersize=15)

    # ax.set_ylabel("MAE in eV")
    # ax.set_xlabel(r"Step size in \unit{\angstrom}")

    ax.set_xscale("log", base=10)

    # ax.set_xticks(ds)
    # ax.set_xticklabels([f"{d:.0e}" for d in ds])

    # ax.set_yscale("log", base=10)
    # ax.set_xlim(0.9e-6, 1.1e-2)

    # m = np.argmin(y)
    # ax.plot(ds[m], y[m], color=red, marker=star, markersize=18)
    savefig(fig, f"fd/convergence_{suffix}_values.png")
    # savefig(fig, img / f"gk/si-lj_stress_fd_convergence_{suffix}.pdf")
