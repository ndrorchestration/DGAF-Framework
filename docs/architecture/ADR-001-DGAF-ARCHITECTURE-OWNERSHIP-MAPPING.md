# ADR-001 — DGAF Architecture Ownership and Mapping Method

**Status:** PROPOSED  
**Date:** 2026-09-28  
**Decision owner:** DGAF architecture governance  
**Scope:** DGAF repository architecture classification and drift control

## Context

DGAF contains a governance kernel, cross-cutting assurance mechanisms, multiple research/assurance profiles, UI projections, retained historical artifacts, and external execution integrations.

Several artifacts use similar words—authorization, verification, state, replay, custody, freeze, recovery—while operating at different scopes. A file-by-file documentation-only approach risks:
- accidental dual authority;
- treating profile specialization as duplication;
- treating observers as authority;
- conflating runtime and scientific states;
- rewriting historical evidence;
- allowing new control engines to emerge without explicit ownership.

The repository therefore needs a repeatable architecture ownership method with machine-checkable drift detection.

## Decision

DGAF uses the architecture method defined in:
- `DGAF_SYSTEM_ARCHITECTURE_TAXONOMY.md`;
- `DGAF_CORE_COMPONENT_INVENTORY.md`;
- `DGAF_ARCHITECTURE_MAPPING_METHOD.md`.

The canonical internal owners are:
- K1–K8 governance-kernel components;
- A1–A4 cross-cutting assurance components;
- P-* governed profiles;
- X-* external integrations.

Every active architecture-sensitive artifact has exactly one primary owner and may declare multiple secondary dependencies.

Architecture overlap is classified before remediation as:
- O1 TRUE_DUPLICATE_AUTHORITY;
- O2 PROFILE_SPECIALIZATION;
- O3 ADAPTER_OR_IMPLEMENTATION_VARIANT;
- O4 HISTORICAL_OR_SUPERSEDED;
- O5 ASSURANCE_OBSERVER;
- O6 ORPHAN_OR_AMBIGUOUS.

High-risk unmapped authority candidates are architecture-review priorities. Advisory scanners remain advisory until their false-positive behavior is sufficiently understood.

## Consequences

### Positive
- authority ownership becomes explicit;
- profile-specific controls can remain specialized without being mistaken for parallel DGAF kernels;
- historical provenance is preserved;
- significant ownership changes become reviewable;
- drift can be detected automatically;
- current-facing architecture can be generated from source registries rather than maintained only as prose.

### Costs
- registry maintenance is required for architecture-sensitive changes;
- some artifacts need interpretation rather than filename-based classification;
- profile and assurance inventories will grow over time;
- automated scanners require tuning before they are safe as blocking gates.

## Supersession rule

If K1–K8/A1–A4 ownership, the one-primary-owner rule, or the overlap taxonomy changes materially, create a new ADR and supersede this one rather than rewriting the accepted decision history.

## Evidence at proposal

At exact branch head `e8600bc63426de6ba3c5b984cdd456a9d5e3d079`:
- core component registry: PASS;
- artifact ownership registry: PASS (44 records);
- focused architecture/capability tests: 52 passed;
- advisory scanner: HIGH_UNMAPPED=0;
- remaining candidates are profile, medium, and assurance classes.

This is same-system engineering evidence and does not constitute independent validation.

## Non-effect

This ADR changes no runtime authority, experimental state, scientific N, efficacy, independent-validation state, production readiness, or High-Assurance authorization.
