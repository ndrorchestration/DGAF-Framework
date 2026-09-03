---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_deployment_identity: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_deployment_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_deployment_state: READY
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to the exact tested SHA, workflow run, deployment, and artifact.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The current mainline executable candidate is `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`. Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` is READY and bound to that exact Git SHA.

The former candidate `48c12c6660df7decb61f9aac4d8560526a8754eb` and deployment `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` are historical/non-transferable.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Executable candidate | CURRENT / PRE-FREEZE | `7c1cc4…` |
| Candidate deployment | ESTABLISHED / READY | `dpl_8Msuf…` bound to `7c1cc4…` |
| P2 runtime | CLOSED / VERIFIED | Run `33730195621`; artifact `9883521704` |
| P6a CORS | CLOSED / VERIFIED | Run `33728695806`; artifact `9882965299` |
| P3 | VERIFIED AT ENGINEERING/WORKFLOW SCOPE | Current exact-candidate operational closure remains required where specified |
| P4 | OPEN | Operational blinding/custody |
| P5 | OPEN | Final exact-candidate reproducibility |
| P6 | OPEN / FAIL-CLOSED | Durable archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact candidate/protocol/analysis/freeze binding |
| P8 | OPEN / FAIL-CLOSED | Current-cycle prerequisites and analysis lock |
| P9 | OPEN | Fresh current-candidate independent verification |
| Freeze | NOT ESTABLISHED | No immutable pilot identity |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## Runtime evidence boundary

P2 and P6a are closed only for the exact `7c1cc4…` / `dpl_8Msuf…` binding. P2 artifact `9883521704` records all five required runtime predicates passing. P6a artifact `9882965299` records all four required CORS POST/preflight predicates passing with the canonical production origin.

The successful PDMAL instrumentation run on PR #213 is not current-main experimental evidence. It validates the trigger-isolation change on that PR candidate. The instrumentation workflow must be deliberately executed against the exact intended candidate before current-cycle P3/P4/P5/P6 closure can be claimed.

## Evidence rules

A runtime or experimental result is closing only when its workflow execution binds to the exact candidate and required deployment identity. Historical artifacts cannot be promoted by documentation changes. Documentation commits do not authorize execution or create a freeze.

## Required closure sequence

1. Review/accept PR #213 trigger isolation after checks.
2. Deliberately execute PDMAL instrumentation against exact candidate `7c1cc4…`; do not substitute documentation-branch runs.
3. Re-establish current-cycle P3/P4/P5 evidence.
4. Complete P6 durable archive, independent retrieval, and SHA-256 round-trip proof.
5. Execute fresh independent P9 against the same exact candidate/evidence set.
6. Finalize P7 candidate/protocol/analysis binding.
7. Evaluate P8 only after current prerequisites are satisfied and exact-bound.
8. Create and independently verify immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
