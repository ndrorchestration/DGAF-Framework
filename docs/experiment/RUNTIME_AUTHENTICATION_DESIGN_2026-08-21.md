# Runtime Authentication Design

**Established:** 2026-08-21  
**Status:** DESIGN — NOT YET IMPLEMENTED  
**Step:** 7 of 28 (Gate 3: Engineering and Evidence Closure)

---

## Problem

Currently `run_pilot.py` performs gating via environment variable checks:

```python
def require_frozen_commit() -> None:
    frozen_sha = os.getenv("PDMAL_FROZEN_COMMIT_SHA")
    if not frozen_sha:
        raise RuntimeError("PDMAL_FROZEN_COMMIT_SHA not set")
    # ... validates against expected SHA

def require_pilot_authorization() -> None:
    if os.getenv("PDMAL_PILOT_AUTHORIZED") != "1":
        raise RuntimeError("PDMAL_PILOT_AUTHORIZED not set to 1")
```

These checks verify that env vars are set, but they do NOT cryptographically verify that the code being executed matches the authorized candidate. If someone modifies the code on disk (or checks out a different SHA) but sets the env vars, the gating functions would still pass.

This is a gap: the runner can be tricked into running unauthorized code if the env vars are set to match.

---

## What Runtime Authentication Needs

The runner must verify that **the code it is executing** matches **the authorized candidate SHA** before proceeding. This is a cryptographic binding between:

1. **The code on disk** (what is actually being executed)
2. **The authorized candidate** (what the freeze manifest and manifest say should be running)

The verification should happen at runner startup, before any experimental work begins.

---

## Approaches

### Approach A: Runner reads its own blob SHA

The runner computes its own SHA at startup and compares to the authorized candidate SHA:

```python
def verify_candidate_sha(expected_sha: str) -> None:
    """Verify that the runner's own code matches the expected candidate SHA."""
    runner_path = Path(__file__).resolve()
    actual_sha = subprocess.check_output(
        ["git", "ls-tree", "HEAD", str(runner_path)],
        text=True
    ).split()[2]  # blob SHA
    if actual_sha != expected_sha:
        raise RuntimeError(
            f"Runner SHA mismatch: actual={actual_sha}, expected={expected_sha}"
        )
```

**Pros:** Cryptographically binding. The runner verifies its own code.
**Cons:** Requires git to be available at runtime. Depends on HEAD being the candidate (not a different checkout). If the repo is in a dirty state, the SHA check may be ambiguous.

### Approach B: Wrapper script verifies SHA before invoking runner

A separate wrapper script computes the SHA of all candidate components and compares to the manifest before invoking the runner:

```bash
#!/bin/bash
# verify-and-run.sh
EXPECTED_SHA=$(jq -r '.candidate_identity.candidate_sha' CANDIDATE_MANIFEST_2026-08-21.json)
ACTUAL_SHA=$(git rev-parse HEAD)
if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
    echo "ERROR: Candidate SHA mismatch. Expected $EXPECTED_SHA, got $ACTUAL_SHA"
    exit 1
fi
# Also verify key component SHAs...
exec python experiments/pdmal_pilot/run_pilot.py "$@"
```

**Pros:** Separates verification from execution. Can verify all components, not just the runner. Does not require git inside the Python runner.
**Cons:** Adds a shell dependency. The wrapper itself could be subverted if not protected.

### Approach C: Embed candidate SHA in the runner

The expected candidate SHA is embedded in the runner code itself (or in a companion file that is part of the candidate):

```python
EXPECTED_CANDIDATE_SHA = "94fb6fdff64f2919d35938c5b1cb506625cf1139"

def verify_self() -> None:
    # Verify runner's own SHA against embedded expectation
    ...
```

**Pros:** No external dependency. The runner carries its own expectation.
**Cons:** If the code is modified, the embedded SHA is also wrong (unless the modification also updates the embedded SHA, which would be detectable by comparing to the manifest).

---

## Recommended Approach

**Approach B (wrapper script) with Approach A (self-verification) as a secondary check.**

The wrapper script is the primary gate: it verifies all candidate components against the manifest before invoking the runner. The runner also performs a secondary self-check for defense in depth.

This provides:
1. **Cryptographic binding** — the code is verified against a specific SHA, not just env vars.
2. **Component-level verification** — all candidate components (runner, schemas, configs) are verified, not just the runner.
3. **Defense in depth** — even if the wrapper is bypassed, the runner's self-check provides a secondary gate.

---

## What This Prevents

1. **Running modified code with correct env vars.** If someone changes the code but keeps the env vars set, the SHA check fails.
2. **Running code from the wrong branch.** If someone checks out a different branch but keeps the env vars, the SHA check fails.
3. **Silent code substitution.** The cryptographic binding makes it detectable if the code doesn't match the manifest.

---

## Gap from PR #77

PR #77 provides:
- `require_frozen_commit()` — checks env var, NOT cryptographic
- `require_pilot_authorization()` — checks env var, NOT cryptographic
- `blind_condition()` — blinding function, NOT authentication

PR #77 does NOT provide:
- SHA verification of the runner or any component
- A wrapper script that verifies the candidate before running
- Any cryptographic binding between the code and the authorized candidate

This is a **missing control** that must be added before the candidate can be considered authenticated at runtime.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This is a design document for a control that does NOT yet exist. It does NOT describe an implemented or tested mechanism.
