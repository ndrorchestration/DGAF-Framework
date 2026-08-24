# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE
**Authority:** DGAF/PDMAL experimental-design control
**Purpose:** Bind the executable primary analysis and its artifact contract to the adopted P7 scientific target before any unblinding or empirical interpretation.

## P7 inputs fixed

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed, paired by root seed identity.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean of complete paired seed effects.
- FFCR: proportion of complete topology × failure-count cells whose recorded `ffcr_success` is true.
- No outcome-dependent weighting, exclusion, or silent imputation.

## Current candidate tree

The previously recorded P8 binding at `b681c87...` is superseded as a candidate-closure identity because six subsequent commits modified the Governance CI workflow, P8 analysis lock, runner, pilot artifact schema, and security tests. The prior `94fb6fd...` local candidate and PR #77 head `b25a914c...` are historical/stale for current P8 candidate reporting.

**Current exact candidate tree:** `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f`

| Binding | Value | State |
|---|---|---|
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CANDIDATE |
| Analysis blob | `24e7375f5ac907713460269ea2b65408ea6f0455` | CANDIDATE |
| Analysis configuration SHA | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | CANDIDATE |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CANDIDATE; blob `36c147c36fe2f1977e3cc904bf62c671bfbee9fe` |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CANDIDATE; blob `21a40aeb455150666bad6e01fb306a15eb112d0b` |
| Governance CI | `.github/workflows/governance-ci.yml` | CANDIDATE; blob `38164e0571a4df932b3e65454e3c40235bf95e48` |
| Protocol | v`0.7.5`, blob `d986923643b1ef6f17d4099a628e0dfd2e20c147` | CANDIDATE |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |
| Secondary policy | Holm if confirmatory; otherwise exploratory/descriptive | SELECTED |

## P8 discrepancy and correction

Candidate audit found that the first P8 implementation pass was still not end-to-end compatible: the runner emitted `ffcr_success`, but the pilot artifact schema did not require it, and the analysis required top-level `topology` and `failure_count` coordinates that the runner had not exposed at those locations.

Subsequent corrections now make `ffcr_success`, `topology`, and `failure_count` required, integrity-covered artifact fields. The runner emits those fields directly and defines `ffcr_success` as successful execution **and** satisfied consensus criterion, matching the governing protocol. The schema rejects malformed outcomes and impossible `ffcr_success=true` / non-`SUCCESS` combinations. Adversarial tests cover the contract, and Governance CI now invokes the P8 analysis/security test pair.

The correction sequence invalidated earlier apparatus-base identities as closure candidates. The exact candidate tree is now explicitly identified above, but it remains **unverified** until Governance CI is actually executed against that exact tree and the resulting run is inspected.

## Analysis boundaries

The canonical analysis consumes validated seed artifacts plus an explicit post-unblinding condition mapping. It does not execute trials, regenerate observations, repair incomplete records, infer missing outcomes, or unblind labels. It rejects missing or duplicate matrix cells and malformed outcomes, and resamples complete paired seed effects rather than individual trials.

## Closure blockers

P8 remains **OPEN** pending all of:

1. Candidate-scoped Governance CI execution on exact `2a80f819...`.
2. Inspection of the explicit P8 artifact-schema and analysis test results.
3. Exact executed-tree SHA/provenance reconciliation and binding update.
4. Environment/topology reproducibility evidence.
5. Durable evidence retention with direct retrieval and integrity verification.
6. Independent verification required by the governing acceptance process.

A successful CI run is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.
**Empirical N:** 0.
**New freeze:** NOT CREATED.
