# DGAF/PDMAL Experiment Candidate Definition

**Established:** 2026-08-21  
**Candidate SHA:** `94fb6fdff64f2919d35938c5b1cb506625cf1139` (PR #77, local `pr-77-head`)  
**GitHub PR #77 head:** `b25a914c0e86333a9af4b216a9acdfaec28e42b0` (diverged from local)  
**Local HEAD:** `3510b86889cd341f7a7cf9ab684fd37b2fafd758` (main)  
**Freeze target SHA:** `915e454e27eb2770e7f40a067a881b0783feaae4` (from freeze manifest)  
**Status:** IDENTIFIED — NOT YET IMMUTABLE

---

## What This Candidate Is

This is the PR #77 corrected pilot apparatus — the engineering response to the DGAF/PDMAL sprint findings. It is a **collection of code, configuration, documentation, and workflow files** that together form the proposed corrected pilot boundary.

The candidate is identified by the PR #77 head SHA (`94fb6fd` locally, `b25a914c` on GitHub). Everything at that SHA constitutes the candidate. Anything not at that SHA is NOT part of the candidate (even if it's on local HEAD or on disk).

---

## Candidate Components

### Runner
- **Path:** `experiments/pdmal_pilot/run_pilot.py`
- **Blob SHA:** `184f4aa72e4eb0a0ad254aee57b6cbdd5d13f9fd`
- **Key properties:**
  - Uses `ConsensusTask` (not `ScriptedTask`) — corrected executor
  - Has `require_frozen_commit()` and `require_pilot_authorization()` gating functions
  - Writes FROZEN artifacts with `protocol_status='FROZEN'`, `empirical_data_collection=True`, 40-char `frozen_commit_sha`
  - Uses `blind_condition()` for blinded condition labels
  - Does NOT import `artifact_schema` or `pilot_artifact_schema` (inline validation gap)
  - Computes artifact SHA via `json.dumps` + `hashlib.sha256` (not `canonical_json_bytes()`)

### Pilot Artifact Schema (FROZEN)
- **Path:** `experiments/pdmal_pilot/pilot_artifact_schema.py`
- **Blob SHA:** `2918a9d506ab39e6a0514608618f02f7f4de400d`
- **Key properties:**
  - FROZEN pilot validation: requires `protocol_status=FROZEN`, `empirical_data_collection=True`, 40-char `frozen_commit_sha`
  - Exactly 180 records per seed
  - SHA recomputation via `canonical_json_bytes()` (sort_keys, compact separators)
  - Sidecar verification via `verify_sidecar()`
  - NOT imported by `run_pilot.py`

### Artifact Schema (PRE-FREEZE)
- **Path:** `experiments/pdmal_pilot/artifact_schema.py`
- **Blob SHA:** `41a90485246bbc1e7e13829fc1791133da5c3d4c`
- **Key properties:**
  - PRE-FREEZE contract validation: 16 required fields
  - No SHA recomputation
  - `canonical_json_bytes()` for deterministic serialization
  - Requires `protocol_status=PRE-FREEZE`, `empirical_data_collection=False`
  - Unchanged from local HEAD
  - Semantically incompatible with `pilot_artifact_schema` (both v1.0 but mutually exclusive requirements)

### Security Controls Test
- **Path:** `experiments/pdmal_pilot/test_security_controls.py`
- **Blob SHA:** `ddc595713e433469fa7c01d8918a03518e3e37b5`
- **Key properties:**
  - 6 adversarial tests
  - Imports `validate_artifact` from `pilot_artifact_schema`, `blind_condition` and `require_frozen_commit` from `run_pilot`
  - Tests env var gating via monkeypatching
  - Does NOT test actual env var state (only that gating functions exist)

### CI Workflow (Pre-Authorization Security)
- **Path:** `.github/workflows/pdmal-preauth-security.yml`
- **Blob SHA:** `9cff92a5c05703dbae636fb4b091ea89906cbcb0`
- **Key properties:**
  - Python 3.12.0
  - Installs from `requirements-full-lock.txt` (SHA `3ac4bd2851864af3a5a5ddb8ef707c26e7e81200`)
  - Runs `test_security_controls.py` + `test_artifact_schema.py`
  - Triggers on `pull_request` (paths: `experiments/pdmal_pilot/**`, `docs/experiment/**`, `.github/workflows/pdmal-preauth-security.yml`)
  - Triggers on `push` to `main` (same paths)
  - Has NOT been executed (no CI run results available)

### Blinding Operational Test Workflow
- **Path:** `.github/workflows/pdmal-blinding-operational-test.yml`
- **Blob SHA:** `7506f41207ba231750d14f0f43ddff83d8d2cd3c`
- **Key properties:**
  - Blinding operational test workflow
  - Triggers on `pull_request`
  - Has NOT been executed

### Documentation (7 files at PR #77)

| File | Blob SHA | Purpose |
|---|---|---|
| `PRE_AUTHORIZATION_VERIFICATION_RECORD_2026-08-20.md` | `f51aea7aad12e3a9b9953eeebc8d440bbfe99c01` | Consolidated closure checklist. "Corrected apparatus verified: NO; New freeze created: NO; Pilot authorized: NO; Empirical N: 0." |
| `DOCUMENTATION_GAP_AUDIT.md` | `524eb7592a3a3ee80e862e5adfe95c4a5cf7458b` | Documents doc-vs-commit mismatches. |
| `FREEZE_MANIFEST_RECONCILIATION_2026-08-20.md` | `968b05df4143c7aa4154bceb60b32b2ce929b7df` | Historical freeze must NOT be reused for corrected runner. |
| `PDMAL_ANALYSIS_CONTROL_PLAN.md` | `3e556882fdc2de7b0d4fa91f519bc74e3924a57f` | Partial estimand chain. Records that `PDMAL_STATISTICAL_ANALYSIS_PLAN.md` and `PDMAL_PIPELINE_SPEC.md` NOT FOUND. |
| `POST_FREEZE_DOCUMENTATION_RECONCILIATION_2026-08-20.md` | `e5bdb5244634fccd229279e614d66c48b1a360b3` | Post-freeze documentation reconciliation plan. |
| `CURRENT_STATE.md` | `f48bfe4a297d148f049dd6349e54458aaa0eb490` | Protocol state: PRE-FREEZE. Executor state: OPEN. Empirical: 0. |
| `PDMAL_CURRENT_CONTROL_STATE.md` | `8f763eb80b6f2a6b6857310e335435602e9d91be` | Protocol freeze: BLOCKED. Pilot authorization: NOT GRANTED. Empirical: 0. |

### Modified Documentation (existing files changed by PR #77)

| File | Purpose |
|---|---|
| `docs/experiment/FREEZE_MANIFEST.md` | Updated to FROZEN status with corrected apparatus. Primary contrast: OPEN. N=0. |
| `docs/CURRENT_STATE.md` | Updated to reflect PRE-FREEZE state. |
| `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | Updated gate board. |

### Other Files

| File | Status |
|---|---|
| `experiments/pdmal_pilot/durable_retention.py` | NOT at PR#77. Present on disk at local HEAD only. |
| `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | NOT at PR#77. Present at local HEAD (86 lines, ACTIVE/PRE-FREEZE). |
| `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` | NOT at PR#77. Referenced for topology definitions. |
| `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` | NOT at PR#77. Present at local HEAD. |
| `docs/experiment/PDMAL_ANALYSIS_PLAN_CERTIFICATE.md` | NOT FOUND at PR#77 or local HEAD. |
| `.github/workflows/pdmal-freeze-preparation.yml` | EXISTS at PR#77 (blob `4b6a1e45`), NOT executed. |

---

## What Is NOT Part of This Candidate

- Local HEAD (`3510b86889`) — the historical superseded freeze. Retained as historical evidence.
- Anything on disk that is not committed at `94fb6fd` — including `durable_retention.py` (on disk, not at PR#77).
- The GitHub PR #77 head (`b25a914c`) — diverged from local `94fb6fd` with additional commits not yet fetched.
- `PDMAL_STATISTICAL_ANALYSIS_PLAN.md` — does not exist at any path.
- `PDMAL_PIPELINE_SPEC.md` — does not exist at any path.
- `PDMAL_ANALYSIS_PLAN_CERTIFICATE.md` — does not exist at any path.

---

## What Makes This Candidate Incomplete

This candidate is **identified but not yet complete**. The following are missing from the candidate as defined by PR #77:

1. **Primary contrast adjudication** — 4 candidates identified, none selected. This is a scientific/governance decision, not an engineering fix.
2. **Candidate manifest committed to repository** — this document defines the candidate but is not yet committed.
3. **Development/candidate separation** — no separation exists between development HEAD and the candidate.
4. **P2 bound to candidate** — CI runs on pull_request paths, not pinned to a specific SHA.
5. **Runtime authentication** — env var gating exists but no cryptographic SHA binding.
6. **FLAG-02 migration** — not assessed.
7. **Propagation checking** — not specified.
8. **Audit self-staleness** — not designed.
9. **False-green CI elimination** — workflow exists but gaps remain.
10. **Inline validation wiring** — runner does not call schema validation.
11. **SHA computation consistency** — runner's SHA method vs schema's method unverified.
12. **Blinding key custody chain** — not established.
13. **Analysis plan certificate** — does not exist.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This candidate definition does NOT constitute a freeze. It does NOT authorize empirical data collection. It does NOT close any predicate unambiguously. It is a description of what exists at PR #77, nothing more.

The candidate is IDENTIFIED. It is NOT YET IMMUTABLE. Immutability requires:
1. This manifest committed to the repository
2. Development separated from candidate
3. A freeze manifest created with an actual freeze commit SHA
