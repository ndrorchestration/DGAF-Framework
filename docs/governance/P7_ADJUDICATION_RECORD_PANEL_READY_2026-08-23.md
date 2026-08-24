---
status: OPEN
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
review_base_sha: 15416ee189c7de7bdf725cd7e445dd4a2107ab06
empirical_n: 0
---

# P7 Adjudication Record — Panel-Ready Scientific Specification

## Authority and epistemic boundary

This is the **panel-ready P7 adjudication record**. It resolves the technical ambiguities identified during the P7 integrity review and presents the current proposals for formal adoption. It is not evidence of execution, not a freeze manifest, and not pilot authorization.

**P7 remains OPEN until the designated experimental-control authority explicitly adopts the record and the adopted decision is bound to the exact protocol/candidate identity used for the new freeze.**

The primary contrast already selected in the preceding reconciliation is retained:

> **DGAF condition versus null/reference condition on FFCR.**

Current repository design establishes four pilot conditions, five topologies, nine failure-count levels, 50 planned seeds, and **180 trial combinations per seed (4 × 5 × 9)**. The inferential unit is the root seed, not the individual trial.

## Decision 1 — Reference condition

**Current proposal:** `null`, implemented by the frozen condition registry/runner as the baseline with the DGAF intervention absent. The current runner defines `null` as the alpha=0.5 neighbor-averaging condition.

**Required binding:** exact condition identifier and implementation SHA must be copied into the freeze manifest. `simple` and `static` are secondary conditions, not alternate references.

**Rationale:** preserves the already selected DGAF-vs-null primary contrast and gives a direct intervention-versus-baseline comparison.

**Analysis consequence:** primary effect is `FFCR_dgaf(seed) - FFCR_null(seed)`.

**Falsification implication:** evidence of a non-positive or clearly negative primary effect does not support the directional DGAF hypothesis.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 2 — Exact estimand

**Current proposal:** the mean paired seed-level FFCR difference under the frozen experimental design:

`theta = E[FFCR_dgaf(S) - FFCR_null(S)]`

where `S` denotes a root seed drawn from the prespecified seed-generating process and both condition-level FFCR values are defined under the same frozen matrix.

The finite-sample estimator is:

`theta_hat = mean_s(Delta_s)`

with `Delta_s = FFCR_dgaf(s) - FFCR_null(s)` over analyzable paired seeds.

**Integrity requirement:** the estimand (population quantity) and estimator (sample statistic) must remain distinct in P8.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 3 — Unit of analysis and pairing

**Current proposal:** one root seed is one paired inferential block. Each seed contains **180 trial combinations: 4 conditions × 5 topologies × 9 failure-count levels**. The 45 topology × failure-count cells occur once per condition.

Raw trials are not independent inferential observations. The primary analysis reduces each condition's 45 cells to a condition-level FFCR and then forms the paired seed effect.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 4 — Direction of effect

**Current proposal:** higher FFCR is better. Therefore `Delta_s > 0` and `theta > 0` favor DGAF.

The primary inferential convention is a **two-sided 95% confidence interval with a directional support rule**: support requires the point estimate to be positive and the entire interval to lie above zero.

A one-sided test is not introduced implicitly; changing the two-sided convention requires explicit re-adjudication before unblinding.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 5 — Primary endpoint aggregation

**Current proposal:** for each seed and condition:

`FFCR = successful eligible cells / complete eligible cells`

The matrix contains 45 topology × failure-count cells per condition. Each of the 45 cells contributes equally to the condition-level FFCR. No topology or failure-count stratum receives additional inferential weight.

A cell is successful only when its recorded `ffcr_success` is true under the frozen artifact contract. The analysis does not reconstruct FFCR from `final_std`, repair missing outcomes, or silently impute cells.

Thus the design is **equal-cell weighting within each seed-condition, followed by equal-seed weighting in the primary estimand**.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 6 — Confidence interval method and convention

**Current proposal:** two-sided 95% **percentile paired-bootstrap confidence interval** over complete seed-level paired effects `Delta_s`.

Bootstrap resampling must resample complete paired seed effects, never individual trials independently.

The method/convention is a P7 scientific decision; implementation constants are bound in P8.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 7 — Bootstrap parameters and RNG separation

**Current proposal:** **10,000 bootstrap resamples** using analysis RNG seed `20260823`, with the bootstrap RNG kept in the analysis-resampling stream/domain and not reused as the topology, failure-injection, task-initialization, or trial-order RNG.

The bootstrap seed is an **analysis parameter**, not the experimental root seed. No bootstrap parameter may be changed after unblinding without re-adjudication.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 8 — Multiplicity treatment

**Current proposal:** the single pre-specified DGAF-vs-null primary estimand receives no multiplicity adjustment. Secondary contrasts are exploratory/descriptive unless a confirmatory family is explicitly declared in P8.

If secondary contrasts are promoted to confirmatory claims, Holm-Bonferroni is the required correction unless separately adjudicated before unblinding. The secondary family must enumerate its members before confirmatory inference.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 9 — Exclusion and missing-data rules

**Current proposal:**

1. No outcome may be excluded because it is favorable or unfavorable.
2. A primary cell must have a valid schema-conformant record and explicit `ffcr_success` value.
3. Missing or duplicate matrix cells invalidate the affected condition-level FFCR rather than being silently imputed.
4. A seed enters primary inference only when both DGAF and null condition-level FFCR values are computable from complete required matrices.
5. A seed missing an unrecoverable member of the primary pair is excluded from primary paired inference and its reason is recorded.
6. Apparatus-level protocol/infrastructure failures are classified as such rather than selectively converted into outcome exclusions.
7. Exclusion counts and reasons are mandatory analysis outputs.

The previously proposed arbitrary **10% seed-exclusion threshold is not adopted** unless separately justified and adjudicated; the present contract uses explicit matrix completeness and pairability rules.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 10 — Success criterion

**Current proposal:** primary support requires all of the following:

1. a valid authorized pilot dataset exists;
2. the locked analysis executes without protocol/schema/integrity failure;
3. `theta_hat > 0`; and
4. the two-sided 95% paired-bootstrap CI lies wholly above zero.

This is an **experimental evidence criterion**, not a claim of general real-world efficacy.

The prior `0.15` value is retained as a sample-size/planning minimum detectable difference unless separately re-established as a substantive-effect threshold. It is not silently converted into the P7 success boundary.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Decision 11 — Falsification / non-support criterion

**Current proposal:**

- **Not supported:** `theta_hat <= 0`, or a 95% CI that includes zero.
- **Evidence against:** the entire 95% CI lies below zero.
- **Inconclusive:** the interval overlaps zero without being wholly below it.

Failure to support is **not automatically equivalent to falsification**. An inconclusive result must not be described as proof that DGAF has no effect. Secondary/exploratory findings cannot convert a failed or inconclusive primary result into primary support.

If the panel wishes to define falsification as failure to achieve a practically meaningful effect rather than failure to establish positive improvement, that threshold must be explicitly specified before freeze.

**Status:** OPEN / PENDING AUTHORITY ADOPTION.

## Resolution matrix

| # | Requirement | Current proposal | Status |
|---|---|---|---|
| 1 | Reference | `null` baseline; exact implementation bound at freeze | OPEN |
| 2 | Estimand | `E[FFCR_dgaf - FFCR_null]`; estimator = mean paired seed effects | OPEN |
| 3 | Unit | Root seed; 180 trials/seed = 4×5×9; 45 cells/condition | OPEN |
| 4 | Direction | Higher FFCR better; DGAF−null positive | OPEN |
| 5 | Aggregation | Equal weighting of 45 cells within condition; equal weighting of paired seeds | OPEN |
| 6 | CI | Two-sided 95% percentile paired bootstrap | OPEN |
| 7 | Bootstrap | 10,000 resamples; analysis seed `20260823`; RNG domains separated | OPEN |
| 8 | Multiplicity | None for sole primary; Holm if secondary family becomes confirmatory | OPEN |
| 9 | Exclusions | Explicit matrix completeness/pairability; no outcome-aware exclusion; no arbitrary 10% threshold | OPEN |
| 10 | Success | Positive estimate + CI wholly above zero, on valid authorized dataset | OPEN |
| 11 | Falsification | CI wholly below zero = evidence against; overlap = inconclusive/non-support | OPEN |

## Formal closure conditions

P7 **does not close merely because this document exists**. Formal closure requires:

1. explicit adoption of all 11 decisions by the designated experimental-control authority;
2. verification that treatment/reference identifiers match the actual candidate apparatus;
3. reconciliation of the adopted decisions with the exact protocol and P8 analysis specification;
4. recording the authority, date, and adopted decision identity; and
5. binding the adopted record to the exact freeze candidate without silently changing any decision.

Only after those conditions are satisfied may P7 be marked `CLOSED`.

P8 may continue technical preparation in parallel, but its authoritative analysis lock may not claim scientific closure beyond the adopted P7 state.

**Pilot authorization:** NOT GRANTED.
**Empirical N:** 0.
**New freeze:** NOT CREATED.
