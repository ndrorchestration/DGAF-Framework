# P4 Mode T — Google OIDC signing-key authentication

Date: 2026-09-06  
Scope: Confidential Space admission proof / cryptographic trust layer  
Status: **IMPLEMENTED FOR SYNTHETIC REVIEW; CI PENDING AT CREATION; REAL TOKEN NOT YET VERIFIED**

Controlling scientific state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Why this exists

The Confidential Space claim contract cannot treat a caller-supplied `signature_verified=True` value as security evidence by itself. A token signature establishes Google Cloud Attestation identity only when the verifying public key is obtained through an authenticated, reviewed Google trust path and the token is cryptographically verified before its claims are admitted.

This change adds that missing trust layer. It does not close P4 and does not replace the existing exact-match Confidential Space claim contract.

## Reviewed Google trust path

The verifier is pinned to the Google Cloud Attestation OIDC issuer and discovery path:

- issuer: `https://confidentialcomputing.googleapis.com`
- discovery: `https://confidentialcomputing.googleapis.com/.well-known/openid-configuration`
- accepted signing algorithm: `RS256`
- reviewed JWKS URI: `https://www.googleapis.com/service_accounts/v1/metadata/jwk/signer@confidentialspace-sign.iam.gserviceaccount.com`

Current Google Confidential Space documentation describes discovery through that OIDC metadata and selection of the rotating signing key by the JWT `kid`. Multiple keys may coexist during rotation.

The implementation therefore does **not** pin one long-lived Google public key. It authenticates the reviewed discovery/JWKS endpoints over normal system-CA HTTPS, validates the discovery issuer and exact reviewed JWKS URI, and selects an RSA signing key by `kid`.

## Fail-closed trust-source policy

`mode_t_google_oidc_verifier.py` enforces all of the following before it produces a `VerifiedTokenContext`:

1. HTTPS uses the system trust store and hostname verification; no custom CA or insecure TLS mode is accepted by the production path.
2. Redirects are rejected for both discovery and JWKS retrieval.
3. Discovery must identify the exact Google Cloud Attestation issuer, advertise `RS256`, and return the exact reviewed JWKS URI.
4. JWKS keys must have a unique non-empty `kid`, `kty=RSA`, `use=sig`, `alg=RS256`, a valid odd exponent, and an RSA size between 2048 and 8192 bits.
5. JWT header `alg` must be exactly `RS256`; `jku`, embedded `jwk`, `x5u`, and `crit` are rejected rather than allowed to redirect trust.
6. The signature is verified with RSA PKCS#1 v1.5 / SHA-256 before signed claims are used.
7. The signed issuer must again be the exact Google Cloud Attestation issuer.
8. Signed `iat`, `nbf`, and `exp` values must be integer timestamps and satisfy the bounded clock-skew policy.
9. Discovery/JWKS documents and JWTs have strict size limits; duplicate JSON keys and duplicate JWKS `kid` values are rejected.

## Rotation, cache, outage, and provenance

A cached JWKS is usable only until its bounded expiry. `Cache-Control: max-age` is honored with an upper cap; `Age` reduces remaining cache lifetime. `no-cache` or `no-store` prevents reuse.

If a valid, unexpired cache lacks the requested `kid`, the verifier performs exactly one authenticated discovery/JWKS refresh. This permits normal Google key rotation without silently widening the trust root. If the requested `kid` is still absent, verification fails.

If the authenticated source is unavailable:

- a previously authenticated key may continue to verify only while its cache entry remains valid;
- an unknown `kid` cannot be accepted without a successful authenticated refresh;
- an expired cache is never used as an outage fallback.

Retention-safe provenance records the exact discovery URL, exact JWKS URI, raw discovery-document SHA-256, raw JWKS-document SHA-256, selected `kid`, canonical selected-JWK SHA-256, fetch time, cache expiry, algorithm, and transport-authentication policy. It records the token SHA-256 rather than persisting the token in the evidence summary.

## Dependency reproducibility

The verifier depends on `cryptography==50.0.1`. The Mode-T security lane has its own reviewed lock:

- `requirements-mode-t-security.in`
- `requirements-mode-t-security-lock.txt`

The lock is intentionally scoped to the reviewed **CPython 3.12 / Linux x86-64** lane and contains hashes for the selected `cryptography`, `cffi`, and `pycparser` wheels. CI installs it with both `--require-hashes` and `--only-binary=:all:` and then asserts the installed versions.

A Python/platform/runtime change invalidates that bounded wheel review and requires regeneration/re-review rather than silent cross-platform resolution.

## Synthetic negative-control coverage

The dedicated test lane covers, at minimum:

- valid RS256 verification and retained key-source provenance;
- successful handoff into the current PRE_EXECUTION Confidential Space claim contract;
- signature tampering;
- algorithm confusion;
- JWT-supplied key-source redirection;
- wrong signed issuer;
- expired signed token;
- discovery issuer substitution;
- discovery JWKS substitution;
- malformed discovery algorithm metadata;
- redirected discovery;
- duplicate `kid` ambiguity;
- authenticated key rotation;
- unknown-`kid` refresh outage;
- bounded valid-cache behavior followed by fail-closed expiry;
- `Age`-reduced cache lifetime;
- non-signature JWK use.

These tests deliberately use an injected synthetic fetcher. Operational lifecycle code must call `verify_google_confidential_space_token(...)`, which constructs the default authenticated HTTPS verifier and exposes no fetcher parameter.

## Required next evidence

This implementation is necessary but insufficient for Mode-T admission. Before P4 can move from OPEN, all of the following remain required:

1. GitHub CI must pass on the exact branch head with the hash-locked security lane.
2. The implementation must receive an independent security review that does not merely repeat its own test assumptions.
3. The current key-provider stack must be reconciled with the corrected two-phase attestation contract.
4. An integrated synthetic lifecycle must exercise immutable authorization consumption C → authenticated PRE_EXECUTION verification → in-process key generation → blinded output/manifest → authenticated POST_EXECUTION verification → two-phase lineage binding, including crash/retry failure paths.
5. A real Confidential Space admission run must use an authenticated GCP project and reviewed workload/launch configuration and must produce independently re-verifiable real attestation evidence.

Until those gates are satisfied, **P4 remains OPEN / NOT EXECUTED for real custody; freeze is not established; pilot authorization is not granted; empirical N=0**.
