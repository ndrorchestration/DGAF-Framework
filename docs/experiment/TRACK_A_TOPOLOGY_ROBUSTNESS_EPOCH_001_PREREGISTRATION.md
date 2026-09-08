# Track A topology-robustness Epoch 001 preregistration

Controller: #410

## Decision

**PROPOSAL ONLY — prospectively preregister Track A; do not authorize collection.**

This protocol is the first prospective empirical proposal for `PDMAL_TOPOLOGY_ROBUSTNESS_PROFILE_V1` after the structural-matrix gate closed in PR #409. It fixes the scientific question, design, seed set, endpoint, estimand, analysis policy, QC policy, and blinding/custody sequence before any Track A empirical runner exists or any outcome is collected.

The treatment is the neutral reference algorithm `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`. Track A is not a DGAF semantic-treatment experiment, and the labels `dgaf`, `full_dgaf`, and `canonical_dgaf` are prohibited as Track A treatment identities.

## Exact source boundary

The preregistration is bound to the already-adjudicated Track A sources:

- workload-specific architecture merge: `5e4f00a065c00cefec0b3a79c32b88a5f36a55c2`;
- Track A profile merge: `b1e333ee9f9e0a4da78788e5ff019603296888eb`;
- P-30/P-11 qualification merge: `647f612a2412818dca0d632229f352e857e1187e`;
- structural adjudication merge: `ccabc065d0c1d183e1954ea36a947289fb084831`;
- neutral task-engine blob: `90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05`;
- harness-contract blob: `bb97c54ddf087fef568b1b3c8f8df72c30dad11e`.

Any drift in those bound sources requires a new protocol version and explicit adjudication. It must not be silently inherited by this epoch.

## Research question and directional hypothesis

**Research question:** Under the neutral reference update and the fixed failure matrix, is mean seed-paired FFCR higher for the PDMAL topology than for the random-regular topology?

**Directional hypothesis:** the equal-weight mean of the paired seed effects

`FFCR_pdmal(seed) - FFCR_random_regular(seed)`

is greater than zero.

This is the only confirmatory contrast.

## Fixed design

- Nodes: **20**
- Algorithm: `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`, alpha = `0.5`
- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`
- Primary topology: `pdmal`
- Primary comparator: `random_regular`
- Descriptive/exploratory topologies: `ring`, `small_world`, `complete`
- Fresh paired root seeds: integers `20261301..20261350` inclusive
- Cells per seed: `5 × 9 = 45`
- Planned cells: `50 × 45 = 2,250`
- Primary paired cells per seed: `2 × 9 = 18`

The scientific seed set is fixed before outcomes. It is disjoint from the known prior empirical ranges `20260819..20260868`, `20260901..20260950`, and `20261001..20261050`, and from the later diagnostic-only seeds `20261101`, `20261102`, `20261201`, and `20261202`.

## Primary endpoint

The per-cell primary endpoint is the explicit boolean `ffcr_success`.

For this Track A epoch it is defined by the existing `ConsensusTrialResult.consensus_success` contract: `true` only when `final_std < 0.01` and execution status is `SUCCESS` after the fixed 100-iteration `ConsensusTask` execution. There is no convergence-based early stopping.

Missing or non-boolean endpoint values are fail-closed. The runner or analysis must not reconstruct, impute, or repair `ffcr_success` from another field.

## Estimand and locked analysis

For each complete root seed and topology:

`FFCR_topology(seed) = mean(ffcr_success over the nine fixed failure-count cells)`.

The paired seed effect is:

`Delta_seed = FFCR_pdmal(seed) - FFCR_random_regular(seed)`.

The primary estimand is the equal-weight mean of the 50 preregistered paired seed effects.

The confirmatory interval is a two-sided 95% percentile bootstrap over complete paired seed effects:

- resamples: `10,000`;
- analysis-only RNG seed: `20261399`;
- alpha: `0.05`;
- directional support requires both a positive point estimate and a two-sided 95% CI lower bound greater than zero;
- no primary p-value is required.

There is one confirmatory contrast, so no multiplicity adjustment is applied to that contrast. Every other topology contrast is exploratory/nonconfirmatory and cannot independently satisfy the preregistered directional hypothesis.

The analysis implementation does not yet exist for this Track A epoch and must be separately reviewed and exact-bound before freeze.

## Sample-size rationale

The planned sample is fixed at **50 paired root seeds** before outcome collection. This matches the prior bounded Solo epoch seed count and provides a controlled pilot-scale paired design while keeping the experimental matrix finite and auditable.

This is **not** presented as a formal power guarantee or minimum-detectable-effect claim. There is no outcome-dependent resizing, no outcome-dependent stopping, and no post-hoc replacement-seed rule.

## Prospective QC

The future runner and pre-analysis QC must fail closed unless all of the following hold:

1. the exact 50 preregistered root seeds are present once each;
2. every seed contains exactly 45 unique `seed × topology × failure_count` cells;
3. the complete dataset contains exactly 2,250 unique cells;
4. topology and failure-count values are exactly the preregistered sets;
5. every cell contains an explicit boolean `ffcr_success`;
6. no missing cell is repaired, imputed, silently dropped, or replaced;
7. no seed is silently excluded or replaced;
8. no QC rule is changed after outcome inspection;
9. bound source or preregistration drift stops the gate and requires a new version/adjudication.

A dataset that fails completeness or integrity QC is not eligible for primary analysis under this preregistration.

## Blinding, custody, and unblinding

A fresh protected blinding key is required at the future frozen-candidate stage.

Before authorized unblinding:

- retained scientific records expose opaque topology identifiers, not plaintext topology names;
- the protected topology mapping is held separately;
- topology fingerprints are not emitted into the public pre-unblinding scientific dataset;
- execution order is derived from an HMAC-SHA-256 token over epoch, seed, topology, and failure count using the fresh protected key;
- outcome inspection during collection is prohibited.

The completed dataset and sidecar digest must be locked before any topology mapping is released. Unblinding requires a separate authorization artifact. Same-operator key custody is explicitly non-independent unless a later record establishes otherwise.

This is procedural identity blinding. It does not claim that outcome patterns can never support subjective guesses about topology identity.

## Successor gates

Merging this preregistration may advance only to a separately reviewed Track A empirical runner and analysis implementation. That successor gate must add:

- negative authorization tests;
- exact preregistration/source binding;
- reproducibility and environment evidence;
- fail-closed QC implementation;
- no empirical collection.

Only after runner/analysis stabilization may a later gate establish an immutable exact-commit freeze manifest, final closure packet, verification classification, and a separate one-file collection authorization.

`SCIENTIFIC_N_INCREMENT = 0`

`TRACK_A_PROTOCOL = PROPOSAL_ONLY`

`TRACK_A_FREEZE = NOT_ESTABLISHED`

`TRACK_A_EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

`CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`

`HIGH_ASSURANCE = NOT_AUTHORIZED / N=0`
