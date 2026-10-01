# ClaimGraph v0 — Public Profile and Portability Contract

Controller: #1173

## Status

PUBLIC-PROFILE SPECIFICATION ONLY.

The executable substrate already exists through merged PR #808. This document does not replace the existing Structural Epistemics schemas or validator, establish claim truth, infer evidence independence, grant authorization, or change DGAF/PDMAL scientific state.

## Purpose

Define a reusable public profile over the accepted Structural Epistemics claim/evidence graph.

Core abstraction:

```text
claims + evidence + typed relations + dependency structure
    -> structurally valid epistemic graph
```

A structurally valid graph is not necessarily true, independent, causal, authorized, compliant, production-ready, or safe.

## Compatibility rule

ClaimGraph v0 is a **profile over schema v1**, not a schema-v2 redesign.

Existing normative sources remain:

- `docs/research/STRUCTURAL_EPISTEMICS_CLAIM_RECORD_SCHEMA.json`
- `docs/research/STRUCTURAL_EPISTEMICS_EVIDENCE_GRAPH_SCHEMA.json`
- `scripts/validate_structural_epistemics_claim_graph.py`

A future schema v2 requires an evidenced incompatibility that cannot be handled safely by profile documentation, adapters, optional extension metadata, or a validation-receipt layer.

## Normative claim fields

ClaimGraph v0 retains:

- claim ID;
- proposition;
- claim class;
- exact system/context scope and exclusions;
- temporal validity and review condition;
- source roots;
- dependency signature;
- supporting evidence IDs;
- contradicting evidence IDs;
- explicit defeaters;
- decomposed uncertainty;
- calibration status;
- verification status;
- epistemic state;
- applicability state;
- causal level;
- authorization relevance;
- supersedes / superseded-by lineage;
- retraction state and reason.

## Normative evidence-node fields

Retain:

- evidence ID;
- evidence class;
- source roots;
- dependency roots;
- observation time;
- validity state and review condition;
- provenance reference.

## Normative relation vocabulary

Retain:

- `SUPPORTS`
- `CONTRADICTS`
- `DERIVED_FROM`
- `REPLICATES`
- `SHARES_SOURCE_ROOT`
- `SHARES_MODEL_LINEAGE`
- `SHARES_PROMPT_OR_POLICY`
- `SHARES_TOOL_OUTPUT`
- `DEFEATS`
- `SUPERSEDES`
- `RETRACTS`
- `VALID_DURING`

## Existing machine-decidable invariants

The accepted validator already enforces:

1. schema conformance for graph and claim records;
2. unique claim/evidence/relation identifiers;
3. non-colliding claim/evidence identifiers;
4. relation endpoint referential integrity;
5. no self-relations;
6. support/contradiction listings agree with explicit relations;
7. the same evidence cannot support and contradict one claim;
8. known/unknown dependency signatures are internally consistent;
9. triggered defeaters cannot leave a claim CURRENT;
10. retraction state and applicability state agree;
11. VERIFIED / EMPIRICALLY_SUPPORTED states require verified status;
12. EMPIRICALLY_SUPPORTED requires empirical support evidence;
13. CAUSAL_IDENTIFIED requires experiment or causal-design evidence;
14. non-proposed claims require current supporting evidence;
15. supersession declarations are reciprocal;
16. shared support roots require explicit dependence relations.

## Truth and authorization ceilings

A validator PASS establishes only:

> The supplied graph conforms to the declared ClaimGraph / Structural Epistemics structure and machine-decidable invariants.

Required public effect semantics:

```text
truth_effect = NONE
authorization_effect = NONE
```

A PASS does not establish:

- proposition truth;
- evidence independence;
- calibration correctness;
- empirical efficacy;
- causal validity beyond the encoded evidence/invariants;
- authorization or execution permission;
- legal/regulatory compliance;
- certification;
- production readiness;
- system-wide epistemic correctness.

## Uncertainty doctrine

ClaimGraph v0 does not collapse uncertainty into a single confidence scalar.

The existing decomposition remains normative:

- aleatoric;
- model / parameter;
- structural / model-form;
- data coverage;
- provenance;
- dependency;
- measurement;
- temporal;
- adversarial;
- decision / consequence.

`UNKNOWN` is an explicit state, not zero uncertainty.

## Dependency and independence doctrine

Evidence count is not independent-evidence count.

Shared roots/dependencies remain visible through:

- source roots;
- dependency roots;
- dependency signature;
- `SHARES_*` relations.

No universal evidence-weighting or confidence-aggregation function is part of ClaimGraph v0.

## Contradiction and revision doctrine

- retain contradictory evidence;
- retain triggered defeaters;
- retain superseded and retracted claims for historical reconstruction;
- supersession does not erase historical provenance;
- retraction removes present applicability, not history;
- temporal validity/review conditions remain explicit.

## Causal discipline

These remain distinct:

- association;
- prediction;
- intervention;
- mechanism hypothesis;
- causal identification.

Repeated agreement, graph structure, correlation, feature importance, or confidence does not itself establish a causal claim.

## Authorization relevance

`authorization_relevance` is metadata about how a claim may be used by a separate decision process.

It is not authorization.

ClaimGraph must not:

- execute actions;
- grant permissions;
- approve deployment;
- change DGAF/PDMAL state;
- substitute for Action Admission or another authority system.

## Validation receipt target

A reusable developer surface should add a JSON-safe validation result with:

- `valid`;
- `graph_id`;
- `schema_version`;
- stable reason/error codes;
- checks performed;
- claim count;
- evidence count;
- relation count;
- `truth_effect = NONE`;
- `authorization_effect = NONE`.

This receipt is a usability/conformance artifact only.

## Portability gate

Before classifying ClaimGraph as reusable beyond its originating program:

1. keep the #808 schema, fixture, and tests passing;
2. create one non-DGAF/PDMAL graph;
3. validate it with the same validator without forking the core;
4. preferred first example: software incident/root-cause analysis or AI workflow evaluation findings;
5. document any adoption friction as evidence;
6. add a public quickstart explaining support, contradiction, dependence, defeaters, staleness, supersession, retraction, and uncertainty.

## Packaging decision

Keep ClaimGraph within the Structural Epistemics / DGAF repository for the first portability tranche.

Do not create a standalone repository/package until an actual external consumer demonstrates a need for independent versioning, dependency ownership, or release cadence.

## Evidence boundary

The repository already has an accepted executable Structural Epistemics validator and schema. ClaimGraph v0 currently concerns public profile, developer usability, portability, and packaging.

The following remain NOT ESTABLISHED:

- external developer adoption;
- cross-domain usefulness beyond demonstrated examples;
- general epistemic correctness;
- independent validation;
- production readiness;
- certification/compliance;
- product-market fit.
