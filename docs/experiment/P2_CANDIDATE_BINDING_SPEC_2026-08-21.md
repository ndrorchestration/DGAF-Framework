# P2 Candidate Binding Specification

**Established:** 2026-08-21  
**Status:** SPECIFICATION — NOT YET IMPLEMENTED

---

## What P2 Must Verify

P2 (Execution Contract) verifies that the gating functions, security controls, and schema validation exist and are correctly structured. It does NOT verify that they work correctly in an actual run — that requires execution evidence (CI or separate audit).

For P2 to close against this candidate, the verification must establish:

```
P2 result
    ↓
candidate SHA (94fb6fd / b25a914c)
    ↓
candidate manifest (CANDIDATE_MANIFEST_2026-08-21.json)
```

This prevents a green test from being incorrectly attributed to the experimental artifact if the test was actually run against a different code state.

---

## What P2 Currently Requires (from PDM_CURRENT_CONTROL_STATE.md gate board)

From `PDMAL_CURRENT_CONTROL_STATE.md` at PR #77 (`8f763eb8`):

| Gate | Status | What it checks |
|---|---|---|
| Protocol freeze | BLOCKED | All required controls closed |
| Pilot authorization | NOT GRANTED | Explicit post-freeze authorization |
| Empirical data | 0 | No empirical execution authorized |
| Blinding custody | OPEN | Synthetic dry-run only |
| Long-term retention | OPEN | Archive not established |
| Freeze packet | PENDING | Dependent on blinding and retention closure |

---

## How P2 Binds to the Candidate

### Current state (NO binding)

The `pdmal-preauth-security.yml` workflow runs on:
- `pull_request` paths: `experiments/pdmal_pilot/**`, `docs/experiment/**`, `.github/workflows/pdmal-preauth-security.yml`
- `push` to `main` paths: same

This means:
- When a PR is opened, the workflow tests whatever code is in the PR.
- When code is pushed to `main`, the workflow tests whatever is on `main`.
- The workflow does NOT pin to a specific candidate SHA.

This is **not P2 bound to the candidate.** It tests "whatever happens to be in the PR" or "whatever is on main."

### What binding requires

P2 bound to the candidate means:

1. **The CI workflow checks out the candidate SHA**, not the PR merge commit or `main`.
2. **The workflow records which SHA it ran against** in its output (visible in the run log).
3. **The P2 result is attributed to that specific SHA**, not to "the PR" or "main."
4. **A reviewer can verify** that the SHA the CI ran against matches the candidate manifest.

### Recommended binding mechanism

```
# In the CI workflow, before running tests:
- name: Checkout candidate
  uses: actions/checkout@v4
  with:
    ref: pdmal-candidate-2026-08-21  # or the specific SHA

# Record the SHA being tested:
- name: Record candidate SHA
  run: echo "CANDIDATE_SHA=$(git rev-parse HEAD)" >> $GITHUB_ENV

# Then run tests against that exact checkout:
- name: Run security controls
  run: python -m pytest experiments/pdmal_pilot/test_security_controls.py
- name: Run artifact schema tests
  run: python -m pytest experiments/pdmal_pilot/test_artifact_schema.py
```

This binds P2 to the candidate because:
- The tests run against the exact candidate checkout.
- The `CANDIDATE_SHA` environment variable records which SHA was tested.
- A reviewer can match the SHA in the CI output to the candidate manifest.

---

## What P2 Does NOT Verify

Even with binding, P2 does NOT verify:

1. **Actual artifact validity** — P2 checks that the schema validation code exists, not that actual artifacts pass validation.
2. **SHA computation consistency** — P2 does not verify that `run_pilot.py`'s SHA computation matches `pilot_artifact_schema.py`'s `canonical_json_bytes()`.
3. **Inline validation** — P2 checks that validation functions exist, not that they are called inline by the runner.
4. **Empirical results** — P2 is about the apparatus, not about experimental outcomes.
5. **Primary contrast** — P2 does not adjudicate which contrast is the scientific question.
6. **Blinding key custody** — P2 checks that blinding functions exist, not that the key custody chain is established.
7. **CI execution status** — P2 checks code presence, not whether CI has actually run and passed.

---

## The Gap: CI Not Executed

The most important gap in P2 right now:

**`pdmal-preauth-security.yml` exists but has NOT been executed.**

No CI run results are available. The workflow code exists (blob `9cff92a5`), the test files exist (blobs `ddc59571` and others), but there is no evidence that the workflow has actually run and passed.

This means:
- P2 is IMPLEMENTED (code exists) but NOT VERIFIED (no execution evidence).
- The PRE_AUTHORIZATION_RECORD correctly states "Corrected apparatus verified: NO."
- A verbal claim that "the CI passes" would be unsupported.

To close P2, the workflow must be executed and the results must be recorded. This can happen either:
- Via a manual workflow dispatch against the candidate SHA, or
- Via a PR merge (if the candidate is merged to main and the push trigger fires)

---

## What the 6 Adversarial Tests Cover (from test_security_controls.py)

From `test_security_controls.py` at PR #77 (`ddc59571`):

1. **Env var gating** — tests that `require_frozen_commit()` and `require_pilot_authorization()` fail when env vars are not set (monkeypatching).
2. **Blind condition** — tests that `blind_condition()` produces consistent blinded IDs.
3. **Schema validation** — tests that `validate_artifact()` rejects invalid records.
4. **Sidecar verification** — tests that `verify_sidecar()` detects mismatches.
5. **Runtime ceiling** — tests that `validate_seed_runtime()` enforces the ceiling.
6. **Failure semantics** — tests that failure/recovery states are correctly classified.

These tests verify that the **code exists and behaves correctly in isolation.** They do NOT verify that the runner actually uses these functions in an integrated run, or that the env vars are set correctly in a real environment.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This specification describes how P2 SHOULD bind to the candidate. It does NOT describe a binding that exists today. P2 is currently NOT bound to the candidate — the CI runs on pull_request/push paths, not pinned to a specific SHA.

The specification is a design document, not evidence of compliance.
