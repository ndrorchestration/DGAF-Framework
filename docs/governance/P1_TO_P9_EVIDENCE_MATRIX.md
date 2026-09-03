# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-03  
**Documentation lineage:** `main`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Validated P-35 implementation candidate:** `0b1190fe91db6b963da0b31492d61fa1a34381e3`  
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
- `0b1190fe…` — exact implementation candidate on which P-35 was freshly validated.
- `92ff830b…` — superseded runtime candidate; P2/P6a evidence remains bound to its exact deployment.
- `a43219b…` — superseded completion candidate; PDMAL/P9 evidence remains bound to its exact tree.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity, candidate identity, tree, deployment identity, and complete provenance | **OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **HISTORICAL VERIFIED / RE-RUN REQUIRED** | fresh run against final selected candidate/deployment |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED** | fresh candidate-bound evidence after final candidate selection |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | current-cycle operational blinding/custody evidence independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | full current-candidate reproducibility evidence |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | durable current-candidate archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **HISTORICAL VERIFIED / RE-RUN REQUIRED** | fresh run against final selected candidate/deployment |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all current-candidate prerequisites and final P9 evidence satisfied |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED** | fresh exact-candidate P9 after final candidate rebinding |

## P-35 remediation boundary and adjudication

PR #199 is the minimal current-mainline P-35 remediation: DGAF pilot execution requires an explicit callable `PDMAL_PREMISE_CHECKER`; omission or invalid configuration is fail-closed; `ConsensusTask(condition="dgaf")` requires the checker; and the checker is propagated into `DGAF_TGLAdapter` and `TGLHooks`.

Exact implementation candidate `0b1190fe91db6b963da0b31492d61fa1a34381e3` completed the fresh validation wave successfully. Exact-head evidence includes PDMAL Pre-Freeze Runner Validation run `33697643625` and Governance CI run `33697643702`; the other candidate-bound validation workflows were also successful.

The P-35 regression verifies explicit checker invocation through the real runner/task/adapter/TGL path while preserving the fail-closed `UNRECOVERED_FAILURE` / `ffcr_success=False` contract. P-35 is therefore **CLOSED / VALIDATED for exact candidate `0b1190fe…`**.

This adjudication does not create a freeze, grant authorization, transfer historical evidence, or permit empirical execution.

## Historical evidence boundary

Previous P2/P6a evidence on `92ff830b…` and previous PDMAL/P9 evidence on `a43219b…` remain valid only for those exact identities. They are retained for provenance and must not be promoted to the active candidate.

## Remaining critical path

1. Select/reconcile the final experimental candidate and deployment identity.
2. Complete fresh P3 artifact-contract evidence.
3. Complete P4 operational blinding/custody evidence.
4. Complete P5 environment/topology/RNG reproducibility evidence.
5. Complete P6 durable archive/retrieval/hash evidence.
6. Bind P7 to the exact candidate/protocol/analysis/final-freeze identity.
7. Close P8 from current-candidate evidence only.
8. Independently verify P9 against the final exact candidate.
9. Create and independently verify a new immutable freeze.
10. Obtain separate explicit pilot authorization.
11. Only then execute the blinded pilot and allow empirical N to advance from 0.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-transfer rule

No historical candidate, deployment, artifact, runtime result, or experimental observation transfers to another candidate merely because code or documentation appears equivalent. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope.
