# Machine-Readable Document Control Specification v0.1

**Status:** PROPOSED  
**Scope:** documentation/governance metadata only  
**Scientific effect:** NONE  
**Authorization effect:** NONE

## Purpose

Define a small, machine-readable projection contract for documentation authority, handoff conformance, and threshold provenance without creating a second source of truth.

Machine-readable records are pointers/projections to an owning authority. They do not independently promote scientific, governance, implementation, deployment, or authorization state.

## Core record

```yaml
schema_version: "0.1"
record_id: stable-id
title: human-readable title
record_class: CURRENT_AUTHORITY | CURRENT_SUPPORTING | HISTORICAL | SUPERSEDED | AUDIT | PROVENANCE | EXPLORATORY
domain: project | portfolio | evidence | architecture | quality | experiment | vocabulary | pattern | ip | externalization
owner:
  authority_type: notion_page | github_repo | protocol | deployment | data_service
  authority_ref: exact-reference
scope: bounded-scope
lifecycle_state: controlled-value
epistemic_state: controlled-value-or-null
authorization_state: controlled-value-or-null
current_state_ref: exact-authority-pointer
evidence_refs: []
depends_on: []
blocks: []
supersedes: []
superseded_by: []
terminal_reason: value-or-null
last_verified_at: timestamp-or-null
next_gate: bounded-action-or-null
projection_state: VERIFIED | NOT_VERIFIED | STALE | INVALID
notes: []
```

`schema_version`, `record_id`, `record_class`, `domain`, `owner`, `scope`, `lifecycle_state`, `current_state_ref`, and `projection_state` are part of the base projection contract. `terminal_reason` is required only when a terminal/superseded record has no valid `superseded_by` reference. `notes` is explanatory only and MUST NOT carry authority that is absent from structured fields.

`last_verified_at` records verification of the projection itself, not merely the date its source document was edited. A `NOT_VERIFIED`, `STALE`, or `INVALID` projection SHOULD use `null` unless a separate verification-history field is introduced by a later schema version.

## Handoff extension

```yaml
handoff:
  standard_version: "0.1"
  profile: H1 | H2 | H3 | H4 | H5 | H6
  conformance: C0 | C1 | C2 | C3 | C4 | C5
  source_ref: exact-reference
  receiver_ref: exact-reference
  transformation_ref: exact-reference-or-null
  threshold_refs: []
  validation_state: controlled-value
  exception_refs: []
```

The H/C vocabulary mirrors the ecosystem **Cross-Disciplinary Handoff & Promotion Standard v0.1**, whose current lifecycle state is PILOTED rather than ADOPTED. Reusing these labels here does not adopt that standard or create a second owner for its semantics.

Profiles:

- **H1 — Empirical→Operational**
- **H2 — Evaluator→Governance**
- **H3 — Measurement/Data→Inference**
- **H4 — Pattern/Research→Implementation**
- **H5 — Implementation Evidence→Public Claim**
- **H6 — Novelty Hypothesis→Disclosure/Publication Decision**

Conformance classes:

- **C0 — DOCUMENTED:** owner and intended handoff identified.
- **C1 — CONTRACT-COMPLETE:** required handoff fields and semantics present.
- **C2 — SOURCE-VALIDATED:** source evidence or measurement semantics verified.
- **C3 — RECEIVER-VALIDATED:** receiving system validates assumptions and transformation.
- **C4 — OPERATIONALLY MONITORED:** rollback/monitoring and real-use evidence exist.
- **C5 — INDEPENDENTLY REVIEWED:** independent or structurally separated review completed.

C-level metadata records conformance evidence only. It MUST NOT be interpreted as a scientific grade, evidence strength outside the handoff scope, or authorization state. A higher C-level MUST NOT be inferred from a lower level.

## Threshold provenance extension

```yaml
threshold:
  threshold_id: stable-id
  value: scalar-or-structured
  units: explicit
  direction: explicit
  source_class: STANDARD_DERIVED | EMPIRICAL | ENGINEERING_HEURISTIC | PLACEHOLDER
  source_ref: exact-reference
  calibration_context: bounded-context
  version: semantic-version
  applies_to: exact-scope
  expires_or_review_trigger: value-or-null
```

A PLACEHOLDER or ENGINEERING_HEURISTIC threshold MUST NOT silently inherit EMPIRICAL status. `STANDARD_DERIVED` means derived from a named standard within the exact declared scope; it does not imply that the surrounding system is certified or conformant to that standard.

## Projection and extension rules

1. Core structured fields carry projection state; free-text `notes` cannot override them.
2. Optional extensions such as `handoff` and `threshold` add bounded metadata but do not replace the core authority pointer.
3. Unknown extension keys may be retained during the PROPOSED/R1 fixture phase, but a future R2 validator must either register them explicitly or classify the projection `NOT_VERIFIED` rather than silently accepting new semantics.
4. A projection must not copy mutable evidence, authorization, deployment, or scientific state when an exact pointer can be used instead.
5. If source and projection disagree, the canonical source controls and the projection becomes `STALE` or `INVALID`; the projection never wins by recency alone.

## Initial drift rules

A future validator should flag:

1. `CURRENT_AUTHORITY` without an owner/current-state pointer.
2. `SUPERSEDED` without `superseded_by` or an explicit `terminal_reason`.
3. Embedded mutable version/SHA state inconsistent with its owning authority.
4. Evidence or authorization copied through a dependency without an explicit handoff.
5. Thresholds without units, source class, or exact scope.
6. C2+ handoffs without source-validation evidence.
7. C3+ handoffs without receiver-validation evidence.
8. ADOPTED standards without an adoption decision and version owner.
9. External/public claims lacking required canonical claim/evidence references.
10. Historical records exposed as current-state navigation without a current-authority pointer.
11. A `VERIFIED` projection without `last_verified_at`.
12. A `NOT_VERIFIED`, `STALE`, or `INVALID` projection that presents a verification timestamp as current proof.
13. H/C labels whose meanings diverge from the referenced handoff-standard version.
14. Free-text notes that contradict structured authority, epistemic, authorization, or projection state.

## Rollout

- **R0 — Specification:** this document only.
- **R1 — Fixtures:** encode one current-authority record and representative H2/H3 records.
- **R2 — Validator:** schema validation plus adversarial fixtures; define closed/registered extension handling before any blocking use.
- **R3 — Report:** non-blocking drift report.
- **R4 — Enforcement:** promote only stable, low-false-positive rules to blocking CI.
- **R5 — Review:** measure maintenance burden and false positives before wider adoption.

## Anti-bureaucracy invariant

If maintaining metadata duplicates more mutable state than the automation eliminates, redesign the projection rather than expanding the schema.

## Fail-closed interpretation

Absence, invalidity, or staleness of this metadata does not demote or promote the owning system. It means the projection is **NOT VERIFIED**, **STALE**, or **INVALID** as applicable, and consumers must resolve the canonical owner directly.
