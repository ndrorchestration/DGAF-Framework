# P4 Mode T — Side-effect-free Sigstore verifier boundary

Date: 2026-09-06  
Issues: #287 / #296 / #310 / #316  
Parent PR: #323  
Status: **VERIFIER CANDIDATE / EXACT-HEAD CI REQUIRED**

Controlling state remains **P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

PR #323 deliberately introduced a normalized `VerifiedTransparencyContext` rather than implementing Sigstore cryptography inside the retention contract. That separation is useful, but it creates a trust seam if an active path can populate cryptographic-verification booleans directly.

This tranche adds a read-only cryptographic boundary around the retention contract without creating a second signer, OIDC client, Rekor uploader, or time authority.

The public DGAF entry point requires:

1. a predeclared `TransparencyExpectation`;
2. the exact reviewed Cosign Linux/amd64 binary identity;
3. an existing public/non-secret record artifact;
4. an existing standardized Sigstore v0.3 bundle;
5. exact certificate identity from the predeclared expectation;
6. the fixed GitHub Actions OIDC issuer;
7. a positive `cosign verify-blob` result;
8. an actual transparency-log inclusion proof;
9. exact artifact digest equality when the result is handed to the retention contract.

It does **not** sign, request OIDC, upload to Rekor, or perform a DGAF external-retention write.

## Load-bearing Cosign identity

The verifier pins:

```text
version policy: v3.1.3
linux-amd64 SHA-256: 4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71
```

This minimum is security-relevant rather than cosmetic. Cosign v3.1.3 is the first v3 release patched for **GHSA-fx35-mq7g-6g98**, a keyless `verify-blob` verification bypass affecting legacy JSON bundles in v3 <= 3.1.2.

The DGAF wrapper does not accept a caller-selected Cosign digest. The fixed executable digest is code policy.

## Bundle-format policy

Current Sigstore protobuf specifications define the current bundle as v0.3 and identify transparency entries through `LogId` plus `logIndex`.

DGAF therefore accepts only the reviewed v0.3 standardized media types:

- `application/vnd.dev.sigstore.bundle.v0.3+json`
- `application/vnd.dev.sigstore.bundle+json;version=0.3`

Legacy Cosign JSON bundles and standardized v0.1/v0.2 bundles are rejected by this lane even if a future tool invocation would otherwise accept them.

An `inclusionPromise` alone is not enough for DGAF's normalized anti-deletion inclusion predicate. The bundle must contain a non-empty `inclusionProof`.

## Log identity correction

The retention schema previously used the name `log_entry_uuid` for Sigstore `logId.keyId`. That was semantically inaccurate: `LogId.keyId` identifies the transparency log key, not an entry UUID.

The child lane corrects the field to `log_id_key_id` and keeps `log_index` separately. No UUID claim is made.

## Protobuf JSON numeric compatibility

Sigstore protobuf JSON may encode uint64 values such as `logIndex` and `integratedTime` as decimal strings. The verifier accepts either a non-negative integer or a canonical unsigned decimal string and normalizes to Python integers.

It rejects booleans, negatives, signs, whitespace, non-decimal forms, and non-canonical leading-zero encodings.

`integratedTime` remains **metadata only**. It is not promoted to an independent wall-clock or L-before-release proof.

## API trust boundary

The old public `normalize_verified_bundle(...)` shape is removed. Bundle normalization is private and can only be reached through the public cryptographic verification flow in ordinary API use.

The public function is:

```text
verify_retention_record_with_sigstore(...)
```

It consumes the predeclared expectation and does not accept a caller-selected OIDC issuer or Cosign digest.

`retention_safe_evidence(...)` accepts the resulting verified wrapper rather than a caller-supplied tool digest, preventing evidence serialization from substituting a different Cosign identity.

## Dedicated CI

The dedicated workflow performs two classes of evidence:

### Deterministic repository tests

Tests cover:

- exact read-only `verify-blob` command construction;
- fixed GitHub OIDC issuer and expectation-bound certificate identity;
- wrong Cosign binary rejection before verification;
- non-zero Cosign result rejection;
- no public normalize-without-crypto entry point;
- no caller-selectable Cosign digest or OIDC issuer;
- legacy/v0.1/v0.2 bundle rejection;
- promise-only bundle rejection;
- missing/multiple transparency-entry rejection;
- canonical protobuf uint64 parsing;
- tampered/missing log identity rejection;
- no promotion to real retention, temporal order, freeze, authorization, or empirical N.

### Real read-only upstream cryptographic smoke test

The workflow downloads the official Cosign v3.1.3 Linux/amd64 release binary and its official Sigstore bundle, requires the exact reviewed SHA-256, and performs identity-based `verify-blob` verification against the documented release identity:

```text
keyless@projectsigstore.iam.gserviceaccount.com
https://accounts.google.com
```

It then appends one byte to a copy and requires verification to fail.

This is a **public upstream verifier-mechanics fixture only**. It is not a DGAF Mode-T record, does not create a transparency entry, and does not satisfy DGAF retention or time-order gates.

## Trust interpretation

A successful DGAF call can establish that supplied artifact/bundle bytes passed the exact reviewed local cryptographic verification path and that the normalized result matches the predeclared record digest and identity.

That is still narrower than real P6/P4 evidence. The verifier performs no DGAF external write and cannot establish that a separately controlled durable copy exists merely because a bundle verifies.

Likewise, transparency inclusion is kept separate from temporal-order evidence.

## Remaining real blockers

This tranche does not close:

- independently retained and re-verifiable R/A/C admission-policy evidence under #316;
- an actual Sigstore bundle for a real Mode-T DGAF record;
- independently retrieved/reverified durable DGAF external-retention evidence;
- duplicate/one-C-per-authorization adjudication on the real external evidence source;
- independent L-before-release time/order evidence if that predicate remains required;
- independent security review;
- authenticated Confidential Space execution and independently reverified PRE/POST evidence;
- repository merge-enforcement configuration.

**P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
