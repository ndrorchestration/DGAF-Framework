# PR #77 Comprehensive Audit

**Audited:** 2026-08-21  
**PR #77 head SHA (local):** `94fb6fdff64f2919d35938c5b1cb506625cf1139`  
**PR #77 head SHA (GitHub):** `b25a914c0e86333a9af4b216a9acdfaec28e42b0`  
**Local HEAD:** `3510b86889cd341f7a7cf9ab684fd37b2fafd758`  
**Status:** AUDIT COMPLETE — NOT YET VERIFIED BY EXECUTION

---

## Overview

PR #77 ("Pre-authorization completeness: corrected pilot boundary and security controls") introduces 15 files to the DGAF-Framework repository. This audit examines each file, its purpose, what it provides, and what gaps remain.

**Overall finding:** PR #77 provides substantial engineering corrections (corrected runner, pilot artifact schema, security tests, CI workflow, documentation reconciliation) but does NOT close the governance gap (primary contrast adjudication) and has several implementation gaps (no inline validation wiring, no SHA consistency verification, not mergeable, CI not executed).

---

## Workflows (3 files)

### 1. `pdmal-preauth-security.yml`
- **Path:** `.github/workflows/pdmal-preauth-security.yml`
- **Blob SHA:** `9cff92a5c05703dbae636fb4b091ea89906cbcb0`
- **Status:** NEW at PR #77
- **Purpose:** CI workflow that runs adversarial controls and artifact schema tests.
- **What it does:**
  - Checks out code, sets up Python 3.12.0
  - Installs dependencies from `requirements-full-lock.txt` (SHA `3ac4bd28`)
  - Runs `test_security_controls.py` (adversarial controls)
  - Runs `test_artifact_schema.py` (schema tests)
  - Triggers on `pull_request` (paths: `experiments/pdmal_pilot/**`, `docs/experiment/**`, `.github/workflows/pdmal-preauth-security.yml`)
  - Triggers on `push` to `main` (same paths)
- **What it provides:** Automated testing of security controls and schema validation on PRs and main pushes.
- **Gaps:**
  - Has NOT been executed (no CI run results available)
  - Runs on PR paths — tests whatever is in the PR, not a specific candidate SHA
  - Tests the validator, not actual artifacts
  - No content verification of test files
  - No lockfile SHA verification

### 2. `pdmal-blinding-operational-test.yml`
- **Path:** `.github/workflows/pdmal-blinding-operational-test.yml`
- **Blob SHA:** `7506f41207ba231750d14f0f43ddff83d8d2cd3c`
- **Status:** NEW at PR #77
- **Purpose:** Blinding operational test workflow.
- **What it does:** Triggers on `pull_request`.
- **What it provides:** Infrastructure for blinding operational verification.
- **Gaps:** Has NOT been executed. Specific test content not examined in this audit.

### 3. `pdmal-freeze-preparation.yml`
- **Path:** `.github/workflows/pdmal-freeze-preparation.yml`
- **Blob SHA:** `4b6a1e45b340ca64f6c6fe978ea8cd2f7eefdca6`
- **Status:** NEW at PR #77
- **Purpose:** Freeze preparation CI workflow.
- **What it does:** Checks out code, sets up Python 3.12.0, installs from `requirements-full-lock.txt` (SHA `3ac4bd28`), runs `test_security_controls.py` + `test_artifact_schema.py` on `pull_request` + `push` to `main`.
- **What it provides:** Automated testing infrastructure for freeze preparation gating.
- **Gaps:**
  - Has NOT been executed (no CI run results available)
  - Runs on `pull_request` paths — tests whatever is in the PR, not a specific candidate SHA
  - Same false-green and candidate-pinning gaps as `pdmal-preauth-security.yml`

---

## Runner and Schema (3 files)

### 4. `run_pilot.py`
- **Path:** `experiments/pdmal_pilot/run_pilot.py`
- **Blob SHA:** `184f4aa72e4eb0a0ad254aee57b6cbdd5d13f9fd`
- **Status:** NEW at PR #77
- **Purpose:** Fail-closed PDMAL pilot runner. Uses `ConsensusTask` (not `ScriptedTask`).
- **What it provides:**
  - `require_frozen_commit()` — env var gating for frozen commit SHA
  - `require_pilot_authorization()` — env var gating for pilot authorization
  - `blind_condition()` — blinding function for condition labels
  - Writes FROZEN artifacts with `protocol_status='FROZEN'`, `empirical_data_collection=True`, 40-char `frozen_commit_sha`
  - Computes artifact SHA via `json.dumps` + `hashlib.sha256`
  - Writes sidecar via `_write_sidecar()` helper
- **What it does NOT provide:**
  - Does NOT import `artifact_schema` or `pilot_artifact_schema` (grep: 0)
  - Does NOT call `validate_artifact()` or `verify_sidecar()` inline
  - Does NOT cryptographically verify its own SHA against a manifest
  - SHA computation method (`json.dumps` + `hashlib.sha256`) may not match `canonical_json_bytes()` in `pilot_artifact_schema.py`
- **Gaps:**
  - Inline validation wiring missing (HIGH)
  - SHA computation consistency unverified (HIGH)
  - No runtime authentication / SHA binding (MEDIUM)

### 5. `pilot_artifact_schema.py`
- **Path:** `experiments/pdmal_pilot/pilot_artifact_schema.py`
- **Blob SHA:** `2918a9d506ab39e6a0514608618f02f7f4de400d`
- **Status:** NEW at PR #77
- **Purpose:** FROZEN pilot artifact validation.
- **What it provides:**
  - Validates `protocol_status=FROZEN`, `empirical_data_collection=True`, 40-char `frozen_commit_sha`
  - Requires exactly 180 records per seed
  - SHA recomputation via `canonical_json_bytes()` (sort_keys, compact separators)
  - Sidecar verification via `verify_sidecar()`
  - `validate_artifact()` function for validating artifact documents
- **What it does NOT provide:**
  - Is NOT imported by `run_pilot.py` — the runner doesn't use it for inline validation
- **Gaps:**
  - Not wired into the runner (HIGH)
  - SHA computation method (`canonical_json_bytes()`) may not match runner's method (HIGH)

### 6. `artifact_schema.py`
- **Path:** `experiments/pdmal_pilot/artifact_schema.py`
- **Blob SHA:** `41a90485246bbc1e7e13829fc1791133da5c3d4c`
- **Status:** UNCHANGED from local HEAD (same blob at PR #77)
- **Purpose:** PRE-FREEZE contract validation.
- **What it provides:**
  - 16 required fields for seed records
  - `canonical_json_bytes()` for deterministic serialization
  - No SHA recomputation
  - Validates `protocol_status=PRE-FREEZE`, `empirical_data_collection=False`
- **What it does NOT provide:**
  - Is semantically incompatible with `pilot_artifact_schema.py` (both v1.0, mutually exclusive requirements)
  - Does NOT validate FROZEN pilot artifacts (would reject them)
- **Gaps:**
  - Version label collision: both modules declare `ARTIFACT_SCHEMA_VERSION = "1.0"` but are mutually incompatible
  - No unified versioning scheme

---

## Tests (2 files)

### 7. `test_security_controls.py`
- **Path:** `experiments/pdmal_pilot/test_security_controls.py`
- **Blob SHA:** `ddc595713e433469fa7c01d8918a03518e3e37b5`
- **Status:** NEW at PR #77
- **Purpose:** Adversarial controls for the PDMAL pilot boundary.
- **What it provides:**
  - 6 adversarial tests (per `pr77_doc_briefing.json` and `independent_verification_design.json`)
  - Imports `validate_artifact` from `pilot_artifact_schema`
  - Imports `blind_condition` and `require_frozen_commit` from `run_pilot`
  - Tests env var gating via monkeypatching
  - Tests `blind_condition()` consistency
  - Tests `validate_artifact()` rejection of invalid records
  - Tests `verify_sidecar()` detection of mismatches
  - Tests `validate_seed_runtime()` enforcement of ceiling
  - Tests failure/recovery state classification
- **What it does NOT provide:**
  - Does NOT test actual env var state (only that gating functions exist and respond to monkeypatching)
  - Does NOT test that the runner actually calls these functions in an integrated run
  - Does NOT test that the runner's SHA computation matches the schema's
- **Gaps:**
  - Monkeypatching tests function existence, not real env var behavior (MEDIUM)
  - No integrated end-to-end test (MEDIUM)

### 8. `test_artifact_schema.py`
- **Path:** `experiments/pdmal_pilot/test_artifact_schema.py`
- **Blob SHA:** NOT INDIVIDUALLY VERIFIED in this audit (present at PR #77 per `git ls-tree -r`)
- **Status:** NEW at PR #77
- **Purpose:** Schema tests for artifact validation.
- **What it provides:** Tests for artifact schema validation logic.
- **Gaps:** Not individually read in this audit. Content not verified.

---

## Documentation — New Files (5 files)

### 9. `PRE_AUTHORIZATION_VERIFICATION_RECORD_2026-08-20.md`
- **Path:** `docs/experiment/PRE_AUTHORIZATION_VERIFICATION_RECORD_2026-08-20.md`
- **Blob SHA:** `f51aea7aad12e3a9b9953eeebc8d440bbfe99c01`
- **Status:** NEW at PR #77
- **Purpose:** Consolidated closure checklist for the corrected pilot apparatus.
- **Key content:**
  - "Corrected apparatus verified: NO"
  - "New freeze created: NO"
  - "Pilot authorized: NO"
  - "Empirical N: 0"
  - Distinguishes IMPLEMENTED (9 gates) from VERIFIED (execution evidence or human decision)
  - OPEN gates: env, smoke, CI, fingerprints, retention, contrast, analysis SHA, new freeze, authorization
- **Assessment:** Most honest document in PR #77. Explicitly states verification status is NO.

### 10. `DOCUMENTATION_GAP_AUDIT.md`
- **Path:** `docs/experiment/DOCUMENTATION_GAP_AUDIT.md`
- **Blob SHA:** `524eb7592a3a3ee80e862e5adfe95c4a5cf7458b`
- **Status:** NEW at PR #77
- **Purpose:** Documents doc-vs-commit mismatches.
- **Key content:** Claims "Protocol freeze CLOSED" for historical freeze — but this refers to the historical freeze for the old runner, not the corrected runner. Corrected report clarifies this.
- **Assessment:** Contains a claim that could be misread as the corrected apparatus being frozen. Requires careful reading.

### 11. `FREEZE_MANIFEST_RECONCILIATION_2026-08-20.md`
- **Path:** `docs/experiment/FREEZE_MANIFEST_RECONCILIATION_2026-08-20.md`
- **Blob SHA:** `968b05df4143c7aa4154bceb60b32b2ce929b7df`
- **Status:** NEW at PR #77
- **Purpose:** States that the historical freeze (3510b86889) must NOT be reused for the corrected runner.
- **Key content:** Historical freeze is retained as historical evidence. Corrected runner is a NEW freeze candidate.
- **Assessment:** Correct. Aligns with expert panel correction C3 (preservation, not consolidation).

### 12. `PDMAL_ANALYSIS_CONTROL_PLAN.md`
- **Path:** `docs/experiment/PDMAL_ANALYSIS_CONTROL_PLAN.md`
- **Blob SHA:** `3e556882fdc2de7b0d4fa91f519bc74e3924a57f`
- **Status:** NEW at PR #77
- **Purpose:** Repository-local control record for the statistical analysis boundary.
- **Key content:**
  - Records that `PDMAL_STATISTICAL_ANALYSIS_PLAN.md` and `PDMAL_PIPELINE_SPEC.md` were NOT FOUND at expected paths during 2026-08-20 GitHub audit
  - Records partial estimand chain
  - Does NOT adjudicate primary contrast
  - Does NOT record an analysis plan certificate
- **Assessment:** Honest about what's missing. Does not claim to be a complete analysis specification.

### 13. `POST_FREEZE_DOCUMENTATION_RECONCILIATION_2026-08-20.md`
- **Path:** `docs/experiment/POST_FREEZE_DOCUMENTATION_RECONCILIATION_2026-08-20.md`
- **Blob SHA:** `e5bdb5244634fccd229279e614d66c48b1a360b3`
- **Status:** NEW at PR #77
- **Purpose:** Post-freeze documentation reconciliation plan.
- **Assessment:** Planning document. Does not represent a completed reconciliation.

---

## Documentation — Modified Files (3 files)

### 14. `CURRENT_STATE.md`
- **Path:** `docs/CURRENT_STATE.md`
- **Blob SHA:** `f48bfe4a297d148f049dd6349e54458aaa0eb490`
- **Status:** MODIFIED at PR #77
- **Key content (at PR #77):**
  - Protocol state: PRE-FREEZE
  - Executor state: OPEN (run_pilot.py fail-closes pilot mode)
  - Empirical: 0
- **Assessment:** Correctly reflects PRE-FREEZE state.

### 15. `PDMAL_CURRENT_CONTROL_STATE.md`
- **Path:** `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`
- **Blob SHA:** `8f763eb80b6f2a6b6857310e335435602e9d91be`
- **Status:** MODIFIED at PR #77
- **Key content (at PR #77):**
  - Protocol freeze: BLOCKED
  - Pilot authorization: NOT GRANTED
  - Empirical data: 0
  - Blinding custody: OPEN (synthetic dry-run only)
  - Long-term retention: OPEN (archive not established)
  - Freeze packet: PENDING
- **Assessment:** Correctly reflects BLOCKED/NOT GRANTED state.

### 16. `FREEZE_MANIFEST.md`
- **Path:** `docs/experiment/FREEZE_MANIFEST.md`
- **Blob SHA:** `1a143b293317a2c8b26e9e1358e2eec975d4c226`
- **Status:** MODIFIED at PR #77
- **Key content (at PR #77):**
  - Status: FROZEN
  - State: FROZEN — post-freeze verification in progress
  - Primary contrast: OPEN
  - N = 0
  - Pilot authorization: NOT GRANTED
  - Freeze commit SHA: PLACEHOLDER
- **Assessment:** This is the FROZEN version of the freeze manifest (corrected). Distinct from local HEAD version which has PRE-FREEZE body text. Correctly records primary contrast as OPEN.

---

## Summary: What PR #77 Provides vs. What's Missing

### Provided by PR #77

| Component | Status |
|---|---|
| Corrected runner (ConsensusTask) | PRESENT |
| Pilot artifact schema (FROZEN validation) | PRESENT |
| Artifact schema (PRE-FREEZE, unchanged) | PRESENT |
| Security controls tests (6 adversarial) | PRESENT |
| Artifact schema tests | PRESENT |
| CI workflow (pre-auth security) | PRESENT |
| Blinding operational test workflow | PRESENT |
| Pre-authorization verification record | PRESENT |
| Documentation gap audit | PRESENT |
| Freeze manifest reconciliation | PRESENT |
| Analysis control plan | PRESENT |
| Post-freeze documentation reconciliation | PRESENT |
| Modified CURRENT_STATE.md | PRESENT |
| Modified PDM_CURRENT_CONTROL_STATE.md | PRESENT |
| Modified FREEZE_MANIFEST.md (FROZEN version) | PRESENT |

### NOT Provided by PR #77

| Gap | Severity | Step Affected |
|---|---|---|
| Inline validation wiring | HIGH | Step 6 |
| SHA computation consistency verification | HIGH | Step 6 |
| Primary contrast adjudication | CRITICAL | Step 1 (Gate 1) |
| Candidate manifest (committed) | HIGH | Steps 2-3 (Gate 2) |
| Dev/candidate separation | MEDIUM | Step 4 (Gate 2) |
| P2 bound to candidate | MEDIUM | Step 5 (Gate 2) |
| Runtime authentication (cryptographic) | MEDIUM | Step 7 (Gate 3) |
| FLAG-02 migration | UNKNOWN | Step 8 (Gate 3) |
| Propagation checking | MEDIUM | Step 9 (Gate 3) |
| Audit self-staleness | MEDIUM | Step 10 (Gate 3) |
| False-green CI elimination | HIGH | Step 11 (Gate 3) |
| CI execution | HIGH | Steps 12-13, 17 |
| Blinding key custody chain | HIGH | Step 20 |
| Analysis plan certificate | HIGH | Step 19 |
| `pdmal-freeze-preparation.yml` | MEDIUM | Step 6 |
| `durable_retention.py` at PR #77 | MEDIUM | Step 14 |

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This audit examines code and documentation at PR #77. It does NOT verify that any CI has executed, that any artifact validation has occurred, or that any empirical data exists. N=0.
