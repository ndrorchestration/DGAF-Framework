# Historical Custody Attestation Record: P4 Security / Blinding Gate

**Historical Candidate SHA:** `c6157158bf0ee4840e99a381a4b99bd2febe2302`  
**Date:** 2026-08-30  
**Status:** HISTORICAL / SUPERSEDED FOR CURRENT COMPLETION CYCLE

This record documents a prior P4 verification. It is retained for provenance only and is **not** current P4 closure evidence for PR #199 or validated P-35 candidate `0b1190fe91db6b963da0b31492d61fa1a34381e3`.

## 1. Historical operational role separation

The prior verification covered the PDMAL pilot runner's fail-closed security model and operational separation:

| Role | Responsibility | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Orchestrator** | Pilot Execution & Data Collection | `run_pilot()` requires `PDMAL_PILOT_AUTHORIZED=1` and a valid `PDMAL_BLINDING_KEY` provided out-of-band. |
| **Auditor** | Artifact Validation | `validate_artifact()` ensures that the resulting JSON documents match the expected schema and that internal record SHAs are intact. |
| **Warden** | Durable Retention | `archive_artifact()` (in `durable_retention.py`) manages immutable storage of artifacts and retention manifests, bound to a `frozen_commit_sha`. |

The historical verification found execution blocked without explicit authorization, rejection of mismatched `PDMAL_FROZEN_COMMIT_SHA`, and separation of durable retention from the execution runner.

## 2. Historical blinding storage integrity

The prior verification covered HMAC-SHA256 condition blinding, distinct non-cleartext labels, mock-key separation, and the runner's handling of the blinding key.

## 3. Current-cycle disposition

Those controls remain implementation references only for the present completion cycle. Current P4 closure requires fresh candidate-bound operational blinding/custody evidence for the final selected experimental candidate. No historical P4 evidence is transferred to `0b1190fe…` or any later candidate.

**Current P4 Gate Result:** OPEN / CURRENT-CYCLE VERIFICATION REQUIRED
