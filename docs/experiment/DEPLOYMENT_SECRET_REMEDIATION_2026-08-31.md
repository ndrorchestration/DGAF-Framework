# Deployment Secret Remediation — 2026-08-31

## Status

PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

## Blocking prerequisites

Production deployment requires these GitHub Actions repository secrets:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

The deployment workflow checks for presence before attempting production deployment. Missing secrets intentionally result in `Deployment Evidence Unavailable`; this is not runtime verification.

## Operator remediation

Configure the three secrets in the repository's GitHub Actions secret store without exposing their values in source control, logs, comments, or evidence artifacts.

After configuration:

1. Run the production deployment workflow on the exact intended candidate commit.
2. Verify `READY`, `target=production`, and exact Vercel source-SHA equality.
3. Retain the deployment provenance artifact.
4. Only then run candidate-bound P2/P6a.

## Guardrail

Do not substitute a manually known Vercel URL or historical deployment identity for a missing authenticated deployment. The workflow must establish the deployment identity itself.
