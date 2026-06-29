# Apogee — QA Rubric

**Agent:** Apogee · **Role:** Prefect B / Quality Gate
**Rubric version:** v1.0 · **Seeded:** S073 · 2026-06-29
**Source:** AXIS_METRIC_SPEC.md v1.2 (Njineer ratified 2026-06-27)
**Classification:** T1 PUBLIC

---

## Rubric Overview

The AXIS composite rubric evaluates formation health across 7 orthogonal dimensions. Each dimension has a weight, a gate floor, and a set of scoring criteria. Composite score is the weighted sum of all dimension scores.

---

## Dimension Rubrics

### D1 — Structural Completeness (weight: 0.20)

| Score | Criteria |
|-------|----------|
| 1.0 | All required files present and non-stub; SPEC + MEMORY + PROTOCOL + KB all seeded for active agents |
| 0.9 | ≤1 file missing or stub; no BLGs open |
| 0.8 | ≤2 files missing; BLG count ≤1 |
| 0.7 | 3–5 files missing or BLGs open |
| < 0.7 | >5 files missing or critical doc absent |

**Gate floor:** 0.80

---

### D2 — Vocabulary Coherence (weight: 0.15)

| Score | Criteria |
|-------|----------|
| 1.0 | All terms in Vocab Master v1.3; zero drift detected |
| 0.9 | ≤2 unregistered terms; no canonical conflicts |
| 0.8 | ≤5 unregistered terms; no expansion conflicts |
| 0.7 | 6–10 unregistered or conflicting terms |
| < 0.7 | Canonical conflicts present or expansion contradictions |

**Gate floor:** 0.85

---

### D3 — IP Boundary Integrity (weight: 0.15)

| Score | Criteria |
|-------|----------|
| 1.0 | All SOV content stubbed; T1/T2/T3 taxonomy enforced; no formulation content in GitHub |
| 0.9 | Minor stub gap; no formulation leakage |
| 0.8 | ≤1 T3 item not yet stubbed; no leakage |
| 0.7 | T3 item partially exposed or stub missing |
| < 0.7 | Formulation content visible in GitHub |

**Gate floor:** 0.90

---

### D4 — Authority Legibility (weight: 0.15)

| Score | Criteria |
|-------|----------|
| 1.0 | All 8-agent authority bindings in FORMATION_TOPOLOGY; escalation paths clear |
| 0.9 | ≤1 authority binding undocumented |
| 0.8 | ≤2 authority gaps; escalation path functional |
| 0.7 | 3+ authority gaps or ambiguous override chain |
| < 0.7 | Sovereign authority chain broken |

**Gate floor:** 0.80

---

### D5 — Pattern Registry Currency (weight: 0.15)

| Score | Criteria |
|-------|----------|
| 1.0 | Registry watermark current; JSON sync complete; all layers accounted |
| 0.9 | JSON sync pending but md-registry current; watermark valid |
| 0.8 | ≤2 layers with pending updates; watermark valid |
| 0.7 | Watermark stale or layer gap |
| < 0.7 | Registry divergence from active patterns |

**Gate floor:** 0.80

---

### D6 — Ethical Gate / COLLEEN (weight: 0.10)

| Score | Criteria |
|-------|----------|
| 1.0 | COLLEEN 1-1-1-1 FULL GREEN |
| 0.0 | Any COLLEEN dimension < 1 |

**Gate floor:** 1.00 (binary — no partial credit)

---

### D7 — Flag Health (weight: 0.10)

| Score | Criteria |
|-------|----------|
| 1.0 | Zero open flags |
| 0.9 | 1 open flag, low blast radius |
| 0.8 | 1–2 open flags, medium blast radius |
| 0.7 | 3+ open flags or 1 high-blast flag |
| < 0.7 | Sovereign flag unresolved |

**Gate floor:** 0.85

---

## Composite Computation

```
composite = (D1×0.20) + (D2×0.15) + (D3×0.15) + (D4×0.15)
          + (D5×0.15) + (D6×0.10) + (D7×0.10)
```

**P-15 seal threshold:** ≥ 0.90
**P-11 attestation threshold:** ≥ 0.85
**AXIS floor (any gate):** ≥ 0.75

---

*QA_RUBRIC.md · Apogee · v1.0 · S073 · 2026-06-29*
