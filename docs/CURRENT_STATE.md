---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
verified_executable_candidate_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
verified_executable_candidate_branch: candidate/p35-validated-control-state-2026-09-02
verified_executable_deployment: dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
verified_executable_deployment_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
latest_pr200_control_plane_head: fc45d95e5cdae4026e4e50e2746d48e1cc3b7389
candidate_status: PRE-FREEZE / FAIL-CLOSED / DEPLOYMENT-BOUND / NOT AUTHORIZED
empirical_n: 0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

## Current identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The independently verified executable candidate is `48c12c6660df7decb61f9aac4d8560526a8754eb` on `candidate/p35-validated-control-state-2026-09-02`. Vercel independently reports deployment `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` as READY with Git SHA `48c12c...` and the same candidate branch. This is the current deployment-bound execution candidate.

PR #200 later advanced to documentation/control-plane head `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`. That later commit is not promoted to a deployment-bound runtime candidate because no verified deployment is bound to that SHA. Its dispatch handoff preserves the `48c12c...` candidate/deployment pair.

Earlier candidates including `92ff830b...`, `a43219b...`, and remediation-only heads are historical or engineering-scoped identities. Their deployment-bound runtime and experimental evidence does not transfer to the current execution candidate.

## Runtime gate state

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Executable candidate | CURRENT / PRE-FREEZE | `48c12c…` |
| Candidate deployment | VERIFIED READY | `dpl_CW4…` bound to `48c12c…` |
| P2 | OPEN / RE-RUN REQUIRED | exact candidate/deployment workflow execution |
| P6a | OPEN / RE-RUN REQUIRED | exact candidate/deployment workflow execution |
| P3 | OPEN FOR FINAL CLOSURE | current-candidate operational evidence as required |
| P4 | OPEN | operational blinding/custody |
| P5 | OPEN | full reproducibility |
| P6 | OPEN / FAIL-CLOSED | durable archive/retention |
| P7 | FORMAL BINDING OPEN | exact final candidate/protocol/analysis authority binding |
| P8 | OPEN / FAIL-CLOSED | current-cycle closure remains required |
| P9 | SCOPED EVIDENCE ONLY | fresh final independent closure remains required |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized pilot execution |

## P2 / P6a dispatch boundary

P2 requires candidate SHA `48c12c6660df7decb61f9aac4d8560526a8754eb`, deployment `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`, and the exact deployment URL. P6a requires the same values plus the configured allowed origin. Both workflows require the repository's protected Vercel automation bypass secret and emit candidate/deployment-bound provenance artifacts.

The existing deployment is reachable but protected by Vercel SSO from an unauthenticated session. Direct reachability therefore does not substitute for the authenticated workflow evidence.

## Evidence boundary

No historical P2/P6a artifact transfers across candidate SHA, deployment identity, or triggering workflow identity. Documentation commits do not authorize execution, create a freeze, or advance empirical N.

## Closure sequence

`P2 + P6a exact runtime → P3/P4/P5/P6 operational closure → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
