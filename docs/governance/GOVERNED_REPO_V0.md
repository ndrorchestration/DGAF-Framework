# Governed Repo v0

Status: **candidate / non-mutating / promotion-eligibility only**

Tracked by issue #1178.

## Purpose

Governed Repo v0 is a pure decision layer for one question:

> Is this exact repository change, at this exact base/head state, supported by the required gates and upstream receipts to be eligible for canonical promotion?

It does **not** perform a merge, push, deployment, release, or other repository mutation.

## Core contract

Inputs:

- exact repository/change identity;
- expected and observed base/head identities;
- required gate policy;
- observed gate receipts;
- optional upstream decisions such as evidence, claim-scope, mutation-policy, or authority receipts.

Output:

- one machine-readable `PromotionReceipt`;
- stable reason code;
- exact base/head identities;
- checked, missing, failed, and nonterminal gates;
- upstream receipt references;
- explicit non-effects:
  - `merge_executed = false`
  - `mutation_executed = false`
  - `authorization_effect = NONE`

## Stable v0 reason codes

- `ELIGIBLE_FOR_PROMOTION`
- `INPUT_INVALID`
- `STALE_BASE`
- `HEAD_IDENTITY_MISMATCH`
- `REQUIRED_CHECK_MISSING`
- `REQUIRED_CHECK_NOT_TERMINAL`
- `REQUIRED_CHECK_FAILED`
- `EVIDENCE_INSUFFICIENT`
- `CLAIM_SCOPE_INVALID`
- `MUTATION_POLICY_BLOCKED`
- `AUTHORITY_UNRESOLVED`
- `LIFECYCLE_BLOCKED`
- `HOLD`

## Fail-closed behavior

Governed Repo v0 denies promotion eligibility when:

- required identities are absent or invalid;
- the observed base does not match the expected base;
- the observed head does not match the expected head;
- a required check is missing;
- a required check is not terminal;
- a required check failed;
- a required gate receipt is bound to another head/base;
- a required upstream receipt is absent or not accepted;
- lifecycle or explicit hold state blocks promotion.

Blocked, queued, cancelled, missing, or unreadable required checks are never represented as passes.

## Separation from other components

Governed Repo does not redefine:

- **Action Admission** authority semantics;
- **Evidence Gate** provenance/evidence admission semantics;
- **ClaimGraph** claim/evidence graph semantics.

It may consume bounded decisions from those components through generic `UpstreamDecision` inputs.

## Example

```python
from components.governed_repo import (
    ChangeIdentity,
    GateReceipt,
    GateRequirement,
    PromotionPolicy,
    assess_promotion,
)

receipt = assess_promotion(
    ChangeIdentity(
        repository="example/repo",
        change_id="pr-42",
        base_sha="abc",
        head_sha="def",
        observed_base_sha="abc",
        observed_head_sha="def",
        observed_at="2026-10-01T14:00:00Z",
    ),
    PromotionPolicy(
        required_gates=(
            GateRequirement(
                gate_id="ci",
                gate_class="quality",
                require_head_binding=True,
                require_base_binding=True,
            ),
        )
    ),
    (
        GateReceipt(
            gate_id="ci",
            status="completed",
            conclusion="success",
            observed_at="2026-10-01T14:01:00Z",
            head_sha="def",
            base_sha="abc",
        ),
    ),
)

assert receipt.eligible is True
assert receipt.merge_executed is False
```

## Portability boundary

This initial tranche is an in-repository core extraction only.

Reusable-product classification still requires:

1. DGAF adapter/conformance without weakening existing controls;
2. one materially different repository using the same core without a fork;
3. both positive and negative cases in that second repository;
4. installation/integration friction documented;
5. fresh exact-head CI on the candidate.

## Claim ceiling

A passing promotion receipt establishes only that the supplied inputs satisfy the declared Governed Repo v0 policy.

It does not establish:

- merge authority;
- successful merge or deployment;
- production security;
- complete GitHub branch-protection correctness;
- compliance/certification;
- independent validation;
- scientific efficacy;
- High-Assurance authorization;
- product-market fit.
