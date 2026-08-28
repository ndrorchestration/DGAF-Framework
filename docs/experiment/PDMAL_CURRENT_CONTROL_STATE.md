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
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is not the corrected-apparatus freeze |
| Current verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` |
| Corrected runner | CANDIDATE | Explicit `ffcr_success`, schema validation, sidecar verification, and matrix coordinates are implemented; execution evidence remains pending |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN FOR FREEZE BINDING | Primary contrast selected; exact protocol/candidate/freeze binding remains required |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation/configuration controls exist; candidate-scoped execution evidence is incomplete |
| Candidate CI evidence | OPEN | Required applicable CI/test runs must execute against the exact candidate and be retained |
| Artifact contract | PARTIAL | End-to-end semantics and adversarial tests exist; fresh candidate evidence required |
| Blinding custody | PARTIAL | Synthetic/control evidence exists; operational custody and unblinding procedure remain evidence-bound |
| Durable retention | OPEN | Archive destination plus independent retrieval/hash proof required |
| Runtime-dependent verification | PARTIAL / APPLICABILITY REQUIRED | Candidate-scoped P2/P6a evidence or a pre-specified justified applicability decision is required |
| P9 independent verification | NOT EXECUTED | Must be independent of candidate self-validation |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## Candidate and documentation boundary

The current verification boundary is `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. Documentation-only commits may clarify verification records but do not redefine the apparatus. A substantive protocol, analysis, runner, artifact, or evidence change creates a new candidate cycle.

Historical references must retain the identity of what was actually examined. Zero-count cleanup is not a valid reason to rewrite historical provenance.

## P7 boundary

P7 is **technically adjudicated but formally open for freeze binding**. The primary treatment/reference boundary — full `dgaf` versus `null` — is selected, and FFCR is the primary outcome with seed as the paired analysis unit. Formal closure for the experimental freeze still requires exact candidate/protocol/analysis binding and the remaining governance predicates. P7 content must not be treated as empirical evidence or authorization.

## P8 boundary

P8 is explicitly fail-closed. Candidate implementation work—including analysis code, explicit FFCR artifact semantics, adversarial contract tests, CI wiring, and candidate bindings—does not close P8 until the applicable checklist items have executed candidate-scoped evidence.

Required evidence includes, as applicable:

1. Governance CI/test hierarchy on exact candidate `ac8ea267...`.
2. Analysis, artifact-schema/security, and compilation evidence with retained run identity and inspected logs.
3. Executed-tree reconciliation with P8 bindings.
4. Environment, topology fingerprint, seed/RNG separation, and trial-ordering evidence.
5. Durable retention plus independent retrieval/hash verification.
6. Blinding custody evidence that does not expose the key.

## Independent audit and authorization boundary

Independent verification should include adversarial preflight appropriate to the candidate's claims, including candidate identity reconciliation, artifact substitution resistance, blinding-boundary checks, and enforcement of relevant runtime constraints. Independent audit must not merely repeat candidate self-validation through the same assumptions.

Authorization is considered only after the required predicate evidence and freeze boundary are satisfied. Freeze is not authorization; authorization is not empirical efficacy.

## Required next evidence events

1. Execute and inspect applicable CI/test workflows against exact candidate `ac8ea267...`.
2. Retain run IDs, exact SHA/ref/event, logs, and artifact integrity values.
3. Complete durable evidence custody with independent retrieval/hash proof.
4. Complete operational blinding custody and formal unblinding readiness without exposing the key.
5. Resolve runtime verification applicability or retain the relevant predicate OPEN.
6. Reconcile topology, environment, seed/RNG, and analysis bindings against the exact candidate.
7. Derive P1–P8 only from candidate-scoped evidence.
8. Create an immutable freeze after pre-freeze closure.
9. Perform independent/adversarial verification of the frozen candidate.
10. Obtain explicit pilot authorization before empirical execution.

**No empirical execution is authorized by this record. N = 0. Authorization is NOT GRANTED.**
