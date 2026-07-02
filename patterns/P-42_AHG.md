# P-42 — Adaptive Harmonic Governance (AHG)

> **Pattern ID:** P-42
> **Layer:** 12 — Cognitive Control Plane
> **P-36 Class:** ADVISORY (v1.1) → BLOCKING (v2.0 MPHG target)
> **Status:** 🟡 Specified — Implementation Pending
> **Registered:** 2026-06-29 · Post-S077 autonomous sprint
> **Version:** v1.3-card (Phase A coherence sync — S072 · 2026-07-02)
> **Steward:** Amethyst × COLLEEN
> **Full spec:** [`docs/theory/AHG_ARCHITECTURE.md`](../docs/theory/AHG_ARCHITECTURE.md)

---

## Summary

AHG is a control-theoretic governance layer that continuously estimates the **Cognitive Phase Energy** (φ) of the multi-agent collective and dispatches **Conductor Archetypes** to steer the ensemble toward productive divergence and away from destabilizing entropy.

It sits above the existing gate stack (P-35–P-41) as a **meta-governance signal** — it does not replace any gate but modulates the operational mode that agents run in between gates.

---

## Core Concepts

| Term | Symbol | Definition |
|---|---|---|
| Cognitive Phase Energy | φ | Central governance signal — continuous measure of harmonic regime. Range [1.0, 1.8] via logistic normalization. |
| Stability Index | S(t) | Raw input to φ: w_1·D_e + w_2·N + w_3·C + w_4·R |
| Phase Velocity | v_φ | Directional rate of change of φ |
| Phase Acceleration | a_φ | Second derivative — enables predictive intervention |
| State Vector | x_t | D, N, C, R, M, K (Divergence, Novelty, Constraint, Revision, Momentum, Coherence) |
| Exploratory Divergence | D_explore | Useful hypothesis generation — preserved, feeds Novelty |
| Corrective Dissent | D_correct | Flaw identification — preserved, feeds Apogee Auditor |
| Destabilizing Entropy | D_e | Hallucination / loops — suppressed, enters S(t) |
| Productive Divergence | D_p | D_explore + D_correct (simplified 2-subtype model) |
| Conductor Archetype | — | Governance regime selector: Executor, Flow/Synthesizer, Sentinel, Explorer, Integrator, Auditor, Tribunal |
| Phase Intent | I_t | Broadcast packet (mode, weights, constraints, TTL) |
| Compliance Coefficient | α_i | Per-agent conformance weight |
| Mission Utility Function | J | λ_Q·Q + λ_E·E + λ_N·N + λ_S·S − λ_G·G |
| Recovery Score | R_c | Tribunal exit criterion |
| Governance Momentum | M | Hysteresis term preventing mode thrashing |

---

## φ Canonical Computation

```
S(t) = w_1·D_e + w_2·N + w_3·C + w_4·R
φ(t) = 1 + 0.8 · σ(S(t))        where σ(x) = 1 / (1 + e^(-x))
```

**Default weights:** w_1=0.35, w_2=0.20, w_3=0.25, w_4=0.20

Only D_e (destabilizing entropy) enters S(t). D_explore and D_correct are excluded and tracked separately.

This bounds φ ∈ [1.0, 1.8] by construction. φ is derived from measurable agent behaviors, not asserted.

---

## Seven-State Harmonic Regime Table

| Regime | φ Range | Cognitive Mode | DGAF Archetype | Notes |
|---|---|---|---|---|
| Grounded | 1.00–1.15 | Convergent / Execution | Executor | Exploit known solutions |
| Flow | 1.15–1.30 | Moderate Exploration | Synthesizer | COLLEEN primary |
| Vigilance | 1.30–1.45 | Adaptive / Validation | Sentinel | DemiJoule activates |
| Expansion | 1.45–1.60 | Divergent / Exploratory | Explorer | Herald primary |
| **Integration** | **1.60–1.70** | **Consolidate Discoveries** | **Synthesizer + Auditor** | **NDR-STASIS φ=1.618 — peak productive phase** |
| Introspection | 1.70–1.80 | Self-Audit | Auditor | Apogee Lens mandatory |
| Tension | > 1.80 | Unstable / Entropy | Tribunal | Amethyst + P-38 OPEN |

---

## 3D Cognitive Phase Space

The 1D φ scalar drives archetype dispatch. The **3D Cognitive Phase Space** provides interpretive context for *why* φ is at a given value and informs Tribunal recovery path selection. Required before MPHG (v2.0).

**Phase Space Axes:**

| Axis | Poles | Role |
|---|---|---|
| Axis 1 | Exploration ↔ Exploitation | Is the collective generating new hypotheses or executing known solutions? |
| Axis 2 | Consensus ↔ Dissent | Are agents converging or diverging on outputs? |
| Axis 3 | Confidence ↔ Uncertainty | Are agents asserting or hedging? |

**Trajectory examples:**

| State | 3D Position | φ Implication | Tribunal Response |
|---|---|---|---|
| Productive research sprint | High Exploration, High Dissent, High Uncertainty | φ ≈ 1.50–1.618 | Explorer archetype, preserve |
| Deadlock | Low Exploration, High Dissent, High Uncertainty | φ > 1.80 | Tribunal — break symmetry via Herald Explorer injection |
| False consensus | Low Exploration, High Consensus, Low Uncertainty | φ ≈ 1.10 | Executor — but Auditor forced dissent needed |
| Hallucination spiral | High Exploration, High Dissent, Low Confidence | φ rising rapidly, high a_φ | Anticipatory Tribunal — ground claims, Executor mode |

> Full formalism: `docs/theory/AHG_ARCHITECTURE.md` §2.7

---

## Conductor Archetype × Agent Mapping

| Archetype | DGAF Agent | Primary Bias |
|---|---|---|
| Executor | Professor Prodigy | Low novelty, precision execution |
| Synthesizer | Herald / COLLEEN | Integration, coherence |
| Sentinel | DemiJoule | Validation, constraint enforcement |
| Explorer | Herald | High novelty, hypothesis generation |
| Auditor | Apogee Lens | Contradiction discovery, logic review |
| Tribunal | Amethyst | Convergence, de-escalation, failure resolution |

---

## Interaction with Existing Patterns

- **P-32 (Phi-Closure Gate):** P-42 AHG extends P-32 from binary (PASS/FAIL) to continuous φ estimation
- **P-29 (Sentinel):** Tribunal archetype (φ > 1.80) fires P-29 `risk_block` via DemiJoule
- **P-33 (PDMAL):** Governance Momentum (M) tracked via PDMAL Frobenius norm substrate
- **P-38 (Circuit-Breaker):** AHG Tribunal mode emits circuit-breaker OPEN signal on φ > 1.80

---

## Implementation Status

| Component | File | Status |
|---|---|---|
| AHG full spec | `docs/theory/AHG_ARCHITECTURE.md` | ✅ v1.2 |
| Pattern card | `patterns/P-42_AHG.md` | ✅ v1.3-card (this file) |
| Conductor implementation | `components/ahg_conductor.py` | 🔴 Planned v1.3 |
| Sidecar Monitor | `components/ahg_sidecar.py` | 🔴 Planned v1.3 |
| Heartbeat schema | `schemas/ahg_heartbeat.json` | 🔴 Planned v1.3 |
| Test suite | `tests/test_ahg_conductor.py` | 🔴 Planned v1.3 |
| Eval tasks (hallucination, recovery) | `tests/dgaf_eval_suite.py` | 🔴 Add in Issue #32 |
| MPHG optimizer | `components/ahg_mphg.py` | 🔴 Roadmap v2.0 |

---

*P-42 · AHG · Adaptive Harmonic Governance · v1.3-card · 2026-07-02 · Amethyst × COLLEEN*
*Phase A coherence sync (S072): 3D Phase Space added (A1), S(t) default weights added (A2), impl table completed (A3)*
