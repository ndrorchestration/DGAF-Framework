# P4-B Mode T Protected-Material Leakage Contract — 2026-09-06

## Status

Status: **STATIC/DYNAMIC SURFACE-GUARD EVIDENCE ONLY / NOT PROTECTED EXECUTION / NOT CUSTODY / NOT AUTHORIZATION**

Scientific boundary remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.

## Purpose

Issue #295 requires evidence that no protected mapping, key, nonce, or plaintext secret can appear in the continuity helper's ordinary observable surfaces: stdout, stderr, command-line arguments, environment variables, step outputs, job summaries, or uploaded artifacts.

This tranche converts the currently reviewed Mode-T helper and CI surface into a fail-closed contract. It does not use protected material. Instead, it constrains which data channels are permitted and fails whenever a future code/workflow change expands those channels without explicit review.

## Helper contract

`validate_mode_t_leakage_contract.py` requires the strict verifier to retain all of these properties:

- decryption occurs only through `tlock.New(network).Strict().Decrypt(...)`;
- stdout is constrained to the continuity report JSON encoder;
- stderr is constrained to the failure report JSON encoder;
- the report JSON-tag set is an exact allowlist of provenance, frozen-network identity, ciphertext/plaintext commitments, booleans, status, and empirical-state metadata;
- raw plaintext/mapping/private-key report fields are forbidden;
- the CLI flag set is an exact allowlist: endpoint, ciphertext path, expected plaintext SHA-256, evidence SHA, run ID, and run attempt;
- raw plaintext, mapping, key, nonce, secret, password, or passphrase CLI inputs are forbidden;
- direct environment-variable input from the verifier is forbidden;
- decrypted bytes may only be obtained, hashed, zeroed, and then the buffer reset;
- direct stdout/stderr print primitives and verifier-owned file output are forbidden.

The ciphertext path and expected plaintext SHA-256 are identifiers/commitments, not the protected plaintext itself.

## Workflow contract

The validator reviews the strict-verifier prototype, cross-runner reproducibility, live-synthetic continuity, and leakage-contract workflows. For each reviewed workflow it requires:

- `contents: read` permissions and no write/OIDC permissions;
- no `${{ secrets.* }}`-style secret references;
- no environment-variable names representing plaintext, mapping, keys, nonce, secrets, tokens, passwords, or passphrases;
- no `GITHUB_OUTPUT`, `GITHUB_STEP_SUMMARY`, legacy `set-output`, or shell tracing (`set -x` / `bash -x`);
- exact pinned checkout action identity;
- uploaded paths limited to `.txt` evidence records and `.txt.sha256` sidecars;
- artifact paths cannot resemble ciphertext/plaintext/mapping/private-key/nonce or binary protected material.

The contract is self-auditing: its own workflow is included in the workflow set it validates.

## Evidence boundary

A PASS shows that the reviewed source/workflow definitions have no configured channel for protected plaintext/key/mapping material and that decrypted bytes inside the helper remain confined to hash/zero/reset operations before a metadata-only report is emitted.

A PASS does **not** prove that an eventual operator could never expose a secret outside these reviewed definitions, nor does it establish the final protected ciphertext/commitment identity or accepted P6 retention. Final accepted execution must still bind exact inputs and preserve this contract.

## Remaining Issue #295 work after a PASS

At minimum:

- bind the final accepted ciphertext identity and separately committed expected-plaintext identity;
- bind the final accepted helper/repository/run attempt;
- retain accepted continuity evidence through the independent P6/transparency mechanism rather than GitHub artifact storage alone;
- perform final independent review/adjudication of the integrated continuity path.

No freeze, authorization, custody sufficiency, empirical execution, efficacy, or N change is created by this tranche.

Scientific posture: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
