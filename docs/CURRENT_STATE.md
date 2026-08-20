---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-19
applies_to_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
---

# DGAF-Framework / PDMAL — Current State

This is the repository's concise current-state snapshot. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA. The current main branch head is authoritative from the Git ref and is not duplicated here as self-referential document metadata.

## Repository Metadata

| Field | Value |
|---|---|
| Current branch | `main` |
| PR #65 merge baseline / freeze target | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Current verified implementation SHA | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Protocol document | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` |
| Protocol state | PRE-FREEZE / NO DATA COLLECTION AUTHORIZED |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — `f34129d8ecc2c8287bfb5a4f0433f551a9ce8894` — ACCEPTED / INCORPORATED per governance record |
| Freeze manifest | `docs/experiment/FREEZE_MANIFEST.md` — PRE-FREEZE / PENDING FINAL CONTROLS |
| Primary-contrast record | `docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` — OPEN / METHODOLOGICAL ADJUDICATION REQUIRED |
| Latest implementation CI | Run #74 (`32111556449`) on `08500a7` |
| Runtime characterization | Run #14 (`32112658368`) on `a0ff248`; 72/72 trials completed, ceiling PASS |
| Runtime artifact | GitHub artifact `9315467977`; ZIP digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Runtime inner JSON | `runtime_characterization.json`; SHA-256 `f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea` |
| Blinding dry-run workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding dry-run evidence | CLOSED / PASS — Run `32113226935`, artifact `9328114023` |
| Retention policy | `docs/experiment/PDMAL_RETENTION_POLICY.md`; durable archive implementation/verification remains open |
| Pilot executor | OPEN — `run_pilot.py` fail-closes pilot mode because the real experimental task executor is not yet implemented |

## Pilot Matrix

The v0.7.5 amendment is incorporated into the current protocol and accepted by governance. The protocol remains pre-freeze because other final controls, the primary contrast decision, and the actual pilot executor remain open.

```text
Conditions:      null, simple, static, dgaf
Topologies:      ring, pdmal, random_regular, small_world, complete
Out of scope:    dgaf_pdmal
```

| Gate | Status | Evidence / blocker |
|---|---|---|
| PR #65 merge | CLOSED | Merge commit `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Environment lock | CLOSED | Run #67 generated the full hash lock; locked installation passed and Run #68 corroborated infrastructure state |
| Topology provenance | VERIFIED | Fresh PDMAL CI coverage in the pre-freeze series |
| Artifact schema/integrity | VERIFIED | Run #74 |
| ConsensusTask implementation | VERIFIED | Run #74 on `08500a7` |
| Runtime characterization | OPERATIONALLY CHARACTERIZED | Run #14; 72/72 trials completed and artifact validated |
| 300-second ceiling | VERIFIED FOR CHARACTERIZATION MATRIX | All measured seed runtimes remained below 300 seconds |
| Matrix amendment | ACCEPTED / INCORPORATED | v0.7.5 incorporated; governance acceptance recorded separately; not the same as protocol freeze |
| Primary contrast | OPEN | `PRIMARY_CONTRAST_ADJUDICATION.md`; expert/statistical adjudication required |
| Blinding operational verification | CLOSED / PASS | Run `32113226935`; synthetic custody dry-run; no production secret access; no empirical data |
| Long-term retention | OPEN | Durable research archive not yet independently verified |
| Topology fingerprints | OPEN | Fingerprint function exists; final values not yet recorded in freeze manifest |
| Freeze manifest | PENDING | Exact provenance, fingerprints, retention, primary contrast, and execution hardening remain open |
| Runner freeze-SHA binding | OPEN | Environment gates exist; execution is not yet bound to the recorded freeze commit SHA |
| Pilot executor implementation | OPEN | `run_pilot.py` explicitly refuses pilot mode because the real experimental task executor is not implemented |
| Protocol freeze | BLOCKED | Primary contrast + retention + exact freeze metadata + execution hardening + pilot executor remain open |
| Pilot authorization | NOT GRANTED | Separate governance decision after freeze |

## Evidence boundary

The merge of PR #65 is a repository-state event, not empirical evidence. Runtime characterization remains scoped to its exact executed SHA `a0ff248eadb736f9b5835f2436791dc6ab5f66cc`; the blinding operational run remains scoped to its recorded execution evidence.

The ZIP artifact digest and inner `runtime_characterization.json` digest are distinct provenance identities and must not be substituted for one another.

Empirical data remains `0`. Pilot authorization remains `NOT GRANTED`.

## Current Next Actions

1. Obtain and record the expert/statistical adjudication of the primary contrast.
2. Establish and directly verify durable retention for the research artifact set.
3. Generate and record the deterministic topology fingerprints required by the freeze manifest.
4. Populate the remaining exact protocol, task-spec, runner/component, topology, and environment provenance fields in the freeze manifest.
5. Implement and test exact freeze-SHA binding in the pilot runner so execution cannot proceed from an unintended code state.
6. Implement and verify the real experimental task executor required for pilot mode.
7. Reconcile the stale pre-freeze wording in `PDMAL_EXPERIMENT_PROTOCOL.md` so it reflects matrix acceptance and the still-open primary contrast before the freeze packet is finalized.
8. Perform the final adversarial freeze audit.
9. Create the dedicated freeze commit once all freeze preconditions are genuinely satisfied.
10. Record the freeze commit SHA and timestamp and verify the frozen tree.
11. Make a separate explicit pilot-authorization decision after freeze.
12. Only then execute empirical work.

**Empirical data remains 0 until explicit pilot authorization is recorded.**
