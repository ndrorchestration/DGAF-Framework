# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Current documentation/evidence lineage:** `main`  
**Engineering/production source:** `303f4424d2198f0d0cf76305c589263dd1e417dc`  
**Historical experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` (HISTORICAL; not silently promoted)  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface for P1–P9. It does not constitute executed experimental evidence. Historical evidence remains scoped to the exact SHA/run/artifact that produced it. Production deployment provenance is now verified for the merged DGAF v1 engineering source, but production readiness does not close experimental predicates.

## State precedence

`current verified executable boundary > documentation-only successors > historical candidate/freeze`

The prior `ac8ea267…` experimental record remains historical apparatus evidence. The merged DGAF v1 production source is `303f4424…`, but a **new experimental apparatus identity/freeze** must be explicitly bound before experimental execution. A substantive protocol, runner, analysis, artifact, or evidence change requires affected-predicate re-verification.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source identity and provenance | **OPEN** | final apparatus packet reconciled and bound |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **VERIFIED** | run `33300481208` passed all five cases against candidate `303f4424…` / deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` and retained artifact `9728767844` |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **IMPLEMENTED / OPEN** | fresh candidate-scoped execution evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current apparatus evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED / OPEN** | end-to-end current evidence verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **VERIFIED** | run `33302495240` passed four live cases on exact candidate/deployment and retained artifact `9729387603` |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / BINDING PENDING** | adopted record cryptographically bound to exact frozen protocol/apparatus/analysis/freeze identity |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without monoculture |

## P2 evidence record

P2 is **VERIFIED** for the exact production runtime boundary exercised by authenticated workflow run `33300481208` (`P2 Live Runtime Verification`, `workflow_dispatch`). The run's `p2-runtime` job `99227568599` completed successfully, consumed the protected Vercel automation bypass secret, executed the five-case matrix, and retained artifact `9728767844` (`p2-runtime-verification-303f4424d2198f0d0cf76305c589263dd1e417dc`) with recorded digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`.

The artifact records `evidence_class = P2_RUNTIME_EXECUTION`, source commit `303f4424d2198f0d0cf76305c589263dd1e417dc`, deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`, endpoint `https://project-7ybao.vercel.app/api/orchestrate`, and `all_pass = true`. Cases passed: `valid_missing_audit` → HTTP 503 / `BLOCKED`; `invalid_body_shape` → HTTP 400 / `REJECT`; `confidence_out_of_range` → HTTP 400 / `REJECT`; `invalid_turn` → HTTP 400 / `REJECT`; `malformed_json` → HTTP 400 with invalid-JSON response and no decision field.

This verifies the authenticated runtime contract only. It does not establish PDMAL efficacy, close P3–P6, close P8, create a freeze, grant pilot authorization, or increase empirical N.

## P6a evidence record

P6a is **VERIFIED** for the exact runtime boundary exercised by run `33302495240` (`P6a Live CORS Verification`, `workflow_dispatch`). Candidate SHA: `303f4424d2198f0d0cf76305c589263dd1e417dc`. Deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. Retained artifact: `9729387603`. Recorded artifact upload digest: `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`. The protected Vercel automation bypass secret was present and consumed without exposing its value; all four live CORS checks passed.

This verifies only P6a. It does not close P3–P6, close P8, establish empirical efficacy, create a freeze, or grant authorization.

## TGL contract prerequisite

The current-main TGL/P-35 remediation is integrated and validated in the DGAF v1 engineering line. Required-gate `SKIP` semantics, fail-closed handling, authority identity semantics, and exact final returned gate-set sealing are covered by the current governance test suite. This is engineering/control evidence, not experimental authorization.

## Supporting repository-native evaluator evidence

Governance CI run `33162492796` on exact tree `061286b1c17fe671cd5c58df025767befbeb55cd` retained repository-native evaluator results. These are `SYNTHETIC` / repository-authored evaluator-mechanism evidence only. They do not establish model-facing efficacy, production efficacy, or experimental validity.

## Additional freeze-admissibility predicates

| Predicate | Requirement | State |
|---|---|---|
| E2b | immutable verifier-toolchain runtime/dependency/workflow/environment fingerprint | **CLOSED / VERIFIED** for its recorded exact execution boundary |
| M6 | machine-retained proof of N=0/no authorization/no pilot/no unblinding | **CLOSED / VERIFIED** for its recorded exact execution boundary |

Historical M6 evidence remains bound to `ac8ea267…` and is not silently transferred to `303f4424…`.

## Production provenance

Production source/provenance predicate is **CLOSED** for the merged DGAF v1 engineering source:

- GitHub main merge SHA: `303f4424d2198f0d0cf76305c589263dd1e417dc`
- Vercel deployment: `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`
- Target: `production`
- State: `READY`
- Vercel Git SHA: exact match
- `/api/health`: HTTP `200 OK`
- Runtime: Node `v24.18.0`

This closes deployment/source provenance only. It does not close experimental efficacy or authorize an experiment.

## P7 adoption

The scientific decision remains adopted in substance: `dgaf` vs `null`, FFCR primary endpoint, paired root-seed estimand, two-sided 95% percentile bootstrap, 10,000 resamples, deterministic bootstrap seed `20260823`, α=`0.05`. Exact cryptographic binding to the final frozen apparatus remains open.

## Remaining critical path

1. Establish the final experimental apparatus identity on top of the merged production source.
2. Candidate-scoped P3 artifact-contract execution evidence.
3. P4 blinding/custody verification.
4. P5 environment/topology/RNG reproducibility verification.
5. P6 durable archive/retrieval/hash verification.
6. P7 exact binding.
7. P8 exact binding and closure.
8. Independent P9 verification.
9. New immutable freeze and independent freeze verification.
10. Separate explicit pilot authorization.
11. Only then authorized blinded pilot execution.

**P2 VERIFIED. P6a VERIFIED. P3–P6 remain evidence-gated. P8 OPEN / FAIL-CLOSED. P9 NOT EXECUTED. No freeze. No pilot is authorized. Empirical N = 0.**
