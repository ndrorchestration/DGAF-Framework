# Solo P-30 Explicit Variant Empirical Epoch 003 — Adjudication

## Status

`EXECUTED / ANALYZED / NEGATIVE_DIRECTIONAL_RESULT_FOR_SYNTHETIC_VARIANT / N=9000 / NOT_CANONICAL_DGAF`

This record closes the bounded empirical question preregistered for `PDMAL-SOLO-P30-EXPLICIT-V1`. It does not alter, erase, relabel, repair, or pool Solo final experiment 001 or non-empirical diagnostic Epoch 002.

## Treatment and claim identity

- Experiment ID: `PDMAL-SOLO-P30-EXPLICIT-V1`
- Variant scope: `DGAF-P30-EXPLICIT-0.45`
- P-30 binding: `SYNTHETIC_MINIMUM_PASSING_P30_FIXTURE_V1`
- Binding kind: `SYNTHETIC_MINIMUM_PASSING_FIXTURE`
- Fixed confidence: `0.45`
- Real/calibrated Apogee confidence: **NO**
- Canonical DGAF efficacy claim permitted: **NO**
- High-Assurance claim permitted: **NO**

Issue #165 designates P-30 grades and `D -> KILL` but does not designate a canonical source or calibration procedure for Apogee confidence. This epoch therefore answers only the explicitly synthetic-bound variant question.

## Execution identity

- Preregistration PR: `#372`
- Final preregistration head: `b98755ec50024661b408e006006e122d7fcf9a46`
- PR exact-head verification: `20/20` returned workflows successful
- Preregistration merge: `49a1a4c00aeb24fdd143fce1c5b464902291b151`
- Empirical branch: `solo-p30-variant/run-20260907-003`
- Exact one-file authorization / frozen empirical SHA: `ac72196151dd33907811cf1b172127d57a0a0bcb`
- GitHub Actions run: `34169097968` — `SUCCESS`
- Fresh seed range: `20260901..20260950`
- Seed count: `50`
- Cells per seed: `180`
- Empirical observations: `9,000`

## Locked blinded evidence

Dataset artifact:

- ID: `10035250498`
- digest: `sha256:3a9feba409bf7124269c02628b59bafd998405db834efa6df52786c06cf71150`

Separate key artifact:

- ID: `10035250680`
- digest: `sha256:f5dad9fbf23b9e1c3cea6951ff7ff4c7e86a6a4dda4f1c2187764efe8af54c8c`
- custody: `SAME_SYSTEM_GITHUB_ACTIONS_ARTIFACT`
- independent custody: **NO**

The collection workflow completed the 50-seed execution, structural lock, dataset upload, and separate key upload successfully. The lock recorded `LOCKED_BLINDED`, `outcomes_inspected_by_collection_workflow=false`, `unblinding_authorized=false`, validation track `SOLO_DEVELOPER_VARIANT`, and independent verification `NOT_ESTABLISHED_BY_RUNNER`.

Before key access, an independent structural recheck of the retained dataset verified:

- all 50 seed artifact hashes match the lock manifest;
- all SHA-256 sidecars match retained bytes;
- exactly 180 unique blinded matrix cells per seed;
- four balanced blinded arms, 45 cells per arm per seed;
- complete five-topology × nine-failure matrix within every blind arm;
- retained archive copies are byte-identical to output copies;
- one consistent environment fingerprint across the panel;
- no plaintext canonical condition-label leakage.

No outcome field was read during that pre-unblinding adjudication.

## Controlled unblinding

GitHub #309 comment `5576605180` separately authorized key release only after the blinded lock and structural recheck passed. The released key reconstructed exactly the four blinded identifiers present in the locked dataset.

## Locked analysis identity

- Statistical implementation: `experiments/pdmal_pilot/analysis.py`
- Source blob SHA: `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`
- Analysis-config SHA-256: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`
- Variant wrapper: `experiments/pdmal_pilot/analyze_p30_variant.py`
- Wrapper blob SHA: `92d7cb38c67572ef208425097c4433da50a968b3`
- Primary contrast: `DGAF-P30-EXPLICIT-0.45 - null`
- Unit: paired seed
- Estimator: mean paired seed FFCR difference
- Bootstrap: paired-seed percentile bootstrap
- Resamples: `10,000`
- RNG seed: `20260823`
- Alpha: `0.05`

No endpoint, exclusion, sample size, bootstrap, treatment-binding, or classification rule was changed after collection began.

## Locked primary result

- Mean paired FFCR effect: **`-0.11911111111111111`**
- Two-sided 95% paired-bootstrap CI: **`[-0.14844444444444443, -0.09066666666666666]`**
- Mechanical base classification: `EVIDENCE_AGAINST_DIRECTIONAL_DGAF`
- Bounded classification: **`EVIDENCE_AGAINST_DIRECTIONAL_DGAF_P30_EXPLICIT_0_45_VARIANT`**
- Aggregate variant FFCR: `0.7244444444444444`
- Aggregate null FFCR: `0.8435555555555555`

Across the 50 paired seed effects, `42` were negative, `8` were exactly zero, and `0` were positive.

Unlike experiment 001, this epoch did not exhibit deterministic P-30 termination. Execution-status structure was identical across all four conditions: each condition contained `250` no-failure `SUCCESS` cells and `2,000` failure-injected `RECOVERED` cells. The negative primary result is therefore not attributable to the experiment-001 missing-substrate `D -> KILL -> FAIL_CLOSED` apparatus defect.

## Post-primary exploratory description

The following topology summaries were calculated only after the locked primary analysis and are descriptive, not confirmatory. Aggregate FFCR difference, variant minus null:

- `ring`: `-0.19111111111111112`
- `pdmal`: `-0.008888888888888835`
- `random_regular`: `-0.3622222222222222`
- `small_world`: `-0.033333333333333326`
- `complete`: `0.0`

No topology-specific confirmatory claim is made from these summaries.

## Adjudication

**Retain as scientifically interpretable negative evidence for the explicitly synthetic-bound variant.**

Under the preregistered Solo PDMAL v0.7.6 apparatus and fixed 50-seed panel, `DGAF-P30-EXPLICIT-0.45` did not show directional FFCR benefit over null; the locked primary result instead provides evidence against directional benefit for this variant.

This result does **not** establish a negative or positive efficacy conclusion for canonical Apogee-calibrated DGAF because no real/calibrated Apogee confidence source was designated or tested.

It also does not establish independent verification, Confidential Space qualification, production readiness, High-Assurance acceptance, external certification, or independently retained custody.

## Prior and parallel evidence boundaries

- Solo Pilot run 001: `N=360`; retained QC/apparatus evidence.
- Solo final experiment 001: `N=9,000`; retained apparatus-falsification evidence; invalid for intended canonical-DGAF efficacy inference; never pooled with this epoch.
- P-30 diagnostic Epoch 002: non-empirical; 90/90 engineering diagnostic pass; scientific N increment `0`.
- Epoch 003: `N=9,000`; executed/analyzed; negative evidence for `DGAF-P30-EXPLICIT-0.45` only.
- High-Assurance: authorization not granted; empirical `N=0`.

GitHub #309 primary result record: comment `5576619491`.
