# PR #139 CI Execution Record

## Current status

CI EXECUTION / NON-AUTHORIZING

**Current confirmed PR #139 head:** `b7d1fe4e49f4e126b7033d3341e7d831e67dff28`

The v1 candidate contains the deterministic control-plane suite, TGL integration suite, adversarial contract suite, capability-boundary suite, and dedicated security/evidence workflows.

## Candidate binding

The authoritative engineering candidate is the exact PR head SHA reported by GitHub. Historical run results must not be relabeled as evidence for a later head.

## Historical diagnostic execution

An earlier dedicated v1 contract execution on a PR merge ref observed **32 passed / 3 failed**. The failures were diagnosed as contract-test mismatches: a stale side-effect inheritance expectation, a stale post-escalation assertion, and an abort-transition expectation inconsistent with the then-current lattice. The corresponding controls/tests were corrected.

An earlier PR #132 adversarial execution remains a separate historical signal: **41 passed / 2 failed** at the TGL → P-35 seam. The current consolidated implementation is in PR #139; the earlier result remains diagnostic provenance.

## Current exact-head evidence

For `7807d956…`, the dedicated `DGAF v1 Control-Plane Contract` run `33246694071` completed **SUCCESS**, with exact candidate checkout and pinned dependency setup passing and the deterministic control-plane/TGL/adversarial/capability-boundary suite passing **40/40**.

The current candidate later received documentation/governance reconciliation commits and a non-destructive merge commit incorporating current `main`, followed by a Herald-status regression correction. Fresh exact-head verification of the latest code-changing head remains required where that head changes implementation semantics.

## CI hardening

The dedicated workflow definition is configured to:

- check out `${{ github.event.pull_request.head.sha || github.sha }}`;
- assert `git rev-parse HEAD` exactly equals the expected candidate SHA;
- install pinned repository CI dependencies plus pinned pandas;
- execute core control-plane, TGL integration, adversarial, and capability-boundary suites.

## Deployment blocker

Vercel source identity remains a separate provenance gate under Issue #137. Green or rate-limited status contexts do not establish exact deployment-source identity by themselves.

## Interpretation

CI success, deployment readiness, deterministic fixtures, synthetic evaluator results, and documentation consistency are engineering evidence only. None constitutes PDMAL efficacy evidence, a new freeze, or pilot authorization.

## Current experimental state

PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0
