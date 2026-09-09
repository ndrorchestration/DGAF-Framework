# Live Staging Breaker Evidence Contract

## Purpose

This contract governs Issue #518: one controlled circuit-breaker exercise on an exact-source-bound disposable Vercel preview deployment.

It upgrades the historical repository-local breaker harness into deployed-runtime structural evidence. It does **not** establish scientific efficacy, production reliability, or High-Assurance acceptance.

## Runtime surface

The exercise endpoint is `/api/staging-breaker` and is deliberately unavailable unless all of the following hold:

- `VERCEL_ENV == preview`;
- `DGAF_STAGING_BREAKER_EXERCISE_ENABLED == true`;
- the request carries the exact run-bound `x-dgaf-staging-exercise-id` expected by that preview deployment.

Production requests must receive `404 NOT_AVAILABLE`. The normal production deployment workflow carries a negative control for this property.

## Fixed exercise

The endpoint does not accept a caller-selected breaker threshold or fault severity.

The declared structural exercise is:

- breaker threshold: `0.80`;
- controlled synthetic fault score: `0.95`;
- required sequence: `STAGING -> ACTIVE -> BREAKER_OPEN -> FROZEN -> ROLLBACK -> VERIFIED`.

The fault contains no empirical observation, protected mapping, custody material, model output, or scientific outcome.

## Exact-source binding

The PR workflow:

1. checks out the exact PR head;
2. creates a single-run exercise identity from workflow run, attempt, and source SHA;
3. deploys that exact source to a Vercel preview;
4. retrieves Vercel deployment metadata;
5. requires `READY`, a non-production target, a concrete deployment ID, and exact source SHA equality;
6. exercises the deployed endpoint once for that run attempt;
7. requires the complete declared transition sequence;
8. verifies `/api/health` after rollback;
9. emits an attempt-bound evidence document plus SHA-256 sidecar.

A later rerun is a different attempt and must retain its own evidence. A failed attempt is not erased by a later successful attempt.

## Evidence class

A successful exercise is classified only as:

`PASS_STRUCTURAL_LIVE_STAGING_ONLY`

It establishes that the reviewed preview-only runtime path executed the declared fixed breaker transition sequence on an exact-source-bound Vercel preview and that the same deployment passed the post-rollback health check.

## Explicit limitations

This apparatus does not prove:

- persistent distributed breaker state across serverless instances;
- a production breaker event;
- production rollback;
- Sentinel -> AOGA integration;
- Track A custody or unblinding;
- primary-analysis authorization or execution;
- DGAF efficacy;
- AHG efficacy;
- model robustness;
- High-Assurance acceptance.

The staging endpoint is intentionally isolated from `/api/orchestrate`. The current production orchestrator still fails closed at Phi-Closure checkpoints because live audit state is not wired into that route. This exercise therefore establishes only a deployed preview structural sequence if its retained evidence passes review; it does not establish a persistent production breaker implementation and does not by itself close any stronger runtime-control claim.

## Scientific boundary

Every endpoint/workflow evidence record fixes:

- `protected_or_empirical_material_used = false`;
- `scientific_state_effect = NONE`;
- `primary_analysis_authorized = false`;
- `canonical_dgaf_efficacy = NOT_ESTABLISHED`;
- `high_assurance_authorized = false`.
