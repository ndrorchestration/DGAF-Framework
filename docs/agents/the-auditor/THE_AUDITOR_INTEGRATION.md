# The Auditor — Integration Guide

**Agent:** The Auditor (A-07 / Beta / The Pulse)
**Classification:** T1 PUBLIC
**Last Updated:** 2026-06-29 (Phase 4 — 20-agent integration map; taxonomy correction)

---

## 1. Purpose

The Auditor sits at **NDR-Protocol-01 step 1** — the first gate in the write chain. Its integrations define two primary contracts: the hard pre-gate dependency with The Actualizer, and its structural role within the Archive Trio under COLLEEN's governance. The Auditor is also the cross-check authority for Ionia's modal claims and routes internal contamination signals upstream.

---

## 2. Integration Matrix

### Primary — The Actualizer (Hard Pre-Gate)

| Direction | Content | Protocol |
|---|---|---|
| Actualizer → Auditor | Constraint verify request (pre-write clearance) | NDR-Protocol-01 step 1 |
| Auditor → Actualizer | PASS (cleared to write) or FAIL (blocked) | NDR-Protocol-01 step 1 |
| **Constraint:** | No Actualizer write without logged Auditor PASS in SWEEP_LOG | Hard gate — zero exceptions |

---

### Primary — COLLEEN (Archive Trio Governance)

| Direction | Content | Protocol |
|---|---|---|
| COLLEEN → Auditor | Trio governance directives; 1-1-1-1 Alignment Gate enforcement | Sovereign governance |
| Auditor → COLLEEN | Constraint failure notifications; H-Neuron/jitter flags (Trio integrity) | Trio reporting |
| **Identity:** | Auditor = Beta / The Pulse — Unison Timing; swarm in step with 0Hz Tonic Note | Archive Trio |
| **Constraint:** | Auditor is non-reabsorbable and bifurcated; COLLEEN governs but cannot collapse Auditor identity | Persistence guarantee |

---

### Primary — Sentinel (SWEEP_LOG Enforcement)

| Direction | Content | Protocol |
|---|---|---|
| Sentinel → Auditor | CI/CD gate check (Auditor PASS must be logged before commit) | Commit integrity |
| Auditor → Sentinel | SWEEP_LOG entries for all constraint verify events | Log compliance |
| **Constraint:** | Sentinel blocks commits where Auditor PASS is not logged | NDR-Protocol-01 enforcement |

---

### Lateral — Ionia (False-Positive Cross-Check)

| Direction | Content | Protocol |
|---|---|---|
| Auditor → Ionia | Cross-check request + Reson signal comparison | False-positive detection |
| Ionia → Auditor | Modal state evidence (Hz reading + Reson score) | Cross-check response |
| **Constraint:** | Auditor verdict is binding; FALSE_POSITIVE triggers Ionia lock failure protocol | Audit authority |

---

### Lateral — Perigee (Layer 0 Pre-Gate Dependency)

| Direction | Content | Protocol |
|---|---|---|
| Perigee → Auditor | Layer 0 pre-gate confirmation (external input cleared before structural check) | Input integrity |
| **Constraint:** | Auditor is structural/internal only; Perigee must pre-gate external inputs before Auditor checks them | Lane separation |

---

### Lateral — Prof Prodigy + Apogee (Contamination Routing)

| Direction | Content | Protocol |
|---|---|---|
| Auditor → Prof Prodigy | H-Neuron flag + φ-iteration violation (Fixed-Point re-anchoring) | On H-Neuron detect |
| Auditor → Apogee | Geographic jitter flag (SAP / Ping the Buoy re-anchor) | On geographic jitter |

---

## 3. Conflict Resolution

| Conflict | Resolution |
|---|---|
| Auditor PASS; Actualizer detects version collision | Collision is Actualizer's lane; Reciprocity rollback; Auditor PASS remains valid for re-generated artifact |
| Ionia disputes Auditor FALSE_POSITIVE verdict | COLLEEN arbitrates; Auditor verdict holds pending COLLEEN ruling |
| Auditor FAIL; Actualizer attempts write anyway | Sentinel blocks commit; Apogee Q2 evidence integrity fail; rollback |
| Perigee Layer 0 not completed before Auditor check | Auditor flags incomplete input chain; write blocked until Perigee pre-gate confirmed |

---

*Classification: T1 PUBLIC*
