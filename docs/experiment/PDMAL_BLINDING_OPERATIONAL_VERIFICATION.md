---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-08-18
applies_to_sha: pending-next-verification-commit
state: PLAN / EXECUTION PENDING
---

# PDMAL Blinding Operational Verification

## Purpose

Verify the operational custody and unblinding controls without using production secrets or empirical pilot data.

## Scope

This test uses synthetic condition labels, a mock blinding key, and mock blinded records only. It must never load or print `PDMAL_BLINDING_KEY` from GitHub Actions or any production secret.

## Roles

| Role | Test requirement |
|---|---|
| Key holder | Supplies a mock key to the dry-run harness only. Production key access is not exercised. |
| Executor | Receives only blinded identifiers in the mock dataset. |
| Analyst | Receives only the blinded mock dataset and cannot derive the mapping from the dataset. |
| Unblinder / panel chair | Performs the mock mapping only after the mock dataset is declared frozen. |

## Procedure

1. Create a mock mapping for the four pilot conditions: `null`, `simple`, `static`, `dgaf`.
2. Generate blinded identifiers using the existing HMAC-SHA256 blinding primitive.
3. Create a mock dataset containing blinded identifiers only.
4. Confirm the mock analytical dataset contains no key or cleartext condition labels.
5. Declare the mock raw dataset frozen and compute its SHA-256 digest.
6. Perform mock unblinding using a separately held mock mapping.
7. Confirm the recovered cleartext labels exactly match the original synthetic mapping.
8. Confirm the executor/analyst dataset never contains the mock key.
9. Record timestamp, workflow/run ID, tested commit, dataset digest, and outcome.
10. Destroy the mock key and temporary mapping after the test.

## Pass criteria

- blinded identifiers are deterministic for the same key and label;
- different labels produce different mock blinded identifiers;
- the analytical mock dataset contains no secret material;
- unblinding is impossible from the dataset alone;
- unblinding succeeds only after the mock freeze event;
- recovered labels exactly match the synthetic mapping;
- no production secret is accessed or emitted;
- the procedure and evidence record are retained.

## Failure criteria

The control remains OPEN if any of the following occur:

- a secret appears in the mock analytical artifact;
- cleartext condition labels are exposed before the mock freeze gate;
- the mapping can be reconstructed from the dataset alone;
- recovered labels do not exactly match the synthetic mapping;
- the test requires a production secret;
- role separation cannot be demonstrated.

## Evidence record

The successful test must produce an immutable record containing:

```text
control_id: PDMAL-BLINDING-OPS-v1
commit_sha: <executed SHA>
workflow_run_id: <run ID>
mock_dataset_sha256: <digest>
result: PASS | FAIL
timestamp_utc: <timestamp>
production_secret_accessed: false
notes: <bounded notes>
```

This test is operational control verification. It is not empirical validation and does not authorize pilot execution.
