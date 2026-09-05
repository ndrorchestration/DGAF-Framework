# Issue #270 — Current-Lineage Quality Regression

**Last updated:** 2026-09-05  
**Status:** OPEN / MYPY TRANCHE CLOSED / FORMATTING + IMPORT + STYLE DEBT REMAINS

## Why this issue exists

Issue #47 remains a valid historical exact-tree closure for commit `e46ffb3913794b506bf413e837fcf5be99d8f426`. It does not certify every later tree.

A later Python Tests & Quality Checks execution associated with PR #269 exposed formatting/import/type diagnostics on the current lineage. Those findings are tracked here rather than retroactively rewriting the historical #47 result.

## Current evidence boundary

Current protected `main`: `0c7b83558c2677f73fd71ad8bfa2a9b265b87965`  
Current `main` tree: `892e65b7e354bcb1eb6e9ddfdfed77faa6ca68b5`  
PR #272 exact head: `198669c2574b37f6e83cd9544ec172ecd0ee64f1`  
PR #272 merge: `0c7b83558c2677f73fd71ad8bfa2a9b265b87965`  
Python Tests & Quality Checks run: `33965667752`

PR #272 passed all **15/15 returned exact-head workflows** before merge.

## Mypy tranche — CLOSED / CLEAN

The earlier current-lineage baseline run `33957199893` reported six mypy errors in four component files:

- `components/KAPPA/dynamic_weight_router.py`
- `components/ensemble_v17.py`
- `components/ensemble_v16.py`
- `components/ahg_herald_trace.py`

PR #272 repaired those six findings with narrow type/runtime checks only. It did not add mypy exclusions for the findings, weaken the workflow, or perform an unrelated formatting sweep.

Direct logs from run `33965667752` establish the result independently of the workflow's advisory-success semantics:

- Python 3.10: `Success: no issues found in 12 source files`
- Python 3.11: `Success: no issues found in 12 source files`
- Python 3.12: `Success: no issues found in 12 source files`
- command: `mypy components/ --ignore-missing-imports --no-implicit-optional`

Blocking pytest remained green. Python 3.10 and Python 3.12 each recorded **190 passed / 4 skipped**; the Python 3.11 job also completed successfully. The broader exact-head governance, regression, truth/evidence, PDMAL harness, and pre-freeze workflows also passed before merge.

Codecov delivery encountered an external HTTP 429 rate limit in the Python jobs. The action is configured non-blocking and repository coverage artifacts were still uploaded. This record therefore does **not** claim that the Codecov upload succeeded.

## Remaining current-lineage debt

The workflow still marks Black, isort, mypy, and broad lint diagnostics `continue-on-error: true`. Workflow-level SUCCESS therefore must not be described as proof that all quality diagnostics are clean.

### Black — OPEN

`black --check components/ tests/ --line-length=120` still reports **28 files would be reformatted** on the #272 exact head.

### isort — OPEN

`isort --check-only components/ tests/ --profile=black` still reports import-order failures across current-lineage component and test files.

### Broad flake8 diagnostics — OPEN

The broad diagnostic invocation still reports **224 style findings** on the #272 exact head. The blocking fatal subset remains clean:

`flake8 components --count --select=E9,F63,F82 --show-source --statistics` → `0`

The remaining style findings must not be conflated with the now-clean mypy tranche.

## Required remediation sequence

1. Mechanically normalize Black/isort scope without mixing in semantic refactors.
2. Re-run Black/isort/mypy and the supported pytest/security/regression suites against the exact normalization head.
3. Reassess broad flake8 findings after Black/isort normalization and repair residual findings in a separate bounded tranche if needed.
4. Preserve exact-run diagnostics and provenance.
5. Only after a clean intended baseline exists, remove `continue-on-error` from the quality checks intended to be blocking.
6. Verify the newly blocking checks actually fail closed under a controlled negative regression or equivalent deterministic test.
7. Keep current-facing documentation explicit about advisory-vs-blocking semantics until that transition is verified.

## Acceptance criteria

- [ ] `black --check components/ tests/ --line-length=120` exits 0.
- [ ] `isort --check-only components/ tests/ --profile=black` exits 0.
- [x] `mypy components/ --ignore-missing-imports --no-implicit-optional` exits 0 across Python 3.10/3.11/3.12 on PR #272 exact head.
- [ ] intended quality steps are blocking after clean-baseline verification.
- [x] full pytest/security/regression suites remained green for the mypy tranche.

## Scientific boundary

This is engineering-quality work only. It does not alter PDMAL candidate identity, P1–P9 scientific status, freeze, authorization, blinding/unblinding, empirical execution, or empirical N.

**PDMAL remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
