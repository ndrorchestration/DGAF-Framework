# Documentation Reconciliation — 2026-08-21

## Purpose

This record documents the repository-wide documentation consistency pass performed on 2026-08-21. It distinguishes **living/current documentation** from **historical evidence** so that provenance is preserved without allowing stale records to masquerade as current state.

## Current authority

Resolve current state from:

1. `docs/CURRENT_STATE.md`
2. `docs/PROJECT_STATUS.md`
3. `docs/governance/TEST_EXECUTION_READINESS_2026-08-21.md`
4. `docs/governance/P3_P4_P5_P6_FREEZE_READINESS_2026-08-21.md`
5. `docs/governance/P7_PRIMARY_CONTRAST_ADJUDICATION_PACKET_2026-08-21.md`
6. `docs/governance/FREEZE_PACKET_TEMPLATE.md`
7. `docs/governance/CANDIDATE_RUNTIME_VERIFICATION_2026-08-21.md` for the historical candidate snapshot only

GitHub is authoritative for implementation/CI. Governance decisions remain a separate authorization layer.

## Reconciled living documents

The following were updated to remove stale current-state assertions or clarify temporal scope:

- `README.md` — current pre-freeze state, gate board, historical evidence boundary, terminology correction.
- `docs/PROJECT_STATUS.md` — current gate board and closure sequence.
- `docs/CURRENT_STATE.md` — current predicates and historical/candidate boundaries.
- `docs/experiment/P2_RUNTIME_VERIFICATION.md` — historical runtime evidence separated from current candidate verification.
- `docs/experiment/P6a_CORS_VERIFICATION.md` — historical verified deployment separated from current candidate verification.
- `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` — FLAG-02 temporal namespace and 340% claim status reconciled.
- `SESSION_ANCHOR.md` — explicitly classified as historical while preserving its session record.
- `docs/SESSION_ANCHORS.md` — explicitly classified as historical while preserving S069–S072 provenance.
- `docs/governance/CANDIDATE_RUNTIME_VERIFICATION_2026-08-21.md` — explicitly classified as a historical candidate snapshot because later documentation commits moved `main`.

## Historical documentation policy

Historical documents are **not** automatically rewritten to match current state. Their original terminology, decisions, and claims may be retained when needed for provenance. They must, however, be clearly identifiable as historical when a current reader could otherwise mistake them for active governance.

Examples include:

- S069/S070/S071/S072 session records;
- historical P2 and P6a execution records;
- historical freeze records;
- old candidate/deployment snapshots;
- audit records documenting former terminology or former gate states.

## FLAG-02 namespace reconciliation

The repository now uses a temporal vocabulary:

```text
Historical FLAG-02
    = historical identifier associated with the former 340% coordination-gain claim

Current qualitative
    = current canonical evaluation-mode terminology

New documents
    = must not introduce FLAG-02 as a current identifier
```

A historical occurrence is not itself a defect. A current document presenting FLAG-02 as an active current label is a defect.

## 340% coordination-gain reconciliation

The former 340% claim is not a current verified result. Historical occurrences may remain when explicitly historical. Current occurrences require contextual qualification and provenance.

The propagation checker is an **advisory QA control**, not an epistemic closure predicate. Proximity-based qualification cannot establish semantic applicability by itself.

## Historical deployment boundary

The following evidence remains valid only for its exact original source/deployment:

- P2 historical execution: `e1f077f` / `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7`
- P6a historical execution: `e1f077f` / `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7`
- historical freeze: `3510b86889cd341f7a7cf9ab684fd37b2fafd758`
- historical candidate snapshot: `94fb6fd...` / `dpl_G5uLJy8gibitJ6xRbQNfn3PYVm5F`

None is the current freeze or a substitute for fresh current-candidate execution evidence.

## Current gate statement

As of this reconciliation:

- P1 — PARTIAL
- P2 — PARTIAL
- P3 — PARTIAL
- P4 — PARTIAL
- P5 — PARTIAL
- P6 — OPEN
- P7 — PARTIAL; primary contrast OPEN
- P8 — OPEN
- P9 — NOT EXECUTED
- New freeze — NOT CREATED
- Pilot authorization — NOT GRANTED
- Empirical N — 0

## Test/documentation boundary

Test definitions, scripts, and workflows may be present without corresponding execution evidence. Documentation must therefore distinguish:

`DEFINED` / `IMPLEMENTED` / `TEST AVAILABLE` / `EXECUTED` / `PASS` / `VERIFIED` / `HISTORICAL` / `OPEN` / `NOT EXECUTED`.

No documentation update in this reconciliation promotes a predicate merely because implementation exists.

## Completion criterion

Documentation reconciliation is considered complete when:

1. current-state documents agree on the gate board;
2. historical evidence is temporally bounded;
3. FLAG-02 and the former 340% claim have explicit temporal semantics;
4. candidate/deployment identities are not presented as mutable current truth;
5. P2/P6a historical evidence cannot be mistaken for current evidence;
6. the repository's full-audit mechanism remains the authoritative path for literal file-coverage verification.

This record does not claim that every historical document has been rewritten. Preserving historical records is intentional and required for provenance.
