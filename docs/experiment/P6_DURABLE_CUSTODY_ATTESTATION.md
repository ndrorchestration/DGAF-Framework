# P6 Durable Evidence Custody — Historical Attestation

> **SUPERSEDED FOR CURRENT CANDIDATE USE.** This attestation records a prior P6 mechanism/integrity proof. It must not be used as current P6 closure evidence for the 2026-09-01 completion candidate.

| Field | Value |
|---|---|
| Historical Candidate SHA | `c6157158bf0ee4840e99a381a4b99bd2febe2302` |
| Historical Tree SHA | `6195063e2e6e01069ddef8a25e90bfe9d8a3283c` |
| Date (UTC) | 2026-08-30 |
| Historical Gate | P6 — Durable Evidence Custody |
| Historical Status | **CLOSED within recorded historical scope** |
| Current-candidate status | **DO NOT TRANSFER** |

## Historical archive scope

No external durable archive was configured in the historical run: `PDMAL_ARCHIVE_ROOT` was unset. The historical closure path used the independent retrieval / hash-proof alternative permitted by that gate: verify that the retention primitive round-tripped a retained artifact and independently re-hash it with a separate implementation.

## Historical hash proof

The historical proof covered `test-artifacts/pdmal-pre-freeze-runner-manifest.json` and reported SHA-256 equality across source, archived, and retrieved stages, with an independently implemented `hashlib` re-hash:

`b2c5527a39ee7200ea5ac9a6d1aa513ffbae8d8ec8966a5578200a6f5cde5678`

Round-trip match was reported as true.

## Current-candidate boundary

The current controlled completion candidate is `a43219b4ed91fff8615f6c655ab3d17ca871fc29`. The historical P6 result above does not establish P6 closure for that candidate because candidate identity is part of the evidence scope.

Current P6 remains subject to the active P4/P5/P6 checklist and current-candidate evidence chain, including the required durable retention/retrieval proof bound to the current candidate.

**Current Gate Result:** OPEN / FAIL-CLOSED until current-candidate requirements are satisfied.
