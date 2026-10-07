# DGAF Architecture-Control Lifecycle Vocabulary

**Status:** ACTIVE_NON_AUTHORIZING / DOCUMENT-LIFECYCLE CONTROL / NON-AUTHORIZING  
**Date:** 2026-09-28  
**Scope:** architecture-control documents, registries, ADRs, and related classification metadata

## Purpose

Define lifecycle labels for DGAF architecture-control artifacts without conflating repository adoption with scientific validation, runtime authorization, independent validation, or High-Assurance authorization.

This vocabulary controls only the lifecycle of architecture documentation and machine-readable architecture-control metadata.

## Core separation

Architecture lifecycle state is separate from:

- scientific/experimental state;
- runtime authorization state;
- independent-validation state;
- evidence class;
- High-Assurance authorization;
- production-readiness claims.

A document may be current and active while the system it describes remains unvalidated, non-authorized, or fail-closed.

## Controlled lifecycle states

### PROPOSED

Use when an architecture-control artifact has been authored but has not yet been adopted into the repository's current architecture-control baseline.

Meaning:

- candidate architecture/control metadata;
- review may still alter its normative role;
- not yet part of the current accepted repository architecture baseline.

### ACTIVE_NON_AUTHORIZING

Use for current architecture-control artifacts that are part of the repository's active architecture baseline but have no direct runtime, scientific, or authorization effect.

Typical examples:

- architecture taxonomy;
- component inventory;
- mapping method;
- machine-readable ownership/profile/assurance registries;
- architecture boundary records;
- architecture debt register.

This state means "current architecture metadata" only.

It does **not** mean:

- scientifically validated;
- independently validated;
- runtime-authorized;
- production readiness established;
- High-Assurance authorized.

### ACCEPTED

Use only for an Architecture Decision Record when the decision has been adopted as the current repository architecture decision.

An accepted ADR records a decision, not a scientific validation result.

### REJECTED

Use only for a decision record whose proposed architecture decision was explicitly considered and declined.

Retain for provenance. Do not rewrite history as though it were never proposed.

### SUPERSEDED

Use when a later architecture-control artifact or ADR explicitly replaces the current meaning of the artifact.

Requirements:

- name the successor;
- preserve the superseded artifact;
- do not silently rewrite historical decision state.

### HISTORICAL

Use for retained architecture material that is no longer current but remains relevant for lineage, reconstruction, or provenance and is not necessarily replaced by one direct successor.

### RETIRED

Use when an architecture-control artifact is intentionally withdrawn from active architecture use and no longer participates in current control interpretation.

Retirement must not delete evidence-bearing history.

## Transition rules

Allowed ordinary transitions:

```text
PROPOSED -> ACTIVE_NON_AUTHORIZING
PROPOSED -> ACCEPTED              # ADR only
PROPOSED -> REJECTED              # ADR only

ACTIVE_NON_AUTHORIZING -> SUPERSEDED
ACTIVE_NON_AUTHORIZING -> HISTORICAL
ACTIVE_NON_AUTHORIZING -> RETIRED

ACCEPTED -> SUPERSEDED            # ADR only
ACCEPTED -> HISTORICAL            # ADR only where appropriate
```

Do not infer a transition merely because:

- a file exists on a branch;
- CI is green;
- a PR is mergeable;
- a scientific gate passed;
- a runtime adapter executed;
- a deployment exists.

Repository adoption should be evidenced by an accepted/merged repository change at the exact applicable scope.

## Artifact-class guidance

| Artifact class | Normal current state |
|---|---|
| Architecture taxonomy / mapping / inventory | `ACTIVE_NON_AUTHORIZING` |
| Machine-readable architecture registry | `ACTIVE_NON_AUTHORIZING` |
| Architecture boundary/alignment record | `ACTIVE_NON_AUTHORIZING` when adopted |
| ADR before decision adoption | `PROPOSED` |
| Current adopted ADR | `ACCEPTED` |
| Declined ADR | `REJECTED` |
| Replaced ADR or architecture record | `SUPERSEDED` |
| Lineage-only retained architecture material | `HISTORICAL` |
| Intentionally withdrawn control artifact | `RETIRED` |

## Non-authority invariant

Architecture lifecycle labels MUST NOT be used as aliases for scientific or execution authority.

The following remain independent and must be sourced from their own governed records:

```text
SCIENTIFIC_N_INCREMENT
INDEPENDENT_VALIDATION
CANONICAL_DGAF_EFFICACY
HIGH_ASSURANCE
runtime authorization
experimental gate state
```

For example:

```text
architecture_lifecycle = ACTIVE_NON_AUTHORIZING
INDEPENDENT_VALIDATION = NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED
HIGH_ASSURANCE = NOT_AUTHORIZED
```

is valid and expected.

## Reconciliation rule for PR #1089 artifacts

PR #1089 established the architecture ownership taxonomy and related control artifacts on protected `main`.

That merge is sufficient evidence to review the affected current architecture-control documents for transition from `PROPOSED` to either:

- `ACTIVE_NON_AUTHORIZING` for current non-ADR architecture-control artifacts; or
- `ACCEPTED` for ADR-001 if the repository treats the merged architecture decision as adopted.

This document does not itself perform those transitions.

## Validation guidance

A future validator may check:

1. allowed lifecycle values;
2. ADR-only use of `ACCEPTED` and `REJECTED`;
3. required successor metadata for `SUPERSEDED`;
4. separation of lifecycle state from scientific/authorization fields;
5. current architecture-control files do not retain stale `PROPOSED` labels after explicit adoption.

The current advisory validator is `scripts/validate_dgaf_architecture_lifecycle.py`. It checks an explicit adopted-baseline set rather than recursively promoting every file under `docs/architecture/`. Historical and genuinely proposed material therefore remain outside the baseline unless adoption is separately evidenced.

The validator remains advisory while its baseline coverage, historical exclusions, and false-positive behavior are evaluated.

## Boundary

This vocabulary is documentation/architecture metadata only.

It does not change runtime authority, experimental state, scientific N, efficacy, independent-validation state, production readiness, or High-Assurance authorization.
