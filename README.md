# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and implemented artifacts. Individual claims of validation, certification, performance, or standards alignment require the evidence identified in the corresponding artifact. Historical certifications are not treated as current certification without a fresh evidence-backed run.

## Current project state — 2026-08-20

The DGAF/PDMAL experimental track is **PRE-FREEZE**. The runtime-characterization baseline is published, the blinding operational test is closed, and security hardening PR #70 has been merged. Epistemic architecture PR #65 has been **merged** at `915e454e27eb2770e7f40a067a881b0783feaae4`. PR #75 (evidence architecture and governance doc updates) has been **merged** at `a44e42cd3040`.

Current security baseline:

```text
main: df7d5fd8c8595cbb9d0c04caeaace13738d760ae
```

Pilot authorization has **not** been granted and no empirical pilot data exists.

For the authoritative gate board, provenance identities, remaining sequence, and freeze requirements, see [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md).

## Repository scope

DGAF contains governance and evaluation components, agent specifications, control/gate definitions, provenance practices, and related research artifacts. It is the canonical home for the project's current governance vocabulary and epistemic classification standard.

### Canonical terminology

- **DGAF** — Dynamic Governance Agentic Formation.
- **AHG** — Adaptive Harmonic Governance. Historical/conflicting expansions are retained in the acronym registry rather than used as current definitions.
- **PDMAL / PDMA-L** — Phi-Driven Multi-Agent Lattice. This term refers to the project's lattice/control research track; the current evidence does not establish a complete Byzantine Fault Tolerance (BFT) consensus protocol merely from the lattice topology.
- **AXIS** — Agent X-axis Invariant Spectrum. The expansion is canonical; operational or empirical claims require their own evidence.
- **SACP, MDAR, and FML** — project-local acronyms whose expansions remain source-controlled; consult `docs/taxonomy/NDR_ACRONYM_REGISTRY.md` rather than inferring an expansion.

## Epistemic standard

Claims are classified according to the repository standard:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

A mathematical term, external framework name, benchmark number, or agent role does not by itself establish implementation, validation, or equivalence.

## Core areas

- Agent orchestration and control-plane design
- Evaluation and quality-assurance tooling
- Provenance and traceability
- Governance gates and deployment controls
- Epistemic auditing and vocabulary management
- Experimental mathematical and structural research

## Current project state

For PDMAL/DGAF work, start with the documentation spine below:

1. [Current State — machine-adjacent snapshot](docs/CURRENT_STATE.md)
2. [PDMAL Current Control State](docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md)
3. [Authoritative PDMAL Task Specification v0.7.4](docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md)
4. [PDMAL Evidence Index](docs/evidence/PDMAL_EVIDENCE_INDEX.md)
5. [Evidence Ladder Policy](docs/evidence/EVIDENCE_LADDER_POLICY.md)
6. [Freeze Manifest Template](docs/experiment/FREEZE_MANIFEST_TEMPLATE.md)
7. [PDMAL Experiment Protocol](docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md)

## Documentation

- [Current Project Status](docs/PROJECT_STATUS.md)
- [Technical README](README.technical.md)
- [Governance README](README.governance.md)
- [Agent Registry](ENSEMBLE_ROSTER.md)
- [Ecosystem Map](CROSS_REF.md)
- [Epistemic Vocabulary Standard](docs/taxonomy/EPISTEMIC_VOCABULARY_STANDARD.md)
- [Acronym Registry](docs/taxonomy/NDR_ACRONYM_REGISTRY.md)
- [GATE-11Q](docs/gates/GATE_11Q.md)

## Status and validation

This repository contains artifacts at different maturity levels. Do not infer repository-wide validation from a component-level test, a historical attestation, or a README badge. Current verification should identify the exact commit, test/evaluation run, and evidence supporting the claim.

The v0.7.5 runtime-characterization release is an immutable historical baseline. Later security and epistemic-governance changes are not retroactively included in that release.

## Related ecosystem

Related repositories include Acoustic-mesh, Driftwatch, Amethyst-Governance-Eval-Stack, agent-control-plane, phi-calculus-app, and other ndrorchestration projects. They are separate repositories and tracks; shared terminology does not imply that their implementations are equivalent or that one repository validates another.

## License

See [LICENSE](LICENSE) for the repository's applicable license.

## Provenance

Developed by Ndr / Ender Hensel (`ndrorchestration`).
