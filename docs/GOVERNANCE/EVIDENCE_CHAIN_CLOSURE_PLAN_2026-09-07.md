# Evidence-Chain Closure Plan — 2026-09-07

> **Controlling state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
> **Final v0.7.6 candidate:** NOT DESIGNATED (Issue #309).
> **Source-bound external-acceptance handoff baseline:** PR #343 merge `8928a83e93cf9a53f0aeee89a05d57e37b3cc9c2`, tree `442fc81d30c311c6e2cd2f89db5276465982e1c5`; this is not a statement of current repository HEAD.
> This document records the concrete deliverables for #277, #320, and #316. No scientific-state transition is claimed by this document.

---

## 1. #277 — Repository Merge Enforcement Ruleset Correction

### 1.1 Current verified state

| Property | Value |
|----------|-------|
| Ruleset ID | `16909314` |
| Name | `Main` |
| Target | `branch` |
| Enforcement | `active` |
| Current rules | `deletion`, `non_fast_forward` |
| Missing rules | `required_pull_request`, `required_status_checks` |
| Connected integration write access | **No** — can read rulesets, cannot modify |

### 1.2 Required ruleset configuration

```json
{
  "name": "Main",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "rules": [
    {
      "type": "deletion"
    },
    {
      "type": "non_fast_forward"
    },
    {
      "type": "required_pull_request",
      "parameters": {
        "required_approving_review_count": 1,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_reviews": false,
        "require_last_push_approval": false,
        "allowed_merge_methods": ["squash", "merge"],
        "required_review_thread_resolution": false,
        "autocancel_approving_reviews": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "required_status_checks": [
          {
            "context": "pptl-ci",
            "integration_id": 0
          },
          {
            "context": "python-tests",
            "integration_id": 0
          },
          {
            "context": "governance-ci",
            "integration_id": 0
          },
          {
            "context": "pdmal-pre-freeze-runner",
            "integration_id": 0
          },
          {
            "context": "p4-mode-t-confidential-space-admission-contract",
            "integration_id": 0
          },
          {
            "context": "p4-mode-t-retention-contract",
            "integration_id": 0
          },
          {
            "context": "p4-mode-t-google-oidc-verifier",
            "integration_id": 0
          },
          {
            "context": "p4-mode-t-sigstore-verifier",
            "integration_id": 0
          },
          {
            "context": "p4-mode-t-tlock-supply-chain",
            "integration_id": 0
          },
          {
            "context": "mode-t-external-acceptance-handoff",
            "integration_id": 0
          },
          {
            "context": "p9-final-frozen-chain",
            "integration_id": 0
          }
        ],
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": false,
        "required_status_checks_parameters": {
          "required_status_checks": [
            "pptl-ci",
            "python-tests",
            "governance-ci",
            "pdmal-pre-freeze-runner",
            "p4-mode-t-confidential-space-admission-contract",
            "p4-mode-t-retention-contract",
            "p4-mode-t-google-oidc-verifier",
            "p4-mode-t-sigstore-verifier",
            "p4-mode-t-tlock-supply-chain",
            "mode-t-external-acceptance-handoff",
            "p9-final-frozen-chain"
          ]
        }
      }
    }
  ],
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": ["refs/heads/main"]
    }
  }
}
```

### 1.3 Required workflow context names

The following workflow job IDs must be registered in `required_status_checks`:

| Context | Workflow file | Purpose |
|---------|---------------|---------|
| `pptl-ci` | `pptl-ci.yml` | Existing enforced baseline |
| `python-tests` | `python-tests.yml` | Core unit/integration tests |
| `governance-ci` | `governance-ci.yml` | Governance/evidence validation |
| `pdmal-pre-freeze-runner` | `pdmal-pre-freeze-runner.yml` | Candidate-role/custody assertions |
| `p4-mode-t-confidential-space-admission-contract` | `p4-mode-t-confidential-space-admission-contract.yml` | Mode T admission policy |
| `p4-mode-t-retention-contract` | `p4-mode-t-retention-contract.yml` | Durable retention evidence |
| `p4-mode-t-google-oidc-verifier` | `p4-mode-t-google-oidc-verifier.yml` | OIDC/JWKS verification |
| `p4-mode-t-sigstore-verifier` | `p4-mode-t-sigstore-verifier.yml` | Sigstore/Cosign verification |
| `p4-mode-t-tlock-supply-chain` | `p4-mode-t-tlock-supply-chain.yml` | tlock binary supply chain |
| `mode-t-external-acceptance-handoff` | `mode-t-external-acceptance-handoff.yml` | #344 external result intake |
| `p9-final-frozen-chain` | `p9-final-frozen-chain.yml` | Final chain verification |

### 1.4 Application method

**Option A (requires admin):** Repository admin applies the JSON via GitHub web UI → Settings → Rules → Rulesets → Edit `Main` → Import ruleset JSON.

**Option B (requires permission elevation):** Grant the connected GitHub integration `Administration` permission on `rulesets` scope, then apply via `gh api` PUT to `/repos/ndrorchestration/DGAF-Framework/rulesets/16909314`.

**Option C (process-only, current state):** Until Option A or B is completed, maintain process discipline requiring all listed workflow checks to pass before merging. This is the current operating mode and is explicitly noted in #277.

### 1.5 What this does NOT do

- Does **not** close P4.

- Does **not** authorize the experiment.

- Does **not** constitute freeze.

- Does **not** change scientific state.

- Strengthens process integrity only.

---

## 2. #320 — Independent Security Review Charter

### 2.1 Review scope freeze

The following source identities are frozen for #320 review. No other code is in scope.

| Artifact | Path | SHA (at time of charter) |
|----------|------|--------------------------|
| Google OIDC verifier | `experiments/pdmal_pilot/mode_t_google_oidc_verifier.py` | `HEAD` |
| Sigstore verifier | `experiments/pdmal_pilot/mode_t_sigstore_verifier.py` | `HEAD` |
| Retention contract | `experiments/pdmal_pilot/mode_t_retention_contract.py` | `HEAD` |
| Durable retention | `experiments/pdmal_pilot/durable_retention.py` | `HEAD` |
| Admission policy | `experiments/pdmal_pilot/mode_t_admission_policy.py` | `HEAD` |
| Attestation verifier | `experiments/pdmal_pilot/mode_t_confidential_space_attestation.py` | `HEAD` |
| Launch contract | `experiments/pdmal_pilot/mode_t_confidential_space_launch.py` | `HEAD` |
| Integrated lifecycle | `experiments/pdmal_pilot/mode_t_integrated_lifecycle.py` | `HEAD` |
| OIDC workflow | `.github/workflows/p4-mode-t-google-oidc-verifier.yml` | `HEAD` |
| Sigstore workflow | `.github/workflows/p4-mode-t-sigstore-verifier.yml` | `HEAD` |
| Retention workflow | `.github/workflows/p4-mode-t-retention-contract.yml` | `HEAD` |
| Admission workflow | `.github/workflows/p4-mode-t-confidential-space-admission-contract.yml` | `HEAD` |
| Launch workflow | `.github/workflows/p4-mode-t-confidential-space-launch-contract.yml` | `HEAD` |
| Claim policy (from #314) | `experiments/pdmal_pilot/mode_t_admission_policy.py` | `HEAD` |

### 2.2 Review checklist

**Google OIDC/JWKS:**

- [ ] JWKS discovery URL uses HTTPS with system-CA validation

- [ ] Issuer claim matches `https://accounts.google.com` or `https://firebase.googleapis.com`

- [ ] `kid` rotation handled without stale-cache acceptance

- [ ] Algorithm restriction enforced (`RS256` only, no `alg:none`)

- [ ] Expiry/skew handling within acceptable bounds

- [ ] No JWT key-source manipulation vectors

**TLS/redirects:**

- [ ] All external fetches validate TLS certificates

- [ ] Redirect behavior is bounded and explicit

- [ ] No implicit trust on redirect chains

**Issuer/JWKS consistency:**

- [ ] JWKS `kid` matches JWT header `kid`

- [ ] JWKS fetched from canonical Google endpoint

- [ ] No fallback to unverified sources

**Time/expiry/skew:**

- [ ] Clock-skew tolerance documented and bounded

- [ ] Expired tokens rejected deterministically

**Parser/DoS:**

- [ ] Input size bounded before parsing

- [ ] Malformed JWTs rejected without exception escalation

- [ ] No unbounded recursion or regex in parser path

**Confidential Space claim interpretation:**

- [ ] PRE/POST attestation token fields verified against Google schema

- [ ] No claim fields trusted without cryptographic verification

- [ ] Remaining #340/#341 claim questions resolved or marked ACCEPTED WITH RATIONALE

**#314/#316 policy binding:**

- [ ] Admission policy digest verified before synthetic key generation

- [ ] Caller-provided digest cannot bypass policy check

- [ ] Tampered/promoted C evidence rejected

### 2.3 Finding taxonomy

Every finding must be classified as one of:

| Classification | Meaning |
|----------------|---------|
| `RESOLVED` | Issue fixed and verified in CI |
| `ACCEPTED WITH RATIONALE` | Risk acknowledged, mitigation documented, accepted by reviewer and operator |
| `BLOCKED` | Must be fixed before proceeding to candidate designation |
| `UNKNOWN` | Cannot be determined from available evidence; requires additional data |

### 2.4 Reviewer requirements

- Organizationally independent (not DGAF/PDMAL contributor)

- Has access to the frozen source identities above

- Produces findings in machine-readable format (JSON or structured Markdown)

- No code-changing remediation is applied until all `BLOCKED` findings are resolved

---

## 3. #316 — Production Trust/Retention Authority Audit

### 3.1 Current verified state

**What exists:**

- #299: Sigstore/Cosign `verify-blob` implementation pinned to exact Cosign binary SHA-256 (`0fda1e0f...`)

- #314: Admission policy bound through R→A→C chain; production key acquisition **disabled** until independent C/policy verifier exists

- #323: Retention contract with synthetic-only evidence (not real independently retained evidence)

**What is missing (blocking production trust authority):**

1. **Real independently retained R/A/C evidence** — current retention evidence is synthetic/injected

2. **Production TrustedRoot bytes + SHA frozen** — not yet produced

3. **TUF bootstrap/expiry/rotation semantics specified** — not yet documented

4. **Proof that production key acquisition consumes retained authorization** — not yet demonstrated

5. **Independent retrieval and cryptographic reverification** — not yet executed

6. **Production key acquisition re-enabled** — currently disabled pending #320 + real C evidence

### 3.2 Audit checklist

**R (Root) evidence:**

- [ ] TrustedRoot bytes produced and SHA-256 frozen

- [ ] Root stored in independently retained location

- [ ] Root retrieval independently verified

- [ ] Root identity bound to candidate/tree

**A (Authority) evidence:**

- [ ] Signing authority identity documented

- [ ] Authority capability independently attested

- [ ] No caller-asserted authority accepted without retained proof

**C (Certificate/Claim) evidence:**

- [ ] Certificate chain verified against TrustedRoot

- [ ] Certificate identity matches expected signer

- [ ] Certificate retention independently verified

- [ ] #320 review results incorporated

**Retention path:**

- [ ] Retention location independently controlled

- [ ] Retention retrieval independently executable

- [ ] Cryptographic reverification automated

- [ ] Synthetic retention explicitly excluded from production path

**TUF semantics:**

- [ ] Bootstrap procedure documented

- [ ] Expiry policy defined

- [ ] Rotation procedure defined

- [ ] Update semantics defined (manual vs automated)

**Production key acquisition:**

- [ ] Consumption of retained authorization demonstrated

- [ ] Cannot be bypassed via caller-provided digest

- [ ] Cannot be bypassed via `independent_retention_verified=true` flag

- [ ] Re-enabled only after #320 findings RESOLVED and real C evidence produced

### 3.3 Acceptance criteria

Production trust authority is established when:

1. #320 review is complete with zero `BLOCKED` findings.

2. Real independently retained R/A/C evidence exists and is independently retrievable.

3. TrustedRoot bytes + SHA are frozen and bound to final candidate (post-#309).

4. TUF bootstrap/expiry/rotation semantics are documented and verified.

5. Production key acquisition demonstrably consumes retained authorization.

6. All of the above is CI-verified before candidate designation.

---

## 4. Immediate next steps

1. **#277 ruleset spec** — this document contains the ready-to-apply JSON. Needs admin application via web UI or permission elevation.

2. **#320 charter** — source identities frozen above; ready to issue to independent reviewer.

3. **#316 audit** — checklist ready; execution blocked on #320 completion and real retention evidence production.

4. **#310 Stage-A** — preparation can proceed in parallel (#320/#316) but execution requires authenticated GCP.

---

*Document written: 2026-09-07*
*Controlling state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0*
*No scientific-state transition claimed.*
