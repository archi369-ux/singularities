# Boundary / GR Prototype Action Log

This is an action-only sequence log.
It records what we did, not the user prompts.

## Format
- Step number
- Action performed
- Outcome

---

1. Established a reduced Schwarzschild radial testbed in ingoing Eddington–Finkelstein coordinates.
   Outcome: baseline smooth-spacetime prototype created.

2. Identified singular/core handling as the main instability region.
   Outcome: exact-core continuation was treated as suspect.

3. Introduced pre-core event detection instead of exact-singularity forcing.
   Outcome: numerics became more workable.

4. Built branch-aware / boundary-aware geodesic experiments.
   Outcome: continuation could be tested without evolving through the exact singular point.

5. Implemented Christoffel-based geodesic integration rather than relying only on first-integral shortcuts.
   Outcome: connection-driven dynamics became testable directly.

6. Added core-safe integration safeguards.
   Outcome: trajectories could be advanced closer to the trigger region without immediate numerical failure.

7. Implemented a first practical reset law after trigger.
   Outcome: outward recovery became possible, but consistency was still unverified.

8. Ran mass and trigger sensitivity tests.
   Outcome: trigger behavior appeared stable enough to compare across cases.

9. Compared connection-driven continuation against a first-integral baseline.
   Outcome: connection-driven recovery behaved materially differently from the baseline.

10. Improved the baseline and repeated comparison.
    Outcome: mismatch persisted; connection-driven dynamics were doing nontrivial work.

11. Checked timelike normalization after reset.
    Outcome: the original damped-flip continuation was numerically stable but geometrically inconsistent.

12. Replaced the original reset with constraint-preserving reset families.
    Outcome: one family failed, one family preserved normalization in some cases.

13. Added anti-retrigger strategies.
    Outcome: cooldown worked better than simple hysteresis or farther reset.

14. Fixed root/sign selection in the constraint-preserving reset.
    Outcome: normalization preservation and stable recovery improved substantially.

15. Validated the corrected constraint-preserving law on staged cases.
    Outcome: stable outward recovery with machine-precision normalization was achieved.

16. Expanded validation to the full 4x5 tested grid.
    Outcome: the constraint-preserving + cooldown law passed the completed grid as a practical reduced-model law.

17. Tested a second invariant: Killing energy.
    Outcome: the validated normalization-preserving law produced a large energy jump at reset.

18. Built an exact double-constraint reset enforcing both normalization and energy at reset.
    Outcome: instantaneous matching succeeded, but the outgoing evolution became catastrophically unstable.

19. Built blended resets between the normalization-preserving and energy-preserving endpoints.
    Outcome: energy jump could be reduced, but instability / constraint degradation emerged.

20. Built a constrained-optimization reset on the old state space.
    Outcome: reduced reset mismatch did not solve the structural instability.

21. Added a short transition-layer outgoing law after the double reset.
    Outcome: catastrophe was softened but not eliminated; the same deep tradeoff remained.

22. Reframed the problem as a test of the smooth-spacetime-only closure hypothesis.
    Outcome: the target of criticism became explicit: same smooth state space, same smooth continuation law.

23. Formalized the falsification-style criterion:
    - outgoing admissibility
    - stable recovery
    - normalization consistency
    - energy consistency
    Outcome: smooth-only continuation could now be tested systematically.

24. Compared smooth-state-space continuation families under that criterion.
    Outcome: no old-state-space continuation satisfied all desired conditions together.

25. Tested a genuinely different post-boundary model: boundary-manifold evolution.
    Outcome: energy continuity and stable recovery improved dramatically, but normalization degraded badly.

26. Tested simple projection on top of the boundary-manifold model.
    Outcome: it did not materially improve the normalization problem.

27. Reassessed the framework in light of boundary semantics.
    Outcome: the results supported a domain-boundary interpretation rather than exact smooth continuation through the core.

28. Distinguished clearly between:
    - standard GR outside the boundary
    - a non-smooth post-boundary continuation regime
    Outcome: the prototype became a hybrid model rather than pure smooth-spacetime-only GR.

29. Attacked the smooth-spacetime-only closure assumption directly.
    Outcome: it remained unsupported in the prototype.

30. Integrated the boundary-style interpretation into the research direction.
    Outcome: the next target became a genuinely new post-boundary state space rather than more local reset tweaks.

---

## Current state

Practical winner in the old state space:
- constraint-preserving reset + cooldown
- strong normalization behavior
- weak energy continuity

Best alternative post-boundary model so far:
- boundary-manifold evolution
- strong energy behavior
- weak normalization behavior

Main unresolved issue:
- no tested model yet preserves both normalization and energy while also remaining stably recoverable in one unified post-boundary description.

## Current theoretical direction

- Treat smooth GR as an exterior regime.
- Treat the core/singularity region as a boundary of validity.
- Search for a new post-boundary state space rather than forcing continuation inside the old one.
