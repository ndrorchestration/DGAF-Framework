# Candidate Runtime Dispatch Blocker — 2026-08-31

## Status

### Current gate status

PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Exact candidate runtime identity

- Candidate SHA: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- Candidate tree SHA: `0dfd39883c4ea8604ef2e72a98e9c2024557330f`
- Production deployment: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- Deployment URL: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`
- Deployment status: `READY`
- Deployment source SHA: `48c12c6660df7decb61f9aac4d8560526a8754eb`

## Blocking condition

The repository contains candidate-bound `workflow_dispatch` definitions for P2 and P6a. Their required runtime inputs are fully known and exact. The connected GitHub integration available to the orchestration agent does not expose a workflow-dispatch write action, so the workflows cannot be triggered from this interface.

This is an execution-plumbing limitation, not a missing candidate identity, deployment identity, URL, CORS origin, or constitutive contract.

## Required P2 inputs

- `candidate_sha`: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id`: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url`: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`

## Required P6a inputs

- `candidate_sha`: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id`: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url`: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Runtime observations already available

The exact deployment has shown the expected P6a request shape in Vercel runtime logs: two `POST /api/orchestrate` requests and two `OPTIONS /api/orchestrate` preflight requests. The observed responses were `503`, `503`, `204`, and `403`, respectively. These runtime observations do not constitute a current-candidate P6a workflow pass; the preserved P6a artifact remains historical because it is bound to a superseded candidate.

## Evidence non-transfer rule

Historical P2/P6a runs bound to superseded candidates remain historical and cannot be reused for the current candidate. In particular, prior P2/P6a artifacts for `92ff830b...` do not transfer to `48c12c...`.

## Closure condition

Close this blocker only when fresh P2 and P6a runs have executed against the exact candidate/deployment identity above and produced retained provenance artifacts.

No freeze, pilot authorization, unblinding, or empirical-N advancement follows from this record.
