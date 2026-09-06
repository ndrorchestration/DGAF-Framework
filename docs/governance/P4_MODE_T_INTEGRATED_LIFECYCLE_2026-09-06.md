# P4 Mode T — Integrated lifecycle synthetic verification

Date: 2026-09-06  
Issue: #310  
Stack: #311 claim contract → #313 Google OIDC trust layer → this lifecycle tranche  
Status: **SYNTHETIC INTEGRATION ONLY / REAL CONFIDENTIAL SPACE NOT EXECUTED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

The previous implementation had individually tested pieces but no trustworthy test of their ordering as one lifecycle. This tranche connects the reviewed boundaries without executing the real pilot:

`R → A → C → authenticated PRE_EXECUTION → in-process key capability → blinded synthetic output → output manifest → authenticated POST_EXECUTION → two-phase lineage binding`

The test uses synthetic authorization and synthetic attestation material. No test fixture is a real authorization, real Google attestation, real custody record, or empirical output.

## Corrected key-generation boundary

The stale #312 prototype required `output_manifest_sha256` before generating the Mode-T key. That is incompatible with the corrected two-phase contract because the output manifest does not exist until after the key has been generated and used to create blinded output.

The replacement `mode_t_inprocess_key.py` now accepts only a normalized **PRE_EXECUTION** admission and requires:

- claim contract PASS;
- phase exactly `PRE_EXECUTION`;
- cryptographic signature verification true;
- token digest present;
- C digest present and equal to the PRE binding digest;
- `output_manifest_sha256` absent/`None`;
- runtime-identity digest present;
- runtime identity still attests Confidential Space, `GCP_INTEL_TDX`, secure boot, production debug state, disabled memory monitoring, and restart policy `Never`;
- no externally supplied `PDMAL_BLINDING_KEY` or Mode-T key environment value.

The generated 256-bit key remains inside a non-serializable lease. The API exposes only domain-separated HMAC capabilities for blinded identifiers, ordering tokens, and a commitment. The owned mutable buffer is best-effort zeroized when the lease exits, including exception paths.

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

Only after this manifest exists does the synthetic POST token bind `SHA256(manifest)` as its nonce. The final lineage record verifies:

- PRE is bound to C;
- POST is bound to the exact output manifest;
- PRE and POST have the same runtime identity;
- PRE and POST token digests are distinct;
- manifest runtime identity equals the attested runtime identity;
- manifest PRE-token digest equals the accepted PRE token;
- POST does not substitute for PRE and PRE does not substitute for POST.

The final record is `PASS_SYNTHETIC_ONLY`, with `real_confidential_space_admission=false`, `independent_retention_verified=false`, `freeze_established=false`, `pilot_authorized=false`, and `empirical_n=0`.

## Crash/retry coverage

Dedicated controls exercise crashes at these post-C boundaries:

1. immediately after C and before PRE attestation;
2. after PRE admission and before key generation;
3. after key generation, verifying lease destruction on exception;
4. after blinded output and before POST attestation;
5. after a successful complete synthetic lifecycle.

Every case rehydrates the C ledger and proves the same authorization cannot be consumed again. A later execution would require a new R/A/C identity chain.

The key boundary separately rejects:

- POST_EXECUTION evidence presented for key generation;
- a PRE record carrying an output-manifest binding;
- an externally supplied operational blinding key environment value.

## What this verifies

If exact-head CI passes, this tranche verifies that the current synthetic implementations can be connected in the required causal order and that the modeled post-C retry rule remains fail-closed across simulated process loss.

It materially raises confidence beyond isolated unit tests because the same C digest flows into PRE attestation, the admitted PRE result gates the key, the resulting blinded artifact feeds the manifest, the manifest digest feeds POST, and the final two-phase verifier reconciles the lineage.

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

1. Complete independent security review of the signature/key-source implementation, including any findings from standards comparison.
2. Keep the Google OIDC dependency lock and exact-head CI green.
3. Replace the synthetic C retention model with the reviewed independently retained evidence path required by P4-T.
4. Build/review the exact Confidential Space workload image and launch configuration.
5. Run one authenticated synthetic-only real Confidential Space admission attempt and retain both real PRE and POST token evidence.
6. Independently retrieve/re-verify the real tokens, source keys, launch claims, C/manifest nonces, and retained provenance.
7. Only then adjudicate Mode T for P4.

Until those are completed: **P4 OPEN / real execution NOT EXECUTED / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.
