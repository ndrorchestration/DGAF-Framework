# P6a CORS Verification

## Status

**Gate: VERIFIED for designated deployment/source binding**

The live P6a CORS verification completed successfully. The retained GitHub Actions artifact demonstrates all four predeclared assertions against the designated immutable deployment and deployed application source.

## Current provenance

| Item | Value |
|---|---|
| Repository | `ndrorchestration/DGAF-Framework` |
| PR | `#65` |
| Current PR head at latest documentation sync | `c55476746126ca29f3963887c1c81ad6110c5738` |
| Verification workflow | `.github/workflows/p6a-cors-verification.yml` |
| Workflow commit containing P6a | `e94bfb5c` |
| Deployment under test | `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` |
| Deployed application source | `e1f077fec746acd6066db689ef40db000e027f2f` |
| Deployed URL | `https://dynamicgovernanceagenticformation-dp3baqm9p-ndrorchestration.vercel.app` |
| Allowed origin | `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app` |
| Disallowed origin | `https://untrusted.com` |
| P6a workflow run | `32092041579` |
| P6a job | `95576028593` |
| P6a artifact | `p6a-cors-verification-e1f077f` (ID `9308650112`) |
| Artifact SHA-256 | `d9f21fd1202ac220d987fa7a0f15526fb3e874c8f889f39921669e983284d6eb` |

## Evidence class boundary

The P6a artifact is explicitly scoped to the deployed application source `e1f077f` and immutable deployment `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7`. It establishes live CORS behavior for that endpoint, deployment, environment, and configured origins.

It does **not** certify the later PR head `c5547674` as a general source/CI state. Historical P0/P2/PDMAL evidence remains scoped to the exact source/deployment it tested. Current-head required checks and PR mergeability remain separate controls.

## Frozen P6a matrix and observed results

### 1. Allowed-origin POST

**Expected:** normal application status and `Access-Control-Allow-Origin` exactly matching the allowed origin.

**Observed:** HTTP `503`; `Access-Control-Allow-Origin` matched the allowed origin; **PASS**.

### 2. Disallowed-origin POST

**Expected:** normal application status; `Access-Control-Allow-Origin` absent.

**Observed:** HTTP `503`; `Access-Control-Allow-Origin` absent; **PASS**.

### 3. Allowed-origin OPTIONS preflight

**Expected:** HTTP `204` and required CORS headers.

**Observed:** HTTP `204`; `Access-Control-Allow-Origin` matched the allowed origin; `Access-Control-Allow-Methods` included `POST`; `Access-Control-Allow-Headers` included `Content-Type`; **PASS**.

Observed negotiated headers:

```text
Access-Control-Allow-Origin: https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app
Access-Control-Allow-Methods: GET,POST,OPTIONS
Access-Control-Allow-Headers: Content-Type,Authorization,X-AHG-Session,X-AHG-Turn
```

### 4. Disallowed-origin OPTIONS preflight

**Expected:** HTTP `403`; `Access-Control-Allow-Origin` absent.

**Observed:** HTTP `403`; `Access-Control-Allow-Origin` absent; **PASS**.

## Retained provenance artifact

GitHub Actions artifact:

`p6a-cors-verification-e1f077f` — artifact ID `9308650112`

The artifact contains machine-readable evidence with:

- evidence class `P6A_CORS_RUNTIME_EXECUTION`;
- `status: PASS`;
- source commit `e1f077fec746acd6066db689ef40db000e027f2f`;
- deployment URL and endpoint;
- all four case results;
- explicit epistemic boundary limiting the claim to the tested endpoint/deployment/environment/origins.

Artifact ZIP SHA-256:

`d9f21fd1202ac220d987fa7a0f15526fb3e874c8f889f39921669e983284d6eb`

## Workflow execution note

The workflow run itself reports the retained artifact against the designated immutable application source `e1f077f`. The workflow run's GitHub ref metadata is separate from the application source under test. This distinction is preserved rather than treating the workflow ref as application provenance.

## Promotion rule

P6a is promoted to **VERIFIED** for the designated immutable deployment/source binding because the retained run provides:

1. a run ID and completed job record;
2. all four HTTP cases;
3. response-header evidence for each case;
4. the retained `p6a-cors-verification.json` artifact; and
5. all four frozen assertions passing against the designated deployment/source binding.

The following remain separate and are not promoted by P6a:

- current PR-head CI verification;
- general application security hardening;
- production-wide CORS claims beyond the tested endpoint/configuration;
- empirical DGAF/PDMAL efficacy.

## 2026-08-18 verification update

P6a Live CORS Verification run `32092041579` completed successfully. Job `95576028593` completed successfully. Artifact `9308650112` was retained and independently inspected.

All four frozen assertions passed:

```text
Allowed POST       503 + matching ACAO       PASS
Disallowed POST    503 + ACAO absent        PASS
Allowed OPTIONS    204 + required headers   PASS
Disallowed OPTIONS 403 + ACAO absent        PASS
```

**P6a = VERIFIED for `e1f077f` / `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7`.**

The current PR head remains a separate provenance/required-check question and must be reassessed before merge.
