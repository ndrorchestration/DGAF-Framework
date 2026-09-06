# P4 Mode T — Retention evidence contract correction

Date: 2026-09-06  
Issues: #287 / #310 / #316  
Status: **NORMALIZED CONTRACT / EXPLICIT ROOT BYTE BINDING / NO REAL SIGSTORE ENTRY / NO TIME AUTHORITY APPROVED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

Mode-T retention must keep two predicates separate:

1. **inclusion / anti-deletion evidence** — a signed public R/C/X/L record was accepted into a verifiable transparency system under the expected identity; and
2. **temporal-order evidence** — L occurred strictly before the deterministic timelock release boundary.

They are not interchangeable.

## Normalized retention contract

`mode_t_retention_contract.py` consumes already-verified normalized metadata from the separate Sigstore verifier. It does not sign, retrieve trust roots, monitor logs, perform external retention, or establish time.

For one expected record it now requires normalized evidence for signature, certificate chain, certificate identity, GitHub Actions OIDC issuer, transparency inclusion, signed-entry timestamp, exact record SHA-256, exact signer workflow SHA/repository/ref, and the **exact predeclared TrustedRoot SHA-256**.

A successful result records:

- `anti_deletion_inclusion_evidence = VERIFIED_NORMALIZED`;
- `trusted_root_explicit_and_digest_bound = true`;
- `trusted_root_independently_approved = false`;
- `temporal_order_verified = false`;
- `real_external_retention_established = false`;
- `pilot_authorized = false`;
- `empirical_n = 0`.

The TrustedRoot distinction is deliberate: equality to a predeclared digest proves that verification used the expected bytes. It **does not prove independent approval of those bytes**, their TUF bootstrap/update path, validity policy, or final production suitability.

No final DGAF production TrustedRoot is selected or frozen here.

## Transparency semantics

Sigstore `LogId.keyId` identifies the transparency-log key and is represented as `log_id_key_id`; it is not treated as an entry UUID. `log_index` is retained separately.

Rekor `integratedTime` remains metadata only. Neither inclusion nor that value establishes an independent wall-clock L-before-release proof.

Accepted record classes remain:

- `PDMAL_MODE_T_RUN_RESERVATION`;
- `PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION`;
- `PDMAL_P4_T_EXECUTION`;
- `PDMAL_P4_T_ANALYSIS_LOCK`.

## Analysis-lock rule

`verify_analysis_lock_temporal_order(...)` cannot return temporal PASS in this contract version. Arbitrary caller-supplied `before_release` or unapproved time-authority claims remain rejected.

## Remaining requirements for real retention

The production path still requires:

1. independent review and freeze of the exact DGAF TrustedRoot and TUF bootstrap/update semantics;
2. a final frozen signer identity/workflow;
3. real DGAF signing and cryptographic bundle verification;
4. independent durable retention and later retrieval/reverification of the exact public record and bundle;
5. duplicate/one-C-per-authorization adjudication;
6. fail-closed handling of signing/logging/retrieval/retention failure;
7. integration with independently retained C/admission-policy evidence under #316; and
8. a separate solution for L-before-release temporal ordering if retained by the protocol.

## Non-effects

No Sigstore identity token is requested. No Fulcio certificate is issued. No Rekor record is uploaded. No external archive is written. No independent time authority is used. No real C/policy retention is established. No authorization, key, freeze, or empirical execution occurs.

**P4 remains OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
