# Assurance Profile v0 — Core Contract

Controller: #1183

## Status

Candidate reusable assurance profile extracted from AOSS semantics.

This profile is non-authorizing and non-certifying. It does not replace AOSS,
ACP, DGAF, Evidence Gate, Action Admission, or ClaimGraph.

## Six dimensions

1. Measurement / apparatus.
2. Runtime / source / environment binding.
3. Authorization / decision separation.
4. Custody / replay / integrity.
5. Readiness / preflight.
6. Trust / independence review.

Each dimension records:
- status;
- whether it is required;
- evidence references;
- optional limitation.

## Status vocabulary

- `PASS`
- `FAIL`
- `UNKNOWN`
- `NOT_APPLICABLE`

A required dimension may not be `NOT_APPLICABLE`.

A required dimension that is not `PASS` produces an unresolved blocker.

## Independence classes

- `SAME_SYSTEM`
- `INDEPENDENT_VERIFIED`
- `INDEPENDENT_UNVERIFIED`
- `UNKNOWN`

If trust/independence review is required, `UNKNOWN` and
`INDEPENDENT_UNVERIFIED` remain blockers.

`SAME_SYSTEM` is a valid classification. It does not become independent by
repetition.

## Receipt semantics

The evaluator returns:
- pass/fail for the declared profile;
- dimension statuses;
- unresolved blockers;
- deduplicated evidence references;
- independence classification;
- claim ceiling;
- `authorization_effect = NONE`;
- `certification_effect = NONE`.

## Interpretation

A PASS means only:

> All dimensions marked required by this exact profile input were recorded as
> PASS, and no required independence state remained unknown or unverified.

A PASS does not establish:
- High Assurance;
- production security or safety;
- independent validation unless independently sourced evidence is actually
  verified;
- scientific efficacy;
- certification or compliance;
- execution or mutation authority;
- deployment or release authority;
- product readiness or market demand.

## First portability sequence

1. Exercise the core against an ACP profile/configuration.
2. Exercise the same core against one materially unrelated system.
3. Keep target-specific differences in adapters/configuration.
4. Do not fork evaluator semantics by target.
