# P6a CORS Verification

## Status

**Gate: NOT VERIFIED**

This document records the current evidence boundary for live CORS verification of PR #65. The gate is intentionally not promoted until a retained GitHub Actions execution artifact demonstrates all four predeclared assertions against the designated immutable deployment.

## Current provenance

| Item | Value |
|---|---|
| Repository | `ndrorchestration/DGAF-Framework` |
| PR | `#65` |
| Current PR head | `e94bfb5c2ae01ce21642fee5b01d88db620b2878` |
| Verification workflow | `.github/workflows/p6a-cors-verification.yml` |
| Workflow commit containing P6a | `e94bfb5c` |
| Deployment under test | `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` |
| Deployed application source | `e1f077fec746acd6066db689ef40db000e027f2f` |
| Deployed URL | `https://dynamicgovernanceagenticformation-dp3baqm9p-ndrorchestration.vercel.app` |
| Allowed origin | `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app` |
| Disallowed origin | `https://untrusted.com` |

## Evidence class boundary

The following evidence is already retained but remains scoped to the deployed application source `e1f077f` and is not silently promoted to the later PR head `e94bfb5c`:

- Python Tests & Quality Checks: GitHub Actions run `32088344498` — success.
- PDMAL instrumentation dry run: GitHub Actions run `32088344456` — success.
- P2 live runtime verification: GitHub Actions run `32090160638`, artifact `9308051857` — success for deployment/source `e1f077f`.

The current PR head is seven commits ahead of `e1f077f`. The difference includes the P6a and P2 verification workflows plus related P2 documentation/runner changes. The historical evidence therefore does not close the current-head provenance gap by itself.

## Frozen P6a matrix

### 1. Allowed-origin POST

**Request:** `POST` with `Origin: <allowed>`.

**Expected:** normal application status (`200`, `400`, or `503` depending on request/application state) and `Access-Control-Allow-Origin` exactly matching the allowed origin.

### 2. Disallowed-origin POST

**Request:** `POST` with `Origin: <untrusted>`.

**Expected:** normal application status; `Access-Control-Allow-Origin` is absent. The server may execute the application request; browser enforcement prevents a disallowed origin from reading the response.

### 3. Allowed-origin OPTIONS preflight

**Request:** `OPTIONS` with the allowed origin and preflight headers.

**Expected:** HTTP `204` and the required CORS headers, including the allowed origin.

### 4. Disallowed-origin OPTIONS preflight

**Request:** `OPTIONS` with the untrusted origin and preflight headers.

**Expected:** HTTP `403` and no `Access-Control-Allow-Origin` header.

## Execution requirement

The workflow supports `workflow_dispatch`, `push`, and `pull_request`. A manual `workflow_dispatch` on `epistemic/evidence-architecture-v1` is the planned execution mechanism when a repository maintainer needs to produce the retained run record.

The currently exposed GitHub connector does not provide a workflow-dispatch mutation or repository-wide workflow-run enumeration. An empty result from the PR-only run query is therefore an observational limitation, not evidence that no dispatch run exists.

No synthetic commit or artificial branch movement should be created solely to manufacture a workflow event.

## Promotion rule

P6a may be promoted to **VERIFIED** only when a retained GitHub Actions run provides:

1. a run ID and job execution record;
2. the four HTTP cases above;
3. response header evidence for each case;
4. a retained `p6a-cors-verification.json` artifact; and
5. all four frozen assertions passing against the designated deployment/source binding.

Until then:

```text
P6a = NOT VERIFIED
```

## Current next action

Trigger `P6a Live CORS Verification` manually from GitHub Actions on branch `epistemic/evidence-architecture-v1`. After the run exists, inspect the job logs and provenance artifact before changing the gate.

## 2026-08-18 evidence update

Current GitHub inspection confirms PR #65 is open with head `e94bfb5c2ae01ce21642fee5b01d88db620b2878`. Vercel deployment `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` is READY and bound to source `e1f077fec746acd6066db689ef40db000e027f2f`. No P6a provenance artifact has been observed through the currently exposed connector surface.

This record deliberately distinguishes source/CI verification, deployment evidence, runtime evidence, and live CORS header evidence. No higher evidence class is inferred from an adjacent lower class.
