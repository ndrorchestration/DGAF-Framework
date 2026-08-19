---
status: ACTIVE
state: PRE-FREEZE
authority: Both
owner: DGAF/PDMAL experimental-design control
last_verified: 2026-08-19
applies_to_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
protocol_blob_sha: PENDING-AFTER-COMMIT
supersedes: prior protocol revisions; v0.7.5 matrix amendment incorporated
---

# PDMAL Experiment Protocol

## Status

PRE-FREEZE / PANEL-ADJUDICATED / NO DATA COLLECTION AUTHORIZED

This document is the consolidated control document for the planned PDMAL empirical evaluation. The scientific and methodological decisions have been adjudicated. The protocol remains `PRE-FREEZE` until the implementation provenance and execution-control fields identified below are concretely verified and the final contract is committed with a freeze SHA and timestamp.

No pilot or final experimental seed may be generated while this document is in `PRE-FREEZE` status.

## Merge baseline record

PR #65 merged at `915e454e27eb2770e7f40a067a881b0783feaae4`. This commit is the current repository merge baseline / freeze-target baseline. It is not the eventual freeze commit, does not make this protocol `FROZEN`, and does not authorize empirical execution. Historical execution evidence remains scoped to its exact executed SHA.

## v0.7.5 Pilot Matrix Amendment — Incorporated

The pre-registered pilot scope is explicitly limited to the following matrix:

### Conditions

1. `null`
2. `simple`
3. `static`
4. `dgaf`

The repository-recognized `dgaf_pdmal` condition is explicitly **out of scope for this pilot** and reserved for later experimentation.

### Topologies

1. `ring`
2. `pdmal`
3. `random_regular`
4. `small_world`
5. `complete`

### Failure counts

```text
0, 1, 2, 3, 4, 5, 6, 8, 10
```

### Observation count

Each seed contains:

```text
4 conditions × 5 topologies × 9 failure-count levels = 180 observations
```

The planned 50-seed pilot therefore contains:

```text
50 × 180 = 9,000 raw observations before exclusions
```

This matrix is incorporated from `PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`. It remains **PRE-FREEZE** until the documented acceptance record, remaining freeze controls, and dedicated freeze commit are complete.

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
| 1 | Pilot matrix | Four conditions (`null`, `simple`, `static`, `dgaf`) across five topologies (`ring`, `pdmal`, `random_regular`, `small_world`, `complete`) and nine failure counts (`0,1,2,3,4,5,6,8,10`); 180 observations per seed; 9,000 for 50 seeds before exclusions. | **ACCEPTED / INCORPORATED / PRE-FREEZE** |
| 2 | Primary endpoint | Failure-Free Completion Rate (FFCR) = completed trials without unrecovered failure / eligible trials; higher is better; report condition-wise estimate and prespecified risk-difference contrasts with 95% CIs. | **RESOLVED** |
| 3 | Secondary endpoints | Recovery success rate, recovery latency, unrecovered failure count, runtime, primary-outcome variance, connectivity/surviving component size, protocol-compliance rate, missing/invalid rate, gate-block frequency; `D_a`, phi/convergence traces, and topology diagnostics are exploratory only. Prespecified multiplicity treatment applies. | **RESOLVED** |
| 4 | RNG streams | NumPy `Generator(PCG64)` with a root `SeedSequence` and domain-separated child streams via `SeedSequence.spawn()`. Streams: trial-order, failure/perturbation, topology-construction, analysis-resampling, and the appended `task_initialization` stream from v0.7.4. Exact NumPy/Python versions and stream manifest recorded at freeze. | **RESOLVED / ENVIRONMENT RECORD REQUIRED** |
| 5 | Trial ordering | Block-randomized within each seed; one randomized condition permutation per seed using the dedicated ordering stream; exact permutation retained in provenance without exposing blinded labels to the analyst. | **RESOLVED** |
| 6 | Failure semantics | A trial attempt fails when it exceeds the frozen per-attempt timeout or enters an explicitly unrecoverable state. A trial is unrecovered only after exhausting the frozen retry budget without successful completion. Recovery-window and rerouting rules are distinct from the per-attempt timeout. | **RESOLVED / VALUES VERIFIED IN RUNNER** |
| 7 | Exclusion rules | Objective protocol violations only; excluded records remain retained with explicit reason. Valid unfavorable outcomes are never excluded. | **RESOLVED** |
| 8 | Stopping rules | No efficacy-based early stopping. Halts are limited to predefined safety, blinding, provenance, protocol-integrity, secret-exposure, catastrophic execution, or loss-of-comparability conditions. | **RESOLVED** |
| 9 | Statistical unit + analysis | One seed = one paired experimental block. Each seed produces one FFCR value per condition. Primary analysis uses paired raw FFCR differences on the original 0–1 proportion scale; effect size is the mean paired difference (risk difference). 95% CI is obtained by a prespecified paired bootstrap procedure. Secondary contrasts are exploratory unless included in the frozen multiplicity procedure. | **RESOLVED** |
| 10 | Sample-size rule | Pilot estimates the within-seed standard deviation of the paired FFCR difference. Target power 0.80, alpha 0.05, minimum detectable absolute FFCR difference 0.15. Final N is determined by the frozen paired-difference power equation using the pilot SD and rounded upward with `math.ceil`. The exact analysis/power implementation must be verified before freeze. | **RESOLVED / IMPLEMENTATION VERIFICATION REQUIRED** |
| 11 | Artifact schema | One JSON artifact per seed containing all trial records and provenance; required fields include experiment/protocol identifiers, seed, blinded condition ID, outcome data, failure/recovery state, runtime, status, exclusion information, environment fingerprint, and hashes. Raw artifacts are retained in GitHub Actions artifacts/durable artifact storage; repository stores protocol/manifests rather than the canonical raw dataset. | **RESOLVED / SCHEMA+RETENTION VERIFICATION REQUIRED** |
| 12 | Blinding/unblinding | `PDMAL_BLINDING_KEY` controls blinded mapping. Repository owner holds the operational secret and does not participate in analysis. Executor and analyst see blinded IDs only. Panel chair is unblinder after raw-data freeze, preprocessing freeze, exclusion freeze, integrity verification, and explicit authorization. Mapping is held separately as a protected object. | **RESOLVED / OPERATIONAL DRY-RUN PASS; CUSTODY RETAINED AS FREEZE CONTROL** |
| 13 | Pilot pass/fail | PASS requires 100% expected trials attempted, zero blinding breaches, missing/invalid <= 5%, all conditions execute, no comparability-affecting protocol deviation, all required provenance/artifact checks pass, and seed runtime is at or below the frozen ceiling. | **RESOLVED / RUNTIME CHARACTERIZATION VERIFIED** |

## Topology and baseline specification

### Pilot experimental conditions

The pilot uses exactly four conditions:

1. `null` — baseline
2. `simple` — slow-mixing control
3. `static` — fixed Metropolis-Hastings weights without failure-time renormalization
4. `dgaf` — governance runtime via the verified DGAF adapter

`dgaf_pdmal` is reserved for later work and is not part of this pilot.

### Pilot topology set

The pilot uses exactly five topologies:

1. `ring`
2. `pdmal`
3. `random_regular`
4. `small_world`
5. `complete`

All five must use the verified topology generators and provenance/fingerprint controls.

### Failure-count set

The pilot uses exactly:

```text
0, 1, 2, 3, 4, 5, 6, 8, 10
```

No other failure-count level enters the pre-registered pilot without a protocol amendment before data collection.

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

## Deterministic workload specification

The authoritative workload is defined by `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md`. A trial is identified by `(seed, topology, condition, failure_count)` and retries reproduce the same trial state.

Consensus dynamics:

- 20 nodes.
- Initial values `Uniform(-1,1)` from the dedicated `task_initialization` RNG stream.
- Exactly 100 iterations; no convergence-based early stopping.
- Failure injection at iteration 33; recovery at iteration 66.
- Failed nodes retain state and are excluded from active-neighbor sets while failed.

## Primary endpoint

```text
FFCR_condition,seed =
  successful eligible component trials /
  eligible component trials
```

Each condition produces one seed-level FFCR from the 45 component workload cells spanning five topologies and nine failure-count levels. Each component trial has equal weight; no topology-first or failure-level-first averaging is performed before the seed-level FFCR is calculated.

A trial is **eligible** when it is attempted, including execution-level retries, and is not excluded under the frozen objective exclusion rules. An excluded trial remains retained with an explicit reason and is removed from the denominator only when a pre-registered exclusion rule applies. A valid unfavorable outcome is never excluded because of its result.

Failure count `0` is included in the primary workload and contributes equally to the denominator as a no-failure baseline condition.

Direction: **higher is better**.

The primary estimand is the mean paired difference in FFCR across seeds for each explicitly adjudicated primary contrast. The primary contrast hierarchy itself remains an open pre-freeze methodological decision recorded in `docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md`.

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
- gate-block frequency;
- `final_std` as a consensus-quality secondary endpoint, with the diagnostic threshold `final_std < 0.01`.

Exploratory diagnostics:

- `D_a`;
- phi/convergence traces;
- topology-specific graph diagnostics;
- other internal instrumentation values.

`final_std < 0.01` is not the definition of overall experimental success. `D_a` is explicitly **not** a universal success/failure threshold. The current mathematical correction requires operating-regime calibration before an operational threshold claim can be made.

## Statistical unit and analysis

Statistical unit: one seed = one paired experimental block.

For each seed, all four pilot conditions are executed under the frozen block randomization and common experimental control structure. Each condition yields one FFCR proportion for that seed.

Primary analysis:

```text
For each explicitly adjudicated primary contrast:
  d_i = FFCR_treatment(seed_i) - FFCR_baseline(seed_i)

Effect size = mean(d_i)
```

Confidence interval:

- 95% paired bootstrap confidence interval over seed-level paired differences;
- fixed resampling procedure and seed/count must be frozen before analysis.

The paired t-test is used only as an analytical sensitivity/reference calculation if the frozen diagnostics indicate its assumptions are sufficiently reasonable. The primary inference does not require an arcsin transformation; the estimand remains the raw FFCR risk difference on the original 0–1 scale.

Secondary contrasts are exploratory unless the final multiplicity procedure explicitly promotes them to confirmatory status.

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
trial_order
failure_injection
topology_construction
analysis_resampling
task_initialization
```

`task_initialization` is appended after the existing streams so prior stream identities remain stable.

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

## Trial ordering

Within each seed, the four pilot conditions form one randomized block. A dedicated ordering stream generates a permutation in which each condition appears exactly once. The realized order is retained in provenance in a form that preserves auditability while maintaining blinded analytical labels.

## Failure, retry, recovery, and rerouting semantics

```text
Trial timeout per attempt:       60 seconds
Maximum retry attempts:           3
Recovery window between attempts: 30 seconds
Seed runtime ceiling:            300 seconds
```

These values are implemented in the verified runner and runtime characterization has confirmed the 300-second ceiling for the characterization matrix. The values remain part of the frozen protocol control set.

Definitions:

- **Failed attempt:** an individual attempt exceeds the 60-second timeout or enters the prescribed failed state.
- **Successful trial:** an attempt completes the prescribed task within the timeout before the retry budget is exhausted.
- **Unrecovered trial failure:** all allowed attempts fail without successful completion.
- **Recovery window:** the maximum allowed interval for prescribed reset/recovery between attempts.
- **Seed runtime ceiling:** maximum wall-clock time for the entire characterized seed execution.

The 300-second seed runtime ceiling is a **protocol/runtime integrity control**, not an automatic FFCR failure.

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

- 100% of the planned 9,000 raw observations are attempted;
- zero blinding breaches;
- missing/invalid trial rate <= 5%;
- all four conditions execute;
- all five topologies execute;
- all nine failure-count levels execute;
- no protocol deviation affecting comparability;
- all required provenance and artifact-integrity checks pass;
- seed runtime remains at or below the frozen runtime ceiling.

## NotebookLM boundary

NotebookLM is a research-synthesis and source-interrogation environment. Material originating there has no evidentiary authority unless independently incorporated into an authoritative protocol, implementation, or evidence record.

## Current pre-freeze controls

The protocol cannot transition to `FROZEN` until the following are independently verified:

- expert-panel acceptance of the incorporated v0.7.5 matrix;
- explicit adjudication of the primary contrast hierarchy;
- blinding operational dry-run;
- durable retention archive and integrity record;
- final freeze manifest with exact file blob SHAs and tested-run references;
- authorization guard review demonstrating that pilot execution is fail-closed and bound to the recorded frozen state rather than environment variables alone.

Status remains PRE-FREEZE. No empirical execution is authorized.
