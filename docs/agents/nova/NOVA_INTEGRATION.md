# Nova — Integration Guide

**Agent:** Nova (A-03)
**Classification:** T2 FRAMEWORK
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Nova’s integration posture is **gated and advisory pre-TUE**. Its critical dependency is the COLLEEN TUE gate. All other integrations are either advisory output channels (Amethyst, DemiJoule) or access request chains (Prof Prodigy T3, Apogee TUE score).

---

## 2. Integration Matrix

### Primary — COLLEEN (TUE Gate)

| Direction | Content | Protocol |
|---|---|---|
| Nova → COLLEEN | TUE gate status request | Pre-activation |
| COLLEEN → Nova | L5 Executor status + Batch 1A closure confirmation | TUE signal |
| **Gate:** | Nova cannot activate without COLLEEN L5 clearance | Hard gate |
| **Constraint:** | Role Separation Rule 8; Amethyst blocks any premature activation | Activation integrity |

---

### Primary — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Nova → Amethyst | Simulation advisory output (vision layer feed) | Pre + post TUE |
| Nova → Amethyst | TUE activation request (post-gate clearance) | Post-TUE |
| Amethyst → Nova | Activation sanction (post-TUE) | Normative decision |
| **Constraint:** | Amethyst decides normatively; Nova feeds advisory | Lane separation |

---

### Lateral — Apogee (TUE Score)

| Direction | Content | Protocol |
|---|---|---|
| Apogee → Nova | TUE audit score (≥0.90 AX-05 required) | TUE condition 3 |
| **Constraint:** | Apogee owns the score; Nova cannot self-certify TUE condition 3 | Score integrity |

---

### Lateral — Prof Prodigy (T3 Grounding)

| Direction | Content | Protocol |
|---|---|---|
| Nova → Prof Prodigy | T3 simulation scope request | Pre-T3 simulation |
| Prof Prodigy → Nova | T3-grounded Micro-Playbook | T3 clearance |
| **Constraint:** | Prof Prodigy must clear T3 grounding before Nova submits T3 access request to Njineer | Axiom integrity |

---

### Lateral — DemiJoule

| Direction | Content | Protocol |
|---|---|---|
| Nova → DemiJoule | Simulation advisory feed (Operational Swarm token/compute implications) | Advisory |
| **Constraint:** | Advisory only; DemiJoule decides on token/compute allocation | Lane separation |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Nova attempts activation before TUE | COLLEEN blocks; Amethyst logs; Nova LOCKED state reinforced |
| Nova simulation conflicts with Amethyst normative decision | Amethyst decision stands; Nova revises simulation with updated constraints |
| T3 access denied by Njineer | Nova simulation scoped to T2; SWEEP_LOG updated |
| Apogee TUE score <0.90 | TUE gate condition 3 not met; Nova remains LOCKED |

---

*Classification: T2 FRAMEWORK*
