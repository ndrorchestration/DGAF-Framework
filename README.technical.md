# DGAF-Framework — Technical Reference

> **Audience:** engineers, researchers, and contributors working with DGAF implementation and control artifacts.
>
> **Evidence boundary:** This reference describes project architecture and implementation surfaces. A design, implementation, passing test, mathematical result, historical attestation, independently validated result, and successful deployment are different evidence states.

DGAF is a framework for governed agent orchestration, evaluation, provenance, and control design. This document provides a technical map; authoritative specifications and current experimental status remain in the linked records.

For industry-neutral explanations of DGAF-specific terminology, start with [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md). For live state, use [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md).

## Architecture at a glance

DGAF's implementation surfaces include:

- **Control and gates** — project-defined checks and execution constraints.
- **Runtime components** — routing, evaluation, replay, and constraint implementations.
- **Governance Command Center** — presentation-only views over normalized governance/current-state data.
- **Patterns** — reusable architecture and governance conventions.
- **Trace and provenance tooling** — mechanisms for recording and examining execution context.
- **Repository assurance inventory** — machine-readable mappings of selected recurring assurance families and explicit coverage gaps.
- **Experimental infrastructure** — research apparatus maintained separately from general engineering claims.

## Project control stack

DGAF uses named gates and controls where a project contract requires explicit evaluation or escalation. Gate names and PASS states are project-local unless supported by additional claim-specific evidence.

Current specifications: [`docs/gates/`](./docs/gates/)

| Area | Examples |
|---|---|
| Control checks | P-10, P-11, P-13 and related gate contracts |
| Authority and promotion | Agent authority controls and project-defined promotion procedures |
| Structural review | Project-local architecture and consistency checks |
| Presentation projection | Decision Frontier, Governance Map, State-Space Explorer V0, ORBIT/Evidence Observer |
| Assurance inventory | `registry/audit_catalog.v1.json`, coverage-gap scanner |

## Governance Command Center

The current accepted source architecture is a decomposed Next.js application under `app/` with normalized governance state in `app/lib/`, dedicated presentation components under `app/components/`, and semantic styles under `app/styles/`.

Three Semantic Control Field tranches are accepted on protected `main`:

1. **Decision Frontier — PR #776**
   - derives from canonical governance stages rather than maintaining a second lifecycle;
   - presents current governed state, supporting evidence/provenance, blocking boundary, nearest admissible transition, unreachable transitions, consequence preview, and receipt semantics;
   - remains presentation-only.
2. **Governance Map — PR #779**
   - derives its vertical spine from canonical governance stages;
   - renders explicitly named lateral relationships rather than inferred coupling;
   - renders global field conditions separately from lifecycle stages;
   - preserves evidence/authorization/non-effect boundaries and avoids readiness percentages or continuous-state implications.
3. **State-Space Explorer V0 — PR #783**
   - derives canonical stage identity/order, native predicate state, and global constraints from the shared governance truth model;
   - projects categorical `established`, `frontier`, and `blocked_by_predecessor` reachability separately from native stage state;
   - classifies candidate dimensions as `projectable`, `bounded`, or `not_modeled` rather than inventing scalar coordinates;
   - explicitly leaves consequence and reversibility **NOT MODELED — DO NOT INFER** and remains presentation-only.

State-Space Explorer V0 establishes only a discrete categorical projection. Conceptual tensor/manifold research remains non-authoritative guidance unless later formalization defines and verifies exact continuous coordinates, transition geometry, authorization distance, efficacy gradients, or other quantitative state-space semantics.

## Repository assurance inventory

The repository now contains a bounded machine-readable assurance catalog:

- `registry/audit_catalog.v1.json` — accepted partial catalog with `coverage.status = PARTIAL_CORE_FAMILIES_ONLY`;
- `registry/audit_catalog.py` — deterministic loading/validation and workflow coverage-gap helpers;
- tests under `tests/` that validate catalog structure and coverage behavior.

The accepted sequence is:

- **PR #780** — initial bounded catalog and deterministic validation;
- **PR #782** — workflow coverage-gap scanner for `.github/workflows/*.yml|*.yaml` not exactly bound by catalog `implementation` paths;
- **PR #785** — seven additional source-verified recurring assurance mappings.

Important semantics:

- catalog membership is not the same as protected-branch requiredness;
- current protected-main required contexts are separately read as **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**;
- an unmapped workflow is a coverage gap only;
- `UNMAPPED` or `UNCLASSIFIED` must not be translated into “non-assurance” without explicit adjudication;
- catalog coverage remains partial and does not claim exhaustive audit, security, governance, or scientific assurance.

## Current materialization tooling lineage

The accepted Epoch 002 materialization apparatus is tooling/provenance only:

- predecessor Stage-1 / Stage-2 tooling: PR #713 / PR #715;
- accepted Stage-1 locked-archive representation repair: PR #794;
- accepted Stage-2 provenance rebind: PR #797;
- accepted Stage-1 identity: commit `cf32a62bbf08a1b8db39709f4989be1be800d64e`, blob `3a825b026423952c2844cb18664eb6395b72fdc1`.

The dedicated materialization workflow verifies tooling-only mode, Stage-1 tests, the Stage-1→Stage-2 binding, and bound Stage-2 bundle behavior. The real evidence-admission and real receipt-event paths remain unexecuted/skipped. No real materialization, receipt, primary-analysis authorization, scientific-N increment, efficacy, or independent validation is established by these tooling results.

## Runtime components

| Component | Purpose |
|---|---|
| KAPPA Dynamic Confidence Router | Confidence-gated routing and category-sensitive weight selection |
| Evaluate Router | Batch pipeline composition |
| Normative Constraint | Project-defined deontic and epistemic constraint implementation |
| PPTL | Experimental topology and orchestration harness |
| Replay authority contracts | Fail-closed replay/effect handling and provider-neutral persistence boundaries |
| External runtime ingress contract | Provider-neutral non-authoritative input-envelope validation |

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
- [`registry/audit_catalog.v1.json`](./registry/audit_catalog.v1.json)

A successful source/build/CI result does not establish deployment health. A READY or failed deployment does not establish scientific authorization or empirical support. The same separation applies in the opposite direction: experimental evidence does not silently upgrade runtime or production state.

## Mathematical and research terminology

DGAF uses project-specific mathematical notation in some research tracks. Mathematical notation should be interpreted according to the repository's notation policy and the scope of the associated model; a mathematical property of a model does not automatically describe a deployed system.

See [`docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](./docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md).

## Current and historical state

For current project status and experimental boundaries, use:

- [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) — live current-facing state authority;
- [`docs/PROJECT_STATUS.md`](./docs/PROJECT_STATUS.md) — compatibility entrypoint that redirects to current state.

Historical implementation records and earlier terminology remain available for provenance. See [`docs/HISTORICAL_RECORDS_INDEX.md`](./docs/HISTORICAL_RECORDS_INDEX.md) before treating an older record as current authority.

## Related references

- [`README.md`](./README.md) — public project overview
- [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md) — plain-English terminology and claim-state translation
- [`README.governance.md`](./README.governance.md) — governance model and standards crosswalk
- [`docs/PATTERN_COMMONS_ARCHITECTURE.md`](./docs/PATTERN_COMMONS_ARCHITECTURE.md) — ecosystem pattern architecture

---

*This reference is an implementation map, not a certification, regulatory-conformance statement, deployment attestation, or efficacy report. Updated 2026-09-18. Exact source identity is established by Git history and the protected `main` commit at the time of use; this document does not embed a volatile SHA as a standing current-state claim.*
