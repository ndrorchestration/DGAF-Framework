# Documentation Reconciliation — 2026-08-28

## Purpose

This reconciliation records the documentation changes required by the adversarial TGL review and subsequent DGAF v1 control-plane integration. It preserves historical evidence while preventing historical remediation records or generic engineering verification from being mistaken for current experimental apparatus verification.

## Current authoritative state

- `main` remains documentation/evidence lineage, not experimental apparatus identity.
- Experimental verification boundary remains `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` until a separately governed candidate transition is created.
- PR #132 and PR #133 remain historical diagnostic/remediation records.
- PR #134 is the current-main TGL/P-35 remediation lane; exact-head validation remains a prerequisite to candidate rebinding.
- PR #136 is a separate generic DGAF v1 control-plane engineering candidate; its dedicated deterministic contract lane is verified, but it is non-authorizing and not experimental evidence.
- No new freeze exists.
- Pilot authorization is not granted.
- Empirical N remains 0.

## Reconciled living documents

The current pass updates or establishes agreement across the following surfaces:

- `README.md` — public-surface statement and governance boundary.
- `docs/CURRENT_STATE.md` — authoritative current-state gate board and TGL/v1 boundary.
- `docs/PROJECT_STATUS.md` — project gate board, current remediation status, and closure sequence.
- `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` — PDMAL pre-authorization control boundary.
- `docs/governance/P8_ANALYSIS_LOCK.md` — P8 candidate binding and closure requirements.
- `docs/governance/CANDIDATE_BOUNDARY_BINDING_2026-08-28.md` — candidate identity and non-authorizing binding rules.
- `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md` — v1 control-plane boundary, concurrency, provenance, and adapter obligations.

## TGL documentation rule

The TGL contract is documented as a control-plane contract rather than a utility-class convention. Documentation must distinguish:

- gate result from turn status;
- `SKIP` due to unwiring from `SKIP` due to dependency suppression or non-applicability;
- a sealed audit representation from a merely generated audit object;
- implementation availability from executed verification evidence;
- deployment readiness from authenticated runtime identity.

The established P-35 API is authoritative for compatibility until an independently governed architectural change explicitly supersedes it.

## DGAF v1 documentation rule

The generic control plane must remain distinct from experimental authority. In particular:

- `COMMIT_READY` is not execution;
- `CommitGate` authorization is not inferred from model output or controller state;
- control-plane CI is not PDMAL experimental evidence;
- active concurrency is distinct from node counts and bounded across recursive lineage;
- branch-retention contracts do not by themselves prove adapter-level durable persistence;
- semantic diversity, consensus, topology, and harmonic/geometric motifs are not proof of independent evidence;
- changes to an executable experimental adapter require candidate rebinding and affected-predicate re-verification.

## Historical evidence policy

Historical documents are not rewritten merely to match current state. Their original claims and terminology may be retained when necessary for provenance, provided their scope is clear. Historical runtime, freeze, deployment, run, and acceptance records cannot be transferred to a later candidate without explicit re-verification and rebinding.

## Governance boundary

Documentation updates are non-authorizing. No documentation commit, PR, CI result, deployment readiness state, regression-suite result, or generic control-plane verification may create a freeze, authorize a pilot, unblind data, or increase empirical N.

## Completion criterion

This reconciliation is complete for the current TGL/v1 documentation pass when current-state surfaces agree that PRs #132/#133 are historical, PR #134 is the current-main TGL remediation lane, PR #136 is generic non-authorizing control-plane infrastructure, the experimental boundary remains candidate-scoped at `ac8ea267…`, and the experimental state remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N = 0.
