# #320 Independent Security Review — Review Checklist

> **Review ID:** 320  
> **Title:** Independent security review: Mode T production trust and Google Confidential Space admission path  
> **Frozen source manifest:** `docs/GOVERNANCE/review_packages/320_mode_t_oidc_security/SOURCE_IDENTITIES.json`  
> **Frozen source commit:** `1f0a7f1e99787777d18b1bd62fe41dce5286a102`  
> **Frozen source tree:** `ace8fce9a51b97e43e883795748ff07896292e22`  
> **Controlling state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0  
> **Final candidate:** NOT DESIGNATED (Issue #309)  
> **Reviewer requirement:** Organizationally independent (not a DGAF/PDMAL contributor)

This checklist is a review instruction, not a PASS claim. Repository tests and CI are supporting evidence only. The gate remains NOT EXECUTED until an independent reviewer verifies the frozen identities and returns a conforming review report.

---

## 0. Identity preflight — required before substantive review

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 0.1 | Repository is `ndrorchestration/DGAF-Framework` | Exact match | |
| 0.2 | Reviewed commit is `1f0a7f1e99787777d18b1bd62fe41dce5286a102` | Exact match | |
| 0.3 | Reviewed tree is `ace8fce9a51b97e43e883795748ff07896292e22` | Exact match | |
| 0.4 | Every primary-source file matches its manifest Git blob SHA | All exact | |
| 0.5 | Workflow/test evidence used by the review matches its listed blob SHA | All exact | |
| 0.6 | Any identity mismatch is treated fail-closed | `UNKNOWN` / review not gate-valid | |

Do not silently substitute a newer `main`. If a later source revision must be reviewed, create a new source manifest and review that new immutable boundary.

---

## 1. Google Confidential Space OIDC/JWKS authenticity

The repository contract under review is deliberately narrower than generic Google identity. The reviewer must independently verify whether the following values are correct for the intended Confidential Space attestation-token path:

- issuer: `https://confidentialcomputing.googleapis.com`
- discovery: `https://confidentialcomputing.googleapis.com/.well-known/openid-configuration`
- JWKS: `https://www.googleapis.com/service_accounts/v1/metadata/jwk/signer@confidentialspace-sign.iam.gserviceaccount.com`
- JWT algorithm: `RS256`

`accounts.google.com`, Firebase issuer URLs, generic OAuth certificate endpoints, JWT-supplied `jku`/`jwk`/`x5u`, and alternate caller-supplied key sources are **not** accepted substitutes by the reviewed verifier.

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 1.1 | Discovery request is exact HTTPS with system CA + hostname validation | Pass | |
| 1.2 | Discovery document issuer equals the exact Confidential Space issuer above | Pass | |
| 1.3 | Discovery `jwks_uri` equals the exact reviewed Confidential Space signer endpoint | Pass | |
| 1.4 | JWT signed issuer equals the same Confidential Space issuer | Pass | |
| 1.5 | `RS256` is required; `alg:none` and algorithm confusion are rejected | Pass | |
| 1.6 | JWT header cannot redirect key trust through `jku`, `jwk`, `x5u`, or `crit` | Pass | |

---

## 2. TLS, redirects, fetch bounds, and key rotation

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 2.1 | External discovery/JWKS fetches validate TLS certificates and hostname | Pass | |
| 2.2 | Redirects are rejected rather than followed into a new trust origin | Pass | |
| 2.3 | Discovery/JWKS documents have bounded size | Pass | |
| 2.4 | Cache TTL is bounded and expired key caches are not reused | Pass | |
| 2.5 | Missing `kid` causes at most one authenticated refresh before fail-closed rejection | Pass | |
| 2.6 | Duplicate `kid` or malformed JWK records are rejected | Pass | |

---

## 3. JWK/RSA and JWT validation

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 3.1 | JWK `kty`, `use`, and `alg` are constrained to the reviewed RSA signing contract | Pass | |
| 3.2 | RSA key size is bounded to an acceptable range and exponent is validated | Pass | |
| 3.3 | JWT compact serialization and base64url canonicalization are validated | Pass | |
| 3.4 | Duplicate JSON keys cannot alter interpretation | Pass | |
| 3.5 | Token size is bounded before expensive processing | Pass | |
| 3.6 | Signature verification occurs before claims are accepted by the attestation layer | Pass | |

---

## 4. Time and replay-relevant handling

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 4.1 | `iat`, `nbf`, and `exp` are integer-valued and consistently checked | Pass | |
| 4.2 | Clock skew is explicit and bounded | Pass | |
| 4.3 | Expired and not-yet-valid tokens fail closed | Pass | |
| 4.4 | Attestation contract enforces the reviewed maximum token lifetime | Pass | |
| 4.5 | PRE and POST use distinct phase-specific nonce bindings and distinct tokens | Pass | |

---

## 5. Confidential Space claim interpretation

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 5.1 | `aud` must equal the operator-frozen expected audience; verifier does not invent an audience | Pass | |
| 5.2 | `sub` must equal the operator-frozen exact VM subject/selfLink | Pass | |
| 5.3 | Expected workload service-account identities are exact and non-empty | Pass | |
| 5.4 | Software identity, hardware model, TCB, Secure Boot, debug status and support attributes are checked exactly as intended | Pass | |
| 5.5 | Workload image digest, args, environment, command override, restart policy and memory-monitoring state are checked against frozen expectations | Pass | |
| 5.6 | Unsupported/missing claim fields fail closed rather than being interpreted permissively | Pass | |

The reviewer must compare these assumptions with authoritative Google Confidential Space documentation and record `BLOCKED` or `UNKNOWN` for any schema/semantic mismatch rather than adapting the claims informally.

---

## 6. PRE/POST lifecycle and key-release control

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 6.1 | PRE_EXECUTION is bound to the already-consumed authorization record | Pass | |
| 6.2 | Only a successfully verified PRE attestation may gate operational key acquisition | Pass | |
| 6.3 | Operational key material cannot be returned/reused outside the intended in-process lease | Pass | |
| 6.4 | Exceptions/crashes trigger fail-closed cleanup rather than key persistence | Pass | |
| 6.5 | POST_EXECUTION is bound to the final output/evidence manifest | Pass | |
| 6.6 | PRE and POST attestations must resolve to one runtime identity while remaining distinct token events | Pass | |
| 6.7 | Retry/recovery behavior cannot skip authorization consumption, PRE admission, or POST evidence binding | Pass | |

---

## 7. Admission and launch policy binding

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 7.1 | Admission-policy identity is derived/validated from canonical policy state rather than caller assertion | Pass | |
| 7.2 | Caller-provided digest cannot bypass policy verification | Pass | |
| 7.3 | Tampered or promoted authorization/C evidence is rejected | Pass | |
| 7.4 | Workload image is digest-pinned and mutable `latest` is rejected by the launch contract | Pass | |
| 7.5 | Unreviewed Confidential Space metadata keys and operator cmd/env overrides fail closed | Pass | |
| 7.6 | Launch-contract PASS is explicitly predeclared/synthetic and cannot itself establish real admission, freeze or authorization | Pass | |

---

## 8. Sigstore and retention/custody path

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 8.1 | Sigstore/Cosign verification is bound to the intended certificate identity and trusted root | Pass | |
| 8.2 | Synthetic verification cannot be promoted to production provenance | Pass | |
| 8.3 | Retention evidence binds archive/retrieval/hash identities without treating local existence as independent custody | Pass | |
| 8.4 | Durable-retention primitives preserve artifact identity across archive and retrieval | Pass | |
| 8.5 | Any claim of independent custody identifies the actual independent actor/system and evidence boundary | Pass | |

---

## 9. CI and test evidence

| ID | Check | Expected | Finding |
|----|-------|----------|---------|
| 9.1 | Frozen workflows actually exercise the intended frozen sources | Pass | |
| 9.2 | Tests include negative/fail-closed cases for key-source manipulation, signature failure, claim mismatch, stale/invalid time, nonce mismatch and lifecycle ordering | Pass | |
| 9.3 | Test-only injected fetchers/synthetic tokens are unmistakably marked synthetic | Pass | |
| 9.4 | Passing CI is treated as supporting evidence, not as the independent review conclusion | Pass | |

---

## 10. Findings, independence, and disposition

Every substantive finding must use one of:

| Classification | Meaning |
|----------------|---------|
| `RESOLVED` | Finding is fixed and the reviewer has verified the remediation against a new explicit identity |
| `ACCEPTED WITH RATIONALE` | Residual risk is stated precisely and accepted with written rationale; does not silently imply zero risk |
| `BLOCKED` | Must be remediated before #320 can close |
| `UNKNOWN` | Available evidence is insufficient; fail closed for gate purposes |

The overall classification must be one of `PASS`, `PASS_WITH_ACCEPTED_RISK`, `BLOCKED`, or `UNKNOWN`.

A DGAF/PDMAL contributor, this assistant, or repository CI may prepare the package and supporting evidence but **cannot satisfy the organizational-independence requirement by reviewing its own work**.

---

## Output contract

Return:

`docs/GOVERNANCE/review_packages/320_mode_t_oidc_security/SECURITY_REVIEW_REPORT.json`

The report must satisfy `SOURCE_IDENTITIES.json` → `review_output_contract`, including exact reviewed repository/commit/tree, artifact identity verification, reviewer identity/organization, independence declaration, findings, overall classification, and a report SHA-256.

Until a conforming independent report exists and its findings are dispositioned, #320 remains **NOT EXECUTED / OPEN / FAIL-CLOSED** for governance purposes.

---

*Checklist corrected: 2026-09-07*  
*Controlling state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0*
