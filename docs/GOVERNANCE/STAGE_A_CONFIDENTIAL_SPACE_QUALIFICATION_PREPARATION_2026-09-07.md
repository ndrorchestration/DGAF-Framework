# Stage-A Confidential Space Qualification Preparation

> **Status:** CORRECTED SPECIFICATION DRAFT / NOT EXECUTED / NOT VERIFIED BY REAL GCP EVIDENCE.  
> **Controlling state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.  
> **Scope:** Engineering preparation for authenticated Google Cloud Confidential Space qualification only.  
> **Final v0.7.6 candidate:** NOT DESIGNATED under Issue #309.  
> **Source-review base:** `bd0b8751b9556b91a63a93c04875daac18b134fc`.  
> This document must not be used to claim P4 closure, freeze, authorization, final P9, or empirical execution.

---

## 1. Purpose and evidence boundary

Stage-A is intended to qualify the Mode-T apparatus against a **real** Confidential Space environment while keeping empirical `N=0`. It is an engineering evidence exercise, not the pilot and not scientific execution.

A future Stage-A run may be classified `PASS` only after all required real-cloud evidence is produced, retained, retrieved, cryptographically reverified, and adjudicated under the applicable governance track. Until then the state is **NOT EXECUTED**.

This corrected procedure deliberately separates three things that the earlier draft conflated:

1. the Google-provided **Confidential Space VM image**;
2. the separately built and digest-pinned **DGAF workload container** launched through `tee-image-reference`;
3. the **attestation verifier/relying party**, which verifies the returned token and the DGAF claim contract.

Official Google references reviewed for this correction:

- [Deploy Confidential Space workloads](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/deploy-workloads)
- [Retrieve and validate Confidential Space attestation tokens](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/connect-external-resources)
- [Attestation token validation endpoint fields](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/token-validation-endpoint-fields)
- [Confidential VM supported configurations](https://docs.cloud.google.com/confidential-computing/confidential-vm/docs/supported-configurations)
- [Create a Confidential VM](https://docs.cloud.google.com/confidential-computing/confidential-vm/docs/create-a-confidential-vm-instance)

---

## 2. Repository contracts that control Stage-A

Stage-A must conform to the executable repository contracts rather than inventing a parallel policy.

### 2.1 Launch contract

`experiments/pdmal_pilot/mode_t_confidential_space_launch.py` currently requires, among other exact properties:

| Property | Required value |
|---|---|
| Confidential Space image family | `confidential-space` |
| Confidential Computing type | `TDX` |
| VM maintenance policy | `TERMINATE` |
| Compute automatic restart | `false` |
| Container restart policy | `Never` |
| Secure Boot | enabled |
| Workload image | exact digest-pinned reference |
| `tee-container-log-redirect` | `false` |
| `tee-monitoring-memory-enable` | `false` |
| command override | prohibited |
| environment override | prohibited |
| additional capabilities | prohibited |
| cgroup namespace | prohibited |
| additional mounts | prohibited |

The source contract remains the authority if this prose diverges.

### 2.2 Attestation contract

`experiments/pdmal_pilot/mode_t_confidential_space_attestation.py` currently requires:

- issuer `https://confidentialcomputing.googleapis.com`;
- hardware model `GCP_INTEL_TDX`;
- `attester_tcb == ["INTEL"]`;
- Secure Boot attested true;
- debug status `disabled-since-boot`;
- `STABLE` Confidential Space support attribute;
- memory monitoring exactly disabled;
- container restart policy `Never`;
- exact workload image digest, args, environment, command override, audience, subject, and service-account set;
- no environment override;
- an attestation lifetime no longer than one hour;
- exactly one phase-specific SHA-256 nonce binding.

`PRE_EXECUTION` binds to the already-consumed authorization record C and is the only phase that may gate operational-key generation. `POST_EXECUTION` binds the same runtime identity to the final blinded output/evidence manifest.

### 2.3 Cryptographic token verification

`experiments/pdmal_pilot/mode_t_google_oidc_verifier.py` is the production token-signature entry point. It is currently bound to:

- discovery: `https://confidentialcomputing.googleapis.com/.well-known/openid-configuration`;
- issuer: `https://confidentialcomputing.googleapis.com`;
- algorithm: `RS256`;
- the reviewed Confidential Space signer JWKS endpoint;
- HTTPS with system CA and hostname verification;
- no redirects and no JWT-supplied alternate key source;
- bounded key caching with one authenticated refresh for normal `kid` rotation.

A signature-verification pass authenticates the Google token source only. The separate claim contract still decides DGAF admission.

---

## 3. Prerequisites

The following must be established before any Stage-A execution is attempted.

| Item | Requirement |
|---|---|
| GCP identity | Authenticated project/operator with permission to create the required Confidential VM resources |
| Workload service account | Dedicated service account attached to the Confidential Space VM |
| Attestation role | Workload service account has `roles/confidentialcomputing.workloadUser` |
| Container retrieval | Workload service account has `roles/artifactregistry.reader` when Artifact Registry is used |
| Operator attachment permission | Workload operator has permission equivalent to `roles/iam.serviceAccountUser` for the attached service account |
| Hardware | A currently supported Intel TDX machine type and zone |
| VM image | Google production `confidential-space` image family from project `confidential-space-images` |
| Workload image | Separate DGAF workload container referenced by immutable digest, not a mutable tag |
| Authorization binding | Exact already-consumed C-record SHA-256 available before PRE token request |
| Relying-party identity | Exact audience and expected VM subject/service-account set frozen before verification |
| Evidence custody | Predeclared retention/retrieval path; no claim of independence unless a genuinely independent actor performs it |

For Intel TDX, do **not** set `--min-cpu-platform`. Current Google supported configurations list Intel TDX on supported Intel machine families such as `c3-standard-*` and, where available, `c4-standard-*`; N2D is an AMD SEV/SEV-SNP family and must not be paired with `TDX`.

---

## 4. Workload container preparation

The DGAF workload is a normal container image authored separately from the Google Confidential Space VM image.

### 4.1 Required properties

Before launch:

1. build the Stage-A synthetic-only workload from reviewed source;
2. publish it to an approved registry;
3. resolve the immutable container digest;
4. record the full `...@sha256:<64-hex>` reference;
5. bind that exact digest into the DGAF launch and attestation expectations;
6. prohibit mutable `:latest` or branch-like references from being treated as evidence identities.

The container must enter a bootstrap state on launch and **must not generate an operational key or perform the protected action before PRE_EXECUTION attestation has passed**.

Do not base the workload Dockerfile on a guessed `gcr.io/confidential-space/...` container. Google Confidential Space is supplied as the VM image; `tee-image-reference` identifies the separate workload container.

---

## 5. TDX Confidential Space VM launch template

The exact machine type and zone must be selected from Google's then-current TDX-supported matrix at execution time and recorded in the evidence packet.

The launch shape below mirrors Google's documented Confidential Space CPU workload flow and the current repository launch contract. Placeholders are not executable evidence.

```bash
gcloud compute instances create "$INSTANCE_NAME" \
  --confidential-compute-type=TDX \
  --machine-type="$TDX_MACHINE_TYPE" \
  --maintenance-policy=TERMINATE \
  --no-restart-on-failure \
  --shielded-secure-boot \
  --image-project=confidential-space-images \
  --image-family=confidential-space \
  --metadata="^~^tee-image-reference=${WORKLOAD_IMAGE_AT_DIGEST}~tee-restart-policy=Never~tee-container-log-redirect=false~tee-monitoring-memory-enable=false" \
  --service-account="$WORKLOAD_SERVICE_ACCOUNT" \
  --scopes=cloud-platform \
  --zone="$ZONE" \
  --project="$PROJECT_ID"
```

Additional network flags may be added only after the exact egress design has been reviewed. Do not assert `--no-address` while also assuming internet reachability unless the required private/NAT path is actually configured and evidenced.

Creating the VM launches the Confidential Space environment and its configured workload container. The earlier instruction to create the VM but "not start the workload yet" was incorrect.

---

## 6. PRE_EXECUTION attestation

### 6.1 Phase meaning

PRE is an **application lifecycle boundary inside the launched workload**, before operational-key generation or the protected action. It is not a token retrieved from `gcloud compute instances describe` and it is not a pre-boot VM metadata field.

### 6.2 Token acquisition

For Google Cloud Attestation, the workload must request the token through the Confidential Space launcher:

- Unix domain socket: `/run/container_launcher/teeserver.sock`
- HTTP endpoint over that socket: `POST http://localhost/v1/token`
- token type: `OIDC`
- `audience`: exact predeclared relying-party audience set by the workload
- `nonces`: exactly one lowercase 64-character SHA-256 hex value for the DGAF PRE binding

For DGAF PRE_EXECUTION, that nonce is the exact SHA-256 of the already-consumed authorization record C expected by the attestation contract.

Conceptual request body:

```json
{
  "audience": "<exact-frozen-relying-party-audience>",
  "token_type": "OIDC",
  "nonces": ["<authorization-consumption-sha256>"]
}
```

The production workload must use an HTTP client capable of dialing the Unix socket. Do not assume the production Confidential Space environment contains a shell or `curl`.

### 6.3 Cryptographic and claim verification

Use the repository production entry point first, then the claim contract:

```python
from experiments.pdmal_pilot.mode_t_google_oidc_verifier import (
    verify_google_confidential_space_token,
)
from experiments.pdmal_pilot.mode_t_confidential_space_attestation import (
    AttestationExpectation,
    PRE_EXECUTION,
    verify_confidential_space_attestation,
)

verified = verify_google_confidential_space_token(pre_token)
pre_evidence = verify_confidential_space_attestation(
    verified.claims,
    AttestationExpectation(
        phase=PRE_EXECUTION,
        audience=frozen_audience,
        subject=frozen_subject,
        expected_service_accounts=(workload_service_account,),
        image_digest=workload_image_digest,
        binding_sha256=authorization_consumption_sha256,
        expected_args=frozen_args,
        expected_env=frozen_non_secret_env,
        expected_cmd_override=(),
    ),
    verified.token_context,
)
```

Any exception is FAIL-CLOSED. Do not generate the operational key after an incomplete or failed PRE verification.

### 6.4 PRE evidence to retain

At minimum retain, through the approved evidence path:

- raw token bytes or an equivalently retrievable immutable token record for later independent reverification;
- token SHA-256;
- `verified.evidence()` including discovery/JWKS digests and key provenance;
- normalized `pre_evidence` from the claim contract;
- exact repository commit/tree and source blobs used by verifier and claim contract;
- exact workload image digest, VM identity, service account, zone, machine type, and launch metadata;
- exact authorization-consumption SHA-256 used as the nonce binding.

Never print raw attestation tokens, keys, or protected plaintext into workload logs or serial output.

---

## 7. Stage-A synthetic action

After PRE_EXECUTION passes, Stage-A may execute only its predeclared **synthetic engineering action**. It must not collect empirical experiment observations.

The test action must preserve the existing Mode-T lifecycle invariant:

`authorization consumption → PRE attestation → operational key generation/use → blinded synthetic output/evidence manifest → POST attestation`

The exact synthetic payload, expected args, and non-secret environment must be frozen before launch because the attestation contract compares them exactly.

---

## 8. POST_EXECUTION attestation

After the final blinded output/evidence manifest exists, compute its exact SHA-256 and request a **new** Google Cloud Attestation token from the workload through the same launcher socket/endpoint.

The POST request uses:

```json
{
  "audience": "<same-exact-frozen-relying-party-audience>",
  "token_type": "OIDC",
  "nonces": ["<final-output-manifest-sha256>"]
}
```

Verify the new token cryptographically, then call `verify_confidential_space_attestation` with `phase=POST_EXECUTION` and `binding_sha256=output_manifest_sha256`.

Finally call the repository two-phase binding verifier so PRE and POST must represent the same admitted runtime identity while binding to their distinct phase records:

```python
from experiments.pdmal_pilot.mode_t_confidential_space_attestation import (
    verify_two_phase_attestation_binding,
)

binding_evidence = verify_two_phase_attestation_binding(
    pre_evidence,
    post_evidence,
    authorization_consumption_sha256=authorization_consumption_sha256,
    output_manifest_sha256=output_manifest_sha256,
)
```

The PRE and POST token records must be distinct. Failure of POST or two-phase binding does not retroactively create a PASS from successful PRE.

---

## 9. Independent retrieval and reverification

Repository verification performed by the same operator is not automatically "independent." That label may be used only when the actor/custody boundary required by the controlling governance track is actually established.

A qualifying retrieval/reverification record should establish:

1. exact evidence object identity and retention location;
2. who retained it and under what authority boundary;
3. independent retrieval of the retained bytes;
4. SHA-256 match against the original retained identities;
5. fresh cryptographic token verification through the reviewed Google discovery/JWKS path;
6. fresh claim-contract verification against the frozen expectations;
7. two-phase runtime/binding verification;
8. explicit adjudication outcome and unresolved findings.

Do not replace cryptographic JWT verification with ad hoc `openssl` commands or the generic `https://www.googleapis.com/oauth2/v3/certs` endpoint. The current DGAF verifier intentionally authenticates the Confidential Space discovery document and exact reviewed JWKS authority.

---

## 10. Leak-surface checks

Stage-A must record evidence that the launch and workload did not intentionally expose protected material through enabled observability surfaces.

Required controls include:

| Surface | Required condition |
|---|---|
| container stdout/stderr redirection | disabled by `tee-container-log-redirect=false` |
| memory monitoring | disabled by `tee-monitoring-memory-enable=false` |
| command override | absent/prohibited |
| environment override | absent/prohibited |
| additional mounts | absent/prohibited |
| additional Linux capabilities | absent/prohibited |
| cgroup namespace | absent/prohibited |
| token/key/plaintext logging | prohibited by workload implementation and review |

Read-only inspection of Cloud/serial/audit records may be used to look for accidental disclosure if those records exist, but the procedure must not require SSH into the production Confidential Space image or introduce a debug image merely to perform the check.

---

## 11. Teardown

After evidence collection completes or any FAIL-CLOSED condition occurs:

1. stop protected processing;
2. ensure the required evidence has reached the predeclared retention path;
3. delete the qualification VM and any temporary resources that the run explicitly created;
4. record deletion results and any residual resources;
5. never treat resource deletion as evidence that earlier leakage did not occur.

A concrete teardown command may be executed only with the exact Stage-A instance/zone/project identities:

```bash
gcloud compute instances delete "$INSTANCE_NAME" \
  --zone="$ZONE" \
  --project="$PROJECT_ID" \
  --quiet
```

Do not invent a temporary-disk name or storage-copy command unless that resource/path was actually created by the approved launch/evidence plan.

---

## 12. Stage-A acceptance criteria

Stage-A may be recorded as **PASS for bounded engineering qualification only** when all of the following are supported by retained evidence:

1. a real production Confidential Space VM image ran on a supported Intel TDX configuration;
2. the exact digest-pinned workload container and launch policy were attested;
3. a real PRE token was obtained through the launcher socket and passed production OIDC verification plus the DGAF PRE claim contract;
4. operational-key generation/protected synthetic action occurred only after PRE passed;
5. a real POST token was obtained after the final blinded output/evidence manifest existed;
6. POST passed production OIDC verification plus the DGAF POST claim contract;
7. PRE/POST runtime identity and phase bindings passed the repository two-phase verifier;
8. no required fail-closed predicate was bypassed;
9. the required retention/retrieval/reverification record exists for whatever governance scope is being claimed;
10. the result is adjudicated without promoting Stage-A into P4 closure, freeze, authorization, final P9, or empirical evidence.

If any required predicate is missing, malformed, unavailable, or not independently verifiable where independence is required, the result is **FAIL-CLOSED or NOT VERIFIED**, never partial PASS.

---

## 13. Explicit non-claims

Even a successful Stage-A engineering qualification does **not** by itself:

- designate the final v0.7.6 candidate under #309;
- close P4;
- complete #316 production trust/retention authority;
- replace the independent #320 security review;
- establish protocol freeze;
- grant pilot authorization;
- execute final P9;
- unblind protected results;
- increase empirical `N` above zero;
- establish scientific efficacy or robustness.

---

*Corrected source review: 2026-09-07*  
*Controlling state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0*  
*Cloud execution performed by this documentation correction: NO.*
