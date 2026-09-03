# P2 / P6a Dispatch Handoff — Exact Completion Candidate

**Status:** READY FOR DISPATCH / PRE-FREEZE / FAIL-CLOSED / N=0

This file supersedes the earlier contents of this dated handoff. Historical P2/P6a verification records remain evidence for their original candidate/deployment identities only and do not transfer to the current completion candidate.

## Exact candidate binding

- `candidate_sha`: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- `candidate_branch`: `candidate/p35-validated-control-state-2026-09-02`
- deployment branch: `deploy/exact-candidate-48c12c6`
- `deployment_id`: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url`: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestrration.vercel.app`
- `disallowed_origin`: `https://untrusted.com`

The deployment is READY/preview. Runtime paths are SSO-protected from the current unauthenticated session, so SSO redirects are not runtime-failure evidence. Vercel Git-SHA confirmation for the deployment remains pending.

## P2 dispatch contract

Workflow: `.github/workflows/p2-runtime-verification.yml`

Required inputs:

- `candidate_sha = 48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id = dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url = https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`

The workflow independently verifies the SHA format and requires `VERCEL_AUTOMATION_BYPASS_SECRET`. It then executes five cases against `/api/orchestrate` and writes candidate/deployment-bound provenance.

## P6a dispatch contract

Workflow: `.github/workflows/p6a-cors-verification.yml`

Required inputs:

- `candidate_sha = 48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id = dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url = https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `allowed_origin = https://dynamicgovernanceagenticformation-ndrorchestrration.vercel.app`

The workflow independently verifies the SHA/input presence and requires `VERCEL_AUTOMATION_BYPASS_SECRET`. It then executes allowed/disallowed POST and preflight checks and writes candidate/deployment-bound provenance.

## Current execution state

No fresh P2 or P6a runtime result is asserted here. The available GitHub integration exposes workflow inspection and rerun operations but no workflow-dispatch write operation. Therefore these workflows remain awaiting authenticated manual dispatch or another authorized dispatch path.

The earlier invalid P2 run is not evidence of runtime behavior because its supplied candidate/deployment/base-URL inputs were malformed and did not bind to the exact candidate.

## Evidence boundary

P2/P6a completion requires successful execution against the exact candidate and exact deployment above. No historical P2/P6a result transfers across candidate or deployment identity. These predicates do not establish efficacy, freeze, authorization, unblinding, or empirical execution.

## Downstream state

- P3: `VERIFIED` for the completion candidate
- P4: workflow-level evidence; operational closure open
- P5: workflow-level evidence; full closure open
- P6: workflow-level evidence; durable archive/retention closure open
- P7: technically adjudicated; formal adoption/exact freeze binding open
- P8: `OPEN / PRE-FREEZE / FAIL-CLOSED`
- P9: scoped pass for exact candidate; broader closure open
- Freeze: `NOT ESTABLISHED`
- Authorization: `NOT GRANTED`
- Empirical N: `0`

## Current closure sequence

`P2 + P6a exact runtime → operational P4/P5/P6 → P7 exact adoption/binding → P8 → final broader P9 → immutable freeze → explicit authorization → blinded pilot`.
