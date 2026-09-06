# P4 Mode T — Confidential Space Admission Boundary

**Status:** DESIGN + SYNTHETIC CONTRACT ONLY / P4 OPEN / NOT EXECUTED  
**Scientific state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Decision

Ordinary GitHub-hosted runners are not accepted as the final Mode-T custody substrate for this cycle because the required analyst/admin live-memory control separation has not been established.

Google Confidential Space production advances only to a bounded admission proof. This is a conditional engineering decision, not P4 closure.

If real attestation evidence cannot satisfy the contract in Issue #310, Mode T is rejected for this cycle and an admissible H/I custody path must be used.

## Why this substrate is materially different

Google documents Confidential Space as a trusted execution environment intended to protect a workload and its secrets from an untrusted workload operator, including an operator with broad project-administrator powers. Its production image disables remote access, uses protected ephemeral storage and encrypted memory, measures the workload and configuration, and exposes remote-attestation claims describing the software, hardware, container image, monitoring state, and launch configuration.

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
3. independently verified runtime attestation from the accepted execution;
4. exact run-specific nonce/data bindings;
5. retained evidence proving the key never crossed an operator-visible surface.

A different image, debug image, launch argument, override, monitoring configuration, restart configuration, or mismatched run binding is a different execution and must be rejected.

## Required attestation contract

The first admission attempt is intentionally narrow. Required claims include:

- issuer `https://confidentialcomputing.googleapis.com`;
- exact predeclared custom audience;
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
- exactly two unique SHA-256 nonce bindings:
  - digest of authorization-consumption record C;
  - digest of the emitted Mode-T output/evidence manifest.

The current Google token-claims reference explicitly documents `aud`, `secboot`, `hwmodel`, `attester_tcb`, `dbgstat`, `eat_nonce`, `confidential_space.monitoring_enabled`, `container.args`, `container.cmd_override`, `container.env`, `container.env_override`, `container.image_digest`, and `container.restart_policy`. The verifier treats omission or mismatch of the selected security-critical values as rejection rather than relying on cloud defaults.

Token parsing is not signature verification. A caller must cryptographically authenticate the attestation token before the claim contract can pass.

## Secret lifecycle requirement

The operational blinding key must be generated inside the accepted TEE process with at least 256 bits of CSPRNG entropy. It must not be supplied through environment variables, command-line arguments, disk files, logs, workflow outputs, or diagnostics.

The intended protected lifecycle is:

`C consumed -> attested workload -> in-process CSPRNG key -> blinded execution -> timelock wrap -> blinded artifact + commitments + attestation evidence -> key zeroization`

Only non-secret provenance, blinded artifacts, timelock ciphertext/commitments, and attestation evidence may leave the TEE before release.

## Operator powers that remain

The operator can still cause denial of service by terminating the VM, changing networking, constraining resources, or launching an inadmissible workload. DGAF does not require the TEE to prevent DoS.

The admission requirement is narrower and load-bearing: those powers must not reveal the accepted run's key/mapping/plaintext or convert an altered execution into an accepted one.

A crash or failure after C consumes the run authorization. It cannot silently retry into an accepted run. A later attempt requires a new reservation/authorization/consumption chain.

## Offline verifier in this branch

`experiments/pdmal_pilot/mode_t_confidential_space_attestation.py` implements only the fail-closed claim contract after a separate cryptographic token-verification layer reports success.

Its synthetic negative controls reject:

- unverified token signature;
- wrong issuer or audience;
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
- wrong, duplicate, or missing nonce bindings;
- expired or not-yet-valid tokens;
- malformed token digest or missing claim groups.

Passing these tests establishes only that the local acceptance predicate fails closed on the reviewed synthetic fixtures.

## Real admission evidence still required

Before Mode T can be accepted:

1. add the in-process Mode-T key provider without changing H/I behavior;
2. extend leakage tests to the TEE path;
3. independently review the exact container image and launch policy;
4. perform one real Confidential Space run using synthetic fixtures only;
5. independently authenticate and re-evaluate its attestation token;
6. independently retrieve/re-hash the output evidence;
7. verify no protected secret appears in any observable surface;
8. adjudicate PASS, FAIL, or UNKNOWN against Issue #310.

A PASS permits Mode-T integration into the final-candidate reconstruction lane. FAIL or UNKNOWN rejects Mode T for this cycle.

## Non-effects

This document and the synthetic verifier do not establish P4 custody, designate the final candidate, select W, close P7/P8/P9, create freeze F, grant pilot authorization, execute empirical work, unblind anything, or increase empirical N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
