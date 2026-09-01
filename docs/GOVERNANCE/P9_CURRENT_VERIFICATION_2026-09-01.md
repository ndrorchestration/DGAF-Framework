# P9 Current Verification — 2026-09-01

**Status:** SCOPED PASS / BROADER CLOSURE OPEN
**Run:** `33572123857`
**Workflow:** `P9 Independent Verification`
**Candidate:** `a43219b4ed91fff8615f6c655ab3d17ca871fc29`
**Branch:** `completion/2026-09-01-exact-candidate`
**Artifact:** `9825316781`
**Artifact ZIP digest:** `sha256:15e5ba72dd524f90b0bb3499c9b0b3f7de602f0e1905b0734183e830c22af671`

## Verified

- Exact candidate checkout: `git rev-parse HEAD == GITHUB_SHA`.
- Independent canonicalization: `jq -S -c`.
- Independent hash: `sha256sum`.
- Independent digest matched the DGAF/Python-produced deterministic-case digest:
  `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.
- Exact-candidate authority regression: `pytest -q tests/test_agent_authority_matrix.py` → `4 passed`.
- Independent evidence JSON and SHA-256 sidecar were uploaded with `if-no-files-found: error`.
- The evidence payload records `authorization_is_external=true` and `empirical_execution_requested=false`.

## Independence boundary

This run establishes independence of the canonicalization/hash method from the DGAF/Python path through the separate `jq -S -c` + `sha256sum` implementation. It does not make the GitHub Actions platform an independent execution substrate; both the candidate verification and artifact retention still execute within GitHub Actions.

## Anti-transfer rule

The successful earlier P9 run `33567199896` is scoped to superseded candidate `562753b…`. This run supersedes it only for the new candidate `a43219b…`; neither result transfers to mainline runtime candidate `92ff830b…` or any future candidate.

## Remaining closure boundary

This P9 result does not by itself establish:

- current-candidate P2/P6a production runtime evidence for `a43219b…`;
- complete P3/P4/P5/P6 evidence-chain closure;
- final P7 scientific/freeze binding;
- complete P8 closure;
- external durable archive beyond GitHub Actions artifacts;
- immutable freeze;
- pilot authorization;
- empirical execution or efficacy.

**Disposition:** `P9 scoped independent verification = PASS`; `broader P9 closure = OPEN`.

**Hard boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
