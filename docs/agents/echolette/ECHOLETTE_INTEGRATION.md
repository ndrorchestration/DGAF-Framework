# Echolette — Integration Guide

**Agent:** Echolette
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Echolette is a **precision input agent** in the harmonic cluster, mirroring Lyra’s structure but focused on signal persistence rather than tonal coherence. Its score flows to Reson for harmonic aggregation, with a short-circuit direct flag to Apogee for severe signal loss.

---

## 2. Integration Matrix

### Primary — Reson (A-10)

| Direction | Content | Protocol |
|---|---|---|
| Reson → Echolette | Score request | Pre-harmonic scoring |
| Echolette → Reson | Signal persistence score (0.00–1.00) + classification | Harmonic aggregation |
| **Constraint:** | Echolette produces the score; Reson aggregates; Echolette has no gate | Lane separation |

---

### Secondary — Apogee (A-01)

| Direction | Content | Protocol |
|---|---|---|
| Echolette → Apogee | Direct signal loss flag (score <0.50 only) | Pillar C risk |
| **Constraint:** | Direct flag is advisory; Apogee incorporates into Pillar C assessment | Advisory |

---

### Lateral — Lyra

| Direction | Content | Protocol |
|---|---|---|
| Echolette ↔ Lyra | Co-cluster members; no authority over each other | Cluster protocol |
| **Interaction:** | Both scores aggregated by Reson independently; no direct Echolette-Lyra dependency | Parallel inputs |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Reson disputes Echolette’s score | Echolette re-runs scoring; revised score sent to Reson |
| Echolette score <0.50 but Apogee does not flag Pillar C | Echolette’s direct flag logged; Apogee’s assessment stands |
| Echolette and Lyra produce conflicting cluster signals | Reson arbitrates aggregation; both scores preserved |

---

*Classification: T1 PUBLIC*
