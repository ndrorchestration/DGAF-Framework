# P4 Mode T — Retention evidence contract correction

Date: 2026-09-06  
Issues: #287 / #310  
Status: **NORMALIZED CONTRACT / NO REAL SIGSTORE ENTRY / NO TIME AUTHORITY APPROVED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

The original Mode-T transparency design correctly identified a need for evidence outside deletable GitHub Actions history, but it conflated two distinct predicates:

1. **inclusion / anti-deletion evidence** — evidence that a signed public R/C/X/L record was accepted into an append-only transparency system under the expected identity; and
2. **temporal-order evidence** — evidence that L occurred strictly before the deterministic timelock release boundary.

Current Sigstore documentation requires those predicates to be separated.

## Sigstore/Rekor evidence boundary

Sigstore describes Rekor as a verifiable transparency log and provides inclusion proofs/bundles that can support public, auditable evidence that an artifact/signing event was included. Its security model also makes monitoring and trust-root assumptions explicit.

This remains useful for Mode T because GitHub workflow history can be deleted. A valid independently verified and retained R/C/X record can make silent deletion/suppression materially harder.

However, current Sigstore timestamp documentation states for Rekor v1 that `integratedTime` is sourced from Rekor's internal clock and is **not externally verifiable**; the timestamp is not itself the Merkle-log node whose append-only consistency is checked.

Therefore:

- Rekor inclusion is not rejected;
- Rekor `integratedTime` may be retained as metadata;
- neither inclusion nor the internal timestamp is promoted into independent wall-clock proof;
- L-before-release remains OPEN until a separate time/order mechanism is justified or the protocol is redesigned not to require that external wall-clock inequality.

## `mode_t_retention_contract.py`

The module consumes only **already-verified normalized metadata** from a separate Sigstore-capable cryptographic verifier. It does not perform Sigstore signing, Fulcio verification, Rekor inclusion-proof verification, TUF trust-root retrieval, log monitoring, or external retention itself.

For one expected public record it requires normalized evidence that:

- artifact signature was verified;
- Sigstore certificate chain was verified;
- expected certificate identity was verified;
- expected GitHub Actions OIDC issuer was verified;
- transparency inclusion was verified;
- signed entry timestamp signature was verified;
- verified record SHA-256 equals the exact expected public record digest;
- bundle SHA-256, log UUID, and non-negative log index are retained.

Accepted record classes are limited to the reviewed Mode-T public sequence:

- `PDMAL_MODE_T_RUN_RESERVATION`;
- `PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION`;
- `PDMAL_P4_T_EXECUTION`;
- `PDMAL_P4_T_ANALYSIS_LOCK`.

A successful normalization returns `PASS_NORMALIZED_INCLUSION_ONLY` and explicitly records:

- `anti_deletion_inclusion_evidence = VERIFIED_NORMALIZED`;
- `temporal_order_verified = false`;
- `external_sigstore_crypto_performed_by_this_module = false`;
- `real_external_retention_established = false`;
- `pilot_authorized = false`;
- `empirical_n = 0`.

This is intentionally narrower than real P6/P4 evidence.

## Analysis-lock rule

`verify_analysis_lock_temporal_order(...)` can accept an already normalized L-inclusion record, but it cannot return temporal PASS in this contract version.

Without a separately reviewed time/order authority it returns:

- inclusion verified: true;
- temporal order verified: false;
- temporal status: OPEN;
- Rekor integrated time promoted: false;
- reason: separate independent time/order mechanism required.

Supplying an arbitrary caller dictionary that claims an external clock or `before_release=true` is rejected. This prevents a future caller from bypassing the unresolved design question with another unverified boolean.

## What still must be implemented for real external retention

A future real evidence path must separately establish:

1. a pinned/reviewed Sigstore-capable verifier and trust-root path;
2. exact certificate identity and OIDC issuer policy for the frozen workflow;
3. cryptographic verification of the signature, certificate chain, bundle, and Rekor inclusion evidence;
4. independent durable retention of the public record plus verification bundle;
5. a monitoring/trust disposition consistent with Sigstore's published model;
6. duplicate-search / one-C-per-authorization adjudication suitable for the real external log;
7. fail-closed behavior when signing, logging, retrieval, verification, or retention is unavailable;
8. a separate solution for L-before-release temporal ordering if that requirement remains in the protocol.

## Non-effects

No Sigstore identity token was requested. No Fulcio certificate was issued. No Rekor record was uploaded. No external archive was written. No independent time authority was used. No authorization, key, freeze, or empirical execution occurred.

**P4 remains OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
