# P4 Mode T — Side-effect-free Sigstore verifier boundary

Date: 2026-09-06  
Issues: #287 / #296 / #310 / #316  
Parent PR: #323  
Status: **VERIFIER CANDIDATE / EXACT-HEAD CI REQUIRED**

Controlling state remains **P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

This tranche adds a read-only Sigstore/Cosign verification boundary around #323's normalized retention contract. It does not sign, request OIDC, upload to Rekor, establish a time authority, or perform an external DGAF retention write.

The public verifier requires a predeclared `TransparencyExpectation`, the exact reviewed Cosign v3.1.3 Linux/amd64 executable, the exact artifact and standardized v0.3 bundle, exact signer identity/provenance, and now an **explicit TrustedRoot JSON file whose SHA-256 must equal the predeclared expectation**.

Ambient/default trust-material selection is therefore not accepted by the DGAF wrapper.

## Explicit TrustedRoot boundary

`verify_retention_record_with_sigstore(...)` now requires `trusted_root=Path(...)`. Before Cosign is invoked, the wrapper:

1. requires the TrustedRoot file to exist;
2. requires valid UTF-8 JSON with an object at the top level;
3. computes the exact file SHA-256;
4. requires equality with `TransparencyExpectation.trusted_root_sha256`;
5. passes that exact file to Cosign using `--trusted-root`.

The resulting normalized context and retention-safe evidence retain the same digest and state:

- `trusted_root_explicit_and_digest_bound = true`;
- `trusted_root_independently_approved = false`.

That distinction is load-bearing. **Exact root-byte binding is not independent governance approval of those roots, their TUF bootstrap, update semantics, validity interval, or production suitability.** No final DGAF production TrustedRoot value is selected or frozen by this tranche.

## Load-bearing Cosign and bundle policy

Cosign Linux/amd64 remains fixed to v3.1.3 SHA-256:

`4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71`

v3.1.3 is retained because it contains the fix for GHSA-fx35-mq7g-6g98. The wrapper accepts only reviewed standardized Sigstore v0.3 bundle media types and requires a non-empty transparency `inclusionProof`; promise-only evidence is rejected.

Sigstore `logId.keyId` is represented as `log_id_key_id`, not as a Rekor entry UUID. Protobuf JSON uint64 values are accepted only as canonical non-negative integers or canonical decimal strings. Rekor `integratedTime` remains metadata only, not an independent time authority.

## Signer provenance boundary

The expectation binds certificate identity plus exact GitHub workflow SHA, repository, and branch ref. These are passed into Cosign certificate-policy checks and rechecked by the retention contract.

The current synthetic fixture identity references `p4-mode-t-transparency.yml`, but no final production signer with that authority is established on `main`. #296/#299 remains the canonical controlled signing/timing apparatus. This tranche must not create a duplicate signer merely to satisfy a test fixture.

## Dedicated CI

Repository tests cover exact `--trusted-root` command construction; root digest propagation; tampered-root rejection; missing-root rejection; invalid-JSON-root rejection; wrong Cosign identity; Cosign failure; signer/OIDC mismatch; standardized-v0.3-only parsing; inclusion-proof enforcement; canonical integer handling; and non-promotion to retention/time/freeze/authorization/empirical claims.

The dedicated workflow also performs a real **read-only upstream verifier-mechanics smoke test** using the official Cosign v3.1.3 binary and bundle. For that smoke test only, Cosign creates a local TrustedRoot using its current default Sigstore services and the workflow explicitly passes the resulting file via `--trusted-root`. The root is hashed and validated as JSON.

That dynamically acquired root is an **upstream smoke-only fixture**. It is not a frozen or independently approved DGAF production TrustedRoot and is not evidence of DGAF retention.

The smoke test verifies the official artifact and requires a one-byte-tampered copy to fail. It creates no new transparency entry.

## What remains open

Even after exact-head CI succeeds, this tranche does not establish:

- independent approval/freeze of a final DGAF TrustedRoot or TUF bootstrap/update policy;
- a final production DGAF retention signer;
- a real DGAF Sigstore bundle or independently durable external retention;
- independently retained R/A/C admission-policy evidence required by #316;
- independent L-before-release temporal evidence;
- independent security review under #320;
- real Confidential Space admission or custody;
- repository merge-enforcement configuration;
- freeze, pilot authorization, or empirical execution.

**P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
