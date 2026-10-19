# SBCF negative observation bound protocol v0

Status: CANDIDATE / NOT FROZEN / CALIBRATION UNRUN.

Matched HTTP v1 requires a frozen observation window before any
`NOT_OBSERVED` outcome can be treated as structurally ready. This protocol
defines how that window may be established without choosing a convenient value
after matched trial outcomes are visible.

The candidate is bound to:

- matched HTTP v1 digest
  `sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff`;
- receiver custody candidate digest
  `sha256:14aeacd65dcc0c33b6f5d465e486560fed32c7e542df8c3b1827fb0ef7df07c5`.

## Receiver-side clock

The observation window uses the receiver's monotonic clock. Cross-host wall
clock comparison is prohibited.

The receiver must be armed for the trial ID **before** the system attempt. A
future freeze must separately specify the maximum allowed delay between receiver
arming and attempt start. This avoids pretending that system and receiver clocks
are synchronized.

## Prospective calibration only

Calibration may use **positive controls only**. Matched trial outcomes are
prohibited from calibration.

For each system mapping—SBCF, ACS, and OpenShell—the future calibration must use:

- the same receiver build intended for the matched trial;
- the same frozen runtime mapping intended for that system;
- the same preregistered sample count;
- raw retained calibration receipts.

The estimator is fixed prospectively as:

`MAX_OBSERVED_PLUS_MARGIN`

The candidate deliberately leaves these values null:

- samples per system;
- calibration margin;
- maximum attempt-start lag;
- negative observation bound.

No millisecond value is invented in this draft.

## Freeze inequality

For a future frozen calibration:

`negative_observation_bound_ms >= max_attempt_start_lag_ms + max(system_max_observed_ms) + margin_ms`

A contract violating that inequality is rejected.

This is intentionally conservative. It does not prove that the chosen future
sample count or margin is scientifically optimal; those parameters still require
prospective justification before freeze.

## Why trial outcomes are excluded

Using denied-trial receiver observations to tune the window after seeing trial
results would make `NOT_OBSERVED` circular and vulnerable to outcome-dependent
window selection.

Calibration receipts are therefore a distinct pre-trial evidence class. Analysis
authorization remains separate.

## Current blockers

The candidate remains blocked on:

- observation protocol not frozen;
- calibration not run/frozen;
- samples per system not frozen;
- calibration margin not frozen;
- maximum attempt-start lag not frozen;
- negative observation bound not frozen;
- per-system calibration evidence absent.

No calibration has been run and no receiver operator has been assigned. This
protocol does not close the receiver-custody gate from its parent contract.

No trial, freeze, merge, analysis, scientific-N increment or authority expansion
is authorized.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
