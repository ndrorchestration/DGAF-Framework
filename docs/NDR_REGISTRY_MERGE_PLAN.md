# NDR Pattern Registry — Unified Merge Pre-Plan

**DGAF-Framework · S066**
Plan author: Amethyst · Governance authority: Triumvirate (Amethyst / COLLEEN / Apogee)
Created: 2026-05-30 | Updated: 2026-05-30 (PHASE 1 COMPLETE — Ender ratification received · PM-04 CLOSED S067)
Target: Next available session — Phase 3 merge execution NOW OPEN

---

## Objective

Consolidate three active NDR pattern registries into a single unified file
(`docs/NDR_PATTERN_REGISTRY_UNIFIED.md`) covering P-01 through P-34+, with
a machine-readable JSON export (`docs/ndr_patterns_unified.json`).

The merge does **not** change any pattern specs. It changes only:
- File location (one file, not three)
- Navigation (unified TOC + anchor links)
- Cross-references (explicit pattern-number references, not layer-name references)

---

## Source Files

| # | Source | Patterns | Disposition |
|---|--------|----------|-------------|
| A | `docs/NDR_PATTERN_REGISTRY.md` | P-01–P-10 (full) + P-11–P-34 (index) | Becomes unified file base |
| B | `docs/patterns/NDR_PATTERN_REGISTRY.md` | P-27–P-30 (full) + stasis P-12–P-26 | Full specs absorbed; file deprecated |
| C | `patterns/NDR_SCPE_v1.md` | P-31 | Card absorbed as section; archived |
| D | `patterns/NDR_PHI_CLOSURE_GATE_v1.md` | P-32 | Card absorbed as section; archived |
| E | `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` | P-33 | Card absorbed as section; archived |
| F | `patterns/ndr_patterns.json` | v0.3.0 index | Replaced by `docs/ndr_patterns_unified.json` |

---

## Target Structure: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`

```
# NDR Pattern Registry (Unified)
## Registry Metadata
## How to Use This Registry
## Pattern Layers Quick-Reference

## Layer 1 — Trace & Audit          P-01, P-02
## Layer 2 — Testing & CI           P-03, P-04, P-05
## Layer 3 — Architecture Lab       P-06
## Layer 4 — Governance Formation   P-07, P-08, P-09, P-10
## Layer 5 — Quality Gate           P-11, P-30
## Layer 6 — Stasis                 P-12–P-26
## Layer 7 — Router Calibration     P-27, P-28, P-34
## Layer 8 — Safety & Sentinel      P-29
## Layer 9 — Long-Context Safety    P-31, P-32, P-33

## Pattern Interaction Map (unified)
## Governance Orchestration Stack (unified)
## Triad Formation Quick-Reference
## Merge Provenance Log
```

---

## Merge Phases

### Phase 1 — Pre-Merge Blockers ✅ COMPLETE

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| PM-01 | Add P-32 ↔ P-29 cross-ref to Phi-Closure Gate card | Amethyst | ✅ CLOSED S066 |
| PM-02 | Update P-03 ALTER note to reference P-30 by number | Amethyst | ✅ CLOSED S066 |
| PM-05 | COLLEEN stasis audit: P-12–P-26 gap/duplicate check | COLLEEN | ✅ CLOSED — CONDITIONAL PASS — Ender ratified 2026-05-30 |
| PM-07 | Apogee P-30 attestation pass on P-34 | Apogee | ✅ CLOSED — A-TIER 94.5% — Ender ratified 2026-05-30 |

### Phase 2 — Soft Pre-Merge ✅ COMPLETE

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| PM-03 | Sync `patterns/ndr_patterns.json` with P-31–P-34 | Amethyst | ✅ CLOSED S066 |
| PM-04 | Update P-07 COMPOSE mode note re: issue-resolution source | Amethyst | ✅ CLOSED S067 — registry v2.3, graduation script dual-format |

### Phase 3 — Merge Execution 🟢 OPEN

> **UNBLOCKED as of 2026-05-30 02:49 EDT. Ender ratification received.**
> Execute in next available session. COLLEEN secondary stasis review required
> before deprecation PRs merge. BLG-P34-01 and BLG-P34-02 must close in merged spec.

1. **Draft unified file** at `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`
   - Copy P-01–P-10 full specs from source A
   - Copy P-11, P-27–P-30 full specs from source B
   - **Expand stasis block P-12–P-26 from source B** — FIRST action; COLLEEN secondary review required
   - Absorb P-31–P-33 card content from sources C/D/E
   - Insert P-34 full spec — add explicit tradeoff block (BLG-P34-01) + ref path (BLG-P34-02)
   - Build unified interaction map and orchestration stack diagram

2. **Triumvirate review**
   - Amethyst: structure, completeness, interaction map accuracy
   - COLLEEN: stasis block expansion secondary sign-off
   - Apogee: confirm BLG-P34-01 and BLG-P34-02 resolved; update attestation to ATTESTED

3. **PRs** (separate, merge in order):
   - PR-A: Add `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` + `docs/ndr_patterns_unified.json`
   - PR-B: Add redirect notice to `docs/patterns/NDR_PATTERN_REGISTRY.md`
   - PR-C: Archive `patterns/NDR_*.md` → `patterns/archive/`
   - PR-D: Update `docs/NDR_PATTERN_REGISTRY.md` to redirect-only stub
   - PR-E: Update CROSS_REF to unified path; run P-10 graduation check

4. **Post-merge validation**
   - P-10 graduation check passes
   - CROSS_REF updated
   - All internal links resolve
   - `ndr_patterns_unified.json` parseable
   - BLG-P34-01 and BLG-P34-02 confirmed closed
   - COLLEEN stasis expansion secondary sign-off on record

### Phase 4 — Deprecation

- `docs/patterns/NDR_PATTERN_REGISTRY.md` → redirect stub
- `patterns/ndr_patterns.json` → replaced by `docs/ndr_patterns_unified.json`
- `patterns/NDR_*.md` → moved to `patterns/archive/` with redirect stubs

---

## Merge Governance

Triumvirate-governed per P-08 + P-09:
- **Prime:** Amethyst
- **Prefect A:** COLLEEN (stasis block expansion secondary review; archival integrity)
- **Prefect B:** Apogee (BLG-P34-01/02 resolution; final attestation ATTESTED promotion)

Mandate must be issued per P-09 before Phase 3 execution begins.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| P-numbering gap in stasis P-12–P-26 | Medium | High | COLLEEN secondary review on expanded source B — required before deprecation |
| Cross-ref links break after path changes | Medium | Medium | All refs use pattern numbers after merge |
| P-34 BLG-P34-01/02 not resolved at merge | Low | Medium | Apogee confirms resolution before ATTESTED promotion |
| Stasis patterns inadvertently modified | Low | High | COLLEEN signs off on expanded stasis section |
| Merge creates conflicting interaction maps | Medium | Medium | Unified map written fresh, not concatenated |

---

## Ratification Record

| Item | Artifact | Verdict | Ratified by | Date/Time |
|------|----------|---------|-----------|-----------|
| PM-05 COLLEEN stasis audit | `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md` | ⚠️ CONDITIONAL PASS | Ender | 2026-05-30 02:49 EDT |
| PM-07 Apogee 11Q P-34 | `docs/qa/APOGEE_11Q_P34.json` | A-TIER 94.5% / 2 minor BLGs | Ender | 2026-05-30 02:49 EDT |

---

*NDR Registry Merge Pre-Plan v1.4 · S067 · 2026-05-30*  
*PHASE 1 COMPLETE ✅ · PHASE 2 COMPLETE ✅ · PHASE 3 OPEN 🟢*  
*Merge execution: UNBLOCKED — next available session (S068)*
