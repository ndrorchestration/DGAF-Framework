# Stage-A Confidential Space Qualification Preparation

> **Controlling state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. 
> **Scope:** Engineering preparation for authenticated GCP Confidential Space execution. 
> **What this is:** Specification and procedure only. No cloud actions, no key material, no empirical evidence. 
> **Final candidate:** NOT DESIGNATED (Issue #309). 
> **Live main:** `c2dd87eda2b92f72c8e06fe225de833e0c2d319a`

---

## 1. Purpose and boundary

Stage-A proves apparatus viability against a **real** Confidential Space environment while keeping `N=0`. It is not the pilot, not freeze, not authorization, not P4 closure. It is a controlled qualification run whose only acceptable outcomes are:

- **PASS** — real PRE/POST attestation verified, no key/plaintext leaks detected, evidence independently retrievable.

- **FAIL-CLOSED** — any step cannot be completed or verified; record the exact failure mode; do not proceed to candidate designation.

Stage-A does not generate empirical observations. It generates engineering evidence that the apparatus can execute end-to-end in a real TEE.

---

## 2. Pre-requisites

 |  Item  |  Requirement  |
 | ------ | ------------- |
 |  GCP project  |  Authenticated project with Confidential Space API enabled  |
 |  Service account  |  Dedicated SA with `roles/confidentialspace.operator` and minimum required IAM  |
 |  Network  |  Outbound HTTPS to `confidentialcomputing.googleapis.com`, `oauth2.googleapis.com`, `accounts.google.com`  |
 |  tlock binary  |  Verified SHA-256 `0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57`  |
 |  Cosign binary  |  Pinned and verified per #299  |
 |  Candidate source  |  Exact tree to be designated under #309 (post-designation only)  |

---

## 3. Synthetic-only workload image

### 3.1 Image requirements

The Stage-A workload image must be digest-pinned and built from a deterministic source. No external runtime dependencies.

```dockerfile
# Stage-A synthetic-only workload
FROM gcr.io/confidential-space/minimal:latest
LABEL org.dgaf.stage_a.workload="synthetic-only"
LABEL org.dgaf.stage_a.purpose="apparatus viability qualification"

# Copy synthetic workload
COPY workload/ /app/
WORKDIR /app

# Run as non-root
USER 65534:65534

# No entrypoint override allowed by launch contract
ENTRYPOINT ["/app/synthetic_workload"]
CMD ["--mode", "stage-a-qualification"]
```

### 3.2 Digest pinning

```bash
# Build and pin
docker build -t stage-a-workload:under-test .
DIGEST=$(docker inspect stage-a-workload:under-test --format='{{index .RepoDigests 0}}')
echo "Pinned digest: $DIGEST"

# Record in launch contract
# digest_pin: sha256:<exact-image-sha256>
```

### 3.3 Restrictions

- **No debug symbols** in production image

- **No shell access** in runtime container

- **No network egress** except to Google attestation endpoints

- **No environment variable overrides** permitted by launch policy

- **No command-line overrides** permitted by launch policy

- **Memory monitoring disabled** (`tee-monitoring-memory-enable: false`)

---

## 4. GCP configuration

### 4.1 Required exact identities

```yaml
# stage_a_gcp_config.yaml — fill with real values at execution time
project_id: <exact-gcp-project-id>
zone: <exact-zone>
region: <exact-region>
machine_type: n2d-standard-2
min_cpu_platform: "AMD Rome"

service_account: <sa-name>@<project-id>.iam.gserviceaccount.com
service_account_scopes:

  - https://www.googleapis.com/auth/cloud-platform

confidential_space:
  tee_type: "SEV"
  # or "TDX" per REQUIREMENTS
  compute_type: "TDX"
  restart_policy: "Never"
  debug_mode: false
  memory_monitoring: false

network:
  no_external_ip: true
  # or exact VPC connector if egress required
```

### 4.2 Launch contract binding

The launch contract (`mode_t_confidential_space_launch.py`) validates:

 |  Field  |  Required value  |
 | ------- | ---------------- |
 |  `tee.launch_policy.allow_capabilities`  |  `false`  |
 |  `tee.launch_policy.allow_cgroups`  |  `false`  |
 |  `tee.launch_policy.allow_cmd_override`  |  `false`  |
 |  `tee.launch_policy.allow_env_override`  |  `""`  |
 |  `tee.launch_policy.allow_mount_destinations`  |  `""`  |
 |  `tee.launch_policy.log_redirect`  |  `never`  |
 |  `tee.launch_policy.monitoring_memory_allow`  |  `never`  |
 |  `tee-restart-policy`  |  `Never`  |
 |  `tee-container-log-redirect`  |  `false`  |
 |  `tee-monitoring-memory-enable`  |  `false`  |

---

## 5. PRE attestation procedure

### 5.1 Trigger

Execute `gcloud compute instances create` with the exact configuration above. Do **not** start the workload yet.

### 5.2 Retrieve PRE token

```bash
# Retrieve PRE attestation token from instance metadata
PRE_TOKEN=$(gcloud compute instances describe \
  <instance-name> \
  --zone=<zone> \
  --format='value(confidentialSpaceConfig.attestationToken)')
```

### 5.3 Verify PRE token

```python
from experiments.pdmal_pilot.mode_t_google_oidc_verifier import GoogleOIDCVerifier
from experiments.pdmal_pilot.mode_t_confidential_space_attestation import (
    verify_attestation_token,
    PRE_EXECUTION,
)

verifier = GoogleOIDCVerifier()
claims = verifier.verify(PRE_TOKEN)

# Verify PRE_EXECUTION phase
result = verify_attestation_token(
    claims=claims,
    phase=PRE_EXECUTION,
    expected_subject=<exact-instance-self-link>,
    expected_service_account=<sa-email>,
    expected_image_digest=<pinned-image-digest>,
)
assert result.phase == PRE_EXECUTION
assert result.debug_status == "disabled-since-boot"
assert result.restart_policy == "Never"
assert result.hardware_model == "GCP_INTEL_TDX"
```

### 5.4 Record PRE evidence

```bash
# Independent retrieval: save token and claims to operator-controlled storage
mkdir -p /workspace/stage_a_evidence/pre
echo "$PRE_TOKEN" > /workspace/stage_a_evidence/pre/token.b64
echo "$CLAIMS_JSON" > /workspace/stage_a_evidence/pre/claims.json

# Cryptographic reverification
sha256sum /workspace/stage_a_evidence/pre/token.b64 > /workspace/stage_a_evidence/pre/token.sha256
```

---

## 6. Workload execution

### 6.1 Start workload

```bash
gcloud compute instances start <instance-name> --zone=<zone>
```

### 6.2 Synthetic workload behavior

The synthetic workload:

- Generates deterministic output from sealed seed

- Writes output to `/workspace/output/` (ephemeral, in-memory only)

- Does **not** write to persistent disk

- Does **not** make external network calls

- Does **not** spawn child processes

- Exits with code 0 on success, non-zero on apparatus failure

### 6.3 Monitoring during execution

 |  Check  |  Method  |  Pass condition  |
 | ------- | -------- | ---------------- |
 |  No key material in logs  |  `gcloud compute ssh` with metadata inspection  |  No private key material in serial port 1-4  |
 |  No plaintext in environment  |  Instance metadata API  |  No workload secrets in environment variables  |
 |  Memory monitoring disabled  |  Launch policy audit  |  `tee-monitoring-memory-enable: false`  |
 |  No unauthorized mounts  |  Launch policy audit  |  `allow_mount_destinations: ""`  |
 |  No cmd/env override  |  Launch policy audit  |  `allow_cmd_override: false`, `allow_env_override: ""`  |

---

## 7. POST attestation procedure

### 7.1 Retrieve POST token

```bash
POST_TOKEN=$(gcloud compute instances describe \
  <instance-name> \
  --zone=<zone> \
  --format='value(confidentialSpaceConfig.attestationToken)')
```

### 7.2 Verify POST token

```python
result = verify_attestation_token(
    claims=claims,
    phase=POST_EXECUTION,
    expected_subject=<exact-instance-self-link>,
    expected_service_account=<sa-email>,
    expected_image_digest=<pinned-image-digest>,
)
assert result.phase == POST_EXECUTION
# Same hardware/debug/restart assertions as PRE
```

### 7.3 Record POST evidence

```bash
mkdir -p /workspace/stage_a_evidence/post
echo "$POST_TOKEN" > /workspace/stage_a_evidence/post/token.b64
echo "$CLAIMS_JSON" > /workspace/stage_a_evidence/post/claims.json
sha256sum /workspace/stage_a_evidence/post/token.b64 > /workspace/stage_a_evidence/post/token.sha256
```

---

## 8. Evidence retrieval and independent reverification

### 8.1 Operator-controlled storage

All evidence must be written to storage the operator controls, not to instance-local or GCP-managed storage:

- Preferred: Operator-controlled Cloud Storage bucket with uniform bucket-level access

- Alternative: Local filesystem with independent hash verification

- Prohibited: Instance persistent disks, GCP-managed metadata, workload stdout/stderr as sole record

### 8.2 Independent reverification steps

```bash
# 1. Verify token SHA-256 matches recorded hash
echo "<expected-sha256>  token.b64"  |  sha256sum -c -

# 2. Verify JWT signature independently
openssl ssl -verify <trusted-root-pem> -inform PEM -in <jwt-header>.pem

# 3. Verify issuer and kid
ISSUER=$(echo "$POST_TOKEN"  |  cut -d. -f1  |  base64 -d  |  jq -r .iss)
KID=$(echo "$POST_TOKEN"  |  jq -r .kid)
echo "Issuer: $ISSUER, Kid: $KID"

# 4. Verify JWKS consistency
curl -s https://www.googleapis.com/oauth2/v3/certs  |  jq -r ".[]  |  select(.kid==\"$KID\")"
```

### 8.3 Leak-surface verification

 |  Surface  |  Check  |  Pass condition  |
 | --------- | ------- | ---------------- |
 |  Serial ports 1-4  |  `gcloud compute instances get-serial-port-output`  |  No key material  |
 |  Instance metadata  |  `gcloud compute instances describe`  |  No workload secrets  |
 |  Cloud Audit Logs  |  `gcloud logging read`  |  No private key material  |
 |  Cloud Storage (if used)  |  Bucket ACL audit  |  Operator-controlled only  |

---

## 9. Teardown

```bash
# Stop and delete instance — do NOT retain disk
gcloud compute instances delete <instance-name> --zone=<zone> --quiet

# Delete any temporary disks
gcloud compute disks delete <disk-name> --zone=<zone> --quiet

# Archive evidence to operator-controlled storage
gsutil cp -r /workspace/stage_a_evidence gs://<operator-bucket>/stage_a_<timestamp>/

# Verify archive integrity
gsutil hash gs://<operator-bucket>/stage_a_<timestamp>/*  |  sha256sum
```

---

## 10. Acceptance criteria

Stage-A is **PASS** only when:

1. Real PRE attestation token obtained from live Confidential Space instance and independently verified.

2. Real POST attestation token obtained after workload execution and independently verified.

3. Pinned workload image digest confirmed in both attestation claims.

4. TDX/Secure Boot/non-debug/Never-restart verified in both PRE and POST.

5. No protected key material or plaintext leaks detected on any observable surface.

6. All evidence independently retrievable and cryptographically reverifiable from operator-controlled storage.

7. Every step documented with exact GCP identities, timestamps, and SHA-256 hashes.

Stage-A is **FAIL-CLOSED** if any criterion cannot be met. No partial credit. No synthetic substitution.

---

## 11. What Stage-A does NOT do

- Does **not** designate the final candidate (#309)

- Does **not** close P4

- Does **not** establish production trust authority (#316)

- Does **not** replace #320 independent security review

- Does **not** constitute freeze or authorization

- Does **not** generate empirical observations or transition N=0 → N>0

- Does **not** prove long-term retention; proves only that the apparatus can execute in a real TEE

---

*Document written: 2026-09-07* 
*Controlling state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0* 
*No scientific-state transition claimed.*
