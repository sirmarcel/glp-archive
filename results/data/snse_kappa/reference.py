import numpy as np

# taking the isotropic averages and averages of ranges
experiments = {
    "zhao": (0.47 + 2 * 0.7) / 3,
    "wasscher": 1.9,
    "chen": 1.1,
    "sassi": (0.7 + 1.2) / 2,
    "zhang": 0.9,
    "wei": 1.3,
    "li": (0.9 + 1.2) / 2,
    "leng": (0.7 + 0.9) / 2,
    "han": (0.7 + 1.1) / 2,
    "spitzer": 1.8,
}

brorsson = [0.571, 1.464, 1.321]

# choosing the 10x10x4 results
liu = [0.57, 1.25, 0.76]
liu_errors = [0.05, 0.24, 0.08]

knoop = 1.403515652
knoop_errors = 0.3823255076

data = {
    **experiments,
    "brorsson": brorsson,
    "liu": liu,
    "liu_errors": liu_errors,
    "knoop": knoop,
    "knoop_errors": knoop_errors,
}

np.savez_compressed("reference.npz", **data)
