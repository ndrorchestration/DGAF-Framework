---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-20
applies_to_sha: ba3a38bb3553886e6bf449662d066b52b60d1b5b
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA.

## Current authoritative state

| Gate | Status | Evidence / note |
|---|---|---|
| PR #75 | MERGED | `a44e42cd3040a822656e724c8b47aa02221baf3f` |
| Historical implementation freeze | SUPERSEDED FOR CORRECTED RUNNER | `3510b86889cd341f7a7cf9ab684fd37b2fafd758`; retained as historical evidence |
| Corrected pilot runner | CANDIDATE | `fec7a6f577373aeb5037b8b5960bcfa7e0384a0d` |
| Frozen pilot artifact schema | CANDIDATE | `pilot_artifact_schema.py` |
| Security adversarial suite | CANDIDATE | `test_security_controls.py`; requires CI execution |
| Environment | VERIFY | Locked target: Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1 |
| Primary contrast | OPEN | Explicit methodological adjudication required before authorization |
| Topology fingerprints | VERIFY / RECONCILE | Final frozen values must be checked against manifest/protocol |
| Durable retention | VERIFY / RECONCILE | Pilot archive location and checksum procedure require direct evidence |
| Analysis implementation | MUST BE FROZEN BEFORE UNBLINDING | Exact implementation/configuration SHA not yet recorded |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | 0 | Acceptance/characterization observations remain non-empirical |

## Freeze boundary

The historical freeze at `3510b868...` must not be silently reused after material runner corrections. The corrected runner is therefore a new freeze candidate. No pilot execution is authorized from this branch until CI, smoke, security, environment, scientific, retention, and analysis-lock gates close and a new freeze manifest is created.

## Pilot matrix

```text
Conditions:      null, simple, static, dgaf
Topologies:      ring, pdmal, random_regular, small_world, complete
Failure counts:  0, 1, 2, 3, 4, 5, 6, 8, 10
Trials/seed:     180
Pilot seeds:     50
Expected pilot records: 9,000
```

## Evidence boundary

The historical 360-observation executor acceptance run demonstrates execution capability at its exact SHA. It does not establish PDMAL efficacy and remains outside empirical N. The corrected runner has not yet produced pilot data.

## Immediate next actions

1. Run CI for the corrected runner/security suite.
2. Verify Python 3.12.0 and locked dependencies.
3. Run final one-seed smoke and artifact validation.
4. Reconcile topology fingerprints and durable retention.
5. Adjudicate the primary contrast.
6. Identify and freeze the analysis implementation/configuration SHA.
7. Create the new freeze manifest for the corrected runner.
8. Produce the pre-authorization verification record.
9. Obtain explicit pilot authorization.
10. Only then execute the 50-seed pilot.

**Empirical data remains 0. Pilot authorization is not granted.**
