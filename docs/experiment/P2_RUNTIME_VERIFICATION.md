# P2 Runtime Verification

## Purpose

This record defines the evidence boundary for live end-to-end verification of `/api/orchestrate`.

## Target

- Commit under test: `3159a99184138fe753acc924c687a1cf9b2a7554` (current PR #65 head)
- Endpoint: `/api/orchestrate`
- Required environment: controlled staging or Vercel deployment built from the exact commit under test
- Runner: `scripts/p2_runtime_matrix.py`

## Predeclared cases

| Case | Expected HTTP | Expected decision |
|---|---:|---|
| Valid request with audit state unavailable | 503 | BLOCKED |
| Invalid body shape | 400 | REJECT |
| Confidence out of range | 400 | REJECT |
| Invalid turn | 400 | REJECT |
| Malformed JSON | 400 | REJECT |

## Evidence requirements

Each execution must record:

- exact base URL
- exact commit SHA running in the environment
- environment type
- UTC timestamps
- exact request payload or raw body
- actual HTTP status
- actual response body
- `decision`
- `evidence.status`
- trace when present

## Current status

**BLOCKED / NOT VERIFIED.**

The current repository head has source-level and CI evidence for the fail-closed orchestrator behavior, but no direct live execution evidence for the exact current head is available yet. The latest READY Vercel deployment observed during this gate was built from an earlier commit and is therefore not valid current-head P2 evidence.

A successful historical deployment may be used for diagnostic comparison only and must not promote P2.

## Promotion rule

P2 may be promoted to **VERIFIED** only when all five predeclared cases pass against the exact commit under test in a documented execution environment.

P2 verification does not establish broad DGAF efficacy, comparative superiority, or empirical PDMAL validity.
