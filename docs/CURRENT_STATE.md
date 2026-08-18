---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 1d8c62386ea09f09c1dac768e1e59d4df284edee
---

# DGAF-Framework / PDMAL — Current State

This is the repository's concise current-state snapshot. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA.

## Repository Metadata

| Field | Value |
|---|---|
| Current branch | `epistemic/evidence-architecture-v1` |
| Current head at this synchronization | `1d8c62386ea09f09c1dac768e1e59d4df284edee` |
| Current verified implementation SHA | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Protocol document | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` |
| Protocol state | PRE-FREEZE / NO DATA COLLECTION AUTHORIZED |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` |
| Latest implementation CI | Run #74 (`32111556449`) on `08500a7` |
| Runtime characterization | Run #14 (`32112658368`) on `a0ff248`; 72/72 trials completed, ceiling PASS |
| Runtime artifact | GitHub artifact `9315467977`; digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Blinding dry-run workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding dry-run evidence | OPEN — no dedicated run observed yet |
| Retention policy | `docs/experiment/PDMAL_RETENTION_POLICY.md`; policy decided, durable archive implementation still open |

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
| Blinding operational verification | OPEN | Synthetic dry-run workflow implemented; execution evidence not yet observed |
| Long-term retention | OPEN | Policy decided; durable research archive not yet established/verified |
| Freeze packet | PENDING | Waits for blinding and durable-retention closure |
| Protocol freeze | BLOCKED | Required controls remain open |
| Pilot authorization | NOT GRANTED | Explicit authorization required after freeze |
| Empirical data | 0 | No pilot execution authorized |

## Evidence boundary

Run #14 is operational characterization evidence only. It does not authorize empirical execution. Run #67/#68 and Run #74 remain scoped to their exact executed SHAs. Documentation changes after those runs do not inherit verification automatically.

The blinding dry-run uses only synthetic labels and a mock key. It must not access or print `PDMAL_BLINDING_KEY`.

## Current Next Actions

1. Execute the dedicated blinding operational dry-run workflow.
2. Review its artifact and custody evidence.
3. Establish and verify the durable research archive required by the retention policy.
4. Assemble the freeze packet.
5. Freeze protocol, implementation, environment, and analysis plan with exact SHAs and timestamp.
6. Obtain explicit pilot authorization.
7. Only then execute empirical work.

**Empirical data remains 0 until explicit pilot authorization is recorded.**
