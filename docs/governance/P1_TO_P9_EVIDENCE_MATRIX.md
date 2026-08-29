# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Current documentation/evidence lineage:** `main`  
**Experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**TGL contract remediation:** PR #134 current-main candidate; PR #132/#133 are closed historical remediation lanes  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface for P1–P9. It does not constitute executed evidence. Historical evidence remains scoped to the exact SHA/run/artifact that produced it. The TGL remediation candidate is a prerequisite/control repair and does not redefine the experimental apparatus or authorize execution.

## State precedence

`current verified executable boundary > documentation-only successors > historical candidate/freeze`

The current experimental verification boundary remains `ac8ea267…`. Documentation corrections and TGL remediation work must not silently rebind that boundary. A substantive apparatus change requires a new candidate identity and affected-predicate re-verification.

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
| P8 Analysis Lock | analysis/schema/runner/protocol bindings + candidate-scoped verification | **OPEN / FAIL-CLOSED** | all applicable P8 predicates evidenced and inspected, including TGL contract closure where applicable |
| P9 Independent Verification | independent reproduction/audit of identity, artifacts, analysis, invariants, adversarial cases | **NOT EXECUTED** | independent verifier passes without monoculture |

## TGL contract prerequisite

The pre-freeze contract suite exposed a substantive TGL/P-35 regression: 41 tests passed and 2 failed because the PR #132 implementation called `ProcludingPremiseGate` through an incompatible constructor/method contract and bypassed the established premise-hook injection path.

The remediation is now isolated in current-main PR #134 and is classified as **control-plane contract restoration**, not experimental authorization. Required closure includes:

- established P-35 constructor compatibility;
- `evaluate(..., check_fn=...)` callback injection;
- fail-closed exception containment;
- explicit required/conditional gate semantics;
- deterministic `PASS/WARN/SKIP/ESCALATE/KILL` reduction;
- distinction between unwired and dependency-suppressed `SKIP`;
- audit-seal coverage of the exact returned audit object;
- regression coverage for the above;
- exact candidate/source identity validation.

PR #132 and PR #133 are closed and must not be treated as authoritative executable state. PR #134 is the current remediation candidate and must not be treated as a freeze or authorization evidence merely because its tests pass.

## Supporting repository-native evaluator evidence

Governance CI run `33162492796` on exact tree `061286b1c17fe671cd5c58df025767befbeb55cd` retained repository-native evaluator results. These are `SYNTHETIC` / repository-authored evaluator-mechanism evidence only. They support implementation/evaluator correctness only; they do not close P1–P9, establish model-facing robustness, prove production reliability, establish DGAF/PDMAL efficacy, or change authorization/freeze state.

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

## Deployment evidence

The recorded experimental candidate deployment is supporting infrastructure evidence only. READY/health status does not substitute for authenticated P2/P6a matrices or establish efficacy. Exact source-to-runtime identity must be retained for any runtime closure.

## P7 adoption

The scientific decision remains adopted in substance. Its content is governance decision material, not empirical evidence, and remains pending exact cryptographic binding to the final freeze identity.

## P8 boundary

The P8 lock remains fail-closed. Analysis implementation, schema, runner, protocol, configuration, TGL contract prerequisites, and candidate identity must be reconciled before final freeze binding. Documentation-only successors do not silently inherit candidate evidence as new execution evidence.

## Remaining critical path

1. Close the TGL/P-35 contract prerequisite without altering the experimental boundary.
2. Validate the corrected candidate on its exact source tree.
3. Authenticated P2 five-case runtime verification.
4. Authenticated P6a four-case CORS verification.
5. Candidate-scoped P3 artifact-contract verification.
6. P4 blinding/custody verification.
7. P5 environment/topology/RNG reproducibility verification.
8. P6 durable archive/retrieval/hash verification.
9. P7 exact binding.
10. P8 exact binding and closure.
11. Independent P9 verification.
12. New immutable freeze and independent freeze verification.
13. Separate explicit pilot authorization.
14. Only then authorized blinded pilot execution.

**No freeze exists. No pilot is authorized. Empirical N = 0.**
