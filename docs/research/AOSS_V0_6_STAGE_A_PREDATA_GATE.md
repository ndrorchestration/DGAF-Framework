# AOSS v0.6 Stage A — Pre-Data Readiness Gate

**Controller:** #810  
**Current state:** NOT READY / FAIL-CLOSED  
**Outcome collection:** NOT AUTHORIZED BY THIS GATE

This gate converts the Stage-A pre-data checklist into a machine-checked readiness contract. It does not select missing scientific or operational values.

The accepted #859 apparatus is bound as the starting evidence state. Predicates already established by that apparatus or the frozen study document may be marked `BOUND`. Every unresolved predicate must remain `PARTIAL`, `OPEN`, or `BLOCKED` and must state exactly what is missing.

The validator refuses a ready state while any required predicate is unresolved. Even when every predicate is eventually bound, the resulting status is only `READY_FOR_SEPARATE_AUTHORIZATION_REVIEW`; the readiness record itself can never authorize outcome collection, establish external validation, or increment scientific N.

Current unresolved families include:

- owning AOSS decision policy or a new prospective v0.6 policy freeze;
- practical-effect/adoption rule;
- analysis/uncertainty/multiplicity;

The observer/trust-domain boundary, extraction-function/tolerance identity, whole-study artifact/hash/replay receipt, numeric freshness/calibration rule, episode eligibility/repetition plan, and per-class failure-injection ground truth are now separately frozen. Exact timestamp extraction remains distinct from freshness adjudication, and replay passes remain deterministic checks rather than independent observations.

CI intentionally executes:

```text
python scripts/validate_aoss_v0_6_stage_a_predata_readiness.py --assert-not-ready
```

A green result therefore means the repository is accurately fail-closed, not that Stage A may begin.
