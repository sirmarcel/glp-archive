from tbx import *

data = xr.open_dataset(results / "snse_kappa_convergence_N_t/production_models_train_default_L2.nc")
data_l1 = xr.open_dataset(results / "snse_kappa_convergence_N_t/production_models_train_default_L1.nc")
data_l3 = xr.open_dataset(results / "snse_kappa_convergence_N_t/production_models_train_default_L3.nc")




def show_single_point(ax, data, choice, highlight=False, **kwargs):
    n, m = choice
    d = data.sel(n_atoms=n, maxsteps=m)
    k = d.kappa_mean
    e = d.kappa_stderr

    base_position = ls[list(ns).index(n)]
    position = base_position - start + distance * list(maxstepss).index(m)
    _, _, bars = ax.errorbar(
        position,
        [k.data],
        linewidth=0,
        markeredgecolor=black,
        **kwargs,
    )
    if highlight:
        ax.fill_between(
            [0, 50], [k - e] * 2, [k + e] * 2, alpha=0.35, color=kwargs["color"]
        )


production = (864, 500000)
semi = (768, 125000)

fig, ax = fig_and_ax(figsize=(0.95 * colwidth, 4))

ns = data.n_atoms.data
ls = ns ** (1 / 3)
maxstepss = data.maxsteps.data[1::2]

distance = 0.1  # distance between labels
start = ((len(maxstepss) - 1) * distance) / 2

for i_n, n in enumerate(ns):
    base_position = ls[i_n]

    d = data.sel(n_atoms=n).sel(maxsteps=maxstepss)
    k = d.kappa_mean
    e = d.kappa_stderr

    _, _, bars = ax.errorbar(
        (base_position - start) + distance * np.arange(len(maxstepss)),
        k.data,
        yerr=e.data,
        color=black,
        elinewidth=2.0,
        linewidth=3,
        label=nolabel,
    )

    for bar in bars:
        bar.set_alpha(0.4)

    # if n in data_l1.n_atoms.data:
    #     d = data_l1.sel(n_atoms=n).sel(maxsteps=maxstepss)
    #     k = d.kappa_mean
    #     e = d.kappa_stderr

    #     _, _, bars = ax.errorbar(
    #         (base_position - start) + distance * np.arange(len(maxstepss)),
    #         k.data,
    #         yerr=e.data,
    #         color=teal,
    #         elinewidth=2.0,
    #         linewidth=3,
    #         label=nolabel,
    #     )

    # if n in data_l3.n_atoms.data:
    #     d = data_l3.sel(n_atoms=n).sel(maxsteps=maxstepss)
    #     k = d.kappa_mean
    #     e = d.kappa_stderr

    #     _, _, bars = ax.errorbar(
    #         (base_position - start) + distance * np.arange(len(maxstepss)),
    #         k.data,
    #         yerr=e.data,
    #         color=blue,
    #         elinewidth=2.0,
    #         linewidth=3,
    #         label=nolabel,
    #     )


show_single_point(
    ax,
    data,
    (production),
    highlight=True,
    color=red,
    marker=star,
    markersize=11,
    label="Production",
)
# show_single_point(
#     ax,
#     data,
#     semi,
#     highlight=False,
#     color=teal,
#     marker=thiamond,
#     markersize=11,
#     label="Light",
# )

ax.set_xticks(ls)
ax.set_xticklabels(list(map(str, ns)))
ax.set_xlabel("Number of atoms ($N^{1/3}$) (offset for simulation time $t$)")
ax.set_xlim(3.0, 18.5)

ax.set_ylabel(kappa_label())
ax.set_ylim(0, 2)

ax.legend(loc="lower right", ncol=2)
# ax.set_title(render_temp(temp))

# plt.subplots_adjust(hspace=0.40)
savefig(fig, "preview.png")
savefig(fig, img / "si-snse_kappa_convergence.pdf")
