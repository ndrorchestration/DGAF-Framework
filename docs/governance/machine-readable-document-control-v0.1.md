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
last_verified_at: timestamp-or-null
next_gate: bounded-action-or-null
```

## Handoff extension

```yaml
handoff:
  standard_version: 0.1
  profile: H1 | H2 | H3 | H4 | H5 | H6
  conformance: C0 | C1 | C2 | C3 | C4 | C5
  source_ref: exact-reference
  receiver_ref: exact-reference
  transformation_ref: exact-reference-or-null
  threshold_refs: []
  validation_state: controlled-value
  exception_refs: []
```

C-level metadata records conformance evidence only. It MUST NOT be interpreted as a scientific grade or authorization state.

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

A PLACEHOLDER or ENGINEERING_HEURISTIC threshold MUST NOT silently inherit EMPIRICAL status.

## Initial drift rules

A future validator should flag:

1. `CURRENT_AUTHORITY` without an owner/current-state pointer.
2. `SUPERSEDED` without `superseded_by` or an explicit terminal reason.
3. Embedded mutable version/SHA state inconsistent with its owning authority.
4. Evidence or authorization copied through a dependency without an explicit handoff.
5. Thresholds without units, source class, or exact scope.
6. C2+ handoffs without source-validation evidence.
7. C3+ handoffs without receiver-validation evidence.
8. ADOPTED standards without an adoption decision and version owner.
9. External/public claims lacking required canonical claim/evidence references.
10. Historical records exposed as current-state navigation without a current-authority pointer.

## Rollout

- **R0 — Specification:** this document only.
- **R1 — Fixtures:** encode one current-authority record and representative H2/H3 records.
- **R2 — Validator:** schema validation plus adversarial fixtures.
- **R3 — Report:** non-blocking drift report.
- **R4 — Enforcement:** promote only stable, low-false-positive rules to blocking CI.
- **R5 — Review:** measure maintenance burden and false positives before wider adoption.

## Anti-bureaucracy invariant

If maintaining metadata duplicates more mutable state than the automation eliminates, redesign the projection rather than expanding the schema.

## Fail-closed interpretation

Absence, invalidity, or staleness of this metadata does not demote or promote the owning system. It means the projection is **NOT VERIFIED** and consumers must resolve the canonical owner directly.
