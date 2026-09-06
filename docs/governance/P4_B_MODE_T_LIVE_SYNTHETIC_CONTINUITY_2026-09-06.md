# P4-B Mode T Live Synthetic Continuity — 2026-09-06

## Status

**DESIGN / SYNTHETIC ENGINEERING EVIDENCE ONLY / NOT CUSTODY / NOT AUTHORIZATION**

Scientific boundary remains:

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

This tranche extends the strict Mode-T continuity verifier with a narrowly scoped live-public-network test against the frozen drand quicknet identity. It is intended to close three synthetic verifier mechanics that remain open after the offline adversarial prototype and cross-runner build-reproducibility work:

1. a correct-chain ciphertext for an already available quicknet round can be decrypted through `tlock.New(network).Strict().Decrypt(...)` and accepted only when its precommitted plaintext SHA-256 matches;
2. a correct-chain decrypt with an intentionally wrong expected plaintext commitment fails closed as `PLAINTEXT_COMMITMENT_MISMATCH`;
3. a future-round ciphertext is classified explicitly as `TOO_EARLY` rather than becoming a generic or false PASS.

No protected mapping, key, nonce, empirical observation, freeze state, or authorization state is used.

## Exact dependency boundary

- tlock source commit: `7b54141a9733fd6fa207587a11148280e6fb020d`
- Go toolchain: `1.22.12`, `GOTOOLCHAIN=local`
- target: Linux/amd64, `GOAMD64=v1`, `CGO_ENABLED=0`
- quicknet chain hash: `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`
- quicknet scheme: `bls-unchained-g1-rfc9380`
- endpoint used by the dedicated lane: `https://api.drand.sh/`

The verifier's frozen public-key check remains active before decryption.

## Test mechanics

The build-tagged live test file is excluded from ordinary offline prototype execution. The dedicated workflow overlays the verifier and live tests into the exact pinned upstream tlock module graph and runs three cases separately.

For released-round tests, the fixture is a fixed synthetic plaintext encrypted in memory to a round derived from a timestamp 45 seconds in the past. No plaintext or ciphertext fixture is written to the repository or to disk by the test.

For the too-early case, the fixed synthetic plaintext is encrypted in memory to a round derived from a timestamp two minutes in the future. The test requires the verifier to return the explicit `TOO_EARLY` classification.

The workflow has read-only repository permissions. Its only external interaction is read-only access to the public drand endpoint needed to resolve network metadata and beacon signatures.

## Evidence record

A successful run emits only a small non-secret text record plus SHA-256 sidecar. It records exact repository/run identity, pinned source identity, quicknet identity, and booleans for the three accepted synthetic cases.

The evidence record explicitly keeps all of the following false:

- durable P6 retention established;
- custody sufficiency established;
- freeze established;
- pilot authorized;
- empirical data collection;
- empirical N greater than zero.

The artifact is ordinary GitHub Actions storage with 30-day retention. It is not append-only, independent custody, or accepted P6 durability by itself.

## What a PASS establishes

A PASS establishes only that, at the exact tested head and public-network conditions:

- frozen quicknet metadata passed the verifier's preflight;
- strict correct-chain decryption succeeded for a synthetic released-round fixture;
- plaintext commitment verification accepted the correct commitment;
- an intentionally wrong commitment was rejected after decryption;
- a future-round fixture was classified as too early;
- the tests did not promote scientific or authorization state.

## What remains open for Issue #295

This tranche does not by itself close P4-B continuity or Issue #295. Remaining acceptance work includes, at minimum:

- final ciphertext/commitment identity binding for the eventual accepted protected-material path;
- broader leakage review across command-line, environment, logs, summaries, artifacts, and process surfaces;
- accepted exact-run provenance for the final continuity execution;
- P6/transparency retention through the finally accepted independent mechanism;
- independent final review of the complete continuity path;
- replay/repeated-verification non-mutation verification at the integrated lifecycle boundary.

Cross-runner byte identity under GitHub-hosted Ubuntu families remains separate evidence and is not promoted to independent-operator reproducibility.

## Non-effects

This work does not establish Mode-T custody sufficiency, select analysis-lock window `W`, create a freeze, grant pilot authorization, execute PDMAL empirical work, unblind protected material, establish DGAF efficacy, or increase empirical N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
