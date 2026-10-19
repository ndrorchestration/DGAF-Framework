# SBCF prospective one-sided tolerance preregistration v0

Status: CANDIDATE / NOT FROZEN / ZERO CALIBRATION OBSERVATIONS.

This child of the matched HTTP calibration receiver (#1410) defines the
**prospective statistical design gate** for positive-control timing calibration.
No coverage, confidence, sample count, margin, receiver build, runtime mapping,
independent operator or observation-bound value is selected or authorized here.

## Exact parents

The closed fixture is bound to the parent contract digests:

- matched HTTP v1: `sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff`;
- receiver custody: `sha256:14aeacd65dcc0c33b6f5d465e486560fed32c7e542df8c3b1827fb0ef7df07c5`;
- negative-observation protocol: `sha256:d01d33de9f14d9bdace222528325d5766f5422088c8a4fa4c109adc1465e55cf`;
- calibration receiver: `sha256:3d05f5c94a0aca51fd8b80fe20e4acb84330e649b5e7a1251064fd9721aa0cd5`.

## Statistical rationale

For independent identically distributed positive-control latencies from a stable
target population, the maximum of `n` observations can be used as a one-sided,
distribution-free *upper statistical tolerance limit*. If `p` is the desired
proportion of the target population below the sample maximum and `gamma` is
the desired confidence level, the sample-size condition is:

`1 - p**n >= gamma`.

The minimal `n` is derived *after* the scientific coverage/confidence pair is
prospectively justified and registered. This is a population-coverage confidence
statement, **not** a guaranteed bound on every future latency, a proof of no
false negatives, or a confidence interval for the mean.

Primary statistical references:

- NIST/SEMATECH Engineering Statistics Handbook,
  <https://itl.nist.gov/div898/handbook/prc/section2/prc264.htm>:
  distribution-free tolerance intervals based on order statistics;
- NIST/SEMATECH Engineering Statistics Handbook,
  <https://www.itl.nist.gov/div898/handbook/prc/section2/prc263.htm>:
  distinction between tolerance limits and mean confidence intervals.

The NIST handbook includes a *two-sided* minimum/maximum formula. This
candidate uses the distinct **one-sided maximum** relation above, derived
directly from the probability that all `n` IID values lie below the
`p`-population quantile. The two-sided formula must not be substituted for
this one-sided sample-size rule.

## Exact bounded calculator

The calculator accepts exact decimal **strings** `0.x` (one to six digits
after the decimal) and uses rational arithmetic. Floats, booleans, values
outside `(0,1)`, malformed decimals and post-hoc target selection are
rejected. The smallest sufficient positive integer is obtained with an exact
binary-search inequality, not floating-point rounding.

It refuses requirements exceeding 100,000 samples per system. This is an
explicit **implementation resource ceiling**, not a statistical recommendation
or a selected sample budget.

Unit-test-only illustrations (not research selections):

| Hypothetical coverage | Hypothetical confidence | Minimum IID controls |
| --- | --- | --- |
| 0.90 | 0.90 | 22 |
| 0.95 | 0.95 | 59 |
| 0.99 | 0.95 | 299 |
| 0.99 | 0.99 | 459 |

The candidate fixture leaves every actual value null.

## Assumptions and validity limits

A mathematically sufficient `n` does **not** show that actual calibration
observations meet the theorem's conditions.

Before freeze, a separate sampling-design artifact must address:

- why positive-control samples can reasonably be treated as independent and
  identically distributed rather than correlated retries;
- stability of receiver build, runtime mapping, host/network conditions and
  workload population over the sampling period;
- exact treatment of timeouts, censored measurements and missing receipts
  without silently discarding slow controls;
- warm-up, run order, reset/restart policy and any sampling stratification;
- receiver-monotonic clocks and same predeclared measurement protocol;
- evidence of representativeness for the future matched-trial conditions.

The fixture records these as **requirements**, not satisfied empirical facts.
A hypothetical structural `FROZEN` test state can document the design but
still labels sampling assumptions `DOCUMENTED_UNVERIFIED`.

The sample-size relation applies separately to each system's calibration
population. It does **not** automatically provide a simultaneous confidence
guarantee for all three systems, nor a guarantee for non-stationary conditions.
Any familywise coverage criterion or failure-posture strata must be specified
prospectively by the study designer; this module does not assume a correction.

No receiver custody, independent validation, scientific efficacy, network
containment or run authorization follows from structural readiness.

## Closed freeze gate

The actual candidate remains `CANDIDATE_NOT_FROZEN`. It blocks on:

- `coverage_confidence_target_unselected`;
- `sampling_design_unassessed`;
- `sample_count_unset`;
- `sample_budget_unset`;
- `tolerance_preregistration_not_frozen`.

A future structurally frozen packet must include a written prospective
scientific rationale for the coverage/confidence pair, a documented sampling
design identity, and an integer planned sample count at least the **exact**
calculated minimum, within its declared budget. Equal per-system counts and
pre-calibration registration remain mandatory.

Matched-trial outcomes are prohibited from target selection or calibration.
External custody, retention, runtime mapping freeze and adjudication remain
separate gates.

## QA and first observation

Initial focused test suite: **32 passed**. Initial static checks:
Black reported two formatting deltas and flake8 reported one 123-character test
line; isort and mypy passed. Only Black formatting was applied, after which
focused tests and all Black/isort/flake8/mypy gates passed.

A final type-coercion review identified that Python compares integer zero equal
to Boolean false. The outcome-selection firewall now explicitly requires
`is False`, with a regression test rejecting `0`; fixture bytes are unchanged.

Final complete SBCF suite: **293 passed / 7 strict xfailed / 37 subtests**.
Bandit blocking threshold, JSON parsing, Markdown lint and diff checks passed
after this type-hardening follow-up. Final focused tests: **33 passed**.

The candidate fixture digest is
`sha256:e65c715973577ac4877407b478750f7e98a8b7cbd03eeee920e4683a6919ce91`.

This is a synthetic mathematical contract test only. No empirical calibration
or matched-system execution was performed.

## Invariants

Pre-freeze / fail-closed / not authorized. No merge, calibrated bound, trial,
analysis, independent adjudication or efficacy promotion is authorized.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
