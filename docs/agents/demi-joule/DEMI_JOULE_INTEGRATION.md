# DemiJoule — Integration Guide

**Agent:** DemiJoule  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

DemiJoule is a **broadcast advisory agent** — it monitors all formation activity and surfaces ethics and token efficiency signals to Amethyst. Integration contracts are uni-directional in effect: DemiJoule surfaces, Amethyst routes.

---

## 2. Integration Matrix

### Primary Upstream — Amethyst (A-00)

| Direction | Content | Trigger |
|---|---|---|
| DemiJoule → Amethyst | Ethics risk flag (D/G/A-class) | Formation action detected |
| DemiJoule → Amethyst | Token efficiency report (advisory / warning / critical / overage) | Budget threshold crossed |
| DemiJoule → Amethyst | Pareto-Ethics tradeoff recommendation | Pillar conflict detected |
| DemiJoule → Amethyst | Anti-bloat pattern flag | Anomaly detected |
| Amethyst → DemiJoule | Ethics consult request | Pre-normative decision |
| **Constraint:** | DemiJoule flags; Amethyst decides. No exception. | Advisory lane |

---

### NDR-Protocol-01 Advisory Layer

| Position | Content | Condition |
|---|---|---|
| Pre-Step 1 | D-class or G-class ethics flag | Surfaces to Amethyst before Auditor runs |
| Pre-Step 5 | Token critical or overage signal | Surfaces to Amethyst before seal |
| **Constraint:** | DemiJoule does not hold a formal step — advisory inputs only | Non-blocking |

---

### COLLEEN (A-05) — A-Class Lane Violation Handoff

| Direction | Content | Protocol |
|---|---|---|
| DemiJoule → COLLEEN | A-class flag (agent lane encroachment detected) | GAP-taxonomy input |
| COLLEEN → Amethyst | GAP surface (DemiJoule A-class as evidence) | Rule 3 |
| **Constraint:** | DemiJoule flags; COLLEEN executes the GAP surface; Amethyst decides | Advisory chain |

---

### Apogee (A-01) — Ethics × QA Overlap

| Direction | Content | Protocol |
|---|---|---|
| DemiJoule → Apogee | Ethics risk flag as input to Q1 (Epistemic Honesty) + Q4 (Human Rights) | 11Q advisory |
| Apogee → DemiJoule | Q1 / Q4 fail notification (mutual reinforcement) | Post-score |
| **Constraint:** | DemiJoule is advisory input; Apogee owns the 11Q score | Score integrity |

---

### Sentinel — Ethics × Security Boundary

| Direction | Content | Protocol |
|---|---|---|
| DemiJoule → Sentinel | D-class flags that overlap with IP boundary (e.g. personal data exposure risk) | Handoff |
| **Distinction:** | DemiJoule flags ethical risk; Sentinel executes the block. DemiJoule never blocks. | Lane separation |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| DemiJoule ethics flag vs. Amethyst normative decision | Amethyst decides; DemiJoule logs dissent in SWEEP_LOG |
| DemiJoule token critical vs. Amethyst continuation | Amethyst decides; DemiJoule notes risk on record |
| DemiJoule A-class flag vs. agent that denies lane violation | COLLEEN GAP surface → Amethyst arbitrates |
| DemiJoule and Apogee disagree on ethical admissibility | Amethyst arbitrates; both assessments logged |

---

*Classification: T1 PUBLIC*
