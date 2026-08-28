# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED
**Current verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
**Documentation successor(s):** do not redefine the executable boundary
**Empirical N:** `0`
**Pilot authorization:** `NOT GRANTED`
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface for P1–P9. It does not constitute executed evidence. Historical evidence remains scoped to the exact SHA/run/artifact that produced it.

## State precedence

`current verified executable boundary > documentation-only successors > historical candidate/freeze`

The historical executable candidate `e6beeb66335e1b50a239697badab22dab50eb5ba` remains provenance only for current freeze decisions. The current experimental verification boundary is `ac8ea267…`.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact current-tree identity and provenance | **OPEN** | current candidate retained and independently reconciled |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **BLOCKED / OPEN** | matrix passes with exact candidate/deployment identity |
| P3 Artifact Contract | schema/identity/uniqueness/balance/canonical matrix/deviation integrity | **OPEN** | current candidate-scoped evidence retained |
| P4 Security / Blinding | custody, bijection, access separation, operational procedure | **OPEN** | operational evidence retained and independently checked |
| P5 Provenance / Reproducibility | environment/toolchain/topology/RNG fingerprints and reproduction | **OPEN** | current candidate evidence retained |
| P6 Durable Evidence Custody | archive → independent retrieval → hash verification | **BLOCKED / OPEN** | end-to-end current evidence verified |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **BLOCKED / OPEN** | matrix passes on same deployment as P2 |
| P7 Scientific Target | adopted scientific decision + exact binding | **ADOPTED / BINDING PENDING** | adopted record cryptographically bound to exact frozen protocol/apparatus/analysis/freeze identity |
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced and inspected |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without monoculture |

## Supporting repository-native evaluator evidence

Governance CI run `33162492796` on exact tree `061286b1c17fe671cd5c58df025767befbeb55cd` retained the current repository-native evaluator results:

- `role_boundary_coherence`: 10/10
- `governance_schema_conformance`: 1000/1000, deterministic seed `20260828`
- `contraction_proof_fidelity`: 100/100
- `evaluation_integrity_fixture_suite`: 12/12 across six registered threat classes

These results are `SYNTHETIC` / repository-authored evaluator-mechanism evidence. They support implementation/evaluator correctness only; they do not close P1–P9, establish model-facing robustness, prove production reliability, establish DGAF/PDMAL efficacy, or change authorization/freeze state.

## Additional freeze-admissibility predicates

| Predicate | Requirement | State |
|---|---|---|
| E2b | immutable verifier-toolchain runtime/dependency/workflow/environment fingerprint | **CLOSED / VERIFIED** for its recorded exact execution boundary |
| M6 | machine-retained proof of N=0/no authorization/no pilot/no unblinding | **CLOSED / VERIFIED** for Governance CI run `33050398324` on `ac8ea267…` |

### M6 retained evidence

- Run: `33050398324`
- Exact executed candidate/tree: `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
- Retained artifact digest: `sha256:dabe2f1909535671e795bb8c1cad0ef0840be4732acebff8f1a340c62b4943b6`
- Independently recomputed digest: **MATCH**
- Observed N: `0`
- Authorization: `NOT_GRANTED`
- Freeze: `NOT_CREATED`
- Pilot invocation: `false`

## Current deployment evidence

The exact experimental candidate deployment is READY and source-bound to `ac8ea267…`, with `/api/health` returning HTTP 200. This is deployment/health evidence and is not a substitute for authenticated P2/P6a matrices.

## P7 adoption

The scientific decision is formally adopted by the designated experimental-control authority in commit `98db6563aad9a7afb45cdd064172efa7f221ef0d`. Its content is governance decision material, not empirical evidence. The adopted decision remains pending exact cryptographic binding to the final freeze identity.

## P8 boundary

The P8 lock has been reconciled to the experimental verification boundary. Analysis implementation, schema, runner, protocol, and configuration must be cryptographically rebound in the eventual freeze packet. Documentation-only successors do not silently inherit candidate evidence as new execution evidence.

## Remaining critical path

1. Authenticated P2 five-case runtime verification.
2. Authenticated P6a four-case CORS verification.
3. Candidate-scoped P3 artifact-contract verification.
4. P4 blinding/custody verification.
5. P5 environment/topology/RNG reproducibility verification.
6. P6 durable archive/retrieval/hash verification.
7. P8 exact binding and closure.
8. Independent P9 verification.
9. New immutable freeze and independent freeze verification.
10. Separate explicit pilot authorization.
11. Only then authorized blinded pilot execution.

**No freeze exists. No pilot is authorized. Empirical N = 0.**
