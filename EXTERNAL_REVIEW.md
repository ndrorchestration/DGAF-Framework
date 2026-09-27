# External Review

DGAF has two separate external-review lanes. Do not treat evidence from one lane
as satisfying the other by inheritance.

## 1. Governance-benchmark independent reproduction

Controller: GitHub Issue #1067.

Frozen review target:

`b5057bf836f67136c6030a81a604e5fd0d269076`

Expected deterministic review-bundle SHA-256:

`1a55c88c7e8536be67ea13e2ba0718fc8318cc938f0b3bf4e275be4961c4de48`

Start here:

- `docs/qa/GOVERNANCE_BENCHMARK_EXTERNAL_REVIEW_HANDOFF.md`
- `docs/qa/GOVERNANCE_BENCHMARK_HANDOFF_CANDIDATE_FREEZE_2026-09-26.md`
- `docs/qa/GOVERNANCE_BENCHMARK_EXTERNAL_REVIEW_RETURN_TEMPLATE.md`

The reviewer should independently clone this repository, check out the exact
frozen target, run the bounded contract tests, regenerate the deterministic
review bundle, retain evidence independently, and return a REPRODUCED, MISMATCH,
or BLOCKED result with the required identity/environment/disclosure fields.

A negative result is valid evidence. Preserve the first attempt rather than
silently rerunning after outcome inspection.

## 2. AOSS Stage-A external review

Controller: GitHub Issue #929.

Accepted handoff:

`docs/research/AOSS_V0_6_STAGE_A_INDEPENDENT_VALIDATION_HANDOFF.md`

This is a separate runtime-assurance review. Governance-benchmark reproduction
under #1067 does not satisfy #929 unless the returned evidence is separately
applicable and separately adjudicated against #929's requirements.

## Claim boundary

Neither reviewer preparation nor a successful same-system rehearsal establishes
any of the following:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
STATE_OF_THE_ART=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

A structurally valid external return becomes admissible evidence for later
adjudication. It does not self-promote the project into independent validation,
efficacy, SOTA status, certification, compliance, or High-Assurance.
