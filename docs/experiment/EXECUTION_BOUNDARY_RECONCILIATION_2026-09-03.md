# Execution Boundary Reconciliation — 2026-09-03

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / EMPIRICAL N=0

This is the current execution-boundary documentation authority. It separates the independently verified executable candidate from later documentation/control-plane commits and records non-closing runtime observations explicitly.

## Authoritative identities

- Immutable P-35 validation boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`
- Verified executable candidate: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- Candidate branch: `candidate/p35-validated-control-state-2026-09-02`
- Verified Vercel deployment: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- Verified deployment SHA: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- Verified deployment URL: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- Allowed origin: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- Later PR #200 control-plane/documentation head: `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`

The later `fc45d95e...` commit is not promoted to a deployment-bound runtime candidate. Its dispatch-handoff content preserves the `48c12c...` candidate/deployment pair. No separate Vercel deployment bound to `fc45d95e...` has been verified.

## Deployment verification

Vercel independently reports `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` as `READY`, source `git`, branch `candidate/p35-validated-control-state-2026-09-02`, and Git SHA `48c12c...`. The deployment therefore establishes an exact candidate/deployment identity for runtime testing.

Direct unauthenticated access reaches the Vercel SSO protection boundary. This demonstrates reachability/protection only; it is not P2/P6a closure evidence.

## Non-closing P6a runtime observation

A live observation against the verified deployment exercised the four P6a request classes and matched the defined response predicates:

| Case | Observed result | Interpretation |
|---|---|---|
| Allowed-origin POST | `503` + expected `Access-Control-Allow-Origin` | Matches P6a predicate |
| Disallowed-origin POST | `503` + no `Access-Control-Allow-Origin` | Matches P6a predicate |
| Allowed-origin preflight | `204` + required origin/method/header allowances | Matches P6a predicate |
| Disallowed-origin preflight | `403` + no `Access-Control-Allow-Origin` | Matches P6a predicate |

This is deployment-scoped runtime observation. It does not close P6a because the governing evidence contract requires the designated GitHub Actions workflow run to execute and upload its candidate/deployment-bound artifact.

## Required exact dispatch inputs

### P2

```text
candidate_sha=48c12c6660df7decb61f9aac4d8560526a8754eb
deployment_id=dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
base_url=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app
```

### P6a

```text
candidate_sha=48c12c6660df7decb61f9aac4d8560526a8754eb
deployment_id=dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
base_url=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app
allowed_origin=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app
```

Both workflows require `VERCEL_AUTOMATION_BYPASS_SECRET`; its value must remain secret and must never be written to repository documentation.

## Evidence policy

Evidence is non-transferable across candidate SHA, deployment identity, workflow-trigger identity, or materially different control state. Historical P2/P6a artifacts remain historical even when the observed application behavior is compatible with the same predicate.

CI success, Vercel READY state, direct HTTP reachability, deterministic dry runs, and documentation reconciliation are not substitutes for a designated gate artifact unless the governing predicate explicitly says so.

## Current gate boundary

- P2: `OPEN / RERUN REQUIRED`
- P6a: `OPEN / RERUN REQUIRED`
- P3: current-cycle closure remains required where operational evidence is specified
- P4: `OPEN`
- P5: `OPEN`
- P6: `OPEN / FAIL-CLOSED`
- P7: formal exact binding remains open
- P8: `OPEN / FAIL-CLOSED`
- P9: fresh final independent closure remains required
- Freeze: `NOT ESTABLISHED`
- Authorization: `NOT GRANTED`
- Empirical N: `0`

## Closure sequence

`P2 + P6a exact workflow execution → operational P3/P4/P5/P6 closure → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`

No documentation-only change in this reconciliation establishes freeze, authorization, unblinding, or empirical execution.
