# P4 Mode T — Retention evidence contract correction

Date: 2026-09-06  
Issues: #287 / #310 / #316  
Status: **NORMALIZED CONTRACT / NO REAL SIGSTORE ENTRY / NO TIME AUTHORITY APPROVED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

The Mode-T evidence design needs two distinct predicates:

1. **inclusion / anti-deletion evidence** — evidence that a signed public R/C/X/L record was accepted into a verifiable transparency system under the expected identity; and
2. **temporal-order evidence** — evidence that L occurred strictly before the deterministic timelock release boundary.

These predicates must not be collapsed into one another.

This tranche is stacked on the lineage-reconciled Confidential Space launch contract and current #314 policy-bound lifecycle rather than the stale #317/#319 chain.

## Sigstore/Rekor evidence boundary

A valid, independently verified transparency inclusion can support public evidence that a specific signed record was included under an expected signing identity. That is useful because ordinary GitHub Actions history is not accepted as immutable anti-deletion evidence.

However, Rekor v1 `integratedTime` is treated only as log metadata here, not as an independently verifiable wall-clock authority. Therefore:

- transparency inclusion is not rejected;
- `integratedTime` may be retained as metadata;
- neither inclusion nor that timestamp proves L-before-release;
- temporal ordering remains OPEN until a separately reviewed mechanism exists or the protocol is redesigned not to require that wall-clock claim.

## `mode_t_retention_contract.py`

The module consumes only **already-verified normalized metadata** from a separate Sigstore-capable cryptographic verifier. It does not itself perform signing, Fulcio verification, Rekor inclusion-proof verification, TUF trust-root retrieval, log monitoring, or external durable retention.

For one expected public record it requires normalized evidence that:

- artifact signature is verified;
- certificate chain is verified;
- expected certificate identity is verified;
- expected GitHub Actions OIDC issuer is verified;
- transparency inclusion is verified;
- signed-entry timestamp signature is verified;
- verified record SHA-256 equals the exact expected public-record digest;
- bundle SHA-256, log UUID, and non-negative log index are retained.

Accepted record classes are restricted to:

- `PDMAL_MODE_T_RUN_RESERVATION`;
- `PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION`;
- `PDMAL_P4_T_EXECUTION`;
- `PDMAL_P4_T_ANALYSIS_LOCK`.

A successful normalized result is `PASS_NORMALIZED_INCLUSION_ONLY` and explicitly records:

- `anti_deletion_inclusion_evidence = VERIFIED_NORMALIZED`;
- `temporal_order_verified = false`;
- `external_sigstore_crypto_performed_by_this_module = false`;
- `real_external_retention_established = false`;
- `pilot_authorized = false`;
- `empirical_n = 0`.

This is intentionally narrower than real P6/P4 evidence and does not satisfy the independently retained C/policy source still required by #316.

## Analysis-lock rule

`verify_analysis_lock_temporal_order(...)` can consume an already normalized L-inclusion record, but cannot return temporal PASS in this contract version.

Without a separately reviewed time/order authority it returns inclusion verified but temporal status OPEN. Supplying an arbitrary caller dictionary claiming `before_release=true` or another unapproved time source is rejected. This prevents another caller-supplied boolean from being promoted into evidence.

## What still must be implemented for real external retention

A future real path must separately establish:

1. a pinned/reviewed Sigstore-capable verifier and authenticated trust-root path;
2. exact certificate identity and OIDC issuer policy for the frozen workflow;
3. cryptographic verification of signatures, certificate chain, bundle, SET, and inclusion evidence;
4. independent durable retention of the exact public record and verification bundle;
5. monitoring/trust disposition consistent with the selected transparency system;
6. duplicate-search / one-C-per-authorization adjudication suitable for the real external evidence path;
7. fail-closed behavior when signing, logging, retrieval, verification, or retention is unavailable;
8. integration with the independently retained C/admission-policy evidence required by #316; and
9. a separate solution for L-before-release temporal ordering if that requirement remains in the protocol.

## Non-effects

No Sigstore identity token is requested. No Fulcio certificate is issued. No Rekor record is uploaded. No external archive is written. No independent time authority is used. No real C/policy retention is established. No authorization, key, freeze, or empirical execution occurs.

**P4 remains OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
