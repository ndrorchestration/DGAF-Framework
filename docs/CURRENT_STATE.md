---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 781e5e3fd44f953c67057fb5afd105ee8cb8bd70
---

# DGAF-Framework / PDMAL — Current State

This is the repository's concise current-state snapshot. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA.

## Repository Metadata

| Field | Value |
|---|---|
| Current branch | `epistemic/evidence-architecture-v1` |
| Current head at this synchronization | `781e5e3fd44f953c67057fb5afd105ee8cb8bd70` |
| Current verified implementation SHA | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Protocol document | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` |
| Protocol state | PRE-FREEZE / NO DATA COLLECTION AUTHORIZED |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — `f34129d8ecc2c8287bfb5a4f0433f551a9ce8894` |
| Freeze manifest | `docs/experiment/FREEZE_MANIFEST.md` — PRE-FREEZE |
| Latest implementation CI | Run #74 (`32111556449`) on `08500a7` |
| Runtime characterization | Run #14 (`32112658368`) on `a0ff248`; 72/72 trials completed, ceiling PASS |
| Runtime artifact | GitHub artifact `9315467977`; digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Blinding dry-run workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding dry-run evidence | OPEN — no dedicated run observed yet |
| Retention policy | `docs/experiment/PDMAL_RETENTION_POLICY.md`; policy decided, durable archive implementation still open |

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
| Environment lock | CLOSED | Run #67 generated the full hash lock; locked installation passed and Run #68 corroborated infrastructure state |
| Topology provenance | VERIFIED | Fresh PDMAL CI coverage in the pre-freeze series |
| Artifact schema/integrity | VERIFIED | Run #74 |
| v0.7.4 task specification | APPROVED | Expert-panel approval recorded |
| ConsensusTask implementation | VERIFIED | Run #74 on `08500a7` |
| Runtime characterization | OPERATIONALLY CHARACTERIZED | Run #14; 72/72 trials completed and artifact validated |
| 300-second ceiling | VERIFIED FOR CHARACTERIZATION MATRIX | All measured seed runtimes remained below 300 seconds |
| Pilot matrix reconciliation | OPEN | Amendment v0.7.5 committed; final protocol incorporation and panel record pending |
| Blinding operational verification | OPEN | Synthetic dry-run workflow implemented; execution evidence not yet observed |
| Long-term retention | OPEN | Policy decided; durable research archive not yet established/verified |
| Freeze packet | PENDING | Waits for matrix, blinding, and durable-retention closure |
| Protocol freeze | BLOCKED | Required controls remain open |
| Pilot authorization | NOT GRANTED | Explicit authorization required after freeze |
| Empirical data | 0 | No pilot execution authorized |

## Evidence boundary

Run #14 is operational characterization evidence only. It does not authorize empirical execution. Run #67/#68 and Run #74 remain scoped to their exact executed SHAs. Documentation changes after those runs do not inherit verification automatically.

The blinding dry-run uses only synthetic labels and a mock key. It must not access or print `PDMAL_BLINDING_KEY`.

The matrix amendment is a specification artifact, not yet the frozen protocol. The final pilot scope must be incorporated into the protocol and recorded as accepted before freeze.

## Current Next Actions

1. Obtain expert-panel acceptance of the matrix amendment and incorporate it into the final protocol.
2. Execute the dedicated blinding operational dry-run workflow.
3. Review its artifact and custody evidence.
4. Establish and verify the durable research archive required by the retention policy.
5. Assemble the freeze packet and populate the final freeze manifest with exact blob SHAs.
6. Freeze protocol, implementation, environment, and analysis plan with exact SHAs and timestamp.
7. Obtain explicit pilot authorization.
8. Only then execute empirical work.

**Empirical data remains 0 until explicit pilot authorization is recorded.**
