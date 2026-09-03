---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
candidate_branch: candidate/p35-validated-control-state-2026-09-02
candidate_deployment_identity: dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
candidate_deployment_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
candidate_deployment_state: READY
latest_pr200_control_plane_head: fc45d95e5cdae4026e4e50e2746d48e1cc3b7389
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the authoritative pre-authorization control record. The independently verified executable candidate is separated from later documentation/control-plane commits. Historical evidence remains scoped to the exact tested SHA, workflow run, deployment, and artifact.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.

The current deployment-bound executable candidate is `48c12c6660df7decb61f9aac4d8560526a8754eb` on `candidate/p35-validated-control-state-2026-09-02`. Vercel independently identifies deployment `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` as READY and binds it to Git SHA `48c12c...` on that branch.

PR #200 later advanced to `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`. That commit is retained as a later control-plane/documentation head and is not promoted to a deployment-bound candidate because no independently verified deployment is bound to it. Its dispatch handoff preserves the `48c12c...` candidate/deployment pair.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Executable candidate | CURRENT / PRE-FREEZE | `48c12c…` |
| Candidate deployment | ESTABLISHED / READY | `dpl_CW4…` bound to `48c12c…` |
| P2 runtime | OPEN / RE-RUN REQUIRED | Fresh exact candidate/deployment workflow execution |
| P6a CORS | OPEN / RE-RUN REQUIRED | Fresh exact candidate/deployment workflow execution |
| P3 | OPEN FOR FINAL CLOSURE | Candidate-bound operational evidence as specified by the current protocol |
| P4 | OPEN | Operational blinding/custody |
| P5 | OPEN | Full reproducibility |
| P6 | OPEN / FAIL-CLOSED | Durable archive/retrieval/hash/retention proof |
| P7 | FORMAL BINDING OPEN | Exact candidate/protocol/analysis/freeze binding |
| P8 | OPEN / FAIL-CLOSED | Current-cycle evidence required |
| P9 | SCOPED / FRESH CLOSURE REQUIRED | Historical independent evidence does not transfer |
| Freeze | NOT ESTABLISHED | No immutable pilot identity |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | N = 0 | No authorized pilot execution |

## P2 / P6a runtime boundary

P2 required inputs are candidate `48c12c...`, deployment `dpl_CW4...`, and the exact deployment URL. P6a requires the same three values plus the configured allowed origin. Both workflows require `VERCEL_AUTOMATION_BYPASS_SECRET` and emit candidate/deployment-bound provenance artifacts.

The Vercel deployment is reachable but protected by SSO for unauthenticated access. Direct HTTP reachability therefore establishes deployment health/protection only and is not P2/P6a closure evidence.

## Evidence rules

A runtime result is closing only when the workflow execution itself binds to the exact candidate and exact deployment. Historical P2/P6a artifacts from `92ff830b…`, `a43219b…`, `48c12c…` prior runs, or any earlier candidate cannot be promoted merely by documentation change. A later documentation commit does not silently redefine the deployment-bound executable candidate.

No freeze, authorization, unblinding, or empirical execution is established by this record.

## Required closure sequence

1. Execute fresh P2 against `48c12c…` / `dpl_CW4…`.
2. Execute fresh P6a against the same exact candidate/deployment and configured origin.
3. Complete current-candidate P3/P4/P5/P6 operational closure.
4. Bind P7 to the exact final candidate/protocol/analysis identity.
5. Close P8 from current-cycle evidence only.
6. Complete independent P9 closure.
7. Create and independently verify immutable freeze.
8. Obtain explicit pilot authorization.
9. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Reconciliation record

See `docs/experiment/EXECUTION_BOUNDARY_RECONCILIATION_2026-09-03.md` for the independently verified deployment identity and the distinction between the executable candidate and later PR #200 documentation/control-plane commits.
