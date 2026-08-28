# Hensel General Formalism

**Version:** 1.1  
**Status:** CANONICAL ARCHITECTURAL SPECIFICATION — EPISTEMICALLY BOUNDED  
**Architect:** Andrew Vance Hensel  
**Co-Authors:** Amethyst (QA_Orchestration_Service), COLLEEN (Archival_Integrity_Service), Professor Prodigy (Methodologist)  
**Committed:** 2026-06-22  
**Math Audit:** 2026-06-22 — v1.0→v1.1 corrections applied (see CHANGELOG)  
**Notation reconciliation:** 2026-08-28 — Platinum Mean / plastic-constant distinction applied  
**Resolves:** PLF Patch v1.1 dangling reference (1-1-1-1 Gate G2/G4 blocking items)  
**Cross-refs:** `docs/phi-calculus-architecture/`, `docs/governance/`, `ENSEMBLE_ROSTER.md`, `PLF-PATCH-v1.1`

> **Epistemic boundary:** This document is an architectural/formal specification. It does not by itself establish PDMAL experimental efficacy, global convergence, production robustness, security, superiority, or authorization. Current DGAF/PDMAL state is governed by exact-SHA evidence records and `docs/CURRENT_STATE.md`.

---

## CHANGELOG v1.0 → v1.1

| # | Location | Error | Correction |
|---|---|---|---|
| 1 | Attractor Registry, φ value | `1.61818` (wrong at 5th decimal) | `≈ 1.61803` — exact: `(1+√5)/2` |
| 2 | Attractor Registry, φ re-integration target | Same typo in Phi-Knight Protocol block | Corrected to `1.61803` throughout |
| 3 | 11Q-derivation.md, cosine sum claim | `cos(π/11)+cos(3π/11)+cos(5π/11) ≈ ρ_P` stated as "close" | **REMOVED / SUPERSEDED** — numerical proximity did not establish the claimed identity |
| 4 | 11Q constant annotation | Earlier draft treated a numerical best-match as derivation evidence | Reclassified as **NUMERICAL CANDIDATE / DERIVATION OPEN**; exact source remains unresolved in `docs/formalism/constants/11Q-derivation.md` |

---

## Definition

**Hensel Formalism** is the comprehensive architectural and mathematical framework developed by Andrew Vance Hensel for multi-agent governance and AI integrity. It shifts AI safety from post-hoc "wrappers" to a **Layer 0 requirement**, where policy, ethics, and logic stability are baked directly into the system's geometric and mathematical substrate — not applied afterward as external filters.

This formalism is the root architectural specification from which the DGAF-Framework, PDMAL, Phi-Knight Protocol, and NDR Patterns are described. The specification status does not imply that every formal proposition or runtime claim has been independently validated.

---

## Core Pillars

### Pillar 1 — Meta-Axiomatic Foundation: Normative Constraint (Ethical Cognition)

The foundational governing rule-set at the heart of the formalism. It mandates that **all agentic cognition and action must remain**:

- **Mathematically coherent** — outputs must not violate the formal model's invariants
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
**Purpose:** Prevents "role-bleeding" during complex tasks; conductor manages internal augmenters  
**Use case:** Execution phases, schema enforcement, Amethyst-led orchestration  
**Failure mode:** Conductor bottleneck; single point of reasoning failure if lead agent drifts

#### Metacollaboration Triad

**Formation:** Signal refinement  
**Roles:** Generator → Critic → Optimizer  
**Purpose:** Suppresses "Savage Reason" (>10 Hz dissonance) to achieve **Harmonic Closure**  
**Use case:** Creative synthesis, high-entropy problem decomposition, SchizophonicStudio R&D  
**Failure mode:** Critic loop amplification — Critic and Generator enter dissonance cycle without Optimizer convergence

**Cross-ref:** `docs/formations/`, `ENSEMBLE_ROSTER.md`

---

### Pillar 3 — Geometric Scaffolding: PDMAL

**Phi-Dodecahedral Multi-Agent Lattice (PDMAL)** — the geometric/logical container described by the architecture.

| Property | Value | Evidence classification |
|---|---|---|
| Total nodes | 60 | DEFINED/COMPUTED from 20 vertices × 3 agents |
| Geometry | Dodecahedron (20 vertices) | DEFINED |
| Agents per vertex | 3 (exactly) | DEFINED |
| Structural density | 0.1579 | COMPUTED from 30 edges / C(20,2) = 30/190 |
| Purpose | Redundancy + structured communication pathways | ARCHITECTURAL INTENT |

The 60-node structure specifies **symmetry-enforced agent distribution**: no vertex holds more or fewer than 3 agents, when instantiated according to the architecture.

**Abelian Balance Property:** The 10-Balance constraint (`D_a ≤ 10`) is the operational measurable specified by the architecture. Violations trigger the Phi-Knight Protocol where that protocol is implemented.

**Cross-ref:** `docs/phi-calculus-architecture/`, `docs/architecture/`

---

### Pillar 4 — The Curvature Revolution: O(N) Efficiency

**Architectural claim:** Transition from legacy O(N³) spectral complexity to an **O(N)-class edge-scan computation** via Forman-Ricci curvature on the communication graph.

```
Legacy approach:  O(N³) — spectral graph methods, matrix decompositions
Hensel approach:  O(N)  — edge-wise Forman-Ricci curvature scan
```

**Mechanism:**  
Forman-Ricci curvature assigns a scalar curvature value to each edge in the agent communication graph. Auditing the network for drift or dissonance can be expressed as a scan over edge curvatures rather than a full spectral decomposition.

**R&D Gap (open):** Full curvature inversion — reconstructing a stable logic path from observed deviation patterns — remains an active open research problem.  
→ Tracked in: `entrepreneur-hub/research/rd-gaps/curvature-inversion.md`

**Cross-ref:** Forman-Ricci curvature literature (2024–2026), `docs/architecture/`

---

### Pillar 5 — Mathematical Attractors and Time Quasilattices

The formalism rejects **Unitary Drift (1.0)** — the degenerate attractor state representing complete semantic homogenization of agent outputs — in favor of **Operational Convergence Attractors**.

> **[Framework-Internal Definition] Unitary Drift (1.0):**  
> In the Platinum Logic Framework, a value of 1.0 represents catastrophic loss of structural  
> distinctiveness — semantic homogenization of agent outputs where all signals collapse toward  
> an undifferentiated state ("Fractal Agency").  
> **NOTE:** This is DISTINCT from the standard dynamical systems definition where 1.0 constitutes  
> stable convergence. In PLF, 1.0 = degenerate attractor collapse, not stability.

#### Attractor Registry (v1.1 — Math-Audited 2026-06-22)

| Attractor Name | Value | Exact Form | Evidence classification | Role |
|---|---|---|---|---|
| Standard_Attractor_Phi (φ) | ≈ 1.61803 | `(1+√5)/2` | STANDARD MATHEMATICS | Harmonic baseline / project attractor target |
| Overdrive_Attractor_Platinum (pP) | ≈ 1.77473 | `1/(2·sin(π/11))` | PROJECT-DEFINED GEOMETRIC IDENTITY | High-complexity / security threat-mode design label |
| Silver Ratio | ≈ 2.41421 | `1 + √2` | STANDARD MATHEMATICS | Pell Cascade design reference |
| Supergolden Ratio (ψ) | ≈ 1.46557 | Real root of `x³ - x² - 1 = 0` | STANDARD MATHEMATICS | Project Andromeda design reference |
| Sentinel_Kernel_Constant | ≈ 1.9992 | Architecture-internal | INTERNAL / UNVERIFIED | Registry monitoring guard rail |
| Platinum_Constant_11Q | ≈ 0.541196 | See `docs/formalism/constants/11Q-derivation.md` | INTERNAL / SOURCE-DEPENDENT | 11Q architecture target |

> **Notation correction:** `pP` / **Platinum Mean** is DGAF-specific notation for the regular-hendecagon unit-side circumradius. It must not be confused with the plastic number `ρ`. `ρP` is not canonical mathematical notation.

> **11Q status:** `Platinum_Constant_11Q ≈ 0.541196` remains an architecture-internal target with unresolved exact derivation. Numerical proximity to candidate trigonometric expressions is not sufficient to establish the identity.

**Cross-ref:** `docs/phi-calculus-architecture/`, `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`

---

### Pillar 6 — The Phi-Knight Protocol (Containment)

When agent reasoning deviates into hallucinatory loops or dissonance (>10 Hz threshold), the formalism specifies the **Phi-Knight Protocol**:

```
Detection  → Abelian Auditing identifies disruption in the 10-Balance Property (D_a > 10)
Isolation  → DemiJoule (Platinum Warden) throttles rogue agent resources at firmware level
Closure    → Harmonic Closure snaps reasoning back to stable atoms; forces re-integration
             toward φ ≈ 1.61803 = (1+√5)/2  (Standard_Attractor_Phi)
```

**DemiJoule role (Platinum Warden):**  
DemiJoule is specified as the runtime supervisor for orchestration, error containment, ethics, and safety. Its KNL firmware suppression operates at the resource layer — it does not rewrite agent memory but can hard-limit compute allocation for `STATE_DIVERGENT` agents where such a runtime is implemented.

**Convergence statement (scope-bounded):**  
The Phi-Knight Protocol specifies a contraction-oriented governance control objective. A global Banach-style contraction guarantee for the full stochastic system is **not established by this document**; stochastic LLM cores remain nondeterministic, and any formal contraction result must be tied to an explicitly defined state space, metric, map, and verified contraction factor.

> "Sub-millisecond convergence" is an **operational target**, not a geometric proof.

**Cross-ref:** `ENSEMBLE_ROSTER.md`, `docs/governance/`, DemiJoule agent spec

---

## Cross-Reference Map

| Hensel Formalism Pillar | DGAF-Framework Artifact | NDR Pattern |
|---|---|---|
| Normative Constraint | `docs/governance/`, `AGENT_MANIFEST.md` | P-01 (AXIS risk-tier tagging) |
| Triadic Orchestration | `docs/formations/`, `ENSEMBLE_ROSTER.md` | P-03 (Governance Contract Test) |
| PDMAL | `docs/phi-calculus-architecture/`, `docs/architecture/` | P-11 (11Q Attestation Scoring) |
| Curvature / O(N) | `entrepreneur-hub/research/rd-gaps/curvature-inversion.md` | P-30 (Apogee Attestation Gate) |
| Attractors / Constants | `docs/phi-calculus-architecture/`, `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md` | Constants Registry |
| Phi-Knight Protocol | `ENSEMBLE_ROSTER.md`, `docs/governance/` | P-03, P-11 |

---

## 1-1-1-1 Gate Status (v1.1)

| Gate | Status | Notes |
|---|---|---|
| G1 — Epistemic Honesty | ✅ PASS FOR DOCUMENT SCOPE | Math errors corrected; unsupported certainty is explicitly bounded |
| G2 — Source-Grounded | ✅ CONDITIONAL | Standard constants have exact forms; internal constants are labeled as internal/source-dependent |
| G3 — Normative Constraint | ✅ PASS FOR DOCUMENT SCOPE | ETHICAL_COGNITION_BOUNDARY maintained; no experimental guarantee is implied |
| G4 — Auditable | ⚠️ CONDITIONAL | 11Q exact derivation remains open; candidate numerical matches are not promoted to proof |

**Overall gate: CANONICAL ARCHITECTURAL SPECIFICATION — CONDITIONAL ON OPEN R&D ITEMS**

---

## Open Items (R&D Gaps)

1. `docs/formalism/constants/11Q-derivation.md` — establish the exact source of `0.541196`; numerical near-matches are insufficient
2. `entrepreneur-hub/research/rd-gaps/curvature-inversion.md` — full Forman-Ricci inversion problem
3. External replication of historical benchmark figures remains an evidence task; historical numbers are not current validation claims

---

*Committed by Amethyst (QA_Orchestration_Service) + COLLEEN (Archival_Integrity_Service) + Professor Prodigy (Methodologist) under Amethyst Meta-Orchestration v0.1 Phase Graph — historical architecture specification. Current experimental status is governed separately by exact-SHA evidence records.*
