# DGAF-Framework — Technical Reference

> **Audience:** engineers, researchers, and contributors working with DGAF implementation and control artifacts.
>
> **Evidence boundary:** architecture, implementation, passing tests, accepted source, deployment/runtime evidence, authorization, and empirical support are distinct states.

DGAF is a framework for governed agent orchestration, evaluation, provenance, authorization, and control design. For live status use [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md); for industry-neutral terms use [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md).

## Current protected source

Protected signed/verified `main` is `b1d91621bd73e70866d5ff8fd38fb98e440b30e9` after accepted PR #783.

## Architecture at a glance

DGAF implementation surfaces include:

- governance stages, claim/action authority, and fail-closed gates;
- runtime routing/evaluation/replay/constraint components;
- the Governance Command Center and ORBIT/Evidence Observer presentation layers;
- provenance, custody, trace, and evidence tooling;
- a bounded machine-readable repository assurance catalog;
- prospective/blinded experimental apparatus and analysis-control tooling.

## Governance Command Center

The current frontend is a decomposed Next.js application under `app/`, with normalized governance/state models in `app/lib/`, dedicated components under `app/components/`, and semantic styles under `app/styles/`.

### Accepted Semantic Control Field tranches

**Decision Frontier — PR #776**

- derives from canonical governance stages rather than a duplicate lifecycle;
- presents current governed state, supporting evidence/provenance, blocking boundary, nearest admissible transition, unreachable transitions, consequence preview, and receipt semantics;
- remains presentation-only.

**Governance Map — PR #779**

- derives its vertical spine from canonical governance stages;
- renders named lateral relationships rather than inferred coupling;
- renders global field conditions separately from lifecycle stages;
- keeps evidence, authority, authorization, and non-effects inspectable;
- avoids readiness scores and continuous-state implications.

**State-Space Explorer V0 — PR #783**

- derives stage identity/order and the current frontier from canonical governance stages;
- keeps native predicate state separate from derived reachability;
- uses discrete categories: `established`, `frontier`, `blocked_by_predecessor`;
- derives global constraints from the existing truth boundary;
- marks dimensions as projectable, bounded, or `not_modeled` rather than inventing coordinates;
- keeps consequence and reversibility explicitly unmodeled in V0;
- includes structural/non-color semantics, responsive behavior, reduced-motion treatment, and CSS containment regression coverage.

V0 explicitly prohibits readiness percentages, inferred authority, scalar evidence-quality scores, numeric confidence, success/authorization likelihood, distance-to-authorization, continuous interpolation/manifold coordinates, efficacy gradients, or inferred consequence/reversibility values.

## Repository assurance inventory

The accepted repository assurance inventory is bounded and machine-readable:

- `registry/audit_catalog.v1.json` — partial recurring-assurance catalog;
- `registry/audit_catalog.py` — deterministic loading/validation and workflow coverage-gap helpers;
- focused tests under `tests/`.

Accepted progression:

- **PR #780** — initial catalog + validator;
- **PR #782** — deterministic `collect_unmapped_workflows(...)` behavior;
- **PR #785** — seven additional source-verified recurring assurance mappings.

`coverage.status` remains **`PARTIAL_CORE_FAMILIES_ONLY`**.

Important semantics:

- catalog membership is not protected-branch requiredness;
- current protected-main required contexts are separately **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**;
- an unmapped workflow is a coverage gap only;
- `UNMAPPED` / `UNCLASSIFIED` must not be translated into “non-assurance” without explicit adjudication;
- **PR #784** was closed unmerged; its proposed workflow-role census is not accepted implementation.

## Runtime and authority separation

Selected runtime surfaces include:

| Component / area | Purpose |
|---|---|
| KAPPA Dynamic Confidence Router | Confidence-gated routing and category-sensitive weight selection |
| Evaluate Router | Batch pipeline composition |
| Normative Constraint | Project-defined deontic/epistemic constraints |
| PPTL | Experimental topology/orchestration harness |
| Replay authority contracts | Fail-closed replay/effect handling and provider-neutral persistence boundaries |
| External runtime ingress contract | Provider-neutral non-authoritative input-envelope validation |

A successful source/build/CI result does not establish current deployment health. A READY or failed deployment does not establish scientific authorization or empirical support. Runtime/provider evidence remains identity- and revision-bound.

## Scientific/experimental boundary

Current Track A Epoch 002 state:

- collection COMPLETE at 50 paired seed units / 2,250 blinded observations;
- dataset lock ESTABLISHED;
- bounded unblinding AUTHORIZED for controlled mapping release/decryption only;
- Stage-1/Stage-2 materialization apparatus ACCEPTED;
- prospective primary-analysis authorization tooling ACCEPTED / TOOLING ONLY;
- real materialization and materialization receipt NOT ESTABLISHED;
- primary analysis NOT AUTHORIZED / NOT RUN;
- scientific-N increment 0;
- canonical efficacy and independent validation NOT ESTABLISHED.

Current scientific transition:

`real materialization → non-secret evidence admission → immutable materialization receipt → separate primary-analysis authorization → locked analysis → interpretation/adjudication`

## Testing and evidence

Tests establish behavior only for the contracts, source identities, and environments they cover. Useful references:

- [`docs/CLAIM_EVIDENCE_INDEX.md`](./docs/CLAIM_EVIDENCE_INDEX.md)
- [`docs/evidence/EVIDENCE_LADDER_POLICY.md`](./docs/evidence/EVIDENCE_LADDER_POLICY.md)
- [`docs/EPISTEMIC_EVIDENCE_STANDARD.md`](./docs/EPISTEMIC_EVIDENCE_STANDARD.md)
- [`docs/qa/README.md`](./docs/qa/README.md)
- [`registry/audit_catalog.v1.json`](./registry/audit_catalog.v1.json)

## Patterns, roles, and terminology

Pattern identifiers, role labels, mathematical notation, and visualization metaphors are project vocabulary; their existence does not establish universal validity or effectiveness.

- [`docs/patterns/NDR_PATTERN_REGISTRY.md`](./docs/patterns/NDR_PATTERN_REGISTRY.md)
- [`docs/agents/AGENT_AUTHORITY_MATRIX.md`](./docs/agents/AGENT_AUTHORITY_MATRIX.md)
- [`docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`](./docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md)

## Current and historical routing

- [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) — live state authority;
- [`docs/PROJECT_STATUS.md`](./docs/PROJECT_STATUS.md) — compatibility entrypoint;
- [`README.md`](./README.md) — public overview;
- [`README.governance.md`](./README.governance.md) — governance and standards crosswalk;
- [`docs/HISTORICAL_RECORDS_INDEX.md`](./docs/HISTORICAL_RECORDS_INDEX.md) — historical/provenance routing.

---

*This reference is an implementation map, not a certification, legal-conformance statement, deployment attestation, or efficacy report. Updated 2026-09-17 through protected-main `b1d91621…`.*
