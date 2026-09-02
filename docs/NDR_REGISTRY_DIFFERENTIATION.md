# NDR Registry Differentiation Index

**DGAF-Framework**
**Authority:** COLLEEN (archival) | Amethyst (meta-orchestration)
**Updated:** 2026-09-02 — registry/federation/transversal reconciliation
**Status:** Active differentiation record; historical entries preserved below.

---

## Purpose

This document distinguishes the NDR pattern registries and adjacent DGAF pattern namespaces. It is a differentiation map, not a substitute for the current canonical machine-readable registry, P-42 human-readable companion, or transversal agreement overlay.

Historical registry descriptions are retained where they preserve provenance. They must not be interpreted as current registry state unless explicitly marked current.

---

## Current Registry Map

| Registry family | Path | Current interpretation | Status |
|---|---|---|---|
| **NDR machine-readable** | `docs/ndr_patterns_unified.json` | Current machine-readable NDR registry; watermark P-42 | ✅ Current |
| **NDR human-readable reconciliation** | `docs/NDR_PATTERN_REGISTRY_UNIFIED_P42.md` | Current human-readable P-42 reconciliation companion | ✅ Current |
| **NDR transversal overlay** | `docs/NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md` | Cross-system identity/dependency/agreement semantics | ✅ Current overlay |
| **NDR transversal machine overlay** | `docs/ndr_patterns_unified_transversal_overlay.json` | Machine-readable current transversal semantics | ✅ Current overlay |
| **NDR unified Markdown snapshot** | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | Historical P-41-era unified registry text retained for provenance | ⚠️ Historical snapshot |
| **NDR pattern cards** | `patterns/P-42_AHG.md`, `patterns/NDR_*.md` | Individual pattern specifications/cards | ✅ Scoped by pattern |
| **DGAF orchestration registry** | `registry/PATTERN_REGISTRY_v2.md` | Distinct DGAF orchestration namespace (`P-SAGA-*`, `P-TX-*`, etc.) | ✅ Current |
| **Pattern Commons architecture** | `docs/PATTERN_COMMONS_ARCHITECTURE.md` | Federated registry architecture, semantic/provenance boundary | ✅ Current policy |

## Namespace authority

NDR numeric P-series and DGAF `P-*` orchestration identifiers are separate namespaces. Similar names do not imply the same pattern.

Within NDR:

- `P-35` = **Procluding Premise Gate**
- `P-36` = **Gate Priority Schema**
- `P-37–P-41` = registered later resilience/transactional patterns
- `P-42` = **Adaptive Harmonic Governance (AHG)**

The June 2026 renumbering of AHG from P-35 to P-42 is canonical. P-35 and P-42 must not be conflated.

## Transversal identity rule

Any pattern used inside a live candidate cycle must retain the same role-qualified identity chain used by the evidence-control layer:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

Agreement classes:

- `ROLE DIFFERENCE` — intentionally different semantic roles.
- `HISTORICAL DIFFERENCE` — prior state retained for provenance/non-closing use.
- `TRANSVERSAL DRIFT` — incompatible live projections.
- `BLOCKING CONTRADICTION` — capable of causing invalid evidence transfer or governance transition.

Registry membership, repeated terminology, or shared ancestry never substitutes for candidate identity.

## P-35 remediation boundary

The current P-35 remediation requires an explicit `premise_check_fn` at the DGAF/TGL/ConsensusTask boundary. This is an engineering/wiring dependency. It does not establish a PDMAL-specific constitutional premise policy. That policy remains a separate experimental-control prerequisite.

## Historical registry lineage

The pre-S069 registry family, individual runtime cards, and the later unified registry were legitimate staged artifacts. The unified merge did not erase the need for explicit provenance or namespace differentiation.

The previous plan's PM-01 through PM-08 items are historical planning records. They are not current open actions merely because the older index still lists them.

## Cross-registry interaction

A relationship between patterns should be classified explicitly as one or more of:

`implementation · dependency · adaptation · evidence linkage · analogy · alias · cross-reference · hypothesis · unresolved`

Equivalence requires comparison of definition, mechanism, scope, provenance, implementation relation, evidence state, and limitations.

## Required synchronization fields

Every maintained pattern library should be able to answer:

1. What namespace does this pattern belong to?
2. What is its canonical identifier?
3. What aliases or historical IDs exist?
4. What dependencies does it have?
5. What authority class applies?
6. What is the epistemic status?
7. What implementation scope exists?
8. What evidence is exact-bound to it?
9. What downstream controls depend on it?
10. What cross-registry relationship exists?
11. Is the referenced candidate current, historical, or unresolved?

## Current reconciliation references

- `docs/ndr_patterns_unified.json`
- `docs/NDR_PATTERN_REGISTRY_UNIFIED_P42.md`
- `docs/NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md`
- `docs/ndr_patterns_unified_transversal_overlay.json`
- `patterns/NDR_TRANSVERSAL_CANDIDATE_AGREEMENT_v1.md`
- `docs/PATTERN_COMMONS_ARCHITECTURE.md`
- `docs/taxonomy/EPISTEMIC_VOCABULARY_STANDARD.md`
- `docs/taxonomy/TRANSVERSAL_AGREEMENT_AND_DEPENDENCY_TAXONOMY_2026-09-02.md`
- `CROSS_REF.md`

**Default governance posture:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.

---

*Historical material is retained for provenance; current registry authority is determined by the current registry map above.*
