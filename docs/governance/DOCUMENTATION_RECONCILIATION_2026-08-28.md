# Documentation Reconciliation — 2026-08-28

## Purpose

This reconciliation records the documentation changes required by the adversarial TGL review and PR #132 contract regression. It preserves historical evidence while preventing the current TGL remediation candidate from being mistaken for experimental apparatus verification.

## Current authoritative state

- `main` remains documentation/evidence lineage, not experimental apparatus identity.
- Experimental verification boundary remains `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`.
- PR #132 is **BLOCKED / DRAFT / UNMERGED**.
- The observed **41-pass / 2-fail** result is a substantive TGL/P-35 contract regression signal.
- PR #133 is the isolated remediation candidate.
- No new freeze exists.
- Pilot authorization is not granted.
- Empirical N remains 0.

## Reconciled living documents

The 2026-08-28 pass updated or established the following current surfaces:

- `README.md` — public-surface statement and current TGL remediation state.
- `docs/CURRENT_STATE.md` — authoritative current-state gate board and TGL/P-35 boundary.
- `docs/PROJECT_STATUS.md` — project gate board, remediation status, and closure sequence.
- `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` — PDMAL pre-authorization control boundary and TGL blocker.
- `docs/governance/TEST_EXECUTION_READINESS_2026-08-21.md` — current contract-suite blocker and required TGL coverage.
- `docs/governance/TGL_PR132_ADVERSARIAL_REVIEW_2026-08-28.md` — canonical adversarial findings and remediation boundary.

## TGL documentation rule

The TGL contract is documented as a control-plane contract rather than a utility-class convention. Documentation must distinguish:

- gate result from turn status;
- `SKIP` due to unwiring from `SKIP` due to dependency suppression or non-applicability;
- a sealed audit representation from a merely generated audit object;
- implementation availability from executed verification evidence;
- deployment readiness from authenticated runtime identity.

The established P-35 API is authoritative for compatibility until an independently governed architectural change explicitly supersedes it.

## Historical evidence policy

Historical documents are not rewritten merely to match current state. Their original claims and terminology may be retained when necessary for provenance, provided their scope is clear. Historical runtime, freeze, deployment, run, and acceptance records cannot be transferred to PR #133 or a later candidate without explicit re-verification and rebinding.

## Governance boundary

Documentation updates are non-authorizing. No documentation commit, PR, CI result, deployment readiness state, or regression-suite result may create a freeze, authorize a pilot, unblind data, or increase empirical N.

## Completion criterion

This reconciliation is complete for the current TGL review when current-state surfaces agree that #132 is blocked, #133 is remediation-only, the TGL/P-35 contract is not yet closed, and the experimental boundary remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N = 0.
