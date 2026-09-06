# P4 Mode T — Confidential Space Admission Boundary

**Status:** DESIGN + SYNTHETIC CONTRACT ONLY / P4 OPEN / NOT EXECUTED  
**Scientific state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Decision

Ordinary GitHub-hosted runners are not accepted as the final Mode-T custody substrate for this cycle because the required analyst/admin live-memory control separation has not been established.

Google Confidential Space production advances only to a bounded admission proof. This is a conditional engineering decision, not P4 closure.

If real attestation evidence cannot satisfy the contract in Issue #310, Mode T is rejected for this cycle and an admissible H/I custody path must be used.

## Why this substrate is materially different

Google documents Confidential Space as a trusted execution environment intended to protect a workload and its secrets from an untrusted workload operator, including an operator with broad project-administrator powers. Its production image disables remote access, uses protected ephemeral storage and encrypted memory, measures the workload and configuration, and exposes remote-attestation claims describing the software, hardware, VM identity, validated service accounts, container image, monitoring state, and launch configuration.

The relevant source documents reviewed on 2026-09-06 are:

- Confidential Space security overview: <https://docs.cloud.google.com/docs/security/confidential-space>
- Confidential Space overview: <https://docs.cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview>
- Attestation token claims: <https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/token-claims>
- Attestation assertions: <https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/attestation-assertions>
- Launch policies: <https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/launch-policies>
- External-resource attestation/data binding: <https://docs.cloud.google.com/confidential-computing/confidential-space/docs/connect-external-resources>

These sources support testing a Mode-T custody claim. They do not themselves prove DGAF's eventual workload, configuration, or execution satisfies that claim.

## Solo-operator trust boundary

The same person can hold workload-author, workload-operator, and resource-owner powers before freeze. Therefore DGAF must not treat a mutable IAM policy or cloud-project configuration controlled by that person as sufficient custody evidence.

Instead, final acceptance must bind to:

1. the exact pre-frozen workload image digest and source/toolchain identity;
2. the exact final DGAF candidate/freeze tuple;
3. the exact Confidential VM subject and validated service-account set;
4. independently verified runtime attestation from the accepted execution;
5. phase-specific run/data nonce bindings;
6. retained evidence proving the key never crossed an operator-visible surface.

A different VM, service account, image, debug image, launch argument, override, monitoring configuration, restart configuration, or mismatched run binding is a different execution and must be rejected.

## Required attestation claims

The first admission attempt is intentionally narrow. Each accepted token must bind:

- issuer `https://confidentialcomputing.googleapis.com`;
- Google Cloud OEM ID `11129`;
- exact predeclared custom audience;
- exact VM `sub` subject;
- exact validated `google_service_accounts` set;
- software identity `CONFIDENTIAL_SPACE`;
- hardware model `GCP_INTEL_TDX`;
- `attester_tcb` exactly `['INTEL']` for the selected TDX policy;
- Secure Boot attested true;
- debug state `disabled-since-boot`;
- production support attributes including `STABLE`;
- Confidential Space memory monitoring exactly disabled;
- exact frozen workload image digest;
- exact full container `args` vector;
- exact expected command override list;
- exact expected non-secret environment inputs;
- no environment overrides;
- restart policy `Never`;
- valid `iat`, `nbf`, and `exp` bounds;
- exactly one phase-specific SHA-256 nonce.

The current Google token-claims reference explicitly documents these top-level and container claims. The verifier treats omission or mismatch of the selected security-critical values as rejection rather than relying on cloud defaults.

Token parsing is not signature verification. A caller must cryptographically authenticate each attestation token before the claim contract can pass.

## Two-phase attestation lifecycle

A single pre-execution token cannot bind the final output-manifest digest because that manifest does not yet exist. Requiring it would create a circular dependency. The contract therefore uses two distinct, non-interchangeable attestations.

### Phase 1 — PRE_EXECUTION

After reservation/instance identity is established and authorization record C is consumed, request a custom attestation token whose single nonce is:

`SHA256(C)`

The token must satisfy the complete runtime/launch predicate above. Only a `PRE_EXECUTION` PASS is eligible to gate in-process Mode-T key generation.

### Phase 2 — POST_EXECUTION

After the blinded output/evidence manifest exists, request a second independently authenticated attestation token from the same admitted runtime. Its single nonce is:

`SHA256(output/evidence manifest)`

The token must satisfy the same runtime/launch predicate and must be classified `POST_EXECUTION`.

### Pair acceptance

The two normalized attestation records are accepted as one lineage only if:

- both cryptographic signatures were independently verified;
- the first phase is PRE_EXECUTION and the second POST_EXECUTION;
- C and manifest bindings match their exact expected digests;
- both tokens produce the same runtime-identity SHA-256, including VM subject, service accounts, image, hardware, monitoring state, argv, environment, overrides, and restart policy;
- the token digests are distinct;
- the post-execution token was issued no earlier than the pre-execution token.

This converts the prior circular two-nonce design into a sequential evidence chain without weakening the runtime identity requirement.

## Secret lifecycle requirement

The operational blinding key must be generated inside the accepted TEE process with at least 256 bits of CSPRNG entropy. It must not be supplied through environment variables, command-line arguments, disk files, logs, workflow outputs, or diagnostics.

The intended protected lifecycle is:

`C consumed -> PRE_EXECUTION attestation -> in-process CSPRNG key -> blinded execution -> timelock wrap -> blinded artifact + commitments -> output manifest -> POST_EXECUTION attestation -> key zeroization / evidence retention`

Only non-secret provenance, blinded artifacts, timelock ciphertext/commitments, and attestation evidence may leave the TEE before release.

## Operator powers that remain

The operator can still cause denial of service by terminating the VM, changing networking, constraining resources, or launching an inadmissible workload. DGAF does not require the TEE to prevent DoS.

The admission requirement is narrower and load-bearing: those powers must not reveal the accepted run's key/mapping/plaintext or convert an altered execution into an accepted one.

A crash or failure after C consumes the run authorization. It cannot silently retry into an accepted run. A later attempt requires a new reservation/authorization/consumption chain.

## Offline verifier in this branch

`experiments/pdmal_pilot/mode_t_confidential_space_attestation.py` implements the fail-closed claim contract after a separate cryptographic token-verification layer reports success, plus a two-phase pairing check.

Its synthetic negative controls reject, among other cases:

- unverified token signature;
- wrong issuer, OEM ID, audience, VM subject, or validated service account;
- wrong software identity;
- wrong hardware model or attester root;
- Secure Boot false;
- debug image;
- missing STABLE support;
- memory monitoring enabled;
- wrong workload image digest;
- wrong full container argument vector;
- command override mismatch;
- unexpected environment input or environment override;
- restart policy other than Never;
- wrong, multiple, or missing phase nonce;
- expired or not-yet-valid tokens;
- malformed token digest or missing claim groups;
- reversed attestation phases;
- pre/post runtime-identity drift;
- same-token replay across phases;
- post-execution token timestamp preceding the pre-execution token;
- wrong expected C or output-manifest binding.

Passing these tests establishes only that the local acceptance predicate fails closed on the reviewed synthetic fixtures.

## Real admission evidence still required

Before Mode T can be accepted:

1. add the in-process Mode-T key provider without changing H/I behavior;
2. extend leakage tests to the TEE path;
3. independently review the exact container image and launch policy;
4. perform one real Confidential Space run using synthetic fixtures only;
5. independently authenticate and re-evaluate both attestation phases;
6. independently retrieve/re-hash the output evidence;
7. verify no protected secret appears in any observable surface;
8. adjudicate PASS, FAIL, or UNKNOWN against Issue #310.

A PASS permits Mode-T integration into the final-candidate reconstruction lane. FAIL or UNKNOWN rejects Mode T for this cycle.

## Non-effects

This document and the synthetic verifier do not establish P4 custody, designate the final candidate, select W, close P7/P8/P9, create freeze F, grant pilot authorization, execute empirical work, unblind anything, or increase empirical N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
