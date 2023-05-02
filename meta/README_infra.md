## `glp-infra`

This contains the code used to run and post-process molecular dynamics simulations in this project; it will be developed further separately in the [`gkx`](https://github.com/sirmarcel/gkx) repository in the future, but is kept here in its original state.

The infra depends on `glp` and its dependencies, and additionally the dependencies listed in `pyproject.toml`. For production use, we of course also require `mlff` for so3krates models.