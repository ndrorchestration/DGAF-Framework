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

The current executable verification candidate is **`e6beeb66335e1b50a239697badab22dab50eb5ba`**.

Current `main` is `bc325486a2986256532e58dccf39a155ed75a72a`. The candidate is the exact executable apparatus identity for P8 verification. The 18 commits between the candidate and current `main` are treated as documentation/governance synchronization successors unless a substantive executable/schema/workflow/dependency/protocol/analysis change is identified. Such a substantive change would invalidate the candidate binding and require a new candidate plus affected-predicate re-verification.

| Binding | Value | State |
|---|---|---|
| Executable candidate | `e6beeb66335e1b50a239697badab22dab50eb5ba` | CANDIDATE |
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CANDIDATE; blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` |
| Analysis configuration SHA | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | SELECTED |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CANDIDATE; blob `970360c868b58e9fcc63ed1fc32cc6f7ce698f12` |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CANDIDATE; blob `6b604d4eabaaf42b1dc9bd46099c8a09893ba1e9` |
| Governance CI | `.github/workflows/governance-ci.yml` | CANDIDATE; blob `d30c92d15e6aeae755a50416ffe0a0a0dd48c56e` |
| Canonical protocol | v`0.7.5` | CURRENT SPECIFICATION |
| Canonical protocol blob on `main` | `0923010a1b601290f10699a961a5231576430258` | PRE-FREEZE / BOUND AT P8 LOCK |
| Protocol applicability | `applies_to_sha: e6beeb...` | ALIGNED |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |
| Secondary policy | Holm if confirmatory; otherwise exploratory/descriptive | SELECTED |

## Protocol/candidate separation rule

The executable candidate and the living canonical protocol are separate provenance objects. The candidate apparatus is bound to `e6beeb...`; the current protocol blob is the methodology authority and explicitly declares `applies_to_sha: e6beeb...`. The protocol remains PRE-FREEZE. Its blob hash must be captured in the eventual freeze manifest. No protocol text is treated as experimental data or authorization.

## P8 discrepancy and correction history

The first P8 implementation pass was not end-to-end compatible: the runner emitted `ffcr_success`, but the pilot artifact schema did not require it, and the analysis required matrix coordinates that the runner had not exposed at those locations.

Subsequent corrections now make `ffcr_success`, `topology`, and `failure_count` required, integrity-covered artifact fields. The runner emits those fields directly and defines `ffcr_success` as successful execution **and** satisfied consensus criterion, matching the governing protocol. The schema rejects malformed outcomes and impossible `ffcr_success=true` / non-`SUCCESS` combinations. Adversarial tests cover the contract, and Governance CI invokes the P8 analysis/security test pair.

Additional corrective work has addressed boolean-as-integer acceptance, artifact/document identity binding, duplicate matrix/trial rejection, exact 4×45 blinded balance, retry clock injection, recovery-state semantics, durable retention overwrite/fail-open behavior, bijective unblinding, unique/finite bootstrap inputs, and associated regression tests.

## Analysis boundaries

The canonical analysis consumes validated seed artifacts plus an explicit post-unblinding condition mapping. It does not execute trials, regenerate observations, repair incomplete records, infer missing outcomes, or unblind labels. It rejects missing or duplicate matrix cells and malformed outcomes, and resamples complete paired seed effects rather than individual trials.

## Closure blockers

P8 remains **OPEN / FAIL-CLOSED** pending all of:

1. Candidate-scoped Governance CI execution on exact `e6beeb...` with the resulting run and artifacts inspected.
2. P2 authenticated five-case runtime verification against the exact READY deployment.
3. P6a authenticated four-case CORS verification against the same deployment identity.
4. Environment/topology reproducibility evidence.
5. Durable evidence retention with direct retrieval and integrity verification.
6. E2b verifier-toolchain provenance and hash-pinning, tracked by #105.
7. M6 machine-retained negative-state evidence, tracked by #106.
8. Formal P7 authority adoption and cryptographic binding.
9. Independent verification required by the governing acceptance process.

A successful CI run or deployment readiness is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.
**Empirical N:** 0.
**New freeze:** NOT CREATED.
