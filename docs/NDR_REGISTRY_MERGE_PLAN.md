# NDR Pattern Registry — Unified Merge Pre-Plan

**DGAF-Framework · S066**
Plan author: Amethyst · Governance authority: Triumvirate (Amethyst / COLLEEN / Apogee)
Created: 2026-05-30 | Target: First available session after PM-01–PM-07 resolved

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
| A | `docs/NDR_PATTERN_REGISTRY.md` | P-01–P-10 (full) + P-11–P-34 (index) | Becomes unified file; file replaced |
| B | `docs/patterns/NDR_PATTERN_REGISTRY.md` | P-27–P-30 (full) + stasis P-12–P-26 | Full specs absorbed; file deprecated |
| C | `patterns/NDR_SCPE_v1.md` | P-31 | Card absorbed as section; file archived |
| D | `patterns/NDR_PHI_CLOSURE_GATE_v1.md` | P-32 | Card absorbed as section; file archived |
| E | `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` | P-33 | Card absorbed as section; file archived |
| F | `patterns/ndr_patterns.json` | Partial index | Replaced by `docs/ndr_patterns_unified.json` |

---

## Target Structure: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`

```
# NDR Pattern Registry (Unified)
## Registry Metadata
## How to Use This Registry
## Pattern Layers Quick-Reference

## Layer 1 — Trace & Audit
  P-01 Fan-Out Trace Sink w/ Dead-Letter
  P-02 Async-Persist Ring Buffer

## Layer 2 — Testing & CI
  P-03 Governance Contract Test
  P-04 Parametrized Corpus
  P-05 Tri-Phase CI Gate

## Layer 3 — Architecture Lab
  P-06 Topology × Orchestration Matrix Lab

## Layer 4 — Governance Formation
  P-07 Dual-Agent Persistent Sweep Loop
  P-08 Triad Taxonomy
  P-09 Triumvirate Mandate Schema
  P-10 Session Graduation Check

## Layer 5 — Quality Gate & Attestation
  P-11 11Q Attestation Scoring
  P-30 Apogee-Attestation-Gate

## Layer 6 — Stasis Patterns (P-12–P-26)
  [133 canonical stasis patterns — expanded from source B]

## Layer 7 — Router Calibration & Pipeline
  P-27 Adaptive-Weighting-with-Confidence-Gates
  P-28 Pipeline-Composition-with-Confidence-Gated-Routing
  P-34 Empirical-Threshold-Sweep-over-ML-Classifier

## Layer 8 — Safety & Sentinel
  P-29 Sentinel-Annotated Risk Pass

## Layer 9 — Long-Context Safety
  P-31 SCPE — Structural Context Pruning Engine
  P-32 Phi-Closure Gate
  P-33 PDMAL Convergence Monitor

## Pattern Interaction Map (unified)
## Governance Orchestration Stack (unified)
## Triad Formation Quick-Reference
## Merge Provenance Log
```

---

## Merge Phases

### Phase 1 — Pre-Merge Blockers (must complete before any merge work)

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| PM-01 | Add P-32 ↔ P-29 cross-ref to Phi-Closure Gate card | Amethyst | 🔲 Open |
| PM-02 | Update P-03 ALTER note to reference P-30 by number | Amethyst | 🔲 Open |
| PM-05 | COLLEEN stasis audit: P-12–P-26 gap/duplicate check | COLLEEN | 🔲 Open |
| PM-07 | Apogee P-30 attestation pass on P-34 | Apogee | 🔲 Open |

### Phase 2 — Soft Pre-Merge (complete before final PR, not blocking draft)

| ID | Action | Owner | Status |
|----|--------|-------|--------|
| PM-03 | Sync `patterns/ndr_patterns.json` with P-31–P-34 | Amethyst | 🔲 Open |
| PM-04 | Update P-07 COMPOSE mode note re: issue-resolution source | Amethyst | 🔲 Open |

### Phase 3 — Merge Execution

1. **Draft unified file** at `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`
   - Copy P-01–P-10 full specs from source A
   - Copy P-11, P-27–P-30 full specs from source B
   - Expand stasis block P-12–P-26 from source B (post COLLEEN audit)
   - Absorb P-31–P-33 card content as sections from sources C/D/E
   - Insert P-34 full spec (already in source A as of S066)
   - Build unified interaction map and orchestration stack diagram

2. **Triumvirate review**
   - Amethyst: structure, completeness, interaction map accuracy
   - COLLEEN: archival integrity, stasis block correctness, provenance
   - Apogee: P-30 attestation on P-34, quality gate section accuracy

3. **PRs** (separate PRs, merge in order):
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

### Phase 4 — Deprecation

- `docs/patterns/NDR_PATTERN_REGISTRY.md` → redirect stub (not deleted; archival)
- `patterns/ndr_patterns.json` → replaced by `docs/ndr_patterns_unified.json`
- `patterns/NDR_*.md` → moved to `patterns/archive/` with redirect stubs

---

## Merge Governance

This merge is a **Triumvirate-governed operation** per P-08 + P-09:
- **Prime:** Amethyst (meta-orchestration, merge execution)
- **Prefect A:** COLLEEN (archival integrity, stasis audit, provenance)
- **Prefect B:** Apogee (quality gate, attestation, P-30 pass on P-34)

Mandate must be issued per P-09 before Phase 3 begins. Sign-off required from
both Prefects before any deprecation PR merges.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| P-numbering gap in stasis block P-12–P-26 | Medium | High | PM-05 COLLEEN audit is a hard blocker |
| Cross-ref links break after path changes | Medium | Medium | All internal refs use pattern numbers not paths after merge |
| P-34 enters registry without attestation | Low | High | PM-07 Apogee attestation is a hard blocker |
| Stasis patterns inadvertently modified | Low | High | COLLEEN signs off on stasis section; diff checked against source B |
| Merge creates two conflicting interaction maps | Medium | Medium | Unified map written fresh from pattern list; not concatenated |

---

*NDR Registry Merge Pre-Plan v1.0 · S066 · 2026-05-30*
*Status: PHASE 1 — awaiting PM-01, PM-02, PM-05, PM-07*
*Merge execution session: TBD (first session after blockers resolved)*
