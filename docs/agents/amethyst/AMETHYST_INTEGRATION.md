# Amethyst — Integration Guide

**Agent ID:** A-00  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

This document defines Amethyst’s integration contracts with every agent in the 20-agent taxonomy. For each peer, it specifies: what Amethyst sends, what it receives, handoff conditions, and conflict resolution.

---

## 2. Integration Matrix

### Tier 1 — Strategic Quintet Peers

#### Amethyst ↔ Apogee (A-01)
| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Apogee | Score request (artifact ref + context) | P-11 |
| Apogee → Amethyst | 11Q composite score (0.00–1.00) | P-11 |
| **Gate:** | Amethyst gates on ≥0.90; blocks commit if below | P-15 |
| **Conflict:** | Amethyst cannot override Apogee score — must re-trigger scoring cycle | — |

#### Amethyst ↔ Perigee (A-02)
| Direction | Content | Protocol |
|---|---|---|
| Perigee → Amethyst | Post-hoc block notification (auto-executed) | NDR-133 peer |
| Amethyst → Perigee | Escalation routing when block is disputed | Compliance Dyad |
| **Gate:** | Perigee blocks auto-execute — Amethyst receives result, does not pre-approve | — |

#### Amethyst ↔ Nova (A-03)
| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Nova | TUE clearance signal (when COLLEEN L5 achieved) | TUE gate |
| Nova → Amethyst | 90-Day Executor Roadmap proposals (post-TUE) | Strategic Quintet |
| **Gate:** | Nova is advisory-only pre-TUE; proposals enter Amethyst normative pipeline post-TUE | — |
| **Constraint:** | Amethyst must not activate Nova before COLLEEN TUE — Rule 8 |

#### Amethyst ↔ Professor Prodigy (A-04)
| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Prof Prodigy | Proof request (formal verification task) | P-10 |
| Prof Prodigy → Amethyst | Micro-Playbook (T1/T2 abstraction of T3 proof) | P-12 |
| **Gate:** | Amethyst gates Micro-Playbook inclusion into canonical docs; Prodigy does not self-commit | — |

---

### Tier 2 — Operational Swarm

#### Amethyst ↔ COLLEEN (A-05)
| Direction | Content | Protocol |
|---|---|---|
| Amethyst → COLLEEN | Session open instruction; BLG surface request | P-02 |
| COLLEEN → Amethyst | BLG queue; registry delta; gap surface | P-02, P-08 |
| **Gate:** | Amethyst makes normative decisions on COLLEEN’s gap surfaces — Rule 3 (COLLEEN does not decide) | — |
| **TUE:** | COLLEEN signals L5 Executor status to Amethyst → Amethyst unlocks Nova | TUE gate |

#### Amethyst ↔ The Auditor (A-07)
| Direction | Content | Protocol |
|---|---|---|
| Auditor → Amethyst | Constraint verify pass/fail | NDR-Protocol-01 step 1 |
| Amethyst → Auditor | Override (if Auditor fail is disputed) | Amethyst normative decision |
| **Gate:** | Amethyst cannot bypass Auditor without explicit override + SWEEP_LOG entry | — |

#### Amethyst ↔ The Actualizer (A-08)
| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Actualizer | Indirect — via NDR-Protocol-01 chain (Auditor must pass first) | NDR-Protocol-01 |
| Actualizer → Amethyst | Artifact delivery (for Apogee scoring + Amethyst seal) | NDR-Protocol-01 step 5 |

#### Amethyst ↔ Zenith (A-09)
| Direction | Content | Protocol |
|---|---|---|
| Zenith → Amethyst | System High alert (load imbalance, symmetry broken) | Escalation |
| Amethyst → Zenith | Session pause authorization (if europe-west1 node failure) | Amethyst normative |

---

### Tier 3 — Resonance Cluster

#### Amethyst ↔ Reson (A-10)
| Direction | Content | Protocol |
|---|---|---|
| Reson → Amethyst | Harmonic score (0.00–1.00) | P-15 pre-condition |
| Amethyst → Reson | Re-score request (if session drift detected) | P-21 state anchor |
| **Gate:** | Amethyst gates on ≥0.75 for seal commits; <0.50 is hard stop | P-15 |

#### Amethyst ↔ Ionia (A-13)
| Direction | Content | Protocol |
|---|---|---|
| Ionia → Amethyst | Modal lock confirmation (0Hz state achieved) | NDR-Protocol-01 convergence |
| **Gate:** | Amethyst requires Ionia lock confirmation before seal on harmonic-sensitive sessions | P-15 |

---

### Legacy Extended Formation

#### Amethyst ↔ Sentinel
| Direction | Content | Protocol |
|---|---|---|
| Sentinel → Amethyst | Sovereign veto notification | P-15 sovereign guard |
| **Conflict:** | Sentinel veto overrides Amethyst — Njineer resolves. Amethyst cannot lift Sentinel block. | Rule 2 |

#### Amethyst ↔ Reciprocity
| Direction | Content | Protocol |
|---|---|---|
| Reciprocity → Amethyst | Rollback path definition | P-15 checkpoint 9 |
| Amethyst → Reciprocity | Rollback execution confirmation | Amethyst normative |

#### Amethyst ↔ Herald
| Direction | Content | Protocol |
|---|---|---|
| Amethyst → Herald | State confirmation (current state is final before relay) | Herald Relay activation |
| **Constraint:** | Herald reads T1 only; Amethyst must strip T2/T3 before Herald relay | NDR-133 scan |

---

### T3 SOVEREIGN (A-14→A-19)

| Integration | Contract |
|---|---|
| Amethyst → T3 agents | Activation requires explicit Amethyst call + Njineer approval |
| T3 agents → Amethyst | Outputs route to Drive first; GitHub-safe abstractions only via PROPRIETARY.md stubs |
| **Constraint:** | No T3 agent may be invoked by name until Njineer surfaces names from Drive |

---

## 3. Conflict Resolution Matrix

| Conflict | Resolution |
|---|---|
| Two formations issue conflicting instructions | Higher seat-count formation takes precedence |
| Sentinel veto vs. Amethyst commit | Sentinel wins; Njineer resolves |
| Compliance Dyad veto vs. any formation | Dyad wins; overrides all |
| Perigee block vs. Amethyst routing | Perigee block stands; escalation is post-hoc |
| Tie (same seat count) | Amethyst casting vote |
| Unresolvable | Escalate to Njineer |

---

*Classification: T1 PUBLIC*
