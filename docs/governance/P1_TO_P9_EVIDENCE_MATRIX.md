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
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **BLOCKED / OPEN** | matrix passes with exact final candidate/deployment identity |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **IMPLEMENTED / OPEN** | fresh candidate-scoped execution evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current apparatus evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED / OPEN** | end-to-end current evidence verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **BLOCKED / OPEN** | matrix passes on same deployment as P2 |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / BINDING PENDING** | adopted record cryptographically bound to exact frozen protocol/apparatus/analysis/freeze identity |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without monoculture |

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

This closes deployment/source provenance only. It does not close P2/P6a or authorize an experiment.

## P7 adoption

The scientific decision remains adopted in substance: `dgaf` vs `null`, FFCR primary endpoint, paired root-seed estimand, two-sided 95% percentile bootstrap, 10,000 resamples, deterministic bootstrap seed `20260823`, α=`0.05`. Exact cryptographic binding to the final frozen apparatus remains open.

## Remaining critical path

1. Establish the final experimental apparatus identity on top of the merged production source.
2. Authenticated P2 five-case runtime verification.
3. Authenticated P6a four-case CORS verification.
4. Candidate-scoped P3 artifact-contract execution evidence.
5. P4 blinding/custody verification.
6. P5 environment/topology/RNG reproducibility verification.
7. P6 durable archive/retrieval/hash verification.
8. P7 exact binding.
9. P8 exact binding and closure.
10. Independent P9 verification.
11. New immutable freeze and independent freeze verification.
12. Separate explicit pilot authorization.
13. Only then authorized blinded pilot execution.

**No freeze exists. No pilot is authorized. Empirical N = 0.**
