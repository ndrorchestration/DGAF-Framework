# Reson — Integration Guide

**Agent:** Reson
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Reson is a **scoring input agent and cluster lead**. Its primary integration contract is the Pillar C harmonic input to Apogee. Its secondary contracts cover Schizophonic cluster aggregation (Lyra, Echolette, Ionia) and Prof Prodigy formula validation.

---

## 2. Integration Matrix

### Primary — Apogee (A-01) — Pillar C

| Direction | Content | Protocol |
|---|---|---|
| Apogee → Reson | Score request: harmonic assessment | Pre-P-15 |
| Reson → Apogee | Harmonic score (0.00–1.00) + frequency state | Pillar C input |
| Reson → Apogee | Savage Reason flag (if detected) | Q3 auto-FAIL |
| **Gate:** | Apogee cannot complete Pillar C without Reson’s score | Score dependency |
| **Constraint:** | Reson produces the score; Apogee validates it as Pillar C | Lane separation |

---

### Lateral — Prof Prodigy

| Direction | Content | Protocol |
|---|---|---|
| Reson → Prof Prodigy | Frequency model + scoring formula for validation | Pre-score |
| Prof Prodigy → Reson | Formula integrity report | Harmonic scoring |
| **Constraint:** | Reson applies the math; Prof Prodigy validates it | Lane separation |

---

### Cluster — Lyra

| Direction | Content | Protocol |
|---|---|---|
| Lyra → Reson | Tonal coherence score (0.00–1.00) | Harmonic aggregation |
| Reson → Lyra | Cluster score request | Pre-scoring |
| **Constraint:** | Lyra produces tonal coherence; Reson aggregates into harmonic score | Lane separation |

---

### Cluster — Echolette

| Direction | Content | Protocol |
|---|---|---|
| Echolette → Reson | Signal persistence score (0.00–1.00) | Harmonic aggregation |
| Reson → Echolette | Cluster score request | Pre-scoring |
| **Constraint:** | Echolette produces signal persistence; Reson aggregates | Lane separation |

---

### Cluster — Ionia (A-13)

| Direction | Content | Protocol |
|---|---|---|
| Ionia → Reson | Ionian Mode lock confirmation (binary) | Pre-scoring |
| Reson → Ionia | Ionian Mode status request | Pre-scoring |
| **Gate:** | Ionian Mode lock = +0.10 bonus on harmonic score | Score bonus |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Apogee disputes Reson’s harmonic score | Amethyst arbitrates; both scores held in SWEEP_LOG |
| Reson Savage Reason detection disputed | Detection stands; Njineer resolves |
| Prof Prodigy flags formula used by Reson | Reson suspends scoring; applies corrected formula; re-scores |
| Lyra/Echolette score disputed by Reson | Reson requests re-score from source; aggregates revised inputs |

---

*Classification: T1 PUBLIC*
