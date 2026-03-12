
# Branch GR Engine v1

This bundle contains a minimal Python prototype for branch-aware GR experiments.

## Files

- `branch_gr_engine_v1.py`
- `README_branch_gr_engine_v1.md`

## What it does

- detects denominator zero sets for protected quotients like `A / r^n`
- lifts them into guarded branch objects
- propagates guards through simple scalar algebra
- models a Schwarzschild-style scalar `K(r) = A / r^6`
- runs a reduced radial infall simulation with:
  - `terminate`
  - `transition`

## Run

```bash
python branch_gr_engine_v1.py
```

## Important

This is not full GR.
It is a scaffold for future tensor, geodesic, and Einstein-equation upgrades.
