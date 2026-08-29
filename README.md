# DGAF Framework

**Dynamic Governance Agentic Formation (DGAF)** is a research and implementation framework for building **governed agentic systems**—systems in which agent orchestration, evaluation, provenance, and control are treated as first-class engineering concerns.

DGAF is designed around a simple premise: capable agents need more than prompts and tools. They need explicit boundaries, inspectable decisions, evidence-aware evaluation, and mechanisms for preventing an implementation from quietly becoming more authoritative than its evidence supports.

> **Project status — 2026-08-29:** The engineering track is active. The separate PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**. Current engineering work does not constitute experimental authorization or empirical efficacy.

[Current State](docs/CURRENT_STATE.md) · [Project Status](docs/PROJECT_STATUS.md) · [Pattern Commons Architecture](docs/PATTERN_COMMONS_ARCHITECTURE.md) · [Cross-Reference](CROSS_REF.md)

---

## Why DGAF?

Most agent systems focus on what an agent can do. DGAF focuses on the control surface around those capabilities:

- **Authority** — what an agent or component is allowed to decide or invoke.
- **Governance** — how decisions move through explicit gates and constraints.
- **Evidence** — what was actually observed, computed, tested, or verified.
- **Provenance** — which source, candidate, environment, deployment, and run produced an artifact.
- **Epistemic discipline** — preventing hypotheses, historical results, terminology, or confidence from silently becoming facts.
- **Failure containment** — preserving fail-closed behavior when required controls are missing, ambiguous, or broken.
- **Reproducibility** — making important claims traceable to concrete execution boundaries rather than to documentation alone.

The goal is not to make stronger claims about an agent. The goal is to make the **claims and controls around an agent inspectable**.

## What is in this repository?

DGAF is the governance and implementation substrate for a broader research ecosystem. Major areas include:

| Area | Purpose |
|---|---|
| **Agent orchestration** | Control-plane structures, agent contracts, authority boundaries, and governed coordination |
| **TGL** | Governance-gate and status-reduction mechanisms with fail-closed semantics |
| **Evaluation** | Deterministic tests, regression coverage, execution contracts, and quality controls |
| **Provenance** | Source identity, evidence lineage, artifact integrity, and audit records |
| **Epistemic governance** | Explicit distinctions between defined, implemented, computed, verified, historical, and hypothetical claims |
| **Semantic governance** | Vocabulary, ontology, terminology, and semantic-drift controls |
| **PDMAL** | A separate experimental research track for Phi-Driven Multi-Agent Lattice structures |
| **Pattern Commons** | Cross-repository pattern identity, provenance, aliases, and evidence relationships |

DGAF does **not** claim ownership of every pattern, taxonomy, template, or research artifact associated with the surrounding ecosystem. Repository boundaries and evidence relationships are maintained explicitly.

## Architecture at a glance

```text
                         ┌─────────────────────────┐
                         │       Human / Rights    │
                         │   Constitutional Layer  │
                         └────────────┬────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │     Governance / TGL    │
                         │  authority + gate logic │
                         └────────────┬────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
   ┌─────────▼─────────┐   ┌──────────▼─────────┐   ┌────────▼─────────┐
   │ Agent / Control    │   │ Evaluation / QA    │   │ Provenance /     │
   │ Plane              │   │                   │   │ Evidence         │
   └─────────┬─────────┘   └──────────┬─────────┘   └────────┬─────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │ Governed Execution /    │
                         │ Research Substrates     │
                         └────────────┬────────────┘
                                      │
                         ┌────────────▼────────────┐
                         │   PDMAL Research Track  │
                         └─────────────────────────┘
```

The architecture is intentionally layered: an experimental result is not allowed to become a governance fact merely because the underlying component exists or a test happens to pass.

## Current engineering state

The current engineering lane is **PR #139**, which consolidates the governed control-plane work and TGL hardening. Its substantive implementation checkpoint passed **41/41** control-plane, TGL, adversarial, and capability-boundary tests at the exact checkpoint `a728ce3ee8a024646c0971c9d4f392abaa3d691a`. Subsequent changes on the current PR head are documentation, governance, CI, and provenance-hardening changes; claims from the earlier checkpoint are therefore kept scoped to that exact SHA.

The experimental boundary is intentionally separate:

- **PDMAL experimental state:** PRE-FREEZE / FAIL-CLOSED
- **Pilot authorization:** NOT GRANTED
- **Empirical N:** 0
- **Current experimental verification boundary:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
- **New immutable freeze:** NOT CREATED

These constraints are not a statement that the engineering work is inactive. They are the boundary between **building the apparatus** and **claiming experimental evidence from it**.

For the detailed, machine-oriented state record, see [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md).

## Evidence model

DGAF uses an explicit evidence vocabulary:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

The sequence is not a maturity score. It is a way to prevent different kinds of statements from being conflated.

A passing component test does not automatically validate the whole system. A deployment does not automatically validate the source that produced it. A historical run does not automatically validate a later candidate. A mathematical term, framework name, or agent role does not establish implementation or authority by itself.

See [`docs/evidence/EVIDENCE_LADDER_POLICY.md`](docs/evidence/EVIDENCE_LADDER_POLICY.md) for the formal policy.

## Human and societal boundary

DGAF treats human dignity, human rights, safety, lawful operation, privacy, non-discrimination, human agency, legitimate oversight, public accountability, and appropriate disclosure as constraints that precede technical optimization.

This is a governance boundary, not a claim of legal compliance. DGAF distinguishes law and regulation, recognized standards, governance frameworks, human-rights instruments, best practices, social expectations, engineering conventions, and DGAF-specific design choices.

See [`docs/agents/LAYER_0_CONSTITUTION.md`](docs/agents/LAYER_0_CONSTITUTION.md) and [`docs/agents/AGENT_AUTHORITY_INVARIANT.md`](docs/agents/AGENT_AUTHORITY_INVARIANT.md).

## Research tracks

### Governed control plane

The primary engineering effort is a governed recursive control plane with explicit authority inheritance, bounded execution, deterministic lifecycle behavior, provenance, authorization barriers, and hardened governance semantics.

### TGL

TGL provides governance-gate semantics for evaluating whether required controls are satisfied. Current work emphasizes explicit required/conditional gate behavior, deterministic status reduction, fail-closed exception handling, and auditable sealing of the resulting gate state.

### PDMAL

PDMAL (**Phi-Driven Multi-Agent Lattice**) is a separate experimental research track. Its topology and mathematical structures are hypotheses and research objects until the corresponding experimental protocol, verification boundary, and evidence establish stronger claims.

In particular, the repository does not treat PDMAL topology alone as proof of a complete Byzantine Fault Tolerance protocol or any other externally defined property.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/ndrorchestration/DGAF-Framework.git
cd DGAF-Framework
```

### 2. Start with the project state

Read [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) before interpreting experimental or verification claims. It records the authoritative current boundary and distinguishes active engineering work from historical evidence.

### 3. Explore the architecture

Start with:

- [`docs/PATTERN_COMMONS_ARCHITECTURE.md`](docs/PATTERN_COMMONS_ARCHITECTURE.md)
- [`docs/agents/AGENT_AUTHORITY_MATRIX.md`](docs/agents/AGENT_AUTHORITY_MATRIX.md)
- [`docs/agents/AGENT_AUTHORITY_INVARIANT.md`](docs/agents/AGENT_AUTHORITY_INVARIANT.md)
- [`docs/evidence/EVIDENCE_LADDER_POLICY.md`](docs/evidence/EVIDENCE_LADDER_POLICY.md)

### 4. Explore the experimental track

For PDMAL, use the protocol and evidence documents rather than README summaries:

- [`docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md`](docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md)
- [`docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`](docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md)
- [`docs/evidence/PDMAL_EVIDENCE_INDEX.md`](docs/evidence/PDMAL_EVIDENCE_INDEX.md)
- [`docs/experiment/FREEZE_MANIFEST_TEMPLATE.md`](docs/experiment/FREEZE_MANIFEST_TEMPLATE.md)

## Canonical terminology

- **DGAF** — Dynamic Governance Agentic Formation.
- **TGL** — the repository's governance-gate/control semantics layer.
- **PDMAL** — Phi-Driven Multi-Agent Lattice, the experimental lattice/control research track.
- **Pattern Commons** — the proposed ecosystem-level layer for pattern identity, provenance, aliases/equivalence, epistemic status, and evidence relationships.
- **NDR** — a project pattern namespace/family within the broader Pattern Commons architecture.
- **pP / Platinum Mean** — intentional DGAF notation for `1/(2 sin(π/11)) ≈ 1.774732842`. This is project-specific notation and is not presented as a universal mathematical symbol.

For mathematical notation, historical terminology, and semantic corrections, see [`docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md).

## Documentation map

| Need | Start here |
|---|---|
| Current project state | [`CURRENT_STATE.md`](docs/CURRENT_STATE.md) |
| Executive/project status | [`PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) |
| Architecture | [`PATTERN_COMMONS_ARCHITECTURE.md`](docs/PATTERN_COMMONS_ARCHITECTURE.md) |
| Evidence policy | [`EVIDENCE_LADDER_POLICY.md`](docs/evidence/EVIDENCE_LADDER_POLICY.md) |
| PDMAL experiment | [`PDMAL_EXPERIMENT_PROTOCOL.md`](docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md) |
| Agent authority | [`AGENT_AUTHORITY_MATRIX.md`](docs/agents/AGENT_AUTHORITY_MATRIX.md) |
| Public documentation standard | [`PUBLIC_SURFACE_QA_STANDARD.md`](docs/governance/PUBLIC_SURFACE_QA_STANDARD.md) |
| Commercialization boundary | [`DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`](docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md) |
| Cross-repository relationships | [`CROSS_REF.md`](CROSS_REF.md) |

The repository contains substantially more detailed governance and evidence records. The README deliberately acts as the **public entry point**, not as the complete control ledger.

## Open source and contribution

DGAF is released under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

The public repository is intended to remain inspectable and reproducible enough for independent technical evaluation. Commercial differentiation, where applicable, may exist in managed operations, integration, assurance, support, hosting, specialized tooling, customer-specific configurations, training, or future certification programs; those possibilities do not change the evidence requirements for public technical claims.

For contribution and community expectations, see the repository's contribution and governance documentation. Issues and pull requests should identify the affected component, evidence boundary, and expected behavioral change rather than relying on broad claims about the system as a whole.

## Support and project navigation

- **Current state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Project status:** [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
- **Issues and engineering work:** use the repository's GitHub Issues and Pull Requests
- **Funding:** GitHub Sponsors is available through [`.github/FUNDING.yml`](.github/FUNDING.yml)

## Maintainer

**Ndr / Ender Hensel** — [`ndrorchestration`](https://github.com/ndrorchestration)

DGAF is developed as an open research and engineering project. Its documentation intentionally separates what the project **is building** from what the evidence has **already established**.
