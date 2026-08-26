# AHG Stability Analysis — Formal Companion to AHG_ARCHITECTURE.md v1.2

> **Epistemic boundary:** This document contains a mathematical/control-theoretic analysis of the AHG model. Algebraic consequences are conditional on the stated definitions, assumptions, and parameterization. They do **not** by themselves establish runtime correctness, deployed-system convergence, safety, production performance, or empirical efficacy. Performance values in Section V are falsifiable hypotheses/predictions, not observed results.
>
> **Document type:** Formal stability analysis and theoretical grounding
> **Companion spec:** [`docs/theory/AHG_ARCHITECTURE.md`](AHG_ARCHITECTURE.md)
> **Pattern:** P-42 — Adaptive Harmonic Governance
> **Authors:** Amethyst × COLLEEN
> **Date:** 2026-06-29
> **Source:** Derived from *"Adaptive Harmonic Governance: A Stability-Guided Framework for Multi-Agent Systems"* (executive summary, 2026-06-29)

---

## I. The Control-Theoretic Shift

The primary architectural claim of AHG is that the Phi (φ) signal is modeled as a **feedback-control variable** rather than a descriptive visualization. This is a model-level architectural interpretation; whether the signal is reliably measurable and whether it produces beneficial behavioral changes are empirical questions.

Under the stated model:

1. **φ is defined as measurable** from the model inputs {D, N, C, R}; this establishes a calculation rule, not proof that the underlying measurements are reliable in deployed systems.
2. **φ is bounded by construction** under the stated logistic normalization; this is an algebraic property of the definition, not evidence of runtime stability.
3. **φ is intended to drive behavior** through the modeled dispatch and intent mechanisms; implementation and observed efficacy require separate evidence.

These are model properties and design requirements, not independent validation claims.

## II. Mathematical Foundations

### II.1 Stability Index Derivation

The Stability Index S(t) is a weighted linear combination of the four primary instability drivers:

```
S(t) = w_D·D_t + w_N·N_t + w_C·C_t + w_R·R_t
```

Each variable is independently measurable at the agent boundary:

| Variable | Measurement Source | Scale |
|---|---|---|
| D_t | Divergence across agent output embeddings (cosine distance) | [0, 1] |
| N_t | TF-IDF or embedding novelty vs. prior-turn corpus | [0, 1] |
| C_t | Constraint violation count / total active constraints | [0, 1] |
| R_t | Revision events per turn / total claims | [0, 1] |

All inputs are normalized to [0, 1], making S(t) a bounded linear combination. With default weights summing to 0.80, S(t) ∈ [0, 0.80] under the stated model assumptions.

### II.2 Logistic Normalization Properties

The canonical φ computation:

```
φ(t) = 1 + 0.8 · σ(S_adj(t))     where σ(x) = 1/(1 + exp(−x))
```

Key analytic properties:

| Property | Value / Behavior |
|---|---|
| Domain | S_adj ∈ (−∞, +∞) |
| Range | φ ∈ (1.0, 1.8) — open interval; boundaries are asymptotes |
| Monotonicity | Strictly increasing: dφ/dS_adj > 0 for all S_adj |
| Midpoint | φ(0) = 1 + 0.8·0.5 = 1.40 |
| Sensitivity | Maximum at midpoint S_adj = 0; tails compress extreme inputs |
| Fibonacci intersection | φ(t) = 1.618 ⟺ σ(S_adj) = 0.7725 ⟺ S_adj ≈ 1.237 |

The Fibonacci intersection point S_adj ≈ 1.237 is a **derived model value** under this normalization. It identifies the φ value at which the model's regime map intersects the 1.618 anchor; it does not establish that a deployed collective has entered a scientifically validated "Integration" state.

### II.3 Divergence Decomposition — Formal Specification

The composite divergence term is:

```
D_t = w_explore·D_explore_t + w_correct·D_correct_t + w_entropy·D_entropy_t
```

With default weights: w_explore = 0.30, w_correct = 0.40, w_entropy = 1.00.

**Subtype classification decision boundary:**

Let e_i be the embedding of agent i's output at turn t, and H be the set of prior-established facts.

- **D_entropy:** Classification fires if e_i contradicts a claim in H that has P-11 attestation score ≥ 0.85, OR if e_i is detected as a repetition loop (cosine similarity ≥ 0.95 to a turn within the last 5 turns where the claim was already contested).
- **D_correct:** Classification fires if e_i contradicts a claim in H AND the agent provides an evidence reference or logical argument (Apogee Lens dissent signal present).
- **D_explore:** Default classification for all divergence not classified as D_entropy or D_correct.

This forms an exhaustive, mutually exclusive partition under the stated classification rules: D_t = D_explore + D_correct + D_entropy (normalized).

### II.4 Phase Velocity and Acceleration — Stability Conditions

```
v_φ(t) = φ(t) − φ(t−1)          (first finite difference)
a_φ(t) = v_φ(t) − v_φ(t−1)      (second finite difference)
```

**Model stability condition:** Under the stated discrete-time model, a state is classified as stable when:

```
|v_φ(t)| < θ_v   AND   |a_φ(t)| < θ_a
```

For the anticipatory Tribunal trigger:

```
a_φ(t) > θ_a  AND  φ(t) > φ_warn (= 1.70)  ⟹  pre_empt_tribunal()
```

This is structurally analogous to bang-bang control on the modeled governance mode. It describes the control rule; it does not establish that a deployed system will satisfy the stability condition or that the trigger improves outcomes.

### II.5 Hysteresis as Institutional Memory

The hysteresis band (≥ 2 consecutive turns in a new regime before transition fires) is mathematically analogous to a dead-band controller. This is a model interpretation intended to reduce oscillation at regime boundaries; whether it does so in observed workloads is empirical.

The Governance Momentum term M_t is:

```
M_t = β·M_{t−1} + (1−β)·Archetype_weight_t
```

where β ∈ [0, 1] is the EMA decay factor (default β = 0.8). M_t enters S_adj as a suppressor in the model. The resulting "inertia" interpretation is a modeling consequence, not a demonstrated runtime property.

---

## III. Architectural Refinements — Formal Properties

### III.1 Sidecar Monitor — Complexity Analysis

| Architecture | Per-turn Computation | Bottleneck Risk |
|---|---|---|
| Centralized Conductor (naive) | O(n · context_length) | High — Conductor parses all agent outputs |
| Sidecar Monitor (AHG) | O(n · heartbeat_size) | None in the stated fixed-heartbeat model |

Since heartbeat_size is a fixed-size vector (8 scalar fields in v1.2 schema), the **modelled** Sidecar Monitor complexity is O(n) under the stated architecture assumptions. Implementation profiling is still required before making a production performance claim.

### III.2 Phase Intent as Distributed Coordination

The Phase Intent update rule:

```
π_i' = (1 − α_i)·π_i + α_i·I_t
```

is formally a convex combination when π_i and I_t lie in a convex admissible policy space. Under that assumption:

1. **Boundedness:** π_i' remains inside the convex hull of valid policies.
2. **Autonomy preservation:** At α_i = 0, the model leaves π_i unchanged. Higher α values imply stronger conformity in the modeled update rule.
3. **Asymptotic alignment:** If I_t is held constant and 0 < α_i ≤ 1, the recurrence approaches I_t at rate (1−α_i)^T. With α_i = 0.9 and T = 5, the residual coefficient is 10^-5.

These are recurrence properties under the stated assumptions. They are not evidence that an LLM collective will converge to, or beneficially follow, the modeled intent in deployment.

---

## IV. The 3D Cognitive Phase Space — Formal Specification

The Cognitive Phase Space provides a richer **modelled state description** than φ alone:

```
CPS_t = (E_t, C_t_consensus, F_t)
```

Where:

- **E_t** (Exploration): `E_t = w_EN·N_t + w_ED·D_explore_t` — normalized to [0,1]
- **C_t_consensus** (Consensus): `C_t_consensus = 1 − (D_t / D_max)` — normalized to [0,1]
- **F_t** (Confidence): `F_t = 1 − (w_FR·R_t + w_FC·C_t)` — normalized to [0,1]

**CPS trajectory interpretation:**

The collective's path through CPS is a trajectory in the model's coordinate representation. The following are proposed recovery mappings, not empirically optimal policies:

| Entry Path | CPS Trajectory | Proposed Recovery Archetype |
|---|---|---|
| Exploratory overload | E↑, C↓, F↓ → high φ | Synthesizer — integrate excess hypotheses |
| Adversarial conflict | E↓, C↓, F↑ → high φ | Auditor — adjudicate confident contradictions |

This CPS-conditional recovery selection is proposed as a v1.4 design direction. It requires implementation and controlled evaluation before any claim of optimality or improved recovery can be made.

---

## V. Performance Claims — Derivation and Falsifiability

### V.1 Hallucination Reduction — Hypothesis (20–40% prediction)

**Mechanism hypothesis:** AHG proposes two modelled failure pathways:

1. **D_entropy persistence** — a hallucinated claim is not corrected in subsequent turns.
2. **Anticipatory governance failure** — the system reaches Tension without triggering correction.

The proposed response is to weight D_entropy in S(t) and use a_φ pre-emption.

**Predicted magnitude:** 20–40% reduction in `audit_hallucination_rate`.

This is a **prediction to be tested**, not an observed result.

**Falsifiability conditions:**

- Null hypothesis: AHG produces no statistically significant change in `audit_hallucination_rate` vs. ungoverned baseline.
- Test design: 50-turn triadic traces with and without AHG active; measure D_entropy carry-over across turn boundaries.
- Significance threshold: p < 0.05, effect size ≥ 0.20 reduction.

### V.2 Efficiency — Hypothesis

**Metric:** `entropy_recovery_turns` — turns from first D_entropy spike to φ < 1.45 (Vigilance exit).

**Prediction:** AHG may reduce `entropy_recovery_turns` by ≥ 2 turns on average compared to reactive-only governance. This requires controlled execution and comparison against the stated baseline.

### V.3 Reliability — Hypothesis

**Mechanism hypothesis:** The modeled Governance Momentum term may reduce the probability of secondary revision cascades.

**Prediction:** `revision_loop_count` per session may decrease by ≥ 15% vs. baseline. This is unverified until a controlled comparison is executed.

---

## VI. NDR-STASIS Anchor — Formal Alignment

The NDR-STASIS design value φ = 1.618033... is the Fibonacci-derived stability anchor used in this model. Within the logistic normalization:

```
φ = 1.618  ⟺  σ(S_adj) = 0.7725  ⟺  S_adj = ln(0.7725 / 0.2275) ≈ 1.2366
```

This is a **derived mathematical correspondence inside the model**. It should not be read as evidence that 1.618 is an empirically optimal operating point.

**Model interpretation:** At φ = 1.618, the configured regime table places the state within the Integration interval. This is a regime-map definition, not an empirical observation.

The further observation that distances to adjacent configured boundaries numerically relate to Fibonacci quantities is descriptive mathematics of the chosen constants. It does not establish causal significance, optimality, or a natural-law property.

---

## VII. Open Questions for MPHG (v2.0)

| Question | Relevance |
|---|---|
| What is the optimal prediction horizon H for the MPHG objective? | Determines lookahead depth: `u_t = argmax Σ_{k=0}^{H} J(x_{t+k})` |
| How should λ weights in J be tuned per task domain? | Scientific discovery vs. execution tasks require different λ_N vs. λ_Q balance |
| Can CPS trajectory prediction replace reactive φ monitoring? | Requires empirical comparison with reactive monitoring |
| What is the empirical dead-band width for β in M_t? | Requires controlled characterization |

---

*AHG Stability Analysis · P-42 Companion · 2026-06-29*
*Amethyst × COLLEEN · Post-S077 autonomous sprint*
*Derived from: "Adaptive Harmonic Governance: A Stability-Guided Framework for Multi-Agent Systems" (historical research source)*
