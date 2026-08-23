# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE
**Authority:** DGAF/PDMAL experimental-design control
**Purpose:** Bind the executable primary analysis to the adopted P7 scientific target before any unblinding or empirical interpretation.

## P7 inputs now fixed

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed.
- Seed pairing key: root seed identity with matched frozen matrix coordinates.
- Seed-level primary difference: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean seed-level paired difference over analyzable paired seeds.
- Positive difference favors DGAF.
- FFCR is computed as the proportion of complete topology × failure-count matrix cells whose recorded `ffcr_success` is true.
- Secondary/exploratory family: PDMAL vs Ring; condition × topology interaction; structural/execution diagnostics.
- No post-observation weighting changes are permitted.
- No outcome-dependent seed exclusion or silent seed-level imputation is permitted.

## P8 implementation decisions now fixed

The first canonical analysis implementation is `experiments/pdmal_pilot/analysis.py`.

| Binding | Current value | State |
|---|---|---|
| Analysis implementation path | `experiments/pdmal_pilot/analysis.py` | CANDIDATE |
| Analysis implementation SHA | Pending final candidate commit binding | OPEN |
| Configuration | Canonical configuration emitted by `analysis_config_bytes()` | CANDIDATE |
| Configuration SHA | Produced by `analysis_config_sha256()` | OPEN — bind exact value |
| Bootstrap | Paired seed effects; percentile interval | SELECTED |
| Bootstrap resamples | `10,000` | SELECTED |
| Bootstrap RNG seed | `20260823` | SELECTED |
| Confidence interval | Two-sided percentile 95% CI | SELECTED |
| Alpha | `0.05` | SELECTED |
| Primary decision | Estimate > 0 and CI lower bound > 0 | SELECTED |
| Secondary multiplicity | Holm if a secondary family is presented with confirmatory inference; otherwise descriptive/exploratory | SELECTED |
| Exclusion/missingness | Complete paired seed required; no outcome-aware exclusion; infrastructure failures recorded separately | SELECTED |
| Protocol identity | Exact protocol blob SHA after final protocol commit | OPEN |
| Manifest identity | Exact new freeze/manifest binding | OPEN |

## Execution/artifact dependency discovered during P8

The existing pilot runner previously recorded `final_std` as `primary_outcome` but did not emit an explicit boolean `ffcr_success`. Because P7 defines FFCR as failure-free completion proportion, an explicit `ffcr_success` field is required for the canonical analysis to consume the immutable artifacts without reconstructing execution semantics.

The runner has therefore been amended to record `consensus_success` as `ffcr_success`. This is an apparatus change and therefore must be included in candidate verification before any freeze.

The runner also currently reports protocol version `0.7.4` while the governing protocol incorporates the v0.7.5 matrix amendment. This version identity must be reconciled before P8 closure/freeze rather than silently ignored.

## Analysis boundaries

The canonical analysis:

- consumes validated seed artifacts only;
- does not execute trials;
- does not regenerate observations;
- does not repair incomplete records;
- rejects duplicate/missing matrix cells;
- rejects malformed `ffcr_success` values;
- resamples complete paired seed effects, never individual trials;
- reports exclusions and missingness explicitly;
- cannot convert exploratory secondary results into the primary conclusion.

## Lock rules

1. No empirical observation may be used to choose any open binding.
2. No unblinding may occur before every required binding is populated and independently checked.
3. Changing a locked binding after unblinding invalidates the current analysis lock and requires a new governance decision.
4. Historical analysis or characterization artifacts cannot substitute for the exact candidate implementation/configuration binding.
5. P8 closure does not authorize the pilot; authorization remains a separate governance transition after freeze and P9 verification.

## Current blocker

P8 is materially advanced but remains **OPEN** pending:

- final candidate commit identity;
- configuration digest binding;
- protocol version/identity reconciliation;
- candidate-scoped CI and analysis-test verification;
- independent verification of the analysis implementation;
- exact manifest/freeze identity.

**Pilot authorization:** NOT GRANTED.
**Empirical N:** 0.
**New freeze:** NOT CREATED.
