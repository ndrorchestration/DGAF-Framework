# NDR Registry Differentiation Index — HISTORICAL

**Status:** SUPERSEDED — historical migration record only  
**Superseded by:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
**Current cross-family architecture:** `docs/PATTERN_COMMONS_ARCHITECTURE.md`  
**Historical source state:** S066 / 2026-05-30

> This file is retained for provenance. It is **not** an active registry, pattern-number authority, merge plan, or source of truth.

## Current authority

- **NDR family:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`
- **Machine-readable NDR representation:** `docs/ndr_patterns_unified.json`
- **Cross-family identity/relationship model:** `docs/PATTERN_COMMONS_ARCHITECTURE.md`
- **DGAF orchestration-pattern namespace:** `registry/PATTERN_REGISTRY_v2.md`

The historical three-registry model described below has been superseded by the unified NDR registry. The distinct DGAF orchestration registry remains a separate namespace and must not be conflated with NDR P-series identity.

## Why this file remains

The original index documented the S066/S067 migration from several NDR registries into a unified representation. Its historical tables, planned actions, and pre-merge statuses are preserved in Git history and are intentionally no longer presented as current state.

In particular, the former instruction that new P-numbers "must be registered here first" is retired. New NDR identifiers are governed by the canonical unified registry and its release/reconciliation controls.

## Important non-equivalence

A shared word such as "registry," a similar filename, or overlapping terminology does not establish semantic equivalence. NDR patterns, DGAF orchestration patterns, external patterns, templates, agents, evidence records, and ecosystem indexes remain distinct artifact families unless their identity, scope, mechanism, provenance, and authority are explicitly reconciled.

## Historical disposition

- `docs/NDR_PATTERN_REGISTRY.md` → redirect/superseded
- `docs/patterns/NDR_PATTERN_REGISTRY.md` → superseded by unified NDR registry
- individual NDR runtime cards → archived/absorbed where applicable
- `patterns/ndr_patterns.json` → superseded by `docs/ndr_patterns_unified.json`
- this differentiation index → **historical only**
- `docs/NDR_REGISTRY_MERGE_PLAN.md` → historical migration record

No scientific, experimental, freeze, authorization, or empirical status is implied by this documentation cleanup.

---

*Historical migration record retained to preserve provenance. Do not use this document for current registry decisions.*
