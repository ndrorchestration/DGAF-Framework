---
status: PRE-FREEZE
state: PENDING FINAL CONTROLS
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-18
freeze_commit_sha: TBD
---

# PDMAL Experiment — Freeze Manifest

This is the pre-freeze manifest. It is not evidence of protocol freeze and does not authorize pilot execution. Every value marked `TBD` or `PENDING` must be resolved with direct evidence before the freeze commit.

## 1. Protocol / Design

| Item | Value |
|---|---|
| Protocol | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` — PRE-FREEZE |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` — APPROVED |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — `f34129d8ecc2c8287bfb5a4f0433f551a9ce8894` |
| Primary endpoint | FFCR |
| Secondary endpoint | `final_std` |
| Consensus threshold | `< 0.01` |
| Iterations | 100 |

## 2. Pilot Matrix

| Field | Frozen pre-freeze value |
|---|---|
| Conditions | `null`, `simple`, `static`, `dgaf` |
| Topologies | `ring`, `pdmal`, `random_regular`, `small_world`, `complete` |
| Failure counts | `0,1,2,3,4,5,6,8,10` |
| Observations per seed | `180` |
| Planned pilot seeds | `50` |
| Planned raw observations | `9000` |
| `dgaf_pdmal` | OUT OF SCOPE for this pilot |

## 3. Implementation Provenance

| Item | Value |
|---|---|
| Verified ConsensusTask implementation commit | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Verified implementation CI | Run #74 — `32111556449` |
| DGAF adapter | Verified; do not modify without new adjudication |
| Protocol final blob SHA | `TBD at freeze` |
| v0.7.4 task-spec blob SHA | `TBD at freeze` |
| Runner/component blob SHAs | `TBD at freeze` |
| Topology provenance SHAs | `TBD at freeze` |
| Freeze commit SHA | `TBD` |

## 4. Environment

| Item | Value |
|---|---|
| Python | `3.12.0` in verified characterization workflow |
| NumPy | Exact pinned version from lockfile — `TBD verify at freeze` |
| NetworkX | Exact pinned version from lockfile — `TBD verify at freeze` |
| Full lockfile | `experiments/pdmal_pilot/requirements-full-lock.txt` |
| Lockfile blob SHA | `TBD at freeze` |
| Runtime CI SHA | `a0ff248eadb736f9b5835f2436791dc6ab5f66cc` |

## 5. Characterization Evidence

| Item | Value |
|---|---|
| Runtime characterization run | #14 — `32112658368` |
| Runtime artifact | `9315467977` |
| Runtime artifact digest | `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| 300-second ceiling | VERIFIED for characterization matrix |
| Blinding workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding run | `TBD` |
| Blinding artifact | `TBD` |

## 6. Durable Retention

| Item | Value |
|---|---|
| CI artifact retention | 30 days |
| Durable archive provider | `TBD` |
| Durable archive record / DOI | `TBD` |
| Archived runtime artifact digest | `TBD` |
| Archive retention period | `TBD` |
| Access-control owner | `TBD` |

## 7. Governance

| Item | Value |
|---|---|
| Expert-panel approval of v0.7.4 | Recorded in governance record |
| Matrix amendment panel approval | `PENDING` |
| Freeze timestamp | `TBD` |
| Freeze author | `Ndr Orchestration` |
| Pilot authorization record | `TBD — NOT GRANTED` |

## 8. Freeze Preconditions

The freeze manifest may only be promoted to `FROZEN` after:

1. the matrix amendment is accepted into the final protocol;
2. the exact implementation/topology/environment blob SHAs are recorded;
3. the blinding operational workflow passes and its artifact is retained;
4. durable retention is implemented and directly verified;
5. all protocol/document lifecycle metadata is updated to `FROZEN`;
6. a final freeze commit is created and its SHA recorded;
7. explicit pilot authorization is recorded.

**Current status: PRE-FREEZE. Empirical execution remains prohibited.**
