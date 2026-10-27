# CI dependency security candidate — cross-Python proof, 2026-10-27

**Status: UNVERIFIED SECURITY-REMEDIATION CANDIDATE. DO NOT PROMOTE LOCKS OR MERGE.**

## Scope and prerequisite

This isolated branch is based on existing `proof/black-26-10-1-locks-1477`, **not** on protected main or any signed bootstrap. It retains the previously reviewed direct `black==26.10.1` pin under [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477) and tests the other reported vulnerabilities under [#1530](https://github.com/ndrorchestration/DGAF-Framework/issues/1530). Only the `requirements-ci.txt` direct candidates change: `setuptools==83.0.0 -> 84.2.1` and `certifi==2026.10.19 -> 2026.10.23`, after PyPI source inspection. There is NO direct `filelock` pin in this file.

The source of authority for each candidate resolution remains the **existing hosted Ubuntu 24.04 x64 proof workflows**:
- `.github/workflows/ci-dependency-lock-generation-proof.yml` — Python 3.10, 3.11, 3.12 plus fixed 3.12 microversions;
- `.github/workflows/control-plane-pandas-lock-proof.yml` — Python 3.12, 3.12.0 and 3.12.3 with pandas 3.0.5 overlay.

Both run pip 26.2.1, generate a wheel-hash lock from the exact candidate source, upload manifest and freeze evidence, and verify the complete lock in an isolated environment. The only workflow change is an **additional non-waived, blocking `pip-audit --local` using that isolated verified environment after artifact upload**. The scan is allowed to fail; no advisory is ignored.

## Key compatibility hypothesis — may block Python 3.10

The advisory reported `filelock==4.0.3` with three CVEs and **fix >=4.2.1**. PyPI lists `filelock==4.2.1` and `4.2.4` as **Requires-Python >=3.11**; the Python 3.10-compatible `filelock==4.0.12` cannot be presumed safe, because it predates the reported fixed version. For Python 3.10, either a non-vulnerable compatible solution or dependency removal/isolation must be demonstrated in a proof artifact; **do not silently drop Python 3.10 or waive its advisory**. The hosted lock report will identify the actual resolved filelock version, its dependency ancestry and whether a complete set can pass a non-waived audit.

## Acceptance criteria, never inferred

1. The exact PR-head five-lane CI proof and three-lane control-plane proof produce reproducible source SHA-256, resolved-set SHA-256, lock-file SHA-256, package count, PyPI wheel hash, fresh venv `pip check`, and audit outcomes.
2. No unsupported Python interpreter, no fallback to an unsigned or unreviewed wheel, no hand-edited canonical `requirements-ci-py*.lock`, no modification of lock contract hashes without matching proof.
3. All four historical package advisories (Black, certifi, filelock, setuptools) and any newer findings must be rechecked for all intended lanes. A single failed lane means aggregate security admission remains **BLOCKED**.
4. Canonical promotion and signed admission are **separate** decisions requiring independent review; this draft is only candidate generation.

**Scientific/control state:** No human or external operator identity, scientific N, primary experiment, production runtime, protected main, release authorization or High Assurance change. `DGAF_V1_RELEASE=HOLD`, `SCIENTIFIC_N_INCREMENT=0`, `HIGH_ASSURANCE=NOT_AUTHORIZED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`.
