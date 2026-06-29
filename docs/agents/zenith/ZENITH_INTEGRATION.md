# Zenith — Integration Guide

**Agent:** Zenith (A-09)
**Classification:** T2 FRAMEWORK
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Zenith is the **infrastructure layer agent**. Its integrations run beneath the formation logic layer — it supplies compute health signals upward to DemiJoule and Amethyst and responds downward to GCP infrastructure events.

---

## 2. Integration Matrix

### Primary — DemiJoule

| Direction | Content | Protocol |
|---|---|---|
| Zenith → DemiJoule | Compute efficiency signal (per-session load report) | Continuous |
| Zenith → DemiJoule | Escalation (token/compute spike or silent debt) | On detection |
| DemiJoule → Zenith | Token spend data (for cross-check) | Cross-check |
| **Constraint:** | Zenith provides compute signal; DemiJoule governs token budget decisions | Lane separation |

---

### Primary — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Zenith → Amethyst | Session pause request (symmetry unrestorable) | On failure |
| Zenith → Amethyst | Node failure notification + failover status | Immediate |
| Amethyst → Zenith | Session pause decision / continue on degraded symmetry | Normative |
| **Constraint:** | Zenith requests; Amethyst decides session continuity | Lane separation |

---

### Lateral — Perigee

| Direction | Content | Protocol |
|---|---|---|
| Perigee → Zenith | Hard block events (blocked signal load reduction) | Awareness |
| **Constraint:** | Perigee’s Layer 0 blocks reduce signal throughput; Zenith adjusts load expectations | Infrastructure awareness |

---

### Lateral — Reson

| Direction | Content | Protocol |
|---|---|---|
| Zenith → Reson | Compute load state (high load can affect harmonic scoring environment) | Awareness |
| **Constraint:** | Informational only; Reson scores harmonic state independently | Advisory |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Zenith requests session pause; DemiJoule reports token budget healthy | Amethyst arbitrates; infrastructure and budget signals both considered |
| GCP failover fails; Njineer unavailable | Session pause mandatory; Herald broadcasts SESSION_PAUSE to formation |
| Zenith and DemiJoule report conflicting load data | Both reports logged; Amethyst arbitrates |
| Perigee hard block spike causes unexpected load shift | Zenith logs; rebalance attempted; DemiJoule notified |

---

*Classification: T2 FRAMEWORK*
