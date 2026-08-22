# CI Workflow Analysis: pdmal-preauth-security.yml

**Analyzed:** 2026-08-21  
**Workflow blob SHA:** `9cff92a5c05703dbae636fb4b091ea89906cbcb0` (at PR #77, `4983f44a`)  
**Status:** ANALYSIS COMPLETE — WORKFLOW EXISTS BUT NOT EXECUTED

---

## Workflow Structure

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

## What the Workflow CAN Verify

### 1. Code presence
The workflow checks out the code and runs tests. If the code files don't exist, `pytest` fails. This verifies that the required files are present in the checked-out commit.

### 2. Python environment
The workflow uses Python 3.12.0 (matching the candidate's environment specification). The lockfile is installed with `--require-hashes`, ensuring dependency integrity.

### 3. Test execution
The workflow runs `pytest` with verbose output. If the tests fail, the workflow fails. This verifies that the test code runs and passes against the checked-out source code.

### 4. Schema validation correctness
`test_artifact_schema.py` tests that `validate_artifact()` and related functions behave correctly. This verifies that the schema validation code is correct in isolation.

### 5. Security control existence
`test_security_controls.py` tests that `require_frozen_commit()`, `require_pilot_authorization()`, `blind_condition()`, and related functions exist and behave as expected under monkeypatching.

### 6. Dependency integrity
`--require-hashes` ensures that the installed packages match the locked hashes. If the lockfile is tampered with, the install fails.

---

## What the Workflow CANNOT Verify

### 1. Actual artifact validity
The workflow runs tests on the source code, not on actual artifacts produced by a runner execution. It verifies that the validation code works, but not that actual artifacts pass validation. This is a structural limitation: CI tests code, not artifacts.

### 2. SHA computation consistency
The workflow does not compare `run_pilot.py`'s SHA computation (`json.dumps` + `hashlib.sha256`) with `pilot_artifact_schema.py`'s `canonical_json_bytes()`. Both methods exist in the code, but their equivalence is not tested by the CI.

### 3. Inline validation
The workflow does not verify that `run_pilot.py` actually calls `validate_artifact()` or `verify_sidecar()` after writing artifacts. The test files test those functions in isolation, but the runner's use of them is not tested.

### 4. Env var state
The workflow sets `PYTHONPATH` but does not set `PDMAL_FROZEN_COMMIT_SHA` or `PDMAL_PILOT_AUTHORIZED`. The adversarial tests use monkeypatching to simulate env var behavior, but the actual env var state in a real runner environment is not verified.

### 5. Blinding key custody
The workflow does not verify that a blinding key exists, is supplied correctly, or is custodied properly. The blinding function is tested in isolation, but the key supply mechanism is not part of the CI.

### 6. Runtime authenticiation
The workflow does not verify that the runner performs SHA-based runtime authentication. The gating functions are tested, but the cryptographic binding between the running code and the authorized candidate is not tested.

### 7. CI execution status
Most fundamentally: the workflow has NOT been executed. No CI run results exist. The workflow code is present (blob `9cff92a5`), but there is no evidence that it has ever run and passed.

---

## The CI-Validates-Validator Distinction

This is the core epistemic limitation of CI for this system:

```
CI validates the VALIDATOR (the code that will validate artifacts).
Separate audit validates the ARTIFACTS (the output of the runner).
```

The CI workflow (`pdmal-preauth-security.yml`) does the first. It does not do the second.

This is not a bug — it's a design distinction from `independent_verification_design.json`:
- **CI-appropriate checks (10 items):** Deterministic code invariants — schema validation correctness, security control existence, dependency integrity, etc.
- **Separate-audit checks (12 items):** Evidence-level verification — actual artifact validation, sidecar verification, runtime_seconds check, blinded ID recomputation, fingerprint consistency, etc.

The CI can close the CI-appropriate checks. The separate audit must close the separate-audit checks. Neither can substitute for the other.

---

## False-Green Risks (Detailed)

See `FALSE_GREEN_CI_ANALYSIS_2026-08-21.md` for the full analysis. Summary:

| Risk | Severity |
|---|---|
| Workflow never executed | HIGH |
| Tests validator, not artifacts | HIGH |
| Tests PR code, not candidate | MEDIUM |
| Empty test file passes | MEDIUM |
| Push to main tests new code | LOW-MEDIUM |
| Dependency drift | LOW |

---

## Recommended CI Improvements

1. **Trigger the workflow** against the candidate SHA and record the run.
2. **Pin to candidate SHA** in the workflow (checkout the candidate tag, not the PR merge).
3. **Record the SHA** being tested in the workflow output.
4. **Add content verification** for critical test files.
5. **Add lockfile SHA verification** in the workflow.
6. **Document that CI cannot close artifact-level checks** — this is a separate audit responsibility.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This analysis examines the CI workflow code. It does NOT describe a CI execution that has occurred. No CI run has been performed (N=0).
