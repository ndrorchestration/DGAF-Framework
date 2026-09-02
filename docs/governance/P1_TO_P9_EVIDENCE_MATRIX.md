# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-02  
**Documentation lineage:** `main`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Active completion/remediation candidate:** `fb485e9e0fd253be03e6937a448f4818eb8d54a1`  
**Active candidate branch:** `remediation/p35-minimal-mainline-2026-09-02`  
**Active candidate PR:** `#199`  
**Candidate deployment:** none claimed  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus provenance anchor.
- `275756fd…` — current `main` control-plane base for the active remediation.
- `fb485e9e…` — active P-35 remediation/completion candidate, PR #199.
- `92ff830b…` — superseded runtime candidate; P2/P6a evidence remains bound to its exact deployment.
- `a43219b…` — superseded completion candidate; PDMAL/P9 evidence remains bound to its exact tree.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — historical deployment for `92ff830b…`.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — historical preview deployment for `a43219b…`.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity, candidate identity, tree, deployment identity, and complete provenance | **OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **HISTORICAL VERIFIED / RE-RUN REQUIRED** | fresh run against final selected candidate/deployment |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED** | fresh candidate-bound evidence after remediation |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | current-cycle operational blinding/custody evidence independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | full current-candidate reproducibility evidence |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | durable current-candidate archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **HISTORICAL VERIFIED / RE-RUN REQUIRED** | fresh run against final selected candidate/deployment |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all current-candidate prerequisites and final P9 evidence satisfied |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED** | fresh exact-candidate P9 after remediation and candidate rebinding |

## P-35 remediation boundary

The prior completion candidate omitted explicit premise-checker injection at the DGAF adapter/task boundary. The active PR #199 is a minimal current-mainline remediation: DGAF pilot execution requires an explicit callable `PDMAL_PREMISE_CHECKER`; omission or invalid configuration is fail-closed; `ConsensusTask(condition="dgaf")` requires the checker; and the checker is propagated into `DGAF_TGLAdapter` and `TGLHooks`.

Regression coverage includes missing/malformed/non-callable configuration, explicit checker loading, task-level refusal, adapter injection, premise KILL, and the real runner/task/adapter/TGL path. This is implementation evidence only until an exact-head pre-freeze run is produced and P-35 is formally adjudicated.

No PDMAL-specific constitutional policy is invented by the remediation. Pilot execution remains blocked until an approved checker is supplied by the experimental-control design.

## Historical evidence boundary

Previous P2/P6a evidence on `92ff830b…` and previous PDMAL/P9 evidence on `a43219b…` remain valid only for those exact identities. They are retained for provenance and must not be promoted to the active candidate.

## Remaining critical path

1. Exact-head pre-freeze validation of PR #199.
2. P-35 adjudication.
3. Select the resulting exact experimental candidate.
4. Fresh P3–P6 and affected P2/P6a evidence against that candidate/deployment.
5. Final P7 binding.
6. P8 closure.
7. Independent P9 verification against the final candidate.
8. New immutable freeze and independent verification.
9. Separate explicit pilot authorization.
10. Only then execute the blinded pilot and allow empirical N to advance from 0.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-transfer rule

No historical candidate, deployment, artifact, runtime result, or experimental observation transfers to another candidate merely because code or documentation appears equivalent. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope.
