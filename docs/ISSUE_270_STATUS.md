# Issue #270 — Current-Lineage Quality Regression

**Last updated:** 2026-09-05  
**Status:** VERIFIED / CURRENT-LINEAGE QUALITY REGRESSION CLOSED AT WORKFLOW LEVEL

## Why this issue exists

Issue #47 remains a valid historical exact-tree closure for commit `e46ffb3913794b506bf413e837fcf5be99d8f426`. It does not certify every later tree.

A later Python Tests & Quality Checks execution associated with PR #269 exposed current-lineage type, formatting, import-order, and lint diagnostics. Issue #270 tracked those later findings without rewriting the historical #47 result.

## Final verified boundary

Current protected `main`: `7ecc2578ca636fceca49504e0ee40de9a5213bd6`  
Current `main` tree: `a33ec18e4d2ebba607e18c8b537d2597c8e82bc3`  
Final workflow-hardening PR: #276  
PR #276 exact head: `151239e9131ebbf0f2dc2a5382553b3bec12e44e`  
PR #276 merge: `7ecc2578ca636fceca49504e0ee40de9a5213bd6`  
Exact-head Python run: `33974534482`  
Main push Python run: `33974834700`

PR #276 passed all **15/15 exact-head workflows** before merge. The main push Python run `33974834700` also completed successfully against merge SHA `7ecc2578…`.

## Remediation history

### Mypy — CLOSED

PR #272 repaired six current-lineage mypy findings with narrow type/runtime corrections and no suppressions for those findings.

Direct matrix evidence established:

- Python 3.10: `Success: no issues found in 12 source files`
- Python 3.11: `Success: no issues found in 12 source files`
- Python 3.12: `Success: no issues found in 12 source files`

### Black / isort — CLOSED

PR #274 mechanically normalized the current Python scope with the pinned toolchain:

- Black `26.5.1`
- isort `8.0.1`

The formatter/import tranche was verified independently before merge and did not rotate any PDMAL scientific identity.

### Broad flake8 — CLOSED

PR #275 repaired the remaining seven concrete lint findings and introduced a minimal root `.flake8` configuration:

```ini
[flake8]
max-line-length = 120
# E203 conflicts with Black-formatted slice syntax.
extend-ignore = E203
```

No other lint code was ignored or excluded. Normal PR CI reproduced fatal flake8 = `0`, broad flake8 = `0`, Black clean, isort clean, mypy clean, and pytest green.

### Fail-closed quality workflow — CLOSED

PR #276 converted the now-clean quality baseline from advisory diagnostics into fail-closed workflow gates:

- broad flake8 no longer uses `--exit-zero`;
- flake8, Black, isort, and mypy no longer use `continue-on-error: true`;
- `.flake8` is covered by both push and pull-request path filters;
- `.github/workflows/python-tests.yml` is covered by both push and pull-request path filters;
- Black remains blocking and emits `--diff` diagnostics on failure;
- deterministic Python 3.12 negative controls require flake8, Black, isort, and mypy each to reject a deliberate isolated violation;
- `tests/test_python_quality_gate_contract.py` locks the trigger and fail-closed semantics against silent regression.

Earlier #276 exact-head attempts failed at a real Black defect in the newly added contract test and skipped later quality stages. That is direct observed fail-closed behavior, not merely static configuration evidence.

## Final exact-head evidence

At PR #276 exact head `151239e9131ebbf0f2dc2a5382553b3bec12e44e`, Python Tests & Quality Checks run `33974534482` established:

- fatal flake8: `0`
- broad flake8: `0`
- Black `26.5.1`: `41 files would be left unchanged`
- isort `8.0.1`: success
- mypy `2.3.1`: `Success: no issues found in 12 source files`
- four workflow-contract tests: PASS
- pytest: **194 passed / 4 skipped / 7 warnings**
- negative controls: all four deliberate violations rejected
  - flake8: unused-import `F401`
  - Black: reformat required
  - isort: import-order failure
  - mypy: incompatible assignment
- diagnostic artifact ID: `9971918880`
- diagnostic ZIP SHA256: `2bd3ba3ada826bf851c1d71db1344ac12fd6f6ae65ad0de6c0971350c6a8a5f0`

The broader exact-head regression, governance, truth/evidence, IP hygiene, PDMAL harness, and PDMAL pre-freeze workflows also completed successfully before merge.

## Mainline reproduction

After merge, protected `main` at `7ecc2578…` triggered Python Tests & Quality Checks run `33974834700` by `push`.

That run completed successfully and reproduced the intended behavior:

- `test (3.10)` — SUCCESS
- `test (3.11)` — SUCCESS
- `test (3.12)` — SUCCESS
- Python 3.12 flake8 / Black / isort / mypy — SUCCESS
- Python 3.12 negative controls — SUCCESS
- pytest — SUCCESS
- `security-scan` — SUCCESS
- `staging-evidence` — SUCCESS
- `integration-tests` job — SUCCESS; no `tests/integration` suite existed at this boundary, so actual integration execution was explicitly detected as unavailable and skipped rather than represented as executed.

## External-service caveat

Codecov encountered HTTP 429 rate limiting during this remediation sequence. The Codecov action is explicitly non-blocking, and repository coverage artifacts were retained. This status therefore does **not** claim successful Codecov delivery where the external upload was rate-limited.

## Separate branch-protection control — OPEN AS #277

Workflow fail-closed behavior and repository merge enforcement are distinct controls.

At `main=7ecc2578…`, branch metadata reports `main` as protected but lists only `PPTL CI` as a required status context. The Python quality matrix is therefore **not currently established as a branch-protection-required merge check** by the available metadata.

The direct branch-protection endpoint returns `403 Resource not accessible by integration`, and the connected mutation surface does not expose branch-protection/ruleset writes.

Issue #277 separately tracks the repository-administration action to require the Python quality matrix (or an equivalent required-workflow policy) before merge and verify that configuration by readback.

This distinction does not reopen the code/workflow regression repaired by #270:

- current-lineage code quality baseline: **CLEAN / VERIFIED**
- workflow fail-closed behavior: **VERIFIED**
- branch-protection merge enforcement for Python quality: **OPEN / TRACKED BY #277**

## Acceptance criteria

- [x] `black --check components/ tests/ --line-length=120` exits 0 on the verified current lineage.
- [x] `isort --check-only components/ tests/ --profile=black` exits 0.
- [x] `mypy components/ --ignore-missing-imports --no-implicit-optional` exits 0 across Python 3.10/3.11/3.12.
- [x] fatal and broad flake8 baselines are clean under the explicit Black-compatible configuration.
- [x] flake8 / Black / isort / mypy are fail-closed inside the Python workflow.
- [x] broad flake8 no longer masks findings with `--exit-zero`.
- [x] `.flake8` and the workflow file itself are covered by push and pull-request triggers.
- [x] deterministic negative controls prove each intended quality tool rejects a controlled violation.
- [x] exact-head and mainline Python runs completed successfully after hardening.
- [x] repository-admin merge-enforcement gap separated into Issue #277 rather than misrepresented as complete.

## Scientific boundary

This remediation is engineering quality and repository workflow governance only. It does not alter PDMAL candidate identity, P1–P9 scientific status, freeze, pilot authorization, blinding/unblinding, empirical execution, or empirical N.

**PDMAL remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
