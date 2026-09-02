---
status: CLOSED
scope: documentation hygiene
verified: 2026-09-02
current_control_ref: main
active_remediation_pr: 188
active_remediation_head: 61f1be8233a30afd7c155851eba16fb4084ec465
---
# Documentation Hygiene Reconciliation — 2026-09-02

## Purpose

Reconcile documentation after the P-35 remediation branch advanced beyond the previously audited remediation head.

## Corrections applied

1. **Current PR head corrected.** PR #188 / `remediation/p35-premise-hook-2026-09-01` is currently at `61f1be8233a30afd7c155851eba16fb4084ec465`.
2. **Prior remediation evidence downgraded to historical scope.** Fresh CI evidence previously associated with `cf84ca30cf34dce406ba80ab624ff24e38b181d3` remains valid for that exact SHA but is not current-head evidence.
3. **Pre-freeze runner status corrected.** The workflow `.github/workflows/pdmal-pre-freeze-runner.yml` is present and includes `test_run_pilot_p35.py`, but no successful exact-current-head pre-freeze execution/manifest is established by this audit.
4. **Completion-candidate evidence retained at exact scope.** P3/P4/P5/P6/P9 evidence for `a43219b4ed91fff8615f6c655ab3d17ca871fc29` remains historical candidate evidence and is not transferred to PR #188 or a successor.
5. **Vercel failure classified correctly.** The current remediation commit's Vercel failure is explicitly a deployment-rate-limit condition, not a P-35 code failure.
6. **Governance boundary preserved.** Documentation changes do not create freeze, authorization, unblinding, or empirical execution.

## Current authoritative posture

- Current control-plane documentation: `main`.
- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Current runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`.
- Controlled completion candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.
- Active P-35 remediation: PR #188, current head `61f1be8233a30afd7c155851eba16fb4084ec465`.
- Pre-freeze runner: implemented, exact-current-head execution unverified.
- Freeze: not established.
- Authorization: not granted.
- Empirical N: 0.

## Required next evidence

1. Exact-current-head pre-freeze runner success plus uploaded `PRE-FREEZE` manifest.
2. Review/closure of PR #188 without treating engineering remediation as experimental authorization.
3. Selection of a new exact experimental candidate after remediation.
4. Fresh candidate-bound P3–P9 and affected P2/P6a verification.

This record is documentation hygiene only and is non-authorizing.
