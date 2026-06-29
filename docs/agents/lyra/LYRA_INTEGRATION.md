# Lyra — Integration Guide

**Agent:** Lyra
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Lyra is a **precision input agent** in the harmonic cluster. Its sole output — the tonal coherence score — flows to Reson for harmonic aggregation. Its secondary output — the direct Apogee flag for scores <0.50 — provides a short-circuit path for severe tonal incoherence.

---

## 2. Integration Matrix

### Primary — Reson (A-10)

| Direction | Content | Protocol |
|---|---|---|
| Reson → Lyra | Score request | Pre-harmonic scoring |
| Lyra → Reson | Tonal coherence score (0.00–1.00) + classification | Harmonic aggregation |
| **Constraint:** | Lyra produces the score; Reson aggregates; Lyra has no gate | Lane separation |

---

### Secondary — Apogee (A-01)

| Direction | Content | Protocol |
|---|---|---|
| Lyra → Apogee | Direct tonal incoherence flag (score <0.50 only) | Pillar C risk |
| **Constraint:** | Direct flag is advisory; Apogee incorporates into Pillar C assessment | Advisory |

---

### Lateral — Echolette

| Direction | Content | Protocol |
|---|---|---|
| Lyra ↔ Echolette | Co-cluster members; no authority over each other | Cluster protocol |
| **Interaction:** | Both scores aggregated by Reson independently; no direct Lyra-Echolette dependency | Parallel inputs |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Reson disputes Lyra’s score | Lyra re-runs scoring; revised score sent to Reson |
| Lyra score <0.50 but Apogee does not flag Pillar C | Lyra’s direct flag logged; Apogee’s assessment stands |
| Lyra and Echolette produce conflicting cluster signals | Reson arbitrates aggregation; both scores preserved |

---

*Classification: T1 PUBLIC*
