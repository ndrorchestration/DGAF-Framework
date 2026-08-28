# P8 Analysis Lock

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED
**Authority:** DGAF/PDMAL experimental-design control
**Purpose:** Bind the executable primary analysis and its artifact contract to the P7 scientific target before any unblinding or empirical interpretation.

## P7 inputs fixed

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: seed, paired by root seed identity.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean of complete paired seed effects.
- FFCR: proportion of complete topology × failure-count cells whose recorded `ffcr_success` is true.
- No outcome-dependent weighting, exclusion, or silent imputation.

## Current verification boundary

The current `main` verification boundary is **`ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`**.

The prior executable candidate `e6beeb66335e1b50a239697badab22dab50eb5ba` is historical provenance only for current verification. The later workflow change at `ac8ea26…` changed candidate binding and therefore required affected-predicate re-verification under the dynamic invalidation rule.

| Binding | Value | State |
|---|---|---|
| Current verification boundary | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` | CURRENT |
| Historical candidate | `e6beeb66335e1b50a239697badab22dab50eb5ba` | HISTORICAL |
| Analysis implementation | `experiments/pdmal_pilot/analysis.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Analysis configuration SHA | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | SELECTED / PRE-FREEZE |
| Artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Runner | `experiments/pdmal_pilot/run_pilot.py` | CURRENT-TREE / RE-BIND AT P8 CLOSURE |
| Governance CI | `.github/workflows/governance-ci.yml` | CURRENT; corrected exact-SHA binding |
| Canonical protocol | v`0.7.5` | CURRENT SPECIFICATION / PRE-FREEZE |
| Bootstrap | 10,000 paired-seed percentile resamples, seed `20260823` | SELECTED |
| CI | two-sided 95%, `alpha=0.05` | SELECTED |
| Directional support | estimate > 0 and CI lower bound > 0 | SELECTED |

## Protocol/candidate separation rule

The executable apparatus and living canonical protocol remain separate provenance objects. A protocol text does not constitute experimental data or authorization. Before freeze, the exact protocol blob, executable tree, analysis implementation/configuration, runner, artifact schema, and verification evidence must be captured and bound in the freeze manifest.

## P8 discrepancy and correction history

The prior P8 implementation corrections remain part of provenance: `ffcr_success`, `topology`, and `failure_count` were made required and integrity-covered; runner and schema semantics were reconciled; adversarial tests cover the artifact contract; and Governance CI invokes the P8 analysis/security test pair. Additional corrections addressed boolean-as-integer acceptance, identity binding, duplicate rejection, blinded balance, retry/recovery semantics, durable retention, bijective unblinding, bootstrap input integrity, and associated regressions.

## Closure blockers

P8 remains **OPEN / FAIL-CLOSED** pending:

1. Re-binding analysis/schema/runner/protocol identities to the current verification boundary.
2. P2 authenticated five-case runtime verification against the exact deployment.
3. P6a authenticated four-case CORS verification against the same deployment identity.
4. Environment/topology reproducibility evidence.
5. Durable evidence retention with direct retrieval and integrity verification.
6. Current-tree evidence review for E2b/M6, retaining their exact execution boundaries.
7. P7 exact freeze binding and formal closure of the adopted scientific decision record.
8. Independent P9 verification.

A successful CI run or deployment readiness is necessary evidence, not by itself P8 closure.

**Pilot authorization:** NOT GRANTED.
**Empirical N:** 0.
**New freeze:** NOT CREATED.
