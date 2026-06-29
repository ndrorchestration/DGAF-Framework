# Adaptive Harmonic Governance (AHG) — Architecture Specification

> **Pattern:** P-42
> **Layer:** 12 — Cognitive Control Plane
> **Status:** 🟡 Specified — Implementation Pending
> **Version:** v1.2 (logistic normalization · 7-state regime · cognitive phase space · D_correct subtype)
> **Authors:** Amethyst × COLLEEN
> **Date:** 2026-06-29
> **DGAF Integration:** P-32 (Phi-Closure), P-29 (Sentinel), P-33 (PDMAL), P-38 (Circuit-Breaker)
> **Companion:** [`docs/theory/AHG_STABILITY_ANALYSIS.md`](AHG_STABILITY_ANALYSIS.md)

> ⚠️ **Renumber note:** Originally filed as P-35 on 2026-06-29. Corrected to **P-42** (next open slot after P-41) to resolve collision with the pre-existing P-35 Procluding Premise Gate (S069).

---

## 1. Motivation and DGAF Integration

The existing DGAF stack (P-01 through P-41) provides gate-level governance — blocking, advisory, and stasis patterns that enforce structural properties at discrete checkpoints. What it currently lacks is a **continuous cognitive regime signal** that answers: *what mode should the collective be operating in right now?*

AHG provides that signal as **Cognitive Phase Energy (φ)** — a real-valued scalar derived from measurable agent behaviors via a logistic normalization that the Conductor layer uses to dispatch the appropriate governance archetype.

### DGAF Pattern Integration Map

| AHG Concept | Maps To | Notes |
|---|---|---|
| φ estimation | P-32 Phi-Closure Gate | AHG extends from binary PASS/FAIL to continuous φ estimation |
| Tribunal archetype | P-29 Sentinel + P-38 Circuit-Breaker | φ > 1.80 fires P-29 `risk_block` + P-38 OPEN |
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

- **D_t** — Divergence: degree of agent disagreement. Decomposed into three subtypes (see §2.1.1):
  - **D_explore** — Exploratory divergence: multiple plausible hypotheses (desired; increases φ moderately)
  - **D_correct** — Corrective dissent: identification of flaws, contradictions, or errors (desired; increases φ moderately — primary signal for Auditor archetype activation)
  - **D_entropy** — Destabilizing entropy: hallucinations, off-task reasoning, loops (suppressed; increases φ steeply)
- **N_t** — Novelty: proportion of turn content not present in prior turns
- **C_t** — Constraint Pressure: active blocking constraints as fraction of total
- **R_t** — Revision Pressure: rate of self-corrections and retractions
- **M_t** — Governance Momentum: hysteresis term (decaying EMA of prior archetype weights)
- **K_t** — Coherence: semantic similarity across agent outputs

The composite Divergence input to the Stability Index is:

```
D_t = w_explore·D_explore + w_correct·D_correct + w_entropy·D_entropy
```

Default subtype weights: w_explore = 0.3, w_correct = 0.4, w_entropy = 1.0

> **Rationale:** D_entropy is weighted 1.0 (full pass-through) because destabilizing entropy is the primary driver of Tribunal activation. D_correct is weighted above D_explore because corrective dissent is higher-value signal than exploratory divergence — it identifies actual system failure modes.

#### 2.1.1 Subtype Classification Heuristics

| Subtype | Observable Indicators |
|---|---|
| D_explore | Multiple divergent but internally consistent hypotheses; no contradiction with prior established facts |
| D_correct | Direct contradiction of a prior claim with evidence or logical argument; Apogee Lens dissent signal |
| D_entropy | Repetition of disproved claims; circular revision loops; hallucinated citations; off-task output |

---

### 2.2 Stability Index and φ Normalization

#### 2.2.1 Stability Index

The raw Stability Index S(t) is a weighted linear combination of the primary state variables:

```
S(t) = w_D·D_t + w_N·N_t + w_C·C_t + w_R·R_t
```

Default weights: w_D = 0.30, w_N = 0.20, w_C = 0.15, w_R = 0.15

> The momentum (M_t) and coherence (K_t) terms enter as *suppressors* in §2.2.2, not as additive drivers in S(t). This preserves the semantic clarity of S(t) as a pure instability signal.

#### 2.2.2 Logistic Normalization — Canonical φ Computation

φ is derived from S(t) via logistic normalization, bounding it to the interval [1.0, 1.8]:

```
φ(t) = 1 + 0.8 · σ(S_adj(t))
```

Where σ is the standard logistic function:

```
σ(x) = 1 / (1 + exp(−x))
```

And S_adj incorporates the suppressor terms:

```
S_adj(t) = S(t) − w_M·M_t − w_K·K_t
```

Default suppressor weights: w_M = 0.10, w_K = 0.10

**Boundary guarantees:**
- φ(t) → 1.0 as S_adj → −∞ (perfect coherence, zero instability)
- φ(t) → 1.8 as S_adj → +∞ (maximum entropy, fully incoherent)
- φ(t) = 1.4 when S_adj = 0 (logistic midpoint — baseline neutral state)

> **Anti-numerology note:** φ is not asserted. It is fully derived from four independently measurable behavioral variables (D, N, C, R) via a monotone bounded function. The Fibonacci ratio φ = 1.618 emerges as a regime landmark within the derived range — it is not a design parameter.

**NDR-STASIS anchor alignment:** φ = 1.618 (NDR-STASIS design value) falls in the Integration regime (1.60–1.70). This is the peak consolidation phase — the collective is at maximum productive divergence before tipping into Introspection. The NDR-STASIS anchor is not arbitrary: it is the natural equilibrium between Explorer-mode exploration and Auditor-mode contradiction resolution.

---

### 2.3 Phase Velocity and Acceleration

```
v_φ(t) = φ(t) − φ(t−1)
a_φ(t) = v_φ(t) − v_φ(t−1)
```

Phase acceleration enables **predictive (anticipatory) governance**: if a_φ(t) exceeds a threshold θ_a while φ(t) is still below a transition boundary, the Conductor pre-empts the transition rather than reacting after the fact.

**Anticipatory Tribunal trigger:**

```
IF a_φ(t) > θ_a AND φ(t) > φ_warn THEN pre_empt_tribunal()
```

Where φ_warn = 1.70 (one regime below the hard Tension boundary at 1.80).

---

### 2.4 Archetype Dispatch

```
Archetype(t) = argmax_A [ Score(A, φ(t), v_φ(t), a_φ(t)) ]
```

**Hysteresis constraint:** A transition fires only if φ has remained in the new regime band for ≥ 2 consecutive turns. This prevents thrashing at band boundaries and gives the system "temperament" — a resistance to transient noise.

**Score function structure:**

```
Score(A, φ, v_φ, a_φ) = Affinity(A, φ) + β_v · Momentum_bias(A, v_φ) + β_a · Anticipation_bias(A, a_φ)
```

Where Affinity(A, φ) is the archetype's φ-range match score, Momentum_bias rewards archetypes aligned with the direction of travel, and Anticipation_bias weights archetypes suited to where φ is heading.

---

### 2.5 Phase Intent Broadcast

```
I_t = { mode: Archetype(t), weights: w_i, constraints: C_active, TTL: τ }
```

Each agent updates its local policy:

```
π_i' = (1 − α_i)·π_i + α_i·I_t
```

Where α_i ∈ [0,1] is the per-agent compliance coefficient.

> This is **distributed coordination**, not centralized command. Agents voluntarily adjust their policies toward the broadcast intent. An agent with α_i = 0 is fully autonomous; α_i = 1 is fully compliant. Tribunal mode sets all α_i = 0.9.

---

### 2.6 Mission Utility Function

```
J = λ_Q·Q + λ_E·E + λ_N·N + λ_S·S − λ_G·G
```

Where: Q = output quality, E = efficiency, N = novelty (bounded), S = safety compliance, G = governance overhead cost.

> **Key implication:** Tension (φ > 1.80) is a cost, but it may be worth paying when λ_N is high (e.g., scientific discovery, creative generation). The system does not treat stability as the terminal objective — it treats J-maximization as the terminal objective and stability as a constraint.

---

### 2.7 Cognitive Phase Space

φ is a 1D projection of a higher-dimensional cognitive state. To enable richer Tribunal recovery strategies, AHG maintains a 3D **Cognitive Phase Space** context vector alongside φ:

```
CPS_t = (Exploration_t, Consensus_t, Confidence_t)
```

Where each axis is a normalized [0,1] scalar:

| Axis | High Value | Low Value | Primary Source Variable |
|---|---|---|---|
| Exploration ↔ Exploitation | High N_t, high D_explore | Low N_t, high K_t | N_t, D_explore |
| Consensus ↔ Dissent | Low D_t overall | High D_t, high D_correct | D_t subtypes |
| Confidence ↔ Uncertainty | Low R_t, low C_t | High R_t, high C_t | R_t, C_t |

**Why this matters for recovery:** Two collectives at identical φ = 1.75 may require different de-escalation strategies:

- CPS = (High Exploration, High Dissent, Low Confidence) → agents are generating many uncertain hypotheses with no convergence signal. Tribunal mode should bias toward Synthesizer archetype output.
- CPS = (Low Exploration, High Dissent, High Confidence) → agents are confident but in conflict. Tribunal mode should bias toward Auditor archetype — a logical adjudication is needed, not more synthesis.

**CPS is an interpretive layer, not a control variable.** It contextualizes *why* φ is at a given value. It is required for MPHG (v2.0) but optional in v1.2 implementation.

```
CPS_t is logged to P-01 Herald Trace on every turn for post-hoc analysis.
It does not directly modify Archetype(t) in v1.x.
```

---

## 3. Seven-State Conductor Regime Table

The logistic normalization yields a natural 7-state partition of [1.0, 1.8]:

| Regime | φ Range | Cognitive Mode | DGAF Archetype | Activation Condition |
|---|---|---|---|---|
| Grounded | 1.00 – 1.15 | Convergent execution | Executor (Prodigy) | Stable, low divergence; exploit established plans |
| Flow | 1.15 – 1.30 | Moderate exploration | Synthesizer (Herald/COLLEEN) | Medium novelty; integration phase |
| Vigilance | 1.30 – 1.45 | Validation-first | Sentinel (DemiJoule) | Constraint pressure rising; validation needed |
| Expansion | 1.45 – 1.60 | Generative divergence | Explorer (Herald) | High novelty; productive D_explore dominant |
| Integration | 1.60 – 1.70 | Consolidation | Explorer → Auditor transition | Consolidate discoveries; NDR-STASIS anchor φ=1.618 here |
| Introspection | 1.70 – 1.80 | Self-audit | Auditor (Apogee Lens) | Contradiction present; logic review required; anticipatory Tribunal watch |
| Tension | > 1.80 | Crisis / override | Tribunal (Amethyst) | Deadlock, fragmentation, D_entropy dominant; hard ceiling |

> **v1.1 → v1.2 change:** The previous 4-band table (Grounded / Adaptive / Divergent / Tension) is replaced by this 7-state table. The hard ceiling moves from 1.70 to **1.80** (the logistic asymptote), and a new **Introspection** band is inserted at 1.70–1.80. Tribunal activation threshold is updated accordingly in §5.
>
> **DGAF archetype mapping note:** The previous Explorer band (1.45–1.618) and Auditor band (1.618–1.70) are preserved as the Expansion and Integration+Introspection sub-bands. The Explorer/Auditor transition at φ = 1.618 is retained as the NDR-STASIS anchor.

---

## 4. Sidecar Monitor Architecture

O(n) scalable observability — the Sidecar Monitor decouples state estimation from governance control:

```
[Agent_1 Heartbeat] ──┐
[Agent_2 Heartbeat] ──┤──► Sidecar Monitor ──► φ(t) estimation ──► Conductor
[Agent_N Heartbeat] ──┘              │
                                      └──► P-01 Herald Trace (fan-out)
                                      └──► CPS_t logging (§2.7)
```

Heartbeat payload (schema: `schemas/ahg_heartbeat.json`):

```json
{
  "agent_id": "string",
  "turn_id": "int",
  "d_explore": "float [0,1]",
  "d_correct": "float [0,1]",
  "d_entropy": "float [0,1]",
  "novelty": "float [0,1]",
  "constraint_count": "int",
  "revision_count": "int",
  "confidence": "float [0,1]"
}
```

> The Sidecar Monitor never parses full agent context. It reads only compressed Heartbeat signals, keeping overhead O(n) not O(n·context_length). The `d_correct` field is new in v1.2 (split from the prior undifferentiated `divergence_signal`).

---

## 5. Tribunal Recovery Protocol

Activates when φ > 1.80 for ≥ 2 consecutive turns, OR when the anticipatory trigger fires (§2.3):

1. Amethyst broadcasts `I_t = { mode: Tribunal, TTL: 5 turns }`
2. All agents set α_i = 0.9 (high compliance)
3. DemiJoule fires P-29 `risk_block` on all novel claims
4. P-38 Circuit-Breaker transitions to OPEN
5. Apogee Lens runs contradiction audit (D_correct signal prioritized)
6. CPS_t examined to select recovery bias (Synthesizer vs. Auditor — see §2.7)
7. Recovery Score computed each turn:

```
R_c = r_1·ΔD_entropy + r_2·ΔK + r_3·Δv_φ
```

8. Exit condition: `R_c > R_threshold` AND `φ < 1.60` for 2 consecutive turns
9. Graduated de-escalation: Tribunal → Introspection → Integration → regime-appropriate archetype

> **v1.2 change:** Tribunal threshold updated from 1.70 to 1.80. The 1.70–1.80 band (Introspection / Auditor) now serves as a warning zone that can resolve without full Tribunal activation if a_φ reverses.

---

## 6. Implementation Roadmap

| Version | Target | Description |
|---|---|---|
| v1.0 | ✅ Specified | Full formalism, archetype dispatch, DGAF integration map |
| v1.1 | ✅ Done | P-42 renumber, CROSS_REF sync |
| v1.2 | ✅ This version | Logistic normalization · 7-state regime · CPS §2.7 · D_correct subtype · Heartbeat schema v2 · Tribunal threshold 1.80 |
| v1.3 | 🔴 Next | `ahg_conductor.py` scaffold + `ahg_sidecar.py` + `schemas/ahg_heartbeat.json` implementation |
| v1.4 | 🔴 Planned | CPS_t logging wired to P-01 Herald sink |
| v2.0 | 🔴 Roadmap | MPHG: `u_t = argmax Σ_{k=0}^{H} J(x_{t+k})` (Model Predictive Harmonic Governance) — CPS_t required |

---

## 7. Implementation Status Summary

| Component | File | Status |
|---|---|---|
| AHG full spec | `docs/theory/AHG_ARCHITECTURE.md` | ✅ v1.2 this file |
| Stability analysis companion | `docs/theory/AHG_STABILITY_ANALYSIS.md` | ✅ Filed 2026-06-29 |
| Pattern card | `patterns/P-42_AHG.md` | ✅ Updated v1.2 |
| Conductor implementation | `components/ahg_conductor.py` | 🔴 v1.3 |
| Sidecar Monitor | `components/ahg_sidecar.py` | 🔴 v1.3 |
| Heartbeat schema | `schemas/ahg_heartbeat.json` | 🔴 v1.3 |
| CPS logging | `components/ahg_sidecar.py` | 🔴 v1.4 |
| Test suite | `tests/test_ahg_conductor.py` | 🔴 v1.3 |
| Hallucination eval baseline | `tests/dgaf_eval_suite.py` (Issue #32) | 🟡 Baseline registered: 20–40% reduction target |
| MPHG optimizer | `components/ahg_mphg.py` | 🔴 v2.0 |

---

## 8. Evaluation Targets (Issue #32 Integration)

The AHG_STABILITY_ANALYSIS companion document establishes the following falsifiable performance claims for validation against the Nemotron eval suite:

| Metric | Predicted Improvement | Measurement Method |
|---|---|---|
| Hallucination persistence | 20–40% reduction in contradiction carry-over across turns | `audit_hallucination_rate` in `dgaf_eval_suite.py` |
| Entropy recovery rate | Measurable reduction in turns-to-stability after D_entropy spike | New metric: `entropy_recovery_turns` |
| Contradiction persistence | 20–40% reduction (correlated with hallucination metric) | `contraction_proof_fidelity` |
| Redundant revision loops | Reduction via anticipatory governance | `revision_loop_count` per session |

> These targets are **predictions, not guarantees**. They are registered here as falsifiable baselines for Issue #32 eval design. See `docs/theory/AHG_STABILITY_ANALYSIS.md` §V for the full performance expectation derivation.

---

*AHG Architecture Specification v1.2 · P-42 · 2026-06-29*
*Amethyst × COLLEEN · Post-S077 autonomous sprint*
