# Merge-Readiness Summary — PR #151 → NEW Candidate Designation

**Purpose:** make the two irreversible governance acts (merge PR #151; designate new candidate) one approval away.
This document is a proposal/staging aid. No merge, designation, freeze, or authorization is performed here.

**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.

---

## Verified live state (2026-08-30, `gh` + local clone)

|Item|Value|Source|
|---|---|---|
|PR #151 head|`83f93c6725672c8c1bf6e687e454403456ea8c21`|`gh pr view`|
|PR #151 tree|`eb40c67d9b06a171a8f6f01d2bfe482e54d5098e`|`git rev-parse HEAD^{tree}`|
|PR #151 state|OPEN · DRAFT · MERGEABLE|`gh pr view`|
|base `main`|`da1f9481e8b755d5540e699c5b7688d23c3c5c73`|`gh api branches/main`|
|Apparatus tests|78 passed (`experiments/pdmal_pilot/`)|local pytest|
|PPTL CI|required status check on `main` (protected)|repo policy|

## What PR #151 changes (apparatus, not docs-only)

- F1: required-but-unwired TGL gates → FAIL_CLOSED (kill `dgaf==simple` equivalence).
- F2: TGL turn index bound to semantic iteration.
- F3: governance audit/decision/outcome/seal propagated into pilot artifact + hashing.
- Plus R6 reconciliation record (`docs/experiment/CANDIDATE_RECONCILIATION_RECORD.md`) and designation template (`NEW_CANDIDATE_DESIGNATION_TEMPLATE.md`), committed `ebc1b3c` (pushed).

## Act 1 — Merge PR #151 (requires explicit go-ahead)

1. Confirm PPTL CI is green on `83f93c6` (governance CI currently running per prior report; verify before merge).
2. `gh pr merge 151 --squash` (or merge commit) onto `main` (`da1f948`).
3. Result: new `main` tip = post-#151 tree. Capture `git rev-parse HEAD` (post-merge) and `HEAD^{tree}`.

## Act 2 — Designate NEW candidate (requires explicit go-ahead, after Act 1)

1. Fill `NEW_CANDIDATE_DESIGNATION_TEMPLATE.md` with post-merge `new_candidate_sha` + `new_candidate_tree_sha`.
2. Write frozen `NEW_CANDIDATE_MANIFEST.md` on branch `experimental-candidate/<date>-post151`.
3. Commit + push (noreply identity `ndrorchestration@users.noreply.github.com`).
4. State stays PRE-FREEZE until independent P9 passes.

## Post-designation sequence (not yet authorized)

- Fresh candidate-scoped P2/P6a execution (current VERIFIED scope is `303f4424`, does NOT extend).
- Candidate-bound P3–P8 verification.
- Independent P9 pass.
- Freeze (separate, post-P9).
- Authorization → only then pilot. Empirical N stays 0 until then.

## Gate ledger (post-#151, pre-designation)

R1 ✓ R2 ✓ R3 ✓ R4 ✓ R5-plan ✓ R6 ✓ (remediated) · New candidate NOT DESIGNATED ·
P2/P6a VERIFIED (`303f4424` scope) · P3–P8 OPEN/FAIL-CLOSED · P9 NOT EXECUTED · Freeze NOT CREATED · N=0.
All 7 subject gates FAIL-CLOSED per `R1_R4_GATE_RECOVERY_MATRIX.md`.
