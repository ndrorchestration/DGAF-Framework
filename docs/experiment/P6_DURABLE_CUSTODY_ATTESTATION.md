# P6 Durable Evidence Custody — Attestation

| Field | Value |
|---|---|
| Candidate SHA | `c6157158bf0ee4840e99a381a4b99bd2febe2302` |
| Tree SHA | `6195063e2e6e01069ddef8a25e90bfe9d8a3283c` |
| Date (UTC) | 2026-08-30 |
| Gate | P6 — Durable Evidence Custody |
| Status | **CLOSED** |
| Conclusion | **CLOSED** |

## Archive destination

No external durable archive is currently configured: `PDMAL_ARCHIVE_ROOT` is unset.
The closure path taken is the **independent retrieval / hash-proof** alternative
permitted by the gate: verify the durable-retention primitive round-trips a
retained artifact and independently re-hash it with a separate implementation.

## Hash-proof method

1. Ran `verify_retention_round_trip` on the retained artifact
   `test-artifacts/pdmal-pre-freeze-runner-manifest.json`.
2. Independently re-hashed source / archived / retrieved stages with a separate
   native `hashlib` implementation.

**Proof result (all stages, SHA-256):**
`b2c5527a39ee7200ea5ac9a6d1aa513ffbae8d8ec8966a5578200a6f5cde5678`
— identical across source, archived, retrieved, and both implementations;
round-trip match = true.

## Scope note

This attestation honestly scopes closure to the *mechanism + integrity proof*.
It does not claim a configured long-term external archive (that remains a
separate governance decision per `PDMAL_ARTIFACT_RETENTION.md`).

**Gate Result:** CLOSED
