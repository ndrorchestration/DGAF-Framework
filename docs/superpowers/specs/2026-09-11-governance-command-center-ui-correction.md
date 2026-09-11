# DGAF Governance Command Center UI/UX Design Correction

**Date:** 2026-09-11  
**Applies to:** `docs/superpowers/specs/2026-09-11-governance-command-center-ui-design.md`  
**Scientific-state effect:** NONE  
**Authority effect:** NONE

## Corrected runtime integration finding

The approved design correctly requires verification and normalization of the live dashboard transport, but its initial current-state note incorrectly inferred that the dashboard endpoints were absent because they are not under `app/api/`.

The repository is intentionally hybrid. The live dashboard endpoints exist under the Next.js Pages Router:

- `pages/api/health.ts`
- `pages/api/audit.ts`
- `pages/api/roster.ts`
- `pages/api/sweep.ts`

`pages/api/health.ts` explicitly documents that the Pages Router API takes precedence over `app/api` in the current hybrid mode.

## Implementation consequence

The redesign MUST preserve and consume the existing `/api/health`, `/api/audit`, `/api/roster`, and `/api/sweep` routes through a validated frontend adapter layer. It MUST NOT create duplicate App Router API routes unless later evidence shows a concrete transport defect that cannot be fixed safely in the existing route.

The frontend adapter must still validate response shapes, model malformed/unavailable/stale states, preserve the last valid snapshot during polling failures, and never infer governance or scientific state from runtime health.

## Additional observed contract notes

- `/api/audit` is explicitly in-memory and resets on serverless cold start; the UI must surface that limitation rather than presenting those counters as durable governance evidence.
- `/api/sweep` is non-mutating and returns `harmonic_score: null` with `harmonic_score_status: NOT_COMPUTED`; the UI must not fabricate or visually imply a computed score.
- `/api/roster` returns a runtime roster snapshot. Public-facing functional labels should be layered on the returned identities using the repository translation authority rather than rewriting the API payload into stronger identity claims.

This correction supersedes only the inaccurate API-location inference in the original design. All other approved design requirements remain unchanged.
