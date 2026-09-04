# NDR Registry Reconciliation — 2026-09-04

**Status:** Audit control / synchronization blocker
**Base:** `4ac8937f5b8f3358655a06ee7f9d8cd83b87106c`

## Observed state

The repository contains two materially different registry representations:

| Representation | Observed version | Watermark | Notable state |
|---|---:|---:|---|
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | 1.6 | P-41 | Human-readable registry; declares itself canonical |
| `docs/ndr_patterns_unified.json` | 2.4 | P-42 | Machine-readable registry; includes P-42 and 2026-07-03 metadata |

The JSON counterpart also declares `schema v2.4`, while the Markdown document identifies the machine-readable counterpart as schema v2.1 with P-37→P-41 pending synchronization. These claims cannot all be true simultaneously.

## Best-practice target

Treat a registry release as a versioned artifact with a single release identity. The release identity should bind:

```text
registry_release_id
registry_version
registry_watermark
effective_timestamp
source_commit
schema_version
content_digest
authoritative_status
companion_paths
```

The human-readable and machine-readable representations should either be generated from the same source or be deterministically compared before release.

## Synchronization rules

1. A mismatch in version, watermark, schema, or digest is a **DRIFT** state.
2. DRIFT prevents promotion of either representation as the sole current executable authority.
3. Existing historical content must remain preserved.
4. Synchronization must not silently import a later P-series entry into the earlier representation.
5. A successful drift check does not itself validate the semantics of any pattern.
6. The registry release identity must be bound to a source commit, not merely a mutable tag.

## Validation requirements

A deterministic validator should compare at minimum:

- version;
- watermark / highest P-series ID;
- total pattern count;
- named session pattern count;
- formation pattern count;
- schema version;
- pattern IDs and names;
- status/classification fields;
- explicit changelog release identity.

Where the representations intentionally differ, the validator should require an explicit exception record with an expiry/owner rather than passing silently.

## Current disposition

The observed Markdown/JSON divergence is a **synchronization gap**. It is not evidence that either representation is semantically correct. The existing P-42 JSON entry should remain provenance-bound, and the Markdown registry should not be rewritten merely to make counts match until its authority is confirmed.

## Provenance principle

SLSA provenance guidance supports making the origin and production context of artifacts verifiable. For DGAF registry releases, that means the release identity should be tied to an immutable source commit plus content digest rather than inferred from a mutable version label alone.

## Scientific boundary

This control artifact does not alter experimental apparatus, freeze state, candidate identity, or authorization.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
