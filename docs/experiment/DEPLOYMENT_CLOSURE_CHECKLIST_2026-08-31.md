# Deployment Closure Checklist — 2026-08-31

## Current boundary

PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0

## Exact apparatus boundary

`2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`

Documentation-only commits after this SHA do not change the apparatus source.

## Closure predicates

- [ ] Configure `VERCEL_TOKEN` in GitHub Actions secrets.
- [ ] Configure `VERCEL_ORG_ID` in GitHub Actions secrets.
- [ ] Configure `VERCEL_PROJECT_ID` in GitHub Actions secrets.
- [ ] Produce a READY production deployment from the exact intended candidate SHA.
- [ ] Verify Vercel source SHA equals the candidate SHA.
- [ ] Capture deployment ID and URL in retained provenance evidence.
- [ ] Attest effective behavior-affecting environment configuration, including `ENSEMBLE_VERSION=1.8.0` and `PSI_CHECK=enabled`, without recording secret values.
- [ ] Execute fresh candidate-bound P2.
- [ ] Execute fresh candidate-bound P6a with the exact allowed origin.
- [ ] Rebuild downstream P3–P9 evidence from the fresh candidate boundary.
- [ ] Create an immutable freeze manifest only after all core predicates pass.
- [ ] Obtain explicit experiment authorization before N may advance.

## Fail-closed rules

A missing secret, deployment identity mismatch, effective-environment mismatch, stale candidate reference, missing retained artifact, blinding failure, null contamination, or independent-verification failure blocks progression.

Historical deployment evidence is not reusable merely because the current source is lineage-related.
