# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-04  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Last reconciled main tip:** `aabb527b0aec49a04fe763dd06e9b9610f8f1139`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT ESTABLISHED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected apparatus provenance anchor.
- `89be386b…` — consolidated control-state anchor.
- `aabb527b…` — latest reconciled documentation/control-plane mainline tip; not an executable candidate.
- `7c1cc4bb…` — runtime candidate bound to the closed P2/P6a evidence below; retained as the verified executable evidence identity.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — deployment bound to that P2/P6a evidence.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact apparatus/source identity, executable candidate identity, deployment identity, and complete provenance | **OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **CLOSED / VERIFIED** | Run `33730195621`; artifact `9883521704`; candidate `7c1cc4…` / deployment `dpl_8Ms…` |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **OPEN — CURRENT EXECUTION EVIDENCE REQUIRED** | candidate-scoped artifact contract evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN — OPERATIONAL CLOSURE** | current-cycle operational blinding/custody evidence independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN — CURRENT-CANDIDATE CLOSURE** | exact candidate reproducibility and provenance evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | durable archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **CLOSED / VERIFIED** | Run `33728695806`; artifact `9882965299`; candidate `7c1cc4…` / deployment `dpl_8Ms…` |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | current selected candidate passes prerequisites and final binding |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **OPEN** | fresh independent verification against the final bound evidence |

## Current runtime evidence

P2 and P6a are closed against executable candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. Later documentation/control-plane changes do not reopen those closed runtime predicates.

### P2 — Run `33730195621`

Artifact `9883521704`; digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

### P6a — Run `33728695806`

Artifact `9882965299`; digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

## Current-candidate evidence packet

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_PACKET_2026-09-04.md` defines the required P3–P9 packet without asserting unproduced evidence. It separates closed runtime evidence from operational P4, reproducibility P5, durable P6, final P7 binding, P8 lock, and fresh P9 requirements.

## Historical completion evidence — non-transferable

Run `33572123862` verified substantial P3/P4/P5/P6 workflow behavior for exact candidate `a43219b4…`; its evidence remains historical. Run `33572123857` provided a scoped P9 pass for `a43219b4…`; it is likewise historical/non-transferable.

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
