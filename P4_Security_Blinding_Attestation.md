# Custody Attestation Record: P4 Security / Blinding Gate

**Candidate SHA:** `c6157158bf0ee4840e99a381a4b99bd2febe2302`
**Date:** 2026-08-30
**Status:** VERIFIED

## 1. Operational Role Separation
The PDMAL pilot runner enforces a strict fail-closed security model based on the following operational roles:

| Role | Responsibility | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Orchestrator** | Pilot Execution & Data Collection | `run_pilot()` requires `PDMAL_PILOT_AUTHORIZED=1` and a valid `PDMAL_BLINDING_KEY` provided out-of-band. |
| **Auditor** | Artifact Validation | `validate_artifact()` ensures that the resulting JSON documents match the expected schema and that internal record SHAs are intact. |
| **Warden** | Durable Retention | `archive_artifact()` (in `durable_retention.py`) manages the immutable storage of artifacts and their retention manifests, bound to a `frozen_commit_sha`. |

**Verification:**
- Execution is prohibited without explicit authorization (`PDMAL_PILOT_AUTHORIZED`).
- The system rejects any attempt to run with a mismatched `PDMAL_FROZEN_COMMIT_SHA`.
- Durable retention is decoupled from the execution runner, requiring a configured `PDMAL_ARCHIVE_ROOT`.

## 2. Blinding Storage Integrity
Blinding is implemented using HMAC-SHA256 to ensure that condition labels are non-recoverable without the custody key.

**Implementation Details:**
- **Mechanism:** `blind_condition(condition, key)` uses `hmac.new(key.encode(), condition.encode(), hashlib.sha256)`.
- **Storage:** Blinded IDs are prefixed with `blind_` and truncated to 16 characters.
- **Integrity Checks:**
    - `test_blinding_outputs_are_distinct_and_do_not_expose_labels` verifies that outputs are distinct and do not leak cleartext labels.
    - `test_mock_unblinding_requires_the_custody_key` verifies that unblinding is impossible with an incorrect key.
    - `blinding_operational_test.py` validates that cleartext labels and keys never leak into the final blinded dataset.

**Verification:**
- The blinded mapping is not stored with the data; it is derived from the out-of-band key.
- The `run_pilot` runner explicitly pops `PDMAL_BLINDING_KEY` from the environment immediately after use to minimize exposure.

## 3. Conclusion
The operational role separation is effectively implemented and the blinding mechanism provides cryptographically sound isolation between the execution environment and the condition labels.

**Gate Result:** CLOSED
