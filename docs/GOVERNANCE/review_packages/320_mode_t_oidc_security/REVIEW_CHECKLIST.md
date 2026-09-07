# #320 Independent Security Review — Review Checklist

> **Review ID:** 320 
> **Title:** Independent security review: Mode T Google OIDC verifier 
> **Frozen source identities:** `docs/governance/review_packages/320_mode_t_oidc_security/SOURCE_IDENTITIES.json` 
> **Controlling state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 
> **Final candidate:** NOT DESIGNATED (Issue #309) 
> **Reviewer requirement:** Organizationally independent (not DGAF/PDMAL contributor)

---

## Review categories

### 1. Google OIDC/JWKS discovery and authenticity

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  1.1  |  JWKS discovery URL uses HTTPS with system-CA validation  |  Pass  |   |
 |  1.2  |  Issuer claim matches `https://accounts.google.com` or `https://firebase.googleapis.com`  |  Pass  |   |
 |  1.3  |  `kid` rotation handled without stale-cache acceptance  |  Pass  |   |
 |  1.4  |  Algorithm restriction enforced (`RS256` only, no `alg:none`)  |  Pass  |   |
 |  1.5  |  No JWT key-source manipulation vectors  |  Pass  |   |

### 2. TLS and redirects

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  2.1  |  All external fetches validate TLS certificates  |  Pass  |   |
 |  2.2  |  Redirect behavior is bounded and explicit  |  Pass  |   |
 |  2.3  |  No implicit trust on redirect chains  |  Pass  |   |

### 3. Issuer/JWKS consistency

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  3.1  |  JWKS `kid` matches JWT header `kid`  |  Pass  |   |
 |  3.2  |  JWKS fetched from canonical Google endpoint  |  Pass  |   |
 |  3.3  |  No fallback to unverified sources  |  Pass  |   |

### 4. Algorithm restrictions

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  4.1  |  Only `RS256` accepted  |  Pass  |   |
 |  4.2  |  `alg:none` rejected  |  Pass  |   |
 |  4.3  |  No algorithm confusion allowed  |  Pass  |   |

### 5. `kid` rotation/cache behavior

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  5.1  |  Stale `kid` cache entries invalidated before verification  |  Pass  |   |
 |  5.2  |  Cache TTL bounded and documented  |  Pass  |   |
 |  5.3  |  Rotation does not bypass signature verification  |  Pass  |   |

### 6. JWT key-source manipulation

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  6.1  |  Key source cannot be overridden by caller input  |  Pass  |   |
 |  6.2  |  JWKS endpoint is hardcoded or policy-bound  |  Pass  |   |
 |  6.3  |  No fallback to local/untrusted key material  |  Pass  |   |

### 7. JWK/RSA validation

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  7.1  |  RSA key size meets minimum (≥2048 bits)  |  Pass  |   |
 |  7.2  |  Public exponent validation  |  Pass  |   |
 |  7.3  |  Key format validated before use  |  Pass  |   |

### 8. Time/expiry/skew handling

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  8.1  |  Clock-skew tolerance documented and bounded  |  Pass  |   |
 |  8.2  |  Expired tokens rejected deterministically  |  Pass  |   |
 |  8.3  |  `nbf` claim validated  |  Pass  |   |

### 9. Parser/DoS edge cases

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  9.1  |  Input size bounded before parsing  |  Pass  |   |
 |  9.2  |  Malformed JWTs rejected without exception escalation  |  Pass  |   |
 |  9.3  |  No unbounded recursion or regex in parser path  |  Pass  |   |

### 10. Google Confidential Space claim interpretation

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  10.1  |  PRE/POST attestation token fields verified against Google schema  |  Pass  |   |
 |  10.2  |  No claim fields trusted without cryptographic verification  |  Pass  |   |
 |  10.3  |  Remaining #340/#341 claim questions resolved or marked ACCEPTED WITH RATIONALE  |  Pass  |   |

### 11. #314/#316 policy binding

 |  ID  |  Check  |  Expected  |  Finding  |
 | ---- | ------- | ---------- | --------- |
 |  11.1  |  Admission policy digest verified before synthetic key generation  |  Pass  |   |
 |  11.2  |  Caller-provided digest cannot bypass policy check  |  Pass  |   |
 |  11.3  |  Tampered/promoted C evidence rejected  |  Pass  |   |

---

## Finding taxonomy

 |  Classification  |  Meaning  |
 | ---------------- | --------- |
 |  `RESOLVED`  |  Issue fixed and verified in CI  |
 |  `ACCEPTED WITH RATIONALE`  |  Risk acknowledged, mitigation documented, accepted by reviewer and operator  |
 |  `BLOCKED`  |  Must be fixed before proceeding to candidate designation  |
 |  `UNKNOWN`  |  Cannot be determined from available evidence; requires additional data  |

---

## Output format

Findings must be submitted as a JSON file matching the schema in `SOURCE_IDENTITIES.json` → `review_output_schema`.

---

*Checklist created: 2026-09-07* 
*Controlling state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0*
