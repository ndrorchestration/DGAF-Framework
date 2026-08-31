# R5–R7 Gate Recovery Execution Matrix — 2026-08-30

**Scope:** all seven constitutive TGL gates.
**Status:** planning/evidence only; no apparatus mutation.
**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.

## Objective

Turn each evidence-qualified gate into a bounded implementation work package with explicit preservation tests. No proxy becomes admissible merely because the current substrate is convenient.

| Gate | Historical target | Minimum current-state addition | Preservation test | Current lane |
|---|---|---|---|---|
| P-31 | tiered context-token retention/pruning | token identity, tier, insertion time, trust-edge, retention, anchor tracking, prune audit | historical constants/formula reproduce expected retention and audit output | RESTORE-ready |
| P-33 | weighted graph convergence | edge identity, `W_t`, `W_{t-1}`, Frobenius delta, consecutive-state tracking, event emission | manual norm calculation equals monitor result; first turn establishes baseline | RESTORE-ready |
| P-32 | rolling stability ratio vs φ* at Fib checkpoints | stable/total turn counters, checkpoint schedule, tolerance table, failure ladder, HPG bypass state | checkpoint decisions reproduce historical contract for controlled trajectories | RESTORE-ready |
| P-27 | KAPPA confidence-gated category routing | input category/confidence evidence, weight configuration, thresholds, fallback/blend policy, routing audit | historical test vectors reproduce category/policy selection; unsafe/ambiguous cases fail closed | RESTORE-mapping |
| P-29 | Sentinel annotated risk pass | historical risk-review payload and hook semantics must be extracted exactly | every defined hook produces the historical risk state and hard-block behavior | Contract extraction required |
| P-30 | Apogee attestation gate | historical attestation/11Q inputs, scoring semantics, normative-constraint coupling | historical acceptance/rejection examples reproduce exactly | Contract extraction required |
| DemiJoule | six-axis semantic safety gate | exact six-axis payload, decision ladder, escalation/deep-scan semantics | controlled safe/unsafe vectors reproduce historical outcomes | Contract extraction required |

## Implementation order

1. Freeze the recovered historical constants and semantic interfaces for P-31/P-33/P-32/P-27 in a dedicated recovery specification.
2. Extract exact P-29/P-30/DemiJoule contracts from historical source artifacts before writing adapters.
3. Build the substrate extensions behind explicit unit/reference tests.
4. Bind all seven gates through canonical TGL invocation, with missing/invalid state remaining FAIL-CLOSED.
5. Generate a fresh candidate SHA after apparatus changes.
6. Re-run candidate verification (P2/P6a and the required P3–P9 sequence) against that exact SHA.
7. Create an immutable freeze only after the new candidate passes the required chain.
8. Preserve authorization and N=0 until the freeze and authorization predicates are independently satisfied.

## Anti-loop controls

- Do not repeat repository discovery for a gate already marked evidence-qualified unless new authoritative evidence appears.
- Do not infer a current substrate field is equivalent merely because names or numeric ranges resemble the historical input.
- Do not convert simulation results into empirical N.
- Do not carry P2/P6a/P3–P9 evidence from a prior apparatus across a new apparatus SHA.
- Do not designate a candidate or freeze as a documentation side effect.

## Current completion interpretation

The project has moved from broad discovery into bounded recovery engineering. P-31/P-33/P-32 now have historical contract evidence with implementation context. P-27 has a concrete versioned historical component contract. P-29/P-30/DemiJoule are the remaining exact-contract extraction lane. This is sufficient to prevent further unbounded searching while preserving fail-closed semantics.
