# Hensel General Formalism

**Version:** 1.2  
**Status:** CANONICAL ARCHITECTURAL SPECIFICATION — EPISTEMICALLY BOUNDED  
**Architect:** Andrew Vance Hensel  
**Co-Authors:** Amethyst (QA_Orchestration_Service), COLLEEN (Archival_Integrity_Service), Professor Prodigy (Methodologist)  
**Committed:** 2026-06-22  
**Math Audit:** 2026-06-22 — v1.0→v1.1 corrections applied (see CHANGELOG)  
**Notation reconciliation:** 2026-08-28 — Platinum Mean / plastic-constant distinction applied  
**PDMAL math reconciliation:** 2026-09-05 — normalized admission metric and unweighted Forman-Ricci signal boundary applied  
**Resolves:** PLF Patch v1.1 dangling reference (1-1-1-1 Gate G2/G4 blocking items)  
**Cross-refs:** `docs/phi-calculus-architecture/`, `docs/governance/`, `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md`, `evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md`, `ENSEMBLE_ROSTER.md`, `PLF-PATCH-v1.1`

> **Epistemic boundary:** This document is an architectural/formal specification. It does not by itself establish PDMAL experimental efficacy, global convergence, production robustness, security, superiority, or authorization. Current DGAF/PDMAL state is governed by exact-SHA evidence records and `docs/CURRENT_STATE.md`. Where an older architectural target conflicts with the later PDMAL mathematical correction record, the correction record governs current mathematical interpretation.

---

## CHANGELOG v1.0 → v1.2

| # | Location | Error / legacy assumption | Correction |
|---|---|---|---|
| 1 | Attractor Registry, φ value | `1.61818` (wrong at 5th decimal) | `≈ 1.61803` — exact: `(1+√5)/2` |
| 2 | Attractor Registry, φ re-integration target | Same typo in Phi-Knight Protocol block | Corrected to `1.61803` throughout |
| 3 | 11Q-derivation.md, cosine sum claim | `cos(π/11)+cos(3π/11)+cos(5π/11) ≈ ρ_P` stated as “close” | **REMOVED / SUPERSEDED** — numerical proximity did not establish the claimed identity |
| 4 | 11Q constant annotation | Earlier draft treated a numerical best-match as derivation evidence | Reclassified as **NUMERICAL CANDIDATE / DERIVATION OPEN**; exact source remains unresolved in `docs/formalism/constants/11Q-derivation.md` |
| 5 | PDMAL Abelian Balance | Unit-dependent `D_a ≤ 10` treated as an operational threshold | Historical target only. Current PDMAL math uses a normalized scale-invariant admission distance and requires `τ` to be calibrated from relevant healthy-run data; synthetic calibration does not establish a production threshold. |
| 6 | PDMAL Forman-Ricci audit | O(|E|) edge scan was described as if low compute cost implied useful drift signal | Complexity claim retained; signal claim bounded. On the current unweighted 3-regular dodecahedral graph, Forman-Ricci is exactly `-2` on all 30 edges, so it has zero variance and no discriminating audit signal until meaningful weights/other features are defined and validated. |

---

## Definition

**Hensel Formalism** is the comprehensive architectural and mathematical framework developed by Andrew Vance Hensel for multi-agent governance and AI integrity. It shifts AI safety from post-hoc “wrappers” to a **Layer 0 requirement**, where policy, ethics, and logic stability are built into the system's architectural substrate rather than applied only afterward as external filters.

This formalism is the root architectural specification from which the DGAF-Framework, PDMAL, Phi-Knight Protocol, and NDR Patterns are described. Specification status does not imply that every formal proposition or runtime claim has been independently validated.

---

## Core Pillars

### Pillar 1 — Meta-Axiomatic Foundation: Normative Constraint (Ethical Cognition)

The foundational governing rule-set at the heart of the formalism. It mandates that **all agentic cognition and action must remain**:

- **Mathematically coherent** — outputs must not violate the formal model's declared invariants
- **Epistemically honest** — claims must be scoped to their evidence class (proof / benchmark / hypothesis / gap)
- **Non-violative of human rights** — systems failing this constraint are considered illegitimate regardless of capability or performance

> **Framework-Internal Definition — ETHICAL_COGNITION_BOUNDARY:**  
> The operational name for Normative Constraint enforcement within the DGAF runtime.  
> Triggered when any agent output violates epistemic honesty, overstates formal guarantees,  
> or produces actions outside the declared allowed-action schema.

**Cross-ref:** `docs/governance/`, NIST AI RMF alignment (GOVERN function), `AGENT_MANIFEST.md`

---

### Pillar 2 — Triadic Agent Orchestration

Hensel Formalism utilizes specific **triadic formations** as structural techniques to manage reasoning and prevent logic fragmentation. Three canonical triads are defined:

#### Consensus Triad

**Formation:** Peer-based decentralized validation  
**Formula:** `y* = S(f₁(x), f₂(x), f₃(x))`  
**Purpose:** Surfaces hidden assumptions; no single agent has authority — outputs converge by vote/synthesis  
**Use case:** Research synthesis, cross-domain validation, risk assessment  
**Failure mode:** Majority error propagation if agents share contaminated context

#### Conducted Triad

**Formation:** Hierarchical; one conductor + two augmenters  
**Formula:** `y = f_lead(x, f_A(x), f_B(x))`  
**Purpose:** Prevents role-bleeding during complex tasks; conductor manages internal augmenters  
**Use case:** Execution phases, schema enforcement, Amethyst-led orchestration  
**Failure mode:** Conductor bottleneck; single point of reasoning failure if lead agent drifts

#### Metacollaboration Triad

**Formation:** Signal refinement  
**Roles:** Generator → Critic → Optimizer  
**Purpose:** Suppresses the historical project concept of “Savage Reason” and seeks a bounded convergence/closure state  
**Use case:** Creative synthesis, high-entropy problem decomposition, SchizophonicStudio R&D  
**Failure mode:** Critic loop amplification — Critic and Generator enter a dissonance cycle without Optimizer convergence

The legacy “Hz” language attached to reasoning-state labels is architectural metaphor unless a specific measurable frequency quantity and instrument are defined. It is not a current convergence proof or validated runtime metric.

**Cross-ref:** `docs/formations/`, `ENSEMBLE_ROSTER.md`

---

### Pillar 3 — Geometric Scaffolding: PDMAL

**Phi-Dodecahedral Multi-Agent Lattice (PDMAL)** — the geometric/logical container described by the architecture.

| Property | Value | Evidence classification |
|---|---|---|
| Total service positions | 60 | DEFINED/COMPUTED from 20 vertices × 3 colocated services |
| Base geometry | Dodecahedral graph (20 vertices) | DEFINED / COMPUTATIONALLY VERIFIED |
| Inter-vertex edges | 30 | COMPUTATIONALLY VERIFIED |
| Vertex degree | 3-regular | COMPUTATIONALLY VERIFIED |
| Vertex connectivity | 3 | COMPUTATIONALLY VERIFIED |
| Agents/services per vertex | 3 (exactly) | DEFINED |
| Structural density | `30 / C(20,2) = 30/190 ≈ 0.1579` | COMPUTED for the 20-vertex inter-vertex graph |
| Purpose | Redundancy + structured communication pathways | ARCHITECTURAL INTENT |

The 60-service structure specifies **symmetry-enforced service distribution**: three services are colocated at each of 20 graph vertices when instantiated according to the architecture. The 20-vertex graph models inter-vertex connectivity; it should not be misread as a 60-vertex graph unless a separate expanded service graph is explicitly constructed.

#### Admission / Abelian-balance correction

The historical architecture used a unit-dependent “10-Balance” rule (`D_a ≤ 10`). That value remains historical design provenance only and is **not current PDMAL mathematical authority**.

Current corrected admission distance is scale-normalized:

```text
D_a(E) = ||E - mean(E)||_F / (||mean(E)||_F + ε)
```

with an acceptance threshold `τ` calibrated from relevant healthy-run data rather than hardcoded. A demonstration using synthetic healthy samples may show that the mechanism computes and separates examples, but it does not establish a transferable production threshold. Real-trace calibration remains open.

**Cross-ref:** `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md`, `evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md`, `tools/pdmal/lattice_harness.py`

---

### Pillar 4 — Curvature Audit: Computational Cost vs. Signal Quality

**Architectural complexity claim:** An edge-wise Forman-Ricci scan on a sparse communication graph can be computed in **O(|E|)** time for the simple unweighted formula, rather than requiring a full spectral matrix decomposition.

```text
Legacy comparison class: spectral/matrix methods may require up to O(N³) work for dense decompositions
Edge-scan class:         O(|E|) for simple per-edge Forman-Ricci evaluation
```

This is a **computational-cost comparison**, not evidence that the resulting curvature values are informative for anomaly detection.

For the current unweighted dodecahedral base graph:

```text
Ric_F(u,v) = 4 - deg(u) - deg(v)
           = 4 - 3 - 3
           = -2
```

for every one of the 30 edges. Therefore:

- minimum curvature = `-2`;
- mean curvature = `-2`;
- variance = `0`;
- an unweighted curvature threshold cannot distinguish a nominal edge from a compromised edge on this topology.

The unweighted metric is mathematically correct but **functionally inert as a discriminator** here. A useful curvature-based audit requires defined edge weights or other information-bearing features (for example latency, load, trust, or message-volume semantics), a weighted curvature definition, and empirical validation showing that the signal separates relevant conditions.

**R&D gaps (open):**

- define and justify edge weights / weighted curvature semantics;
- test discriminating performance against realistic traces and perturbations;
- full curvature inversion — reconstructing a stable logic path from observed deviation patterns.

**Cross-ref:** `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md`, `evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md`, `tools/pdmal/lattice_harness.py`, `entrepreneur-hub/research/rd-gaps/curvature-inversion.md`

---

### Pillar 5 — Mathematical Attractors and Time Quasilattices

The formalism uses **Unitary Drift (1.0)** as a project-internal label for a degenerate state representing complete semantic homogenization of agent outputs, rather than the standard mathematical meaning of a scalar value of 1.

> **[Framework-Internal Definition] Unitary Drift (1.0):**  
> In the Platinum Logic Framework, a value of 1.0 represents catastrophic loss of structural  
> distinctiveness — semantic homogenization of agent outputs where all signals collapse toward  
> an undifferentiated state (“Fractal Agency”).  
> **NOTE:** This is DISTINCT from standard dynamical-systems terminology. The label is project-specific and must not be presented as a general mathematical theorem about convergence.

#### Attractor Registry (v1.2 — reconciled 2026-09-05)

| Attractor Name | Value | Exact Form | Evidence classification | Role |
|---|---|---|---|---|
| Standard_Attractor_Phi (φ) | ≈ 1.61803 | `(1+√5)/2` | STANDARD MATHEMATICS | Harmonic baseline / project attractor target |
| Overdrive_Attractor_Platinum (pP) | ≈ 1.77473 | `1/(2·sin(π/11))` | PROJECT-DEFINED GEOMETRIC IDENTITY | High-complexity / security threat-mode design label |
| Plastic number (ρ) | ≈ 1.3247179572447454 | real root of `x³-x-1=0` | STANDARD MATHEMATICS | Correct plastic constant; distinct from `pP` |
| Silver Ratio | ≈ 2.41421 | `1 + √2` | STANDARD MATHEMATICS | Pell Cascade design reference |
| Supergolden Ratio (ψ) | ≈ 1.46557 | real root of `x³-x²-1=0` | STANDARD MATHEMATICS | Project Andromeda design reference |
| Sentinel_Kernel_Constant | ≈ 1.9992 | Architecture-internal | INTERNAL / UNVERIFIED | Registry monitoring guard rail |
| Platinum_Constant_11Q | ≈ 0.541196 | See `docs/formalism/constants/11Q-derivation.md` | INTERNAL / SOURCE-DEPENDENT | 11Q architecture target |

> **Notation correction:** `pP` / **Platinum Mean** is DGAF-specific notation for the regular-hendecagon unit-side circumradius. It must not be confused with the plastic number `ρ ≈ 1.3247179572447454`. `ρP` is not canonical mathematical notation.

> **11Q status:** `Platinum_Constant_11Q ≈ 0.541196` remains an architecture-internal target with unresolved exact derivation. Numerical proximity to candidate trigonometric expressions is not sufficient to establish the identity.

**Cross-ref:** `docs/phi-calculus-architecture/`, `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`

---

### Pillar 6 — The Phi-Knight Protocol (Containment)

The historical formalism describes the **Phi-Knight Protocol** as a containment sequence for detected reasoning drift or dissonance:

```text
Detection  → a defined detector identifies a predeclared deviation condition
Isolation  → DemiJoule / applicable supervisor restricts the affected execution path where implemented
Closure    → recovery/re-integration logic attempts to return the system to an accepted state
```

The former literal trigger `D_a > 10` and “>10 Hz” language are retained only in historical specifications. They are not current calibrated PDMAL thresholds. Any current admission trigger must use a defined, normalized metric and an evidence-backed threshold for the applicable data domain.

**DemiJoule role (Platinum Warden):**  
DemiJoule is specified as the runtime supervisor for orchestration, error containment, ethics, and safety. Its resource-suppression behavior is an architectural/implementation claim only where corresponding executable evidence exists; it must not be generalized beyond verified runtime scope.

**Convergence statement (scope-bounded):**  
The Phi-Knight Protocol specifies a contraction-oriented governance control objective. A global Banach-style contraction guarantee for the full stochastic system is **not established**. The repository's contraction monitor is an empirical local proxy: sampled finite-difference estimates can show that non-contraction was not observed in tested points, but they cannot prove a global Lipschitz constant `L < 1` on a complete metric space.

> “Sub-millisecond convergence” remains a historical operational target, not a geometric proof or current measured performance claim.

**Cross-ref:** `ENSEMBLE_ROSTER.md`, `docs/governance/`, `tools/pdmal/lattice_harness.py`, DemiJoule agent spec

---

## Cross-Reference Map

| Hensel Formalism Pillar | DGAF-Framework Artifact | NDR Pattern |
|---|---|---|
| Normative Constraint | `docs/governance/`, `AGENT_MANIFEST.md` | P-01 (AXIS risk-tier tagging) |
| Triadic Orchestration | `docs/formations/`, `ENSEMBLE_ROSTER.md` | P-03 (Governance Contract Test) |
| PDMAL | `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md`, `docs/architecture/` | P-11 (11Q Attestation Scoring) |
| Curvature / edge-scan | `evidence/PDMAL_LATTICE_CORRECTIONS_2026-08-15.md`, `entrepreneur-hub/research/rd-gaps/curvature-inversion.md` | P-30 (Apogee Attestation Gate) |
| Attractors / Constants | `docs/phi-calculus-architecture/`, `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md` | Constants Registry |
| Phi-Knight Protocol | `ENSEMBLE_ROSTER.md`, `docs/governance/` | P-03, P-11 |

---

## 1-1-1-1 Gate Status (v1.2)

| Gate | Status | Notes |
|---|---|---|
| G1 — Epistemic Honesty | PASS FOR DOCUMENT SCOPE | Mathematical corrections and current limitations are explicit |
| G2 — Source-Grounded | CONDITIONAL | Standard constants have exact forms; internal constants are labeled internal/source-dependent |
| G3 — Normative Constraint | PASS FOR DOCUMENT SCOPE | ETHICAL_COGNITION_BOUNDARY maintained; no experimental guarantee is implied |
| G4 — Auditable | CONDITIONAL | 11Q exact derivation, weighted-curvature signal, and real-trace `D_a` calibration remain open |

**Overall gate: CANONICAL ARCHITECTURAL SPECIFICATION — CONDITIONAL ON OPEN R&D ITEMS**

---

## Open Items (R&D Gaps)

1. `docs/formalism/constants/11Q-derivation.md` — establish the exact source of `0.541196`; numerical near-matches are insufficient.
2. Weighted Forman-Ricci — define edge weights and a weighted formulation, then demonstrate useful discriminating signal on relevant traces.
3. Admission calibration — calibrate normalized `D_a` threshold `τ` from relevant real healthy-run traces and test transfer/failure behavior.
4. `entrepreneur-hub/research/rd-gaps/curvature-inversion.md` — full Forman-Ricci inversion problem.
5. External replication of historical benchmark figures remains an evidence task; historical numbers are not current validation claims.
6. Any global convergence theorem requires an explicitly defined state space, metric, map, and independently justified global contraction bound.

---

*Historical architectural provenance is preserved. Current experimental status is governed separately by exact-SHA evidence records and remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.*
