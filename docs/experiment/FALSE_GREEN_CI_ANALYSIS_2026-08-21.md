# False-Green CI Analysis

**Established:** 2026-08-21  
**Status:** ANALYSIS — NOT YET RESOLVED  
**Step:** 11 of 28 (Gate 3: Engineering and Evidence Closure)

---

## What "False-Green" Means

A CI workflow is **false-green** when it reports success (green) despite a required validation being absent, skipped, disconnected, or operating against the wrong artifact.

The desired property:

```
missing verification
       ↓
FAIL
```

The false-green property:

```
missing verification
       ↓
nothing happened (or test passed vacuously)
       ↓
GREEN
```

False-green is worse than red because it creates confidence where none is warranted.

---

## Current CI Workflow: `pdmal-preauth-security.yml`

From the file at PR #77 (`9cff92a5c05703dbae636fb4b091ea89906cbcb0`):

```yaml
name: PDMAL Pre-Authorization Security
on:
  pull_request:
    paths:
      - 'experiments/pdmal_pilot/**'
      - 'docs/experiment/**'
      - '.github/workflows/pdmal-preauth-security.yml'
  push:
    branches: [main]
    paths:
      - 'experiments/pdmal_pilot/**'
      - 'docs/experiment/**'
      - '.github/workflows/pdmal-preauth-security.yml'

jobs:
  security-and-schema:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12.0'
      - name: Install locked dependencies
        run: python -m pip install --require-hashes -r experiments/pdmal_pilot/requirements-full-lock.txt
      - name: Run adversarial controls
        env:
          PYTHONPATH: experiments/pdmal_pilot
        run: python -m pytest experiments/pdmal_pilot/test_security_controls.py -v
      - name: Run artifact schema tests
        env:
          PYTHONPATH: experiments/pdmal_pilot
        run: python -m pytest experiments/pdmal_pilot/test_artifact_schema.py -v
```

---

## False-Green Risks in the Current Workflow

### Risk 1: Workflow exists but has never been executed

**Problem:** The workflow file exists (blob `9cff92a5`), the test files exist (blobs `ddc59571`, etc.), but there is no evidence that the workflow has ever run. The absence of a CI run is not evidence of failure — but it's also not evidence of success.

**False-green mechanism:** If someone claims "the CI passes" without having triggered it, that claim is unsupported. If the CI hasn't run, it can't have failed, so the lack of a failure is vacuously "green" — but that's not a real pass.

**Severity:** HIGH. This is the most basic false-green risk: the workflow hasn't been tried.

**Mitigation:** Trigger the workflow (manual dispatch or push) against the candidate SHA and record the run ID and result.

### Risk 2: Workflow tests the validator but not actual artifacts

**Problem:** `test_security_controls.py` and `test_artifact_schema.py` test that the validation code behaves correctly in isolation (unit tests). They do NOT test that actual artifacts produced by a real `run_pilot.py` execution pass validation.

**False-green mechanism:** The tests can pass (the code works in isolation) while the runner's actual artifact production is broken (e.g., SHA computation mismatch, missing fields, wrong format). The CI reports green, but the actual pilot artifacts would fail validation.

**Severity:** HIGH. This is the gap between "the validator works" and "the artifacts are valid."

**Mitigation:** This requires separate audit (IVD Layer 6/10) with actual artifacts, not just CI unit tests. The CI can't close this gap by design — it's a structural limitation, not a bug.

### Risk 3: Workflow runs on pull_request paths — tests whatever is in the PR

**Problem:** The workflow triggers on `pull_request` with path filters. When a PR is opened or updated, the workflow tests whatever code is in that PR. It does NOT pin to a specific candidate SHA.

**False-green mechanism:** If the PR contains code that passes the tests but is NOT the intended candidate (e.g., a different implementation that happens to pass the same tests), the CI reports green for the wrong code. The green is real (the tests passed) but attributed to the wrong artifact.

**Severity:** MEDIUM. This is the "wrong artifact" false-green risk.

**Mitigation:** Bind the workflow to the candidate SHA (checkout the candidate tag/branch, not the PR merge commit). See `P2_CANDIDATE_BINDING_SPEC_2026-08-21.md`.

### Risk 4: Workflow can pass even if a required test file is missing

**Problem:** The workflow runs `pytest experiments/pdmal_pilot/test_security_controls.py`. If that file doesn't exist, `pytest` returns a non-zero exit code (file not found). But if someone renames the file to `test_security_controls_old.py` and creates a new `test_security_controls.py` that's empty or trivial, the workflow still "passes" — the test suite runs and exits 0.

**False-green mechanism:** A superficial test file that exists and exits 0 satisfies the workflow, even if the actual adversarial tests are gone. The workflow tests for the presence of a passing test, not the presence of the intended test content.

**Severity:** MEDIUM. This requires deliberate subversion, but the workflow doesn't defend against it.

**Mitigation:** Add content checks: verify that the test file contains expected test functions, or pin to a specific test file SHA.

### Risk 5: Workflow runs on push to main — tests whatever is on main

**Problem:** The workflow also triggers on `push` to `main` with the same path filters. After PR #77 is merged, the push trigger fires and tests whatever is now on `main`. If subsequent commits change the code, the next push trigger tests the new code.

**False-green mechanism:** The green run from the PR merge doesn't persist. Each push gets a new run. If someone pushes a change that breaks the tests, the next run is red. But if the change is subtle enough to pass the tests while breaking the actual security properties, the run is green but misleading.

**Severity:** LOW-MEDIUM. This is inherent to any CI that runs on push — it's a feature (tests stay current) but also a risk (tests can be gamed if they're not comprehensive).

**Mitigation:** This is addressed by comprehensive test coverage (which is a separate concern) and by the separate audit path (which verifies actual artifacts, not just code).

### Risk 6: Dependencies can drift

**Problem:** The workflow installs from `requirements-full-lock.txt` (blob `3ac4bd28`). If that lockfile is updated (newer package versions), the workflow tests against different dependencies than the candidate was designed for.

**False-green mechanism:** If a dependency update changes behavior in a way that makes the tests pass (e.g., a bug fix in a dependency that masks a bug in the application code), the CI reports green for code that would fail with the original dependencies.

**Severity:** LOW. The lockfile is hash-pinned, so `pip install --require-hashes` would fail if the lockfile is tampered with. But if the lockfile is legitimately updated, the drift is real.

**Mitigation:** Pin the lockfile SHA in the candidate manifest. The workflow should verify that the lockfile matches the pinned SHA before installing.

---

## Recommended Fixes

### Fix 1: Require explicit workflow runs before claiming verification

```
Claim: "P2 is verified."
Required evidence:
  - Workflow run ID: ___________
  - Workflow run URL: ___________
  - Candidate SHA tested: ___________
  - Result: PASS/FAIL
  - Timestamp: ___________
```

No verbal claim substitutes for the run record.

### Fix 2: Pin the candidate SHA in the workflow

```
- name: Checkout candidate
  uses: actions/checkout@v5
  with:
    ref: pdmal-candidate-2026-08-21  # tag, not PR merge
```

This ensures the workflow tests the candidate, not whatever is in a PR.

### Fix 3: Record the SHA being tested

```
- name: Record candidate SHA
  run: echo "CANDIDATE_SHA=$(git rev-parse HEAD)" >> $GITHUB_ENV
```

This makes the run attributable to a specific SHA.

### Fix 4: Add failure-if-missing semantics

If a required test file doesn't exist, the workflow should fail:

```
- name: Verify test files exist
  run: |
    test -f experiments/pdmal_pilot/test_security_controls.py ||
      { echo "test_security_controls.py MISSING"; exit 1; }
    test -f experiments/pdmal_pilot/test_artifact_schema.py ||
      { echo "test_artifact_schema.py MISSING"; exit 1; }
```

### Fix 5: Add content checks for critical test files

```
- name: Verify test_security_controls has adversarial tests
  run: |
    grep -q "def test_" experiments/pdmal_pilot/test_security_controls.py ||
      { echo "No test functions found"; exit 1; }
    grep -q "monkeypatch\|mock\|patch" experiments/pdmal_pilot/test_security_controls.py ||
      { echo "No mocking detected — adversarial tests may be missing"; exit 1; }
```

This is a basic check. More sophisticated content verification would require parsing the test file's AST.

### Fix 6: Pin the lockfile SHA

```
- name: Verify lockfile
  run: |
    EXPECTED_LOCKFILE_SHA="3ac4bd2851864af3a5a5ddb8ef707c26e7e81200"
    ACTUAL_LOCKFILE_SHA=$(git ls-tree HEAD experiments/pdmal_pilot/requirements-full-lock.txt | awk '{print $3}')
    if [ "$ACTUAL_LOCKFILE_SHA" != "$EXPECTED_LOCKFILE_SHA" ]; then
      echo "Lockfile SHA mismatch: expected $EXPECTED_LOCKFILE_SHA, got $ACTUAL_LOCKFILE_SHA"
      exit 1
    fi
```

---

## The Fundamental Limitation

Even with all fixes applied, CI has a structural limitation:

**CI validates the code. It cannot validate the artifacts.**

The CI runs the test code against the source code. It verifies that:
- The test code is present and runs.
- The test code passes against the source code.

The CI does NOT verify that:
- Actual artifacts produced by a real runner run pass validation.
- The runner's SHA computation matches the schema's SHA computation.
- The env vars are set correctly in a real environment.
- The blinding key is supplied correctly.
- The artifacts are untampered.

These are **separate audit** concerns (IVD Layers 6, 8, 9, 10), not CI concerns.

This is the CI-vs-separate-audit distinction from `independent_verification_design.json`:
- **CI** validates the validator (the code that will validate artifacts).
- **Separate audit** validates the actual artifacts (the output of the runner).

Both are needed. Neither alone is sufficient.

---

## Summary of False-Green Risks

| Risk | Severity | Current State | Fix |
|---|---|---|---|
| 1. Workflow never executed | HIGH | Not executed | Trigger workflow, record run |
| 2. Tests validator, not artifacts | HIGH | Structural limitation | Separate audit (not CI fix) |
| 3. Tests PR code, not candidate | MEDIUM | Runs on pull_request | Pin to candidate SHA |
| 4. Empty test file passes | MEDIUM | No content check | Add content verification |
| 5. Push to main tests new code | LOW-MEDIUM | Inherent to push trigger | Comprehensive tests + separate audit |
| 6. Dependency drift | LOW | Lockfile hash-pinned | Pin lockfile SHA in manifest |

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This analysis identifies risks in the CI workflow design. It does NOT describe a CI that has been executed or verified. No CI run has occurred (N=0).
