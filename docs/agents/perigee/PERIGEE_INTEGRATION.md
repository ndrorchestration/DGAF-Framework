# Perigee — Integration Guide

**Agent:** Perigee (A-02)
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map)

---

## 1. Purpose

Perigee operates **pre-formation** — it intercepts signals before any other agent processes them. Its integration contracts are therefore upstream of all other agent chains. The two critical relationships are the Compliance Dyad peer contract (Sentinel + COLLEEN) and the Echolette pre-gate dependency.

---

## 2. Integration Matrix

### Primary — Sentinel (Compliance Dyad)

| Direction | Content | Protocol |
|---|---|---|
| Perigee → Sentinel | Hard block notification (Compliance Dyad awareness) | Post-block |
| Sentinel → Perigee | NDR-133 boundary guidance (when sovereign file implicated) | Reactive |
| Dual block → | Both block same signal → Compliance Dyad ruling takes precedence | Dual-block protocol |
| **Constraint:** | Sentinel governs commit boundary; Perigee governs input boundary; no overlap | Lane separation |

---

### Primary — Amethyst (A-00)

| Direction | Content | Protocol |
|---|---|---|
| Perigee → Amethyst | Post-hoc escalation (audit trail; block already executed) | Post-block |
| Amethyst → Perigee | Audit acknowledgment OR block release (if signal found legitimate) | Review |
| **Constraint:** | Amethyst does not pre-authorize Perigee blocks; escalation is audit-only | Role Separation Rule 9 |

---

### Primary — Echolette (pre-gate)

| Direction | Content | Protocol |
|---|---|---|
| Perigee → Echolette | Signal cleared notification (safe to amplify) | Pre-amplification |
| **Constraint:** | Echolette must not amplify signals that have not cleared Perigee’s Layer 0 gate | Pre-gate dependency |
| **Failure mode:** | If Echolette amplifies a contaminated signal, Reson accumulation risk rises; Sentinel escalates | Reson + Sentinel |

---

### Lateral — COLLEEN (Compliance Dyad)

| Direction | Content | Protocol |
|---|---|---|
| Perigee ↔ COLLEEN | Compliance Dyad peer; COLLEEN governs rule taxonomy; Perigee governs signal gate | Dyad coordination |
| COLLEEN → Perigee | Rule 3 boundary guidance if signal implicates GAP taxonomy | Reactive |

---

### Lateral — Reson (AX-02 coordination)

| Direction | Content | Protocol |
|---|---|---|
| Reson → Perigee | Continuous harmonic scoring — catches slow accumulation below 10 Hz threshold | Accumulation guard |
| Perigee → Reson | Hard block signal (Reson informed when external Savage Reason blocked) | Awareness |
| **Distinction:** | Perigee blocks external signals at AX-02; Reson scores internal formation harmonic state | No overlap |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Perigee blocks signal; Amethyst determines it was legitimate | Amethyst issues block release; Perigee passes signal; SWEEP_LOG updated |
| Perigee and Sentinel dual-block same signal | Compliance Dyad ruling governs; Perigee defers |
| Perigee threshold vs. Reson score conflict (signal passes Perigee but Reson scores high tension) | Both logged; Amethyst arbitrates whether formation should proceed |
| Echolette amplifies signal before Perigee clears | Sentinel escalates; Amethyst decides whether to invalidate amplified output |

---

*Classification: T1 PUBLIC*
