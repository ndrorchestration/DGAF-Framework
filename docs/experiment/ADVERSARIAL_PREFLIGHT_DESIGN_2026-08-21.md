# Adversarial Preflight Design — DGAF/PDMAL Completion Journey

**Established:** 2026-08-21  
**Status:** DESIGN — NOT YET IMPLEMENTED  
**Step:** 21 (Independent Verification: Adversarial Preflight)

---

## Purpose

Before pilot authorization (Step 23), deliberately attempt to break the control system. The objective is to verify that the controls detect attacks and fail closed, not that they silently allow unauthorized actions.

This is a **proactive verification** step: instead of waiting for a real attack, we simulate attacks and verify the system's response.

---

## Attack Vectors and Expected Responses

### 1. Wrong SHA (Candidate Not Matching Manifest)

**Attack:** The runner is invoked with a candidate SHA that doesn't match the authorized candidate manifest.

**Scenario:** Someone sets `PDMAL_FROZEN_COMMIT_SHA` to a different SHA than the one in `CANDIDATE_MANIFEST_2026-08-21.json`.

**Expected detection:**
- `require_frozen_commit()` in `run_pilot.py` should compare the env var to the expected SHA.
- If the SHA doesn't match, the function should raise an error and fail closed.

**Current status:** PARTIAL. `require_frozen_commit()` exists and checks the env var. But it doesn't cryptographically verify the code's own SHA against the manifest — it only checks that the env var is set. If the env var is set to a valid-looking SHA (even the wrong one), the check passes.

**Gap:** The check should verify that the env var matches the candidate manifest's SHA, not just that it's set. Currently, the function checks `PDMAL_FROZEN_COMMIT_SHA` is set and non-empty, but the specific value check may be against a hardcoded expectation (need to verify).

**Test:** Set `PDMAL_FROZEN_COMMIT_SHA` to a SHA that doesn't match the candidate manifest. Invoke `run_pilot.py`. Expected: failure with clear error message.

---

### 2. Wrong Topology (Different from Frozen Set)

**Attack:** The runner executes a topology that is not in the frozen topology set.

**Scenario:** Someone modifies the topology configuration to use a topology not in the frozen manifest (e.g., a 6th topology not in the 4×5×9 matrix).

**Expected detection:**
- `validate_topology()` from `harness_contract.py` should verify the topology against the frozen set.
- The runner should fail if the topology is not in the authorized set.

**Current status:** The topology validation functions exist (`validate_topology()`, `generate_topology()`). The frozen topology set is defined in `PDMAL_TASK_SPEC_V0.7.4.md` and `PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`. But it's unclear whether the runner actively validates against the frozen set or just uses whatever topology is requested.

**Gap:** The runner should validate that requested topologies are in the frozen set, not just generate whatever is asked.

**Test:** Request a topology not in the frozen set (e.g., a topology with a different number of nodes). Expected: failure with "topology not in authorized set" message.

---

### 3. Wrong Configuration (Env Vars Not Matching Freeze)

**Attack:** The runner executes with environment variables that don't match the frozen configuration.

**Scenario:** Someone sets `PDMAL_PROTOCOL_VERSION` to a version not in the freeze manifest, or sets `PDMAL_TOPOLOGY` to a configuration not authorized.

**Expected detection:**
- The runner should verify that critical env vars match the frozen configuration.
- If env vars don't match, the runner should fail closed.

**Current status:** The runner checks `PDMAL_PROTOCOL_FROZEN` and `PDMERAL_PILOT_AUTHORIZED` (existence, not value). But it's unclear whether the runner validates the VALUES of these env vars against the freeze manifest.

**Gap:** Env var value validation against the freeze manifest. The runner should compare env var values to the frozen configuration, not just check that they're set.

**Test:** Set `PDMAL_PROTOCOL_VERSION` to a version not in the freeze manifest. Expected: failure.

---

### 4. Missing Artifact (Expected Artifact Absent)

**Attack:** After a pilot run, one or more expected artifacts are missing.

**Scenario:** The runner produces artifacts for seeds 1-50, but seed 23's artifact file is deleted or not created.

**Expected detection:**
- The separate audit (IVD Layer 7: artifact count/completeness) should verify that exactly 50 seed artifacts exist (or whatever the expected count is).
- The audit should flag missing artifacts as a failure.

**Current status:** `pilot_artifact_schema.py:validate_artifact_document()` validates individual artifact records. But there's no automated check that all expected artifacts exist. The auditor must manually verify the count.

**Gap:** Automated artifact count verification. The audit should check that the expected number of artifacts exists, not just that each existing artifact is valid.

**Test:** Delete one seed's artifact file. Run the audit. Expected: failure with "missing artifact for seed X" message.

---

### 5. Modified Artifact (Artifact Tampered After Creation)

**Attack:** An artifact file is modified after it was created by the runner.

**Scenario:** Someone changes a field in a seed's artifact JSON (e.g., changes `primary_outcome` from `SUCCESS` to `RECOVERED`).

**Expected detection:**
- The artifact's `artifact_sha256` field should not match the modified content.
- `verify_sidecar()` should detect that the sidecar hash doesn't match the modified artifact.
- `validate_artifact()` might not catch this if the modified content still passes schema validation.

**Current status:** `pilot_artifact_schema.py` provides `verify_sidecar()` which checks that the sidecar hash matches the artifact's raw bytes. If the artifact is modified, the sidecar hash won't match. But this requires the sidecar to exist and the auditor to run `verify_sidecar()`.

**Gap:** The auditor must actively verify each artifact's integrity. There's no automatic tamper detection — the auditor must run the verification. Also, if the sidecar is also modified (both artifact and sidecar tampered together), the detection fails.

**Test:** Modify a field in a seed's artifact JSON. Run `verify_sidecar()`. Expected: failure with hash mismatch. Also test: modify both artifact and sidecar consistently — this should bypass `verify_sidecar()` but might be caught by other checks (e.g., SHA chain verification).

---

### 6. Exposed Condition (Blinding Bypassed)

**Attack:** The condition assignment is revealed to the analysis/review process before the analysis is locked.

**Scenario:** Someone with access to the blinding key decrypts the condition labels before the analysis is locked. Or the condition labels are accidentally exposed in logs, filenames, or configuration.

**Expected detection:**
- The blinding key should be supplied out-of-band (not in the repository).
- The analysis should run blind (using blinded_condition_id, not raw condition names).
- If condition labels appear in any artifact, log, or configuration, that's a blinding failure.

**Current status:** `blind_condition()` exists in `run_pilot.py` and uses HMAC-SHA256. The blinding key is expected to be an env var (`PDMAL_BLINDING_KEY`). But:
- The blinding key custody chain is NOT established (no documentation of key existence, custody, or supply).
- The adversarial tests in `test_security_controls.py` test `blind_condition()` in isolation but don't test that the key is properly supplied or that condition labels don't leak.

**Gap:** Blinding key custody chain not established. No test that condition labels don't appear in outputs. No test that the key is not in the repository.

**Test:** 
1. Search the repository for the blinding key (if it exists). Expected: not found.
2. Run the runner with a known key and inspect artifacts/logs for raw condition names. Expected: only blinded_condition_id appears.
3. Test that filenames don't contain condition information.

---

### 7. Stale Audit (Audit Describing Older State)

**Attack:** An audit from an earlier state is used to draw conclusions about the current state.

**Scenario:** The 2026-08-20 audit says "P2 IMPLEMENTED" for candidate `4983f44a`. Someone updates the candidate to `b25a914c` and uses the 2026-08-20 audit to claim "P2 is implemented" for the new candidate.

**Expected detection:**
- The audit should carry `examined_candidate_sha: 4983f44a`.
- The reviewer should compare this to the current candidate SHA (`b25a914c`).
- If they don't match, the audit is stale for current-state conclusions.

**Current status:** NOT IMPLEMENTED. PR #77 documentation does not carry `examined_candidate_sha`. The `PRE_AUTHORIZATION_VERIFICATION_RECORD.md` records current disposition but doesn't bind to a specific candidate SHA. There's no mechanism to detect when documentation becomes stale.

**Gap:** No audit self-staleness detection. See `AUDIT_SELF_STALENESS_SPEC_2026-08-21.md`.

**Test:** Create an audit for candidate `4983f44a`. Update the candidate to `b25a914c`. Present the audit as applying to `b25a914c`. Expected: staleness detection flags the mismatch.

---

### 8. Missing Test (Required Test Not Run)

**Attack:** A required test is not executed, but the CI reports green.

**Scenario:** `test_security_controls.py` is renamed to `test_security_controls_old.py` and an empty `test_security_controls.py` is created. The CI runs and passes (the empty file exits 0).

**Expected detection:**
- The CI should verify that the required test files exist AND contain the expected test functions.
- If a test file is missing or empty, the CI should fail.

**Current status:** The CI workflow (`pdmal-preauth-security.yml`) runs `pytest` on the test files. If the file doesn't exist, `pytest` fails. But if the file exists and is empty, `pytest` exits 0 (no tests collected, but exit code 0). The CI doesn't verify that the tests contain the expected content.

**Gap:** Content verification for test files. The CI should check that test files contain expected test functions, not just that they exist and exit 0.

**Test:** Replace `test_security_controls.py` with an empty file. Run the CI. Expected: failure with "no tests collected" or content verification failure. (Note: `pytest` with no tests collected exits with code 5 by default, which would fail the CI, but this behavior should be explicitly verified.)

---

### 9. Incorrect Analysis Binding (Analysis Not Matching Locked Spec)

**Attack:** The analysis is performed using code or configuration that doesn't match the locked analysis specification.

**Scenario:** After the analysis is locked (Step 25), someone modifies the analysis code or configuration and runs the analysis with the modified version.

**Expected detection:**
- The analysis output should carry the analysis code SHA and configuration SHA.
- The reviewer should compare these to the locked analysis specification.
- If they don't match, the analysis is not bound to the locked spec.

**Current status:** NOT IMPLEMENTED. There is no analysis plan certificate (`PDMAL_ANALYSIS_PLAN_CERTIFICATE.md` NOT FOUND). There's no mechanism to bind analysis output to a specific analysis SHA. The `PDMAL_ANALYSIS_CONTROL_PLAN.md` is a planning record, not a binding specification.

**Gap:** Analysis binding. The analysis must be locked (Step 25) before unblinding, and the analysis output must carry the locked analysis SHA. See Step 19.

**Test:** Lock an analysis specification (SHA X). Modify the analysis code. Run the analysis. Expected: the output should carry SHA X (the locked version), not the modified version. If the output carries the modified SHA, the binding has failed.

---

### 10. Environment Fingerprint Mismatch

**Attack:** The environment fingerprint recorded in artifacts doesn't match the actual runtime environment.

**Scenario:** The runner records an environment fingerprint that doesn't match the actual Python version, package versions, or system configuration.

**Expected detection:**
- The separate audit (IVD Layer 8: environment fingerprint consistency) should verify that the recorded fingerprint matches the actual environment.
- If the fingerprint is fabricated or incorrect, the audit should detect the mismatch.

**Current status:** `artifact_schema.py` and `pilot_artifact_schema.py` require an `environment_fingerprint` field. `run_pilot.py` computes and records the fingerprint. But the method by which the fingerprint is computed and the method by which the auditor verifies it may not match. Also, the fingerprint is a structural record — the auditor must know what the fingerprint should contain and how to verify it.

**Gap:** Environment fingerprint verification methodology. The auditor needs to know how to independently derive the expected fingerprint and compare it to the recorded one. This requires agreement on the fingerprint derivation method between the runner and the auditor.

**Test:** Run the runner with a known environment. Record the fingerprint. Independently derive the expected fingerprint. Compare. Expected: match. Also test: modify the fingerprint in an artifact. Expected: auditor detects mismatch.

---

### 11. Sidecar Hash Mismatch

**Attack:** The sidecar file's hash doesn't match the artifact's raw bytes.

**Scenario:** The artifact is correct, but the sidecar was generated incorrectly or tampered with.

**Expected detection:**
- `pilot_artifact_schema.py:verify_sidecar()` should detect that the sidecar hash doesn't match the artifact's raw bytes.
- The auditor should run `verify_sidecar()` on each artifact.

**Current status:** `verify_sidecar()` exists and checks the sidecar hash against the artifact's raw bytes. This is a correct detection mechanism. But:
- The runner writes the sidecar but doesn't call `verify_sidecar()` inline (grep: 0 for `verify_sidecar` in `run_pilot.py`).
- The auditor must actively run `verify_sidecar()` — there's no automatic verification.
- If the sidecar is missing, `verify_sidecar()` should fail (need to verify behavior).

**Gap:** Inline sidecar verification by the runner. The runner writes the sidecar but doesn't verify it. The auditor must do the verification. Also, the runner should verify the sidecar before considering the artifact complete.

**Test:** Write an artifact with a correct sidecar. Modify the sidecar (change the hash text). Run `verify_sidecar()`. Expected: failure. Also test: delete the sidecar. Expected: failure.

---

### 12. Record Count Mismatch (Not 180/Seed)

**Attack:** A seed's artifact record contains fewer or more than 180 trials.

**Scenario:** The runner produces only 175 trials for seed 5 (5 trials failed to record). Or the runner produces 185 trials (5 duplicate records).

**Expected detection:**
- `pilot_artifact_schema.py:validate_artifact_document()` should verify that each seed has exactly 180 records.
- The auditor should verify the record count per seed.

**Current status:** `pilot_artifact_schema.py` validates individual records but may not enforce the 180-record count at the document level. Need to verify: does `validate_artifact_document()` check that the record count is exactly 180?

**Gap:** Record count enforcement. If the schema validates the count, this is covered. If not, the auditor must manually verify the count.

**Test:** Create an artifact with 175 records (instead of 180). Run `validate_artifact_document()`. Expected: failure with "record count mismatch" or similar. Also test: create an artifact with 185 records. Expected: failure.

---

## Summary Table

| # | Attack Vector | Expected Detection | Current Status | Gap | Test Feasibility |
|---|---|---|---|---|---|
| 1 | Wrong SHA | require_frozen_commit() fails | PARTIAL — checks env var existence, not manifest match | Verify value check against manifest | HIGH — can test with wrong env var |
| 2 | Wrong topology | validate_topology() fails | PARTIAL — functions exist, unclear if runner validates against frozen set | Verify runner validates topology against frozen set | HIGH — can test with unauthorized topology |
| 3 | Wrong configuration | Env var value validation fails | PARTIAL — checks existence, not value against freeze | Add value validation against freeze manifest | HIGH — can test with wrong env var value |
| 4 | Missing artifact | Audit detects missing artifact | PARTIAL — validate_artifact_document() exists, but count check may be manual | Add automated count verification | HIGH — can test by deleting artifact |
| 5 | Modified artifact | verify_sidecar() detects hash mismatch | YES — verify_sidecar() exists and works | No inline verification by runner; both artifact+sidecar tamper can bypass | HIGH — can test by modifying artifact |
| 6 | Exposed condition | Blinding key not in repo; no condition labels in outputs | PARTIAL — blind_condition() exists; key custody NOT established | Establish key custody chain; test for condition label leakage | MEDIUM — requires key for full test |
| 7 | Stale audit | Audit carries examined_candidate_sha; reviewer detects mismatch | NOT IMPLEMENTED — no examined_candidate_sha in audits | Add examined_candidate_sha to audit documents; implement staleness detection | HIGH — can test with old audit |
| 8 | Missing test | CI fails if test file missing/empty | PARTIAL — pytest fails on missing file; empty file may exit 0 | Add content verification for test files | HIGH — can test with empty file |
| 9 | Incorrect analysis binding | Analysis output carries locked analysis SHA | NOT IMPLEMENTED — no analysis plan certificate; no binding mechanism | Create analysis plan certificate; bind analysis output to spec | MEDIUM — requires analysis lock first |
| 10 | Env fingerprint mismatch | Auditor independently derives and compares fingerprint | PARTIAL — fingerprint field exists; verification methodology unclear | Agree on fingerprint derivation; auditor independently derives | MEDIUM — requires runner + auditor agreement |
| 11 | Sidecar hash mismatch | verify_sidecar() detects mismatch | YES — verify_sidecar() exists and works | No inline verification by runner; auditor must actively verify | HIGH — can test by modifying sidecar |
| 12 | Record count mismatch | validate_artifact_document() enforces 180 records | PARTIAL — need to verify count enforcement | Verify that schema enforces 180-record count | HIGH — can test with wrong count |

---

## Implementation Priority

### Must Have (before authorization)

1. **Wrong SHA detection** — the runner must reject a candidate SHA that doesn't match the manifest.
2. **Wrong topology detection** — the runner must reject topologies not in the frozen set.
3. **Missing artifact detection** — the audit must detect missing artifacts.
4. **Modified artifact detection** — `verify_sidecar()` must be run on all artifacts.
5. **Exposed condition prevention** — blinding key custody must be established; condition labels must not leak.

### Should Have (before authorization)

6. **Stale audit detection** — audits must carry examined_candidate_sha.
7. **Missing test detection** — CI must verify test file content.
8. **Record count enforcement** — schema must enforce 180 records/seed.

### Nice to Have (after authorization, for full verification)

9. **Incorrect analysis binding** — analysis output must carry locked analysis SHA.
10. **Env fingerprint verification** — auditor must independently derive fingerprint.
11. **Sidecar inline verification** — runner should verify sidecar before completing.
12. **Wrong configuration detection** — runner should validate env var values against freeze.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This design document describes attack vectors and expected responses. It does NOT describe tests that have been performed. No adversarial preflight has been executed (N=0). The current status column reflects what exists in the codebase, not what has been verified by testing.
