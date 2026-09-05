# NDR Pattern Registry — Unified Merge Plan — HISTORICAL

**Status:** SUPERSEDED — completed migration record only  
**Canonical registry:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
**Machine-readable counterpart:** `docs/ndr_patterns_unified.json`  
**Cross-family architecture:** `docs/PATTERN_COMMONS_ARCHITECTURE.md`  
**Historical plan state:** S066/S067 · 2026-05-30

> This document records the migration plan that produced the unified NDR registry. It is retained for provenance and is **not an open work queue**.

## Disposition

The planned consolidation of the NDR pattern registries has been executed. The unified Markdown registry now declares itself the canonical NDR family source of truth and records the absorbed legacy registries and cards. The machine-readable registry is maintained as the corresponding structured representation.

The former Phase 3/Phase 4 actions below are therefore historical. They must not be reopened merely because this file still contains the original plan language.

## Historical source set

- `docs/NDR_PATTERN_REGISTRY.md` → redirect/superseded
- `docs/patterns/NDR_PATTERN_REGISTRY.md` → superseded by unified registry
- `patterns/NDR_SCPE_v1.md` → archived/absorbed where applicable
- `patterns/NDR_PHI_CLOSURE_GATE_v1.md` → archived/absorbed where applicable
- `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` → archived/absorbed where applicable
- `patterns/ndr_patterns.json` → superseded by `docs/ndr_patterns_unified.json`

## Historical merge phases

### Phase 1 — Pre-merge blockers

PM-01, PM-02, PM-05, and PM-07 were recorded as closed in the original plan.

### Phase 2 — Soft pre-merge

PM-03 and PM-04 were recorded as closed in the original plan.

### Phase 3 — Merge execution

The original plan called for creation of the unified Markdown/JSON pair, Triumvirate review, deprecation of legacy registries/cards, cross-reference updates, and post-merge validation. Those actions are now historical migration provenance rather than pending tasks.

### Phase 4 — Deprecation

The original plan called for legacy registry/card deprecation and replacement by the unified representations. Current-state authority is now governed by the canonical unified registry and current reconciliation controls.

## Current control rule

Do not create another NDR registry or another competing merge plan. Current NDR registry changes should be made through the canonical unified registry and its release/reconciliation process. Cross-family relationships belong in the Pattern Commons architecture rather than in a second NDR authority document.

The separate `registry/PATTERN_REGISTRY_v2.md` remains a DGAF orchestration-pattern namespace; it is not a duplicate NDR authority merely because it is also named a pattern registry.

## Historical risk notes

The original plan identified risks around P-number collisions, broken cross-references, stasis mutation, and conflicting interaction maps. Those concerns remain useful as historical provenance, but current duplicate/semantic-equivalence decisions should follow the Pattern Commons equivalence rules and canonical NDR release controls.

No scientific, experimental, freeze, authorization, or empirical status is implied by this registry migration documentation.

---

*Historical migration plan retained for provenance. Do not use this document as a current task queue or authority source.*
