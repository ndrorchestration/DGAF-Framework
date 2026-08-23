# PDMAL P7 Adjudication Brief — Primary Contrast Decision Packet

**Prepared:** 2026-08-22  
**Status:** CANDIDATE A SELECTED — REMAINING P7 FIELDS OPEN  
**Authority:** DGAF/PDMAL experimental-control (scientific/governance decision)  
**Protocol state:** PRE-FREEZE  
**Empirical N:** 0  
**Pilot authorization:** NOT GRANTED  
**Candidate SHA:** `94fb6fdff64f2919d35938c5b1cb506625cf1139` (candidate as of GitHub state checked 2026-08-22)  
**Freeze target SHA:** `915e454e27eb2770e7f40a067a881b0783feaae4` (PR #65 merge baseline)  
**PR #77:** open, still lists remaining governance/evidence gates (primary contrast, blinding custody, topology reconciliation, durable retention, analysis SHA, new freeze)

---

## Purpose

This document is a **decision packet**, not an explanatory document. It presents the three candidate primary contrasts for the PDMAL scalar-consensus experiment and requires an explicit record for each of the 12 adjudication fields before the protocol can move toward freeze.

This document does **not** select a contrast, authorize pilot execution, or claim any empirical result. N remains 0.

---

## Current Protocol Framework (pre-specified, not up for adjudication)

These elements are already established by the protocol and task specification. The P7 decision must be **compatible with** these, not redefine them:

| Element | Established value | Source |
|---|---|---|
| Primary endpoint | FFCR (Failure-Free Completion Rate) | PDM_EXPERIMENT_PROTOCOL.md, PDM_TASK_SPEC_V0.7.4.md |
| Statistical unit | One seed | PDM_EXPERIMENT_PROTOCOL.md (line 23), PDM_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md (line 72) |
| Seed-level effect | Paired difference in condition-level FFCR per frozen aggregation rule | PDM_EXPERIMENT_PROTOCOL.md |
| Primary inference | Prespecified paired seed-level analysis + paired-bootstrap CI | PDM_EXPERIMENT_PROTOCOL.md |
| Pilot matrix | 4 conditions × 5 topologies × 9 failure-count levels = 180 trials/seed | PDM_EXPERIMENT_PROTOCOL.md, PDM_TASK_SPEC_V0.7.4.md |
| Planned seeds | 50 (producing 9,000 observations) | PDM_EXPERIMENT_PROTOCOL.md, PDM_ANALYSIS_CONTROL_PLAN.md |
| Conditions | `null`, `simple`, `static`, `dgaf` (`dgaf_pdmal` explicitly out of scope) | PDM_TASK_SPEC_V0.7.4.md |
| Topology fingerprint | Deterministic derivation from topology graph | PDM_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md |
| Iterations per trial | 100 (fixed; no convergence-based early stopping) | PDM_TASK_SPEC_V0.7.4.md |
| Success metric (task level) | Consensus threshold < 0.01 | PDM_TASK_SPEC_V0.7.4.md |

---

## Candidate Primary Contrasts (for adjudication only)

### Candidate 1: dgaf vs null (condition-level)

**Description:** Full DGAF stack (`dgaf` condition) vs no-DGAF baseline (`null` condition), aggregated according to the current FFCR estimand.

**Estimand:** E[FFCR(`dgaf`) − FFCR(`null`)], where each term is the condition-level FFCR aggregated per the frozen rule across all seeds.

**Paired structure:** Each seed contributes a paired difference d_i = FFCR_i(`dgaf`) − FFCR_i(`null`), using the same seed, same topology distribution, same failure-count distribution.

**Direction:** Higher FFCR for `dgaf` expected favorable (hypothesis: DGAF improves execution robustness).

**Multiplicity:** If this is the sole primary contrast, no multiplicity correction required for the primary test. Secondary contrasts would require correction.

**Compatibility:** Directly compatible with the current seed-level paired analysis and paired-bootstrap CI. Most natural fit for the current framework.

**Historical note:** No historical contrast to inherit — this is a fresh hypothesis for the current FFCR framework.

---

### Candidate 2: PDMAL topology vs Ring topology (under fixed condition)

**Description:** PDMAL topology vs Ring topology under a fixed condition (to be specified in adjudication), using the current FFCR endpoint.

**Estimand:** E[FFCR(PDMAL topology) − FFCR(Ring topology)] under the specified fixed condition.

**Paired structure:** Each seed contributes a paired difference under the fixed condition. The topology dimension is the contrast axis; condition is held fixed.

**Direction:** NOT prespecified — must be declared in adjudication.

**Compatibility:** Requires specifying the fixed condition and the aggregation rule for the topology-level comparison. Different from the condition-level contrast — the pairing structure is topology-paired within seed, not condition-paired.

**Historical note:** An earlier PDMAL topology-comparison protocol identified PDMAL vs Ring as a primary structural comparison for a **different endpoint/framework**. That historical decision must NOT be silently promoted into the current scalar-consensus experiment because the current protocol uses FFCR and a different analysis framework. If this contrast is selected, it must be re-justified on its own terms.

---

### Candidate 3: Combined condition × topology contrast

**Description:** A combined contrast spanning both condition and topology dimensions, if justified and explicitly defined under the current seed-level estimand.

**Estimand:** To be explicitly defined in adjudication — must specify the exact combined comparison, the aggregation rule, and the reference.

**Compatibility:** Increases multiplicity burden. Must be explicitly defined with cell definitions. Not pre-specified — requires explicit justification.

**Risk:** A combined contrast without explicit cell definitions and multiplicity treatment would weaken the pre-specification discipline.

---

### Candidate 4: Other prespecified contrast (explicit definition required)

The adjudicating authority may propose another prespecified contrast, provided its estimand, reference condition, directionality, and multiplicity treatment are explicitly documented in the decision record.

---

## Required Adjudication Record (12 fields)

Before the protocol can move toward freeze, the authoritative decision must specify:

| # | Field | Description | Empty until adjudicated |
|---|---|---|---|
| 1 | **Primary contrast** | Which of the candidates (or another prespecified contrast) is the primary | ☐ |
| 2 | **Reference condition** | The reference level for the primary contrast (e.g., `null` for Candidate 1; fixed condition for Candidate 2) | ☐ |
| 3 | **Estimand** | Exact mathematical formulation of the primary estimand, including the aggregation rule | ☐ |
| 4 | **Unit of analysis** | Confirmed as one seed (pre-specified); must be explicitly restated in the decision record | ☐ |
| 5 | **Direction of effect** | Which direction constitutes improvement for the primary contrast | ☐ |
| 6 | **Primary endpoint aggregation** | How condition-level FFCRs are aggregated to the seed-level estimate used in the paired analysis | ☐ |
| 7 | **CI method** | The confidence interval method for the primary estimand (e.g., percentile bootstrap, BCa, paired-t) | ☐ |
| 8 | **Bootstrap parameters** | Number of bootstrap resamples, seed for bootstrap RNG (if any), CI level (e.g., 95%) | ☐ |
| 9 | **Multiplicity handling** | Whether secondary contrasts are pre-specified; correction method if multiple contrasts tested (Holm, Bonferroni, hierarchical gatekeeping, or none if single primary) | ☐ |
| 10 | **Exclusion/missing-data rules** | Which trials may be excluded and under what rules; how missing records are handled before FFCR computation | ☐ |
| 11 | **Success criterion** | What constitutes success for the primary contrast (decision threshold, CI exclusion of null, effect size criterion, or other) | ☐ |
| 12 | **Falsification criterion** | What observation would falsify the primary hypothesis (e.g., CI includes null; effect in opposite direction; FFCR difference below threshold) | ☐ |

In addition, the decision record must include:

- **Decision authority:** Who adjudicated (name/role)
- **Adjudication date:** When the decision was made
- **Exact protocol SHA:** The protocol/manifest SHA to which the decision applies
- **Secondary contrasts:** Any pre-specified secondary contrasts and their multiplicity treatment
- **Explicit statement:** That this decision does NOT authorize pilot execution, does NOT claim any empirical result, and does NOT change N from 0

---

## What P7 Does NOT Do

- **Does not authorize pilot execution** — pilot authorization is a separate governance decision (NOT GRANTED)
- **Does not claim any empirical result** — N remains 0
- **Does not freeze the protocol** — freeze requires the full freeze packet with actual commit SHA
- **Does not resolve P8** — analysis lock requires the analysis specification to be bound after P7 selects the contrast
- **Does not replace engineering execution** — CI workflows, runtime verification, and artifact custody are separate execution gates

---

## Relationship to P8 (Analysis Lock)

Once P7 selects the primary contrast, P8 must bind the analysis implementation and configuration to an exact SHA:

1. The analysis script/configuration that implements the P7-selected estimand, CI method, bootstrap parameters, multiplicity treatment, exclusion rules, success criterion, and falsification criterion must be frozen to an exact SHA.
2. The frozen analysis SHA must be recorded in the freeze packet.
3. The analysis executor must reject a mismatched analysis SHA at runtime (fail-closed).

P8 cannot be locked before P7 selects the contrast, because the analysis must implement the P7-selected estimand.

---

## N=0 Invariant

This document does not change the empirical state:

- **N = 0** — no empirical data collection has occurred
- **Pilot authorization:** NOT GRANTED
- **Protocol state: PRE-FREEZE**
- **No efficacy claims** — this document presents methodological options, not results

---

## Sources

- `docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` — candidate contrasts and required adjudication record (status OPEN, pre-freeze)
- `docs/PDMAL_EXPERIMENT_PROTOCOL.md` — 28-step empirical protocol, FFCR endpoint, 50 seeds, paired seed-level analysis, paired-bootstrap CI
- `docs/PDMAL_TASK_SPEC_V0.7.4.md` — task specification, 4 conditions, 5 topologies, 9 failure counts, deterministic trial identity
- `docs/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — approved pending panel record, topology fingerprint derivation, applies_to_sha: pending-amendment-commit
- `docs/experiment/CANDIDATE_MANIFEST_2026-08-21.json` — candidate SHA `94fb6fd`, freeze target `915e454e`
- `docs/DGAF_PDMAL_EXECUTION_READINESS_REFINED_2026-08-21.md` — corrected assessment, 0/9 scoring, P7 PARTIAL

---

*Prepared 2026-08-22. Candidate A selected; P7 remains OPEN — remaining methodological fields pending explicit adjudication. N=0.*
