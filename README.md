# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and the current pre-freeze governance state. Individual claims of validation, certification, performance, standards alignment, or commercial suitability require exact evidence and defined scope. Historical certifications remain scoped to the SHA/run/deployment that produced them and are not current certification without fresh evidence.

## Current project state — 2026-08-25

The DGAF/PDMAL experimental track remains **PRE-FREEZE**. The corrected pilot apparatus and supporting governance controls are present on `main`, but the current candidate has not been freeze-verified. No new experimental freeze exists, pilot authorization has not been granted, and empirical **N = 0**.

The historical implementation freeze `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains preserved as historical evidence only. It must not be described as the current freeze of the corrected apparatus.

The repository is also undergoing an ecosystem architecture pass separating DGAF implementation from the broader Pattern Commons and from commercialization, trademark, privacy, and security boundaries. These documentation changes do not themselves advance experimental gates.

For the authoritative gate board and remaining sequence, see [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) and [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md). For pattern architecture, see [`docs/PATTERN_COMMONS_ARCHITECTURE.md`](docs/PATTERN_COMMONS_ARCHITECTURE.md). For openness/commercialization boundaries, see [`docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`](docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md). For the asset-level ecosystem inventory, see [`docs/GOVERNANCE/DGAF_ASSET_LEVEL_BOUNDARY_INVENTORY_2026-08-25.md`](docs/GOVERNANCE/DGAF_ASSET_LEVEL_BOUNDARY_INVENTORY_2026-08-25.md). For future trademark/certification governance, see [`docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md).

## Repository scope

DGAF contains governance and evaluation components, agent specifications, control/gate definitions, provenance practices, epistemic auditing, vocabulary management, and experimental research artifacts. DGAF is the implementation/governance substrate; it is **not** the universal owner of every pattern, taxonomy, template, or research artifact in the surrounding ecosystem.

### Canonical terminology

- **DGAF** — Dynamic Governance Agentic Formation.
- **AHG** — Adaptive Harmonic Governance. Historical/conflicting expansions remain historical unless explicitly promoted by current governance.
- **PDMAL / PDMA-L** — Phi-Driven Multi-Agent Lattice. The term refers to the lattice/control research track; current evidence does not establish a complete Byzantine Fault Tolerance protocol merely from the topology.
- **NDR** — a project pattern namespace/family within the broader Pattern Commons architecture, not the entire ecosystem pattern corpus.
- **Pattern Commons** — proposed ecosystem-level layer for pattern identity, provenance, aliases/equivalence, epistemic status, and evidence relationships across repositories.
- **AXIS** — Agent X-axis Invariant Spectrum.
- **FLAG-02** — historical identifier associated with the former 340% coordination-gain claim. Current evaluation-mode terminology is **qualitative**. New documents must not introduce FLAG-02 as a current identifier for either meaning.

Historical documents may retain their original terminology when necessary for provenance, but they must be treated as historical rather than silently reinterpreted as current state.

## Epistemic standard

Claims are classified according to the repository standard:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

A mathematical term, external framework name, benchmark number, deployment, registry entry, commercial status, or agent role does not by itself establish implementation, validation, legal compliance, safety, certification, or independent verification.

## Core areas

- Agent orchestration and control-plane design
- Evaluation and quality-assurance tooling
- Provenance and traceability
- Governance gates and deployment controls
- Epistemic auditing and vocabulary management
- Pattern Commons integration and cross-repository reconciliation
- Experimental mathematical and structural research
- Open-source commercialization and evidence-preserving governance

## Open-source / commercialization posture

DGAF aims to keep the public reference implementation sufficiently complete for independent cloning, inspection, execution, and evaluation. Legitimate commercial differentiation may reside in managed operations, integration, assurance, support, hosting, specialized tooling, customer-specific configurations, training, and future certification programs. Public scientific/technical claims must retain enough evidence for independent evaluation even when adjacent operational assets are commercial or private.

The repository is licensed under Apache-2.0. See [`LICENSE`](LICENSE) for the legal terms. The license does not grant trademark rights; future official, certification, or endorsement claims bearing the DGAF name require separate governance and should not be inferred from repository status or project attestation.

## PDMAL/DGAF documentation spine

1. [Current State](docs/CURRENT_STATE.md)
2. [Project Status](docs/PROJECT_STATUS.md)
3. [PDMAL Current Control State](docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md)
4. [Authoritative PDMAL Task Specification](docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md)
5. [PDMAL Evidence Index](docs/evidence/PDMAL_EVIDENCE_INDEX.md)
6. [Evidence Ladder Policy](docs/evidence/EVIDENCE_LADDER_POLICY.md)
7. [PDMAL Experiment Protocol](docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md)
8. [Freeze Manifest Template](docs/experiment/FREEZE_MANIFEST_TEMPLATE.md)
9. [Propagation Consistency Control](docs/governance/PROPAGATION_CONSISTENCY_CONTROL.md)
10. [Documentation Reconciliation](docs/governance/DOCUMENTATION_RECONCILIATION_2026-08-21.md)
11. [Test Execution Readiness](docs/governance/TEST_EXECUTION_READINESS_2026-08-21.md)
12. [P3–P6 Freeze Readiness](docs/governance/P3_P4_P5_P6_FREEZE_READINESS_2026-08-21.md)
13. [P7 Primary Contrast Adjudication](docs/governance/P7_PRIMARY_CONTRAST_ADJUDICATION_PACKET_2026-08-21.md)
14. [Candidate Runtime Verification](docs/governance/CANDIDATE_RUNTIME_VERIFICATION_2026-08-21.md)
15. [NDR Research Program Charter — Current Status Addendum](docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_CURRENT_STATUS_2026-08-21.md)
16. [Freeze Packet Template](docs/governance/FREEZE_PACKET_TEMPLATE.md)
17. [Pattern Commons Architecture](docs/PATTERN_COMMONS_ARCHITECTURE.md)
18. [Commercialization & Openness Boundary](docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md)
19. [Asset-Level Boundary Inventory](docs/GOVERNANCE/DGAF_ASSET_LEVEL_BOUNDARY_INVENTORY_2026-08-25.md)
20. [Trademark & Certification Policy](docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md)
21. [CROSS_REF](CROSS_REF.md)

## Verification and test status

The repository contains deterministic/unit tests, pilot execution-contract tests, artifact/schema controls, governance consistency checks, propagation checks, and CI workflows. **Existence of a test is not evidence that the test has passed.** Current candidate verification must identify the exact candidate SHA, execution environment, deployment where applicable, run identifier, and retained evidence artifact.

### Current gate boundary

- P1 Candidate integrity — PARTIAL
- P2 Execution contract — PARTIAL
- P3 Artifact contract — PARTIAL
- P4 Security/blinding integrity — PARTIAL
- P5 Provenance/reproducibility — PARTIAL
- P6 Durable evidence custody — OPEN
- P7 Scientific target specification — PARTIAL; primary contrast OPEN
- P8 Analysis lock — OPEN
- P9 Independent verification — NOT EXECUTED
- New freeze — NOT CREATED
- Pilot authorization — NOT GRANTED
- Empirical N — 0

Do not infer repository-wide validation from a component-level test, historical attestation, deployment existence, README text, funding badge, commercial status, or certification language.

## Historical evidence boundary

Historical runtime, P2, P6a, and characterization records remain valid only for the exact source/deployment/run they document. In particular, retained historical results are not current-candidate verification.

## Related ecosystem

Related repositories are separate tracks. Shared terminology does not imply implementation equivalence or cross-repository validation. See [`CROSS_REF.md`](CROSS_REF.md) for the current cross-reference and epistemic boundary index.

## Support / funding

GitHub Sponsors configuration is present through `.github/FUNDING.yml`. Sponsorship supports maintenance and development; it does not confer ownership, certification, endorsement, or special evidence status.

## License

See [LICENSE](LICENSE) for the repository's applicable license.

## Provenance

Developed by Ndr / Ender Hensel (`ndrorchestration`).
