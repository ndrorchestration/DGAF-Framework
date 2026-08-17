# PDMAL Instrumentation Pre-Flight

## Gate

The 50-seed pilot is prohibited until the instrumentation dry run completes successfully.

## Required environment secret

`PDMAL_BLINDING_KEY` must exist as a GitHub Actions repository secret and contain at least 32 characters. The workflow maps it into the job environment but never prints its value. Missing/short secrets cause a fail-closed exit before data generation.

## Dry-run acceptance criteria

- Determinism: identical canonical JSON bytes and SHA-256 for the repeated one-seed case.
- Structural invariants: ring and dodecahedral graph properties match the frozen specification; PDMAL has 30 edges, connectivity 3, diameter 5.
- Post-failure semantics: component metrics are computed from the post-failure graph and use the frozen original-population denominator.
- CSV schema: required fields exist; no required metric column is entirely null or constant for the dry-run fixture.
- Artifact persistence: CSV and `.sha256` sidecar exist and the computed digest matches.
- Artifact upload: GitHub Actions artifact is uploaded with `if-no-files-found: error`.
- One-seed execution: all five topology families execute for the smoke case.

## Evidence rule

A failed dry run is retained as evidence of the failure mode and guardrail behavior. It is not converted into a pass by altering the gate unless the underlying implementation defect is fixed and the failed run remains in the history.

## Current blocker

As of 2026-08-17, the latest dry run failed closed because the `PDMAL_BLINDING_KEY` secret was absent. No unblinded pilot data were generated.

## Secret configuration

Repository owner action is required:

1. Generate a high-entropy secret locally.
2. Add repository secret `PDMAL_BLINDING_KEY` under GitHub Actions secrets.
3. Do not commit, echo, paste into issues, or expose the value in logs.
4. Re-run the PDMAL Instrumentation Dry Run.

The connector used for repository orchestration does not expose repository-secret administration, so secret presence/value cannot be set or inspected programmatically here.
