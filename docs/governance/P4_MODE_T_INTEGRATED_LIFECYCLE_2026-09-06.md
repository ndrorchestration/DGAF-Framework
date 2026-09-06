# P4 Mode T — Integrated lifecycle synthetic verification

Date: 2026-09-06  
Canonical issues: #287 overall Mode T · #310 Confidential Space admission · #316 admission-policy binding · #320 independent OIDC review  
Stack: #311 claim contract → #313 Google OIDC trust layer → #314 integrated lifecycle  
Status: **SYNTHETIC INTEGRATION ONLY / PRODUCTION KEY ENTRY FAIL-CLOSED / REAL CONFIDENTIAL SPACE NOT EXECUTED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

This tranche connects the reviewed boundaries without executing the real pilot:

`pre-authorized launch policy → R → A → C → authenticated PRE_EXECUTION → in-process key capability → blinded synthetic output → output manifest → authenticated POST_EXECUTION → two-phase lineage binding`

The test uses synthetic authorization, synthetic retention, and synthetic attestation material. No test fixture is a real authorization, real Google attestation, real custody record, or empirical output.

## Deduplication / convergence

This record extends the existing #314/#316 work rather than creating a parallel admission-policy subsystem. #287 remains the overall Mode-T authority; #310 remains the bounded Confidential Space admission proof; #316 owns the policy-binding gap; #320 owns independent review; #277 owns merge enforcement; #293 owns timing/W; #296 owns deliberate public-transparency timing; #309 owns final-candidate reconstruction.

PR #312 is CLOSED / SUPERSEDED and retained only as historical provenance because its old key-provider boundary incorrectly required an output-manifest digest before key generation.

## Corrected key-generation boundary

Key generation requires PRE_EXECUTION, exact C binding, no pre-key output-manifest binding, complete normalized runtime identity, a matching verified-token digest, explicit synthetic provenance in the synthetic test path, and no external operational-secret environment variable.

The generated key remains inside a non-serializable lease. Only domain-separated HMAC capabilities for blinded identifiers, ordering tokens, and a commitment are exposed. The owned mutable buffer is best-effort zeroized on normal and exception exits. Python zeroization is not treated as proof that no runtime copies existed.

## Admission-policy binding correction (#316)

A second integration review identified a load-bearing trust gap: authenticating a Google-signed Confidential Space token against a caller-supplied `AttestationExpectation` proves that the token matches the supplied expectation, but does not prove that the expectation itself is the launch policy authorized before execution.

The current design therefore defines one canonical `DGAF_MODE_T_CONFIDENTIAL_SPACE_ADMISSION_POLICY_V1` identity. Its SHA-256 covers the security-critical PRE launch policy, including:

- Google Cloud Attestation issuer/OEM identity;
- Confidential Space software identity;
- required Intel TDX hardware and attester TCB;
- STABLE support requirement;
- secure-boot requirement;
- production debug state;
- disabled memory monitoring;
- restart policy `Never`;
- audience and exact subject/execution identity;
- exact service-account set;
- exact workload image digest;
- container args;
- command override;
- exact explicit non-secret environment;
- prohibition of environment override;
- reviewed clock-skew policy;
- signed `iat`/`nbf`/`exp` validation policy; and
- prohibition of operational-secret environment ingress.

The run-specific C nonce is deliberately **not** part of this policy digest because C does not exist when the policy is pre-authorized.

Synthetic R records bind the policy digest before execution. A carries the exact R policy digest. C requires A/R equality and carries the same digest. Before synthetic key acquisition, the code:

1. verifies the complete sealed C digest;
2. requires the explicit synthetic-only retention marker;
3. requires the PRE expectation binding to equal the exact C digest;
4. recomputes the canonical admission-policy digest from the supplied PRE expectation; and
5. requires exact equality with the policy digest already carried by C.

The output manifest also carries the same admission-policy digest so the completed PRE/output/POST lineage retains the policy identity.

Negative controls reject policy substitution after C, mutation of individual security-critical policy fields, tampered C bytes, a self-consistent caller-created C falsely promoted to independent retention, wrong PRE→C binding, and the earlier runtime/token/key-boundary mutations.

## Production path deliberately disabled

The direct production key entry `admit_and_acquire_mode_t_key(...)` is intentionally fail-closed at the current stage.

A caller-supplied C mapping, policy digest, or `independent_retention_verified=True` boolean would merely move the trust problem and is therefore not accepted. Production entropy generation will remain unreachable until there is a real verifier/capability that independently retrieves or authenticates the retained C/policy evidence and proves the exact authorized policy before token admission/key generation.

This is an intentional security stop, not an unfinished test assertion.

## Google OIDC trust layer

PR #313 authenticates the reviewed Google Cloud Attestation OIDC discovery/JWKS path and verifies RS256 before claims are admitted. It rejects redirects, token-supplied key URLs/objects, algorithm confusion, wrong issuer, invalid key metadata, duplicate/missing `kid`, expired tokens, and stale/outage misuse. Normal `kid` rotation is handled by one authenticated refresh. Source-document/key digests are retained.

Synthetic injected fetchers are explicitly marked `SYNTHETIC_INJECTED_FETCHER`; they cannot emit the production `HTTPS_SYSTEM_CA_HOSTNAME_VERIFIED` provenance label.

The Mode-T crypto lane is separately hash-locked for the reviewed CPython 3.12/Linux x86-64 environment rather than depending on an ambient local `cryptography` installation.

## Single-use R/A/C model

The integrated test uses deliberately synthetic R/A/C records:

- R is a sealed synthetic run reservation fixture and now binds the admission-policy SHA-256.
- A is explicitly `SYNTHETIC_GRANTED_FOR_TEST_ONLY`, binds exact R evidence, and carries the same policy digest.
- C is `CONSUMED_PRE_SECRET_SYNTHETIC`, carries the same policy digest, and records `secret_instantiation_status: NOT_EXECUTED_AT_CONSUMPTION`.
- Once C is created, the authorization ID is marked consumed before any key capability can exist.

The ledger can be snapshotted/rehydrated so tests simulate process loss. Rehydration preserves consumption and rejects a second C for the same A.

This verifies state-machine retry semantics only. `SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED` is explicit and cannot satisfy the production independent-retention requirement.

## Integrated output-manifest order

After policy-bound PRE admission and synthetic key generation, the path creates a blinded synthetic artifact containing opaque HMAC-derived identifiers/order tokens. It checks that supplied clear identifiers are absent from the serialized artifact.

The output manifest then binds:

- candidate commit SHA;
- freeze digest fixture;
- exact C digest;
- exact admission-policy digest;
- runtime-identity digest;
- workload image digest;
- tlock client digest and chain hash;
- blinded-artifact digest;
- timelock-ciphertext digest fixture;
- key commitment;
- PRE token digest; and
- execution start/completion timestamps.

Only after that manifest exists does POST bind `SHA256(manifest)` as its nonce. Final lineage verifies PRE→C, POST→manifest, same runtime identity, exact PRE token identity, and retains the policy digest.

The final synthetic record remains `PASS_SYNTHETIC_ONLY`, `real_confidential_space_admission=false`, `independent_retention_verified=false`, `freeze_established=false`, `pilot_authorized=false`, and `empirical_n=0`.

## Crash/retry coverage

Controls exercise process loss after C, after PRE, after key generation, after blinded output, and after a complete synthetic lifecycle. Every post-C path preserves consumption; later execution requires a new R/A/C identity chain. Exception-path key destruction is checked.

## Verification history

Earlier #314 head `ba490e54432c0b2bc3db423bab08725da36b8e0d` completed 10/10 returned workflows successfully, including `P4 Mode T Integrated Lifecycle`, both broader PDMAL gates, Truth Layer, Epistemic Evidence, control-state, coverage, propagation, and harness checks.

That green result predates the #316 policy-binding hardening and must not be used as proof of the newer policy-bound code. Current policy-bound head verification is tracked separately by exact SHA and workflow run.

## What this does not verify

This tranche does **not** prove:

- real Google signing-key retrieval occurred in the synthetic tests;
- a real Confidential Space token was verified;
- an authenticated GCP project/workload was admitted;
- the synthetic C model is independently retained or anti-deletion;
- the exact launch policy was independently retained in a real authorization system;
- the TEE prevents operator access to protected material in practice;
- final tlock release continuity;
- P4 closure;
- final freeze or pilot authorization; or
- empirical execution.

## Remaining gates

1. Complete exact-head CI for the current policy-bound #314 head.
2. Complete independent security review under #320; rerunning the implementation's own tests is insufficient.
3. Implement and independently verify the real retained C/policy evidence source required by #316 before production key acquisition can be enabled.
4. Reconcile #277 so intended quality/security checks are repository-enforced rather than merely green.
5. Build/review the exact Confidential Space workload image and launch configuration.
6. Execute one authenticated synthetic-only real Confidential Space admission attempt with real PRE and POST tokens.
7. Independently retrieve/reverify Google signing-key provenance, token signatures/claims, authorized policy, C/manifest nonces, workload/launch identity, and retained evidence.
8. Only then adjudicate Mode T for P4.

Until those gates are satisfied: **P4 OPEN / real execution NOT EXECUTED / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.
