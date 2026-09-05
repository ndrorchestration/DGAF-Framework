# PDMAL Deployment Identity Verification — 2026-09-05

**Status:** CURRENT-CANDIDATE IDENTITY EVIDENCE  
**Scope:** P1 deployment/candidate identity only  
**Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Purpose

Retain the independent live retrieval of the deployment identity referenced by the current PDMAL candidate records. This record establishes deployment-to-candidate identity; it does not substitute for P2 runtime-matrix evidence, P6a CORS evidence, P4 human custody separation, analysis lock, freeze, authorization, or empirical execution.

## Verified identity tuple

| Field | Verified value |
|---|---|
| Vercel deployment ID | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` |
| Deployment name | `dynamicgovernanceagenticformation` |
| Vercel project ID | `prj_euzjAnhqct0wayTWWojizanKN3cX` |
| Deployment state | `READY` |
| Deployment target | `production` |
| Deployment source | `git` |
| GitHub repository | `ndrorchestration/DGAF-Framework` |
| Git ref | `main` |
| Git commit SHA | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` |
| Git commit verification | `verified` |
| Runtime candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` |
| Corrected apparatus source | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` |
| Vercel team | `ndrorchestration` |
| Vercel team ID | `team_TJWNcGa1Xh9ARKF3SYbKKxKp` |
| Region | `iad1` |

## Retrieval event

On 2026-09-05 UTC, the Vercel deployment API was queried directly for deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` under team `team_TJWNcGa1Xh9ARKF3SYbKKxKp`. The response reported the deployment as `READY`, target `production`, source `git`, and identified GitHub commit `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` from `ndrorchestration/DGAF-Framework` on `main`.

This independently confirms that the recorded deployment identity resolves live and is source-bound to the designated runtime candidate.

## P1 interpretation

The deployment portion of P1 Candidate Integrity is **VERIFIED** for the exact tuple above. Candidate/tree and apparatus provenance remain governed by the designated-candidate manifest and the self-bound evidence registry. Formal P1 status is reconciled only in the canonical control-state surface.

## Explicit non-claims

This verification does **not** claim that:

- the historical P2 Actions artifact is freshly retrieved;
- the authenticated P2 five-case runtime matrix has been freshly re-executed;
- the historical P6a Actions artifact is freshly retrieved;
- the authenticated four-case CORS matrix has been freshly re-executed;
- P4 human/key custody separation is established;
- P7/P8/P9 are complete;
- an immutable freeze exists;
- pilot authorization has been granted;
- any empirical pilot observation exists.

**Empirical N remains `0`.**
