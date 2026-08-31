# P2 / P6a Dispatch Handoff — Current Candidate

**Status:** READY FOR FRESH RUNTIME VERIFICATION / PRE-FREEZE / FAIL-CLOSED / N=0

## Exact inputs

- `candidate_sha`: `d56b5b3c44e39ddb8c883259584432ab39259306`
- `deployment_id`: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- `base_url`: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Workflows

- P2: `.github/workflows/p2-runtime-verification.yml`
- P6a: `.github/workflows/p6a-cors-verification.yml`

Both workflows are `workflow_dispatch` only and require the inputs above. No historical P2/P6a run may be reused for this candidate.

## P2 dispatch values

```text
candidate_sha=d56b5b3c44e39ddb8c883259584432ab39259306
deployment_id=dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
base_url=https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
```

## P6a dispatch values

```text
candidate_sha=d56b5b3c44e39ddb8c883259584432ab39259306
deployment_id=dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb
base_url=https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app
allowed_origin=https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
```

## Closure requirement

P2 and P6a close only when fresh runs complete successfully against the exact candidate/deployment identity and upload retained provenance artifacts. These runs do not authorize freeze or pilot execution.
