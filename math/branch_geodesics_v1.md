# Branch Geodesics v1

## Goal
Define motion of particles when the connection or metric becomes branch‑valued.

## Classical equation
d²x^μ/dλ² + Γ^μ_{αβ}(dx^α/dλ)(dx^β/dλ) = 0

## Branch form
Γ becomes a branch object:

Γ = {(g_i , Γ_i)}

The geodesic equation therefore splits into branchwise equations.

## Evolution rule
1. Solve classical geodesic inside guard region.
2. Continue until guard boundary encountered.
3. Apply boundary policy.

## Boundary policies

### Termination
Worldline ends when singular guard is reached.

### Transition
Worldline enters core branch with separate evolution rule.

### Reflection (optional future extension)
Incoming branch mapped to outgoing classical branch.

## Minimal v1 choice
Allow:
- Termination
- Transition

## Acceptance criteria
Exterior geodesics reproduce GR exactly.