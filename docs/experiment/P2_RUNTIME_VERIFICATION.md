# P2 Runtime Verification

## Evidence boundary

This document defines the P2 live-runtime verification contract. It is **not** itself current verification evidence. A P2 result becomes current only when the corrected matrix executes successfully against an application deployment whose metadata exactly matches the candidate source SHA.

## Historical execution record

The first authenticated P2 execution tested the historical deployment:

- Application source: `e1f077fec746acd6066db689ef40db000e027f2f`
- Vercel deployment: `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7`
- Endpoint: `/api/orchestrate`
- Historical workflow run: `32089025430`

That execution exposed three matrix/fixture mismatches and established that the authenticated CI path could reach the historical deployment. It did **not** establish P2 verification. The historical result remains bounded to its original source/deployment.

## Current execution status

**NOT VERIFIED FOR CURRENT MAINLINE.**

The corrected P2 contract and execution controls are present in the repository, but a fresh candidate-scoped runtime run with retained evidence has not yet been completed.

The current candidate must be resolved from GitHub `main` at execution time. Do not substitute the historical `e1f077f` deployment or its retained run/artifacts.

## Runtime contract

The deployed endpoint requires `turn >= 1`. Phi-Closure checkpoints are Fibonacci turns `13`, `21`, `34`, and `55`; when live audit state is unavailable at a checkpoint, the endpoint must fail closed with `503 / BLOCKED`.

An arbitrary JSON object is not an invalid body shape because omitted fields default to supported values. The invalid-shape case uses a JSON array.

Malformed JSON is rejected with HTTP 400 and the current endpoint returns the plain body `Invalid JSON` without a `decision` field.

## Corrected P2 cases

| Case | Request | Expected HTTP | Expected decision |
|---|---|---:|---|
| Valid request with audit state unavailable | `{"mandate":"P2 live verification","turn":13}` | 503 | BLOCKED |
| Invalid body shape | `[]` | 400 | REJECT |
| Confidence out of range | `{"mandate":"P2 live verification","confidence":2.0}` | 400 | REJECT |
| Invalid turn | `{"mandate":"P2 live verification","turn":-1}` | 400 | REJECT |
| Malformed JSON | `{` | 400 | None; body `Invalid JSON` |

## Promotion rule

P2 may be promoted to **VERIFIED** only when all five corrected cases pass against the exact application commit under test, in a documented execution environment, with retained machine-readable evidence containing the candidate SHA and deployment identity.

P2 verification does not establish broad DGAF efficacy, comparative superiority, or empirical PDMAL validity.

## Historical provenance rule

The retained historical P2 execution must remain available for provenance and regression analysis. It must never be copied into a current candidate evidence packet merely because the endpoint or test matrix has not materially changed.
