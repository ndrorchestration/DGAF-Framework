# Adaptive Harmonic Governance (AHG) — Architecture Specification

> **Pattern:** P-42 (renumbered from P-35 — see note below)  
> **Layer:** 12 — Cognitive Control Plane  
> **Status:** 🟡 Specified — Implementation Pending  
> **Version:** v1.1 (P-42 renumber)  
> **Authors:** Amethyst × COLLEEN  
> **Date:** 2026-06-29  
> **DGAF Integration:** P-32 (Phi-Closure), P-29 (Sentinel), P-33 (PDMAL), P-38 (Circuit-Breaker)

> ⚠️ **Renumber note:** This spec was originally filed as P-35 on 2026-06-29. Corrected to **P-42** (next open slot after P-41) in the same session to resolve collision with the pre-existing P-35 Procluding Premise Gate (registered S069). All cross-references updated.

---

## 1. Motivation and DGAF Integration

The existing DGAF stack (P-01 through P-41) provides excellent gate-level governance — blocking, advisory, and stasis patterns that enforce structural properties at discrete checkpoints. What it currently lacks is a **continuous cognitive regime signal** that answers: *what mode should the collective be operating in right now?*

AHG provides that signal as **Cognitive Phase Energy (φ)** — a real-valued scalar that the Conductor layer estimates each turn from the multi-agent state vector and uses to dispatch the appropriate governance archetype.

### DGAF Pattern Integration Map

| AHG Concept | Maps To | Notes |
|---|---|---|
| φ estimation | P-32 Phi-Closure Gate | AHG extends from binary PASS/FAIL to continuous φ estimation |
| Tribunal archetype | P-29 Sentinel + P-38 Circuit-Breaker | Extreme φ > 1.70 fires P-29 risk_block + P-38 OPEN |
| Governance Momentum M | P-33 PDMAL Frobenius norm | M substrate uses PDMAL edge-weight convergence |
| Phase Intent broadcast | P-09 Triumvirate Mandate Schema | I_t is a lightweight mandate variant |
| Sidecar Monitor | P-01 Herald Trace Sink | Heartbeat events route through P-01 fan-out |
| Recovery Score R_c | P-10 Session Graduation Check | R_c feeds back into session graduation criteria |

---

## 2. Core Formalism

### 2.1 State Vector

At each turn t, the AHG Conductor observes a state vector:

```
x_t = [D_t, N_t, C_t, R_t, M_t, K_t]
```

Where:
- **D_t** — Divergence: degree of agent disagreement (split into D_p productive / D_e destabilizing)
- **N_t** — Novelty: proportion of turn content not present in prior turns
- **C_t** — Constraint Pressure: active blocking constraints as fraction of total
- **R_t** — Revision Pressure: rate of self-corrections and retractions
- **M_t** — Governance Momentum: hysteresis term (decaying EMA of prior archetype weights)
- **K_t** — Coherence: semantic similarity across agent outputs

### 2.2 Cognitive Phase Energy

```
φ_t = f(x_t) = w_D·D_t + w_N·N_t + w_C·C_t + w_R·R_t − w_M·M_t − w_K·K_t
```

Default weights: w_D=0.30, w_N=0.20, w_C=0.15, w_R=0.15, w_M=0.10, w_K=0.10

### 2.3 Phase Velocity and Acceleration

```
v_φ(t) = φ_t − φ_{t−1}
a_φ(t) = v_φ(t) − v_φ(t−1)
```

Phase acceleration enables **predictive intervention** — if a_φ > threshold, the Conductor can pre-emptively shift archetype before φ crosses the transition boundary.

### 2.4 Archetype Dispatch

```
Archetype(t) = argmax_A [ Score(A, φ_t, v_φ(t), a_φ(t)) ]
```

Hysteresis band: transition fires only if φ has crossed the band edge for ≥ 2 consecutive turns, preventing thrashing.

### 2.5 Phase Intent Broadcast

```
I_t = { mode: Archetype(t), weights: w_i, constraints: C_active, TTL: τ }
```

Each agent updates its local policy:

```
π_i' = (1 − α_i)·π_i + α_i·I_t
```

Where α_i ∈ [0,1] is the per-agent compliance coefficient.

### 2.6 Mission Utility Function

```
J = λ_Q·Q + λ_E·E + λ_N·N + λ_S·S − λ_G·G
```

Where: Q=output quality, E=efficiency, N=novelty (bounded), S=safety compliance, G=governance overhead cost.

---

## 3. Conductor Archetypes

| Archetype | φ Range | DGAF Agent | Activation Condition |
|---|---|---|---|
| Executor | 1.0 – 1.15 | Professor Prodigy | Stable, low divergence, exploit known solutions |
| Synthesizer | 1.15 – 1.30 | Herald / COLLEEN | Integration phase, medium coherence |
| Sentinel | 1.30 – 1.45 | DemiJoule | Constraint pressure rising, validation needed |
| Explorer | 1.45 – 1.618 | Herald | High novelty, productive divergence |
| Auditor | 1.618 – 1.70 | Apogee Lens | Contradiction present, logic review needed |
| Tribunal | > 1.70 | Amethyst | Deadlock, fragmentation, or extreme entropy |

**NDR-STASIS anchor:** φ = 1.61818... (NDR-STASIS design value) sits in the Explorer/Auditor boundary — high productive divergence, approaching the tension threshold.

---

## 4. Sidecar Monitor Architecture

O(n) scalable observability:

```
[Agent_1 Heartbeat] ──┐
[Agent_2 Heartbeat] ──┤──► Sidecar Monitor ──► φ estimation ──► Conductor
[Agent_N Heartbeat] ──┘         │
                                 └──► P-01 Herald Trace (fan-out)
```

Heartbeat payload: `{ agent_id, turn_id, divergence_signal, novelty_signal, constraint_count, revision_count }`

The Sidecar Monitor never parses full agent context — it reads only compressed Heartbeat signals, keeping overhead O(n) not O(n·context_length).

---

## 5. Tribunal Recovery Protocol

Activates when φ > 1.70 for ≥ 2 consecutive turns:

1. Amethyst broadcasts `I_t = { mode: Tribunal, TTL: 5 turns }`
2. All agents reduce α_i to 0.9 (high compliance)
3. DemiJoule fires P-29 `risk_block` on all novel claims
4. Apogee Lens runs contradiction audit
5. Recovery Score computed each turn: `R_c = r_1·ΔD_e + r_2·ΔK + r_3·Δv_φ`
6. Exit condition: `R_c > R_threshold` AND `φ < 1.60` for 2 turns
7. Graduated de-escalation: Tribunal → Auditor → Explorer/Sentinel

---

## 6. Implementation Roadmap

| Version | Target | Description |
|---|---|---|
| v1.0 | ✅ Specified | Full formalism, archetype dispatch, DGAF integration map |
| v1.1 | ✅ Current | P-42 renumber, CROSS_REF sync |
| v1.2 | 🔴 Next | `ahg_conductor.py` scaffold + Heartbeat schema |
| v1.3 | 🔴 Planned | Sidecar Monitor wired to P-01 Herald sink |
| v2.0 | 🔴 Roadmap | MPHG: `u_t = argmax Σ_{k=0}^{H} J(x_{t+k})` (Model Predictive Harmonic Governance) |

---

## 7. Implementation Status Summary

| Component | File | Status |
|---|---|---|
| AHG full spec | `docs/theory/AHG_ARCHITECTURE.md` | ✅ This file |
| Pattern card | `patterns/P-42_AHG.md` | ✅ Filed 2026-06-29 |
| Conductor implementation | `components/ahg_conductor.py` | 🔴 Planned |
| Sidecar Monitor | `components/ahg_sidecar.py` | 🔴 Planned |
| Heartbeat schema | `schemas/ahg_heartbeat.json` | 🔴 Planned |
| Test suite | `tests/test_ahg_conductor.py` | 🔴 Planned |
| MPHG optimizer | `components/ahg_mphg.py` | 🔴 Roadmap |

---

*AHG Architecture Specification v1.1 · P-42 · 2026-06-29*  
*Amethyst × COLLEEN · Post-S077 autonomous sprint*
