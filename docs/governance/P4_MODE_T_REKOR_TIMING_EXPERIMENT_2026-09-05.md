# P4 Mode T Controlled Rekor Timing Experiment — 2026-09-05

**Status:** APPARATUS IMPLEMENTED / NOT EXECUTED / PUBLIC-SIDE-EFFECT CONTROLLED  
**Issue:** #296  
**Parent timing work:** #293 / draft PR #294  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Implement the controlled synthetic timing apparatus needed to measure a candidate external transparency step for Mode T without silently creating public records during ordinary CI.

A successful keyless Sigstore submission creates an irreversible public transparency-log entry. Therefore this workflow is **manual-dispatch only** and this implementation tranche does not execute it.

## Frozen tool identity

```yaml
cosign_version: v3.1.3
cosign_linux_amd64_sha256: 4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71
oidc_issuer: https://token.actions.githubusercontent.com
```

The workflow downloads the exact Linux amd64 binary, recomputes SHA-256 before use, and fails unless the digest matches the frozen value.

## Execution controls

`.github/workflows/p4-mode-t-rekor-timing.yml` has only `workflow_dispatch` and requires two explicit inputs:

1. the exact 40-character commit SHA to execute;
2. `I_UNDERSTAND_PUBLIC_REKOR_ENTRY` before the public-signing job is eligible to run.

The apparatus-validation job has no OIDC permission. The public experiment job is separate, depends on successful apparatus validation, and receives `id-token: write` only because keyless Cosign needs a GitHub OIDC token when the signing command is actually invoked.

Before signing, the workflow verifies:

- event type is `workflow_dispatch`;
- requested evidence SHA is a full SHA and equals the dispatch `GITHUB_SHA`;
- checkout HEAD exactly equals that SHA;
- `GITHUB_RUN_ATTEMPT == 1`;
- the explicit public-side-effect confirmation is present;
- workflow/helper hashes are captured;
- the Cosign binary checksum matches the frozen digest.

A rerun after a failed or completed public attempt is rejected rather than silently generating a second transparency entry.

## Synthetic payload

The signed blob contains only repository/run identities and explicit non-authorizing controls. It asserts:

- `P4_MODE_T_SYNTHETIC_TIMING_NOT_AUTHORIZATION`;
- no empirical data collection;
- no protected material;
- no secret instantiation;
- no freeze;
- no pilot authorization;
- no authorization consumption;
- no analysis lock;
- no numeric W selection;
- empirical N=0.

No PDMAL observations, mapping, key, nonce, outcome, or efficacy claim is included.

## Timing and verification

`experiments/pdmal_pilot/mode_t_rekor_timing.py` uses a monotonic clock around:

1. `cosign sign-blob --bundle ... --yes`;
2. `cosign verify-blob` against the exact expected GitHub workflow certificate identity and GitHub Actions OIDC issuer.

The helper then parses the returned Sigstore bundle and fails unless at least one transparency-log entry contains a valid integrated time, non-negative log index, and inclusion proof or inclusion promise.

The evidence record binds:

- exact repository SHA;
- run ID and first-attempt identity;
- workflow reference/certificate identity;
- Cosign binary digest;
- synthetic blob digest;
- bundle digest;
- signing/submission latency;
- local bundle-verification latency;
- transparency log identity/index/integrated time where represented;
- explicit non-promoting scientific state.

A SHA-256 sidecar is written for the timing evidence record.

## Trust boundary

A verified Rekor/Sigstore bundle is candidate anti-deletion evidence, not infallible wall-clock truth. Log/operator, OIDC, certificate-authority, network, and runner assumptions remain part of the evidence boundary.

GitHub artifact retention is also deletable storage and is not treated as independent durable custody. The final P6 design may require an additional independently retained copy or another verification path.

## What this implementation does not do

The workflow has **not been dispatched** by this tranche. Therefore there is currently no timing result, no accepted ordinary-condition sample, no degraded-condition sample, and no basis to propose `W` from this implementation alone.

Even a future successful controlled run would not automatically select W. #293 still requires repetitions, distributional evidence, a separately documented safety-margin rule, and independent review before any numeric proposal can become eligible.

## Non-effects

Implementation or later execution of this synthetic apparatus does not establish Mode-T custody sufficiency, freeze, authorization, authorization consumption, analysis lock, P4/P7/P8/P9 closure, empirical efficacy, hosted-runner memory independence, or any increase in empirical N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
