---
status: OPEN
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-21
applies_to_sha: 2824d4974567532f3a0579e15b63e9c860edac21
---

# PDMAL Primary Contrast Adjudication

## Status

**OPEN / METHODOLOGICAL ADJUDICATION REQUIRED**

This document records an unresolved methodological decision required before the PDMAL scalar-consensus experiment can be frozen. It does not select a primary contrast, authorize pilot execution, establish efficacy, or change the current empirical state.

## Current protocol framework

- Primary endpoint: **FFCR**.
- Statistical unit: one seed.
- Seed-level effect: paired difference in condition-level FFCR according to the approved aggregation rule.
- Primary inference framework: seed-level paired analysis with paired-bootstrap confidence interval, subject to final adjudication.
- Pilot matrix: 4 conditions × 5 topologies × 9 failure-count levels.
- Planned seeds: 50.

The primary contrast must be selected so that it is compatible with the final estimand, pairing structure, and multiplicity plan.

## Historical contrast boundary

An earlier PDMAL topology-comparison protocol identified **PDMAL vs Ring** as a primary structural comparison for a different endpoint/framework. That decision must not be silently inherited into the current FFCR experiment.

## Candidate contrasts

1. `dgaf` vs `null` at the condition level.
2. PDMAL topology vs Ring under a fixed condition with the current FFCR endpoint.
3. A combined condition/topology contrast if scientifically justified and explicitly defined.
4. Another prespecified contrast with explicit estimand, reference, direction, and multiplicity treatment.

These are candidates only, not approved hypotheses.

## Required adjudication record

Before freeze, the authoritative decision must specify:

- chosen primary contrast;
- treatment/reference definitions;
- exact mathematical estimand and aggregation rule;
- direction of improvement;
- relationship to seed-level pairing;
- compatibility with paired-bootstrap inference;
- secondary contrasts;
- multiplicity treatment;
- success and falsification criteria;
- decision authority and date;
- exact protocol/manifest identity to which the decision applies.

## Freeze boundary

The protocol remains **PRE-FREEZE** until this decision is explicitly adjudicated and incorporated into the freeze packet.

Pilot authorization remains separate and is **NOT GRANTED**. Empirical data remain `N = 0` until authorized pilot execution occurs.
