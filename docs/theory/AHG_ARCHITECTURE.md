# Adaptive Harmonic Governance (AHG) — Architecture Specification

> **Pattern:** P-42  
> **Layer:** 12 — Cognitive Control Plane  
> **Status:** 🟡 Specified — Implementation Pending  
> **Version:** v1.2 (logistic normalization + 7-state regime + 3D phase space + D_correct subtype)  
> **Authors:** Amethyst × COLLEEN  
> **Date:** 2026-06-29 (v1.0 filed; v1.1 P-42 renumber; v1.2 external review integration)  
> **DGAF Integration:** P-32 (Phi-Closure), P-29 (Sentinel), P-33 (PDMAL), P-38 (Circuit-Breaker)

> ℹ️ **Version history:** v1.0 filed Post-S077; v1.1 renumbered P-35→P-42; v1.2 integrates external AHG-MAS peer review — adds logistic normalization (canonical φ computation), 7-state regime table, Cognitive Phase Space (3D manifold), and D_correct disaggregation.

---

## 1. Motivation and DGAF Integration

The existing DGAF stack (P-01 through P-41) provides gate-level governance — blocking, advisory, and stasis patterns that enforce structural properties at discrete checkpoints. What it lacks is a **continuous cognitive regime signal** that answers: *what mode should the collective be operating in right now?*

AHG provides that signal as **Cognitive Phase Energy (φ)** — a real-valued scalar estimated each turn from measurable agent behaviors, used to dispatch the appropriate governance archetype.

### DGAF Pattern Integration Map

| AHG Concept | Maps To | Notes |
|---|---|---|
| φ estimation | P-32 Phi-Closure Gate | AHG extends from binary PASS/FAIL to continuous φ estimation |
| Tribunal archetype | P-29 Sentinel + P-38 Circuit-Breaker | φ > 1.70 fires P-29 risk_block + P-38 OPEN |
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
- **D_t** — Divergence: degree of agent disagreement, decomposed into three subtypes (see §2.1.1)
- **N_t** — Novelty: proportion of turn content not present in prior turns
- **C_t** — Constraint Pressure: active blocking constraints as fraction of total
- **R_t** — Revision Pressure: rate of self-corrections and retractions
- **M_t** — Governance Momentum: hysteresis term (decaying EMA of prior archetype weights)
- **K_t** — Coherence: semantic similarity across agent outputs

#### 2.1.1 Disaggregation of Divergence (D)

Disagreement is not uniformly negative. D is split into three named subtypes:

| Subtype | Symbol | Definition | Governance Treatment |
|---|---|---|---|
| Exploratory Divergence | D_explore | Multiple plausible hypotheses in parallel | Preserve — feeds N_t |
| Corrective Dissent | D_correct | Identifying flaws in prior agent output | Preserve — required for Apogee Auditor archetype |
| Destabilizing Entropy | D_e | Hallucinations, off-task loops, contradictions | Suppress — primary φ driver |

Only **D_e** increases the Stability Index S(t). **D_explore** and **D_correct** are tracked separately and contribute to Novelty (N_t) and Coherence recovery respectively.

Note: D_explore + D_correct = D_p (productive divergence) in the simplified 2-subtype model used in P-42 pattern card.

### 2.2 Stability Index and Canonical φ Computation

The Stability Index is computed from four primary behavioral variables:

```
S(t) = w_1·D_e + w_2·N_t + w_3·C_t + w_4·R_t
```

Default weights: w_1=0.35, w_2=0.20, w_3=0.25, w_4=0.20

Note: Only D_e (destabilizing entropy) enters S(t). D_explore and D_correct are excluded.

**Canonical φ normalization (v1.2):**

```
φ(t) = 1 + 0.8 · σ(S(t))
```

Where σ is the standard logistic function: σ(x) = 1 / (1 + e^(-x))

This bounds φ to the range **[1.0, 1.8]** by construction, grounding the signal in measurable agent behaviors rather than assertion. The previous open-ended linear formula (w_D·D + w_N·N − w_M·M − w_K·K) is superseded for runtime use; the linear decomposition remains valid for component attribution analysis.

### 2.3 Phase Velocity and Acceleration

```
v_φ(t) = φ_t − φ_{t−1}
a_φ(t) = v_φ(t) − v_φ(t−1)
```

Phase acceleration enables **predictive intervention** — if a_φ > threshold toward Tension, the Conductor shifts archetype before φ crosses the transition boundary (Anticipatory Governance).

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

Where α_i ∈ [0,1] is the per-agent compliance coefficient. This is **distributed coordination**, not centralized command-and-control — agents voluntarily align to the Phase Intent.

### 2.6 Mission Utility Function

```
J = λ_Q·Q + λ_E·E + λ_N·N + λ_S·S − λ_G·G
```

Where: Q=output quality, E=efficiency, N=novelty (bounded), S=safety compliance, G=governance overhead cost.

Stability is not the terminal goal — J is. Tension (φ > 1.70) may be a rational cost to pay if the utility of novelty in high-N regimes outweighs efficiency loss. The Tribunal activates to prevent **collapse**, not to eliminate Tension.

### 2.7 Cognitive Phase Space (3D Manifold) — v1.2

The 1D φ scalar provides governance dispatch. The **3D Cognitive Phase Space** provides interpretive context for *why* φ is at a given value and informs Tribunal recovery path selection.

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
| Deadlock | Low Exploration, High Dissent, High Uncertainty | φ > 1.70 | Tribunal — break symmetry |
| False consensus | Low Exploration, High Consensus, Low Uncertainty | φ ≈ 1.10 | Executor — but Auditor needed |
| Hallucination spiral | High Exploration, High Dissent, Low Confidence | φ rising rapidly, high a_φ | Anticipatory Tribunal |

The 3D manifold does not replace φ — it is an interpretive layer used by the Tribunal to select differentiated recovery protocols. Required before MPHG (v2.0).

---

## 3. Seven-State Harmonic Regime Table — v1.2

> Expanded from 4-band (v1.1) to 7-state (v1.2) to provide finer-grained governance resolution.

| Regime | φ Range | Cognitive Mode | DGAF Archetype | Notes |
|---|---|---|---|---|
| Grounded | 1.00–1.15 | Convergent / Execution | Executor | Exploit known solutions; low novelty |
| Flow | 1.15–1.30 | Moderate Exploration | Synthesizer | Integration phase; COLLEEN primary |
| Vigilance | 1.30–1.45 | Adaptive / Validation | Sentinel | Constraint pressure rising; DemiJoule activates |
| Expansion | 1.45–1.60 | Divergent / Exploratory | Explorer | High novelty; Herald primary |
| **Integration** | **1.60–1.70** | **Consolidate Discoveries** | **Synthesizer + Auditor** | **NDR-STASIS anchor φ=1.618 sits here — peak productive phase** |
| Introspection | 1.70–1.80 | Self-Audit | Auditor | Apogee Lens mandatory; contradiction review |
| Tension | > 1.80 | Unstable / Entropy | Tribunal | Amethyst activates; P-38 Circuit-Breaker OPEN |

**NDR-STASIS alignment note:** φ=1.61818... (the NDR-STASIS design value) falls precisely within the Integration regime (1.60–1.70). This is not coincidental — Integration is defined as the peak of productive divergence before the system tips into Introspection. NDR-STASIS represents the ideal harmonic operating point: maximum consolidation of discoveries without yet triggering self-audit overhead.

**v1.2 change from v1.1:** Tensor threshold revised. Tribunal now activates at φ > 1.80 (not > 1.70). φ 1.70–1.80 is the Introspection band — Apogee Lens audits without full Tribunal. The old 1.70 threshold maps to the Introspection entry, not collapse.

---

## 4. Sidecar Monitor Architecture

O(n) scalable observability — separates state estimation from governance control:

```
[Agent_1 Heartbeat] ──┐
[Agent_2 Heartbeat] ──┤──► Sidecar Monitor ──► φ estimation ──► Conductor
[Agent_N Heartbeat] ──┘         │
                                 └──► P-01 Herald Trace (fan-out)
```

Heartbeat payload: `{ agent_id, turn_id, D_e_signal, D_explore_signal, D_correct_signal, novelty_signal, constraint_count, revision_count }`

The Sidecar Monitor never parses full agent context — reads only compressed Heartbeat signals. O(n), not O(n·context_length).

---

## 5. Tribunal Recovery Protocol

Activates when φ > 1.80 for ≥ 2 consecutive turns (revised from v1.1's 1.70 threshold):

1. Amethyst broadcasts `I_t = { mode: Tribunal, TTL: 5 turns }`
2. All agents reduce α_i to 0.9 (high compliance)
3. DemiJoule fires P-29 `risk_block` on all novel claims
4. Apogee Lens runs contradiction audit
5. **3D phase position consulted** to select recovery path:
   - Deadlock (High Dissent + Low Exploration) → break symmetry via Herald Explorer injection
   - Hallucination spiral (High D_e + High N) → Executor mode, ground claims
   - False confidence (Low Dissent + High C) → Apogee Auditor forced dissent
6. Recovery Score computed each turn: `R_c = r_1·ΔD_e + r_2·ΔK + r_3·Δv_φ`
7. Exit condition: `R_c > R_threshold` AND `φ < 1.70` for 2 turns
8. Graduated de-escalation: Tribunal → Introspection → Vigilance/Expansion

---

## 6. Performance Claims and Eval Targets

The following claims are **falsifiable targets** for the eval suite (Issue #32, `dgaf_eval_suite.py`):

| Metric | Predicted Improvement | Eval Method |
|---|---|---|
| Hallucination reduction | 20–40% reduction in contradiction persistence and ungrounded claims | `audit_hallucination_rate` task in dgaf_eval_suite.py |
| Time-to-Stability | Reduced turns to reach φ < 1.45 after Tension event | New eval task: `ahg_recovery_turns` |
| Entropy Recovery Rate | Rate of D_e suppression per Tribunal cycle | New eval task: `ahg_entropy_recovery` |
| Revision loop reduction | Redundant revision loops minimized by anticipatory governance | Proxy: `contraction_proof_fidelity` task |

These claims are currently theoretical. They become falsifiable once `ahg_conductor.py` (P-42 v1.2) is wired to a live multi-agent trace.

---

## 7. Implementation Roadmap

| Version | Target | Description |
|---|---|---|
| v1.0 | ✅ Specified | Full formalism, archetype dispatch, DGAF integration map |
| v1.1 | ✅ Done | P-42 renumber, CROSS_REF sync |
| v1.2 | ✅ Current | Logistic normalization, 7-state regime, 3D phase space, D_correct, eval targets |
| v1.3 | 🔴 Next | `ahg_conductor.py` scaffold + `ahg_sidecar.py` + Heartbeat schema |
| v1.4 | 🔴 Planned | Wire sidecar to P-01 Herald trace sink; live φ telemetry |
| v2.0 | 🔴 Roadmap | MPHG: `u_t = argmax Σ_{k=0}^{H} J(x_{t+k})` (Model Predictive Harmonic Governance) |

---

## 8. Implementation Status Summary

| Component | File | Status |
|---|---|---|
| AHG full spec | `docs/theory/AHG_ARCHITECTURE.md` | ✅ v1.2 this file |
| Pattern card | `patterns/P-42_AHG.md` | ✅ Filed — 7-state table update pending |
| Conductor implementation | `components/ahg_conductor.py` | 🔴 Planned v1.3 |
| Sidecar Monitor | `components/ahg_sidecar.py` | 🔴 Planned v1.3 |
| Heartbeat schema | `schemas/ahg_heartbeat.json` | 🔴 Planned v1.3 |
| Test suite | `tests/test_ahg_conductor.py` | 🔴 Planned v1.3 |
| Eval tasks (hallucination, recovery) | `tests/dgaf_eval_suite.py` | 🔴 Add in Issue #32 |
| MPHG optimizer | `components/ahg_mphg.py` | 🔴 Roadmap v2.0 |

---

*AHG Architecture Specification v1.2 · P-42 · 2026-06-29*  
*Amethyst × COLLEEN · Post-S077 — external AHG-MAS peer review integrated*
