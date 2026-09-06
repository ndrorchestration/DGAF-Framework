# P4-B Mode T Strict Continuity Verifier Prototype — 2026-09-05

**Status:** PROTOTYPE / SYNTHETIC-OFFLINE VALIDATION ONLY / LIVE CONTINUITY NOT EXECUTED  
**Issue:** #295  
**Prerequisite source audit:** draft PR #298  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Implement the next bounded layer of the P4-B Mode-T continuity design: a dedicated decryptor that is structurally incapable of accepting ciphertext-directed chain switching and that compares recovered plaintext only against a separately supplied SHA-256 commitment.

This tranche is a prototype-validation lane. It does not decrypt a DGAF protected mapping or key, does not create custody, does not close P4-B, and does not alter freeze, authorization, analysis, or empirical state.

## Frozen cryptographic identity

```yaml
tlock_version: v1.2.0
tlock_source_commit: 7b54141a9733fd6fa207587a11148280e6fb020d
quicknet_chain_hash: 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971
quicknet_scheme: bls-unchained-g1-rfc9380
quicknet_public_key_hex: 83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a
```

The source identity is already tied to the signed upstream `v1.2.0` tag and the separate release-asset checksum lane. PR #298 validates the exact strict/non-strict source semantics this prototype relies on.

## Verifier behavior

`experiments/pdmal_pilot/mode_t_strict_verifier.go`:

1. requires an explicit drand endpoint, ciphertext path, precommitted plaintext SHA-256, exact DGAF evidence SHA, run ID, and run attempt;
2. constructs the HTTP network with the frozen quicknet chain hash;
3. validates chain hash, scheme, and public key before decryption;
4. decrypts only via `tlock.New(network).Strict().Decrypt(...)`;
5. classifies wrong-chain, too-early, generic decrypt, and plaintext-commitment failures without printing the underlying decrypted material;
6. keeps plaintext only in a memory buffer, hashes it, zeroes the accessible buffer bytes, and resets the buffer;
7. emits only continuity/integrity metadata on PASS;
8. never writes plaintext to disk or stdout;
9. does not retry a too-early or failed decrypt internally;
10. records no scientific-state promotion.

This reduces plaintext exposure but does not prove hosted-runner live-memory confidentiality. That assumption remains UNKNOWN/OPEN.

## Offline adversarial validation

The Go test file exercises safety properties without waiting for a beacon or touching DGAF protected material.

Most importantly, it uses a public upstream tlock ciphertext fixture bound to a different drand chain and a fake frozen-quicknet network. `Strict().Decrypt(...)` must return `ErrWrongChainhash`, must not call `SwitchChainHash`, and must emit zero plaintext bytes.

The tests also cover:

- malformed ciphertext failure with zero plaintext output;
- exact failure classification for wrong-chain and too-early errors;
- strict validation of repository/run identity fields;
- lowercase SHA-256 commitment validation;
- frozen tlock/quicknet constant drift.

A correct-chain successful decrypt is intentionally not claimed by these offline tests.

## Build/dependency boundary

The prototype CI does not introduce a floating DGAF Go module. Instead it:

- pins `actions/setup-go` to immutable commit `40f1582b2485089dde7abd97c1529aa768e1baff`;
- pins Go to `1.22.12` with `GOTOOLCHAIN=local`;
- fetches the exact tlock source commit `7b54141a...`;
- overlays only the DGAF verifier source/tests into that exact upstream module;
- uses the upstream `go.mod` + `go.sum` with `go mod verify` and `-mod=readonly`;
- fixes `CGO_ENABLED=0`, `GOOS=linux`, and `GOARCH=amd64`;
- builds with `-trimpath -buildvcs=false -ldflags=-buildid=`;
- performs a cache-cleared second build and requires byte-identical binary SHA-256;
- deletes both prototype binaries before artifact upload and retains only build/provenance evidence.

Same-run byte-identical rebuilds are useful deterministic-build evidence, but they are **not** yet independent-environment reproducibility. Independent rebuild evidence remains required before this helper can be accepted as the final P4-B verifier.

## Explicit remaining blockers

Before #295 can close, at least the following remain:

- successful correct-quicknet strict decryption after an available synthetic/test round;
- explicit too-early live/test-round behavior with no silent retry;
- wrong expected plaintext commitment against a successfully decrypted synthetic fixture;
- independent-environment/toolchain rebuild comparison, not merely two builds on one runner;
- final accepted ciphertext/protected-material commitment binding format;
- proof that no protected plaintext/key/mapping enters logs, summaries, artifacts, environment variables, or command arguments during the accepted execution path;
- exact final run/attempt/ciphertext/tool/helper provenance record;
- final P6/transparency retention mechanism for continuity evidence;
- review of hosted-runner memory and post-process cleanup assumptions.

## Non-effects

Passing prototype CI does not establish P4-B continuity for any DGAF protected material, custody sufficiency, freeze, authorization, analysis lock, empirical execution, efficacy, or any increase in empirical N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
