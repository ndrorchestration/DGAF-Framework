---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 08500a7a129a39c21dc890a71a85e5d996e4c4b3
verification_evidence: Run #74 (32111556449)
---

# DGAF-Framework / PDMAL — Current State

This is the repository's concise current-state snapshot. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA.

## Repository Metadata

| Field | Value |
|---|---|
| Current branch | `epistemic/evidence-architecture-v1` |
| Current verified implementation SHA | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Protocol document | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` |
| Protocol state | PRE-FREEZE / NO DATA COLLECTION AUTHORIZED |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` |
| Task specification blob SHA | `555b81e9e30420479d26125b958d54764d648957` |
| Latest PDMAL implementation CI | Run #74 (`32111556449`) on `08500a7` |
| Runtime characterization harness | `experiments/pdmal_pilot/runtime_characterization.py` |
| Runtime characterization workflow | `.github/workflows/pdmal-runtime-characterization.yml` |
| Runtime characterization evidence | `OPEN — no dedicated run/artifact observed` |

## Gate Board

| Gate | Status | Evidence / blocker |
|---|---|---|
| Environment lock | CLOSED | Run #67 generated the full hash lock; locked installation passed and Run #68 corroborated infrastructure state |
| Topology provenance | VERIFIED | Fresh PDMAL CI coverage in the pre-freeze series |
| Artifact schema/integrity | VERIFIED | Run #74 |
| v0.7.4 task specification | APPROVED | Expert-panel approval recorded; implementation spec is current |
| ConsensusTask implementation | VERIFIED | Run #74 on `08500a7` |
| Runtime characterization | OPEN | Dedicated characterization workflow exists; execution evidence not yet observed |
| 300-second ceiling | NOT VERIFIED | Requires characterization artifact |
| Blinding operational verification | OPEN | Dry-run and custody evidence required |
| Long-term retention | OPEN | Current workflow retention is 30 days; durable policy not finalized |
| Freeze packet | PENDING | Waits for remaining controls |
| Protocol freeze | BLOCKED | Not all controls closed |
| Pilot authorization | NOT GRANTED | Explicit authorization required after freeze |
| Empirical data | 0 | No pilot execution authorized |

## Latest CI Evidence

- Run #67 (`32108612515`) — SUCCESS; head SHA `584862645ea9e033ac6e33b0dc6364c731eba7b0`; generated the genuine resolver lock.
- Run #68 (`32108821363`) — SUCCESS; head SHA `46c0d4b04025983e1d997094a4d9d404ace31928`.
- Run #73 (`32111238613`) — FAILED on `0e7ecd03`; circular-import defect.
- Run #74 (`32111556449`) — SUCCESS on `08500a7`; verifies the implementation after the circular-import correction.

Runs #67/#68 are valid evidence for the environment/infrastructure state they executed. They are not current-head evidence for later commits.

## Current Next Action

1. Execute the dedicated runtime-characterization workflow.
2. Inspect the characterization artifact and 300-second ceiling result.
3. Close or correct the runtime gate.
4. Complete blinding operational verification and long-term retention decision.
5. Assemble the freeze packet.
6. Freeze the protocol and implementation with explicit SHAs and timestamp.
7. Obtain explicit pilot authorization.

## Evidence Rule

`IMPLEMENTED` does not mean `VERIFIED`; `VERIFIED` does not mean `OPERATIONALLY CHARACTERIZED`; operational verification does not mean empirical support. Documentation alone cannot promote a gate.
