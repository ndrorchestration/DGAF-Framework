# Solo P-30 Explicit Variant Empirical Epoch 003 — Preregistration

## Status

`PREREGISTERED / BLINDED_SOLO_EMPIRICAL_VARIANT / NOT_CANONICAL_DGAF / NOT_YET_EXECUTED`

This epoch is prospective. It does not alter, erase, relabel, or pool Solo final experiment 001 or non-empirical diagnostic Epoch 002.

## Why this is a separate treatment variant

Experiment 001 exposed an apparatus defect: the DGAF condition left the P-30 Apogee confidence substrate unbound, causing deterministic `confidence=0.0 -> D -> KILL` termination. Diagnostic Epoch 002 then demonstrated that the remaining DGAF treatment executes across 90/90 engineering trials when P-30 receives the fixed synthetic minimum-passing fixture `SYNTHETIC_MINIMUM_PASSING_P30_FIXTURE_V1` at confidence exactly `0.45`.

Issue #165 designates P-30 grade semantics and `D -> KILL`, but it does not designate a canonical source or calibration procedure for Apogee confidence. Therefore this epoch does **not** claim to test canonical Apogee-calibrated DGAF. It tests the explicitly named variant **DGAF-P30-EXPLICIT-0.45**.

## Treatment identity

- Experiment ID: `PDMAL-SOLO-P30-EXPLICIT-V1`
- Variant scope: `DGAF-P30-EXPLICIT-0.45`
- P-30 binding ID: `SYNTHETIC_MINIMUM_PASSING_P30_FIXTURE_V1`
- Binding kind: `SYNTHETIC_MINIMUM_PASSING_FIXTURE`
- Confidence: exactly `0.45`
- Real/calibrated Apogee confidence: **NO**
- Canonical DGAF efficacy claim permitted: **NO**
- High-Assurance claim permitted: **NO**

The fixture must not be tuned, optimized, or changed after this preregistration. Any change requires a new epoch.

## Experimental matrix

- Protocol version: `0.7.6`
- Conditions: canonical four (`null`, `simple`, `static`, `dgaf`)
- Topologies: canonical five
- Failure counts: canonical nine (`0,1,2,3,4,5,6,8,10`)
- Fresh seed range: `20260901` through `20260950` inclusive
- Seeds: `50`
- Cells per seed: `180`
- Total blinded observations: `9,000`
- Seeds `20260819` through `20260868` from experiment 001 are not reused.

## Collection controls

1. The run executes only from an exact frozen 40-character commit SHA.
2. The run commit must change exactly one authorization-request file.
3. A fresh protected blinding key controls condition labels and trial order.
4. The collection workflow must not inspect or aggregate outcome fields.
5. Each seed artifact receives a SHA-256 sidecar and durable retained copy.
6. The dataset is structurally verified and locked while blinded before any key release.
7. The key is retained separately under same-system GitHub Actions artifact custody. This is recoverable Solo custody, **not independent custody**.
8. Unblinding is prohibited until a separate post-lock authorization is recorded.

## Locked primary analysis

The primary analysis remains the pre-existing paired-seed FFCR contrast used before this epoch was collected:

- Primary comparison: `DGAF-P30-EXPLICIT-0.45 - null`
- Unit of analysis: seed
- Point estimate: mean paired seed difference
- Bootstrap: paired-seed bootstrap, `10,000` resamples
- Analysis RNG seed: `20260823`
- Alpha: `0.05`
- Directional-support rule: point estimate `> 0` **and** two-sided 95% bootstrap CI lower bound `> 0`

No endpoint, exclusion rule, sample size, bootstrap rule, or classification rule may change after collection begins without invalidating confirmatory interpretation for this epoch.

## Interpretation ceiling

A successful positive result may support only a statement of the form:

> Under the preregistered Solo PDMAL v0.7.6 apparatus, the explicitly synthetic-bound DGAF-P30-EXPLICIT-0.45 variant showed directional FFCR support against null across the fixed 50-seed panel.

It may **not** establish canonical DGAF efficacy, real Apogee calibration, independent verification, Confidential Space qualification, production readiness, High-Assurance acceptance, or external certification.

A null or negative result must be retained and reported under the same scope.

## Relationship to prior epochs

- Solo Pilot run 001: retained separately; `N=360`; apparatus/QC evidence.
- Solo final experiment 001: retained separately; `N=9,000`; valid apparatus-falsification evidence; invalid for intended canonical-DGAF efficacy inference.
- P-30 diagnostic Epoch 002: non-empirical; 90/90 diagnostic attempts successful; scientific N increment `0`.
- Epoch 003: fresh blinded empirical variant; **not yet executed at preregistration**.
