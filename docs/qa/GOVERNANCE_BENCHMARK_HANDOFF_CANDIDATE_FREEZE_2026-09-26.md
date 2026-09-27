# Governance Benchmark Handoff Candidate Freeze Receipt

> **Status:** IN-HOUSE VALIDATED HANDOFF CANDIDATE / NON-AUTHORIZING  
> **Established:** 2026-09-26  
> **Effect on scientific state:** NONE

## Frozen candidate

Repository commit:

`b5057bf836f67136c6030a81a604e5fd0d269076`

Deterministic review bundle:

`DGAF-governance-benchmark-review-b5057bf8.zip`

Bundle SHA-256:

`1a55c88c7e8536be67ea13e2ba0718fc8318cc938f0b3bf4e275be4961c4de48`

Bundle size: `8186` bytes.

## In-house verification evidence

For the exact frozen commit above, all observed repository CI lanes completed
successfully, including Python Tests & Quality Checks, Governance CI, DGAF
Regression Suite, Truth Layer Tests/Validation, Epistemic Evidence Validation,
both Doc Lint lanes, Control-State Consistency, HEAD Binding, Full Repository
Coverage Audit, Ecosystem Registry Audit, IP Hygiene Sweep, PDMAL Harness
Validation, PDMAL Pre-Freeze Runner Validation, PPTL CI, Claim Hygiene,
Vocabulary Translation Matrix, Propagation Consistency, and Critical PR Lane
Custody.

The bounded local verification suite also established reproducible review-bundle
construction before this receipt was created.

## Reviewer reproduction contract

An external reviewer should:

1. independently clone the repository;
2. check out the exact frozen commit;
3. run the benchmark contract tests;
4. regenerate the review bundle with
   `experiments/governance_benchmark/package_review_bundle.py`;
5. compare the regenerated ZIP SHA-256 with the frozen candidate digest;
6. report their environment, commands, results, and discrepancies independently.

A digest mismatch is evidence of a reproduction difference and must be
investigated; it is not automatically evidence that DGAF itself is incorrect.

## Non-effects

This receipt does **not** establish:

- independent validation;
- canonical DGAF efficacy;
- production safety or certification;
- regulatory compliance;
- scientific-N increment;
- state-of-the-art status;
- High-Assurance authorization.

Controlling state remains:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
STATE_OF_THE_ART=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

The purpose of this receipt is to prevent the external-review target from
silently drifting after in-house verification.
