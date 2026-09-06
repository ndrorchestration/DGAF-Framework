# P4-B Mode T Frozen Metadata Preflight — 2026-09-06

## Status

**OFFLINE SYNTHETIC VERIFICATION ONLY / NOT CUSTODY / NOT AUTHORIZATION**

Scientific boundary remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.

## Purpose

This tranche isolates the Issue #295 requirement that a frozen drand network-identity mismatch must fail before ciphertext decryption can begin.

The strict verifier already calls `validateNetworkMetadata(network)` before `tlock.New(network).Strict().Decrypt(...)`. This tranche adds an adversarial fake `tlock.Network` whose `ChainHash()` deliberately disagrees with the frozen quicknet chain hash and whose `Signature(...)` and `SwitchChainHash(...)` methods count any invocation.

The test requires all of the following:

- verifier returns `network chain hash mismatch`;
- signature calls remain exactly zero;
- chain-switch calls remain exactly zero;
- no live drand endpoint, protected material, empirical data, or external side effect is involved.

## Exact boundary

This is evidence only for ordering and fail-closed behavior at the verifier metadata-preflight boundary. It does not prove the final protected ciphertext identity, accepted P6 retention, custody sufficiency, freeze, authorization, empirical execution, or efficacy.

Successful CI does not close Issue #295 by itself. Remaining integrated acceptance work includes final ciphertext/commitment binding, broader leakage review, final exact-run provenance, accepted P6/transparency retention, and independent final review.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
