# AOSS v0.6 Stage A — Pre-Data Readiness Gate

**Controller:** #810  
**Current state:** NOT READY / FAIL-CLOSED  
**Outcome collection:** NOT AUTHORIZED BY THIS GATE

This gate converts the Stage-A pre-data checklist into a machine-checked readiness contract. It does not select missing scientific or operational values.

The accepted #859 apparatus is bound as the starting evidence state. Predicates already established by that apparatus or the frozen study document may be marked `BOUND`. Every unresolved predicate must remain `PARTIAL`, `OPEN`, or `BLOCKED` and must state exactly what is missing.

The validator refuses a ready state while any required predicate is unresolved. Even when every predicate is eventually bound, the resulting status is only `READY_FOR_SEPARATE_AUTHORIZATION_REVIEW`; the readiness record itself can never authorize outcome collection, establish external validation, or increment scientific N.

Current unresolved families include:

- numeric freshness and clock calibration;
- owning AOSS decision policy or a new prospective v0.6 policy freeze;
- episode eligibility/exclusion;
- repetitions/seeds;
- per-class ground-truth expectations;

The observer/trust-domain boundary, extraction-function/tolerance identity, whole-study artifact/hash/replay receipt, finite-corpus analysis/multiplicity contract, and practical-effect/adoption rule are now separately frozen. Exact timestamp extraction remains distinct from freshness adjudication.

Stage A analysis is descriptive over a finite purposive conformance corpus: deterministic replays do not increase the denominator, no sampling CI/p-value/bootstrap is attached, and secondary/post-hoc analyses cannot be relabeled confirmatory. Portability has no minimum decision-divergence threshold; a zero-divergence result does not fail portability when the structural and safety criteria pass.

CI intentionally executes:

```text
python scripts/validate_aoss_v0_6_stage_a_predata_readiness.py --assert-not-ready
```

A green result therefore means the repository is accurately fail-closed, not that Stage A may begin.
