# `glp-archive`
## Code and Data for "Stress and heat flux with automatic differentiation"

This repository contains data, code, and related artefacts supporting the following publication ([preprint](https://arxiv.org/abs/2305.01401):

```
Stress and heat flux via automatic differentiation
by Marcel F. Langer, J. Thorben Frank, and Florian Knoop
to be published in The Journal of Chemical Physics

arXiv:2305.01401
doi:10.1063/5.0155760
```

This repository is available at [https://github.com/sirmarcel/glp-archive](https://github.com/sirmarcel/glp-archive). Selected versions are archived on Zenodo, under [doi:10.5281/zenodo.7852529](https://doi.org/10.5281/zenodo.7852529).


## Overview

Each subfolder in this repository contains a `README.md` with additional information. The subfolders are:

- `results/`: Data and code that produced the figures in the manuscript 
- `work/`: Computational workflows, models, etc.
- `infra/`: Project-specific infrastructure code
- `meta/`: Scripts for assembling this archive; can be ignored but is retained for transparency.

## Related external code

The work in this repository relies on a few tools that the authors maintain separately:

- [`glp`](https://github.com/sirmarcel/glp) implements the quantities discussed in the manuscript
- [`mlff`](http://github.com/thorben-frank/mlff) implements the so3krates model
- [`tools.mlff`](https://github.com/flokno/tools.mlff) provides tools for the equation of state experiments

These tools were developed during the work in the manuscript. The following versions/tags reflect what was used to obtain results:

- `glp @ v0.1.0` (tag)
- `mlff @ v1.0` (branch)
- `mlff.tools @ v0.0.1`

We additionally note that the GK-MD functionality has been factored out into [`gkx`](https://github.com/sirmarcel/gkx).

## Versions

- `v1.1`: published version, archived at [doi:10.5281/zenodo.8406532](https://doi.org/10.5281/zenodo.8406532)
- `v1.0`: arXiv submission v1, archived at [doi:10.5281/zenodo.7852530](https://doi.org/10.5281/zenodo.7852530)
