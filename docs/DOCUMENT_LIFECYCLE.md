---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL documentation control
last_verified: 2026-08-19
applies_to_sha: reconciliation branch; final main synchronization occurs after review
---

# Documentation Lifecycle Registry

This registry prevents documentation drift by making lifecycle state and authority explicit. It is the preferred place to determine whether a document is current, historical, superseded, or a template.

## Lifecycle states

- **ACTIVE** — current authoritative document for its stated scope.
- **SUPERSEDED** — retained for history but must not guide implementation or freeze decisions.
- **HISTORICAL** — factual record of a prior state; do not treat as current state.
- **TEMPLATE** — schema or preparation document intended to be populated later.

## Primary documents

| Document | Lifecycle | Authority | Scope / note |
|---|---|---|---|
| `docs/CURRENT_STATE.md` | ACTIVE | Both | Concise current repository/gate snapshot |
| `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | ACTIVE | Both | Detailed PDMAL operational control record |
| `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | ACTIVE / PRE-FREEZE | Both | Authoritative experimental protocol; remains unfrozen |
| `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` | ACTIVE | Both | Authoritative implementation workload specification |
| `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` | ACTIVE / INCORPORATED / PRE-FREEZE | Both | Accepted matrix amendment; does not authorize execution |
| `docs/evidence/PDMAL_EVIDENCE_INDEX.md` | ACTIVE | Both | Current evidence-to-control mapping |
| `docs/evidence/EVIDENCE_LADDER_POLICY.md` | ACTIVE | Both | Permanent evidence-promotion policy |
| `docs/experiment/FREEZE_MANIFEST_TEMPLATE.md` | TEMPLATE | Both | Preparation template for freeze metadata |
| `docs/experiment/FREEZE_MANIFEST.md` | ACTIVE / PRE-FREEZE | Both | Current freeze-control manifest; becomes the frozen manifest only after formal freeze |
| `docs/experiment/PDMAL_FREEZE_READINESS_RECONCILIATION.md` | ACTIVE / PRE-FREEZE | Both | Reconciliation record for final documentation/adjudication seams |
| `docs/DOCUMENT_LIFECYCLE.md` | ACTIVE | Both | Lifecycle registry itself |

## Task-specification history

The expert-panel review progressed through v0.7.0/v0.7.1/v0.7.2/v0.7.3 drafts before approving v0.7.4. Separate historical files for those drafts are not present in the current repository; therefore no nonexistent files are marked or invented. The review history is preserved in the governance record and repository commit history.

**Rule:** v0.7.4 is the only task specification authorized for implementation in the current branch.

## Authority rules

- GitHub source files and CI runs are authoritative for implementation and execution evidence.
- Notion records are authoritative for governance decisions, panel adjudication, and control-plane state.
- Historical documents remain useful for provenance but cannot override current active documents.
- A document marked `SUPERSEDED` or `HISTORICAL` must never be cited as the current implementation specification.
- NotebookLM is a research-synthesis/reference environment; material originating there has no evidentiary authority unless independently incorporated into an authoritative protocol, implementation, or evidence record.

## Update rule

Every material state change must update the active current-state/evidence records. Historical records are appended or superseded; they are not rewritten to erase prior evidence.
