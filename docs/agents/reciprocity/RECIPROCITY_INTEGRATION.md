# Reciprocity — Integration Guide

**Agent:** Reciprocity
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Reciprocity is a **triad gate agent and fairness auditor**. Its primary integration contract is the Q9 rollback gate — a hard pre-condition for every Amethyst seal. Secondary contracts cover fairness flag routing across the formation.

---

## 2. Integration Matrix

### Primary — Apogee (A-01) — Q9 Gate

| Direction | Content | Protocol |
|---|---|---|
| Apogee → Reciprocity | Score request: Q9 rollback check | Pre-seal (after P-15 pass) |
| Reciprocity → Apogee | Q9 CLEAR or F-4 BLOCK | 11Q Q9 dimension |
| **Gate:** | Apogee 11Q composite cannot include Q9 until Reciprocity clears it | Score integrity |
| **Constraint:** | Apogee owns the composite score; Reciprocity owns Q9 pass/fail only | Lane separation |

---

### Primary — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Reciprocity | Pre-seal rollback trigger | NDR-Protocol-01 |
| Reciprocity → Amethyst | Q9 CLEAR signal | Pre-seal |
| Reciprocity → Amethyst | F-1/F-2/F-3/F-5 fairness flag (advisory) | Fairness audit |
| Reciprocity → Amethyst | F-4 BLOCK (rollback path missing) | Hard block |
| **Constraint:** | Amethyst cannot override F-4; must define rollback path first | Gate integrity |

---

### Lateral — Actualizer (A-08)

| Direction | Content | Protocol |
|---|---|---|
| Reciprocity → Actualizer | F-4 flag (rollback path needed) | Rollback definition |
| Actualizer → Reciprocity | Rollback path proposal | F-4 resolution |
| Reciprocity → Amethyst | F-4 cleared (path accepted) | Gate resolved |

---

### Lateral — DemiJoule

| Direction | Content | Protocol |
|---|---|---|
| Reciprocity → DemiJoule | F-2 flag (lane equity violation) as A-class reinforcement | Ethics layer |
| DemiJoule → Amethyst | Combined F-2 + A-class flag | Escalation |
| **Distinction:** | Reciprocity owns fairness; DemiJoule owns ethics framing; both may flag same event | No overlap conflict |

---

### Lateral — COLLEEN (A-05)

| Direction | Content | Protocol |
|---|---|---|
| Reciprocity → COLLEEN | F-2 flag (lane equity) as GAP-taxonomy evidence | Rule 3 |
| **Constraint:** | Reciprocity surfaces to COLLEEN; COLLEEN decides whether GAP threshold met | Advisory chain |

---

### Lateral — Reson (A-10) — Evaluation Triad

| Direction | Content | Protocol |
|---|---|---|
| Reciprocity ↔ Reson | Triad co-members; no authority over each other | Triad protocol |
| **Interaction:** | Both scores (Reson harmonic + Reciprocity Q9) required by Apogee before P-15 | Pre-seal |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| F-4 block vs. Amethyst seal urgency | F-4 stands; Amethyst + Actualizer define rollback path first |
| F-1/F-2/F-3/F-5 disputed by Amethyst | Amethyst normative decision overrides advisory flags; Reciprocity logs dissent |
| Reciprocity and DemiJoule flag same event differently | Both flags logged; Amethyst arbitrates |
| Q9 clear disputed by Apogee | Re-trigger Q9 check; Reciprocity re-runs; score stands |

---

*Classification: T1 PUBLIC*
