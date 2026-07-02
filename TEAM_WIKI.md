# DGAF Framework — Team Wiki

> **Last updated:** 2026-07-02 · S072 · P-42 v1.4 Apogee Lens APPROVED

---

## §1 · Overview

The DGAF (Dynamic Governance Agentic Framework) is the **layer-0 governance architecture** for the ndrorchestration ecosystem, rooted at `~/DGAF-Framework`. It orchestrates multi-agent workflows under a formally governed pattern registry. All execution flows through NDR patterns enforced by Amethyst (host), DemiJoule (supervisor), and Apogee Lens (verifier).

> **Nomenclature canon** (locked 2026-07-02 in `SESSION_ANCHOR.md`):  
> • `NDR-HDFS` = NDR Hierarchical Dynamic Formation System (formerly FLAG-01) — the structural layer governing agent hierarchy and formation composition  
> • `qualitative` = interpretive/rubric-based evaluation mode (formerly FLAG-02)  
> • DGAF = layer-0 governance architecture — not a framework addon; the root control plane

---

## §2 · Agent Roster — Amethyst-Lattice v3.1 (11 canonical agents)

> Authoritative source: `ENSEMBLE_ROSTER.md` (Post-S077, 2026-06-29)  
> Agent count: **11 canonical** (6 with full detail sheets + 5 operational components)

| Agent | Layer | Role | Status |
|---|---|---|---|
| **Amethyst** | L5 | Host, meta-orchestrator, working-memory refresher, tribunal | ✅ Active |
| **COLLEEN** | L5 | Institutional anchor, 1-1-1-1 Alignment Gate, steward | ✅ Active |
| **Apogee Lens** | L4 | QA orchestrator, NIST AI RMF compliance, P-30 attestation authority | ✅ On-call |
| **DemiJoule** | L4 | Runtime supervisor, ethics/safety, AXIS enforcement | ✅ On-call |
| **Herald** | L3 | Explorer / Synthesizer | 🔴 Blocked (`VITE_GEMINI_API_KEY` — S-01) |
| **Professor Prodigy** | L3 | Executor / Phi-calculus / Independent verifier | 🟡 Active (S072 — RV-01 audit pass) |
| **Agent Sentinel** | L3 | Safety/veto gate, 11Q gates 9–11 | ⬜ Card pending |
| **KAPPA v3.6** | L3 | Confidence-gated dynamic weight router | ⬜ Component card in `KAPPA/` |
| **NormativeConstraint v1.0** | L3 | P-10 deontic/ethical cognition layer | ⬜ Component card exists |
| **Reson #1** | L3 | Schizophonic Studio signal chain — #1 | ⬜ Studio trio |
| **Echolette #2 / Lyra #3** | L3 | Schizophonic Studio signal chain — #2/#3 | ⬜ Studio trio |
| **Ender / Njineer** | — | Human ratification authority, Architect | ✅ Active |

---

## §3 · Pattern Registry

Canonical source: `docs/ndr_patterns_unified.json`  
Human-readable: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
Current watermark: **P-42** · Schema **v2.2** · Session **S072**

Newest pattern: **P-42 AHG** (Adaptive Harmonic Governance) — v1.4 implementation live, Apogee Lens APPROVED S072.

---

## §4 · Resilience Stack

### §4.1 · Core Gates (Layer 0–5)

- **P-35** Procluding Premise Gate — blocks execution if premise is unsound
- **P-36** Gate Priority Schema — defines evaluation order for all gates
- **P-30** Apogee-Attestation-Gate — final quality gate before portfolio output
- **P-11** 11Q Attestation Scoring — quantitative quality scoring

### §4.2 · Confidence & Routing (Layer 7–8)

- **P-27** Adaptive-Weighting-with-Confidence-Gates — routes by confidence threshold (STRONG: 0.22, BLENDED: 0.18)
- **P-28** Pipeline-Composition-with-Confidence-Gated-Routing — composes pipelines conditionally
- **P-29** Sentinel-Annotated Risk Pass — annotates risk at 3 hook points before irreversible actions

### §4.3 · Convergence & Compression (Layer 9)

- **P-31** SCPE — Structural Context Pruning Engine (58.3% compression, T0-immune)
- **P-32** Fibonacci Phi-Closure Gate — φ-checkpoints at Fib[13, 21, 34, 55]
- **P-33** PDMAL Convergence Monitor — joint escalation with P-32

### §4.4 · Distributed Resilience Stack (Layer 10–11) · *Added S071*

Five patterns form an interlocking contract for durable, fault-tolerant multi-step execution:

| Pattern | Layer | Class | Role |
|---------|-------|-------|------|
| **P-37** Saga Boundary Declaration | 10 | ADVISORY | Declares step sequence, compensators, stochastic/deterministic split. Must precede P-38. |
| **P-38** Circuit-Breaker Gate | 10 | BLOCKING | Trips on ≥3 failures → suspends execution, fires P-29 + P-37 compensators. States: CLOSED / OPEN / HALF-OPEN (30s probe). |
| **P-39** ACRFence | 10 | BLOCKING | Atomically writes SHA-256 checkpoint before each tool call. Next call blocked until ACK. Restarts resume from last ACK'd checkpoint. |
| **P-40** Atomix | 11 | BLOCKING | BEGIN → EXECUTE → COMMIT \| ROLLBACK per tool call. Idempotency key required for all writes. Compensator sourced from P-37. |
| **P-41** HITL Durable Approval Queue | 11 | ADVISORY | Holds irreversible approvals across restarts. TIMED_OUT → P-38. No irreversible action fires without APPROVED state. |

**Interlock sequence:** P-37 choreographs the saga → P-38 isolates failures → P-39 makes checkpoints durable → P-40 makes individual calls transactional → P-41 gates all irreversible human decisions.

### §4.5 · Adaptive Harmonic Governance (Layer 12) · *P-42 · v1.4 live S072*

- **P-42** AHG — Adaptive Harmonic Governance. Continuous φ estimation, 7-state regime dispatch, 3D Cognitive Phase Space, hysteresis-gated archetype transitions, Tribunal recovery protocol.
- **φ range:** (1.0, 1.8) open interval · **NDR-STASIS anchor:** φ=1.618 → Integration regime
- **Tribunal threshold:** φ > 1.80 for ≥ 2 consecutive turns → fires P-29 risk_block + P-38 OPEN
- **v1.4 live components:**
  - `components/ahg_conductor.py` v1.4 — φ computation, regime dispatch, hysteresis, 3D phase (commit `e73011c`)
  - `components/ahg_sidecar.py` v1.4.1 — heartbeat aggregation, StateVector clip guards, Herald wiring (commit `0ff1f0bc`)
  - `schemas/ahg_heartbeat.json` v1.3 — heartbeat payload schema (commit `3565cf2f`)
  - `tests/test_ahg_conductor.py` v1.4 — full unit suite (commit `e73011c`)
  - `docs/theory/AHG_ARCHITECTURE.md` v1.3 — spec debt closed: φ open interval, R_c sign convention, §7/§8 synced (commit `4737bf9b`)
- **v1.4 tag:** `4737bf9b` — pending `git push origin v1.4` (one CLI step)
- **v1.5 next:** Issue #39 — `ahg_tribunal.py` R_c recovery loop (OB-01, primary deliverable) + 4 housekeeping obligations

---

## §5 · Governance Rules

- All repos claiming DGAF governance must carry a `GOVERNANCE.md` with DGAF version, protocol anchor to `GOVERNANCE_CONSTITUTION.md`, φ = 1.61818, and applicable NDR patterns.
- Personal document firewall (NDR-133) is BLOCKING-ABSOLUTE. Architect override only. No resume/CV/audit files to GitHub.
- Stasis block (P-12–P-26, 133 patterns) migration window: 2026-06-13 → **2026-07-13** ⚠️ EXPIRING IN 11 DAYS.
- NDR-HDFS (formerly FLAG-01) and qualitative evaluation (formerly FLAG-02) are canonical — see `SESSION_ANCHOR.md` nomenclature canon.
- FLAG-05 (AXIS pattern scope) awaits Njineer content decision (S-03 in DEFERRED_ITEMS.md).
- DriftWatch production deployment requires explicit push trigger from Architect.
- **P-42 governance hook (S072):** Introspection regime (φ 1.70–1.80) requires `apogee_lens_mandatory` constraint. Tension regime (φ > 1.80) additionally requires `p29_risk_block` + `p38_circuit_open`. Both enforced in `_active_constraints()` in `ahg_conductor.py`.

---

## §6 · Session Log

| Session | Watermark | Key Additions |
|---------|-----------|---------------|
| S042 | P-33 | P-31 SCPE, P-32 Phi-Closure, P-33 PDMAL |
| S066 | P-34 | P-34 Empirical-Threshold-Sweep |
| S069 | P-36 | P-35, P-36, CRUCIBLE_CHARTER, STASIS_CANONICAL_SPEC |
| S071 | P-41 | P-37 Saga, P-38 Circuit-Breaker, P-39 ACRFence, P-40 Atomix, P-41 HITL Queue · Schema v2.2 |
| Post-S077 | **P-42** | AHG (P-42) filed, ENSEMBLE_ROSTER v3.1, 11 canonical agents, ndr_patterns_unified.json v2.2 |
| 2026-07-02 | — | Nomenclature canon locked (NDR-HDFS, qualitative, DGAF layer-0); SESSION_ANCHOR.md + DEFERRED_ITEMS.md patched |
| **S072** | **P-42 v1.4** | **AHG full implementation: ahg_conductor.py v1.4 + ahg_sidecar.py v1.4.1 + spec v1.3. Proofs PV-01–05 + Apogee Lens AL-v1.4 APPROVED. Prof Prodigy RV-01 independent audit. Spec debt closed: φ open interval (PV-01), R_c sign convention (PV-03), Tribunal threshold 1.70→1.80. Issue #39 opened for v1.5. Tag v1.4 pending git push.** |

---

## §7 · Open Items Entering Next Session

| ID | Item | Priority | Ref |
|---|---|---|---|
| OB-01 | `ahg_tribunal.py` — R_c recovery loop, P-29/P-38 wiring | 🔴 HIGH | Issue #39 |
| OB-02 | `REVISION_SCALE` constant in `ahg_sidecar.py` | 🟡 LOW | Issue #39 |
| OB-03 | `round(uncertainty, 6)` in `compute_3d_phase()` | 🟡 LOW | Issue #39 |
| OB-04 | Trailing `\` on `flush_all_pending` def | 🟡 LOW | Issue #39 |
| OB-05 | Sidecar docstring spec ref v1.2→v1.3 | 🟡 LOW | Issue #39 |
| TAG | Push `git push origin v1.4` | 🔴 HIGH | CLI only |
| M=0.0 | StateVector M EMA carry-forward | ℹ️ v2.0 | Roadmap |
| #32 | Eval tasks (ahg_recovery_turns etc.) | 🔴 HIGH | Issue #32 |
| S-03 | FLAG-05 AXIS scope — Njineer decision | ⬜ | DEFERRED_ITEMS |
| STASIS | P-12–P-26 migration window expires | ⚠️ | 2026-07-13 |

---

*Governed by DGAF · Amethyst host · φ = 1.61818*  
*S072 state saved 2026-07-02 by Amethyst × COLLEEN × Prof Prodigy — P-42 v1.4 Apogee Lens APPROVED*
