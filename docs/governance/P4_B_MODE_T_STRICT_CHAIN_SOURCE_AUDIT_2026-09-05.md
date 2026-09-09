# P4-B Mode T Strict-Chain Source Audit — 2026-09-05

**Status:** PARTIAL ENGINEERING EVIDENCE / SOURCE AUDIT ONLY / ISSUE #295 REMAINS OPEN  
**Parent Mode-T design:** #287 / draft PR #292  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Establish one narrow, independently rerunnable fact needed by P4-B continuity design before implementing a dedicated decryptor: the exact pinned `drand/tlock` source used by DGAF exposes strict chain-hash enforcement, while the stock `tle` v1.2.0 decryption path does not invoke it.

This tranche does **not** decrypt protected material, construct real custody, select the analysis-lock window `W`, establish freeze, authorize P4, execute empirical work, or close P4-B.

## Frozen upstream identity

```yaml
project: drand/tlock
version: "1.2.0"
source_commit: 7b54141a9733fd6fa207587a11148280e6fb020d
quicknet_chain_hash: 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971
quicknet_scheme: bls-unchained-g1-rfc9380
```

The release-asset checksum boundary was separately verified by PR #291. This audit is source-semantic evidence, not a substitute for that binary checksum evidence.

## Mechanically audited source facts

The workflow retrieves these files directly from the exact source commit:

- `tlock.go`
- `tlock_age.go`
- `cmd/tle/tle.go`

The audit fails closed unless all of the following remain true at that immutable source identity:

1. `tlock.New(network)` defaults `trustChainhash` to `true`.
2. `Tlock.Strict()` sets `trustChainhash` to `false`.
3. the age identity path contains a ciphertext-chain mismatch branch that may invoke `SwitchChainHash(...)` when `trustChainhash` is true.
4. wrong-chain handling exposes `ErrWrongChainhash`.
5. stock `tle` decryption calls `tlock.New(network).Decrypt(dst, src)`.
6. stock `tle` decryption does **not** call `.Strict().Decrypt(...)`.

Therefore stock `tle` v1.2.0 decryption is not accepted as DGAF strict-chain continuity evidence.

## Repository implementation

Added:

- `experiments/pdmal_pilot/mode_t_strict_chain_source_audit.py`
- `experiments/pdmal_pilot/test_mode_t_strict_chain_source_audit.py`
- `.github/workflows/p4-b-mode-t-strict-chain-source-audit.yml`

The audit emits machine-readable JSON plus SHA-256 sidecar and exact-head binding metadata. It records only engineering/source facts and the controlling non-authorizing scientific state.

The workflow uses exact PR-head checkout, pinned GitHub Actions identities, Python 3.12.0, the repository's hash-locked PDMAL dependency file, HTTPS-only pinned-source retrieval, and a non-secret evidence artifact.

## Fail-closed tests

The contract tests reject at least these mutations:

- `Strict()` no longer disables chain-hash switching;
- the upstream mismatch path no longer exposes the chain-switch behavior the audit is designed to detect;
- the expected stock CLI path disappears or changes unexpectedly;
- stock CLI decryption unexpectedly becomes strict at the pinned identity, which would require a fresh design review rather than silent reinterpretation.

## What remains OPEN in #295

This source audit is intentionally insufficient to close the issue. A dedicated continuity verifier still must be designed, dependency-pinned, implemented, and validated to:

- instantiate the frozen quicknet network from an explicit endpoint and chain hash;
- validate chain identity, scheme, and public-key metadata before decryption;
- decrypt only through `tlock.New(network).Strict()`;
- fail closed on wrong-chain, malformed, too-early, or commitment-mismatch cases;
- compare plaintext only to the separately committed expected digest;
- avoid emitting protected plaintext, keys, mappings, or secrets in logs, outputs, artifacts, environment, or command arguments;
- bind output to repository, helper, tool, ciphertext, run, and attempt identities;
- retain accepted evidence through the final P6/transparency mechanism rather than GitHub storage alone;
- demonstrate exact dependency/build reproducibility for any custom Go helper.

## Non-effects

Passing this audit does **not** establish Mode-T custody sufficiency, P4-B completion, a release-margin policy, hosted-runner memory independence, freeze, authorization, empirical execution, efficacy, or any increase in empirical N.

Scientific posture: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
