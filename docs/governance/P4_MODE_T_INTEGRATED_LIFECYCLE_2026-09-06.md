# P4 Mode T — Integrated lifecycle synthetic verification

Date: 2026-09-06  
Issue: #310  
Stack: #311 claim contract → #313 Google OIDC trust layer → this lifecycle tranche  
Status: **SYNTHETIC INTEGRATION ONLY / REAL CONFIDENTIAL SPACE NOT EXECUTED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

This tranche connects the reviewed boundaries without executing the real pilot:

`R → A → C → authenticated PRE_EXECUTION → in-process key capability → blinded synthetic output → output manifest → authenticated POST_EXECUTION → two-phase lineage binding`

The test uses synthetic authorization and synthetic attestation material. No test fixture is a real authorization, real Google attestation, real custody record, or empirical output.

## Corrected key-generation boundary

The stale #312 prototype required `output_manifest_sha256` before generating the Mode-T key. That is incompatible with the corrected two-phase contract because the output manifest does not exist until after the key has been generated and used to create blinded output.

The replacement key path requires PRE_EXECUTION, an exact C binding, no pre-key output-manifest binding, the full admitted runtime identity, and no external operational secret environment variable.

### Second-pass integrity and anti-promotion hardening

Adversarial integration review found two additional defects after the first green #314 head:

1. the lease accepted `runtime_identity` and `runtime_identity_sha256` separately without recomputing the digest immediately before entropy generation; and
2. a production-facing key API that accepted caller-assembled “verified” metadata would recreate the same trust-delegation weakness that the Google signature verifier was intended to eliminate.

Both are now closed in the current design.

The production function `admit_and_acquire_mode_t_key(...)` accepts the **raw attestation token** and a frozen PRE expectation. Inside the same production entry point it:

1. invokes `verify_google_confidential_space_token(...)`, whose production path has no injected fetcher parameter;
2. authenticates the reviewed Google OIDC/JWKS signing-key path and verifies the token signature;
3. evaluates the exact PRE_EXECUTION Confidential Space claim contract;
4. canonically reserializes the complete normalized runtime identity and recomputes SHA-256;
5. requires that recomputed digest to equal the attested `runtime_identity_sha256`;
6. verifies that the `VerifiedGoogleOIDCToken` token digest is the same digest embedded in the normalized PRE record;
7. requires production transport provenance `HTTPS_SYSTEM_CA_HOSTNAME_VERIFIED`;
8. rejects externally supplied operational-secret environment variables; and only then
9. calls the OS-backed CSPRNG for the 256-bit operational key.

The production API therefore does **not** accept a caller-supplied `signature_verified` boolean, provenance dictionary, or alternate key fetcher as its trust boundary.

Synthetic CI uses the separately named `admit_and_acquire_mode_t_key_synthetic(...)`, which requires an explicitly injected `GoogleOIDCVerifier` whose result must carry `SYNTHETIC_INJECTED_FETCHER` provenance. A narrow `acquire_mode_t_key_synthetic_from_verified(...)` seam exists only for adversarial mutation tests after normalization; it is not the production API.

Dedicated controls now prove rejection of:

- runtime identity mutation after claim normalization;
- normalized PRE token-digest substitution;
- a synthetic verifier result forced into the production raw-token path;
- POST_EXECUTION evidence used for key generation;
- a circular pre-key output-manifest binding; and
- external operational-secret environment injection.

The generated key remains inside a non-serializable lease. The API exposes only domain-separated HMAC capabilities for blinded identifiers, ordering tokens, and a commitment. The owned mutable buffer is best-effort zeroized on normal exit and exception paths.

Python zeroization is not treated as proof that no runtime copies existed; real TEE execution and independent leakage review remain required.

## Single-use R/A/C model

The integrated test adds a deliberately synthetic R/A/C model aligned with the Mode-T schema draft:

- R is a sealed synthetic run reservation fixture.
- A is explicitly named and marked `SYNTHETIC_GRANTED_FOR_TEST_ONLY`; it is not a real pilot authorization.
- C is created as `CONSUMED_PRE_SECRET_SYNTHETIC` and records `secret_instantiation_status: NOT_EXECUTED_AT_CONSUMPTION`.
- Once C is created, the authorization ID is marked consumed before the caller can cross into key generation.

The ledger exposes a snapshot/rehydration model so tests can simulate process loss. Rehydrating after C preserves the consumed authorization and rejects a second C for the same A.

This demonstrates state-machine retry semantics only. The retention marker is explicitly `SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED`; it does not establish P6, transparency-log retention, or anti-deletion evidence.

## Integrated output-manifest order

After PRE admission and key generation, the synthetic path creates a blinded artifact containing only opaque HMAC-derived identifiers/order tokens. It checks that supplied clear identifiers do not appear in the serialized artifact.

The output manifest is then built and hashed. It binds:

- candidate commit SHA;
- freeze digest fixture;
- exact C digest;
- runtime-identity digest;
- workload image digest;
- tlock client digest and chain hash;
- blinded-artifact digest;
- timelock-ciphertext digest fixture;
- key commitment;
- PRE token digest;
- execution start/completion timestamps.

Only after this manifest exists does the synthetic POST token bind `SHA256(manifest)` as its nonce. The final lineage record verifies PRE→C, POST→manifest, same runtime identity, distinct token digests, manifest runtime identity, and the exact PRE token digest.

The final record is `PASS_SYNTHETIC_ONLY`, with `real_confidential_space_admission=false`, `independent_retention_verified=false`, `freeze_established=false`, `pilot_authorized=false`, and `empirical_n=0`.

## Crash/retry coverage

Dedicated controls exercise crashes at these post-C boundaries:

1. immediately after C and before PRE attestation;
2. after PRE admission and before key generation;
3. after key generation, verifying lease destruction on exception;
4. after blinded output and before POST attestation;
5. after a successful complete synthetic lifecycle.

Every case rehydrates the C ledger and proves the same authorization cannot be consumed again. A later execution would require a new R/A/C identity chain.

## Standards comparison

The production trust design is consistent with the reviewed security requirements used for this tranche:

- application-fixed RS256 rather than trusting the token-selected algorithm;
- issuer/key association through the authenticated Google discovery/JWKS path;
- no arbitrary `jku`, `jwk`, or `x5u` trust redirection;
- HTTPS discovery/JWKS endpoint and exact issuer consistency;
- signed audience/subject/runtime claims remain fail-closed exact-match checks in the separate admission contract.

This is an implementation/standards review, not an independent organizational security review.

## What this does not verify

This tranche does **not** prove:

- real Google signing-key retrieval occurred during the synthetic integration test;
- a real Confidential Space token was verified;
- an authenticated GCP project/workload was admitted;
- the in-memory C model is independently retained or anti-deletion;
- the TEE prevents operator access to protected key/plaintext in practice;
- final tlock execution/release continuity;
- P4 closure;
- final freeze or pilot authorization;
- empirical execution.

## Remaining gates after synthetic CI

1. Complete independent security review of the signature/key-source and key-acquisition implementation.
2. Keep the Google OIDC dependency lock and exact-head CI green.
3. Replace the synthetic C retention model with the reviewed independently retained evidence path required by P4-T.
4. Build/review the exact Confidential Space workload image and launch configuration.
5. Run one authenticated synthetic-only real Confidential Space admission attempt and retain both real PRE and POST token evidence.
6. Independently retrieve/re-verify the real tokens, source keys, launch claims, C/manifest nonces, and retained provenance.
7. Only then adjudicate Mode T for P4.

Until those are completed: **P4 OPEN / real execution NOT EXECUTED / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.
