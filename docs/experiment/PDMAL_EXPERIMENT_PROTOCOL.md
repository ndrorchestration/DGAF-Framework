---
status: ACTIVE
state: PRE-FREEZE
authority: Both
owner: DGAF/PDMAL experimental-design control
last_verified: 2026-08-26
applies_to_sha: e6beeb66335e1b50a239697badab22dab50eb5ba
protocol_blob_sha: BOUND_EXTERNALLY_BY_P8_LOCK
supersedes: prior protocol revisions; v0.7.5 matrix amendment incorporated
---

# PDMAL Experiment Protocol

This is the PDMAL experiment protocol. It is pre-freeze. No empirical data collection is authorized until the protocol is frozen and pilot authorization is separately recorded.

## 1. Purpose

The PDMAL experiment is designed to characterize the runtime behavior of the DGAF/PDMAL topology stack under controlled conditions, including a pre-specified comparative analysis of the full DGAF condition against the null condition. The comparative analysis is a controlled experimental hypothesis test within the characterization protocol; it is not a claim of production-scale efficacy, real-world effectiveness, or deployment readiness.

## 2. Scope

The protocol covers the topology generators, the harness, the task engine, the DGAF adapter, and the runtime characterization and analysis pipeline. It does not cover production-scale operations, long-term persistence, or any empirical claim about DGAF's effectiveness in any real-world setting.

## 3. Protocol Version

This protocol incorporates the v0.7.5 matrix amendment (`docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`) and the P7 primary-analysis adjudication. These governance decisions are not themselves a protocol freeze.

## 4. Methodology

### 4.1 Task

The experiment executes the ConsensusTask across the registered topology and condition matrix. Each trial is deterministic given its seed.

### 4.2 Topology matrix

| Topology | Description |
|---|---|
| ring | Ring lattice |
| pdmal | PDMAL topology |
| random_regular | Random regular graph |
| small_world | Small-world graph |
| complete | Complete graph |

### 4.3 Condition matrix

| Condition | Description |
|---|---|
| null | Baseline, no DGAF |
| simple | Simple DGAF configuration |
| static | Static DGAF configuration |
| dgaf | Full DGAF configuration |

### 4.4 Endpoint and primary contrast

- **Primary endpoint:** FFCR (Failure-Free Completion Rate), higher is better, recorded per condition per seed.
- **Primary contrast:** full `dgaf` condition versus `null` condition.
- The primary contrast is a pre-specified comparative analysis within this operational-characterization experiment. It does not convert historical characterization results into efficacy evidence.
- For each trial artifact, `ffcr_success` is the explicit boolean execution outcome used to construct FFCR. It is true only when the ConsensusTask's convergence criterion is satisfied and the execution status is successful. The analysis does not reconstruct this outcome from `final_std` or repair missing outcome fields.
- **Secondary/exploratory measures:** `final_std`, `D_a`-style diagnostics, phi-convergence traces, and non-primary condition/topology contrasts. These are not primary success endpoints.

### 4.5 Convergence

Consensus threshold `< 0.01` is the convergence criterion for task execution, not an efficacy threshold. Iterations are fixed at 100; there is no convergence-based early stopping.

## 5. Analysis boundary

The P7 adjudication defines the scientific target and primary analysis contract. P8 binds the executable analysis implementation/configuration to the exact candidate apparatus before any unblinding or empirical interpretation.

The canonical analysis implementation is `experiments/pdmal_pilot/analysis.py`. It consumes validated seed artifacts and an explicit post-unblinding condition mapping; it does not execute trials, regenerate observations, repair incomplete records, or infer missing outcomes.

The primary analysis is seed-paired. For each analyzable seed, condition-level FFCR is the proportion of the complete topology × failure-count matrix cells with `ffcr_success=true`. The primary paired effect is `FFCR_dgaf(seed) - FFCR_null(seed)`. The primary point estimate is the equal-weight mean of these paired seed effects.

The current pre-freeze analysis configuration uses a two-sided 95% percentile paired-bootstrap interval over complete seed effects, with 10,000 resamples, bootstrap RNG seed `20260823`, and alpha `0.05`. The primary directional support criterion is a positive point estimate with the confidence interval wholly above zero. These implementation bindings remain subject to candidate-scoped verification and final P8 lock.

Historical characterization artifacts remain evidence only for the exact SHA and execution conditions under which they were produced.

## 6. Pre-freeze status

The protocol remains pre-freeze. The following remain open:

- Formal adoption/closure of the P7 decision record
- Candidate-scoped P8 implementation/configuration verification and hash binding
- Exact protocol blob SHA is bound externally by the P8 analysis lock after this commit
- Freeze commit SHA
- Independent verification
- Separate pilot authorization

## 7. Evidence boundary

This protocol is a specification artifact.

### Release asset verification

The v0.7.5 runtime characterization release asset was downloaded and verified on 2026-08-20:

- Release asset: `pdmal-runtime-characterization-4a7d00b84693807306f639e9c818f4604517e840.zip`
- ZIP SHA-256: `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20`
- Inner artifact: `runtime_characterization.json`
- Inner artifact SHA-256: `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`
- ZIP-shipped sidecar confirms inner SHA: YES

The v0.7.5 release is a 3-seed, 2-topology operational characterization (72/72 trials completed). It is NOT the 50-seed blinded pilot. Protocol status remains PRE-FREEZE.

This protocol is a specification artifact. It does not authorize empirical execution. N = 0 throughout. Pilot authorization is NOT GRANTED.
