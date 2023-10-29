from shared import *


potential_config = {
    "lennard_jones": {
        "sigma": 3.405,
        "epsilon": 0.01042,
        "cutoff": 10.5,
        "onset": 9.0,
    }
}

calculator_configs = {
    # eq. 19
    "atom_pair_direct": {
        "atom_pair": {
            "skin": skin,
            "heat_flux": True,
            "convective": False,
        }
    },
    "hf_unfolded": {
        "heat_flux_unfolded": {
            "skin": skin,
            "skin_unfolder": skin_unfolder,
            "convective": False,
        }
    },
    "hf_hardy": {
        "heat_flux_hardy": {
            "skin": skin,
            "convective": False,
        }
    },
}

for x64 in [True, False]:
    initial, inputs, outfile = prepare(x64=x64)

    system, velocities, masses = initial

    things = {}

    for key, config in calculator_configs.items():
        print(f"setup {key}")
        fn = get_calculator(potential_config, config)

        calc, state = fn(system)
        calc_fn = jit(calc.calculate)
        _, state = calc_fn(system, state, velocities=velocities, masses=masses)

        things[key] = (calc_fn, state)

    results = {}

    for key, thing in things.items():
        print(f"time {key}")
        calc, state = thing
        start = monotonic()
        for inp in inputs:
            system, velocities, masses = inp
            res, state = calc(system, state, velocities=velocities, masses=masses)
            assert not state.overflow
            np.array(res["heat_flux"])

        end = monotonic()
        results[key] = (end - start) / n_samples

    for key, value in results.items():
        print(f"{key}: {value*1000:.1f}ms")

    with open("heat_flux_" + outfile, "w") as f:
        f.write(yaml.dump(results))
