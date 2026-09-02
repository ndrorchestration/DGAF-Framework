---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
active_p35_remediation_branch: remediation/p35-minimal-mainline-2026-09-02
active_p35_remediation_pr: 199
active_p35_remediation_head: fcdfa0180625c413e692d7fa405ea361c05dc53f
active_p35_candidate_tree: a81faf976de029734772b81a3615e3316ddf7641
active_p35_validation_run: 33652271526
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

> **Current boundary:** `main` remains the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor.
>
> **Active completion/remediation candidate identity:** PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02`, head `fcdfa0180625c413e692d7fa405ea361c05dc53f`, tree `a81faf976de029734772b81a3615e3316ddf7641`. The current exact-head pre-freeze validation run is `33652271526`. The candidate is not frozen and has not been authorized for empirical execution.
>
> **Previous runtime/completion candidates:** `92ff830b…` and `a43219b…` remain historical evidence boundaries for this cycle. Their evidence is not transferred to PR #199.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus provenance anchor.
- `275756fd…` — current `main` control-plane base from which PR #199 was created.
- `fcdfa018…` — active P-35 remediation/completion candidate, PR #199.
- `a81faf97…` — exact tree of the active candidate.
- `92ff830b…` — superseded mainline runtime candidate; P2/P6a evidence remains bound to its exact tree/deployment.
- `a43219b…` — superseded controlled completion candidate; PDMAL/P9 evidence remains bound to its exact tree.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — historical deployment identity for `92ff830b…` P2/P6a evidence.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — historical preview deployment for `a43219b…`; not a deployment identity for PR #199.
- `33652271526` — exact-head PDMAL Pre-Freeze Runner Validation for `fcdfa018…`; run conclusion `FAIL` because its contract suite contained one test expectation mismatch.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Candidate identity | CURRENT P-35 REMEDIATION / NOT FROZEN | `fcdfa018…`; tree `a81faf97…`; PR #199 |
| P-35 implementation | IMPLEMENTED / EXACT-HEAD VALIDATION FAILED ON TEST EXPECTATION | production path raises the existing P-35 KILL exception as designed; regression assertion requires correction |
| Pre-freeze validation run | FAILED | run `33652271526`; 47 passed, 1 failed in contract suite |
| P2 | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` |
| P3 | HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED | prior evidence bound to `a43219b…` |
| P4 | OPEN | current-cycle operational closure required |
| P5 | OPEN | current-cycle reproducibility closure required |
| P6 | OPEN / FAIL-CLOSED | current-cycle durable custody proof required |
| P6a | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` |
| P7 | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding required |
| P8 | OPEN / FAIL-CLOSED | current-candidate P-35/TGL plus full closure evidence required |
| P9 | HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED | prior pass bound to `a43219b…` |
| Freeze | NOT ESTABLISHED | no frozen identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized empirical execution |

## P-35 integration boundary

The active candidate requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF execution. Missing, malformed, unloadable, and non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated through `DGAF_TGLAdapter` into `TGLHooks`. Regression coverage includes missing-checker refusal, explicit injection, premise KILL, and the real runner/task/adapter/TGL path.

The first exact-head run established that the production P-35 rejection path raises `PremiseViolationError` carrying the KILL event. The failed test was asserting a returned result object instead. This is a test-contract mismatch, not evidence of a premise-checker bypass.

## Required closure sequence

1. Correct the P-35 regression assertion and exact candidate binding.
2. Rerun the exact-head pre-freeze validation.
3. P-35 adjudication from passing exact-head evidence.
4. Select/retain the resulting exact experimental candidate.
5. Fresh P3–P6 and affected P2/P6a evidence against that exact candidate/deployment.
6. Final P7 binding.
7. P8 closure.
8. Independent P9 verification.
9. New immutable freeze and independent freeze verification.
10. Separate pilot authorization.
11. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop / evidence-transfer rule

Documentation commits, CI success, deployment readiness, historical evidence, and repeated audits do not authorize empirical execution or transfer evidence across candidates. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope.
