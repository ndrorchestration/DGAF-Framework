# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-03  
**Current documentation/evidence lineage:** `main`  
**Current mainline candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Current exact deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT ESTABLISHED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Identity roles

- `2a54a67d…` — corrected apparatus provenance anchor.
- `7c1cc4bb…` — current mainline candidate after P6a CORS remediation.
- `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` — exact current deployment bound to current P2/P6a runtime evidence.
- `48c12c66…` / `dpl_CW4…` — superseded candidate/deployment; historical and non-transferable.
- `a43219b4…` — prior completion candidate with scoped P3–P6/P9 evidence; historical/non-transferable to `7c1cc4…`.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity, candidate identity, tree, deployment identity, and complete provenance | **OPEN** | exact final candidate/provenance/deployment binding retained and reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **CLOSED / VERIFIED** | Run `33730195621`; artifact `9883521704`; exact candidate `7c1cc4…` / deployment `dpl_8Ms…`; five required cases passed their defined predicates |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **OPEN — CURRENT-CANDIDATE EVIDENCE REQUIRED** | fresh exact-current-candidate artifact contract evidence |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN — OPERATIONAL CLOSURE** | current-cycle operational blinding/custody evidence independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN — CURRENT-CANDIDATE CLOSURE** | current candidate exact binding, reproducibility, environment and RNG evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **OPEN / FAIL-CLOSED** | durable current-candidate archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **CLOSED / VERIFIED** | Run `33728695806`; artifact `9882965299`; exact candidate `7c1cc4…` / deployment `dpl_8Ms…`; four required checks passed |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / FINAL BINDING OPEN** | exact corrected apparatus/candidate/protocol/analysis/freeze binding |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | current selected candidate passes prerequisites and final binding |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **OPEN** | fresh exact-current-candidate P9 after all material prerequisites are current |

## Current exact runtime evidence

### P2 — Run `33730195621`

Exact candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.  
Deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.  
Base URL: `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app`.  
Artifact: `9883521704`.  
Artifact digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

The five-case matrix passed its defined predicates: valid request without live audit state remained fail-closed/BLOCKED; invalid body shape, confidence out of range, and invalid turn were rejected; malformed JSON produced expected non-success handling.

### P6a — Run `33728695806`

Exact candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.  
Deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.  
Base URL: `https://dynamicgovernanceagenticformation-9u712s0cq-ndrorchestration.vercel.app`.  
Allowed origin: `https://dynamicgovernanceagenticformation.vercel.app`.  
Artifact: `9882965299`.  
Artifact digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

The allowed/disallowed POST and preflight predicates all passed.

## Historical completion evidence — non-transferable

Run `33572123862` verified substantial P3/P4/P5/P6 workflow behavior for exact candidate `a43219b4…`, including 19 structural tests, deterministic smoke/reproducibility checks, masked CSV schema validation, checksum sidecar verification, artifact round-trip retrieval, and an evidence registry. P4 and P6 were explicitly workflow-level/synthetic evidence rather than full operational closure. This evidence remains historical because the candidate differs from current main.

Run `33572123857` provided a scoped P9 pass for `a43219b4…`; it is likewise non-transferable to `7c1cc4…`.

## Evaluator integrity

Completion Controller run `33729094860` evaluated documentation PR #210 SHA `25b6379…` rather than current main. This was consistent with its `workflow_run.head_sha` input semantics. A controller result is therefore candidate-scoped evidence and must not be interpreted as current-main evidence unless the triggering candidate is exactly the current candidate.

Current controller runs triggered from the exact `7c1cc4…` candidate are eligible for inspection, but controller success remains an evaluator result and does not itself establish P4/P5/P6 closure, freeze, or authorization.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or experimental observation may be transferred to another candidate merely because code or documentation appears equivalent. Identity must be explicit and exact.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Remaining critical path

1. Produce current-candidate P3–P6 evidence, with P4 operational blinding/custody and P6 durable archive/retrieval/hash proof.
2. Finalize P7 exact scientific/protocol/apparatus binding.
3. Close P8 from current-candidate evidence.
4. Execute fresh independent P9 against the same exact candidate.
5. Create and independently verify immutable freeze.
6. Obtain separate explicit pilot authorization.
7. Only then execute the blinded pilot.
