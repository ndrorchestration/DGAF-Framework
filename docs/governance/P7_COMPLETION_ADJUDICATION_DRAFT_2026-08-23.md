---
status: READY_FOR_AUTHORIZATION
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
base_sha: 6639eef64be229044562730ba111e08a3ad522dc
empirical_n: 0
---

# P7 Completion Adjudication Draft — 2026-08-23

## Purpose and authority boundary

This document completes the technical and methodological adjudication pass for P7 using the current repository contract. It is a **proposed authoritative decision record**, not evidence of execution and not pilot authorization. Formal closure requires explicit adoption of this record and subsequent binding to the exact freeze/protocol identity.

The primary contrast previously selected is retained without modification:

> **Primary contrast: DGAF condition versus null/reference condition on FFCR.**

The current design defines FFCR as failure-free completion proportion per condition per seed, uses the seed as the statistical unit, plans 50 seeds, and specifies a 4-condition × 5-topology × 9-failure-count matrix. The existing analysis-control plan identifies paired seed-level differences and paired-bootstrap confidence intervals as the intended inference framework.

## P7 decision record

### 1. Treatment and reference definitions

**Treatment:** the experiment's configured DGAF condition, executed under the frozen apparatus.

**Reference/null:** the experiment's configured null condition, executed under the same frozen apparatus with the DGAF intervention absent as defined by the condition registry/runner.

No undocumented substitution of a different baseline is permitted. The exact condition identifiers and implementation bindings must be copied verbatim into the freeze manifest.

### 2. Unit of analysis and pairing

The statistical unit is **one root seed**. For each root seed, treatment and reference observations are generated under the matched frozen experimental matrix. Pairing is therefore by identical root seed and matched matrix coordinates defined by the frozen runner.

Raw trials are not treated as independent inferential observations. The analysis reduces matched trial outcomes to the pre-specified condition-level FFCR for each seed before primary inference.

### 3. Primary estimand and aggregation rule

For seed s, let FFCR_DGAF(s) and FFCR_NULL(s) denote the condition-level failure-free completion proportions across all matrix cells assigned to that condition by the frozen protocol. Define the paired seed effect:

Δ(s) = FFCR_DGAF(s) − FFCR_NULL(s).

The primary estimand is the mean paired seed-level effect:

θ = (1 / N) Σ_s Δ(s),

where N is the number of analyzable paired seeds.

The primary point estimate is the sample mean of Δ(s). Each seed receives equal weight; no individual topology or failure-count cell receives additional inferential weight beyond its contribution to the condition-level proportion defined by the frozen matrix.

### 4. Direction of improvement

Higher FFCR is better. Therefore:

- θ > 0 favors DGAF;
- θ = 0 indicates no average difference under the estimand;
- θ < 0 favors the reference/null condition.

### 5. Primary inference

The primary estimate is accompanied by a **two-sided 95% paired-bootstrap confidence interval** over the vector of seed-level paired effects Δ(s).

Bootstrap resampling must resample complete paired seed effects, never individual trials independently. The bootstrap implementation, interval construction, replicate count, and bootstrap RNG seed must be explicitly fixed in P8 before freeze. This document intentionally does not select those implementation constants from convenience after observing pilot data.

### 6. Secondary and exploratory contrasts

The following remain secondary/exploratory:

1. PDMAL topology versus Ring;
2. condition × topology interaction;
3. other contrasts not designated as the primary contrast in the frozen analysis specification.

Secondary analyses must not replace the primary result or rescue a failed primary criterion. Their exact estimands and reporting family must be enumerated in P8.

### 7. Multiplicity treatment

No multiplicity adjustment is applied to the single pre-specified primary estimand. Secondary/exploratory contrasts are reported as secondary/exploratory and must use a multiplicity procedure specified in P8 if they are presented with confirmatory inferential claims. Otherwise they remain descriptive/exploratory with no confirmatory efficacy conclusion.

### 8. Exclusion and missing-data rules

A seed is analyzable only when both DGAF and null condition-level FFCR values can be computed from records satisfying the frozen artifact schema and required matrix completeness rules.

- No observation may be excluded because its outcome is favorable or unfavorable.
- Protocol or infrastructure failures are not silently converted into outcome failures or dropped selectively.
- A seed with an unrecoverable missing member of the primary pair is excluded from paired primary inference and recorded with its failure reason.
- The count of excluded seeds and all exclusion reasons are mandatory outputs.
- If exclusions or missingness indicate a systematic apparatus failure, execution must be classified as a protocol/infrastructure failure rather than interpreted as efficacy evidence.

No outcome-aware exclusion rule may be introduced after unblinding.

### 9. Success criterion

The primary analysis supports the directional DGAF hypothesis only if all of the following hold:

1. the locked analysis executes on a valid authorized pilot dataset;
2. the primary point estimate θ is greater than zero; and
3. the two-sided 95% paired-bootstrap confidence interval for θ excludes zero on the positive side.

This is a criterion for evidence under the defined pilot conditions, not a general claim of real-world efficacy.

### 10. Falsification / non-support criterion

The directional primary hypothesis is **not supported** if the 95% confidence interval includes zero or the point estimate is non-positive.

A result whose confidence interval lies wholly below zero constitutes evidence against the directional hypothesis under the frozen experimental conditions. A statistically inconclusive result is not reclassified as success through secondary contrasts or exploratory analyses.

### 11. Decision identity and binding

This draft applies to repository candidate `6639eef64be229044562730ba111e08a3ad522dc` as the adjudication base only. It is **not itself a freeze identity**.

Before P7 is formally CLOSED, the adopted decision must be bound to:

- exact protocol SHA;
- exact runner/apparatus SHA(s) required by the freeze manifest;
- exact condition identifiers;
- exact analysis specification identity; and
- the new freeze manifest identity.

Any material change to these definitions requires re-adjudication rather than silent inheritance.

## Resolution matrix

| P7 requirement | Resolution | Status |
|---|---|---|
| Primary contrast | DGAF vs null | Selected / retained |
| Reference definition | Frozen configured null condition | Proposed for binding |
| Estimand | Mean paired seed-level FFCR difference | Proposed |
| Unit/pairing | Root seed; matched matrix | Defined |
| Direction | Higher FFCR is better | Proposed |
| Aggregation | Equal-weight seed-level condition FFCR | Proposed |
| CI method | Two-sided 95% paired bootstrap | Proposed; implementation constants deferred to P8 |
| Secondary contrasts | Topology and interaction exploratory | Defined |
| Multiplicity | None for primary; P8-defined for confirmatory secondary claims | Proposed |
| Exclusion/missingness | Pre-specified pair-completeness and audit rules | Proposed |
| Success criterion | Positive estimate and CI wholly above zero | Proposed |
| Falsification criterion | Non-positive or inconclusive does not support; CI wholly below zero opposes | Proposed |
| Authority/date | Explicit adoption required | Open authority action |
| Exact freeze identity | Must be bound at freeze | Open dependency |

## Closure conditions

P7 is **technically adjudicated but not yet formally closed** by this draft. Formal closure requires:

1. explicit adoption by the designated experimental-control authority;
2. verification that the treatment/reference identifiers match the actual frozen apparatus; and
3. binding the adopted record to the exact protocol and freeze identities.

After those actions, P8 may construct the cryptographically bound analysis specification. Pilot authorization remains separate and is **NOT GRANTED**. Empirical N remains **0**.
