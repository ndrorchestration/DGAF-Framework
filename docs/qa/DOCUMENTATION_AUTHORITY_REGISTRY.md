# Documentation Authority Registry

**Status:** ACTIVE  
**Last verified:** 2026-09-02  
**Purpose:** Prevent historical documentation, stale candidate identities, and dated evidence records from masquerading as current control authority.

## Authority classes

| Class | Meaning | May define current state? |
|---|---|---:|
| `LIVING_CONTROL` | Current control-plane state or living checklist | YES |
| `CURRENT_RECONCILIATION` | Current interpretation of historical evidence and current identity | YES, within stated scope |
| `EVIDENCE_RECORD` | Immutable record of a specific run/artifact/candidate | NO; historical truth only |
| `HISTORICAL` | Prior project state retained for provenance | NO |
| `RESEARCH` | Non-closing research/design material | NO |
| `REFERENCE` | Terminology, architecture, or policy reference | Only within its stated policy scope |

## Current authority map

| Path | Authority class | State | Candidate scope | Current-authority rule |
|---|---|---|---|---|
| `docs/CURRENT_STATE.md` | `LIVING_CONTROL` | CURRENT | Control plane | Canonical current-state resolution |
| `docs/experiment/NEW_CANDIDATE_MANIFEST.md` | `LIVING_CONTROL` | CURRENT CYCLE | Runtime candidate `92ff830b…` | Current-cycle manifest; historical candidates explicitly labeled |
| `docs/governance/P8_VERIFICATION_CHECKLIST.md` | `LIVING_CONTROL` | OPEN / FAIL-CLOSED | Current runtime + controlled completion candidate | Checklist only; no freeze/authorization effect |
| `docs/governance/P9_CURRENT_RECONCILIATION.md` | `CURRENT_RECONCILIATION` | CURRENT | `a43219b…` historical scoped PASS; successor reverify required | Current P9 interpretation record |
| `docs/governance/CURRENT_CANDIDATE_POST_KICKOFF_CONTROL_2026-09-01.md` | `CURRENT_RECONCILIATION` | CURRENT | `92ff830b…` and `a43219b…` | Current candidate-boundary reconciliation |
| `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md` | `CURRENT_RECONCILIATION` | CURRENT | Candidate-scoped matrix | Gate status summary; exact evidence remains authoritative |
| `docs/evidence/PDMAL_EVIDENCE_INDEX.md` | `EVIDENCE_RECORD` | ACTIVE INDEX | Multiple exact candidates | Evidence locator; candidate scope mandatory |
| `docs/governance/P7_BINDING_RECORD_2026-08-30.md` | `REFERENCE` | ADJUDICATION RECORD | P7 scientific specification | Scientific decision record; exact freeze binding remains open |
| `docs/substrate/NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md` | `RESEARCH` | SOURCE-INTEGRITY GAP | P-38 | Incomplete source; must not be treated as complete specification |
| `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` | `REFERENCE` | CANONICAL | Ecosystem vocabulary | Terminology/evidence-class policy |

## Historical naming rules

1. A historical candidate SHA may remain in a document only when its historical/superseded role is explicit in the same local context.
2. A historical document must not use an unqualified `latest`, `current`, `authoritative`, or equivalent label for a superseded candidate.
3. Dated evidence records are not automatically current merely because their filename contains `LATEST`.
4. Prefer `CURRENT_RECONCILIATION` for living interpretation and `EVIDENCE_RECORD`/`HISTORICAL` for immutable prior executions.
5. A documentation commit on `main` does not redefine experimental candidate identity unless an explicit candidate-designation record says so.
6. Evidence does not transfer between candidate SHA, tree, deployment, run, or artifact identities by conceptual equivalence.

## Required current-state vocabulary

The living control plane currently uses these distinctions:

- P7: **TECHNICALLY ADJUDICATED / FORMALLY OPEN**
- P8: **OPEN / FAIL-CLOSED**
- P9: **HISTORICAL SCOPED PASS / NEW CANDIDATE REVERIFY REQUIRED**
- Freeze: **NOT ESTABLISHED**
- Authorization: **NOT GRANTED**
- Empirical N: **0**

`ADOPTED / FINAL BINDING OPEN` must not be used as the current P7 state in living control documents; historical records may quote that earlier wording when explicitly labeled historical.

## P-38 source-integrity boundary

`NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md` is intentionally marked incomplete at the recovered source boundary. The repository does not currently possess an authoritative remainder. No missing text is to be reconstructed from inference. Issue #122 remains the recovery record.

## Automation contract

`scripts/lint_document_authority.py` checks the living documentation surface against `docs/CURRENT_STATE.md`. It is a semantic freshness check, not a markdown presentation linter. It must fail on:

- unqualified superseded completion-candidate identities;
- obsolete current P7 wording in living surfaces;
- living cross-references to the deprecated P9 `LATEST` authority record;
- living documents that assert freeze/authorization/N>0 contrary to current control state.

False positives in immutable historical/evidence records must be suppressed by explicit authority classification, not by silently ignoring the mismatch.
