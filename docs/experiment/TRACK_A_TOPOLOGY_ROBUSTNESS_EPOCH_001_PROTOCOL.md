# Track A topology robustness — Epoch 001 prospective protocol

Controller: #410

## Status

**PROPOSAL ONLY · PRE-FREEZE · NOT AUTHORIZED · scientific N increment 0**

Protocol ID: `PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001`

This protocol tests topology, not integrated DGAF. The update algorithm is fixed as `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1` for every topology. Semantic DGAF gates and all Track B/Track C claims are outside scope.

## Research question and primary hypothesis

Question: under the fixed reference neighbor-mean algorithm, does the PDMAL dodecahedral topology produce a higher seed-level failure-free completion rate than a degree- and edge-matched random-regular topology across the fixed node-failure panel?

Primary directional hypothesis:

`mean[FFCR_pdmal(seed) - FFCR_random_regular(seed)] > 0`

PDMAL and random-regular are the primary matched comparison because both have 20 nodes, 30 edges and degree 3. Ring, small-world and complete remain in the matrix for descriptive context only.

## Frozen proposal matrix

- Algorithm: reference neighbor mean, alpha `0.5`.
- Topologies: ring, PDMAL, random-regular, small-world and complete.
- Failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`.
- Fresh seed identifiers: `20261301..20261350` inclusive. They are opaque integers, not dates.
- Cells per seed: `5 × 9 = 45`.
- Proposed observations if later authorized: `50 × 45 = 2,250`.
- Historical pooling: prohibited.

The seed panel is disjoint from experiment 001, Epoch 003, Epoch 004 and the later diagnostic-only panels recorded in repository governance.

## Endpoint and estimand

The primary trial endpoint is the existing boolean `ffcr_success`: true only when final standard deviation is below `0.01` after the fixed 100 iterations and execution status is successful. Missing or malformed outcomes fail closed and are never reconstructed.

For each seed and each primary topology, FFCR is the proportion of successful trials across the nine failure counts. The paired seed effect is:

`delta(seed) = FFCR_pdmal(seed) - FFCR_random_regular(seed)`

The primary estimand is the equal-weight mean of the 50 complete paired seed effects.

## Locked analysis rule

- Two-sided 95% percentile bootstrap interval over complete paired seed effects.
- 10,000 resamples.
- Bootstrap RNG seed `20260908`.
- Directional support only if the point estimate is positive and the interval lower bound is above zero.
- Evidence against only if the point estimate is non-positive and the interval upper bound is below zero.
- Otherwise the result is inconclusive.
- No complete-case deletion: any missing seed fails collection QC.
- All other topology and failure-count summaries are exploratory/descriptive and cannot replace the primary result.

The analysis implementation is intentionally absent from this proposal. A later PR must implement these exact rules and bind its source hash before candidate freeze.

## Sample-size boundary

Fifty paired seeds are fixed prospectively as a pragmatic pilot size aligned with the established harness. No minimum detectable effect or outcome-derived power claim is made. Precision is communicated by the locked confidence interval; seed count cannot be changed after outcomes are generated.

## QC, blinding and custody

Collection must fail closed unless all 2,250 unique cells and all 50 complete seeds exist, topology invariants pass, execution produces no errors, environment identity is recorded, and every seed artifact has a checksum.

Topology labels must remain blinded in analysis-facing artifacts using a protected HMAC-SHA-256 mapping/order. Dataset and key artifacts remain separate. The blinded dataset must be structurally locked before a separate unblinding authorization. Solo same-system custody is labeled non-independent.

## Remaining gates

This proposal does not include an analysis implementation, runner, candidate SHA, freeze manifest, collection request or unblinding request. Required order:

1. merge this prospective protocol after exact-head validation;
2. implement and test the exact locked analysis and runner without collecting data;
3. run non-empirical treatment/input and blinding preflight;
4. designate the exact executable candidate and bind all source hashes;
5. close candidate-scoped reproducibility, security and custody checks;
6. create the immutable freeze record;
7. record a separate exact-commit pilot authorization;
8. collect blinded data;
9. lock and independently inspect structure before any unblinding decision.

`TRACK_A_FREEZE = NOT ESTABLISHED`

`TRACK_A_EMPIRICAL_EXECUTION = NOT AUTHORIZED`

`HIGH_ASSURANCE = NOT AUTHORIZED / N=0`
