# AOSS v0.6 Stage A — Pre-Data Readiness Gate

**Controller:** #810  
**Current candidate state:** READY FOR SEPARATE AUTHORIZATION REVIEW  
**Outcome collection:** NOT AUTHORIZED BY THIS GATE

This gate converts the Stage-A pre-data checklist into a machine-checked readiness contract. It cannot authorize outcome collection, establish external validation, or increment scientific N.

## Comparator amendment boundary

The historical `AOSS_V0_5_OMR_FROZEN` decision rule remains documented, but O/M/R semantic definitions and an ACP→O/M/R extraction contract were not recoverable before Stage-A outcome collection. The historical `(3,1,1.0)` fixture projection is not treated as an extraction rule.

Rather than invent O/M/R, Stage A now carries an explicit prospective pre-data protocol amendment:

- amendment: `AOSS_V0_6_STAGE_A_PRIMARY_COMPARATOR_AMENDMENT_V1`;
- primary comparator: `AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1`;
- executable: `scripts/aoss_v0_6_stage_a_acp_direct_baseline.py`;
- inputs: exact ACP manifest identity plus source-native event kind only;
- richer AOSS observables and injected ground-truth labels are not comparator inputs.

The original OMR gap record is retained as historical evidence of the unrecovered derivation.

## Bound pre-data contracts

All required pre-data predicates in this candidate are evidence-backed, including:

- exact external target identity and telemetry schema;
- external read-only observer/trust-domain boundary;
- extraction functions, units, and tolerances;
- numeric same-host freshness/calibration semantics;
- prospective source-native primary comparator and exact machine derivation;
- prospective executable `AOSS_V0_6_STAGE_A_POLICY_V1` decision policy;
- primary, secondary, safety, and falsification endpoints;
- episode eligibility/exclusion and deterministic replay/repetition plan;
- per-class failure-injection ground truth;
- finite-corpus descriptive analysis/multiplicity contract;
- practical-effect/portability adoption rule;
- whole-study content-addressed replay receipt contract;
- authorization/non-authority boundary.

Stage A remains a finite preregistered purposive conformance corpus. Deterministic replays test stability and do not increase the denominator. No sampling CI, p-value, bootstrap, or population-effect inference is attached to the primary finite-corpus fraction.

## State semantics

`READY_FOR_SEPARATE_AUTHORIZATION_REVIEW` means only that the pre-data contract is complete enough for a separate authorization decision. It does **not** mean:

- outcome collection is authorized;
- external validation is established;
- AOSS is superior to the comparator;
- DGAF or PDMAL efficacy is established;
- scientific N has increased;
- Track A Epoch 002 is reopened.

CI must validate this candidate with:

```text
python scripts/validate_aoss_v0_6_stage_a_predata_readiness.py --assert-ready
```

A green result is readiness evidence only. A separate explicit authorization record is required before Stage-A outcome generation.
