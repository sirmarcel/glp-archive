## model gallery

collect the (main) models used in the present work for later reference.

## Production models

commit: fb6a42c9e5c0c029c567eff0c74cda2eba33c319

`train_default_L2`:

- training with default parameters, but L=2

`train_default_L3`:

- training with default parameters, i.e., L=3

## Training data

- `mlff_data.npz`: The original training data from NVT runs **including the legacy volume scaling for the stress**

- `mlff_data_wo_stress_scaling.npz`: updated data **without volume scaling**

I.e. when training without stress there should be no difference, I included both just to be sure.
