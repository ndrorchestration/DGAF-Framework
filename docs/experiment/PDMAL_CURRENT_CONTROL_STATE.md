---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-24
applies_to_sha: CURRENT_MAIN_AT_VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` is not the corrected-apparatus freeze |
| Exact P8 verification candidate | IDENTIFIED | `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` per the fail-closed P8 checklist |
| Corrected runner | CANDIDATE | Explicit `ffcr_success`, schema validation, sidecar verification, and matrix coordinates are implemented |
|| P7 scientific specification | TECHNICALLY ADJUDICATED / PROPOSED AUTHORITATIVE SPECIFICATION / FORMALLY OPEN | Panel-ready record presents all 11 decisions as OPEN / PENDING AUTHORITY ADOPTION; primary contrast (DGAF vs null) selected but formal adoption not evidenced; see `P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md` for decision-level breakdown | P7 record (`P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md`) + traceability matrix | P8 analysis lock must not claim scientific closure beyond the OPEN P7 state |
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

The current P8 verification checklist names `2a80f819...` as the exact candidate tree. Documentation-only commits after that candidate may clarify verification records but do not redefine the apparatus. A substantive protocol, analysis, runner, artifact, or evidence change creates a new candidate cycle.

Historical references must retain the identity of what was actually examined. Zero-count cleanup is not a valid reason to rewrite historical provenance.

## P7 boundary

P7 is **technically adjudicated as a proposed authoritative scientific specification, but formally OPEN pending authority adoption and candidate binding.** The panel-ready P7 adjudication record (`P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md`) presents proposals for all 11 scientific decisions. The primary treatment/reference boundary — the full `dgaf` condition versus `null` — has been selected in prior reconciliation, and FFCR is the primary outcome with seed as the independent paired analysis unit. However, formal authority adoption has not occurred, the adopted record has not been bound to the exact candidate, and none of the five formal closure conditions in the P7 record are satisfied.

## P8 boundary

P8 is explicitly fail-closed. Candidate implementation work—including analysis code, explicit FFCR artifact semantics, adversarial contract tests, CI wiring, and candidate bindings—does not close P8 until the applicable checklist items have executed candidate-scoped evidence.

Required evidence includes, as applicable:

1. Governance CI/test hierarchy on exact candidate `2a80f819...`.
2. Analysis, artifact-schema/security, and compilation evidence with retained run identity and inspected logs.
3. Executed-tree reconciliation with P8 bindings.
4. Environment, topology fingerprint, seed/RNG separation, and trial-ordering evidence.
5. Durable retention plus independent retrieval/hash verification.
6. Blinding custody evidence that does not expose the key.

## Independent audit and authorization boundary

Independent verification should include adversarial preflight appropriate to the candidate's claims, including candidate identity reconciliation, artifact substitution resistance, blinding-boundary checks, and enforcement of relevant runtime constraints. Independent audit must not merely repeat candidate self-validation through the same assumptions.

Authorization is considered only after the required predicate evidence and freeze boundary are satisfied. Freeze is not authorization; authorization is not empirical efficacy.

## Required next evidence events

1. Execute and inspect applicable CI/test workflows against exact candidate `2a80f819...`.
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
