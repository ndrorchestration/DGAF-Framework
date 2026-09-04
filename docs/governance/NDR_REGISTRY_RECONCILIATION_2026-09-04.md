# NDR Registry Reconciliation — 2026-09-04

**Status:** Audit control / synchronization blocker
**Base:** `4ac8937f5b8f3358655a06ee7f9d8cd83b87106c`

## Observed state

The repository contains two materially different registry representations:

| Representation | Observed version | Watermark |
|---|---:|---|
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | 1.6 | P-41 |
| `docs/ndr_patterns_unified.json` | 2.4 | P-42 |

These claims cannot be treated as one release without explicit reconciliation.

## Target release identity

`registry_release_id + registry_version + registry_watermark + effective_timestamp + source_commit + schema_version + content_digest + authoritative_status + companion_paths`

Human- and machine-readable representations should be generated from one source or deterministically compared before release.

## Synchronization rules

1. Version, watermark, schema, or digest mismatch is **DRIFT**.
2. DRIFT prevents promotion of either representation as sole current executable authority.
3. Historical content remains preserved.
4. Synchronization must not silently import later P-series content.
5. A green drift check does not validate semantic correctness.
6. Release identity binds to an immutable source commit.

## Validation requirements

Compare version, watermark/highest P-series ID, pattern counts, schema, IDs/names, status/classification, and explicit changelog identity. Intentional divergence requires an explicit exception with owner/expiry.

## Current disposition

The Markdown/JSON divergence is a synchronization gap, not evidence that either representation is semantically correct. No silent normalization is permitted.

## Boundary

This control artifact does not alter apparatus, freeze, candidate identity, authorization, or empirical N.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
