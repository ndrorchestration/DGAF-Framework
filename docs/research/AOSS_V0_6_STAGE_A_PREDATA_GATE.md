# AOSS v0.6 Stage A — Pre-Data Readiness Gate

**Controller:** #810  
**Current state:** NOT READY / FAIL-CLOSED  
**Outcome collection:** NOT AUTHORIZED BY THIS GATE

This gate converts the Stage-A pre-data checklist into a machine-checked readiness contract. It does not select missing scientific or operational values.

The accepted #859 apparatus remains the starting evidence state. Predicates established by accepted apparatus or frozen pre-data contracts may be marked `BOUND`. Every unresolved predicate must remain `PARTIAL`, `OPEN`, or `BLOCKED` and must state exactly what is missing.

The validator refuses a ready state while any required predicate is unresolved. Even if every predicate is eventually bound, the resulting status is only `READY_FOR_SEPARATE_AUTHORIZATION_REVIEW`; the readiness record itself can never authorize outcome collection, establish external validation, or increment scientific N.

## Current unresolved families

Exactly one required predicate remains unresolved:

- **comparator input derivation — BLOCKED:** the `AOSS_V0_5_OMR_FROZEN` decision rule is bound, but ACP telemetry does not yet have an accepted machine-bound derivation into `(O,M,R)`. Do not infer the dimensions from their names or reconstruct the mapping from outcomes.

## Frozen pre-data contracts

The following are now separately frozen and evidence-backed:

- external target identity, telemetry schema, observer/trust-domain boundary, and extraction-function/tolerance identity;
- numeric same-host freshness/calibration semantics;
- episode eligibility/exclusion and deterministic replay/repetition plan;
- per-class failure-injection ground truth;
- whole-study content-addressed replay receipt contract;
- finite-corpus descriptive analysis/multiplicity contract;
- practical-effect/portability adoption rule;
- prospective executable `AOSS_V0_6_STAGE_A_POLICY_V1` decision policy, explicitly not a recovered v0.5 implementation;
- primary, secondary, safety, falsification, and non-authority boundaries.

Stage A remains a finite preregistered purposive conformance corpus. Deterministic replays test stability and do not increase the denominator. No sampling CI, p-value, bootstrap, or population-effect inference is attached to the primary finite-corpus fraction. A zero decision-divergence result does not by itself fail bounded portability if all structural and safety criteria pass.

The whole-study replay receipt must bind the frozen AOSS decision-policy contract and the eventual comparator-input derivation contract by SHA-256 before a valid final receipt can exist.

CI intentionally executes:

```text
python scripts/validate_aoss_v0_6_stage_a_predata_readiness.py --assert-not-ready
```

A green result means the repository accurately preserves the fail-closed boundary. It does **not** authorize Stage-A outcome generation.
