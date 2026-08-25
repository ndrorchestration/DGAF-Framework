# P7 Scientific Specification Traceability Matrix

**Purpose:** Map each of the 11 P7 adjudication decisions to its authoritative source document, current proposal, adjudication status, downstream P8 dependency, and whether the decision is scientifically binding vs implementation-configurable.

**P7 record:** `docs/governance/P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md` (status: OPEN / PENDING AUTHORITY ADOPTION)

**Epistemic boundary:** N=0, NOT GRANTED, PRE-FREEZE. Pilot authorization is not granted. No empirical execution has occurred. P7 cannot be formally closed until the designated authority adopts all 11 decisions and binds the adopted record to the exact candidate.

**Date compiled:** 2026-08-24 (post-PR #83/#84/#76 integration, HEAD `b16be6f`)

---

## Decision Traceability

| # | Decision | Authoritative source | Current proposal | Status | P8 dependency | Classification |
|---|----------|--------------------|------------------|--------|---------------|----------------|
| 1 | Reference condition | Decision 1, P7 record | `null` baseline (alpha=0.5 neighbor-averaging); DGAF-vs-null primary contrast | OPEN | Condition identifiers bound to freeze manifest; runner SHA | **P7 scientific** |
| 2 | Estimand | Decision 2, P7 record | `theta = E[FFCR_dgaf(S) - FFCR_null(S)]`; estimator = mean paired seed effects | OPEN | Estimand/estimator separation enforced in analysis.lock | **P7 scientific** |
| 3 | Unit of analysis | Decision 3, P7 record | Root seed; 180 trials/seed = 4×5×9; 45 cells/condition | OPEN | Paired seed effects used in bootstrap; 180 trials/seed in runner | **P7 scientific** |
| 4 | Direction of effect | Decision 4, P7 record | Higher FFCR better; DGAF-null positive; two-sided 95% CI; directional support rule | OPEN | Directional support criterion configured in analysis.lock | **P7 scientific** |
| 5 | Endpoint aggregation | Decision 5, P7 record | FFCR = successful/complete eligible cells; equal-cell weighting; equal-seed weighting | OPEN | FFCR computation in analysis; artifact contract requires `ffcr_success` field | **P7 scientific** |
| 6 | CI method/convention | Decision 6, P7 record | Two-sided 95% percentile paired-bootstrap CI | OPEN | CI method in analysis.lock; implementation constants in P8 | **P7 scientific** |
| 7 | Bootstrap parameters | Decision 7, P7 record | 10,000 resamples; analysis RNG seed `20260823`; RNG domains separated | OPEN | Bootstrap seed, resamples, RNG separation in analysis.lock | **Mixed**: resample count + RNG seed = P8 implementation; RNG domain separation = P7 scientific |
| 8 | Multiplicity | Decision 8, P7 record | No multiplicity for primary; Holm-Bonferroni if secondary becomes confirmatory | OPEN | Primary estimand gets no correction; secondary family enumeration required before confirmatory inference | **P7 scientific** |
| 9 | Exclusion/missing-data rules | Decision 9, P7 record | No outcome-aware exclusion; explicit matrix completeness/pairability; no arbitrary 10% threshold | OPEN | Matrix completeness enforced in artifact contract; exclusion counts required in analysis | **P7 scientific** |
| 10 | Success criterion | Decision 10, P7 record | Positive estimate + CI wholly above zero on valid authorized dataset; `0.15` = planning MDE, not success threshold | OPEN | `decision()` function implements: `estimate > 0` AND `low > 0` = SUPPORTS; `0.15` retained as planning context only | **P7 scientific** |
| 11 | Falsification/non-support | Decision 11, P7 record | CI wholly below zero = evidence against; overlap = inconclusive/non-support; non-support ≠ falsification | OPEN | `decision()` function distinguishes SUPPORTS / NOT_SUPPORTED / EVIDENCE_AGAINST | **P7 scientific** |

---

## Classification: P7 Scientific Decisions vs P8 Implementation Constants

The panel identified a parameter-boundary mismatch: the P8 lock selects 10,000 bootstrap resamples, seed `20260823`, two-sided 95%, alpha 0.05, directional support criterion — but the P7 draft says bootstrap implementation constants are deferred to P8.

To prevent someone from changing an analysis parameter and claiming "only implementation," each parameter must be classified:

| Parameter | Current value | Classification | Rationale |
|-----------|---------------|----------------|-----------|
| Bootstrap resample count | 10,000 | **P8 implementation constant** | P7 Decision 7 defers "implementation constants" to P8; resample count is a precision parameter, not a scientific decision |
| Analysis bootstrap seed | `20260823` | **P8 implementation constant** | P7 Decision 7 defers implementation constants; seed is a reproducibility parameter |
| CI confidence level | 95% (two-sided) | **P7 scientific decision** | P7 Decision 6 explicitly adjudicates "two-sided 95% percentile paired-bootstrap CI" |
| Alpha level | 0.05 | **P7 scientific decision** | Inherent in the 95% CI decision (1 - 0.95 = 0.05); changing it requires re-adjudication of Decision 6 |
| Directional support criterion | estimate > 0 AND CI lower bound > 0 | **P7 scientific decision** | P7 Decision 4 adjudicates the directional support rule; Decision 10 codifies it as the success criterion |
| Bootstrap RNG seed | (analysis seed, separate from experimental root seed) | **P8 implementation constant** | P7 Decision 7 defers implementation constants; RNG seed is a reproducibility parameter |
| RNG domain separation | Analysis RNG separated from topology/failure-injection/task RNG | **P7 scientific decision** | P7 Decision 7 explicitly adjudicates "bootstrap RNG kept in analysis-resampling stream/domain and not reused as topology, failure-injection, task-initialization, or trial-order RNG" |
| Estimand | `E[FFCR_dgaf(S) - FFCR_null(S)]` | **P7 scientific decision** | P7 Decision 2 explicitly adjudicates the estimand |
| Estimator | `mean_s(Delta_s)` | **P7 scientific decision** | P7 Decision 2 explicitly adjudicates the estimator |
| FFCR definition | successful/complete eligible cells, equal weighting | **P7 scientific decision** | P7 Decision 5 explicitly adjudicates the aggregation method |
| Exclusion rules | No outcome-aware exclusion; matrix completeness/pairability; no 10% threshold | **P7 scientific decision** | P7 Decision 9 explicitly adjudicates exclusion rules |

---

## P7 Formal Closure Checklist

Before P7 can be marked CLOSED, all of the following must be satisfied:

- [ ] **1.** Explicit adoption of all 11 decisions by the designated experimental-control authority
- [ ] **2.** Verification that treatment/reference identifiers match the actual candidate apparatus (runner, condition registry, topology definitions)
- [ ] **3.** Reconciliation of adopted decisions with exact protocol SHA and P8 analysis specification SHA
- [ ] **4.** Recording of authority, date, and adopted decision identity
- [ ] **5.** Binding the adopted record to the exact freeze candidate without silently changing any decision
- [ ] **6.** All 11 decisions classified as P7 scientific vs P8 implementation (this matrix)
- [ ] **7.** P7 record status changed from OPEN to CLOSED with provenance

**Current state:** None of the closure conditions are satisfied. P7 remains OPEN.

---

## P7 Scientific Specification State (Corrected)

Per the panel's finding, the repository's current claim that "P7 is adopted" is a contradiction with the P7 adjudication record itself, which states all 11 decisions are OPEN / PENDING AUTHORITY ADOPTION.

**Corrected statement:**

> **P7 scientific specification: TECHNICALLY ADJUDICATED / PROPOSED AUTHORITATIVE SPECIFICATION / FORMALLY OPEN**
>
> The panel-ready P7 adjudication record (`P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md`) presents proposals for all 11 scientific decisions. The primary contrast (DGAF vs null on FFCR) has been selected in prior reconciliation. However, formal authority adoption has not occurred, the adopted record has not been bound to the exact candidate, and none of the five formal closure conditions are satisfied.
>
> P7 may NOT be described as "ADOPTED" until formal authority adoption is evidenced and the binding is complete.

---

## Downstream P8 Dependencies (per decision)

| Decision | P8 artifact / workflow | Binding requirement |
|----------|----------------------|--------------------|
| 1 (Reference) | `condition_registry`, runner, topology definitions | Condition identifiers + implementation SHA in freeze manifest |
| 2 (Estimand) | `analysis.lock`, `analysis.py` | Estimand/estimator separation enforced; verified in checklist Item 1 |
| 3 (Unit) | Runner (`run_pilot.py`), analysis | 180 trials/seed verified; paired seed effects used in bootstrap |
| 4 (Direction) | `analysis.lock` | Directional support criterion = estimate > 0 AND low > 0 |
| 5 (Aggregation) | `analysis.py: condition_ffcr()`, artifact schema | FFCR computation + artifact contract `ffcr_success` field |
| 6 (CI method) | `analysis.lock`, `analysis.py: paired_bootstrap_ci()` | Two-sided 95% percentile paired bootstrap |
| 7 (Bootstrap params) | `analysis.lock`, `analysis.py` | 10,000 resamples, seed `20260823`, RNG domain separation |
| 8 (Multiplicity) | `analysis.py: decision()` | Primary gets no correction; secondary family enumeration required |
| 9 (Exclusions) | Artifact schema, `analysis.py` | Matrix completeness enforced; exclusion counts required |
| 10 (Success) | `analysis.py: decision()` | Positive estimate + CI wholly above zero; `0.15` = planning MDE only |
| 11 (Falsification) | `analysis.py: decision()` | SUPPORTS / NOT_SUPPORTED / EVIDENCE_AGAINST distinctions |

---

## Synthesis

The P7 record is panel-ready but not formally closed. The primary contrast has been selected, but all 11 decisions remain OPEN / PENDING AUTHORITY ADOPTION. The P8 analysis implementation is consistent with the proposed P7 decisions, but P8 cannot claim scientific closure beyond the OPEN P7 state.

The corrected state is: **P7 = technically adjudicated / proposed authoritative specification / formally OPEN.** Not "ADOPTED."

*End of traceability matrix.*
