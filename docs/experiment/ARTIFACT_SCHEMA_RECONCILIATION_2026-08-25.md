# Artifact Schema Reconciliation — 2026-08-25

**Status:** Pre-authorization blocker identified; no empirical execution authorized.

## Finding

The PDMAL apparatus contains two schema modules with the same `ARTIFACT_SCHEMA_VERSION = "1.0"` but different semantics:

- `experiments/pdmal_pilot/artifact_schema.py` — pre-freeze validation.
- `experiments/pdmal_pilot/pilot_artifact_schema.py` — authorized-pilot validation.

The distinction in lifecycle purpose is legitimate, but the shared version number and overlapping field/hash responsibilities create a risk of ambiguous schema authority.

## Concrete differences

### Pre-freeze schema

The pre-freeze validator requires `protocol_status = PRE-FREEZE` and `empirical_data_collection = false`. It validates record structure and SHA formatting but does not recompute the record's `artifact_sha256`. It also does not require `topology` or `failure_count` at the record level. 

### Pilot schema

The pilot validator requires `protocol_status = FROZEN`, `empirical_data_collection = true`, exactly 180 records, and a full `frozen_commit_sha`. It recomputes each record SHA using canonical JSON and requires additional fields including `topology` and `failure_count`.

### Runner

`run_pilot.py` imports the pilot schema directly and computes `artifact_sha256` using the same canonical JSON function before validation. This is directionally correct, but the pre-freeze and pilot modules remain separately authoritative for different lifecycle states while sharing the same schema version.

## Required remediation before pilot authorization

1. Establish a single canonical artifact contract with explicit lifecycle/profile semantics, or assign distinct schema/profile identifiers to pre-freeze and pilot artifacts.
2. Make the runner call the canonical validator inline before artifact acceptance.
3. Centralize canonical JSON serialization and SHA computation so no implementation duplicates the algorithm independently.
4. Add tests proving runner-generated hashes equal validator-recomputed hashes.
5. Add a contract test proving pre-freeze artifacts cannot be accepted as pilot artifacts and vice versa.
6. Bind the artifact contract/profile identifier to the protocol and candidate manifest.
7. Record the resulting schema/profile SHA in the eventual authoritative freeze.

## Authorization boundary

This finding does not authorize or execute PDMAL. It is an apparatus-hardening result.

Current state remains:

- PDMAL: PRE-FREEZE.
- Pilot authorization: NOT GRANTED.
- Empirical N: 0.
