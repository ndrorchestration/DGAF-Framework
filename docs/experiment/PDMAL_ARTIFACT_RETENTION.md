# PDMAL Artifact Retention and Integrity Policy

## Status

**PRE-FREEZE / CONFIGURATION RECORDED / DURABLE LONG-TERM RETENTION NOT YET VERIFIED**

This document records the artifact-retention configuration that is actually present in the PDMAL pre-freeze workflow. It does not claim that a separate durable research archive has been configured.

## Current verified storage

The PDMAL pre-freeze workflow stores its generated verification artifacts as GitHub Actions artifacts.

Current workflow configuration:

```text
Workflow: .github/workflows/pdmal-pre-freeze-runner.yml
Artifact path: test-artifacts/pre-freeze-runner-manifest.json
Retention: 30 days
Missing-file behavior: error
```

The workflow uses `if-no-files-found: error`, so a missing manifest prevents successful artifact publication.

## Integrity controls

Generated JSON artifacts use canonical JSON serialization for hashing where the schema module is applied. SHA-256 sidecars are generated for contract artifacts by the runner, and the machine-readable artifact schema validator requires a 64-character hexadecimal SHA-256 digest field.

The artifact schema is versioned with:

```text
schema_version = 1.0
```

Unsupported or missing schema versions fail validation.

## Long-term retention boundary

The currently verified GitHub Actions retention period is **30 days**. No claim is made here that one-year retention, external archival, Zenodo publication, secondary cloud backup, or another durable archive is already configured.

Before protocol freeze, the project must either:

1. formally adopt a longer retention requirement and configure an approved durable storage mechanism, or
2. explicitly determine that the existing 30-day Actions retention satisfies the adjudicated retention requirement.

That decision must be recorded as evidence before the artifact-retention freeze gate can be marked verified.

## Access control

Repository and workflow permissions govern access to GitHub Actions artifacts. This document does not extend access rights beyond the repository's configured permissions.

Any protected raw experimental dataset or blinding mapping must use a separately documented custody mechanism and must not be inferred from this workflow configuration.
