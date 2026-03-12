# Branch Tensor Calculus v1

## Status

Draft v1.

This document defines a minimal branch-aware tensor framework intended to preserve ordinary tensor calculus on regular regions while replacing true zero-set singular evaluation events with guarded branch structure.

This is **not** a full replacement for differential geometry or General Relativity. It is a local extension layer for handling singular expressions without forcing global collapse into literal infinities or undefined terms.

---

# 1. Purpose

Classical tensor calculus assumes scalar coefficients belong to an ordinary arithmetic domain and that all algebraic manipulations are performed within that domain.

This becomes problematic when tensor components, inverse metrics, connection coefficients, or curvature scalars contain denominator expressions that hit exact zero on genuine singular sets.

The purpose of this framework is to:

1. preserve classical tensor calculus on non-singular regions,
2. represent singular events as guarded branch objects,
3. forbid premature simplification across unresolved zero sets,
4. support later construction of branch-aware geodesic and Einstein systems.

---

# 2. Design Principles

## P1. Exterior classicality
On any region where all relevant denominator expressions are provably nonzero, ordinary tensor calculus is unchanged.

## P2. Local exact-zero semantics
When a denominator expression hits exact zero, evaluation is handled locally by branch semantics rather than by unrestricted divergence.

## P3. Branch firewall
No algebraic simplification may erase, bypass, or silently assume away an unresolved zero-set guard.

## P4. Guarded refinement
Operations between branch objects are defined only after refinement to a common guard partition.

## P5. Boundary caution
Differentiation is classical only on fixed-guard regions. Boundary behavior is not assumed classical unless separately defined.

## P6. Coordinate-artifact caution
Only invariantly meaningful singular sets should be treated as physical core branches. Coordinate singularities must not be regularized merely because a chosen chart produces a zero denominator.

---

# 3. Primitive Objects

We assume an underlying manifold \(M\), or an intended coordinate domain when working locally.

## 3.1 Guards

A **guard** is a logical condition defining a region of validity.

Examples:

- \(r \neq 0\)
- \(r = 0\)
- \(x^2 + y^2 \neq 0\)
- \(f(p) = 0\)
- conjunctions such as \((r=0) \wedge (t>0)\)

Guards are treated as semantic constraints, not merely formatting labels.

A family of guards \(\{g_i\}\) is called **admissible** when:

1. they are pairwise disjoint up to logical equivalence,
2. their union covers the intended evaluation domain.

---

## 3.2 Branch Objects

A **branch object** is a finite guarded family

\[
B = \{(g_i, v_i)\}_{i=1}^n
\]

where:

- each \(g_i\) is a guard,
- each \(v_i\) is a value valid on that guard,
- the guards form an admissible partition of the intended domain.

Interpretation:

\[
B(p) = v_i(p) \quad \text{whenever } g_i(p) \text{ holds.}
\]

---

## 3.3 Core Objects

A **core object** is a distinguished value assigned on a singular guard branch where ordinary scalar evaluation is not retained.

Examples:

- \(\mathcal C_1\)
- \(\mathcal C_K(M)\)
- \(\mathcal C_{\mu\nu}\)

Core objects are not assumed to be ordinary real numbers unless explicitly stated.

They are placeholders for singular-branch values and may later be given additional algebraic rules.

---

# 4. Branch Scalars

A **branch scalar field** is a branch object whose values are scalar fields or core scalar objects.

Example:

\[
\frac{1}{r}
\rightsquigarrow
\left\{
(r \neq 0,\, 1/r),
(r = 0,\, \mathcal C_1)
\right\}
\]

Example:

\[
\frac{A(r)}{r^n}
\rightsquigarrow
\left\{
(r \neq 0,\, A(r)r^{-n}),
(r = 0,\, \mathcal C_n[A])
\right\}
\]

This representation must be introduced before any simplification that would assume \(r \neq 0\).

---

# 5. Branch Tensor Fields

A **branch tensor field** is a tensor-valued branch object

\[
T = \{(g_i, T_i)\}_{i=1}^n
\]

where each \(T_i\) is an ordinary tensor field on the region defined by \(g_i\), or a tensor-valued core object on singular guards.

Examples:

\[
T_{\mu\nu}
=
\left\{
(r \neq 0,\, T^{\text{ext}}_{\mu\nu}),
(r = 0,\, \mathcal C_{\mu\nu})
\right\}
\]

\[
g_{\mu\nu}
=
\left\{
(r \neq 0,\, g^{\text{class}}_{\mu\nu}),
(r = 0,\, g^{\text{core}}_{\mu\nu})
\right\}
\]

No assumption is made in v1 that the core branch metric is nondegenerate or invertible.

---

# 6. Guard Refinement

Operations between branch objects require refinement to a common guard partition.

Given

\[
A = \{(g_i, a_i)\}, \qquad B = \{(h_j, b_j)\},
\]

their common refinement is

\[
A \sqcap B = \{(g_i \wedge h_j, \cdot)\}_{i,j}
\]

after discarding inconsistent intersections.

This is the fundamental rule behind all branchwise operations.

---

# 7. Branchwise Algebra

## 7.1 Addition

Given branch objects \(A=\{(g_i,a_i)\}\) and \(B=\{(h_j,b_j)\}\),

\[
A + B
:=
\{(g_i \wedge h_j,\; a_i + b_j)\}_{i,j}
\]

with inconsistent guards removed.

---

## 7.2 Scalar Multiplication

For a branch scalar \(f=\{(g_i,f_i)\}\) and branch tensor \(T=\{(h_j,T_j)\}\),

\[
fT
:=
\{(g_i \wedge h_j,\; f_i T_j)\}_{i,j}
\]

again removing inconsistent guards.

---

## 7.3 Tensor Product

\[
A \otimes B
:=
\{(g_i \wedge h_j,\; a_i \otimes b_j)\}_{i,j}
\]

---

## 7.4 Contraction

Contraction is defined branchwise:

\[
\operatorname{Contr}(T)
:=
\{(g_i,\; \operatorname{Contr}(T_i))\}
\]

provided contraction is defined on the given branch value.

If contraction requires an inverse metric, that inverse must already exist on the branch where contraction is performed.

---

# 8. The Branch Firewall

This is the tensor version of the guarded-algebra firewall.

## Firewall Rule F1
No simplification may remove a guard condition that distinguishes a zero-hit branch from a nonzero branch.

## Firewall Rule F2
No inverse, cancellation, denominator-clearing step, or contraction that depends on invertibility may be performed before the relevant nonzero guard is established.

## Firewall Rule F3
If a tensor expression contains a factor whose definition depends on a denominator \(D\), and the status of \(D\) is unresolved, the expression must remain branch-protected.

## Firewall Rule F4
Classical identities that require invertibility or nonzero assumptions are branch-local only.

Examples:

- \(g^{\mu\alpha} g_{\alpha\nu} = \delta^\mu{}_\nu\) only on branches where the inverse metric exists.
- \(A/A = 1\) only on branches where \(A \neq 0\).
- cancellation across a factor \(r\) is allowed only under guard \(r \neq 0\).

---

# 9. Fixed-Guard Differentiation

Differentiation is defined only on regions where the active guard is locally fixed.

Let

\[
F = \{(g_i, f_i)\}
\]

be a branch scalar or branch tensor field.

Its **fixed-guard derivative** is

\[
\nabla F := \{(g_i, \nabla f_i)\}
\]

interpreted only on the interior of each guard region.

This means:

- on \(g_i^\circ\), differentiate classically,
- at guard boundaries, no classical derivative is assumed unless additional rules are given.

This avoids false claims about differentiability through singular branch transitions.

---

## 9.1 Boundary-sensitive expressions

If differentiation crosses a guard boundary, the result is flagged as **boundary-sensitive**.

In v1, boundary-sensitive derivatives are not automatically reduced.

This is a deliberate limitation.

---

# 10. Branch Metric Fields

A **branch metric field** is a symmetric branch tensor field of type \((0,2)\):

\[
g = \{(g_i, g_i^{\text{metric}})\}
\]

where on each branch the metric may be classical, degenerate, or core-valued.

## 10.1 Exterior branch
On non-singular guards, the metric behaves as an ordinary pseudo-Riemannian metric.

## 10.2 Core branch
On singular guards, the metric may be represented by a core object or by a separately defined core metric.

In v1, no requirement is imposed that the core branch admits:

- inverse metric,
- Levi-Civita connection,
- ordinary smooth structure.

That is postponed.

---

# 11. Branch Inverse Metrics

If

\[
g = \{(g_i, g_i^{\text{metric}})\},
\]

then the inverse metric is defined only on branches where inversion is valid:

\[
g^{-1}
=
\{(g_i,\; (g_i^{\text{metric}})^{-1})\}
\]

for those branches where inverse exists.

If inversion fails on a branch, that branch must remain explicitly marked as non-invertible or core-valued.

No global identity involving \(g^{-1}\) may be asserted across branches where inversion is not defined.

---

# 12. Branch Connection Skeleton

This document does not fully define branch connections, but it sets the minimum rule.

If \(g\) is branch-valued and a branch admits an inverse metric plus fixed-guard derivatives, then the Levi-Civita expression may be computed on that branch:

\[
\Gamma^\rho_{\mu\nu}
=
\frac12 g^{\rho\sigma}
(\partial_\mu g_{\sigma\nu}
+\partial_\nu g_{\sigma\mu}
-\partial_\sigma g_{\mu\nu})
\]

Thus connection coefficients are branch-local objects.

No single global Christoffel symbol is assumed unless all branches agree.

---

# 13. Singular Scalar Lift Rule

This rule is the main bridge from ordinary singular formulas into branch form.

Suppose an expression contains a scalar singular factor of the form

\[
S_n[A;D] := \frac{A}{D^n}
\]

where \(D\) may hit zero.

Then the branch lift is

\[
S_n[A;D]
\rightsquigarrow
\left\{
(D \neq 0,\; A D^{-n}),
(D = 0,\; \mathcal C_n[A,D])
\right\}
\]

where \(\mathcal C_n[A,D]\) is the chosen core-branch value.

This rule applies before any simplification that relies on \(D \neq 0\).

---

# 14. Invariance Warning

A singular denominator appearing in coordinates is not automatically physically singular.

Example:

- Schwarzschild metric coefficient \((1-2M/r)^{-1}\) blows up at \(r=2M\) in Schwarzschild coordinates,
- but this is a coordinate artifact, not a true invariant singularity.

Therefore:

## Rule I1
Branch lifting should only be applied as physical singular regularization when the zero set corresponds to an invariantly meaningful singular locus or when the framework is explicitly being used at the level of raw symbolic expressions.

## Rule I2
Coordinate singularities must be distinguished from invariant singularities before assigning physical interpretation to the core branch.

---

# 15. Schwarzschild-style Worked Example

We work only at the scalar level inside tensor calculus, since this document is foundational.

Consider the Kretschmann scalar in Schwarzschild spacetime:

\[
K(r)=\frac{48G^2M^2}{c^4 r^6}
\]

Classically, \(K(r)\to\infty\) as \(r\to 0\).

## 15.1 Branch lift

Apply the singular scalar lift rule with

\[
A = \frac{48G^2M^2}{c^4}, \qquad D=r, \qquad n=6
\]

to obtain

\[
K_B(r)
=
\left\{
(r \neq 0,\; \frac{48G^2M^2}{c^4 r^6}),
(r = 0,\; \mathcal C_K(M))
\right\}
\]

where \(\mathcal C_K(M)\) is a core scalar object.

## 15.2 Interpretation

- On the exterior branch \(r \neq 0\), classical curvature is unchanged.
- On the singular branch \(r = 0\), curvature is not treated as literal infinity but as a core branch value.

## 15.3 What this does not yet claim

This does **not** yet claim:

- that the core branch is smooth,
- that Einstein equations hold there classically,
- that geodesics pass through it,
- that the core object is an ordinary finite real number.

It only claims that the singularity has been lifted into a guarded branch representation.

---

# 16. Minimal Axioms for v1

## Axiom A1 — Guard completeness
Every branch object must carry guards covering its intended domain.

## Axiom A2 — Guard exclusivity
Distinct guards in a branch object must be mutually exclusive, up to logical equivalence.

## Axiom A3 — Exterior reduction
On a non-singular guard, branch calculus reduces to ordinary tensor calculus.

## Axiom A4 — Singular locality
Singular handling occurs only on branches where the triggering denominator actually vanishes.

## Axiom A5 — No silent crossing
No derivation may move from one guard branch to another without explicit refinement or transition handling.

## Axiom A6 — Invertibility locality
Any rule requiring invertibility is valid only on branches where invertibility is established.

## Axiom A7 — Boundary caution
Boundary behavior is not inferred from neighboring branch formulas unless explicitly defined.

---

# 17. Non-goals of v1

This document does not yet provide:

1. a full branch connection theory,
2. branch-aware curvature tensors in full detail,
3. distributional boundary calculus,
4. branch-compatible Bianchi identities,
5. a completed physical interpretation of core branches.

These are deferred to later documents.

---

# 18. Acceptance Criteria

This v1 framework is acceptable only if it satisfies all of the following:

## AC1
For regular regions, all tensor operations match ordinary tensor calculus exactly.

## AC2
Expressions with unresolved zero-set denominators remain branch-protected and are not prematurely simplified.

## AC3
Contraction and inverse-dependent identities are applied only on branches where their prerequisites hold.

## AC4
Differentiation is well-defined on fixed-guard interiors.

## AC5
Singular scalar factors can be lifted into branch form without contaminating the regular branch.

## AC6
Coordinate singularities are not automatically granted physical core status.

---

# 19. Outlook

This document provides the minimum algebraic and differential scaffold required for later construction of:

- branch-aware geodesic equations,
- branch-aware connection and curvature objects,
- guarded Einstein equations,
- singular-core toy models.

The next document should be:

**`branch_geodesics_v1.md`**

because geodesic evolution is the first decisive test of whether branch-aware tensor structure can support physically interpretable motion.

---
