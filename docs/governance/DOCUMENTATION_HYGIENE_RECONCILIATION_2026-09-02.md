---
status: ACTIVE
scope: documentation hygiene
verified: 2026-09-02
current_control_ref: main
active_remediation_pr: 188
active_remediation_head: d83ea74c0f7ef7dd3e39a25345d6b201770a370c
active_pre_freeze_run: 33590352168
active_pre_freeze_artifact: 9831586822
---
# Documentation Hygiene Reconciliation — 2026-09-02

## Purpose

Maintain the repository's control-plane documentation after the P-35 remediation advanced and the exact-current-head pre-freeze runner completed successfully.

The earlier state of this document named `61f1be82…` and recorded the pre-freeze runner as unverified. That was correct for the earlier snapshot but is superseded by the verification recorded below.

## Corrections applied

1. **Current PR head corrected.** PR #188 / `remediation/p35-premise-hook-2026-09-01` is currently at `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`.
2. **Prior remediation evidence remains historical.** Evidence associated with `cf84ca30…` and `61f1be82…` remains valid only for those exact SHAs and is not current-head evidence.
3. **Pre-freeze runner verification completed.** Run `33590352168` executed against exact head `d83ea74…` and passed checkout identity, full hash-locked dependency installation, the full contract suite including `test_run_pilot_p35.py`, contract-mode execution, pilot-mode fail-closed verification without freeze/authorization, artifact integrity validation, and PRE-FREEZE manifest upload.
4. **Manifest custody recorded.** Artifact `9831586822` was uploaded from run `33590352168`; workflow artifact digest is `sha256:dedacba56b8430fd995c4230e52fe208d2380f5e5015fa3816073cda3e9d774e`.
5. **P-35 remediation status corrected.** The premise-hook injection path and runner boundary are now verified at engineering/pre-freeze scope. The additional `d83ea74…` correction preserves the sealed KILL audit on premise violation instead of re-raising and discarding it.
6. **Completion-candidate evidence remains exact-scoped.** P3/P4/P5/P6/P9 evidence for `a43219b4ed91fff8615f6c655ab3d17ca871fc29` remains historical candidate evidence and is not transferred to PR #188 or a successor.
7. **Vercel status distinction preserved.** Current deployment-health evidence is not treated as experimental or authorization evidence.
8. **Governance boundary preserved.** Documentation and engineering verification do not create freeze, authorization, unblinding, or empirical execution.

## Current authoritative posture

- Current control-plane documentation: `main`.
- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Current runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`.
- Controlled completion candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.
- Active P-35 remediation: PR #188, current head `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`.
- Pre-freeze runner: **VERIFIED ON REMEDIATION HEAD** via run `33590352168`; manifest artifact `9831586822`.
- P8: remains **OPEN / FAIL-CLOSED** because the verified remediation head is not yet a selected experimental candidate and the full current-cycle candidate evidence chain is not complete.
- Freeze: not established.
- Authorization: not granted.
- Empirical N: 0.

## Required next evidence

1. Review/closure of PR #188 without treating engineering remediation as experimental authorization.
2. Selection of a new exact experimental candidate after remediation.
3. Fresh candidate-bound P3–P9 and affected P2/P6a verification.
4. Exact freeze binding, independent verification, and explicit pilot authorization before any empirical execution.

This record is documentation hygiene only and is non-authorizing.
