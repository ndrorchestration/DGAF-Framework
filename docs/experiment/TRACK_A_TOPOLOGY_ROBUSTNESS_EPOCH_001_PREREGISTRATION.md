# Track A topology-robustness Epoch 001 — preregistration proposal

Controller: Issue #410

## Status

`PROPOSAL_ONLY / EMPIRICAL EXECUTION NOT AUTHORIZED / SCIENTIFIC_N_INCREMENT=0`

This protocol defines the first prospective empirical Track A test after the structural matrix adjudication merged in PR #409. It does not implement a runner, freeze a collection candidate, authorize execution, unblind data, or establish any DGAF efficacy claim.

## Exact source boundary

- Workload architecture merge: `5e4f00a065c00cefec0b3a79c32b88a5f36a55c2`
- Track A profile merge: `b1e333ee9f9e0a4da78788e5ff019603296888eb`
- Track A qualification merge: `647f612a2412818dca0d632229f352e857e1187e`
- Track A structural adjudication merge: `ccabc065d0c1d183e1954ea36a947289fb084831`
- Profile: `PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1`
- Neutral algorithm: `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`
- Retained structural artifact: `10041800252`
- Structural archive digest: `sha256:629ee0be7a48606685f2452800ab4e482611fb45f7268d881e934488e1c1c1d5`
- Structural payload SHA-256: `e51497d150530d983f94002d23a21608be9135ca300d29a47b126ed184fdc489`

The neutral reference algorithm is not an integrated DGAF treatment and no semantic DGAF gate is part of this Track A condition.

## Research question and directional hypothesis

**Question:** under the fixed reference neighbor-mean alpha-0.5 consensus algorithm, does the PDMAL topology produce higher failure-and-recovery success than a matched random-regular topology across the fixed failure-count panel?

**Directional hypothesis:** `PDMAL_TOPOLOGY_FFCR_GREATER_THAN_RANDOM_REGULAR`.

## Fixed matrix

- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0,1,2,3,4,5,6,8,10`
- Fresh seeds: `20270101..20270150`
- Paired seed units: `50`
- Cells per seed: `5 × 9 = 45`
- Expected observations: `2,250`

The seed panel is fixed before outcomes and is disjoint from experiment 001, Epoch 003, Epoch 004, and Track A diagnostic seeds `20261201` and `20261202`.

## Primary endpoint and estimand

The primary endpoint is boolean `ffcr_success` under the pre-existing fixed convergence contract.

For each seed:

1. compute PDMAL FFCR as the mean of `ffcr_success` across the nine registered failure counts;
2. compute random-regular FFCR the same way;
3. compute the paired seed effect as PDMAL FFCR minus random-regular FFCR.

The primary estimand is the mean of the 50 paired seed effects.

Primary uncertainty and decision rule:

- paired-seed percentile bootstrap;
- `10,000` resamples;
- bootstrap RNG seed `20270151`;
- two-sided 95% percentile interval;
- directional support only when the point estimate is positive and the lower CI bound is above zero;
- directional negative evidence only when the point estimate is negative and the upper CI bound is below zero;
- otherwise the result is inconclusive or not directionally supported.

## Multiplicity policy

There is exactly one confirmatory comparison: **PDMAL vs random-regular**.

All other topology contrasts, failure-count-specific contrasts, subgroup analyses, and mechanism analyses are exploratory only. No exploratory result may be relabeled confirmatory after outcome inspection.

## Sample-size rationale

The first Track A empirical epoch fixes 50 paired seed units prospectively. This preserves the established PDMAL experimental scale while reducing the scientific question to one algorithm and one confirmatory topology contrast. No formal power claim is made. Precision and directional interpretation are governed by the preregistered paired-bootstrap interval.

## Prospective QC

Confirmatory analysis fails closed unless all of the following hold:

- exactly 50 registered seeds;
- exactly five registered topologies;
- exactly nine registered failure counts;
- exactly 2,250 observations;
- exactly one record for each seed × topology × failure-count cell;
- no duplicate cells;
- boolean `ffcr_success`;
- exact neutral algorithm identity;
- retained environment fingerprint;
- per-seed integrity sidecar;
- no outcome-based exclusion.

Missing or malformed cells prohibit confirmatory analysis rather than being silently imputed or dropped.

## Blinding and custody

The protocol requires analysis-label blinding, but it does **not** claim that topology identity is fully concealable from structural information.

A fresh label-mapping key must be generated only after protocol freeze, stored separately from the blinded dataset, and withheld until the blinded dataset passes its structural lock. Same-developer custody is explicitly non-independent. Key release requires a separate unblinding authorization.

No outcome inspection is permitted before the structural dataset lock.

## Historical evidence separation

Experiment 001, Epoch 003, Epoch 004, and the two Track A diagnostic seeds remain separate evidence. They may not be pooled into this epoch or used to retune the endpoint, seed panel, primary contrast, bootstrap rule, or interpretation threshold.

## Claim ceiling

If later separately frozen, authorized, and executed, this epoch may support only a claim about **PDMAL vs random-regular topology robustness under the exact frozen reference algorithm and protocol**.

It cannot establish:

- canonical DGAF efficacy;
- integrated Track C behavior;
- independent validation;
- High-Assurance acceptance;
- production readiness.

## Remaining gates

1. merge this proposal after complete exact-head validation;
2. create and lock the Track A analysis implementation before collection;
3. implement the empirical runner in a separate PR;
4. add precollection source/matrix/QC validation and negative controls;
5. freeze the exact empirical candidate;
6. generate fresh blinding material after freeze;
7. create a separate exact-commit collection authorization;
8. collect only after every preceding gate passes;
9. structurally lock the blinded dataset before any key release;
10. separately authorize unblinding and only then run the locked primary analysis.

`TRACK_A_PROTOCOL = PROPOSAL_ONLY`

`TRACK_A_FREEZE = NOT_ESTABLISHED`

`TRACK_A_EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED / N=0`
