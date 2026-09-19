# AOSS v0.6 Stage A — Analysis and Portability-Adoption Contract

**Controller:** #810  
**Status:** FROZEN PRE-DATA CONTRACT · NO OUTCOMES  
**Scientific effect:** NONE

This contract freezes how Stage-A results will be summarized and how a bounded portability conclusion may later be classified. It deliberately avoids pseudo-inference from a small, purposively constructed deterministic fixture corpus.

## Analysis population

Stage A is a **finite preregistered conformance corpus**, not a random sample from a statistical population.

The unit of analysis is one unique eligible episode. Deterministic replay executions test stability; they are not independent observations and never increase the denominator.

## Primary estimator

The primary endpoint remains:

`AOSS decision != frozen OMR comparator decision`

The estimator is the exact finite-corpus fraction:

`divergent eligible unique episodes / eligible unique episodes`

The report must include the numerator, denominator, exact fraction, episode class, reconstructed state, missing/adapter-derived observables, and any `UNMEASURED` or `INCONCLUSIVE` state.

No sampling confidence interval, p-value, bootstrap, or null-hypothesis test is attached to this finite purposive corpus. Doing so would imply a sampling model that the frozen Stage-A design does not provide.

## Uncertainty and multiplicity

Sampling uncertainty is not modeled. Epistemic uncertainty is retained explicitly through typed missing, stale, conflicting, and inconclusive states.

There is one preregistered descriptive primary endpoint and zero inferential tests. Secondary endpoints and failure-class-specific summaries are descriptive. Post-hoc subgroup work is exploratory only. Any future inferential hypothesis requires a new preregistration before data inspection.

No outcome-aware exclusion is permitted. Infrastructure or protocol failure is recorded as invalid/inconclusive rather than silently dropped.

## Practical effect and adoption

There is **no minimum decision-divergence threshold** for the Stage-A portability claim.

This follows directly from the frozen falsification boundary: a null decision-divergence result is not a safety or portability failure. Stage A asks whether the unchanged observer can ingest, reconstruct, preserve missingness/provenance distinctions, replay deterministically, and remain fail-closed against the exact ACP target.

A later `BOUNDED_ACP_PORTABILITY_SUPPORTED` classification therefore requires the complete structural, replay, identity, and zero-safety-violation criteria in the machine-readable adoption contract. Any frozen falsification/safety failure yields `BOUNDED_ACP_PORTABILITY_NOT_SUPPORTED`. Missing required evidence or an invalid protocol yields `INCONCLUSIVE`.

Even a supported result is limited to bounded cross-repository observer portability against the exact ACP commit. It is not AOSS superiority, production-like external validation, production readiness, independent validation, DGAF/PDMAL efficacy, or High-Assurance authorization.

## Machine-readable contracts

- `registry/aoss_v0_6_stage_a_analysis_multiplicity_contract_v1.json`
- `registry/aoss_v0_6_stage_a_practical_effect_adoption_rule_v1.json`
