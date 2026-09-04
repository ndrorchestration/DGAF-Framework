# DGAF Numerical Instrument Reconciliation — 2026-09-04

**Status:** Audit control / pre-canonicalization

## Instrument register

| ID | Family | Current finding | Disposition |
|---|---|---|---|
| QA-11Q-ARTIFACT-v1 | Rubric | Weights sum 1.50 while formula divides by 11 | Explicit mathematical decision; no silent normalization |
| GATE-11Q-v2 | Gate | Naming collision with P-11/11Q | Unique invocation identity |
| AXIS-v1.2 | Metric | 4 invariants, 0–100, `min(I,P,A,E)` | Preserve canonical definition pending complete instrumentation |
| APOGEE-AXIS-RUBRIC-v1 | Derivative rubric | 7 dimensions, 0–1 weighted sum | Mark derivative/adaptation explicitly |
| RESON-HARMONIC-v1 | Rubric | 0.85 seal floor vs 0.75 elsewhere | Scope/authority decision required |
| AHG-S-v1.3 | Control metric | Formal companion uses different parameterization | Establish one parameter authority |
| AHG-ANALYSIS-v1 | Formal companion | Divergence terms total 1.70 but described as normalized | Define normalization or correct model |
| P42-RECOVERY-v1 | Control predicate | Implementation consistent; not efficacy proof | Keep as control signal |
| KAPPA-EVAL-v3.6 | Execution score | Distinct generic-composite family | Keep separate from AXIS/11Q/Reson |

## Evidence identity

Every numerical result used as control evidence must bind to:

`instrument_id + version + formula + parameter_set + scope + implementation + source_commit + execution_run + timestamp + epistemic_status`

## Mathematical tests

Where applicable verify weight sums, score domains, threshold reachability, explicit normalization, critical-fail precedence, threshold scope, derivative deltas, and upstream dependency status.

## Decision discipline

Prohibit automatic normalization, silent threshold selection, newest-document-as-canonical selection without authority, alias collapse, historical-score promotion, and successful non-authoritative CI overriding an unresolved dependency.

## Boundary

This document does not resolve disputed mathematical authority and does not authorize freeze, pilot execution, unblinding, or empirical claims.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
