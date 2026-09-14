# Operator Repository Event Preparers Design

## Scope

Add two bounded, non-authorizing operator helpers that automate assembly of repository file deltas already defined and validated by the accepted Track A Epoch 002 dataset-lock contract.

The helpers do not change governance semantics, execute empirical work, inspect aggregate outcomes, decrypt protected mappings, authorize unblinding or analysis, commit, merge, or mutate Git refs.

## Helper 1: operator evidence-admission preparer

Create `scripts/prepare_track_a_epoch_002_operator_evidence_admission.py`.

Inputs default to the operator retention directory `$HOME/DGAF-Epoch002-Retention` and consume the already-produced non-secret files:

- `track_a_epoch_002_dataset_lock_evidence.json`
- `track_a_epoch_002_pre_lock_result_ledger.json`

Required behavior:

1. Require both source files to remain outside the repository.
2. Reuse `validate_track_a_epoch_002_dataset_lock.py` for evidence and pre-lock ledger validation.
3. Require the canonical repository destinations to be absent from `HEAD` and from the working tree before preparation.
4. Require the relevant dataset-lock tooling to be clean relative to `HEAD`.
5. In dry-run mode, validate inputs and report the exact two destination paths without writing.
6. In `--write` mode, copy exact source bytes into exactly:
   - `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json`
   - `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_PRE_LOCK_RESULT_LEDGER.json`
7. After writing, prove the repository delta is exactly those two untracked additions and no unrelated tracked or untracked change is present.
8. Refuse overwrite if either destination already exists.
9. Print a bounded PASS marker and the next explicit Git staging/commit command; do not execute it.

## Helper 2: operator dataset-lock receipt preparer

Create `scripts/prepare_track_a_epoch_002_operator_dataset_lock_receipt.py`.

This helper is usable only after the two-file evidence-admission event has been committed and the repository is otherwise clean.

Required behavior:

1. Require both canonical admitted evidence files to exist and pass the existing dataset-lock validators.
2. Derive their Git history and require both files to share one unique first-and-only admission commit.
3. Require that admission commit to be an ancestor of `HEAD`.
4. Require the canonical receipt path to be absent from `HEAD` and the working tree.
5. Require a clean repository before preparation.
6. Hash the admitted evidence manifest from repository bytes.
7. Build the receipt by calling the already-accepted `expected_operator_receipt(...)` constructor with the derived evidence-admission commit and current UTC timestamp.
8. Run full existing schema and semantic receipt validation before any write.
9. In `--write` mode, create exactly `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_DATASET_LOCK_RECEIPT.json`, then prove it is the only repository delta.
10. Print a bounded PASS marker and the next explicit Git staging/commit command; do not execute it.

## Fail-closed requirements

Both helpers are dry-run by default and must refuse:

- repository-local source evidence where external retained evidence is required;
- pre-existing canonical destinations;
- dirty or unrelated repository deltas;
- evidence/ledger validation failure;
- divergent or ambiguous evidence-admission histories;
- receipt generation before a committed evidence-admission event;
- overwrite of different bytes;
- any private-key, passphrase, decrypted-mapping, or blinding-secret handling.

## Test strategy

Follow TDD. Add failing tests before production code. Tests cover happy-path construction and fail-closed behavior, including dirty/unrelated worktree changes, existing destinations, divergent history, admission-commit drift, and premature receipt preparation.

The existing `Track A Epoch 002 Dataset Lock` workflow must include both helpers and both test files in its path trigger, adversarial pytest set, tooling-lane allowlist, and secret/decryption surface scan.

## Acceptance

The implementation PR is acceptable only if its exact final head completes the full returned validation wave successfully. Acceptance of these helpers changes operator ergonomics only; it does not itself admit retained evidence or establish dataset lock.