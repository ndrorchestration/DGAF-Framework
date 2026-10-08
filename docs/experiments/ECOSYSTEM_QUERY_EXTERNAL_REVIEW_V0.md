# Experiment 1 External Review Packet V0

Status: **external human measurement protocol**

Controller: GitHub issue #1329  
Experiment controller: GitHub issue #1275

Packet creation source:

```text
DGAF_MAIN_AT_PACKET_CREATION=7e591bd4042fac00b53208a10400165b96bb9c31
```

The reviewer must record the exact DGAF commit actually evaluated.

The evidence record must also record the exact accepted packet commit supplied by controller #1329. The packet creation source above is not the packet acceptance identity; do not treat it as one. If protected `main` advances, do not silently substitute a later commit without recording it.

## Purpose

Evaluate whether the queryable ecosystem-state approach helps an unfamiliar human reconstruct current evidence/state boundaries with less manual work and fewer ambiguities, without turning query output into a competing source of truth.

This packet does **not** contain expected answers.

## Reviewer eligibility

The reviewer should not be:

- the implementation author;
- someone who built the evaluated query/adapters;
- ChatGPT or same-context automation;
- a reviewer coached through expected answers;
- a reviewer relying on unpublished author explanations.

Record coarse background and conflicts in the evidence record. Public attribution is optional.

## Public-material rule

Use public repository material and documented tools only.

Do not request private Notion access, unpublished expected answers, or implementation-author interpretation during the timed task.

If a question cannot be answered from the permitted material, record `UNANSWERABLE_FROM_PERMITTED_MATERIAL`. Do not guess.

## Setup

1. Clone `ndrorchestration/DGAF-Framework`.
2. Checkout and record the exact commit under review.
3. Record environment and Python version.
4. Inspect public/current repository documentation and tool `--help` output as needed.
5. Start the human-workload timer before beginning the eight questions.

The reviewer may run documented read-only query/adaptor commands. A non-zero exit from a fail-closed query is evidence to interpret, not permission to rewrite state.

## Eight frozen questions

Answer each independently and record sources used.

1. Which public-facing claims lack direct supporting evidence?
2. Which Tektite projections depend on capabilities not established?
3. Which artifacts still describe superseded blockers or architecture?
4. Which active controls lack executable tests or retained verification?
5. Which claims rely only on internally produced evidence?
6. Which execution receipts can be mistaken for follow-on authority?
7. Which transitions require fresh adjudication?
8. Which Notion records materially disagree with current repository state?

Allowed answer states:

- `ANSWERED`
- `PARTIAL`
- `UNANSWERABLE_FROM_PERMITTED_MATERIAL`
- `AMBIGUOUS_CONFLICTING_SOURCES`

For every question record:

- answer state;
- answer in the reviewer's own words;
- public source paths/URLs consulted;
- manual cross-surface lookups required;
- ambiguities or contradictions;
- any query output that appeared to overstate currentness, evidence, authority, or validation.

## Required falsification attempts

Actively look for at least these failure modes:

- stale source/pointer identities;
- historical records presented as current;
- evidence labels that imply more than their source supports;
- `EXTERNAL_SOURCE` mistaken for independent validation;
- direct test-reference heuristics mistaken for coverage;
- repository-tip equality mistaken for semantic correctness;
- receipt existence mistaken for follow-on authority;
- query output acting as an undeclared new source of truth.

Negative findings are valid results.

## Human workload metric

Stop the timer after the reviewer has answered or explicitly declined all eight questions and written a bounded conclusion.

Record actual or reviewer-estimated human minutes.

Do **not** derive minutes from:

- GitHub timestamps;
- chat timestamps;
- CI runtime;
- agent runtime;
- tool-call counts.

## Artifact-review metric

Review the material Experiment 1 outputs actually used and classify each as one of:

- `ACCEPTED_NO_SUBSTANTIVE_CORRECTION`
- `ACCEPTED_WITH_SUBSTANTIVE_CORRECTION`
- `REJECTED_REWORKED`
- `INCONCLUSIVE`

A substantive correction changes meaning, scope, evidence interpretation, currentness, authority, or a material answer. Formatting/lint/transport-only repairs should be recorded separately and do not count as substantive corrections.

Human-review survival rate is computed only when at least one artifact is reviewed:

```text
accepted_without_substantive_correction / artifacts_reviewed
```

## Assistance log

Record every intervention or clarification received during the review.

If unpublished author coaching or expected-answer disclosure occurs, record it and consider `PROTOCOL_INVALID`.

## Final dispositions

Choose one:

- `SUPPORTED_FOR_CONTINUED_EXPERIMENTATION`
- `PARTIALLY_SUPPORTED`
- `INCONCLUSIVE`
- `REQUIRES_REDESIGN`
- `FALSIFIED_FOR_CURRENT_APPROACH`
- `PROTOCOL_INVALID`

Explain the disposition in the reviewer's own words.

## Claim ceiling

A successful review supports at most continued development of the queryable ecosystem-state approach.

It does not establish:

- independent scientific validation of DGAF;
- canonical DGAF efficacy;
- scientific-N promotion;
- High-Assurance authorization;
- production security;
- generalized usability;
- product-market fit.

Fixed boundaries:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

Use `docs/experiments/ECOSYSTEM_QUERY_EXTERNAL_REVIEW_RECORD_V0.json` as the blank evidence-record template.
