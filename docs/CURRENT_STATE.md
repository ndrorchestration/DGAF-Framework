---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
current_mainline_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
current_mainline_deployment: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
current_mainline_deployment_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions are recorded through the project's governance process. Historical evidence remains scoped to the exact SHA, workflow run, deployment, and artifact that produced it.

## Current identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The current mainline candidate is `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`. Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` is READY and bound to that exact Git SHA. The canonical production origin used for P6a is `https://dynamicgovernanceagenticformation.vercel.app`; the exact deployment URL is retained separately for deployment identity.

The former executable candidate `48c12c6660df7decb61f9aac4d8560526a8754eb` and deployment `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` are historical/non-transferable. Earlier candidates and control-plane heads remain provenance only.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Current mainline candidate | CURRENT / PRE-FREEZE | `7c1cc4…` |
| Candidate deployment | VERIFIED READY | `dpl_8Msuf…` bound to `7c1cc4…` |
| P2 | CLOSED / VERIFIED | run `33730195621`, artifact `9883521704` |
| P6a | CLOSED / VERIFIED | run `33728695806`, artifact `9882965299` |
| P3 | VERIFIED AT ENGINEERING/WORKFLOW SCOPE | current exact-candidate operational closure remains required where specified |
| P4 | OPEN | operational blinding/custody |
| P5 | OPEN | final exact-candidate reproducibility |
| P6 | OPEN / FAIL-CLOSED | durable archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | exact final candidate/protocol/analysis binding |
| P8 | OPEN / FAIL-CLOSED | current-cycle prerequisites and analysis lock |
| P9 | OPEN | fresh current-candidate independent verification |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized pilot execution |

## Current P2 / P6a evidence

P2 run `33730195621` verified the exact candidate/deployment pair with all five required runtime predicates passing; artifact `9883521704` has digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.

P6a run `33728695806` verified the same exact candidate/deployment binding using the canonical production origin; all four POST/preflight predicates passed. Artifact `9882965299` has digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

## Evaluator and workflow integrity

Completion-controller results are candidate-bound to the triggering workflow's SHA. A successful evaluator run on a documentation branch is not current-main evidence. The PDMAL instrumentation workflow is therefore being isolated from documentation-only changes by PR #213; its successful PR-candidate run is validation of the trigger-isolation change, not experimental evidence for `7c1cc4…`.

## Evidence boundary

No historical P2/P6a artifact transfers across candidate SHA, deployment identity, or triggering workflow identity. Documentation changes do not authorize execution, create a freeze, or advance empirical N. CI success, deployment readiness, deterministic dry runs, and runtime verification are engineering evidence, not experimental efficacy evidence.

## Closure sequence

`operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
