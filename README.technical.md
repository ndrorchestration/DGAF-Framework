# DGAF-Framework — Technical Reference

> **Audience:** engineers, researchers, and contributors working with DGAF implementation and control artifacts.
>
> **Evidence boundary:** This reference describes project architecture and implementation surfaces. A design, implementation, passing test, mathematical result, historical attestation, and independently validated empirical result are different evidence states.

DGAF is a framework for governed agent orchestration, evaluation, provenance, and control design. This document provides a technical map; authoritative specifications and current experimental status remain in the linked records.

## Architecture at a glance

DGAF's implementation surfaces include:

- **Control and gates** — project-defined checks and execution constraints.
- **Runtime components** — routing, evaluation, and constraint implementations.
- **Patterns** — reusable architecture and governance conventions.
- **Trace and provenance tooling** — mechanisms for recording and examining execution context.
- **Experimental infrastructure** — research apparatus maintained separately from general engineering claims.

## Project control stack

DGAF uses named gates and controls where a project contract requires explicit evaluation or escalation. Gate names and PASS states are project-local unless supported by additional claim-specific evidence.

Current specifications: [`docs/gates/`](./docs/gates/)

| Area | Examples |
|---|---|
| Control checks | P-10, P-11, P-13 and related gate contracts |
| Authority and promotion | Agent authority controls and project-defined promotion procedures |
| Structural review | Project-local architecture and consistency checks |

## Runtime components

| Component | Purpose |
|---|---|
| KAPPA Dynamic Confidence Router | Confidence-gated routing and category-sensitive weight selection |
| Evaluate Router | Batch pipeline composition |
| Normative Constraint | Project-defined deontic and epistemic constraint implementation |
| PPTL | Experimental topology and orchestration harness |

See [`components/README.md`](./components/README.md) and [`pptl/README.md`](./pptl/README.md) for implementation-level details.

## Patterns and agent architecture

The NDR pattern registry records project patterns for recurring orchestration, governance, and engineering problems. Pattern identifiers are references to project designs; their existence is not evidence of universal effectiveness.

Named agent roles provide an architectural vocabulary for responsibilities and interfaces. Authority is determined by explicit contracts, not by a role name or an agent's output.

- [`docs/patterns/NDR_PATTERN_REGISTRY.md`](./docs/patterns/NDR_PATTERN_REGISTRY.md)
- [`ENSEMBLE_ROSTER.md`](./ENSEMBLE_ROSTER.md)
- [`docs/agents/AGENT_AUTHORITY_MATRIX.md`](./docs/agents/AGENT_AUTHORITY_MATRIX.md)

## Testing and evidence

Tests establish behavior for the contracts and environments they cover. Read results with their exact source identity, configuration, and retained evidence when making broader claims.

Key references:

- [`docs/CLAIM_EVIDENCE_INDEX.md`](./docs/CLAIM_EVIDENCE_INDEX.md)
- [`docs/evidence/EVIDENCE_LADDER_POLICY.md`](./docs/evidence/EVIDENCE_LADDER_POLICY.md)
- [`docs/EPISTEMIC_EVIDENCE_STANDARD.md`](./docs/EPISTEMIC_EVIDENCE_STANDARD.md)
- [`docs/qa/README.md`](./docs/qa/README.md)

## Mathematical and research terminology

DGAF uses project-specific mathematical notation in some research tracks. Mathematical notation should be interpreted according to the repository's notation policy and the scope of the associated model; a mathematical property of a model does not automatically describe a deployed system.

See [`docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](./docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md).

## Current and historical state

For current project status and experimental boundaries, use:

- [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md)
- [`docs/PROJECT_STATUS.md`](./docs/PROJECT_STATUS.md)

Historical implementation records and earlier terminology remain available for provenance. See [`docs/HISTORICAL_RECORDS_INDEX.md`](./docs/HISTORICAL_RECORDS_INDEX.md) before treating an older record as current authority.

## Related references

- [`README.md`](./README.md) — project overview
- [`README.governance.md`](./README.governance.md) — governance model
- [`docs/PATTERN_COMMONS_ARCHITECTURE.md`](./docs/PATTERN_COMMONS_ARCHITECTURE.md) — ecosystem pattern architecture
- [`docs/governance/PUBLIC_DOCUMENTATION_INFORMATION_ARCHITECTURE.md`](./docs/governance/PUBLIC_DOCUMENTATION_INFORMATION_ARCHITECTURE.md) — documentation placement and navigation

---

*This reference is an implementation map, not a certification, regulatory-conformance statement, or efficacy report.*
