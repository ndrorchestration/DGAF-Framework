# P2 / P6a Dispatch Handoff — Corrected Candidate

**Status:** BLOCKED UNTIL EXACT CURRENT DEPLOYMENT / PRE-FREEZE / FAIL-CLOSED / N=0

## Candidate binding

- `candidate_sha`: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- `candidate_tree_sha`: `973c92335caf84f37fc2b3c4df6dd83b3b855087`
- `deployment_id`: `NOT_ESTABLISHED`
- `base_url`: `NOT_ESTABLISHED`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

## Workflows

- P2: `.github/workflows/p2-runtime-verification.yml`
- P6a: `.github/workflows/p6a-cors-verification.yml`

Both workflows are `workflow_dispatch` only and require candidate-bound runtime inputs. No historical P2/P6a run may be reused for this corrected candidate cycle.

## Dispatch values

P2 and P6a **MUST NOT be dispatched yet**. The exact production deployment identity must first be established from the corrected apparatus source `2a54a67d…`, with authenticated workflow provenance and effective behavior-affecting runtime configuration attested.

Once established, dispatch inputs must use the exact returned deployment ID and URL and must satisfy source-SHA equality with `2a54a67d…`.

## Historical values explicitly retired from dispatch

The following values previously appeared in this handoff but belong to the invalidated pre-correction apparatus and are retained only as historical references:

- candidate: `d56b5b3c44e39ddb8c883259584432ab39259306`
- deployment: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`

They are **NOT valid dispatch inputs for the current cycle**.

## Closure requirement

P2 and P6a close only when fresh runs complete successfully against the exact corrected candidate/deployment identity and upload retained provenance artifacts. These runs do not authorize freeze or pilot execution.

## Boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
