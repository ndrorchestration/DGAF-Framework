# P7 Primary Contrast Adjudication Packet — Adopted 2026-08-23

## Purpose

Provide the bounded scientific decision record for the current FFCR experiment. The primary contrast and associated scientific decisions were adjudicated through the P7 process. This packet does not authorize execution and does not create a protocol freeze.

> **Current-status clarification:** P7 scientific content is treated as technically adjudicated, but formal freeze binding remains OPEN. The older panel-ready traceability record is retained as provenance; current P7 status must be read together with the completion adjudication and exact candidate-binding evidence.

## Adopted primary contrast

### DGAF vs null

**Primary contrast:** full `dgaf` condition versus `null` condition.

**Primary question:** Does the DGAF condition change FFCR relative to the null condition under the current execution contract?

**Treatment:** `dgaf`, the full DGAF configuration defined by the candidate apparatus.

**Reference:** `null`, the baseline configuration with no DGAF.

**Primary endpoint:** FFCR (Failure-Free Completion Rate), higher is better.

**Statistical unit:** seed.

**Primary aggregation:** for each seed and condition, aggregate the condition's trial-level FFCR observations across the registered topology × failure-count matrix (5 topologies × 9 failure-count levels) into one seed-level condition FFCR. The primary seed-level difference is:

`Delta_s = FFCR_s(dgaf) - FFCR_s(null)`

The primary estimand is the expected seed-level paired difference over the pre-specified seed population:

`Delta = E_s[Delta_s]`

No topology or failure-level weighting may be changed after observing pilot results.

**Direction:** positive `Delta` favors DGAF; zero indicates no average difference; negative `Delta` favors null.

## Inference contract

- Primary inference unit: the 50 pre-specified seeds.
- Pairing: `dgaf` and `null` observations from the same seed are paired; seed identity is the pairing key.
- Confidence interval: paired bootstrap over the 50 seed-level differences, resampling seeds with replacement.
- The executable bootstrap count, interval convention, RNG policy, and exact implementation/configuration identity must be recorded and verified in P8 before unblinding or empirical interpretation.
- Empirical data remain `N = 0` until separate pilot authorization and execution.

## Secondary / exploratory family

The following are secondary/exploratory and cannot replace the primary contrast:

1. PDMAL topology vs Ring.
2. Condition × topology interaction.
3. Other structural/execution diagnostics, including `final_std`, `D_a`-style diagnostics, and phi-convergence traces.

No secondary contrast is a confirmatory success criterion unless separately adjudicated and multiplicity-controlled before analysis.

## Exclusion and missing-data boundary

- Exclusions must be deterministic, protocol-defined, and applied before primary inference.
- No seed may be excluded because its observed outcome is unfavorable to DGAF.
- Missing or invalid trial records must be classified using the execution/artifact contract before the seed-level aggregate is calculated.
- A seed-level primary value cannot be silently imputed.
- Any rule that changes the eligible seed population must be recorded before unblinding and invalidates the current P8 lock if changed afterward.

## Decision criteria

The primary result must be reported with its point estimate and confidence interval. A result supports the pre-specified directional DGAF hypothesis only when the locked decision rule is satisfied; absence of such support is not evidence of production efficacy or ineffectiveness.

The exact numerical success threshold, interval convention, bootstrap count, and RNG policy are implementation-lock fields where applicable and must be bound before observing pilot outcomes.

## Historical boundary

The historical PDMAL-vs-Ring contrast is evidence about the historical apparatus, not an automatic current hypothesis, expected direction, or success criterion.

## Protocol reconciliation

The governing experiment protocol describes the study as controlled runtime characterization containing a pre-specified comparative DGAF-versus-null analysis. The comparative analysis does not convert historical characterization artifacts into efficacy evidence and does not establish production or real-world effectiveness.

## Status

**P7 scientific specification: TECHNICALLY ADJUDICATED / FORMALLY OPEN FOR FREEZE BINDING.**

The primary contrast is selected and the scientific decision record is available for binding. P8 must bind the executable analysis implementation path, implementation SHA, configuration SHA, bootstrap parameters, RNG policy, interval convention, and exact protocol/manifest identity before any unblinding or empirical interpretation.

Pilot authorization remains **NOT GRANTED**. Empirical `N = 0`. New freeze remains **NOT CREATED**.
