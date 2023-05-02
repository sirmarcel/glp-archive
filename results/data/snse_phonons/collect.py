import sys

sys.path.insert(0, "../../")

from tbx import *

from vibes.phonopy.postprocess import postprocess
from vibes.phonopy.wrapper import set_bandstructure


def get_phonons(folder, suffix="trajectory.son"):
    phonons = postprocess(folder / suffix, enforce_sum_rules=False)

    set_bandstructure(phonons)

    q_mesh = [45, 45, 45]
    phonons.run_mesh(q_mesh)
    phonons.run_total_dos(use_tetrahedron_method=True)

    return {
        "bs_all_distances": np.array(phonons._band_structure._distances),
        "bs_all_frequencies": np.array(phonons._band_structure._frequencies),
        "bs_labels": np.array(phonons._band_structure._labels),
        "bs_special_points": np.array(phonons._band_structure._special_points),
        "dos_frequency_points": np.array(phonons._total_dos._frequency_points),
        "dos_total_dos": np.array(phonons._total_dos._dos),
    }



np.savez_compressed(
    f"default_L1_256.npz",
    **get_phonons(
        work_remote
        / "runs/snse/production_models_train_default_L1/phonons/phonons_256/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"default_L2_256.npz",
    **get_phonons(
        work_remote
        / "runs/snse/production_models_train_default_L2/phonons/phonons_256/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"default_L3_256.npz",
    **get_phonons(
        work_remote
        / "runs/snse/production_models_train_default_L3/phonons/phonons_256/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"tf_1_m2_256.npz",
    **get_phonons(
        work_remote
        / "runs/snse/tf_models_model_1_m2/phonons/phonons_256/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"aims_256.npz",
    **get_phonons(work_remote / "runs/snse/reference/", suffix="phonons.son"),
)


# np.savez_compressed(
#     f"aims_256_previous.npz",
#     **get_phonons(
#         work_remote / "runs/snse/reference/", suffix="phonons_previously.son"
#     ),
# )


# np.savez_compressed(
#     f"aims_256_2010_basis.npz",
#     **get_phonons(
#         work_remote / "runs/snse/reference/", suffix="phonons_2010_basis.son"
#     ),
# )

# np.savez_compressed(
#     f"aims_256_current_light_default.npz",
#     **get_phonons(
#         work_remote / "runs/snse/reference/", suffix="phonons_current_light_default.son"
#     ),
# )

