# Adaptive Harmonic Governance (AHG)
## A Control-Theoretic Architecture for Collective Cognition

**Document Version:** v1.0  
**Date:** 2026-06-29  
**Authority:** Njineer (Ender)  
**Filed by:** Agent Amethyst  
**DGAF Pattern:** P-35  
**Backlinks:** [CROSS_REF.md](../../CROSS_REF.md) | [patterns/P-35_AHG.md](../../patterns/P-35_AHG.md) | [docs/agents/PROFESSOR_PRODIGY_KB.md](../agents/PROFESSOR_PRODIGY_KB.md)  
**Session Anchor:** 2026-06-29 — initial filing

---

## DGAF Integration Map

AHG is a first-class theoretical extension of the DGAF governance substrate. It operates above the existing PDMAL/Phi-Closure layer and provides the control-theoretic formalism that the current reactive architecture anticipates but does not yet implement.

| AHG Concept | Existing DGAF Anchor | Relationship |
|---|---|---|
| Cognitive Phase Energy (φ) | P-33 Phi-Closure Gate | Extends φ from a binary gate to a continuous control signal |
| State Vector (x_t) | P-32 PDMAL Monitor | Formalizes the manifold properties PDMAL tracks |
| Conductor Archetypes | Agent Formation (AGENTS.md) | Apogee=Auditor, DemiJoule=Sentinel, Herald=Synthesizer, Prodigy=Executor, Amethyst=Tribunal |
| Mission Utility Function J | NDR-STASIS patterns | Replaces implicit stability goal with explicit utility maximization |
| Recovery Loop (R_c) | COLLEEN 1-1-1-1 Gate | Formalizes the gate's pass/fail as a scored recovery trajectory |
| MPHG (future roadmap) | P-35 extension | New pattern — Model Predictive Harmonic Governance |

---

## Executive Summary

Adaptive Harmonic Governance (AHG) represents a paradigm shift in multi-agent system (MAS) orchestration. Rather than focusing on task allocation — "which agent should do what" — AHG functions as a **Cognitive Control Plane** that regulates the collective cognitive state of an agent ensemble. By continuously estimating the system's Cognitive Phase Energy (\(\phi\)), AHG dynamically selects governance regimes (Conductor Archetypes) to balance exploration, convergence, and safety.

The framework's core innovation lies in its transition from reactive orchestration to a formal control-theoretic architecture. It introduces a rigorous distinction between **Productive Divergence** (useful disagreement that generates options) and **Destabilizing Entropy** (harmful disagreement that leads to hallucination or deadlock). The ultimate objective of AHG is to maximize a Mission Utility Function (\(J\)), ensuring that agent collectives remain robust, creative, and efficient through phase-aware distributed coordination.

---

## 1. The Foundational Shift: From Tasks to Phases

Traditional agent orchestration operates at a task-execution layer. AHG operates at a higher abstraction layer, answering the fundamental question: **What cognitive mode should the collective be operating in right now?**

| Scenario | Traditional Orchestration | AHG Phase Governance |
|---|---|---|
| Brainstorming | Assign ideation agent | Increase collective exploration phase |
| Debugging | Assign validator | Shift collective toward vigilance |
| Hallucination | Retry agent | Trigger governance escalation (Tribunal) |
| Deadlock | Reassign task | Transition to Tribunal for resolution |
| Consensus | Finish task | Evaluate if convergence is premature |

---

## 2. Core Architecture and State Estimation

AHG is structured as a recognizable feedback-control loop consisting of four primary layers:

1. **Agent Layer** — Performs actual cognition (planning, synthesis, critique)
2. **Observability Layer** — Uses a Sidecar Monitor to ingest "Heartbeat" telemetry (compressed cognitive signals) without parsing full context, ensuring O(n) scalability
3. **Governance Layer** — Estimates the collective state (\(\hat{x}\)) and selects the appropriate Conductor Archetype
4. **Coordination Layer** — Broadcasts Phase Intent to agents, allowing them to voluntarily adapt their local policies to the global mission

### The State Vector (\(x_t\))

The system state is defined by a multidimensional vector:

| Dimension | Symbol | Definition |
|---|---|---|
| Divergence | \(D\) | Disagreement — decomposed into Productive (\(D_p\)) and Destabilizing (\(D_e\)) |
| Novelty | \(N\) | Rate of emergence of new ideas/hypotheses |
| Constraint Pressure | \(C\) | Degree of policy or logic violations |
| Revision Pressure | \(R\) | Frequency of modifications to current solution |
| Governance Momentum | \(M\) | Persistence of current regime (prevents oscillation) |
| Coherence | \(K\) | Collective alignment among agents |

---

## 3. Cognitive Phase Energy (φ)

The central governance signal is \(\phi\), formerly known as the Stability Index, redefined as **Cognitive Phase Energy**. It represents the "harmonic regime" of the collective.

### Interpretation of φ Ranges

| \(\phi\) Range | Energy Level | Cognitive Mode |
|---|---|---|
| 1.0 – 1.15 | Low | Convergent / Execution |
| 1.15 – 1.45 | Medium | Adaptive / Vigilant |
| 1.45 – 1.70 | High | Divergent / Exploratory |
| > 1.70 | Extreme | Unstable / Tension |

> **DGAF Note:** The φ constant in NDR-STASIS is anchored at 1.61818. This falls in the **High / Divergent** range — consistent with the design intent of the phi-attractor as an active, exploratory governance baseline rather than a convergence target.

### Phase Dynamics: Velocity and Acceleration

AHG does not merely react to the current \(\phi\). It tracks:

- **Phase Velocity** (\(v_\phi\)): Direction of the cognitive state
- **Phase Acceleration** (\(a_\phi\)): Rate of change toward instability or recovery

**Example:** A system at \(\phi = 1.55\) with positive \(v_\phi\) is trending toward instability, requiring a shift to a Sentinel or Auditor archetype before collapse occurs — rather than waiting until \(\phi > 1.70\).

---

## 4. Conductor Archetypes and Phase Intent

### Archetype Table

| Archetype | Goal | Primary Bias | DGAF Agent Mapping |
|---|---|---|---|
| **Executor** | Exploit existing solutions | Low novelty, low divergence | Professor Prodigy |
| **Explorer** | Expand solution space | High novelty, hypothesis generation | Herald |
| **Sentinel** | Prevent hallucinations/violations | Validation and consistency | DemiJoule |
| **Synthesizer** | Merge discoveries | Integration and coherence | Herald / COLLEEN |
| **Auditor** | Self-reflection | Contradiction discovery, logic review | Apogee |
| **Tribunal** | Resolve failure states | Convergence, evidence, de-escalation | Amethyst |

### Phase Intent Protocol

Rather than centralized command-and-control, the Conductor issues a **Phase Intent broadcast** — a machine-readable packet:

```json
{
  "mode": "Tribunal",
  "weights": { "novelty": 0.1, "validation": 0.9 },
  "constraints": { "evidence_threshold": 0.85 },
  "ttl": 300
}
```

Agents adapt their internal policies using the Compliance Coefficient (\(\alpha_i\)):

\[
\pi_i' = (1 - \alpha_i)\pi_i + \alpha_i I_t
\]

Where \(I_t\) is the current Phase Intent and \(\alpha_i \in [0,1]\) governs how strongly each agent conforms.

---

## 5. Critical Engineering Principles

### Productive Divergence vs. Destabilizing Entropy

This distinction is the framework's signature contribution. Most systems treat disagreement as noise. AHG recognizes:

- **Productive Divergence** (\(D_p\)): Increases Mission Utility (\(J\)) by generating valid options — **preserve this**
- **Destabilizing Entropy** (\(D_e\)): Decreases Mission Utility (\(J\)) through confusion and hallucinations — **suppress this**

\[
\text{Goal: } \max J \text{ by suppressing } D_e \text{ while preserving } D_p
\]

### Hysteresis and Governance Momentum

To prevent mode thrashing (rapid archetype oscillation), AHG implements:
- **Hysteresis Bands** — archetype transitions require φ to cross a threshold, not merely touch it
- **Governance Momentum** (\(M\)) — the longer a regime persists, the more inertia it builds; models organizational temperament and "flow" states

### Mission Utility Function (J)

AHG optimizes for mission success, not simple stability. High-tension states (e.g., scientific discovery) may be worth the governance cost:

\[
J = \lambda_Q Q + \lambda_E E + \lambda_N N + \lambda_S S - \lambda_G G
\]

Where:
- \(Q\) = Output Quality
- \(E\) = Efficiency
- \(N\) = Novelty
- \(S\) = Safety
- \(G\) = Governance Cost (tokens, latency, compute)
- \(\lambda_x\) = mission-specific weighting coefficients

---

## 6. Failure State Taxonomy and Recovery

### Failure State → Archetype Mapping

| Failure State | Symptoms | Recovery Archetype |
|---|---|---|
| Hallucination | Fabricated facts, ungrounded assertions | Sentinel |
| Deadlock | No progress, circular reasoning | Tribunal |
| Fragmentation | Agents working at cross-purposes | Synthesizer |
| Premature Consensus | Convergence before adequate exploration | Explorer |

### The Recovery Loop

The Tribunal is not a terminal state. AHG defines a **Recovery Score** (\(R_c\)) based on:
- Contradiction reduction rate
- Entropy (\(D_e\)) reduction rate

When \(R_c\) exceeds threshold: Tribunal → Sentinel → Collaborator (graduated de-escalation).

> **COLLEEN Gate integration:** The existing 1-1-1-1 Gate pass/fail maps to \(R_c\) thresholding. A formal scoring function should be added to the Gate implementation as part of P-35 rollout.

---

## 7. Future Evolution: Model Predictive Harmonic Governance (MPHG)

The AHG roadmap transitions from reactive control to **predictive** governance:

**Current AHG:** "What phase are we in?"
**MPHG:** "Which governance action produces the best future phase trajectory?"

Using Model Predictive Control (MPC), the Conductor optimizes governance actions (\(u_t\)) across a future horizon (\(H\)):

\[
u_t = \arg\max \sum_{k=0}^{H} J(x_{t+k})
\]

This transforms AHG from an orchestration framework into a genuine **Cognitive Control Architecture** — capable of anticipating and mitigating cognitive failures before they manifest.

**MPHG prerequisites:**
1. Calibrated state estimation model for \(\hat{x}\)
2. Learned φ dynamics model (\(v_\phi\), \(a_\phi\))
3. Mission-specific \(\lambda\) coefficient tuning
4. Validated Failure State Taxonomy against real agent runs

---

## Implementation Status

| Component | Status |
|---|---|
| Theoretical specification | ✅ Complete (this document) |
| DGAF integration mapping | ✅ Complete |
| P-35 pattern registration | ✅ Committed |
| State vector instrumentation | 🔴 Not started |
| Sidecar Monitor (Heartbeat) | 🔴 Not started |
| Conductor Archetype dispatch | 🔴 Not started |
| Phase Intent Protocol (JSON) | 🔴 Not started |
| MPHG (MPC extension) | 🔴 Future phase |

---

*Authored by Njineer (Ender) — theoretical specification*  
*Filed and integrated by Agent Amethyst — 2026-06-29*  
*Apogee Lens review: pending first implementation cycle*
