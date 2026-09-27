# Provenance Custody — Matched-Checks Falsification Result

> **Evidence class:** SYNTHETIC PROVENANCE FALSIFICATION EVIDENCE  
> **Scope:** merged DGAF reference transaction receipt/audit chain  
> **Scientific effect:** NONE

## Question

Does DGAF retain a unique provenance-custody advantage when a conventional
stateful policy implementation is allowed the same ordinary schema and
cross-link consistency checks?

## Bound DGAF implementation

The benchmark generates a real bounded transaction through the merged
`run_reference_transaction(...)` implementation and validates the resulting:

- action digest;
- execution receipt;
- capability audit event;
- authorization linkage;
- workflow/invocation linkage;
- adapter/executor identity;
- provider-receipt evidence binding.

## Fairness constraint

The conventional comparator is allowed the same ordinary schema validation and
cross-link consistency checks. It is not intentionally deprived of provenance
state merely to create a DGAF advantage.

## Mutation matrix

The benchmark mutates:

1. action digest;
2. authorization ID;
3. workflow ID;
4. invocation ID;
5. capability ID;
6. adapter identity;
7. executor identity;
8. provider-receipt ID.

## Result

Across all eight mutations:

- C3 detected: **8/8**;
- DGAF detected: **8/8**;
- detection parity: **8/8**;
- operator review count: **8 for both**;
- differences: **0**.

Observed outcome:

`NO_UNIQUE_PROVENANCE_CUSTODY_ADVANTAGE_IN_MATCHED_CHECKS`

This weakens any claim that these bounded receipt/audit cross-link protections
are inherently unique to DGAF when ordinary policy tooling is allowed
equivalent custody checks.

## What remains open

This does not measure:

- durable evidence storage;
- independent custody;
- cross-system append-only guarantees;
- distributed tamper resistance;
- key management;
- cross-provider clock/order ambiguity;
- actual operator time or cognitive burden;
- external reviewer reproducibility.

Those remain better candidates for discovering a genuine architectural
difference.

## Claim ceiling

Unchanged:

- `SCIENTIFIC_N_INCREMENT=0`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `STATE_OF_THE_ART=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`
