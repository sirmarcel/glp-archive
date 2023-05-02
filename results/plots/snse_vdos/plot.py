from tbx import *
from scipy.signal import find_peaks
from scipy.integrate import trapz
from itertools import cycle

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


def rc(cutoff):
    if not develop:
        return r"$r_{\text{c}}=\SI{X}{\angstrom}$".replace("X", f"{cutoff:.1f}")
    else:
        return f"$r_c = {cutoff:.1f}$Å"


def plot_vdos(
    ax, vdos, color=black, offset=0.0, label="__nolabel__", linestyle=solid, alpha=1
):
    integral = trapz(np.asarray(vdos.fillna(0.0)), dx=0.01)

    vdos /= integral
    vdos *= 8

    (vdos + offset).plot(
        ax=ax, color=color, label=label, linewidth=3, linestyle=linestyle, alpha=alpha
    )

    # ax.text(4.2, offset + 0.18, label, fontsize="medium")


def plot_peaks(ax, vdos, color=black, prominence=0.08):
    peaks, _ = find_peaks(vdos, prominence=prominence)
    for p in peaks:
        ax.axvline(vdos.omega.isel(omega=p), color=color, alpha=0.4, linewidth=1)


aims = load(results / "snse_vdos/aims.nc")
sokrates_l1 = load(results / "snse_vdos/default_L1.nc")
sokrates_l2 = load(results / "snse_vdos/default_L2.nc")
sokrates_l3 = load(results / "snse_vdos/default_L3.nc")

fig, ax = fig_and_ax(figsize=(colwidth, 4))

prominence = 0.45

plot_peaks(ax, aims.fourier_transform, color=black, prominence=prominence)
plot_vdos(ax, aims.fourier_transform, label="FHI-aims", color=black)

plot_vdos(
    ax,
    sokrates_l1.fourier_transform,
    color=teal,
    linestyle=dashdot,
    offset=0,
    label=r"$M{=}1$",
    alpha=0.8,
)
plot_vdos(
    ax,
    sokrates_l2.fourier_transform,
    color=blue,
    linestyle=finedot,
    offset=0,
    label=r"$M{=}2$",
    alpha=0.8,
)
plot_vdos(
    ax,
    sokrates_l3.fourier_transform,
    color=red,
    linestyle=finedash,
    offset=0,
    label=r"$M{=}3$",
    alpha=0.8,
)


ax.set_xlim(0, 7.5)
ax.set_ylabel("Intensity")
ax.set_xlabel("Frequency (THz)")

ax.yaxis.set_major_locator(plt.NullLocator())

ax.legend(loc="upper right", handlelength=3.5)

savefig(fig, f"preview.png")
savefig(fig, img / "si-snse_vdos.pdf")
