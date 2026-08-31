# Candidate Runtime Dispatch Blocker — 2026-08-31

## Status

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**

## Exact candidate runtime identity

- Apparatus source: `d56b5b3c44e39ddb8c883259584432ab39259306`
- Production deployment: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- Deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- Allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Blocking condition

The repository contains candidate-bound `workflow_dispatch` definitions for P2 and P6a. Their required runtime inputs are fully known and exact. The connected GitHub integration available to the orchestration agent does not expose a workflow-dispatch write action, so the workflows cannot be triggered from this interface.

This is an execution-plumbing limitation, not a missing candidate identity, deployment identity, URL, CORS origin, or constitutive contract.

## Required P2 inputs

- `candidate_sha`: `d56b5b3c44e39ddb8c883259584432ab39259306`
- `deployment_id`: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- `base_url`: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`

## Required P6a inputs

- `candidate_sha`: `d56b5b3c44e39ddb8c883259584432ab39259306`
- `deployment_id`: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- `base_url`: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Evidence non-transfer rule

Historical P2/P6a runs, including the successful P6a run bound to `303f4424...`, remain historical and cannot be reused for the current candidate.

## Closure condition

Close this blocker only when fresh P2 and P6a runs have executed against the exact candidate/deployment identity above and produced retained provenance artifacts.

No freeze, pilot authorization, unblinding, or empirical-N advancement follows from this record.
