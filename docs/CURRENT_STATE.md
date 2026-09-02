---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_ref: candidate/p35-validated-control-state-2026-09-02
candidate_parent_sha: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
validated_p35_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
validated_p35_pr: 199
validated_p35_runs: 33684805409,33684805218,33684805269,33684805422,33684805339,33684805302,33684805311,33684805272,33684805190,33684805285,33684805328
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

> **Validated remediation boundary:** PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02` passed the exact-head P-35 validation wave at `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. That SHA is preserved as the immutable P-35 evidence boundary.
>
> **Successor candidate:** branch `candidate/p35-validated-control-state-2026-09-02` was created directly from `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` to reconcile canonical control-state identity. Its evidence state is not inherited from historical candidates; it must establish its own exact candidate identity and affected-gate evidence.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus provenance anchor.
- `275756fd…` — current `main` control-plane base used by the P-35 remediation lineage.
- `643dc77a…` — validated P-35 remediation boundary; PR #199; immutable evidence scope.
- `candidate/p35-validated-control-state-2026-09-02` — successor candidate derived directly from `643dc77a…`.
- `92ff830b…` — superseded runtime candidate; prior P2/P6a evidence remains bound to its exact tree/deployment.
- `a43219b…` — superseded completion candidate; prior PDMAL/P9 evidence remains bound to its exact tree.
- Historical deployment identities remain historical and are not promoted to the successor candidate.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| P-35 remediation boundary | VALIDATED / IMMUTABLE EVIDENCE BOUNDARY | PR #199; `643dc77a…` |
| Successor candidate | CONTROL-STATE RECONCILIATION CANDIDATE / NOT FROZEN | branch derived from `643dc77a…` |
| P-35 | VALIDATED | exact-head implementation, regression, harness, pre-freeze, security, governance, provenance and control-state validation wave passed at `643dc77a…` |
| P2 | HISTORICAL / RE-RUN REQUIRED | prior evidence is candidate-bound |
| P3 | OPEN / RE-RUN REQUIRED | fresh artifact-contract evidence against successor/final candidate |
| P4 | OPEN | current-cycle operational blinding/custody closure required |
| P5 | OPEN | current-cycle reproducibility closure required |
| P6 | OPEN / FAIL-CLOSED | current-cycle durable custody proof required |
| P6a | HISTORICAL / RE-RUN REQUIRED | prior evidence is candidate/deployment-bound |
| P7 | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding required |
| P8 | OPEN / FAIL-CLOSED | current-candidate P-35/TGL and full closure evidence required |
| P9 | NOT EXECUTED FOR SUCCESSOR CANDIDATE | independent audit/reproduction required |
| Freeze | NOT ESTABLISHED | no frozen identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized empirical execution |

## P-35 integration boundary

The active implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF execution. Missing, malformed, unloadable, and non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated through `DGAF_TGLAdapter` into `TGLHooks`. Regression coverage exercises missing-checker refusal, explicit injection, premise KILL, and the real runner/task/adapter/TGL path.

P-35 is adjudicated VALIDATED at exact head `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. The successful validation set is recorded in the control-state record and PR #199. This successor branch does not alter that evidence boundary.

## Required closure sequence

1. Complete candidate identity reconciliation and establish the successor's exact head.
2. Rerun only validations made stale by the reconciliation commit(s), then confirm candidate readiness.
3. Complete fresh P3 artifact-contract evidence.
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

## Anti-loop / evidence-transfer rule

Documentation commits, CI success, deployment readiness, historical evidence, and repeated audits do not authorize empirical execution or transfer evidence across candidates. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope. The validated P-35 SHA `643dc77a…` remains the immutable remediation evidence boundary.
