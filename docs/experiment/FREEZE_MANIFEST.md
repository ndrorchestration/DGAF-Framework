---
status: PRE-FREEZE
state: PENDING FINAL CONTROLS
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-19
freeze_target_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
freeze_commit_sha: TBD
---

# PDMAL Experiment — Freeze Manifest

This is the pre-freeze manifest for the merged DGAF/PDMAL control plane. It is not evidence of protocol freeze and does not authorize pilot execution. Every value marked `TBD` or `PENDING` must be resolved with direct evidence before the dedicated freeze commit.

The **freeze state is independent of pilot authorization**. Pilot authorization is a separate governance decision that may occur only after the protocol and associated freeze controls are actually frozen. Pilot authorization is therefore **not a freeze precondition** and remains `NOT GRANTED` unless explicitly recorded after freeze.

## 1. Protocol / Design

| Item | Value |
|---|---|
| PR #65 merge baseline | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Protocol | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` — PRE-FREEZE |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` — APPROVED |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — ACCEPTED / INCORPORATED into `915e454e...` |
| Matrix acceptance evidence | Notion governance record — DGAF-Framework Operational Control Center / post-merge freeze reconciliation |
| Primary endpoint | FFCR |
| Secondary endpoint family | `final_std`; recovery success; recovery latency; unrecovered failure count; runtime; primary-outcome variance; connectivity/surviving component size; protocol-compliance rate; missing/invalid rate; gate-block frequency |
| Consensus-quality diagnostic | `final_std < 0.01`; secondary only, not the overall success definition |
| Exploratory diagnostics | `D_a`; phi/convergence traces; topology-specific graph diagnostics; other internal instrumentation values |
| Primary contrast hierarchy | PENDING EXPLICIT PRE-FREEZE ADJUDICATION; current protocol does not independently establish `dgaf` vs `null` as the sole primary contrast |
| Iterations | 100 |

## 2. Pilot Matrix

| Field | Pre-freeze value |
|---|---|
| Conditions | `null`, `simple`, `static`, `dgaf` |
| Topologies | `ring`, `pdmal`, `random_regular`, `small_world`, `complete` |
| Failure counts | `0,1,2,3,4,5,6,8,10` |
| Observations per seed | `180` |
| Planned pilot seeds | `50` |
| Planned raw observations | `9000` |
| `dgaf_pdmal` | OUT OF SCOPE for this pilot |

### Seed-level FFCR aggregation

Each condition produces one seed-level FFCR from the 45 component workload cells spanning the five topologies and nine failure-count levels:

```text
FFCR_condition,seed =
    successful eligible component trials
    /
    eligible component trials
```

Each component trial has equal weight. There is no topology-first or failure-level-first averaging before the seed-level FFCR is calculated.

A trial is **eligible** when it is attempted, including execution-level retries, and is not excluded under the frozen objective exclusion rules. An excluded trial remains retained with an explicit reason and is removed from the denominator only when a pre-registered exclusion rule applies. A valid unfavorable outcome is never excluded because of its result.

Failure count `0` is included in the primary workload and contributes equally to the denominator as a no-failure baseline condition.

## 3. Implementation Provenance

| Item | Value |
|---|---|
| PR #65 merge commit | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Verified ConsensusTask implementation commit | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Verified implementation CI | Run #74 — `32111556449` |
| DGAF adapter | Verified; do not modify without new adjudication |
| Protocol final blob SHA | `TBD at freeze` |
| v0.7.4 task-spec blob SHA | `TBD at freeze` |
| Runner/component tree and critical-file blob SHAs | `TBD at freeze` |
| Topology generator/provenance SHAs | `TBD at freeze` |
| Generated topology fingerprints | `TBD at freeze` |
| Freeze commit SHA | `TBD` |

## 4. Environment

| Item | Value |
|---|---|
| Python | `3.12.0` in verified characterization workflow |
| NumPy | Exact pinned version from lockfile — `TBD verify at freeze` |
| NetworkX | Exact pinned version from lockfile — `TBD verify at freeze` |
| Full lockfile | `experiments/pdmal_pilot/requirements-full-lock.txt` |
| Lockfile blob SHA | `TBD at freeze` |
| Runtime characterization source SHA | `a0ff248eadb736f9b5835f2436791dc6ab5f66cc` |

## 5. Characterization Evidence

| Item | Value |
|---|---|
| Runtime characterization run | #14 — `32112658368` |
| Runtime artifact | `9315467977` |
| Runtime artifact ZIP digest | `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Inner `runtime_characterization.json` SHA-256 | `f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea` |
| 300-second ceiling | VERIFIED for characterization matrix |
| Blinding workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding run | `32113226935` |
| Blinding artifact | `9328114023` |
| Blinding interpretation | CLOSED / PASS; synthetic custody verification only; no empirical data |

## 6. Durable Retention

| Item | Value |
|---|---|
| CI artifact retention | 30 days |
| Durable archive provider | `TBD` |
| Durable archive record / DOI | `TBD` |
| Archived artifact digest(s) | `TBD` |
| Archive retention period | `TBD` |
| Access-control owner | `TBD` |
| Retrieval verification | `TBD` |

## 7. Governance

| Item | Value |
|---|---|
| Expert-panel approval of v0.7.4 | Recorded in governance record |
| Matrix amendment acceptance | ACCEPTED / INCORPORATED; evidence recorded in governance record |
| Freeze timestamp | `TBD` |
| Freeze author | `Ndr Orchestration` |
| Pilot authorization record | `NOT GRANTED — separate post-freeze decision` |

## 8. Architectural Boundary

The `dgaf` condition tests the verified `DGAF_TGLAdapter` behavior under this workload. It does **not** establish that the broader DGAF/PDMAL architecture is generally effective, validated, or empirically supported.

## 9. NotebookLM Boundary

NotebookLM is a research-synthesis and source-interrogation environment. Material originating there has no evidentiary authority unless independently incorporated into an authoritative protocol, implementation, or evidence record.

## 10. Freeze Preconditions

The freeze manifest may only be promoted to `FROZEN` after:

1. the matrix amendment acceptance is represented consistently in the final protocol and governance records;
2. the exact implementation/topology/environment identifiers are recorded;
3. the seed-level FFCR aggregation rule is incorporated into the final protocol;
4. the primary contrast hierarchy is explicitly adjudicated before freeze;
5. the blinding operational workflow passes and its artifact is retained;
6. durable retention is implemented and directly verified;
7. all protocol/document lifecycle metadata is updated to `FROZEN`;
8. a final freeze commit is created and its SHA is recorded;
9. the resulting freeze commit is independently checked for exact-state consistency.

**Pilot authorization is deliberately excluded from the freeze preconditions.** It is a separate governance gate evaluated only after the freeze state is established.

**Current status: PRE-FREEZE. Empirical execution remains prohibited.**
