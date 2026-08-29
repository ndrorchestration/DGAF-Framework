# PR #139 CI Execution Record

## Current status

CI EXECUTION / NON-AUTHORIZING

**Current confirmed PR #139 head:** `2df8c0601d83488a305f211f510953ea81edcb01`

The v1 candidate contains the deterministic control-plane suite, TGL integration suite, adversarial contract suite, capability-boundary suite, and dedicated security/evidence workflows.

## Candidate binding

The authoritative engineering candidate is the exact PR head SHA reported by GitHub. Historical run results must not be relabeled as evidence for a later head.

## Historical diagnostic execution

An earlier dedicated v1 contract execution on a PR merge ref observed **32 passed / 3 failed**. The failures were diagnosed as contract-test mismatches: a stale side-effect inheritance expectation, a stale post-escalation assertion, and an abort-transition expectation inconsistent with the then-current lattice. The corresponding controls/tests were corrected.

An earlier PR #132 adversarial execution remains a separate historical signal: **41 passed / 2 failed** at the TGL → P-35 seam. The current consolidated implementation is in PR #139; the earlier result remains diagnostic provenance.

## Current exact-head evidence

For `2df8c060…`, exact-head CodeQL completed successfully and exact-head Truth Layer Validation completed successfully. Other repository-wide checks may be triggered independently.

The dedicated `DGAF v1 Control-Plane Contract` check currently has **no exact-head check-run record** for `2df8c060…`. Therefore the consolidated v1 control-plane contract is **not currently verified** on the authoritative head.

## CI hardening

The dedicated workflow definition is configured to:

- check out `${{ github.event.pull_request.head.sha || github.sha }}`;
- assert `git rev-parse HEAD` exactly equals the expected candidate SHA;
- install pinned repository CI dependencies plus pinned pandas;
- execute core control-plane, TGL integration, adversarial, and capability-boundary suites.

## Deployment blocker

GitHub's aggregate status includes a Vercel failure associated with deployment quota/rate-limit conditions. A same-branch READY preview has been observed, but no READY deployment has been accepted as exact-current-main production identity without source-SHA matching. Issue #137 remains the canonical deployment/source-binding gate.

## Interpretation

CI success, deployment readiness, deterministic fixtures, synthetic evaluator results, and documentation consistency are engineering evidence only. None constitutes PDMAL efficacy evidence, a new freeze, or pilot authorization.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**