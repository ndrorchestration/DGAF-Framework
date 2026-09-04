# DGAF Numerical Instrument Reconciliation — 2026-09-04

**Status:** Audit control / pre-canonicalization
**Purpose:** Separate mathematical validity from authority, lineage, implementation, and evidence status.

## Instrument register

| ID | Family | Model | Current defect | Required disposition |
|---|---|---|---|---|
| QA-11Q-ARTIFACT-v1 | Rubric | 11 questions; stated weighted composite | Weights sum 1.50 while formula divides by 11 | Explicit mathematical decision; no silent normalization |
| GATE-11Q-v2 | Gate | 11 deployment gates; ≥3/4 across N≥3 when applicable | Naming collision with P-11/11Q | Unique invocation identity |
| AXIS-v1.2 | Metric | 4 invariants, 0–100, min(I,P,A,E) | Operational measurement cycle incomplete | Preserve as canonical definition pending execution |
| APOGEE-AXIS-RUBRIC-v1 | Derivative rubric | 7 dimensions, 0–1 weighted sum | Does not implement canonical AXIS model | Mark derivative/adaptation explicitly |
| RESON-HARMONIC-v1 | Rubric | 4 H dimensions; weighted average | 0.85 seal floor vs 0.75 P-15 references | Scope/authority decision required |
| AHG-S-v1.3 | Control metric | S(t)=0.35D_e+0.20N+0.25C+0.20R; φ=1+0.8σ(S) | Companion analysis uses different weights/range | Establish one parameter authority |
| AHG-ANALYSIS-v1 | Formal companion | Divergence decomposition with 0.30/0.40/1.00 | “Normalized partition” lacks explicit normalization | Define normalization or correct model |
| P42-RECOVERY-v1 | Control predicate | 0.50ΔD_e+0.30ΔK+0.20Δvφ | No defect found; must remain empirical signal only | Keep implemented but non-probative |
| KAPPA-EVAL-v3.6 | Execution score | Five-score weighted average, selected-weight normalized | Semantic generic-composite collision risk | Keep separate score family |

## Canonical evidence identity

Every numerical result used as control evidence must bind to:

```text
instrument_id + version + formula + parameter_set + scope + implementation + source_commit + execution_run + timestamp + epistemic_status
```

## Mathematical test suite requirements

Where applicable, executable tests should verify:

1. all declared weights have the claimed sum;
2. all score domains are compatible with formulas;
3. the maximum attainable score can reach every advertised threshold;
4. normalization is explicit and reproducible;
5. critical-fail predicates dominate composite scores where specified;
6. threshold semantics are scoped to the correct artifact/gate;
7. derivatives declare exact semantic deltas from canonical models;
8. derived evidence is blocked from promotion when upstream instruments are unresolved.

## Decision discipline

The following are expressly prohibited during reconciliation:

- automatic normalization;
- replacing a threshold with the stricter value merely because it is stricter;
- selecting the newest document as canonical without authority evidence;
- collapsing differently typed instruments under one ID;
- using historical execution results to validate current implementation;
- treating successful non-authoritative CI as an override of a failed gating dependency.

## External best-practice alignment

NIST AI RMF emphasizes rigorous, documented measurement and evaluation, including uncertainty, benchmarks, traceability, and independent review. GitHub's secure-use guidance recommends immutable commit-SHA pinning for actions. SLSA provenance guidance emphasizes verifiable information about where, when, and how artifacts were produced.

## Boundary

This document is an audit/engineering control and does not resolve disputed mathematical authority. DGAF remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
