# Issue #270 — Current-Lineage Quality Regression

**Last updated:** 2026-09-05  
**Status:** OPEN / CURRENT-LINEAGE QUALITY REGRESSION

## Why this issue exists

Issue #47 remains a valid historical exact-tree closure for commit `e46ffb3913794b506bf413e837fcf5be99d8f426`. It does not certify every later tree.

A later Python Tests & Quality Checks execution associated with PR #269 exposed formatting/import/type diagnostics on the current lineage. Those findings are tracked here rather than retroactively rewriting the historical #47 result.

## Evidence boundary

PR #269 exact head: `d6b6fb640e6d310ff31c4a31d08541821824c412`  
Merged `main`: `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`  
Python Tests & Quality Checks run: `33957199893`

### Blocking test result

Pytest remained blocking and passed across the supported Python matrix.

Python 3.12 recorded:

- 190 passed
- 4 skipped
- all seven new `tests/test_audit_hallucination_rate.py` regressions collected and passed

Python 3.10 and 3.11 test jobs also completed successfully.

### Advisory diagnostics

The workflow currently marks Black, isort, mypy, and broad lint steps `continue-on-error: true`.

Therefore the workflow can conclude SUCCESS while these diagnostics report debt. Workflow SUCCESS must not be described as a clean formatting/type baseline.

#### Black

`black --check components/ tests/ --line-length=120` reported 28 files that would be reformatted on the PR execution.

#### isort

`isort --check-only components/ tests/ --profile=black` reported multiple import-order failures.

#### mypy

`mypy components/ --ignore-missing-imports --no-implicit-optional` reported six errors in four component files:

- `components/KAPPA/dynamic_weight_router.py`
- `components/ensemble_v17.py`
- `components/ensemble_v16.py`
- `components/ahg_herald_trace.py`

The component-level mypy failures predate PR #269 and remain later-lineage debt.

## Required remediation sequence

1. Mechanically normalize Black/isort scope without mixing in semantic refactors.
2. Fix the six mypy errors or explicitly machine-scope any intentional exclusions with documented justification.
3. Re-run the supported Python matrix and the broader regression/security workflows.
4. Preserve exact-run diagnostics and provenance.
5. Only after a clean baseline exists, remove `continue-on-error` from the intended blocking quality checks.
6. Verify that CI then fails closed when those checks regress.

## Acceptance criteria

- `black --check components/ tests/ --line-length=120` exits 0.
- `isort --check-only components/ tests/ --profile=black` exits 0.
- `mypy components/ --ignore-missing-imports --no-implicit-optional` exits 0, or every intentional exclusion is explicit and machine-configured.
- intended quality steps are blocking after clean-baseline verification.
- full pytest/security/regression suites remain green.

## Scientific boundary

This is engineering-quality work only. It does not alter PDMAL candidate identity, freeze, authorization, blinding/unblinding, empirical execution, or empirical N.

**PDMAL remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
