# PDMAL Candidate-Bound Execution Path — 2026-08-21

**Prepared:** 2026-08-22  
**Status:** EXECUTION PATH SPECIFICATION — NOT YET EXECUTED  
**Candidate SHA:** `94fb6fdff64f2919d35938c5b1cb506625cf1139` (candidate as of GitHub state checked 2026-08-22)  
**GitHub PR #77:** open, still lists remaining governance/evidence gates (primary contrast, blinding custody, topology reconciliation, durable retention, analysis SHA, new freeze)  
**Protocol state:** PRE-FREEZE  
**Empirical N:** 0  
**Pilot authorization:** NOT GRANTED

---

## Purpose

This document specifies the candidate-bound execution path from candidate SHA to retained evidence with independent SHA verification. It does **not** claim any execution has occurred. Workflow existence is not execution evidence.

Every artifact produced by this path must identify the exact candidate SHA and execution provenance.

---

## Execution Chain (10 stages)

```
candidate SHA (94fb6fd)
    │
    ▼
[P0] Pre-authorization verification
    │   Check: protocol freeze declared + candidate SHA matches authorized value
    │   Gate: require_frozen_commit() + require_pilot_authorization()
    │   Evidence: workflow run record with candidate SHA in output
    │
    ▼
[P2] Runtime matrix execution
    │   Check: live deployment responds correctly to P2 verification matrix
    │   Gate: P2 runtime verification workflow (p2-runtime-verification.yml)
    │   Evidence: workflow run record + runtime response JSON + candidate SHA attribution
    │
    ▼
[P6a] CORS verification
    │   Check: live deployment enforces CORS policy correctly
    │   Gate: P6a CORS verification workflow (p6a-cors-verification.yml)
    │   Evidence: workflow run record + CORS test results + candidate SHA attribution
    │
    ▼
[Instrumentation dry run]
    │   Check: blinding operational test under controlled conditions
    │   Gate: pdmal-instrumentation-dry-run.yml
    │   Evidence: workflow run record + dry-run output + candidate SHA attribution
    │   Note: requires PDMAL_BLINDING_KEY ≥ 32 chars; refuses to run unblinded
    │
    ▼
[Runtime characterization]
    │   Check: non-empirical runtime characterization of candidate apparatus
    │   Gate: pdmal-runtime-characterization.yml
    │   Evidence: workflow run record + characterization output + candidate SHA attribution
    │   Note: non-empirical — no data collection, no efficacy claim
    │
    ▼
[Pre-freeze runner validation]
    │   Check: fail-closed runner contract + dependency lock integrity
    │   Gate: pdmal-pre-freeze-runner.yml
    │   Evidence: workflow run record + pre-freeze-runner-manifest.json + candidate SHA attribution
    │   Artifact: test-artifacts/pre-freeze-runner-manifest.json (30-day retention, if-no-files-found: error)
    │
    ▼
[Schema/security validation]
    │   Check: artifact schema validation + adversarial security tests
    │   Gate: pdmal-preauth-security.yml (schema tests + test_security_controls.py)
    │   Evidence: workflow run record + test results + candidate SHA attribution
    │
    ▼
[Artifact retention — P6 custody]
    │   Check: artifact written → independently retrieved → SHA-256 recomputed → compared → PASS/FAIL
    │   Gate: durable_retention.py + independent retrieval verification
    │   Evidence: write receipt + retrieval receipt + recomputed SHA + comparison result
    │   Note: until this round-trip exists, P6 remains OPEN
    │
    ▼
[Independent SHA verification — P9]
    │   Check: independent verifier re-resolves candidate SHA, re-executes validation, verifies custody
    │   Gate: separate audit path (distinct from CI)
    │   Evidence: independent verification record with PASS/FAIL/INCONCLUSIVE + candidate SHA attribution
    │   Note: requires actual evidence chain as input (candidate + workflow runs + runtime artifacts + provenance + custody proof + hashes + P7 decision + P8 locked spec)
    │
    ▼
[Retained evidence package]
    │   Output: complete evidence package with all run records, artifacts, hashes, provenance
    │   Candidate SHA: 94fb6fd (must be in every artifact's metadata)
    │   Execution provenance: workflow run IDs, timestamps, runner environment
```

---

## Stage-by-Stage Details

### Stage 0: Candidate identity

| Field | Value |
|---|---|
| Candidate SHA | `94fb6fdff64f2919d35938c5b1cb506625cf1139` |
| Candidate label | PR77-corrected-pilot-apparatus |
| Freeze target SHA | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Local PR head | `94fb6fd` (pr-77-head branch) |
| GitHub PR head | `b25a914c` (draft, NOT MERGEABLE) |
| Candidate manifest | `docs/experiment/CANDIDATE_MANIFEST_2026-08-21.json` |

**Candidate identity is established but NOT immutable.** No tag, no protected reference, no freeze commit yet.

---

### Stage 1: P0 Pre-authorization verification

**Workflow:** `pdmal-pre-freeze-runner.yml`

**What it verifies:**

- Protocol freeze declared (env var or configuration)
- Candidate SHA matches authorized value (`require_frozen_commit()`)
- Pilot authorization present (`require_pilot_authorization()`)
- Blinding condition applied (`blind_condition()`)

**Current state:** Workflow exists but NOT EXECUTED against candidate. `require_frozen_commit()` checks env var, not cryptographic binding to specific SHA.

**Required evidence:** Workflow run record that explicitly includes:

- Candidate SHA tested: `94fb6fd`
- Protocol freeze status at time of run
- Authorization status at time of run
- Runner version/SHA used

**Blocker:** Requires protocol freeze + authorization, which are NOT GRANTED.

---

### Stage 2: P2 Runtime matrix

**Workflow:** `p2-runtime-verification.yml`

**What it verifies:**

- Live deployment provenance (Vercel deployment at `dynamicgovernanceagenticformation-dp3baqm9p-ndrorchestration.vercel.app`)
- Five-case P2 verification matrix against live endpoint
- Runtime endpoint behavior under candidate code

**Current state:** Workflow exists but NOT EXECUTED. Requires `VERCEL_AUTOMATION_BYPASS_SECRET` (Vercel SSO-protected). EXPECTED_COMMIT is `e1f077fec746acd6066db689ef40db000e027f2f` — must be updated to candidate SHA before execution.

**Required evidence:** Workflow run record with:

- Candidate SHA tested: `94fb6fd`
- Deployment URL tested
- Five-case matrix results
- Runtime response JSON (stored as artifact)

**Blocker:** Vercel SSO protection; EXPECTED_COMMIT must be updated to candidate SHA.

---

### Stage 3: P6a CORS verification

**Workflow:** `p6a-cors-verification.yml`

**What it verifies:**

- Live deployment CORS policy enforcement
- Allowed origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`
- Disallowed origin test: `https://untrusted.com`

**Current state:** Workflow exists but NOT EXECUTED. Requires `VERCEL_AUTOMATION_BYPASS_SECRET`.

**Required evidence:** Workflow run record with:

- Candidate SHA tested: `94fb6fd`
- CORS test results (allowed/disallowed outcomes)
- Candidate SHA attribution

**Blocker:** Vercel SSO protection.

---

### Stage 4: Instrumentation dry run

**Workflow:** `pdmal-instrumentation-dry-run.yml`

**What it verifies:**

- Blinding operational test under controlled conditions
- Fail-closed when `PDMAL_BLINDING_KEY` < 32 chars (refuses to run unblinded)

**Current state:** Workflow exists but NOT EXECUTED.

**Required evidence:** Workflow run record with:

- Candidate SHA tested: `94fb6fd`
- Blinding key availability (present/absent, length if present)
- Dry-run output
- Candidate SHA attribution

**Blocker:** Requires `PDMAL_BLINDING_KEY` secret configured in GitHub Actions.

---

### Stage 5: Runtime characterization

**Workflow:** `pdmal-runtime-characterization.yml`

**What it verifies:**

- Non-empirical runtime characterization of candidate apparatus
- No data collection, no efficacy claim

**Current state:** Workflow exists but NOT EXECUTED. Triggers on `workflow_dispatch` or push to `epistemic/evidence-architecture-v1`.

**Required evidence:** Workflow run record with:

- Candidate SHA tested: `94fb6fd`
- Characterization output
- Candidate SHA attribution

**Blocker:** None intrinsic — workflow can be dispatched, but output must be attributed to candidate SHA.

---

### Stage 6: Pre-freeze runner validation

**Workflow:** `pdmal-pre-freeze-runner.yml`

**What it verifies:**

- Fail-closed runner contract
- Dependency lock integrity (requires genuine full dependency lock generation)
- Artifact schema validation

**Current state:** Workflow exists but NOT EXECUTED.

**Artifact produced:** `test-artifacts/pre-freeze-runner-manifest.json`

- Retention: 30 days
- Missing-file behavior: error (`if-no-files-found: error`)

**Required evidence:** Workflow run record with:

- Candidate SHA tested: `94fb6fd`
- Pre-freeze-runner-manifest.json (stored as workflow artifact)
- Dependency lock integrity verification
- Candidate SHA attribution

---

### Stage 7: Schema/security validation

**Workflow:** `pdmal-preauth-security.yml`

**What it verifies:**

- Artifact schema validation (`test_artifact_schema.py`)
- Adversarial security tests (`test_security_controls.py`, 6 tests)
- Python 3.12.0 environment
- Dependency integrity (hash-pinned via `requirements-full-lock.txt`)

**Current state:** Workflow exists but NOT EXECUTED. On disk at `.github/workflows/pdmal-preauth-security.yml`. At PR #77: blob `9cff92a5`.

**Required evidence:** Workflow run record with:

- Candidate SHA tested: `94fb6fd`
- Schema test results
- Security test results (6 tests)
- Candidate SHA attribution

**Blocker:** Workflow not executed.

---

### Stage 8: Artifact retention — P6 custody

**Status:** OPEN — NOT YET ESTABLISHED

**What it requires:**

1. Artifact written to durable storage
2. Artifact independently retrieved from storage
3. SHA-256 recomputed from retrieved bytes
4. Recomputed SHA compared to original SHA
5. PASS or FAIL recorded

**Current state:**

- `durable_retention.py` exists on disk at local HEAD (11,666 bytes, 338 lines, 12 functions) but NOT at PR #77
- Archive root NOT SET — TBD
- No retention policy document at PR #77
- No write→retrieve→SHA-verification round-trip has occurred

**Required evidence:**

- Write receipt (timestamp, storage location, original SHA)
- Retrieval receipt (timestamp, retrieved bytes, recomputed SHA)
- Comparison result (PASS/FAIL)
- Candidate SHA attribution

**Blocker:** Archive not established; no round-trip executed.

---

### Stage 9: Independent SHA verification — P9

**Status:** DESIGN ONLY — NOT EXECUTED

**What it requires:**

- Independent verifier (distinct from CI creation path)
- Re-resolves candidate SHA independently
- Re-executes validation against candidate
- Verifies custody proof (write→retrieve→SHA round-trip)
- Verifies runtime artifacts
- Verifies provenance chain
- Produces PASS/FAIL/INCONCLUSIVE record

**Current state:**

- 7-layer verification architecture designed (in prior documentation)
- 10 CI-appropriate checks defined
- 8 separate-audit checks defined
- 8-step freeze verification procedure with PASS/FAIL/INCONCLUSIVE
- Evidence chain defined
- Critical gaps documented

**Required input for P9 execution:**

- Candidate SHA: `94fb6fd`
- Workflow run records (Stages 1-7)
- Runtime artifacts (response JSONs, characterization output, manifests)
- Provenance records (run IDs, timestamps, environments)
- Custody proof (Stage 8 round-trip result)
- Hashes (artifact SHA-256s, sidecar hashes)
- P7 decision record (selected contrast, estimand, CI method, multiplicity, success/falsification criteria)
- P8 locked analysis specification (frozen SHA)

**Blocker:** Requires actual evidence chain as input. Cannot execute until Stages 1-8 produce evidence.

---

### Stage 10: Retained evidence package

**Output:** Complete evidence package containing:

- All workflow run records (Stages 1-7) with candidate SHA attribution
- All runtime artifacts (response JSONs, characterization output, manifests)
- All provenance records (run IDs, timestamps, runner environments)
- Custody proof (Stage 8 round-trip result)
- All artifact hashes (SHA-256s, sidecar hashes)
- P7 decision record
- P8 locked analysis specification (frozen SHA)
- Independent verification record (Stage 9 result)

**Candidate SHA must appear in every artifact's metadata.**

---

## What Workflow Existence Does NOT Prove

| Claim | What existence proves | What's missing |
|---|---|---|
| "P2 is verified" | A workflow exists that could verify P2 | No execution record; no candidate SHA attribution; no runtime evidence |
| "P6a is verified" | A workflow exists that could verify P6a | No execution record; no CORS test results; no candidate SHA attribution |
| "Blinding works" | A workflow exists that tests blinding | No dry-run record; no blinding key configured; no operational custody |
| "Schema validation works" | A workflow exists that runs schema tests | No execution record; no actual artifact validated; no candidate SHA attribution |
| "Candidate is bound" | A manifest exists identifying the candidate | No immutable tag; no protected reference; no freeze commit; CI runs on PR paths not pinned SHA |
| "P6 custody exists" | A retention script exists on disk | No archive established; no write→retrieve→SHA round-trip; no custody proof |

---

## Execution Prerequisites (not yet met)

| Prerequisite | Status |
|---|---|
| Protocol freeze declared | NOT YET — PRE-FREEZE |
| Pilot authorization | NOT GRANTED |
| Candidate immutable tag | NOT YET — no tag, no protected reference |
| Vercel automation bypass secret | NOT CONFIGURED (required for P2/P6a) |
| PDMAL_BLINDING_KEY secret | NOT CONFIGURED (required for dry-run) |
| EXPECTED_COMMIT updated to candidate SHA | NOT YET — currently `e1f077f` |
| Archive root designated and configured | NOT YET — TBD |
| P7 decision record | NOT YET — OPEN |
| P8 analysis specification frozen | NOT YET — BLOCKED BY P7 |

---

## N=0 Invariant

This document does not claim any execution has occurred:

- **N = 0** — no empirical data collection
- **Pilot authorization: NOT GRANTED**
- **Protocol state: PRE-FREEZE**
- **No efficacy claims** — workflow existence ≠ execution evidence
- **No green-status claims** — no workflow has produced a run record against the candidate SHA

---

## Sources

- `.github/workflows/pdmal-preauth-security.yml` — schema + security tests (on disk, NOT EXECUTED)
- `.github/workflows/pdmal-instrumentation-dry-run.yml` — blinding dry-run (on disk, NOT EXECUTED)
- `.github/workflows/pdmal-runtime-characterization.yml` — non-empirical characterization (on disk, NOT EXECUTED)
- `.github/workflows/p2-runtime-verification.yml` — P2 live verification (on disk, NOT EXECUTED)
- `.github/workflows/p6a-cors-verification.yml` — P6a CORS verification (on disk, NOT EXECUTED)
- `.github/workflows/pdmal-pre-freeze-runner.yml` — pre-freeze runner + dependency lock (on disk, NOT EXECUTED)
- `docs/experiment/PDMAL_BLINDING_CUSTODY.md` — blinding primitive verified, operational custody NOT YET VERIFIED
- `docs/experiment/PDMAL_ARTIFACT_RETENTION.md` — 30-day GitHub Actions artifacts, canonical JSON, SHA-256 sidecars
- `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` — gate board (P1-P9 status + blockers)
- `docs/experiment/CANDIDATE_MANIFEST_2026-08-21.json` — candidate identity
- `docs/DGAF_PDMAL_EXECUTION_READINESS_REFINED_2026-08-21.md` — corrected assessment, 0/9 scoring

---

*Prepared 2026-08-21. Execution path specified. No execution claimed. N=0.*
