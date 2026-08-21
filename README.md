# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and the current pre-freeze governance state. Individual claims of validation, certification, performance, or standards alignment require exact evidence. Historical certifications remain scoped to the SHA/run/deployment that produced them and are not current certification without fresh evidence.

## Current project state — 2026-08-21

The DGAF/PDMAL experimental track is **PRE-FREEZE**. The corrected pilot apparatus and supporting governance controls are present on `main`, but the current candidate has **not** been freeze-verified. No new experimental freeze exists, pilot authorization has not been granted, and empirical **N = 0**.

The historical implementation freeze `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains preserved as historical evidence only. It must not be described as the current freeze of the corrected apparatus.

The repository is currently in documentation, provenance, and verification closure. The required execution events are candidate-bound tests, runtime verification, durable evidence custody, primary-contrast adjudication, analysis lock, and independent verification. Documentation changes do not themselves advance those gates.

For the authoritative gate board and remaining sequence, see [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) and [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md).

## Repository scope

DGAF contains governance and evaluation components, agent specifications, control/gate definitions, provenance practices, epistemic auditing, vocabulary management, and experimental research artifacts. It is the canonical home of the project's current governance vocabulary and epistemic classification standard.

### Canonical terminology

- **DGAF** — Dynamic Governance Agentic Formation.
- **AHG** — Adaptive Harmonic Governance. Historical/conflicting expansions remain historical unless explicitly promoted by current governance.
- **PDMAL / PDMA-L** — Phi-Driven Multi-Agent Lattice. The term refers to the lattice/control research track; current evidence does not establish a complete Byzantine Fault Tolerance protocol merely from the topology.
- **AXIS** — Agent X-axis Invariant Spectrum.
- **FLAG-02** — historical identifier associated with the former 340% coordination-gain claim. Current evaluation-mode terminology is **qualitative**. New documents must not introduce FLAG-02 as a current identifier for either meaning.

Historical documents may retain their original terminology when necessary for provenance, but they must be treated as historical rather than silently reinterpreted as current state.

## Epistemic standard

Claims are classified according to the repository standard:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

A mathematical term, external framework name, benchmark number, deployment, or agent role does not by itself establish implementation, validation, or equivalence.

## Core areas

- Agent orchestration and control-plane design
- Evaluation and quality-assurance tooling
- Provenance and traceability
- Governance gates and deployment controls
- Epistemic auditing and vocabulary management
- Experimental mathematical and structural research

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
10. [Test Execution Readiness](docs/governance/TEST_EXECUTION_READINESS_2026-08-21.md)
11. [P3–P6 Freeze Readiness](docs/governance/P3_P4_P5_P6_FREEZE_READINESS_2026-08-21.md)
12. [P7 Primary Contrast Adjudication](docs/governance/P7_PRIMARY_CONTRAST_ADJUDICATION_PACKET_2026-08-21.md)
13. [Candidate Runtime Verification](docs/governance/CANDIDATE_RUNTIME_VERIFICATION_2026-08-21.md)
14. [Freeze Packet Template](docs/governance/FREEZE_PACKET_TEMPLATE.md)

## Verification and test status

The repository contains deterministic/unit tests, pilot execution-contract tests, artifact/schema controls, governance consistency checks, propagation checks, and CI workflows. **Existence of a test is not evidence that the test has passed.** Current candidate verification must identify the exact candidate SHA, execution environment, deployment where applicable, run identifier, and retained evidence artifact.

The full-repository audit mechanism is present and designed to inventory every Git-tracked file, hash it, classify text/binary content, and detect stale historical bindings and documentation-state collisions. Its authoritative coverage artifact still requires an actual GitHub Actions execution against a fixed candidate.

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

Do not infer repository-wide validation from a component-level test, historical attestation, deployment existence, README text, or badge.

## Historical evidence boundary

Historical runtime, P2, P6a, and characterization records remain valid only for the exact source/deployment/run they document. In particular, the retained P6a result for `e1f077f` / `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` is historical evidence and is not current-candidate verification.

## Related ecosystem

Related repositories are separate tracks. Shared terminology does not imply implementation equivalence or cross-repository validation.

## License

See [LICENSE](LICENSE) for the repository's applicable license.

## Provenance

Developed by Ndr / Ender Hensel (`ndrorchestration`).
