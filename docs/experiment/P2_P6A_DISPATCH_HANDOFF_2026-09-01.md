# P2 / P6a Dispatch Handoff — Verified Executable Candidate

**Status:** READY FOR DISPATCH / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

This handoff records the currently verified executable candidate/deployment pair. Historical P2/P6a records remain scoped to their original identities and do not transfer across candidate, deployment, or workflow-trigger identity.

## Exact executable candidate binding

- `candidate_sha`: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- `candidate_branch`: `candidate/p35-validated-control-state-2026-09-02`
- `deployment_id`: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url`: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `disallowed_origin`: `https://untrusted.com`
- deployment state: `READY`
- verified deployment Git SHA: `48c12c6660df7decb61f9aac4d8560526a8754eb`

Vercel independently reports the deployment as a Git deployment of the exact candidate SHA. The deployment is therefore valid for candidate-bound runtime execution.

## Later control-plane head

PR #200 subsequently advanced to control-plane/documentation commit `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`.

That later commit is **not** substituted for the executable candidate because no independently verified deployment is bound to that SHA. Its own dispatch-handoff revision preserves the `48c12c...` execution candidate/deployment pair.

## P2 dispatch contract

Workflow: `.github/workflows/p2-runtime-verification.yml`

Required inputs:

- `candidate_sha = 48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id = dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url = https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`

The workflow requires `VERCEL_AUTOMATION_BYPASS_SECRET`, executes the five required `/api/orchestrate` POST cases, and uploads a candidate/deployment-bound provenance artifact.

## P6a dispatch contract

Workflow: `.github/workflows/p6a-cors-verification.yml`

Required inputs:

- `candidate_sha = 48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id = dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url = https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `allowed_origin = https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`

The workflow requires `VERCEL_AUTOMATION_BYPASS_SECRET`, executes the four required CORS checks, and uploads a candidate/deployment-bound provenance artifact.

## Runtime observation already established

A live observation against this exact deployment exercised the four P6a request classes and matched the workflow predicates:

- allowed-origin POST: `503` with expected `Access-Control-Allow-Origin`;
- disallowed-origin POST: `503` without `Access-Control-Allow-Origin`;
- allowed-origin preflight: `204` with required origin/method/header allowances;
- disallowed-origin preflight: `403` without `Access-Control-Allow-Origin`.

This is deployment-scoped runtime observation only. It does not substitute for the designated exact-candidate workflow artifact.

## Current execution state

Fresh P2 and P6a workflow artifacts have **not** been produced for this exact candidate/deployment pair. The GitHub connection available to the execution operator exposes workflow inspection/rerun capabilities but not `workflow_dispatch` for these manual workflows.

No freeze, authorization, pilot execution, unblinding, or empirical N is established by this handoff.

## Evidence boundary

Do not reuse P2/P6a evidence from `92ff830b...`, `a43219b...`, `fc45d95e...`, or any earlier deployment. Closure requires the designated workflow execution itself to bind the exact candidate and exact deployment and preserve its resulting provenance artifact.

## Closure sequence

`P2 + P6a exact workflow execution → operational P3/P4/P5/P6 closure → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`.
