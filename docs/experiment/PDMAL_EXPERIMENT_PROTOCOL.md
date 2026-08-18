# PDMAL Experiment Protocol

## Status

**PRE-FREEZE / PANEL-ADJUDICATED / NO DATA COLLECTION AUTHORIZED**

This document is the consolidated control document for the planned PDMAL empirical evaluation. The expert-panel decisions below are recorded, but the protocol is not yet frozen because three implementation-dependent values remain to be resolved and the repository transition rule requires the approved experimental commit to be established before pilot authorization.

No pilot or final experimental seed may be generated while this document remains in `PRE-FREEZE` status.

## Evidence boundary

Passing software verification, instrumentation verification, deployment verification, and P6a CORS verification establish that the relevant software/evidence machinery operates under the tested conditions. They do **not** establish PDMAL efficacy or real-world benefit.

The empirical experiment is a separate evidence track.

## Transition rule

The experimental phase may begin only after all of the following are true:

1. PR #65 is merged or an equivalent approved experimental commit is established.
2. This protocol is explicitly frozen with a commit SHA and freeze timestamp.
3. The topology set and baseline matrix are frozen with exact implementation identifiers, parameters, and source SHAs.
4. The primary endpoint and secondary endpoints are frozen.
5. Failure, recovery, rerouting, and timeout semantics are frozen.
6. RNG/seed generation and stream separation rules are frozen.
7. Trial ordering is frozen.
8. Exclusion and stopping rules are frozen.
9. The blinding mechanism is confirmed operational without exposing the secret.
10. The unblinding procedure is frozen.
11. The statistical analysis plan is frozen.
12. Pilot acceptance criteria, including the numeric runtime ceiling, are frozen.
13. The pilot-to-final sample-size rule is frozen.
14. Pilot execution authorization is recorded in the evidence log.

## Panel-adjudicated protocol fields

| # | Field | Panel resolution | Status |
|---|---|---|---|
| 1 | Topology + baselines | Candidate matrix accepted: Null, Simple, Static, DGAF, DGAF+PDMAL; topology study candidates Ring, PDMAL dodecahedral, random-regular degree 3, Small-world, Complete K20. Exact implementation SHAs and generation parameters must be recorded before freeze. | **PANEL-ADJUDICATED / PENDING PROVENANCE** |
| 2 | Primary endpoint | Failure-Free Completion Rate (FFCR) = completed trials without unrecovered failure / eligible trials; higher is better; report point estimate and 95% CI; prespecified baseline contrast. | **RESOLVED** |
| 3 | Secondary endpoints | Recovery success rate, recovery latency, unrecovered failure count, runtime, primary-outcome variance, connectivity/surviving component size, protocol-compliance rate, missing/invalid rate, gate-block frequency; `D_a`/phi/topology diagnostics exploratory only. Secondary multiplicity handled by prespecified correction. | **RESOLVED** |
| 4 | RNG streams | NumPy `Generator(PCG64)`; domain-separated streams; seed derivation uses SHA-256 over concatenated `seed + stream_id`; exact implementation/version recorded at freeze. | **RESOLVED / VERSION RECORD REQUIRED** |
| 5 | Trial ordering | Block-randomized within each seed; condition order randomized per block using the dedicated ordering stream; reproducible ordering retained in provenance. | **RESOLVED** |
| 6 | Failure semantics | Failure = prescribed trial does not complete within the frozen timeout or is classified unrecoverable; recovery/rerouting follow the frozen candidate semantics; exact timeout and recovery window remain implementation-dependent and must be recorded before freeze. | **RESOLVED / TIMEOUT VALUE PENDING** |
| 7 | Exclusion rules | Objective protocol violations only; exclusions retained with explicit reason; unfavorable valid outcomes are never excluded. | **RESOLVED** |
| 8 | Stopping rules | No early efficacy stopping. Only predefined safety, blinding, provenance, protocol-integrity, or catastrophic execution halts. | **RESOLVED** |
| 9 | Statistical analysis | Paired condition-wise comparison of FFCR; effect size = risk difference; 95% CI; secondary outcomes exploratory with prespecified multiplicity correction; missingness handled by frozen rule. | **RESOLVED** |
| 10 | Sample-size rule | Pilot-derived variance/proportion estimate; target power 0.80, alpha 0.05, minimum detectable risk difference 0.15; final N computed by the frozen formula and fixed rounding rule. | **RESOLVED / FORMULA IMPLEMENTATION REQUIRED** |
| 11 | Artifact schema | One JSON artifact per seed containing all trial records and provenance; required fields include experiment/protocol identifiers, seed, blinded condition ID, outcomes, failure/recovery, runtime, status, exclusion information, environment fingerprint, and hashes. | **RESOLVED / IMPLEMENTATION SCHEMA REQUIRED** |
| 12 | Blinding/unblinding | `PDMAL_BLINDING_KEY` controls blinded mapping; mapping stored outside analytical dataset; no secret in artifacts; unblinding only after raw data, preprocessing, and exclusions are frozen and authorization recorded. | **RESOLVED / CUSTODY PROCEDURE REQUIRED** |
| 13 | Pilot pass/fail | PASS requires 100% expected trials attempted, 0 blinding breaches, missing/invalid <= 5%, all conditions execute, no comparability-affecting protocol deviation, and runtime at or below the frozen ceiling. | **RESOLVED / NUMERIC RUNTIME CEILING PENDING** |

## Topology specification candidate

The topology-study candidate matrix is:

1. Ring
2. PDMAL dodecahedral
3. Random-regular degree 3
4. Small-world
5. Complete K20

The PDMAL dodecahedral structure is documented as a 20-vertex, 30-edge, 3-regular graph with three colocated agents/services per vertex (60-service interpretation). The current mathematical correction explicitly separates this topology definition from claims of empirical superiority. Exact topology implementation provenance is mandatory before freeze.

The Small-world parameters are provisionally proposed as `k=4, p=0.3`, but these values are **not frozen** until the implementation and generated graph are verified against the specification.

## Primary endpoint

```text
FFCR = completed_trials_without_unrecovered_failure / eligible_trials
```

Direction: higher is better.

The primary analysis will report the condition-wise estimate, risk-difference effect size for prespecified contrasts, and 95% confidence intervals.

## Secondary diagnostics

`D_a` is explicitly a secondary diagnostic and **not** a universal success/failure threshold. The current mathematical correction requires calibration for a defined operating regime before `D_a` can support an operational threshold claim.

Phi/convergence traces, topology metrics, and other internal diagnostics are similarly subordinate to the primary endpoint.

## RNG specification

Candidate implementation:

```text
Library:       NumPy
Generator:     numpy.random.Generator
Bit generator: PCG64
Derivation:    SHA-256(seed + stream_id)
Streams:       seed-generation, trial-order, failure/perturbation,
               topology-construction (when applicable), analysis-resampling
```

Exact NumPy version and the precise byte/string serialization used before SHA-256 must be recorded in the freeze manifest.

## Trial ordering

For each seed, all conditions form one randomized block. The dedicated ordering stream generates a permutation of condition IDs. Every condition occurs exactly once in the block.

## Failure / recovery / rerouting

A failure is an incomplete trial after the frozen timeout or an explicitly classified unrecoverable state. A recovery succeeds only if the prescribed task state is restored within the frozen recovery window and the trial completes. A reroute is a topology-controlled path change triggered by the prescribed failure semantics.

The exact timeout, retry count, and recovery window are implementation-dependent and remain pending until the runner is pinned.

## Exclusions

Exclude only objectively invalid protocol executions, including corrupted inputs, missing mandatory provenance, invalid seed/protocol records, environment-integrity failures, or executions outside the frozen protocol. Exclusions remain in the provenance dataset with reasons.

## Stopping

No efficacy-based early stopping. A halt may occur for blinding breach, provenance corruption, systematic protocol violation, catastrophic runner instability, secret exposure, or loss of condition comparability.

## Statistical plan

Primary:

- paired comparison of FFCR across prespecified conditions;
- effect size: risk difference;
- uncertainty: 95% CI;
- one prespecified primary contrast, with secondary contrasts treated as exploratory unless the frozen multiplicity procedure states otherwise.

Final sample size:

- target power: 0.80;
- alpha: 0.05;
- minimum detectable risk difference: 0.15;
- pilot-derived event proportion/variance estimate;
- fixed mathematical formula and rounding rule;
- no favorable post-hoc target selection.

## Blinding

`PDMAL_BLINDING_KEY` must never be committed, printed, or included in retained artifacts. The blinded condition mapping is held outside the analytical dataset. The mapping is revealed only after dataset freeze, preprocessing freeze, exclusion freeze, integrity verification, and recorded unblinding authorization.

The exact custody mechanism and unblinding authority are pending final operationalization.

## Canonical artifact

One JSON artifact per seed should contain:

```json
{
  "experiment_id": "...",
  "protocol_version": "...",
  "experiment_commit_sha": "...",
  "seed_id": "...",
  "blinded_condition_id": "...",
  "trial_id": "...",
  "primary_outcome": "...",
  "secondary_outcomes": {},
  "failure": {},
  "recovery": {},
  "runtime_ms": 0,
  "status": "...",
  "excluded": false,
  "exclusion_reason": null,
  "environment_fingerprint": "...",
  "artifact_sha256": "..."
}
```

The final schema, artifact naming convention, and retention location must be implemented and verified before freeze.

## Pilot acceptance criteria

The 50-seed pilot passes only if:

- 100% expected trials are attempted;
- zero blinding breaches occur;
- missing/invalid trial rate is <= 5%;
- every condition executes;
- no protocol deviation affects comparability;
- runtime remains at or below the frozen ceiling;
- required provenance and artifact integrity checks pass.

The numeric runtime ceiling is pending characterization of the pinned runner/environment and must be frozen before data collection.

## H4 historical boundary

The earlier H4 Task-Stratified Topology × Orchestration experiment is methodological precedent only. Its simulated scores, verdicts, and historical outcomes are excluded from the present PDMAL evidence base and are not priors for the present analysis.

## Freeze record

```text
Protocol status:       PRE-FREEZE / PANEL-ADJUDICATED
Panel decision record: CURRENT SESSION ADJUDICATION
Freeze commit SHA:     NOT YET ASSIGNED
Freeze timestamp:      NOT YET ASSIGNED
Pilot authorization:   NOT YET GRANTED
```

## Change control

Any change after freeze requires:

1. a new protocol version;
2. explicit description of the change;
3. reason for the change;
4. determination of whether previously collected data remain valid;
5. a new commit SHA;
6. updated evidence/provenance documentation.
