---
status: ACTIVE
state: PRE-FREEZE RECONCILIATION
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-19
applies_to_sha: reconciliation branch
---

# PDMAL Freeze Readiness Reconciliation — 2026-08-19

## Purpose

This record reconciles the final documentation and definitional seams identified by the adversarial freeze-readiness audit. It preserves historical findings rather than rewriting them and distinguishes documentation closure from methodological adjudication.

## Current disposition

| Item | Disposition | Evidence / next action |
|---|---|---|
| Matrix v0.7.5 acceptance/inclusion contradiction | CLOSED | Amendment now records `ACCEPTED / INCORPORATED` into merge baseline `915e454e...`; current-state and freeze manifest synchronized on this branch. |
| Seed-level FFCR aggregation | DEFINED / INCORPORATION REQUIRED | Exact 45-cell aggregation rule is now recorded in `CURRENT_STATE.md` and `FREEZE_MANIFEST.md`; authoritative protocol must carry the same rule before freeze. |
| Primary contrast hierarchy | OPEN / METHODOLOGICAL ADJUDICATION REQUIRED | The current protocol specifies prespecified contrasts and paired-bootstrap primary inference but does not establish `dgaf` vs `null` as the sole primary contrast. No new contrast is silently promoted. |
| Stale documentation-gap audit | RECONCILED BY THIS RECORD | Prior findings remain historical; current status is superseded by later runtime, blinding, and implementation evidence where applicable. |
| Lifecycle registry | CLOSED | `FREEZE_MANIFEST.md` is now registered as ACTIVE / PRE-FREEZE; reconciliation record is registered as ACTIVE / PRE-FREEZE. |
| Secondary endpoint family wording | CLOSED | Freeze manifest now lists the complete secondary family and identifies `final_std < 0.01` as a secondary consensus-quality diagnostic, not the overall success definition. |
| SHA labeling ambiguity | CLOSED | Current-state record distinguishes authoritative merge baseline, latest main documentation synchronization commit, and current reconciliation branch. Historical execution SHAs remain attached to exact evidence. |
| Topology fingerprints | CONTROL ADDED / VALUES REQUIRED AT FREEZE | Freeze manifest now contains an explicit generated-topology-fingerprint field. Exact fingerprints must be populated from verified artifacts before freeze. |
| NotebookLM authority boundary | CLOSED | Lifecycle/evidence policy now treats NotebookLM as research synthesis/reference only; independent incorporation is required for evidentiary authority. |
| `dgaf` architectural boundary | CLOSED | Freeze manifest explicitly limits the `dgaf` condition claim to verified adapter behavior under the frozen workload. |

## FFCR aggregation contract

For each seed and condition, 45 component workload cells are present: five topologies crossed with nine failure-count levels.

```text
FFCR_condition,seed =
    successful eligible component trials
    /
    eligible component trials
```

Each component trial receives equal weight. No topology-first or failure-level-first average is applied before computing the seed-level FFCR.

**Eligible trial:** an attempted trial, including execution-level retries, that is not excluded under the frozen objective exclusion rules.

**Excluded trial:** an objectively invalid protocol execution meeting a pre-registered exclusion rule. The raw record remains retained with an explicit reason and is removed from the FFCR denominator only when that rule applies.

A valid unfavorable outcome is never excluded because of its result.

Failure count `0` remains part of the primary workload and is included in the denominator as the no-failure baseline condition.

## Statistical-analysis boundary

The current authoritative protocol defines:

- one seed as one paired experimental block;
- one FFCR proportion per condition per seed;
- the primary estimand as the mean paired seed-level FFCR difference for each prespecified primary contrast;
- the primary confidence interval as a prespecified paired bootstrap confidence interval;
- the paired t-test only as a sensitivity/reference calculation where diagnostics support it.

This reconciliation record does **not** create a new primary contrast. The commonly proposed `dgaf - null` contrast remains an adjudication candidate until explicitly supported by the existing panel/statistical authority or formally adjudicated before freeze.

## Historical documentation-gap reconciliation

Earlier audit findings that were subsequently closed remain historical. They are not deleted or rewritten to imply that the control was always closed. Current closure is established by later evidence, including:

- ConsensusTask verification Run #74;
- runtime characterization Run #14, 72/72 trials and 300-second ceiling pass;
- blinding operational verification Run `32113226935`;
- environment/topology/schema verification reflected in the current control state.

Remaining freeze controls are not empirical claims and do not change `N = 0`.

## Freeze boundary

The following remain mandatory before a genuine `FROZEN` state may be asserted:

1. Explicit primary contrast adjudication.
2. Incorporation of the FFCR aggregation rule into the authoritative protocol text.
3. Exact protocol/task/runner/topology/environment provenance identifiers.
4. Verified durable research retention and retrieval.
5. Final freeze metadata and dedicated freeze commit.
6. Independent exact-state verification of the resulting freeze commit.

Pilot authorization remains a separate post-freeze governance decision.

## Epistemic boundary

This reconciliation closes documentation seams and identifies the remaining methodological decision. It does not establish PDMAL efficacy, comparative superiority, convergence, robustness, or real-world benefit. Empirical data remains `N = 0` until explicitly authorized execution occurs.
