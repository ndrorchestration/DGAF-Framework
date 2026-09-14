# Operator Repository Event Preparers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two dry-run-first helpers that safely assemble the already-defined Track A Epoch 002 operator evidence-admission and later dataset-lock receipt repository events without changing governance semantics.

**Architecture:** Reuse the accepted #689 dataset-lock validator as the single source of contract truth. The first helper copies already-validated external non-secret evidence into exactly two canonical repository paths; the second derives the unique accepted evidence-admission commit and creates exactly one validated receipt file. Both helpers refuse dirty/unrelated state and never commit, merge, authorize, decrypt, or run analysis.

**Tech Stack:** Python 3.10–3.12, stdlib (`argparse`, `hashlib`, `importlib`, `json`, `pathlib`, `shutil`, `subprocess`, `datetime`), pytest, existing DGAF dataset-lock validators/workflow.

**Spec:** `docs/superpowers/specs/2026-09-14-operator-repository-event-preparers-design.md`

## Global Constraints

- Dry-run by default; persistent writes require `--write`.
- No private keys, passphrases, protected plaintext, decrypted mappings, or blinding secrets.
- No empirical execution, outcome aggregation, unblinding authorization, primary-analysis authorization, scientific-N increment, or efficacy promotion.
- No Git commit, merge, push, or ref mutation from either helper.
- Existing #689 validator semantics remain authoritative.
- Exact-head PR validation is required before merge.

---

### Task 1: Add failing tests for the evidence-admission preparer

**Files:**
- Create: `tests/test_track_a_epoch_002_operator_evidence_admission_preparer.py`
- Later create: `scripts/prepare_track_a_epoch_002_operator_evidence_admission.py`

**Interfaces:**
- Consumes: `validate_track_a_epoch_002_dataset_lock.validate_evidence_file`, `validate_pre_lock_ledger`, canonical `OPERATOR_EVIDENCE_REL` and `OPERATOR_PRE_LOCK_LEDGER_REL`.
- Produces: `prepare(retention_dir: Path, evidence_path: Path | None = None, ledger_path: Path | None = None, write: bool = False) -> tuple[Path, Path]` and CLI PASS markers.

- [ ] **Step 1: Write failing tests**

Cover: external-source requirement; existing destination refusal; dirty/unrelated worktree refusal; dry-run no-write; `--write` exact-byte copy; post-write exact two-file delta; no commit/ref mutation.

- [ ] **Step 2: Verify RED**

Run the dedicated pytest file on a test-only PR head. Expected: import/module failure because `prepare_track_a_epoch_002_operator_evidence_admission.py` does not exist.

- [ ] **Step 3: Implement minimal helper**

Use subprocess Git read-only commands (`rev-parse`, `status --porcelain`, `ls-tree`) and direct byte copy. Validate source evidence/ledger through the existing validator before any write. Reject all unexpected repository state.

- [ ] **Step 4: Verify GREEN**

Run the dedicated pytest file plus existing dataset-lock adversarial tests. Expected: all pass.

---

### Task 2: Add failing tests for the operator receipt preparer

**Files:**
- Create: `tests/test_track_a_epoch_002_operator_dataset_lock_receipt_preparer.py`
- Later create: `scripts/prepare_track_a_epoch_002_operator_dataset_lock_receipt.py`

**Interfaces:**
- Consumes: existing canonical operator evidence paths; `_single_path_history`; `git_is_ancestor`; `expected_operator_receipt`; `validate_operator_receipt_object`; `canonical_json_bytes`.
- Produces: `prepare(write: bool = False, generated_at_utc: str | None = None) -> dict[str, Any]` and CLI PASS markers.

- [ ] **Step 1: Write failing tests**

Cover: missing admitted evidence; divergent evidence/ledger history; non-ancestor admission commit; pre-existing receipt; dirty repository; exact evidence hash binding; full schema/semantic validation; dry-run no-write; write creates only canonical receipt.

- [ ] **Step 2: Verify RED**

Run the dedicated pytest file on the test-only PR head. Expected: import/module failure because `prepare_track_a_epoch_002_operator_dataset_lock_receipt.py` does not exist.

- [ ] **Step 3: Implement minimal helper**

Derive unique shared admission commit from Git history, require first-and-only history for both files, hash canonical evidence bytes, generate UTC timestamp when not supplied, call the existing receipt constructor and validator, then optionally write exactly one file.

- [ ] **Step 4: Verify GREEN**

Run both new test files and existing dataset-lock test suite. Expected: all pass.

---

### Task 3: Integrate workflow and operator documentation

**Files:**
- Modify: `.github/workflows/track-a-epoch-002-dataset-lock.yml`
- Modify: `docs/experiment/TRACK_A_EPOCH_002_DATASET_LOCK_PROCEDURE.md`

**Interfaces:**
- Consumes: both new helpers/tests.
- Produces: path-triggered validation and a documented operator sequence from local PASS outputs to exact repository deltas.

- [ ] **Step 1: Extend workflow paths and tooling allowlist**

Add both helper scripts and both tests to pull-request path triggers and the tooling-only changed-path allowlist.

- [ ] **Step 2: Extend adversarial pytest command**

Run both new test files alongside existing dataset-lock tests.

- [ ] **Step 3: Extend secret/decryption-surface scan**

Include both helper source files in the source concatenation checked for private/blinding/decrypt/encrypt markers.

- [ ] **Step 4: Update procedure**

Document the two new dry-run/write commands after local retained-byte generation and after accepted two-file evidence admission. Explicitly state that helpers prepare deltas only and do not commit/merge or alter authority.

---

### Task 4: Exact-head review, verification, and guarded completion

**Files:**
- Review all changed files from Tasks 1–3.

- [ ] **Step 1: Open/refresh PR and inspect exact changed-file set**

Expected files: design + plan docs, two helpers, two tests, dataset-lock workflow, dataset-lock procedure.

- [ ] **Step 2: Run/request full exact-head CI**

Require every returned workflow on the final head to reach terminal SUCCESS. Earlier heads are historical only.

- [ ] **Step 3: Review for authority escalation and secret/decryption surfaces**

Confirm neither helper commits, pushes, mutates refs, decrypts, reads private keys/secrets, aggregates outcomes, or creates authorization/scientific-state transitions.

- [ ] **Step 4: Guarded merge only if exact-head green**

Use repository-supported merge method with expected-head discipline. If protection requires external approval, leave merge blocked rather than bypassing.

- [ ] **Step 5: Verify exact merged main push wave**

Record terminal post-merge push results and propagate the checkpoint to current mutable documentation only if merge actually occurs.
