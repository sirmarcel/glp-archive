from tbx import *


def get_data(suffix="32"):
    return load(
        work
        / f"experiments/implementation_stress_and_heat_flux/lj_mk04/results_{suffix}.npz"
    )


def get(suffix, key, prop="stress", component=None):
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

    if component is None:
        true = data[prop + "_reference"].flatten() * factor
        pred = data[prop + "_" + key].flatten() * factor

    else:
        if prop == "stress":
            true = data[prop + "_reference"][:, component[0], component[1]] * factor
            pred = data[prop + "_" + key][:, component[0], component[1]] * factor

    return true, pred


def get_time(prop, suffix, size=864, key=None, use_min=True):
    import yaml

    file = (
        work
        / f"experiments/time_stress_and_heat_flux/lj_mk04/{prop}_results_n{size}_{suffix}.yaml"
    )
    with open(file) as f:
        data = yaml.load(f.read())

    if use_min:
        d = {k: np.array(v).min() for k, v in data.items()}
    else:
        mins = {k: np.array(v).min() for k, v in data.items()}
        maxs = {k: np.array(v).max() for k, v in data.items()}

        d = {k: np.array((maxs[k] - mins[k]) / mins[k]) for k in data}

    if key is not None:
        if key == "fd":
            if suffix == "32":
                step = 1e-3
            elif suffix == "64":
                step = 1e-4

            key = f"finite_differences_{step:.0e}"

        return d[key]

    return d


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


def best(x):
    return r"\maxf{X}".replace("X", x)
