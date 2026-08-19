---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-19
applies_to_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
---

# DGAF-Framework / PDMAL — Current State

This is the repository's concise current-state snapshot. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA.

## Repository Metadata

| Field | Value |
|---|---|
| Current branch | `main` |
| Current documentation-sync head | `038a4fa56bf8e71b137896226a9d94a1bbd8c99a` |
| PR #65 merge baseline | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Current verified implementation SHA | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Protocol document | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` |
| Protocol state | PRE-FREEZE / NO DATA COLLECTION AUTHORIZED |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — `f34129d8ecc2c8287bfb5a4f0433f551a9ce8894` |
| Freeze manifest | `docs/experiment/FREEZE_MANIFEST.md` — PRE-FREEZE / PENDING FINAL CONTROLS |
| Latest implementation CI | Run #74 (`32111556449`) on `08500a7` |
| Runtime characterization | Run #14 (`32112658368`) on `a0ff248`; 72/72 trials completed, ceiling PASS |
| Runtime artifact | GitHub artifact `9315467977`; ZIP digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Runtime inner JSON | `runtime_characterization.json`; SHA-256 `f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea` |
| Blinding dry-run workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding dry-run evidence | CLOSED / PASS — Run `32113226935`, artifact `9328114023` |
| Retention policy | `docs/experiment/PDMAL_RETENTION_POLICY.md`; durable archive implementation/verification remains open |

## Pilot Matrix

The pre-freeze amendment defines the intended pilot matrix pending final protocol incorporation and expert-panel record:

```text
Conditions:      null, simple, static, dgaf
Topologies:      ring, pdmal, random_regular, small_world, complete
Failure counts:  0,1,2,3,4,5,6,8,10
Per seed:        4 × 5 × 9 = 180 observations
50-seed plan:    9,000 planned raw observations before exclusions
Out of scope:    dgaf_pdmal
```

## Gate Board

| Gate | Status | Evidence / blocker |
|---|---|---|
| PR #65 merge | CLOSED | Merge commit `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Environment lock | CLOSED | Run #67 generated the full hash lock; locked installation passed and Run #68 corroborated infrastructure state |
| Topology provenance | VERIFIED | Fresh PDMAL CI coverage in the pre-freeze series |
| Artifact schema/integrity | VERIFIED | Run #74 |
| v0.7.4 task specification | APPROVED | Expert-panel approval recorded |
| ConsensusTask implementation | VERIFIED | Run #74 on `08500a7` |
| Runtime characterization | OPERATIONALLY CHARACTERIZED | Run #14; 72/72 trials completed and artifact validated |
| 300-second ceiling | VERIFIED FOR CHARACTERIZATION MATRIX | All measured seed runtimes remained below 300 seconds |
| Matrix amendment | OPEN | Final incorporation/acceptance record still pending |
| Blinding operational verification | CLOSED / PASS | Run `32113226935`; synthetic custody dry-run; no production secret access; no empirical data |
| Long-term retention | OPEN | Durable research archive not yet independently verified |
| Freeze packet | PENDING | Remaining matrix, retention, and exact freeze-state metadata |
| Protocol freeze | BLOCKED | Required final controls remain open |
| Pilot authorization | NOT GRANTED | Separate governance decision after freeze |
| Empirical data | 0 | No pilot execution authorized |

## Evidence boundary

The merge of PR #65 is a repository-state event, not empirical evidence. Runtime characterization remains scoped to its exact executed SHA `a0ff248eadb736f9b5835f2436791dc6ab5f66cc`; the blinding operational run remains scoped to `1d8c62386ea09f09c1dac768e1e59d4df284edee`.

The ZIP artifact digest and inner `runtime_characterization.json` digest are distinct provenance identities and must not be substituted for one another.

Empirical data remains `0`. Pilot authorization remains `NOT GRANTED`.

## Current Next Actions

1. Obtain and record final matrix-amendment acceptance into the protocol.
2. Establish and directly verify durable retention for the research artifact set.
3. Populate exact protocol, task-spec, runner/component, topology, and environment blob SHAs in the freeze manifest.
4. Create the dedicated freeze commit once all freeze preconditions are genuinely satisfied.
5. Record the freeze commit SHA and timestamp.
6. Make a separate explicit pilot-authorization decision after freeze.
7. Only then execute empirical work.

**Empirical data remains 0 until explicit pilot authorization is recorded.**
