---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-28
applies_to_sha: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is provenance only |
| Current verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| Exact-tree E2b | CLOSED / VERIFIED | Exact-tree run `33047380487` is valid for `d299dd152…`; the corrected workflow boundary is separately scoped and must not be conflated with that historical exact-tree record |
| Exact-candidate M6 | CLOSED / VERIFIED | Governance CI run `33050398324`; exact candidate `ac8ea267…`; retained negative-state artifact independently hash-verified with digest `sha256:dabe2f1909535671e795bb8c1cad0ef0840be4732acebff8f1a340c62b4943b6` |
| Corrected runner | CANDIDATE | Explicit `ffcr_success`, schema validation, sidecar verification, and matrix coordinates are implemented; empirical execution evidence remains absent |
| TGL contract | BLOCKED / ADVERSARIAL REVIEW | PR #132 produced a 41-pass / 2-fail regression at the TGL → P-35 boundary; PR #133 is the isolated remediation candidate |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN FOR FREEZE BINDING | Primary contrast selected; exact protocol/candidate/freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation/configuration controls exist; complete candidate-scoped closure package remains incomplete |
| Candidate governance verification | PARTIALLY CLOSED | Exact-scope E2b/M6 are closed for their stated boundaries; later repository documentation commits do not inherit that evidence automatically |
| Artifact contract | PARTIAL | End-to-end semantics and adversarial tests exist; fresh candidate-scoped evidence for the full artifact contract remains required |
| Blinding custody | PARTIAL | Synthetic/control evidence exists; operational custody and unblinding procedure remain evidence-bound |
| Durable retention | OPEN | Archive destination plus independent retrieval/hash proof required |
| Runtime-dependent verification | PARTIAL / APPLICABILITY REQUIRED | Candidate-scoped P2/P6a evidence or a pre-specified justified applicability decision is required |
| P9 independent verification | NOT EXECUTED | Must be independent of candidate self-validation |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## TGL / P-35 remediation boundary

PR #132 remains blocked and must not be treated as an experimental apparatus identity. The 41-pass / 2-fail result is a concrete contract-regression signal. The identified defects include P-35 constructor/method incompatibility, missing premise-hook injection, weakened exception containment, incomplete status reduction, ambiguous SKIP semantics, and audit-seal sequencing.

PR #133 is an isolated remediation candidate. Its scope is limited to restoring the established TGL/P-35 contract and adding regression coverage. It does not authorize pilot execution, create a freeze, change the PDMAL treatment, or advance empirical N.

TGL must distinguish unwired required-gate `SKIP` from dependency-caused or intentionally non-applicable `SKIP`. Requiredness should be declared rather than inferred solely from step numbers. The final audit seal must represent exactly the authoritative audit object returned to downstream consumers.

## Candidate and documentation boundary

The current verification boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Documentation-only commits may clarify verification records but do not redefine the apparatus. A substantive protocol, analysis, runner, artifact, or evidence change creates a new candidate cycle.

Historical references must retain the identity of what was actually examined. Zero-count cleanup is not a valid reason to rewrite historical provenance.

## P7 boundary

P7 is **technically adjudicated but formally open for freeze binding**. The primary treatment/reference boundary — full `dgaf` versus `null` — is selected, and FFCR is the primary outcome with seed as the paired analysis unit. Formal closure for the experimental freeze still requires exact candidate/protocol/analysis binding and the remaining governance predicates. P7 content must not be treated as empirical evidence or authorization.

## P8 boundary

P8 is explicitly fail-closed. Candidate implementation work—including analysis code, explicit FFCR artifact semantics, adversarial contract tests, CI wiring, and candidate bindings—does not close P8 until the applicable checklist items have executed candidate-scoped evidence.

## Independent audit and authorization boundary

Independent verification should include adversarial preflight appropriate to the candidate's claims, including candidate identity reconciliation, artifact substitution resistance, blinding-boundary checks, and enforcement of relevant runtime constraints. Independent audit must not merely repeat candidate self-validation through the same assumptions.

Authorization is considered only after the required predicate evidence and freeze boundary are satisfied. Freeze is not authorization; authorization is not empirical efficacy.

## Required next evidence events

1. Resolve the TGL/P-35 contract blocker through the isolated remediation candidate and exact-head validation.
2. Complete P7 exact candidate/protocol/analysis binding.
3. Complete remaining P8 artifact, environment, reproducibility, custody, and runtime-dependent evidence.
4. Complete authenticated P2/P6a where required, using the exact candidate/deployment identity.
5. Retain run IDs, exact SHA/ref/event, logs, and artifact integrity values.
6. Complete durable evidence custody with independent retrieval/hash proof.
7. Complete operational blinding custody and formal unblinding readiness without exposing the key.
8. Prepare and execute independent P9 verification.
9. Derive the complete pre-freeze predicate matrix only from candidate-scoped evidence.
10. Create an immutable freeze after pre-freeze closure.
11. Independently verify the freeze.
12. Obtain explicit pilot authorization before empirical execution.

**No empirical execution is authorized by this record. N = 0. Authorization is NOT GRANTED.**
