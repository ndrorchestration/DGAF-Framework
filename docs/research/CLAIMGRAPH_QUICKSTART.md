# ClaimGraph v0 — Quickstart

Status: public-profile candidate over the accepted Structural Epistemics schema/validator.

## What ClaimGraph does

ClaimGraph gives you a machine-readable way to represent:

- what is being claimed;
- what evidence supports or contradicts it;
- which evidence paths share dependencies;
- what uncertainty remains;
- what would defeat the claim;
- when evidence becomes stale;
- how claims are superseded or retracted without deleting history.

Validator success establishes structural contract conformance only.

## Validate a graph

Use the existing accepted validator:

```bash
python scripts/validate_structural_epistemics_claim_graph.py \
  docs/research/fixtures/CLAIMGRAPH_SOFTWARE_INCIDENT_EXAMPLE.json
```

Or request a JSON-safe v0 receipt:

```bash
python scripts/claimgraph_v0.py \
  docs/research/fixtures/CLAIMGRAPH_SOFTWARE_INCIDENT_EXAMPLE.json
```

The receipt includes:

- valid / invalid;
- stable reason code;
- graph ID and schema version;
- claim/evidence/relation counts;
- validation scope;
- `truth_effect: NONE`;
- `authorization_effect: NONE`.

## Minimal mental model

```text
Evidence A ---- SUPPORTS ------> Claim X
Evidence B ---- CONTRADICTS ---> Claim X

Evidence A ---- SHARES_SOURCE_ROOT ---- Evidence C
Claim Y ------- SUPERSEDES -----------> Claim X
```

A graph can contain both support and counterevidence. Contradiction is preserved until explicitly resolved; the system should not silently average incompatible evidence away.

## Support and contradiction

A claim lists supporting and contradicting evidence IDs, and the graph must also contain matching typed relations.

If a supporting evidence ID is listed without a matching `SUPPORTS` relation, validation fails.

If contradicting evidence is listed without a matching `CONTRADICTS` relation, validation fails.

The same evidence cannot simultaneously be listed as both support and contradiction for one claim.

## Shared dependence

Two evidence nodes may look independent while sharing:

- the same source;
- model lineage;
- prompt/policy;
- upstream tool output;
- another dependency root.

When supporting evidence shares roots, the graph must make that dependence explicit through a `SHARES_*` relation.

This prevents “three pieces of evidence” from being silently treated as three independent evidence paths when they are not.

## Defeaters

A defeater is a condition that would undermine the current claim state.

Example:

```json
{
  "defeater_id": "DEF-REPRODUCTION",
  "condition": "controlled replay fails to reproduce the observed behavior",
  "status": "NOT_TRIGGERED"
}
```

If a defeater becomes `TRIGGERED`, the claim may not remain `CURRENT`.

## Staleness

Evidence has an explicit validity state:

- CURRENT
- STALE
- SUPERSEDED
- RETRACTED
- UNKNOWN

A non-proposed claim must retain at least one CURRENT supporting evidence node.

This means old evidence can remain historically visible without being treated as current.

## Supersession

Supersession is reciprocal.

If Claim B says it supersedes Claim A, Claim A must say it is superseded by Claim B.

The earlier claim remains in the graph for provenance/history.

Supersession is not deletion.

## Retraction

Retraction means the claim is no longer presently applicable.

A retracted claim must carry:

- applicability state = RETRACTED;
- retraction state = RETRACTED;
- a reason.

Retraction does not erase the historical claim or its evidence path.

## Uncertainty

ClaimGraph retains multiple uncertainty dimensions rather than collapsing them into one confidence score:

- aleatoric;
- model/parameter;
- structural/model-form;
- data coverage;
- provenance;
- dependency;
- measurement;
- temporal;
- adversarial;
- decision/consequence.

Use `UNKNOWN` when an estimate is not justified.

Unknown is not zero.

## Causal claims

ClaimGraph distinguishes:

- ASSOCIATION
- PREDICTIVE
- INTERVENTION
- MECHANISM_HYPOTHESIS
- CAUSAL_IDENTIFIED

A `CAUSAL_IDENTIFIED` claim requires experiment or causal-design support.

Correlation, graph structure, feature importance, repeated agreement, or high confidence is not enough.

## Authorization relevance

`authorization_relevance` may be:

- NONE
- ADVISORY
- REQUIRED_INPUT

This records how a separate governance/decision system may use the claim.

It does not grant authority.

## Non-DGAF portability example

`docs/research/fixtures/CLAIMGRAPH_SOFTWARE_INCIDENT_EXAMPLE.json` models a software incident:

- deployment timing supports an incident hypothesis;
- error telemetry supports it;
- post-rollback errors contradict a sole-cause interpretation;
- two supporting evidence nodes explicitly share a source root;
- the claim remains CHALLENGED and ASSOCIATION-level rather than being promoted to causal identification.

The same schema and validator are used without DGAF/PDMAL fields or a forked contract.

## Claim ceiling

A passing graph means only:

> The graph satisfies the declared ClaimGraph/Structural Epistemics structural contract and machine-decidable invariants.

It does not establish truth, independence, causal validity, authorization, certification, compliance, production readiness, or system-wide epistemic correctness.
