# DGAF Post-Merge Mainline Canary v1

## Purpose

DGAF Post-Merge Mainline Canary v1 is a deterministic engineering check for the exact revision that has landed on protected `main`.

It answers one bounded question:

> Did this exact mainline revision preserve the minimal governed control path and the repository's canonical control-state reconciliation immediately after merge?

This contract composes existing checks. It does not redefine them.

Review-surface predecessor: PR #1077 merged to `main` as `f51c318929fccef7480fa84ae74c10ab6361e089`. This records only repository lineage; it does not add authority or empirical evidence.

## Required checks

| Gate | Source | Pass condition |
|---|---|---|
| `CANARY_HEAD` | Git checkout identity | Checked-out commit equals the pushed `main` revision. |
| `CANARY_SMOKE` | DGAF Smoke Contract v1 | The embedded smoke result is `PASS` and is bound to the same revision. |
| `CANARY_CONTROL_STATE` | `validate_control_state_head.py` | Existing control-state reconciliation rules pass for the push predecessor and resulting HEAD. |

The canary is `PASS` only when all three gates pass.

## Trigger semantics

The canonical CI workflow runs on every push to `main`, without a path filter.

That makes this a post-merge/mainline check rather than another pull-request smoke variant.

## Evidence semantics

The canary artifact records:

- exact mainline revision;
- push predecessor;
- the embedded Smoke v1 result;
- control-state reconciliation outcome and diagnostic output;
- overall `PASS` / `FAIL`;
- explicit claim ceilings.

A missing artifact is `NOT_OBSERVED`, never an implicit pass.

## Claim ceiling

A passing canary establishes only bounded mainline engineering verification for the exact revision.

It does not establish deployment health, production readiness, independent validation, scientific efficacy, scientific-N promotion, regulatory compliance, SOTA status, or High-Assurance authorization.

The following boundary is mandatory:

```text
SCIENTIFIC_N_INCREMENT=0
AUTHORIZATION_EFFECT=NONE
DEPLOYMENT_HEALTH=NOT_ESTABLISHED
PRODUCTION_READINESS=NOT_ESTABLISHED
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```
