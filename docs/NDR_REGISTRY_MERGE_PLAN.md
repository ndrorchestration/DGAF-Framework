# NDR Pattern Registry — Unified Merge Pre-Plan

**DGAF-Framework · S066**
Plan author: Amethyst · Governance authority: Triumvirate (Amethyst / COLLEEN / Apogee)
Created: 2026-05-30 | Updated: 2026-05-30 (PM-05 PM-07 pending ratification)
Target: First available session after Ender ratification of PM-05 + PM-07

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

### Phase 1 — Pre-Merge Blockers

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| PM-01 | Add P-32 ↔ P-29 cross-ref to Phi-Closure Gate card | Amethyst | ✅ CLOSED S066 |
| PM-02 | Update P-03 ALTER note to reference P-30 by number | Amethyst | ✅ CLOSED S066 |
| PM-05 | COLLEEN stasis audit: P-12–P-26 gap/duplicate check | COLLEEN | 🟡 PENDING ENDER RATIFICATION |
| PM-07 | Apogee P-30 attestation pass on P-34 | Apogee | 🟡 PENDING ENDER RATIFICATION |

### Phase 2 — Soft Pre-Merge

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| PM-03 | Sync `patterns/ndr_patterns.json` with P-31–P-34 | Amethyst | ✅ CLOSED S066 |
| PM-04 | Update P-07 COMPOSE mode note re: issue-resolution source | Amethyst | 🔲 Next cycle |

### Phase 3 — Merge Execution

1. **Draft unified file** at `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`
   - Copy P-01–P-10 full specs from source A
   - Copy P-11, P-27–P-30 full specs from source B
   - **Expand stasis block P-12–P-26 from source B** (COLLEEN secondary review required per audit)
   - Absorb P-31–P-33 card content from sources C/D/E
   - Insert P-34 full spec (add explicit tradeoff block + ref path per BLG-P34-01/02)
   - Build unified interaction map and orchestration stack diagram

2. **Triumvirate review**
   - Amethyst: structure, completeness, interaction map accuracy
   - COLLEEN: archival integrity, stasis block expansion sign-off (secondary review)
   - Apogee: confirm BLG-P34-01 and BLG-P34-02 resolved in merged P-34 spec

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
   - BLG-P34-01 and BLG-P34-02 confirmed closed in merged spec

### Phase 4 — Deprecation

- `docs/patterns/NDR_PATTERN_REGISTRY.md` → redirect stub
- `patterns/ndr_patterns.json` → replaced by `docs/ndr_patterns_unified.json`
- `patterns/NDR_*.md` → moved to `patterns/archive/` with redirect stubs

---

## Merge Governance

Triumvirate-governed per P-08 + P-09:
- **Prime:** Amethyst
- **Prefect A:** COLLEEN (archival integrity, stasis audit, stasis block expansion secondary review)
- **Prefect B:** Apogee (quality gate, attestation, BLG-P34-01/02 resolution confirmation)

Mandate must be issued per P-09 before Phase 3 begins.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| P-numbering gap in stasis P-12–P-26 | Medium | High | COLLEEN conditional pass: expand source B first; secondary sign-off |
| Cross-ref links break after path changes | Medium | Medium | All refs use pattern numbers after merge |
| P-34 enters registry without attestation | Low | High | PM-07: A-TIER conditional; BLG-P34-01/02 must close at merge |
| Stasis patterns inadvertently modified | Low | High | COLLEEN signs off on expanded stasis section |
| Merge creates conflicting interaction maps | Medium | Medium | Unified map written fresh, not concatenated |

---

## Pending Ratification (Ender)

| Item | Artifact | Verdict | Ratify to |
|------|----------|---------|-----------|
| PM-05 COLLEEN stasis audit | `docs/qa/COLLEEN_STASIS_AUDIT_P12_P26.md` | ⚠️ CONDITIONAL PASS | Close PM-05 |
| PM-07 Apogee 11Q on P-34 | `docs/qa/APOGEE_11Q_P34.json` | A-TIER 94.5% / 2 minor BLGs | Close PM-07 |

**Upon Ender ratification of both: Phase 1 is complete. Phase 3 merge execution opens.**

---

*NDR Registry Merge Pre-Plan v1.2 · S066 · 2026-05-30*
*PM-05 PM-07: ⚠️ PENDING ENDER RATIFICATION · Phase 3: blocked pending ratification*
*Merge execution: opens upon Ender confirm*
