# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-04  
**Current documentation/evidence lineage:** `main`  
**Current main tip:** `35436f1c95c11e49d8af7603bf914128cf2b4aee`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT ESTABLISHED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected apparatus provenance anchor.
- `89be386b…` — consolidated current documentation/control-state anchor.
- `35436f1c…` — current `main` tip; later documentation-only descendant of the consolidated anchor.
- `7c1cc4bb…` — runtime candidate bound to the closed P2/P6a evidence below; retained as the verified executable evidence identity.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — deployment bound to that P2/P6a evidence.
- `48c12c66…` / `dpl_CW4…` — superseded candidate/deployment; historical and non-transferable.
- `a43219b4…` — prior completion candidate with scoped P3–P6/P9 evidence; historical/non-transferable.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact apparatus/source identity, executable candidate identity, deployment identity, and complete provenance | **OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **CLOSED / VERIFIED** | Run `33730195621`; artifact `9883521704`; candidate `7c1cc4…` / deployment `dpl_8Ms…`; five required cases passed their defined predicates |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **OPEN — CURRENT EXECUTION EVIDENCE REQUIRED** | candidate-scoped artifact contract evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN — OPERATIONAL CLOSURE** | current-cycle operational blinding/custody evidence independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN — CURRENT-CANDIDATE CLOSURE** | exact candidate reproducibility and provenance evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | durable archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **CLOSED / VERIFIED** | Run `33728695806`; artifact `9882965299`; candidate `7c1cc4…` / deployment `dpl_8Ms…`; four required checks passed |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | current selected candidate passes prerequisites and final binding |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **OPEN** | fresh independent verification against the final bound evidence |

## Current runtime evidence

P2 and P6a are closed against executable candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. Later documentation/control-plane changes do not reopen those closed runtime predicates.

### P2 — Run `33730195621`

Artifact `9883521704`; digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

### P6a — Run `33728695806`

Artifact `9882965299`; digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

## Historical completion evidence — non-transferable

Run `33572123862` verified substantial P3/P4/P5/P6 workflow behavior for exact candidate `a43219b4…`, including 19 structural tests, deterministic smoke/reproducibility checks, masked CSV schema validation, checksum sidecar verification, artifact round-trip retrieval, and an evidence registry. P4 and P6 were explicitly workflow-level/synthetic evidence rather than full operational closure. This evidence remains historical.

Run `33572123857` provided a scoped P9 pass for `a43219b4…`; it is likewise historical.

## Evaluator integrity

Completion Controller run `33729094860` evaluated documentation PR #210 SHA `25b6379…` rather than current main. Its result is therefore candidate-scoped to that triggering workflow and does not establish current-main closure.

## Matrix-control disposition

PRs #220, #230, and #231 were closed without merge after review established that their additional matrix-equality assertion was logically implied by the existing canonical-coordinate membership, exact per-condition cardinality, and duplicate-cell rejection constraints. No active matrix-hardening blocker remains.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or experimental observation may be transferred to another candidate merely because code or documentation appears equivalent. Identity must be explicit and exact. Closed runtime predicates remain closed unless the runtime/control-state surface they test materially changes.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Remaining critical path

1. P3 current execution evidence and exact provenance reconciliation.
2. P4 operational blinding/custody closure.
3. P5 reproducibility closure.
4. P6 durable archive/retrieval/hash proof.
5. P7 final exact binding.
6. P8 analysis lock/verification.
7. P9 independent verification.
8. Freeze.
9. Separate authorization.
10. Only then blinded pilot execution.