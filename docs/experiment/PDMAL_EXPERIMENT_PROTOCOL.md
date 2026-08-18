---
status: ACTIVE
state: PRE-FREEZE
authority: Both
owner: DGAF/PDMAL experimental-design control
last_verified: 2026-08-18
applies_to_sha: 08500a7a129a39c21dc890a71a85e5d996e4c4b3
protocol_blob_sha: f367328fdf0854a12b22bd94a25a58973923c5c7
supersedes: prior protocol revisions; see repository history
---

# PDMAL Experiment Protocol

## Status

**PRE-FREEZE / PANEL-ADJUDICATED / NO DATA COLLECTION AUTHORIZED**

This document is the consolidated control document for the planned PDMAL empirical evaluation. The scientific and methodological decisions have been adjudicated. The protocol remains `PRE-FREEZE` until the implementation provenance and execution-control fields identified below are concretely verified and the final contract is committed with a freeze SHA and timestamp.

**No pilot or final experimental seed may be generated while this document remains in `PRE-FREEZE` status.**

## Evidence boundary

Passing software verification, instrumentation verification, deployment verification, and P6a CORS verification establish that the relevant software/evidence machinery operates under the tested conditions. They do **not** establish PDMAL efficacy, superiority, convergence, robustness, or real-world benefit.

The empirical experiment is a separate evidence track.

## Transition rule

The experimental phase may begin only after all of the following are true:

1. PR #65 is merged or an equivalent approved experimental commit is established.
2. This protocol is explicitly frozen with a commit SHA and freeze timestamp.
3. The topology set and baseline matrix are frozen with exact implementation identifiers, parameters, graph-validation results, and source SHAs.
4. The primary endpoint and secondary endpoints are frozen.
5. Failure, recovery, rerouting, retry, and timeout semantics are frozen.
6. RNG/seed generation and stream-separation rules are frozen.
7. Trial ordering is frozen.
8. Exclusion and stopping rules are frozen.
9. The statistical unit and primary analysis model are frozen.
10. The pilot-to-final sample-size rule is frozen and mathematically consistent with the primary analysis.
11. The blinding mechanism and separation-of-duties custody model are confirmed operational without exposing the secret.
12. The unblinding procedure is frozen.
13. Pilot acceptance criteria, including the numeric seed-runtime ceiling, are frozen.
14. The canonical artifact schema, retention location, integrity manifest, and provenance fields are implemented and verified.
15. The exact execution environment is pinned and recorded.
16. Pilot execution authorization is recorded in the evidence log.

## Panel-adjudicated protocol fields

| # | Field | Panel resolution | Status |
|---|---|---|---|
| 1 | Topology + baselines | Candidate matrix accepted: Null, Simple, Static, DGAF, DGAF+PDMAL; topology-study candidates Ring, PDMAL dodecahedral, random-regular degree 3, Small-world, Complete K20. Exact implementation SHAs, parameters, and graph-validation results required before freeze. | **PANEL-ADJUDICATED / PROVENANCE REQUIRED** |
| 2 | Primary endpoint | Failure-Free Completion Rate (FFCR) = completed trials without unrecovered failure / eligible trials; higher is better; report condition-wise estimate and prespecified risk-difference contrasts with 95% CIs. | **RESOLVED** |
| 3 | Secondary endpoints | Recovery success rate, recovery latency, unrecovered failure count, runtime, primary-outcome variance, connectivity/surviving component size, protocol-compliance rate, missing/invalid rate, gate-block frequency; `D_a`, phi/convergence traces, and topology diagnostics are exploratory only. Prespecified multiplicity treatment applies. | **RESOLVED** |
| 4 | RNG streams | NumPy `Generator(PCG64)` with a root `SeedSequence` and domain-separated child streams via `SeedSequence.spawn()`. Streams: trial-order, failure/perturbation, topology-construction (when applicable), analysis-resampling. Exact NumPy/Python versions and stream manifest recorded at freeze. | **RESOLVED / ENVIRONMENT RECORD REQUIRED** |
| 5 | Trial ordering | Block-randomized within each seed; one randomized condition permutation per seed using the dedicated ordering stream; exact permutation retained in provenance without exposing blinded labels to the analyst. | **RESOLVED** |
| 6 | Failure semantics | A trial attempt fails when it exceeds the frozen per-attempt timeout or enters an explicitly unrecoverable state. A trial is unrecovered only after exhausting the frozen retry budget without successful completion. Recovery-window and rerouting rules are distinct from the per-attempt timeout. | **RESOLVED / VALUES PENDING IMPLEMENTATION PIN** |
| 7 | Exclusion rules | Objective protocol violations only; excluded records remain retained with explicit reason. Valid unfavorable outcomes are never excluded. | **RESOLVED** |
| 8 | Stopping rules | No efficacy-based early stopping. Halts are limited to predefined safety, blinding, provenance, protocol-integrity, secret-exposure, catastrophic execution, or loss-of-comparability conditions. | **RESOLVED** |
| 9 | Statistical unit + analysis | One seed = one paired experimental block. Each seed produces one FFCR value per condition. Primary analysis uses paired raw FFCR differences on the original 0–1 proportion scale; effect size is the mean paired difference (risk difference). 95% CI is obtained by a prespecified paired bootstrap procedure. Secondary contrasts are exploratory unless included in the frozen multiplicity procedure. | **RESOLVED** |
| 10 | Sample-size rule | Pilot estimates the within-seed standard deviation of the paired FFCR difference. Target power 0.80, alpha 0.05, minimum detectable absolute FFCR difference 0.15. Final N is determined by the frozen paired-difference power equation using the pilot SD and rounded upward with `math.ceil`. The exact analysis/power implementation must be verified before freeze. | **RESOLVED / IMPLEMENTATION VERIFICATION REQUIRED** |
| 11 | Artifact schema | One JSON artifact per seed containing all trial records and provenance; required fields include experiment/protocol identifiers, seed, blinded condition ID, outcome data, failure/recovery state, runtime, status, exclusion information, environment fingerprint, and hashes. Raw artifacts are retained in GitHub Actions artifacts/durable artifact storage; repository stores protocol/manifests rather than the canonical raw dataset. | **RESOLVED / SCHEMA+RETENTION VERIFICATION REQUIRED** |
| 12 | Blinding/unblinding | `PDMAL_BLINDING_KEY` controls blinded mapping. Repository owner holds the operational secret and does not participate in analysis. Executor and analyst see blinded IDs only. Panel chair is unblinder after raw-data freeze, preprocessing freeze, exclusion freeze, integrity verification, and explicit authorization. Mapping is held separately as a protected object. | **RESOLVED / CUSTODY VERIFICATION REQUIRED** |
| 13 | Pilot pass/fail | PASS requires 100% expected trials attempted, zero blinding breaches, missing/invalid <= 5%, all conditions execute, no comparability-affecting protocol deviation, all required provenance/artifact checks pass, and seed runtime is at or below the frozen ceiling. | **RESOLVED / RUNTIME CEILING PENDING** |

## Topology and baseline specification

### Experimental conditions

The initial controlled matrix is:

1. Null / no-op control
2. Simple agent/control topology
3. Static-rule control
4. DGAF
5. DGAF + PDMAL

### Topology-study candidates

The topology-study candidate set is:

1. Ring
2. PDMAL dodecahedral
3. Random-regular degree 3
4. Small-world
5. Complete K20

The PDMAL dodecahedral structure is the documented 20-vertex, 30-edge, 3-regular graph with three colocated agents/services per vertex (60-service interpretation). Mathematical correctness of this structure is distinct from claims of empirical superiority.

The Small-world candidate is provisionally parameterized as `k=4, p=0.3`. This parameterization is not frozen until the implemented graph and validation test are inspected.

### Required topology provenance record

Before freeze, every condition/topology must record:

```text
implementation name
source commit SHA
module/file path
algorithm and generation parameters
node count
edge count
degree distribution
connectivity result
canonical graph fingerprint/hash
validation-test result
```

No topology may enter the pilot merely because it is named in documentation; the exact implementation and generated graph must be inspectable.

## Primary endpoint

```text
FFCR_condition(seed) =
  successful_trials_without_unrecovered_failure /
  eligible_trials
```

Direction: **higher is better**.

The primary estimand is the mean paired difference in FFCR across seeds for each prespecified primary contrast.

The primary result is not a claim about arbitrary real-world performance; it is scoped to the frozen workload, environment, conditions, perturbation model, and execution protocol.

## Secondary endpoints and diagnostics

Secondary outcomes:

- recovery success rate;
- recovery latency;
- unrecovered failure count;
- total and per-trial runtime;
- within-condition FFCR variance;
- connectivity / surviving component size;
- protocol-compliance rate;
- missing/invalid rate;
- gate-block frequency.

Exploratory diagnostics:

- `D_a`;
- phi/convergence traces;
- topology-specific graph diagnostics;
- other internal instrumentation values.

`D_a` is explicitly **not** a universal success/failure threshold. The current mathematical correction requires operating-regime calibration before an operational threshold claim can be made.

## Statistical unit and analysis

**Statistical unit: one seed = one paired experimental block.**

For each seed, all conditions are executed under the frozen block randomization and common experimental control structure. Each condition yields one FFCR proportion for that seed.

Primary analysis:

```text
For each primary contrast:
  d_i = FFCR_treatment(seed_i) - FFCR_baseline(seed_i)

Effect size = mean(d_i)
```

Confidence interval:

- 95% paired bootstrap confidence interval over seed-level paired differences;
- fixed resampling procedure and seed/count must be frozen before analysis.

The paired t-test is used only as an analytical sensitivity/reference calculation if the frozen diagnostics indicate its assumptions are sufficiently reasonable. The primary inference does not require an arcsin transformation; the estimand remains the raw FFCR risk difference on the original 0–1 scale.

Secondary contrasts are exploratory unless the final multiplicity procedure explicitly promotes them to confirmatory status.

### Missing/excluded data

Missingness and exclusions are not silently converted into success or failure. The primary analysis uses only the prespecified eligible-trial denominator. Missingness rates are separately reported and any analysis change arising from exclusion or missingness is documented.

## Pilot-to-final sample-size rule

The 50-seed pilot estimates the within-seed standard deviation of the paired FFCR difference, `sigma_diff`.

Target parameters:

```text
Power = 0.80
Two-sided alpha = 0.05
Minimum detectable absolute FFCR difference = 0.15
```

For the primary paired-difference planning approximation:

```text
N = ceil(
      ((z_(1-alpha/2) + z_(power))^2 * sigma_diff^2)
      / MDD^2
    )
```

where `MDD = 0.15`.

The implementation must use the same estimand and scale as the primary analysis. If the pilot demonstrates that the approximation is materially inappropriate for the bounded/proportional outcome or the planned paired bootstrap inference, the protocol must be amended **before** the final experiment rather than silently changing the analysis.

No favorable post-hoc target selection is permitted.

## RNG and reproducibility controls

### Generator

```text
Python: exact pinned version at freeze
NumPy: exact pinned version at freeze
BitGenerator: PCG64
Root construction: numpy.random.SeedSequence(root_seed)
Child streams: SeedSequence.spawn()
```

Required domain-separated child streams:

```text
trial-order
failure-perturbation
topology-construction (if randomized)
analysis-resampling
```

Record in the environment/seed manifest:

```text
experiment root seed
SeedSequence construction parameters
stream IDs / spawn positions
NumPy version
Python version
BitGenerator type
checkpoint state where required
```

The experiment does not use an ad-hoc hash convention as its primary stream-splitting mechanism. Any SHA-256 hashes used for manifests or provenance are integrity identifiers, not substitutes for the RNG stream mechanism.

## Trial ordering

Within each seed, the five experimental conditions form one randomized block. A dedicated ordering stream generates a permutation in which each condition appears exactly once. The realized order is retained in provenance in a form that preserves auditability while maintaining blinded analytical labels.

## Failure, retry, recovery, and rerouting semantics

### Candidate fixed semantics

```text
Trial timeout per attempt:       60 seconds
Maximum retry attempts:           3
Recovery window between attempts: 30 seconds
Seed runtime ceiling:            300 seconds
```

These values remain **PENDING IMPLEMENTATION VERIFICATION** until the exact runner is pinned and tested.

Definitions:

- **Failed attempt:** an individual attempt exceeds the 60-second timeout or enters the prescribed failed state.
- **Successful trial:** an attempt completes the prescribed task within the timeout before the retry budget is exhausted.
- **Unrecovered trial failure:** all allowed attempts fail without successful completion.
- **Recovery window:** the maximum allowed interval for prescribed reset/recovery between attempts.
- **Reroute:** a topology-controlled execution-path change triggered by the frozen failure semantics.
- **Seed runtime ceiling:** maximum wall-clock time for the entire seed across all conditions and retries.

The 300-second seed runtime ceiling is a **protocol/runtime integrity control**, not an automatic FFCR failure. A ceiling violation is retained as a protocol deviation/runtime outcome and is handled under the frozen deviation rule.

## Exclusion rules

Exclude only objectively invalid protocol executions, such as:

- corrupted inputs;
- missing mandatory provenance;
- invalid seed/protocol records;
- environment-integrity failures;
- execution outside the frozen protocol;
- a verified condition-comparability failure requiring exclusion under the frozen deviation rule.

Excluded records remain in the provenance dataset with an explicit reason. A valid unfavorable outcome is never excluded because of its result.

## Stopping rules

There is no efficacy-based early stopping in the 50-seed pilot.

A halt is authorized only for predefined conditions including:

- blinding breach;
- secret exposure;
- provenance corruption;
- systematic protocol violation;
- catastrophic runner instability;
- loss of condition comparability;
- infrastructure failure preventing valid execution.

Any halt is recorded as a protocol event and does not itself authorize protocol amendment during data collection.

## Artifact and provenance architecture

### Canonical raw-data location

Raw experimental outputs are retained as GitHub Actions artifacts or another explicitly approved durable artifact store. The Git repository stores the protocol, runner code, manifests, schemas, and evidence indexes rather than the canonical raw experimental dataset.

### Required artifact controls

Each artifact set must include:

```text
GitHub Artifact ID
artifact name
artifact SHA-256
protocol commit SHA
runner/experiment commit SHA
workflow/run ID
experiment ID
seed manifest hash
environment fingerprint
creation timestamp
```

Where supported, the artifact should also carry a GitHub artifact attestation linking it to the repository, workflow, commit, and triggering event.

### Per-seed JSON structure

Conceptual schema:

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

The exact machine-readable schema, validation test, artifact naming convention, and retention configuration must be implemented and verified before freeze.

## Blinding, custody, and separation of duties

`PDMAL_BLINDING_KEY` must never be committed, printed, or included in retained experimental artifacts.

Role separation:

| Role | Access / restriction |
|---|---|
| Repository owner | Holds the operational secret; does not participate in primary analysis. |
| Experiment executor | Executes only through blinded condition IDs; has no key access. |
| Analyst | Receives blinded dataset; has no key/mapping access. |
| Unblinder / panel chair | Receives the mapping only after raw-data freeze, preprocessing freeze, exclusion freeze, integrity verification, and recorded authorization. |

The real condition-to-blinded-label mapping is stored as a protected object separate from the analytical dataset.

The unblinding event itself must be logged without revealing the secret.

## Pilot acceptance criteria

The 50-seed pilot passes only if all of the following are true:

- 100% of expected trials are attempted;
- zero blinding breaches;
- missing/invalid trial rate <= 5%;
- every condition executes;
- no protocol deviation affecting comparability;
- all required provenance and artifact-integrity checks pass;
- seed runtime remains at or below the frozen runtime ceiling.

The pilot must not be declared a success because the observed efficacy results are favorable. Pilot acceptance is an operational/feasibility gate.

## Environment reproducibility

Before freeze, the execution environment must record:

```text
Python version
NumPy version
all direct experiment dependencies and versions
OS / runner image
CPU architecture where material
lockfile / environment fingerprint
experiment runner commit SHA
protocol commit SHA
```

The same environment definition must be used for pilot and final experiment unless a documented protocol amendment establishes equivalence.

## Protocol deviations

A protocol deviation must record at minimum:

```text
UTC timestamp
seed/trial identifier if applicable
source commit SHA
workflow/run ID
nature of deviation
whether comparability was affected
disposition under the frozen exclusion rule
review/authorization record
```

Valid unfavorable results are not protocol deviations merely because they are unfavorable.

## Documentation lifecycle

This protocol is `ACTIVE` as the current pre-freeze protocol and is not yet `FROZEN`. Freeze requires a new immutable commit SHA, timestamp, completed manifest, and explicit authorization record. The lifecycle metadata at the top of this file is part of the governance record.
