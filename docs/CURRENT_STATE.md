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
| Authoritative repository baseline | `915e454e27eb2770e7f40a067a881b0783feaae4` — PR #65 merge baseline / freeze target baseline |
| Current reconciliation branch | `epistemic/pdmal-freeze-readiness-reconciliation` |
| Current reconciliation branch head | `cd620af806d4cf2830efbc55283891c9e5f239e8` |
| Latest main documentation synchronization commit | `7ed2cd072ee26d12d9417b0e9b41508b76a75d83` |
| Current verified implementation SHA | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Protocol document | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` |
| Protocol state | PRE-FREEZE / NO DATA COLLECTION AUTHORIZED |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — ACCEPTED / INCORPORATED into `915e454e...` |
| Freeze manifest | `docs/experiment/FREEZE_MANIFEST.md` — PRE-FREEZE / PENDING FINAL CONTROLS |
| Latest implementation CI | Run #74 (`32111556449`) on `08500a7` |
| PR #65 documentation/epistemic checks | Doc Lint PR Scope Run #2 (`32224203776`) PASS; Claim Hygiene Run #136 (`32224203749`) PASS; these are scoped PR-governance evidence, not empirical evidence |
| Runtime characterization | Run #14 (`32112658368`) on `a0ff248`; 72/72 trials completed, ceiling PASS |
| Runtime artifact | GitHub artifact `9315467977`; ZIP digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Runtime inner JSON | `runtime_characterization.json`; SHA-256 `f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea` |
| Blinding dry-run workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding dry-run evidence | CLOSED / PASS — Run `32113226935`, artifact `9328114023` |
| Retention policy | `docs/experiment/PDMAL_RETENTION_POLICY.md`; durable archive implementation/verification remains open |

### SHA-labeling rule

The repository identifiers above have distinct meanings:

- **Authoritative repository baseline:** the merged PR #65 commit used as the current experimental freeze target/baseline.
- **Current reconciliation branch head:** the latest documentation/reconciliation commit on the working branch; it is not itself the freeze commit.
- **Latest main documentation synchronization commit:** the newest committed documentation state on `main`; it does not retroactively change the SHA of historical execution evidence.
- **Historical execution SHA:** the exact source commit actually exercised by a retained workflow run or artifact.

Historical execution SHAs must always remain attached to their exact runs and artifacts.

## Pilot Matrix

The v0.7.5 amendment is **ACCEPTED / INCORPORATED** and defines the intended pilot matrix pending final protocol freeze:

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
| Matrix amendment | ACCEPTED / INCORPORATED | Governance acceptance recorded; incorporated into merged control plane `915e454e...` |
| FFCR aggregation rule | PRE-FREEZE DOCUMENTATION CLOSURE | Component-trial aggregation is defined in the freeze-readiness reconciliation; final protocol incorporation pending |
| Primary contrast hierarchy | OPEN / ADJUDICATION REQUIRED | Current protocol specifies prespecified contrasts but does not yet establish `dgaf` vs `null` as the sole primary contrast |
| Blinding operational verification | CLOSED / PASS | Run `32113226935`; synthetic custody dry-run; no production secret access; no empirical data |
| Long-term retention | OPEN | Durable research archive not yet independently verified |
| Freeze packet | PENDING | Primary contrast adjudication, retention, exact provenance, and final freeze-state metadata remain open |
| Protocol freeze | BLOCKED | Required final controls remain open |
| Pilot authorization | NOT GRANTED | Separate governance decision after freeze |
| Empirical data | 0 | No pilot execution authorized |

## FFCR aggregation control

For each seed and condition, the seed-level FFCR is derived from the 45 component workload cells spanning five topologies and nine failure-count levels:

```text
FFCR_condition,seed =
    successful eligible component trials
    /
    eligible component trials
```

Each component trial has equal weight; no topology-first or failure-level-first averaging is performed before the seed-level FFCR is calculated.

A trial is **eligible** when it is attempted, including execution-level retries, and is not excluded under the frozen objective exclusion rules. An **excluded** trial remains retained with an explicit exclusion reason and is removed from the FFCR denominator only when a pre-registered exclusion rule applies. A valid unfavorable outcome is never excluded because of its result.

Failure count `0` is included in the primary workload and contributes equally to the denominator as a no-failure baseline condition.

## Evidence boundary

The merge of PR #65 is a repository-state event, not empirical evidence. Runtime characterization remains scoped to its exact executed SHA `a0ff248eadb736f9b5835f2436791dc6ab5f66cc`; the blinding operational run remains scoped to its exact executed source and artifact.

The ZIP artifact digest and inner `runtime_characterization.json` digest are distinct provenance identities and must not be substituted for one another.

Empirical data remains `0`. Pilot authorization remains `NOT GRANTED`.

## Current Next Actions

1. Resolve the exact primary contrast hierarchy through the existing statistical/panel authority or an explicit pre-freeze adjudication.
2. Establish and directly verify durable retention for the research artifact set.
3. Populate exact protocol, task-spec, runner/component, topology, and environment blob SHAs in the freeze manifest.
4. Complete the P1 documentation reconciliation and run a final contradiction scan.
5. Harden the pilot runner so authorization also verifies the requested execution source against the recorded freeze commit/reference.
6. Create the dedicated freeze commit once all freeze preconditions are genuinely satisfied.
7. Record the freeze commit SHA and timestamp only after Git produces the freeze commit.
8. Make a separate explicit pilot-authorization decision after freeze.
9. Only then execute empirical work.

**Empirical data remains 0 until explicit pilot authorization is recorded.**
