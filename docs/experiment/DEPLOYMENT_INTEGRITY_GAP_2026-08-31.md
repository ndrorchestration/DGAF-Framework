# Deployment Integrity Gap — 2026-08-31

## Status

PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

## Current apparatus

- Corrected apparatus boundary: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Current main tip is later and contains governance/control-only reconciliation commits.
- A fresh execution candidate has **not** been designated.

## Verified deployment prerequisites

`.github/workflows/deploy.yml` requires all three GitHub Actions secrets before production deployment:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

When any is absent, the workflow intentionally skips production deployment and records `DEPLOYMENT_CONFIGURATION_STATUS` rather than fabricating runtime evidence.

## Newly identified pre-freeze integrity issue

The production deployment workflow currently performs two mutable environment writes after the Vercel production deployment step:

- `ENSEMBLE_VERSION=1.8.0`
- `PSI_CHECK=enabled`

Those values can affect runtime/build behavior but are not presently represented as explicit candidate-identity fields in the canonical control state. Therefore source-SHA equality alone is insufficient to establish a fully bound runtime configuration.

## Required disposition

Before a fresh candidate is frozen or any candidate-bound live verification is accepted, one of the following must be completed:

1. Make these environment settings immutable, preconfigured, and explicitly bound in the candidate manifest; or
2. Move the settings into the source-controlled configuration used to build the candidate; or
3. Extend deployment provenance to attest the effective environment configuration using non-secret identifiers/hashes and verify it before runtime evidence is accepted.

The actual secret values must never be recorded in repository documentation or evidence artifacts.

## Non-transferability

Historical deployment IDs, URLs, P2/P6a results, or runtime evidence remain non-transferable across this unresolved deployment-integrity boundary.

## Closure predicate

This gap is closed only when the effective production configuration is mechanically bound to the fresh candidate identity and the deployment workflow proves that binding before P2/P6a runtime evidence is accepted.
