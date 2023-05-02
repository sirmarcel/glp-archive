# `glp-archive`
## Code and Data for "Stress and heat flux with automatic differentiation"

This repository contains data, code, and related artefacts supporting the following publication:

```
Stress and heat flux via automatic differentiation
by Marcel F. Langer, J. Thorben Frank, and Florian Knoop

arXiv: TBD
```

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