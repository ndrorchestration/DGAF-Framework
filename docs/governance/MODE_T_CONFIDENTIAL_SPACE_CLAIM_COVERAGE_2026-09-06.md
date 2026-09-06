# Mode-T Confidential Space signed-claim coverage review — 2026-09-06

## Status and scope

Status: **REVIEW SCAFFOLDING / CURRENT-SOURCE COVERAGE RECORD / NOT INDEPENDENT SECURITY ACCEPTANCE / NOT P4 CLOSURE**

This record maps the reviewed DGAF Mode-T Confidential Space admission implementation to the signed claims documented by Google Cloud. It exists to make omissions and policy choices reviewable before Issue #320 independent security adjudication and before any real admission attempt under Issue #310.

It does not change the verifier, select new thresholds, establish production trust roots, satisfy independently retained R/A/C authority, execute Confidential Space, or close P4.

Scientific/control boundary: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Exact source boundary reviewed

Review-base repository boundary:

- base `main`: `fe1c4be89fff9e5b3e99ca8351aaa398d8c2c9a0`
- base tree: `75f84f28d571125e9bd9a41e8f0053c7dffedf0c`
- claim contract: `experiments/pdmal_pilot/mode_t_confidential_space_attestation.py`
  - Git blob: `622bfe88116162937f4a3e6993ec66075fceb72e`
- Google OIDC verifier: `experiments/pdmal_pilot/mode_t_google_oidc_verifier.py`
  - Git blob: `7085d4c710c29821ade07304e3128ae9d8ef8dbf`
- canonical admission policy: `experiments/pdmal_pilot/mode_t_admission_policy.py`
  - Git blob: `520cd7dab7c0cb4c04c120007f84e05463243eb8`

PR #340 merged this review document as repository `main` `13d6a3b61f96e1bf87181509a852297599ca48a0`, tree `b43bce1cab6f27cca08473799ae40c7ae9616d75`. That merge advanced the repository tip by adding this documentation artifact; it did not change the three reviewed source blobs above.

The coverage classification remains source-current while those reviewed source identities and the security-critical policy semantics they represent remain unchanged. Unrelated repository-tip movement alone does not invalidate the matrix. A change to any reviewed source blob or relevant policy semantics requires a fresh review before the matrix may be treated as current for that changed implementation.

## Current Google sources

Reviewed 2026-09-06:

- Confidential Space attestation token claims:
  `https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/token-claims`
- Confidential Space attestation assertions:
  `https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/attestation-assertions`
- Create and grant access to confidential resources:
  `https://docs.cloud.google.com/confidential-computing/confidential-space/docs/create-grant-access-confidential-resources`
- Confidential Space images:
  `https://docs.cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-images`
- Deploy workloads:
  `https://docs.cloud.google.com/confidential-computing/confidential-space/docs/deploy-workloads`

Google's raw token-claims reference currently documents `hwmodel=GCP_INTEL_TDX` for Intel TDX tokens. Its Workload Identity Pool attestation-assertions surface currently documents the corresponding policy-facing hardware assertion as `INTEL_TDX`. DGAF's direct token claim contract consumes the raw Google attestation token and therefore currently requires the raw-token value `GCP_INTEL_TDX`. This distinction must not be silently normalized across interfaces.

A live 2026-09-06 read of Google's OIDC discovery document also advertised `jti` in `claims_supported`, while the dedicated Confidential Space token-claims table reviewed that day did not list `jti` among its top-level claims. This record does not infer a DGAF requirement from that cross-document difference; it is an explicit standards-consistency question for Issue #320 independent review.

## Classification vocabulary

- **ENFORCED** — current DGAF admission rejects the token when the required value or shape is absent or mismatched.
- **ENFORCED + RUNTIME-IDENTITY-BOUND** — enforced and included in `runtime_identity_sha256` for PRE/POST lineage equality.
- **ENFORCED + POLICY-BOUND** — the acceptance rule or fixed ceiling is included in the canonical admission-policy identity; the observed token value is not thereby claimed to be part of `runtime_identity_sha256`.
- **ENFORCED + PHASE-BINDING** — enforced as a run-phase cryptographic binding rather than as a stable runtime identity field.
- **ENFORCED + RETAINED EVIDENCE** — enforced and emitted in normalized evidence, but the observed value is not part of `runtime_identity_sha256`.
- **CRYPTOGRAPHIC PREREQUISITE** — authenticated before workload claims are accepted, but not itself a workload-policy claim.
- **SIGNED / REVIEW DECISION OPEN** — Google signs or exposes the claim, but current DGAF acceptance does not bind it; Issue #320/#310 must decide whether that is appropriate.
- **INTENTIONALLY VERSION-ABSTRACTED** — exact value is not pinned because the current policy deliberately uses a documented support-state abstraction.
- **CONDITIONAL / NOT CURRENT PATH** — relevant only if the selected deployment mechanism uses that feature.

## Coverage matrix

| Claim or evidence surface | Current DGAF treatment | Current requirement / interpretation | Review note |
| --- | --- | --- | --- |
| JWT signature / Google issuer key provenance | CRYPTOGRAPHIC PREREQUISITE | Separate OIDC verifier must authenticate the token before claim admission | Signature success is not workload-policy acceptance |
| `iss` | ENFORCED | exact Google Cloud Attestation issuer | Other attestation issuers are not accepted by this path |
| `oemid` | ENFORCED | Google PEN `11129` | Exact Google attestation-service identity |
| `aud` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact predeclared audience | Also included in canonical admission-policy identity |
| `sub` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact predeclared Confidential VM subject | Raw token `sub` is a fully qualified VM selfLink and therefore carries project/zone/instance identity indirectly |
| `google_service_accounts` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact predeclared service-account set | Also included in canonical admission-policy identity |
| `swname` | ENFORCED + RUNTIME-IDENTITY-BOUND | `CONFIDENTIAL_SPACE` | Normalized as `software_identity` in runtime identity |
| `hwmodel` | ENFORCED + RUNTIME-IDENTITY-BOUND | raw token value `GCP_INTEL_TDX` | Also policy-bound; do not confuse with the WIP assertion spelling `INTEL_TDX` |
| `attester_tcb` | ENFORCED + RUNTIME-IDENTITY-BOUND | exactly `['INTEL']` | Establishes source of TDX attestation evidence, not real-time TCB freshness |
| `secboot` | ENFORCED + RUNTIME-IDENTITY-BOUND | `true` | Normalized as `secure_boot=true` |
| `dbgstat` | ENFORCED + RUNTIME-IDENTITY-BOUND | `disabled-since-boot` | Also policy-bound; production image only |
| `iat`, `nbf`, `exp` | ENFORCED + RETAINED EVIDENCE | integer time validity with reviewed skew policy | Emitted as evidence; actual timestamps are not part of runtime identity |
| `exp - iat` | ENFORCED + POLICY-BOUND | maximum `3600` seconds | Observed lifetime is retained; fixed ceiling is bound by PR #338 into policy identity |
| `eat_nonce` | ENFORCED + PHASE-BINDING | exactly one expected SHA-256 phase binding | PRE binds C; POST binds the emitted output/evidence manifest |
| `submods.confidential_space.support_attributes` | ENFORCED + RUNTIME-IDENTITY-BOUND | must contain `STABLE` | Policy and runtime identity bind the required support attribute, not the entire observed list |
| `submods.confidential_space.monitoring_enabled.memory` | ENFORCED + RUNTIME-IDENTITY-BOUND | exactly `false` | Prevents admission when configured memory monitoring is active |
| `submods.container.image_digest` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact reviewed image digest | Current workload authorization identity is digest-bound |
| `submods.container.args` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact predeclared arguments | Run-specific non-secret inputs only |
| `submods.container.cmd_override` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact reviewed value | Current production policy expects no unreviewed command substitution |
| `submods.container.env` | ENFORCED + RUNTIME-IDENTITY-BOUND | exact explicit non-secret environment | Operational secrets are not authorized through this surface |
| `submods.container.env_override` | ENFORCED + RUNTIME-IDENTITY-BOUND | empty object | Operator environment substitution fails closed |
| `submods.container.restart_policy` | ENFORCED + RUNTIME-IDENTITY-BOUND | `Never` | Supports single-use / no-silent-retry lifecycle semantics |
| PRE/POST runtime identity equality | ENFORCED | exact `runtime_identity_sha256` equality | Prevents phase substitution across different accepted runtime identities |
| PRE/POST token distinctness and ordering | ENFORCED | distinct token digests and nondecreasing issue time | Lifecycle evidence, not a stable runtime identity field |

## Signed claims not currently bound into DGAF acceptance identity

### Intel TDX TCB status and date

Google's current raw token reference documents signed `tdx.gcp_attester_tcb_status` and `tdx.gcp_attester_tcb_date` fields.

Current DGAF treatment: **SIGNED / REVIEW DECISION OPEN**.

The code does not currently require or bind either field. No threshold is introduced here. Google explicitly states that `gcp_attester_tcb_status` indicates whether the TDX TCB matched Intel reference values when Google began its firmware rollout, but does not guarantee real-time fleet freshness. Treating this field as a real-time patch/freshness oracle would therefore overstate its documented semantics.

Independent review should decide whether final retained evidence must preserve these fields, whether their absence should fail admission, and whether any status policy is supportable without importing a stronger freshness claim than Google makes.

### Exact Confidential Space image version: `swversion`

Current DGAF treatment: **INTENTIONALLY VERSION-ABSTRACTED**.

DGAF currently requires production debug status plus `STABLE` support status rather than an exact `swversion`. Google's attestation-assertions documentation recommends `support_attributes` instead of exact `swversion` for targeting supported image versions, and Google describes `STABLE` as supported and monitored for vulnerabilities.

This is a deliberate policy choice, not evidence that exact image version can never matter. Independent review may require an additional retained `swversion` field for provenance without making it an acceptance pin.

### Explicit GCE project / instance / zone subclaims

Google separately exposes `submods.gce.project_id`, `project_number`, `instance_id`, `instance_name`, and `zone` assertions. The raw token `sub` is itself a fully qualified VM selfLink containing project, zone, and instance identity.

Current DGAF treatment: **SIGNED / REVIEW DECISION OPEN** for the separate GCE subclaims while exact `sub` is ENFORCED.

This record does not declare the separate fields redundant. Independent review must decide whether exact `sub` is sufficient for the intended threat model or whether selected GCE subclaims should also be explicitly bound and cross-checked to prevent inconsistent signed-claim combinations.

### Container `image_id` and `image_reference`

Current DGAF treatment: **SIGNED / REVIEW DECISION OPEN**.

The current admission identity uses exact `image_digest`, which is content-addressed, while `image_reference` is a repository/tag location and `image_id` is a distinct documented identifier. Independent review should determine whether preserving either field improves provenance or inconsistency detection without replacing the digest as the authorization identity.

### Container `image_signatures`

Current DGAF treatment: **CONDITIONAL / NOT CURRENT PATH**.

Google documents container image signatures as an alternate/supplementary workload authorization surface configured through signed-image repositories. The current DGAF policy is exact-image-digest bound and has no separately approved container-signing authority. `image_signatures` must not be treated as accepted merely because the claim can appear in a Google token.

If a signed-image path is adopted later, signer/key identity and update policy require a separate authority decision and candidate rotation where applicable.

## Review questions that remain open

Issue #320 / the eventual independent reviewer should explicitly adjudicate at least these questions:

1. Should TDX `gcp_attester_tcb_status` and `gcp_attester_tcb_date` be mandatory retained evidence, mandatory admission claims, or provenance-only fields?
2. If a TCB status becomes admission-relevant, what externally justified semantics avoid pretending it establishes real-time fleet freshness?
3. Is exact `sub` sufficient VM identity binding, or should selected GCE subclaims be required and cross-consistency checked?
4. Should `swversion` be retained for provenance while `STABLE` remains the acceptance policy?
5. Should `image_id` or `image_reference` be cross-checked in addition to the exact image digest?
6. Is an exact-digest workload identity sufficient for this cycle, or is a separately governed image-signature authority required?
7. Are any signed claims accepted by Google but omitted here security-critical for DGAF's specific no-operator-secret / no-silent-retry threat model?
8. Does the live OIDC discovery document's advertised `jti` support have security-relevant semantics for Confidential Space tokens that are omitted or documented elsewhere, and should DGAF retain or enforce anything only if current Google/JOSE requirements justify it?

## Anti-drift rules

Do not infer any of the following from this matrix:

- absence from the matrix means a claim is absent from a Google token;
- presence in a signed token means DGAF accepts or relies on the claim;
- an ENFORCED row has received independent security review;
- `gcp_attester_tcb_status` proves real-time platform freshness;
- `STABLE` proves zero vulnerability or immutable software identity;
- exact image digest proves signer authority;
- exact `sub` automatically proves the separate GCE claim set is mutually consistent;
- green CI or synthetic fixtures establish real Confidential Space admission;
- unrelated repository-tip movement invalidates or refreshes a source-bound review without checking the reviewed source identities;
- this record satisfies #316 independently retained production R/A/C authority;
- this record satisfies #320 independent review;
- this record closes #310 or P4.

Any final production policy change prompted by this review must be implemented and freshly candidate-bound before final candidate designation under #309.

## Current disposition

The current implementation has broad fail-closed coverage over the claims it deliberately selects, but the signed-claim universe is larger than the present acceptance identity. The remaining omissions are explicit review decisions rather than invisible assumptions. This matrix remains current only for the reviewed source identities and semantics named above; it is not a moving endorsement of future source changes.

**#310 OPEN · #316 OPEN · #320 OPEN · #295 OPEN · final candidate NOT DESIGNATED · PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**
