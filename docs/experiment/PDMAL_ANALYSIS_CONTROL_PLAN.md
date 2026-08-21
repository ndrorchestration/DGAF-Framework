# PDMAL Analysis Control Plan

**State:** PRE-FREEZE
**Purpose:** Repository-local statistical-analysis boundary. This document does not assert an analysis result and does not authorize execution.

## Current design

- Construct: FFCR (failure-free completion proportion per condition per seed).
- Primary endpoint: FFCR per condition, per seed.
- Statistical unit: seed.
- Planned pilot: 50 seeds.
- Trial matrix: 4 conditions × 5 topologies × 9 failure-count levels = 180 trials/seed.
- Planned raw records: 9,000.
- Primary inference: seed-level paired difference with paired-bootstrap confidence interval, subject to primary-contrast adjudication.

## Target specification required before freeze

The authoritative decision must record:

1. primary contrast;
2. treatment and reference definitions;
3. exact mathematical estimand and aggregation rule;
4. direction of improvement;
5. alpha and interval convention;
6. secondary contrast family;
7. multiplicity correction;
8. exclusion and missing-data rules;
9. bootstrap parameters and seed policy;
10. decision authority and date;
11. exact protocol/manifest identity to which the decision applies.

## Analysis lock

Before authorization and before any unblinding, record:

- analysis implementation path;
- analysis implementation SHA;
- configuration SHA;
- exact primary contrast;
- secondary-contrast family definitions;
- exclusion/missing-data rules;
- bootstrap parameters and random-seed policy;
- multiplicity procedure.

No post-unblinding change to these items is permitted without invalidating the analysis lock and triggering a new governance decision.

## Planning utility

`experiments/pdmal_pilot/sample_size.py` remains a planning utility only. It does not read or modify pilot observations and does not establish empirical support.

## Epistemic boundary

Acceptance, characterization, and smoke-test observations are non-empirical infrastructure evidence. Empirical N remains `0` until explicit authorization followed by pilot execution.
