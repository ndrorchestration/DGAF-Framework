---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_sha: fb485e9e0fd253be03e6937a448f4818eb8d54a1
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: fb485e9e0fd253be03e6937a448f4818eb8d54a1
candidate_status: P-35 REMEDIATION CANDIDATE / NOT FROZEN / P3-P9 EVIDENCE REMAINING
active_p35_remediation_head: fb485e9e0fd253be03e6937a448f4818eb8d54a1
active_p35_pre_freeze_run: PENDING EXACT-HEAD VALIDATION
---

# PDMAL Current Control State

This is the current pre-authorization control record. The active implementation candidate is now the current-mainline P-35 remediation branch/PR #199. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.

The previous runtime candidate `92ff830b1c67413df745e37087e6447c9c251b9a` remains historical/non-closing for the current completion cycle. It is not promoted merely because documentation now references the remediation candidate.

The active P-35 remediation is PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02`, currently at `fb485e9e0fd253be03e6937a448f4818eb8d54a1`. This branch was created from current mainline and carries the minimal explicit P-35 premise-checker boundary plus regression coverage. No pilot authorization or empirical execution is enabled.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` is provenance only |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Previous runtime candidate | HISTORICAL / SUPERSEDED FOR CURRENT CYCLE | `92ff830b…`; tree `73cf3ad…` |
| Active completion candidate | CURRENT P-35 REMEDIATION / NOT FROZEN | `fb485e9e…`; PR #199 |
| Candidate lineage | ESTABLISHED | current `main` `275756fd…` → PR #199 |
| Current production deployment | HISTORICAL CANDIDATE-BOUND | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P-35 implementation | IMPLEMENTED / ENGINEERING VALIDATION PENDING | explicit checker load → task → adapter → TGL |
| P2 runtime | HISTORICAL CURRENT-CANDIDATE EVIDENCE | run `33509348174`; artifact `9800942933` |
| P6a CORS | HISTORICAL CURRENT-CANDIDATE EVIDENCE | run `33509416955`; artifact `9800972819` |
| P3 | OPEN | Fresh evidence required against final exact candidate |
| P4 | OPEN | Fresh current-cycle blinding/custody evidence required |
| P5 | OPEN | Fresh current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Fresh durable custody proof required |
| P7 scientific specification | ADOPTED / FINAL BINDING OPEN | Must bind exact candidate/protocol/analysis/freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Requires current-candidate TGL/P-35 and analysis binding |
| P9 independent verification | NOT EXECUTED FOR ACTIVE CANDIDATE | Independent audit/reproduction required |
| New freeze | NOT CREATED | Candidate is not frozen |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## P-35 boundary

The active implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF pilot execution. Missing, malformed, unloadable, or non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated into `DGAF_TGLAdapter` and then into `TGLHooks`. Unexpected premise-checker failures remain governed by the existing fail-closed P-35 path.

This is an implementation control, not yet a closure claim. Exact-head automated evidence must be produced before P-35 is adjudicated closed.

## Required closure sequence

1. Run exact-head pre-freeze validation for PR #199.
2. Adjudicate P-35 from that exact-head evidence.
3. Complete current-candidate P3 artifact-contract evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Bind P7 to the exact candidate/protocol/analysis/final-freeze identity.
8. Close P8 from current-candidate TGL/P-35 evidence only.
9. Execute independent P9 verification against the final exact candidate.
10. Create and independently verify a new immutable freeze.
11. Obtain explicit pilot authorization.
12. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, runtime verification result, historical evidence artifact, or repeated semantic audit does not authorize scientific execution. Evidence must remain bound to its exact candidate/deployment/predicate scope.
