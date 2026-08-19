---
status: OPEN
state: PRE-FREEZE METHODOLOGICAL ADJUDICATION REQUIRED
authority: Expert panel / statistical-design authority
owner: DGAF/PDMAL experimental-design control
last_verified: 2026-08-19
applies_to_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
---

# PDMAL Primary Contrast Adjudication

## Purpose

Record the explicit pre-freeze decision that determines the primary confirmatory contrast for the 50-seed PDMAL pilot.

## Current established statistical framework

The current protocol already establishes:

- statistical unit: one seed = one paired experimental block;
- condition-level outcome: `FFCR_condition,seed`;
- primary effect scale: raw paired FFCR difference on the 0–1 scale;
- primary confidence interval: prespecified 95% paired bootstrap confidence interval;
- secondary analyses remain subject to the frozen multiplicity procedure.

The adjudication below must select the primary contrast without changing those established elements unless a formal protocol amendment is approved before freeze.

## Current decision

**OPEN — NO PRIMARY CONTRAST HAS YET BEEN FORMALLY ADJUDICATED.**

The current protocol does not independently establish `dgaf` vs `null` as the sole primary contrast. No contrast is to be promoted to confirmatory status by implication, implementation convenience, or post-hoc preference.

## Candidate contrasts for panel/statistical review

Examples include:

- `dgaf` vs `null` across the frozen topology/failure-count workload;
- PDMAL topology vs Ring with condition held fixed;
- `dgaf` on PDMAL topology vs `null` on Ring topology;
- another contrast explicitly justified by the preregistered research question and frozen statistical design.

This list is not a ranking and does not itself constitute a preregistered comparison hierarchy.

## Required adjudication

The authorized panel/statistical-design authority must record:

1. the single primary confirmatory contrast;
2. the exact treatment and reference conditions/factors;
3. the factor aggregation rule, consistent with the frozen seed-level FFCR definition;
4. the corresponding paired seed-level difference;
5. the role of all secondary contrasts and their multiplicity treatment;
6. the decision date, authority, and evidence record.

## Freeze gate

This record must be changed from `OPEN` to an explicitly adjudicated state before the PDMAL protocol can enter `FROZEN` status.

## Evidence boundary

This record is methodological governance only. It does not establish empirical efficacy and does not authorize pilot execution. Empirical data remains `N = 0` while this adjudication is open.
