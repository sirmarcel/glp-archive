from tbx import *


def get_data(suffix="32"):
    return load(
        work
        / f"experiments/implementation_stress_and_heat_flux/lj_mk04/results_{suffix}.npz"
    )


def get(suffix, key, prop="stress"):
    data = get_data(suffix=suffix)
    if key == "fd":
        if suffix == "32":
            d = 1e-3
        elif suffix == "64":
            d = 1e-4

        key = f"finite_differences_{d:.0e}"

    if prop == "heat_flux":
        from ase.units import fs
        factor = fs
    else:
        factor = 1

    true = data[prop + "_reference"].flatten() * factor
    pred = data[prop + "_" + key].flatten() * factor

    return true, pred


def mae(true, pred):
    return np.mean(np.abs(true - pred))


def maxae(true, pred):
    return np.max(np.abs(true - pred))


def ape(true, pred):
    return np.abs((true - pred) / pred)


def mape(true, pred):
    return 100 * np.mean(ape(true, pred))


def maxape(true, pred):
    return 100 * np.max(ape(true, pred))


def r2(true, pred):
    mean = np.mean(true)
    sum_of_squares = np.sum((true - mean) ** 2)
    sum_of_residuals = np.sum((true - pred) ** 2)

    return 100 * (1.0 - (sum_of_residuals / sum_of_squares))
