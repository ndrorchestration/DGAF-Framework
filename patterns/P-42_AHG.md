# P-42 — Adaptive Harmonic Governance (AHG)

> **Pattern ID:** P-42
> **Layer:** 12 — Cognitive Control Plane
> **P-36 Class:** ADVISORY (v1.2) → BLOCKING (v2.0 MPHG target)
> **Status:** 🟡 Specified — Implementation Pending
> **Spec version:** v1.2
> **Registered:** 2026-06-29 · Post-S077 autonomous sprint
> **Steward:** Amethyst × COLLEEN
> **Full spec:** [`docs/theory/AHG_ARCHITECTURE.md`](../docs/theory/AHG_ARCHITECTURE.md)
> **Stability analysis:** [`docs/theory/AHG_STABILITY_ANALYSIS.md`](../docs/theory/AHG_STABILITY_ANALYSIS.md)

> ⚠️ **Renumber note:** Originally filed as P-35 on 2026-06-29. Corrected to P-42 to resolve collision with the pre-existing P-35 Procluding Premise Gate (S069).

---

## Summary

AHG is a control-theoretic governance layer that continuously estimates the **Cognitive Phase Energy (φ)** of the multi-agent collective via logistic normalization of a Stability Index, and dispatches **Conductor Archetypes** to steer the ensemble toward productive divergence and away from destabilizing entropy.

φ is bounded to [1.0, 1.8] by construction. The NDR-STASIS anchor φ = 1.618 falls in the Integration regime — the peak consolidation phase between Explorer-mode divergence and Auditor-mode contradiction resolution.

---

## Core Formalism

### Stability Index

```
S(t) = w_D·D_t + w_N·N_t + w_C·C_t + w_R·R_t
```

### Logistic Normalization (canonical φ computation)

```
φ(t) = 1 + 0.8 · σ(S_adj(t))
S_adj(t) = S(t) − w_M·M_t − w_K·K_t
σ(x) = 1 / (1 + exp(−x))
```

Boundary guarantees: φ ∈ [1.0, 1.8]; midpoint φ = 1.4 at S_adj = 0.

### Divergence Decomposition

```
D_t = w_explore·D_explore + w_correct·D_correct + w_entropy·D_entropy
```

Default subtype weights: w_explore = 0.3, w_correct = 0.4, w_entropy = 1.0

---

## Seven-State Regime Table

| Regime | φ Range | Archetype | Key Signal |
|---|---|---|---|
| Grounded | 1.00 – 1.15 | Executor (Prodigy) | Low divergence, stable |
| Flow | 1.15 – 1.30 | Synthesizer (Herald/COLLEEN) | Moderate novelty |
| Vigilance | 1.30 – 1.45 | Sentinel (DemiJoule) | Constraint pressure rising |
| Expansion | 1.45 – 1.60 | Explorer (Herald) | High D_explore |
| Integration | 1.60 – 1.70 | Explorer → Auditor transition | NDR-STASIS anchor φ=1.618 |
| Introspection | 1.70 – 1.80 | Auditor (Apogee Lens) | D_correct dominant; anticipatory Tribunal watch |
| Tension | > 1.80 | Tribunal (Amethyst) | D_entropy dominant; hard ceiling |

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

## Cognitive Phase Space (§2.7)

Auxiliary 3D context vector logged alongside φ:

```
CPS_t = (Exploration_t, Consensus_t, Confidence_t)
```

Contextualizes *why* φ is at a given value. Enables CPS-aware Tribunal recovery strategies. Required for MPHG v2.0.

---

## Interaction with Existing Patterns

| Pattern | Interaction |
|---|---|
| P-32 Phi-Closure Gate | AHG extends from binary PASS/FAIL to continuous φ ∈ [1.0, 1.8] |
| P-29 Sentinel | Tribunal fires P-29 `risk_block` on φ > 1.80 |
| P-33 PDMAL | Governance Momentum M uses PDMAL Frobenius norm substrate |
| P-38 Circuit-Breaker | AHG Tribunal emits P-38 OPEN on sustained φ > 1.80 |
| P-09 Triumvirate Mandate | Phase Intent I_t is a lightweight mandate variant |
| P-01 Herald Trace | Heartbeat events + CPS_t route through P-01 fan-out |

---

## Performance Claims (Issue #32 Eval Targets)

| Metric | Predicted Improvement |
|---|---|
| Hallucination persistence | 20–40% reduction in contradiction carry-over |
| Entropy recovery rate | Measurable reduction in turns-to-stability after D_entropy spike |
| Redundant revision loops | Reduction via anticipatory governance (a_φ-based pre-emption) |

---

## Implementation Status

| Component | Status |
|---|---|
| `docs/theory/AHG_ARCHITECTURE.md` v1.2 | ✅ Filed |
| `docs/theory/AHG_STABILITY_ANALYSIS.md` | ✅ Filed |
| `ahg_conductor.py` | 🔴 v1.3 |
| `ahg_sidecar.py` | 🔴 v1.3 |
| `schemas/ahg_heartbeat.json` | 🔴 v1.3 |
| MPHG | 🔴 v2.0 |

---

*P-42 · AHG · v1.2 · 2026-06-29 · Amethyst × COLLEEN*
