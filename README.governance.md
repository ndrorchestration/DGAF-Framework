# DGAF-Framework — Governance Reference

> **Audience:** readers evaluating DGAF's governance model, control boundaries, evidence discipline, and relationship to external frameworks.
>
> **Important:** DGAF distinguishes project governance design from external legal or regulatory compliance. References to NIST, EU AI Act, OWASP, or other external frameworks are mappings for analysis and design unless a claim is explicitly supported for the relevant system, jurisdiction, version, and evidence scope.

## Governance in one view

DGAF treats governance as an engineering layer around agentic systems rather than as documentation added after implementation. The repository defines authority boundaries, control gates, evidence states, provenance requirements, failure handling, and promotion rules so that system behavior can be inspected and its claims can be traced to evidence.

The central design principle is simple: **a governance rule is not evidence that the implementation satisfies the rule.** Design, implementation, test results, verification, authorization, and empirical findings remain separate states.

## Core governance principles

- **Human authority remains explicit.** Agents operate within defined contracts and do not acquire authority merely through repetition, confidence, or role naming.
- **Failure is contained.** Required controls fail closed when their contract or evidence boundary cannot be established.
- **Evidence is scoped.** A result belongs to the exact artifact, candidate, environment, deployment, and run that produced it.
- **Provenance is first-class.** Important state transitions should remain reconstructable from repository history and retained evidence.
- **Semantics are governed.** New terminology, classifications, and ontology are treated as candidate vocabulary until appropriately established.
- **External frameworks are references, not automatic certifications.** Similarity to a standard or regulation does not establish compliance.

## External-framework mapping

DGAF maintains mappings to external frameworks where they help analyze governance requirements. These mappings should be read as **design correspondence**, not as declarations of legal conformity.

| Reference | DGAF use |
|---|---|
| NIST AI RMF | Risk-management concepts and governance vocabulary |
| EU AI Act | Regulatory concepts used for requirements analysis where applicable |
| OWASP Agentic AI guidance | Security and agentic-risk categories used for control design |
| Other standards/frameworks | Scoped references maintained according to their own versions and applicability |

For a claim of actual compliance, assess the applicable framework version, system role, jurisdiction, legal requirements, implementation evidence, and independent review separately.

## Governance architecture

The public governance model can be understood as six cooperating concerns:

1. **Authority** — who may decide, approve, override, or promote.
2. **Control** — what gates and constraints apply to an operation.
3. **Evidence** — what is known, and at what epistemic level.
4. **Provenance** — which artifact, source, candidate, or execution produced the evidence.
5. **Semantics** — which definitions and ontology are authorized for use.
6. **Review** — how failures, disagreements, regressions, and proposed changes are handled.

These concerns are implemented through project-local gates, agent contracts, evidence policies, repository controls, and experiment governance. The technical details live in the linked specifications rather than being duplicated here.

## Evidence and status

DGAF uses an explicit epistemic vocabulary:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

The vocabulary prevents a common failure mode in technical governance: allowing a design statement, passing unit test, historical attestation, or numerical result to silently become a broader system claim.

Current experimental state is maintained separately from general repository engineering. See [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) and [`docs/PROJECT_STATUS.md`](./docs/PROJECT_STATUS.md) for the authoritative current record.

## Human and societal boundary

DGAF places human dignity, human rights, safety, privacy, non-discrimination, human agency, legitimate oversight, accountability, and appropriate disclosure ahead of technical optimization. This boundary is defined in [`docs/agents/LAYER_0_CONSTITUTION.md`](./docs/agents/LAYER_0_CONSTITUTION.md) and the related authority controls.

The repository distinguishes law and regulation, recognized standards, governance frameworks, human-rights instruments, best practices, social expectations, engineering conventions, and DGAF design choices. Those categories may inform one another, but they are not interchangeable.

## Current experimental boundary

The PDMAL research track is maintained under a deliberately conservative publication posture. Current public documentation should be read as describing **pre-freeze engineering and governance work**, not as evidence of completed empirical validation.

For exact candidate identity, gate state, authorization, and retained evidence, use the current-state and experiment records rather than relying on summary language here.

## Key references

- [Current state](./docs/CURRENT_STATE.md)
- [Project status](./docs/PROJECT_STATUS.md)
- [Evidence ladder policy](./docs/evidence/EVIDENCE_LADDER_POLICY.md)
- [PDMAL experiment protocol](./docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md)
- [Agent authority invariant](./docs/agents/AGENT_AUTHORITY_INVARIANT.md)
- [Agent authority matrix](./docs/agents/AGENT_AUTHORITY_MATRIX.md)
- [Public Surface QA Standard](./docs/governance/PUBLIC_SURFACE_QA_STANDARD.md)
- [Documentation Style Guide](./docs/governance/DOCUMENTATION_STYLE_GUIDE.md)
- [Trademark & Certification Policy](./docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md)

## Certification and commercialization

There is currently no basis in this document for treating DGAF as externally certified, legally compliant, independently validated, or commercially assured. The Apache-2.0 license governs the repository's code and documentation as specified by the repository license; trademarks, certification programs, endorsements, managed services, and commercial offerings are separate governance questions.

---

*This document explains the governance model. It does not alter technical contracts, experimental authorization, evidence state, or repository authority.*
