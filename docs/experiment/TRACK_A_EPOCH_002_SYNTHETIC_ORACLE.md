# Track A Epoch 002 Synthetic Oracle

Status: **SYNTHETIC ENGINEERING ASSURANCE ONLY**

Controller: #822

Scientific-state effect: **NONE**

This lane exercises the exact frozen Track A Epoch 002 primary-analysis
implementation with deterministic synthetic data whose correct answer is known
before execution. It exists to detect analysis-code, runtime, schema, estimand,
decision-rule, and fail-closed defects before an empirical result is interpreted.

It is intentionally separate from
`scripts/run_track_a_epoch_002_locked_primary_analysis.py`. The synthetic oracle
does not consume the accepted materialized input, does not satisfy the empirical
authorization event, does not create the canonical locked-analysis result record,
and does not alter governance or scientific state.

## Concrete run

The machine-readable definition is
`docs/experiment/TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_RUN.json`.

The dedicated workflow uses Python 3.12.0 and the existing frozen requirements
lock without dependency re-resolution. Before execution it requires the exact
frozen analysis blob, requirements blob, analysis-config digest, and NumPy 2.5.1.

Each oracle scenario has the exact Track A shape: 50 preregistered seed IDs ×
5 topologies × 9 failure counts = 2,250 records. Four independent scenarios are
executed, for 9,000 synthetic records total:

1. positive constant signal: PDMAL 8/9 successes versus random-regular 4/9 for
   every seed; expected paired estimate +4/9 and positive directional support;
2. exact null: 5/9 versus 5/9; expected estimate and interval at zero and an
   inconclusive classification;
3. negative constant signal: 3/9 versus 7/9; expected paired estimate -4/9 and
   evidence against the directional hypothesis;
4. balanced mixed signal: 25 seeds at +1/9 and 25 seeds at -1/9; expected mean
   zero with a two-sided interval spanning zero.

The positive scenario is also replayed under reversed record order and with all
non-primary-topology outcomes inverted. The primary result must remain byte
identical. Every scenario is executed twice and the analysis result must be
deterministic.

Five malformed-input controls must fail closed: one missing matrix cell, one
duplicate matrix cell, a non-boolean endpoint, a wrong algorithm identity, and
an attempted outcome exclusion.

## Evidence artifacts

A successful run produces one uploaded artifact bundle containing:

- `TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_INPUT_MANIFEST.json`;
- its SHA-256 sidecar;
- `TRACK_A_EPOCH_002_SYNTHETIC_ORACLE_RESULT.json`;
- its SHA-256 sidecar;
- `track-a-epoch002-synthetic-oracle-tests.xml`.

The input manifest records deterministic fixture hashes rather than treating
synthetic rows as retained empirical data. The result records exact source and
frozen-analysis bindings, runtime versions, estimates, confidence intervals,
classifications, per-scenario runtimes, deterministic result hashes, invariance
checks, and rejection evidence for all negative controls.

## Required measurable outputs

The run is PASS only when all of the following are true:

- 4/4 known-truth scenarios return their specified estimate/decision behavior;
- 4/4 deterministic replays are byte-identical at the analysis-result level;
- record-order invariance passes;
- non-primary-topology outcome invariance passes;
- 5/5 malformed-input controls are rejected for the expected contract reason;
- 9,000 synthetic oracle records are exercised;
- the exact 50-seed paired bootstrap remains fixed at 10,000 resamples,
  seed 20270251, alpha 0.05;
- both JSON artifacts verify against their SHA-256 sidecars;
- the frozen analysis blob/config, dependency lock, Python 3.12.0, and
  NumPy 2.5.1 remain exact.

Runtime in milliseconds is measured per scenario and replay but is reported as
engineering telemetry, not used as a scientific or production-performance claim.

## Fail-closed boundary

Every emitted result must preserve:

- `classification=SYNTHETIC_ENGINEERING_ASSURANCE_ONLY`;
- `empirical_data_used=false`;
- `protected_material_used=false`;
- `real_primary_analysis_performed=false`;
- `scientific_n_increment=0`;
- `canonical_dgaf_efficacy=NOT_ESTABLISHED`;
- `independent_validation=NOT_ESTABLISHED`;
- `high_assurance=NOT_AUTHORIZED_N0`.

A PASS establishes only that the frozen analysis code path behaved correctly on
the specified known-truth synthetic fixtures and rejected the specified malformed
fixtures. It does not predict the empirical result or establish DGAF efficacy.
