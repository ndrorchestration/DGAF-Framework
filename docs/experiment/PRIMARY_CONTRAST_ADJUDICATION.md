---
status: OPEN
state: PRE-FREEZE
authority: DGAF/PDMAL experimental-control
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-19
applies_to_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
---

# PDMAL Primary Contrast Adjudication

## Status

**OPEN / METHODOLOGICAL ADJUDICATION REQUIRED**

This document records an unresolved methodological decision required before the PDMAL scalar-consensus experiment can be frozen. It does **not** select a primary contrast, authorize pilot execution, establish efficacy, or change the current empirical state.

## Current protocol framework

The current PDMAL pilot defines:

- Primary endpoint: **FFCR**.
- Statistical unit: one seed.
- Seed-level effect: paired difference in condition-level FFCR according to the frozen aggregation rule.
- Primary inference framework: the prespecified paired seed-level analysis and paired-bootstrap confidence interval.
- Pilot matrix: 4 conditions × 5 topologies × 9 failure-count levels.
- Planned seeds: 50.

The primary contrast must be selected so that it is compatible with this current estimand and analysis framework.

## Historical contrast that must not be silently inherited

An earlier PDMAL topology-comparison protocol identified **PDMAL vs Ring** as a primary structural comparison for a different endpoint/framework. That historical decision must not be silently promoted into the current scalar-consensus experiment because the current protocol uses FFCR and a different analysis framework.

## Candidate primary contrasts for adjudication

The expert/statistical authority may consider, at minimum:

1. `dgaf` vs `null` at the condition level, aggregated according to the current FFCR estimand.
2. PDMAL topology vs Ring topology under a fixed condition, with the current FFCR endpoint.
3. A combined condition/topology contrast, if justified and explicitly defined under the current seed-level estimand.
4. Another prespecified contrast, provided its estimand, reference condition, directionality, and multiplicity treatment are explicitly documented.

These are **candidate options only**, not approved hypotheses or primary analyses.

## Required adjudication record

Before freeze, the authoritative decision must specify:

- chosen primary contrast;
- treatment and reference definitions;
- exact mathematical estimand;
- direction of improvement;
- relationship to the seed-level pairing;
- compatibility with the paired-bootstrap analysis;
- secondary contrasts;
- multiplicity treatment;
- decision authority and date;
- exact protocol/manifest SHA to which the decision applies.

## Freeze boundary

The protocol must remain **PRE-FREEZE** until this methodological decision is explicitly adjudicated and incorporated into the freeze packet.

Pilot authorization remains separate and is **NOT GRANTED** by this document.

Empirical data remain `N = 0` until authorized pilot execution occurs.
