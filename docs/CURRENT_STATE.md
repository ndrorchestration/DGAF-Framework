---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-04
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
current_mainline_control_plane_head: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
current_state_anchor_note: later documentation-only reconciliation commits descend from this state and do not alter executable runtime semantics
candidate identity: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
verified_runtime_deployment: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
deployment identity: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
verified_runtime_deployment_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it.

## Current identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The current control-plane state is anchored at `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`; subsequent documentation-only descendants, including later reconciliation of dated records, remain documentation reconciliation and do not alter executable runtime semantics. The TLA+ v1.8.0 digest is `16b8cd970e07147ff91f126baecba7edd98202e5ab33220a42f8f4358ee94b2b`.

The verified executable runtime candidate remains `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, with Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to that exact Git SHA. The control-plane/documentation lineage must not be conflated with that separately scoped runtime identity.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Control-plane state anchor | CURRENT | `89be386b…` |
| Verified executable runtime candidate | CURRENT VERIFIED RUNTIME IDENTITY | `7c1cc4…` |
| Candidate deployment | VERIFIED READY | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` bound to `7c1cc4…` |
| P2 | CLOSED / VERIFIED | run `33730195621`, artifact `9883521704` |
| P6a | CLOSED / VERIFIED | run `33728695806`, artifact `9882965299` |
| P3 | OPEN / CURRENT EVIDENCE REQUIRED | artifact-contract closure |
| P4 | OPEN | operational blinding/custody |
| P5 | OPEN | reproducibility/provenance closure |
| P6 | OPEN / FAIL-CLOSED | durable archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | exact final candidate/protocol/analysis binding |
| P8 | OPEN / FAIL-CLOSED | exact prerequisites and analysis lock |
| P9 | OPEN | independent verification |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized pilot execution |

## Closed control-plane remediation

- **PR #223 — MERGED:** TLA+ v1.8.0 digest corrected to the exact official release-asset digest.
- **PR #219 — MERGED:** completion evidence bound to the exact triggering workflow run and artifact.
- **PR #221 — MERGED:** hash-locked dry-run dependencies, no persisted Git credentials, exact-candidate evidence registry.
- **PR #222 — MERGED:** scheduled live regression Vercel protection bypass with fail-closed credential handling.
- **PRs #220/#230/#231 — CLOSED / NOT MERGED:** proposed canonical-matrix assertion determined redundant with existing canonical coordinate membership, exact per-condition cardinality, and duplicate-cell rejection.

## Candidate manifest reconciliation

`docs/experiment/NEW_CANDIDATE_MANIFEST.md` continues to bind the verified executable runtime candidate `7c1cc4…` to deployment `dpl_8Msuf…`. Its control-plane successor reference was corrected to the documentation lineage represented by the current reconciliation anchor. This did not change the runtime candidate, deployment, P2, or P6a evidence boundaries.

## Evidence boundary

Closed P2/P6a runtime evidence remains scoped to the verified executable runtime identity above. Documentation/control-plane changes do not reopen those predicates unless the runtime surface or governing acceptance conditions materially change. No empirical efficacy conclusion follows from runtime or CI checks.

The PDMAL instrumentation workflow remains isolated from documentation-only changes. Structural, pre-freeze, or dry-run success validates workflow/control infrastructure and does not advance empirical N.

## Current substantive closure work

The remaining task is one-candidate evidence assembly, not additional speculative governance architecture:

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

The active completion control record is GitHub Issue #232. Superseded planning records #184 and #186 are retained as historical provenance and no longer define the active critical path.

## Documentation architecture boundary

The agent-identity, registry-synchronization, numerical-instrument, metrics-provenance, and documentation-integration workstreams remain separately scoped. Open issues #224, #225, #226, #228, and #229 are not silently promoted to resolved merely because the mainline control plane has advanced.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
