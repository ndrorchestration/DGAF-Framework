# P6a CORS Verification

## Evidence boundary

P6a is a deployment-specific live CORS control. A historical P6a result remains valid only for the exact source/deployment/environment/origins tested. It does not automatically certify a later mainline candidate.

## Historical verified result

The retained P6a execution is verified for:

| Item | Historical value |
|---|---|
| Repository | `ndrorchestration/DGAF-Framework` |
| Deployment | `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7` |
| Deployed source | `e1f077fec746acd6066db689ef40db000e027f2f` |
| Workflow run | `32092041579` |
| Job | `95576028593` |
| Artifact | `p6a-cors-verification-e1f077f` (ID `9308650112`) |
| Artifact SHA-256 | `d9f21fd1202ac220d987fa7a0f15526fb3e874c8f889f39921669e983284d6eb` |

All four frozen assertions passed in that historical run: allowed POST, disallowed POST, allowed OPTIONS, and disallowed OPTIONS.

## Current candidate status

**NOT VERIFIED FOR CURRENT MAINLINE.**

A fresh P6a execution must target a deployment whose Vercel metadata exactly matches the candidate source SHA resolved from GitHub `main` at execution time. The historical `e1f077f` deployment and artifact are not substitutes for current-candidate evidence.

## Promotion rule

Current P6a may be promoted to **VERIFIED** only when a retained workflow run provides:

1. exact candidate source SHA;
2. exact deployment identity/URL;
3. all four HTTP assertions;
4. response-header evidence;
5. retained machine-readable artifact; and
6. artifact hash and provenance metadata.

P6a does not establish general application security, empirical DGAF/PDMAL efficacy, or pilot authorization.

## Historical boundary

The 2026-08-18 P6a evidence is preserved as historical evidence. Documentation reconciliation must not rewrite its source/deployment identity to a later candidate.
