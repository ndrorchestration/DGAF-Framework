---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_ref: candidate/p35-validated-control-state-2026-09-02
candidate_parent_sha: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
candidate_status: POST-P-35 VALIDATION / PRE-FREEZE / FAIL-CLOSED / P3-P9 EVIDENCE REMAINING
active_p35_remediation_pr: 199
active_p35_validated_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
active_p35_validation_runs: 33684805409,33684805218,33684805269,33684805422,33684805339,33684805302,33684805311,33684805272,33684805190,33684805285,33684805328
---

# PDMAL Current Control State

This is the current pre-authorization control record. The P-35 remediation boundary was validated at exact head `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. This successor candidate is derived directly from that immutable validation boundary and exists to reconcile canonical control-state identity before candidate-bound closure work proceeds.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.

The validated P-35 boundary is PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02` at exact head `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. That SHA is evidence-immutable for P-35 adjudication and is not modified by this successor transition.

The active successor candidate is branch `candidate/p35-validated-control-state-2026-09-02`, created directly from `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. Its purpose is control-state reconciliation and exact-candidate establishment. No pilot authorization or empirical execution is enabled.

Historical candidates remain non-closing for the current cycle. Their evidence does not transfer to the successor candidate merely because documentation references them.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Validated P-35 boundary | VALIDATED / IMMUTABLE EVIDENCE BOUNDARY | PR #199; `643dc77a…`; validation set recorded above |
| Successor candidate | CONTROL-STATE RECONCILIATION CANDIDATE / NOT FROZEN | branch `candidate/p35-validated-control-state-2026-09-02`, parent `643dc77a…` |
| P-35 implementation | VALIDATED | exact-head implementation/regression/harness/pre-freeze/security/governance/provenance checks passed at `643dc77a…` |
| P2 runtime | HISTORICAL / RE-RUN REQUIRED | prior evidence is candidate-bound and does not transfer |
| P6a CORS | HISTORICAL / RE-RUN REQUIRED | prior evidence is candidate/deployment-bound and does not transfer |
| P3 | OPEN | Fresh evidence required against final exact candidate |
| P4 | OPEN | Fresh current-cycle blinding/custody evidence required |
| P5 | OPEN | Fresh current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Fresh durable custody proof required |
| P7 scientific specification | ADOPTED / FINAL BINDING OPEN | Must bind exact candidate/protocol/analysis/freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Requires current-candidate TGL/P-35 and analysis binding |
| P9 independent verification | NOT EXECUTED FOR SUCCESSOR CANDIDATE | Independent audit/reproduction required |
| New freeze | NOT CREATED | Candidate is not frozen |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## P-35 boundary

The active implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF pilot execution. Missing, malformed, unloadable, or non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated into `DGAF_TGLAdapter` and then into `TGLHooks`. Unexpected premise-checker failures remain governed by the existing fail-closed P-35 path.

P-35 is now adjudicated VALIDATED at exact head `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. The successful validation set includes the pre-freeze runner, pre-authorization security, governance CI, control-state consistency/head binding, truth-layer tests/validation, epistemic evidence validation, DGAF regression, PDMAL harness validation, and PDMAL instrumentation dry run recorded in the exact validation-run list above.

## Required closure sequence

1. Establish the successor candidate's exact head after control-state reconciliation.
2. Run only validations made stale by the reconciliation commit(s), then adjudicate candidate readiness.
3. Complete current-candidate P3 artifact-contract evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Re-run authenticated P2 and P6a against the same exact candidate and deployment.
8. Bind P7 to the exact candidate/protocol/analysis/final-freeze identity.
9. Close P8 from current-candidate TGL/P-35 evidence only.
10. Execute independent P9 verification against the final exact candidate.
11. Create and independently verify a new immutable freeze.
12. Obtain explicit pilot authorization.
13. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, runtime verification result, historical evidence artifact, or repeated semantic audit does not authorize scientific execution. Evidence must remain bound to its exact candidate/deployment/predicate scope. The validated P-35 SHA `643dc77a…` is preserved as the immutable remediation evidence boundary; the successor candidate must earn its own closure evidence.
