---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 6680bc95ddbf4fc430973c8eb78e736a28329a38
---

# PDMAL Current Control State

This document is the detailed operational gate record. GitHub Actions evidence is authoritative for execution state; historical runs are never promoted to current-head evidence. Use `docs/CURRENT_STATE.md` for the concise snapshot and `docs/evidence/PDMAL_EVIDENCE_INDEX.md` for evidence mapping.

## Current branch and implementation

- Branch: `epistemic/evidence-architecture-v1`
- Current documentation head at this synchronization: `6680bc95ddbf4fc430973c8eb78e736a28329a38`
- Authoritative task specification: `v0.7.4`
- ConsensusTask implementation: CI-verified by Run #74 on `08500a7`
- Runtime characterization: operationally verified by Run #14 on `a0ff248`
- Blinding operational test: workflow/script implemented; dedicated execution evidence not yet observed
- Retention: policy recorded; durable archive implementation remains open

## Gate board

| Control | State | Evidence / blocker |
|---|---|---|
| Environment lock | CLOSED | Runs #67/#68 passed; genuine resolver lock generation and locked installation observed |
| Fresh contract verification | CLOSED | Run #74 passed after circular-import correction |
| Topology provenance | VERIFIED | Fingerprint/reproducibility tests exercised in the PDMAL CI series |
| Artifact schema/integrity | VERIFIED | Schema versioning, fail-closed validation, and current pre-freeze artifact checks |
| Task specification | APPROVED | v0.7.4 approved for implementation |
| ConsensusTask | VERIFIED | Run #74, commit `08500a7` |
| Runtime characterization | OPERATIONALLY CHARACTERIZED | Run #14 `32112658368`; 72/72 trials completed; artifact validated |
| 300-second seed ceiling | VERIFIED FOR CHARACTERIZATION MATRIX | Runtime artifact shows all measured seed runtimes within ceiling |
| Blinding custody | OPEN | Synthetic dry-run implementation exists; workflow execution and procedural custody evidence pending |
| Long-term retention | OPEN | Policy decided; durable research archive not yet established/verified |
| Freeze packet | PENDING | Dependent on blinding and durable-retention closure |
| Protocol freeze | BLOCKED | Not all required controls closed |
| Pilot authorization | NOT GRANTED | Requires explicit post-freeze authorization |
| Empirical data | 0 | No empirical execution authorized |

## Evidence boundaries

Run #14 is non-empirical operational verification. It does not authorize empirical execution. Its artifact is `9315467977` with digest `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27`.

Run #67, Run #68, and Run #74 remain scoped to their exact executed SHAs. Later documentation commits do not inherit their verification automatically.

The blinding dry-run uses only synthetic labels and a mock key. It must not access or print `PDMAL_BLINDING_KEY`. A passing synthetic dry-run is technical/procedural evidence, not authorization to use the production secret.

## Critical path

1. Execute the dedicated blinding operational dry-run workflow.
2. Review its evidence artifact and document the procedural custody outcome.
3. Establish and verify the durable research archive required by the retention policy.
4. Assemble the freeze packet.
5. Freeze protocol, implementation, environment, and analysis plan with exact SHAs and timestamp.
6. Obtain explicit pilot authorization.
7. Only then execute empirical work.

No empirical execution is authorized by this state record.
