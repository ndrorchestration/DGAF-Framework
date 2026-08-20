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

This is the PDMAL experiment protocol. It is pre-freeze. No empirical data collection is authorized until the protocol is frozen and pilot authorization is separately recorded.

## 1. Purpose

The PDMAL experiment is designed to characterize the runtime behavior of the DGAF/PDMAL topology stack under controlled conditions. It is an operational characterization, not an efficacy demonstration.

## 2. Scope

The protocol covers the topology generators, the harness, the task engine, the DGAF adapter, and the runtime characterization pipeline. It does not cover production-scale operations, long-term persistence, or any empirical claim about DGAF's effectiveness in any real-world setting.

## 3. Protocol Version

This protocol incorporates the v0.7.5 matrix amendment (`docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`). The matrix amendment is accepted by governance but is not the same as a protocol freeze.

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

### 4.4 Endpoint

- **Primary:** FFCR (Failure-Free Completion Rate) — higher is better; per-condition, per-seed
- **Secondary (structural/execution):** `final_std`, `D_a`-style diagnostics, phi-convergence traces — transparency metrics, not success endpoints

### 4.5 Convergence

Consensus threshold `< 0.01` is the convergence criterion for task execution, not an efficacy threshold. Iterations are fixed at 100; there is no convergence-based early stopping.

## 5. Pre-freeze status

The protocol is pre-freeze. The following remain open:

- Primary contrast adjudication
- Exact protocol blob SHA (pending after commit)
- Freeze commit SHA

## 6. Evidence boundary

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
