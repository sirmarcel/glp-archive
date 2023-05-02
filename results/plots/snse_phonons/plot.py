from tbx import *
from tbx.phonons import *

datadir = results / "snse_phonons"


n = 256

aims = load(datadir / f"aims_{n}.npz")
sokrates_l1 = load(datadir / f"default_L1_{n}.npz")
sokrates_l2 = load(datadir / f"default_L2_{n}.npz")
sokrates_l3 = load(datadir / f"default_L3_{n}.npz")
sokrates_old_m2 = load(datadir / f"tf_1_m2_{n}.npz")


# fig, ax = plt.subplots(
#     nrows=1,
#     ncols=2,
#     gridspec_kw={"width_ratios": [3, 1]},
#     sharey=True,
#     figsize=(0.95 * colwidth, 4),
#     dpi=200,
# )
# # fig, ax = fig_and_ax(figsize=(0.7 * textwidth, textheight))

# setup(ax, aims, lim_bs=(-0.1, 6))
# plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
# plot(ax, sokrates_l2, color=red, linestyle=solid, label="so3krates")
# fig.legend(loc="upper center", ncol=3)

# savefig(fig, "preview_l2.png")
# savefig(fig, img / "si-snse_phonons_l2.pdf")


# fig, ax = plt.subplots(
#     nrows=1,
#     ncols=2,
#     gridspec_kw={"width_ratios": [3, 1]},
#     sharey=True,
#     figsize=(0.95 * colwidth, 4),
#     dpi=200,
# )
# # fig, ax = fig_and_ax(figsize=(0.7 * textwidth, textheight))

# setup(ax, aims, lim_bs=(-0.1, 6))
# plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
# plot(ax, sokrates_old_m2, color=red, linestyle=solid, label="so3krates")
# fig.legend(loc="upper center", ncol=3)

# savefig(fig, "preview_previous_l2.png")
# # savefig(fig, img / "gk/snse_phonons.pdf")


# fig, ax = plt.subplots(
#     nrows=1,
#     ncols=2,
#     gridspec_kw={"width_ratios": [3, 1]},
#     sharey=True,
#     figsize=(0.95 * colwidth, 4),
#     dpi=200,
# )
# # fig, ax = fig_and_ax(figsize=(0.7 * textwidth, textheight))

# setup(ax, aims, lim_bs=(-0.1, 6))
# plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
# plot(ax, sokrates_l3, color=red, linestyle=solid, label="so3krates")
# fig.legend(loc="upper center", ncol=3)

# savefig(fig, "preview_l3.png")
# savefig(fig, img / "si-snse_phonons_l3.pdf")


fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    gridspec_kw={"width_ratios": [3, 1]},
    sharey=True,
    figsize=(0.95 * colwidth, 4.5),
    dpi=200,
)
# fig, ax = fig_and_ax(figsize=(0.7 * textwidth, textheight))

setup(ax, aims, lim_bs=(-0.1, 6))
plot(ax, aims, color=black, linestyle=solid, label="FHI-aims", alpha=1, linewidth=2)
plot(
    ax,
    sokrates_l1,
    color=teal,
    linestyle=dashdot,
    label=r"$M{=}1$",
    alpha=0.75,
    linewidth=2,
)
plot(
    ax,
    sokrates_l2,
    color=blue,
    linestyle=finedot,
    label=r"$M{=}2$",
    alpha=0.75,
    linewidth=2,
)
plot(
    ax,
    sokrates_l3,
    color=red,
    linestyle=finedash,
    label=r"$M{=}3$",
    alpha=0.75,
    linewidth=2,
)

fig.legend(loc="upper center", ncol=4, handlelength=3.0)

for label in ax[0].get_xticklabels():
    if "|" in label.get_text():
        label.set_rotation(90)
    else:
        label.set_rotation(0)


savefig(fig, "preview.png")
savefig(fig, img / "si-snse_phonons.pdf")

# from IPython import embed

# embed()
