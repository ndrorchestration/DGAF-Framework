# P2 Runtime Verification

## Purpose

This record defines the evidence boundary for live end-to-end verification of `/api/orchestrate`.

## Deployment under test

- Application source commit deployed: `e1f077fec746acd6066db689ef40db000e027f2f`
- Vercel deployment: `dpl_8YCHnqd4ZLGXnk9U2CuAJozUYLZ7`
- Endpoint: `/api/orchestrate`
- Verification runner: GitHub Actions `P2 Live Runtime Verification`

## Runtime contract derived from source

The deployed endpoint requires `turn >= 1`. Phi-Closure checkpoints are Fibonacci turns `13`, `21`, `34`, and `55`; when live audit state is unavailable at a checkpoint, the endpoint must fail closed with `503 / BLOCKED`.

An arbitrary JSON object is not an invalid body shape by itself because omitted fields default to supported values. The invalid-shape case therefore uses a JSON array.

Malformed JSON is rejected with HTTP 400 and the current endpoint returns the plain body `Invalid JSON` without a `decision` field.

## P2 cases

| Case | Request | Expected HTTP | Expected decision |
|---|---|---:|---|
| Valid request with audit state unavailable | `{"mandate":"P2 live verification","turn":13}` | 503 | BLOCKED |
| Invalid body shape | `[]` | 400 | REJECT |
| Confidence out of range | `{"mandate":"P2 live verification","confidence":2.0}` | 400 | REJECT |
| Invalid turn | `{"mandate":"P2 live verification","turn":-1}` | 400 | REJECT |
| Malformed JSON | `{` | 400 | None; body `Invalid JSON` |

## First live execution result

GitHub Actions run `32089025430` successfully injected the Vercel automation-bypass secret and reached the deployed application. This establishes that deployment protection was bypassed for CI; it does not by itself establish P2.

Observed on the first authenticated run:

- Valid + `turn: 0`: `400 / REJECT` because the runtime contract requires a positive turn. This exposed an outdated matrix fixture, not an application defect.
- `{"foo":"bar"}`: `200 / PASS` with `evidence.status=PARTIAL`. This is valid according to the source because arbitrary JSON objects are accepted and omitted fields use defaults. This exposed an incorrect "invalid body shape" fixture.
- Confidence `2.0`: `400 / REJECT` — PASS against the declared validation rule.
- Turn `-1`: `400 / REJECT` — PASS against the declared validation rule.
- Malformed JSON: `400`, body `Invalid JSON`, no `decision` field. The HTTP behavior is correct; the former verifier incorrectly required `decision=REJECT` for this transport-level parse failure.

**Disposition: NOT VERIFIED.** The live execution path is now proven, but the original P2 matrix contained three specification/fixture mismatches. The matrix and runner have been corrected in follow-up commits; the pinned deployed source remains `e1f077fec...` until a new application deployment is intentionally created.

## Promotion rule

P2 may be promoted to **VERIFIED** only when all five corrected cases pass against the exact application commit under test in a documented execution environment.

P2 verification does not establish broad DGAF efficacy, comparative superiority, or empirical PDMAL validity.
