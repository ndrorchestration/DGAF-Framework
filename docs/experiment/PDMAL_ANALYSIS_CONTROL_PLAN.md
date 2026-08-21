# PDMAL Analysis Control Plan

## Repository status

This file is the repository-local control record for the statistical analysis boundary. It does not claim that an external expert-agent analysis document is present in this repository unless its path and SHA are recorded below.

## Current executable planning basis

`experiments/pdmal_pilot/sample_size.py` implements a paired-difference normal-approximation planning utility with defaults:

- alpha = 0.05
- power = 0.80
- minimum detectable difference = 0.15
- externally supplied paired-difference SD

The utility is explicitly a planning tool and does not read or modify observed pilot data.

## Prespecified experimental structure

- Primary endpoint: FFCR.
- Statistical unit: seed.
- Planned pilot: 50 seeds.
- Matrix: 4 conditions × 5 topologies × 9 failure-count levels.
- Observations: 9,000 raw trial records before exclusions.
- Primary inference: seed-level paired analysis with paired-bootstrap confidence interval, subject to final adjudication of the primary contrast.

## Multiplicity

The final analysis implementation must explicitly encode the approved family structure and Holm-Bonferroni correction before unblinding. No post-unblinding changes are permitted.

## Required analysis lock

Before authorization/unblinding, record:

1. analysis implementation path;
2. analysis implementation SHA;
3. configuration SHA;
4. exact primary contrast;
5. secondary contrast family definitions;
6. exclusion and missing-data rules;
7. bootstrap parameters and random-seed policy;
8. multiplicity procedure;
9. sample-size rationale and external SD source, if applicable.

## Evidence-location reconciliation

The previously reported files `PDMAL_STATISTICAL_ANALYSIS_PLAN.md` and `PDMAL_PIPELINE_SPEC.md` were not found at the expected repository paths during the 2026-08-20 GitHub audit. Their exact repository locations and SHAs must be established before they can be treated as repository-authoritative evidence.

## Epistemic boundary

No analysis result is asserted here. Acceptance/dry-run observations remain characterization evidence and do not enter empirical N. Pilot data remain `N = 0` until explicitly authorized execution occurs.
