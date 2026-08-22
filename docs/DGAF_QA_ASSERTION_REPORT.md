# DGAF QA Assertion Report — 2026-08-21

**Prepared from:** 5 agent-submitted artifacts + corrected sprint report analysis
**Working directory:** `C:\Users\Admin\DGAF-Framework`
**HEAD:** `3510b86889cd341f7a7cf9ab684fd37b2fafd758` (main)
**PR #77 branch:** `chore/preauth-completeness-2026-08-20`, head `4983f44a1867d8ab2f18295a1ce23877ff8ea928`
**N = 0 throughout.** Pilot authorization NOT GRANTED. `3510b868...` is the historical superseded freeze; the corrected apparatus is PRE-FREEZE and not yet frozen.

---

## 1. QA Assertion Report

### What This Is

This is the QA assertion report for the DGAF/PDMAL pre-authorization completeness work. It surfaces what each agent found, what each document claims, what each document does NOT establish, and where the verification boundary stands. It does not approve, authorize, or close any predicate. It reports.

### Agent Outputs (5/5 on disk)

| # | File | Size | Agent | Status |
|---|---|---|---|---|
| 1 | `schema_resolution.json` | 6,218 B | `deleg_bf463b1a` | ✓ COMPLETED |
| 2 | `estimand_chain.json` | 10,801 B | `deleg_0b7232f4` | ✓ COMPLETED |
| 3 | `pr77_doc_briefing.json` | 30,447 B | `deleg_f2483135` | ✓ COMPLETED (from transcript) |
| 4 | `independent_verification_design.json` | 26,366 B | `deleg_43a9c4f6` | ✓ COMPLETED |
| 5 | `experimental_design_integrity.json` | 6,560 B | `deleg_b6e270a3` | ✓ COMPLETED (from transcript) |

### Governing Principles Applied

- P-EXP-2: Configuration must not become evidence — predicate matrix is DERIVED control layer
- P-EXP-5: Independent verification must introduce distinct observation path — CI for deterministic, separate audit for independence-distinct
- P-EXP-8: Anti-yellow-tape — each verification layer must reduce uncertainty or prevent a material failure not already covered
- N = 0: No empirical claims. No pilot authorization. No efficacy claims from implementation evidence.

---

## 2. Agent #1: Schema Resolution (`schema_resolution.json`)

**Canonical module for pilot: `pilot_artifact_schema.py`**

### What it found

| Finding | Detail |
|---|---|
| Existing module role | `artifact_schema.py` (blob `41a9048`) validates PRE-FREEZE artifacts: requires `protocol_status=PRE-FREEZE`, `empirical_data_collection=False`, 16 required fields. Does NOT recompute `artifact_sha256` — only validates presence and format. Used by contract mode and pre-freeze artifact inspection. |
| New module role | `pilot_artifact_schema.py` (PR #77 only, blob `2918a9d`) validates FROZEN pilot artifacts: requires `protocol_status=FROZEN`, `empirical_data_collection=True`, full 40-character `frozen_commit_sha`, exactly 180 records per seed. Recomputes `artifact_sha256` from canonical payload. Provides `verify_sidecar()` for sidecar integrity. This is the validation contract for authorized pilot execution. |
| Schema version | Both declare `ARTIFACT_SCHEMA_VERSION = "1.0"` — **semantically incompatible**. `artifact_schema.py` REJECTS FROZEN status and `empirical_data_collection=True`; `pilot_artifact_schema.py` REJECTS PRE-FREEZE status and `empirical_data_collection=False`. Calling `validate_artifact_document()` from `artifact_schema.py` on a pilot artifact would raise `AssertionError`. The version number is shared but the contracts are distinct. |
| Wiring question | **YES — runner should call validation inline.** Neither local HEAD nor PR #77 `run_pilot.py` imports either schema module (grep count: 0 for both). CI-only validation tests hand-constructed documents, not artifacts the runner actually wrote. |
| SHA computation risk | PR #77 runner computes `artifact_sha256` inline at record construction (`json.dumps + hashlib.sha256`). `pilot_artifact_schema.validate_record()` recomputes with `canonical_json_bytes()`. These must produce identical results or `validate_record()` will reject valid artifacts. This is an unverified consistency gap. |
| Independent verification path | Load artifact JSON → call `pilot_artifact_schema.validate_artifact(document)` → call `pilot_artifact_schema.verify_sidecar(raw_bytes, sidecar_text, filename)` → optionally recompute `artifact_sha256` independently. Distinct from runner (no trial execution, no auth required). CI exercises this path through `test_artifact_schema.py` but uses hand-constructed documents, not real artifacts. |

### What it does NOT establish
- That the runner's inline SHA-256 computation matches the schema module's canonical computation
- That the artifact field sets are compatible between runner and schema
- That `artifact_schema.py` and `pilot_artifact_schema.py` are version-compatible (they are not)
- That inline validation has been wired (it has not)

### 5-point recommendation
1. Differentiate schema versions (`1.0-prefreeze` vs `1.0-pilot`) or unify into one module with dispatch on `protocol_status`
2. Wire `pilot_artifact_schema.validate_artifact()` and `verify_sidecar()` into `run_pilot.py`'s `run_pilot()` immediately after each artifact write — fail-closed self-check
3. Add standalone `verify_artifacts.py` (or extend `test_artifact_schema.py`) that can load and validate artifact files from any directory — independent verification path
4. Resolve the inline SHA-256 computation inconsistency between runner and schema module
5. Confirm runner's record field set matches `REQUIRED_RECORD_FIELDS` in `pilot_artifact_schema.py` — runner includes `topology`, `condition`, `failure_count` inside `secondary_outcomes` but not as top-level fields

---

## 3. Agent #2: Estimand Chain (`estimand_chain.json`)

**Construct:** FFCR — execution robustness characterization, not efficacy claim.

### What it found

| Level | Specification |
|---|---|
| Construct | Failure-Free Completion Rate (FFCR): proportion of trials within a seed completing without failure, aggregated to condition level. Operationalizes "how reliably does the consensus stack complete its assigned workload under a given condition and topology, in the presence of injected failures." Scalar characterization of execution robustness, NOT a claim about DGAF effectiveness in any real-world setting. |
| Estimand | E[FFCR(T) − FFCR(R)] — mean of seed-level paired differences d_i = FFCR_i(T) − FFCR_i(R) across n=50 planned seeds. Inference via prespecified paired-bootstrap CI. |
| Primary endpoint | FFCR per condition, per seed: FFCR = (trials completing without failure) / (total trials for that condition under that seed). 180 trials/seed (4 conditions × 5 topologies × 9 failure counts). Condition-level FFCR aggregates across all topologies and failure-count levels within that seed, or according to frozen aggregation rule. Higher is better. Computed before exclusion/missing-record handling. |
| Statistical unit | One seed (confirmed from protocol line 23: "Statistical unit: one seed"; matrix amendment v0.7.5 line 72: "one paired experimental block"). 180 within-seed observations are component trials, NOT independent units. |
| Secondary endpoints | Three structural/execution metrics: (1) `final_std`, (2) `D_a`-style diagnostics, (3) phi-convergence traces. Explicitly labeled as "structural/execution metrics for transparency, not primary/secondary success endpoints" (freeze manifest lines 36-37) and "transparency metrics, not success endpoints" (protocol line 56). NOT for hypothesis testing under multiplicity. |
| Primary contrast candidates | **(1) dgaf vs null** — full DGAF stack vs no-DGAF baseline. Direction: higher FFCR for dgaf expected favorable. Maps to paired-bootstrap CI on d_i. Most natural primary contrast. <br> **(2) PDMAL topology vs Ring** — under fixed condition. Direction NOT prespecified. Historical contrast that must NOT be silently inherited (different endpoint/framework). Requires specifying fixed condition and aggregation rule. <br> **(3) Combined condition/topology contrast** — if justified and explicitly defined. Increases multiplicity burden. Not pre-specified in current protocol. |
| Multiplicity structure | NOT YET CLOSED. Candidate contrasts form natural family. If one selected as primary, remaining become secondary with correction (Holm, Bonferroni, or hierarchical gatekeeping — to be specified at adjudication). v0.7.5 matrix amendment accepted by governance but panel approval PENDING. |
| Missing for closure (12 items) | (1) Choice of primary contrast, (2) treatment/reference definitions, (3) exact mathematical estimand with aggregation rule, (4) direction of improvement, (5) decision threshold (alpha, CI level, one/two-sided), (6) multiplicity family + correction strategy, (7) whether combined contrast is pre-specified with cell definitions, (8) confirmation historical PDMAL-vs-Ring considered and either adopted (re-justified) or rejected — not silently inherited, (9) decision authority + adjudication date, (10) exact protocol blob SHA (pending after commit), (11) freeze commit SHA (placeholder), (12) explicit pilot authorization (NOT GRANTED) |
| Not an engineering fix | Executor acceptance evidence demonstrates apparatus works (2 dry-run seeds, 360 trials, all success, artifact validation PASSED). FFCR computation, seed-level pairing, and paired-bootstrap framework are fully specified in protocol. Missing is scientific-target choice: **which contrast answers the question.** No code change resolves this. Attempting to resolve by modifying executor, aggregation, or bootstrap would constitute apparatus modification after freeze — prohibited. |

### What it does NOT establish
- A chosen primary contrast
- A success criterion
- A falsification criterion
- A multiplicity strategy
- That the historical PDMAL-vs-Ring contrast has been explicitly considered
- Any empirical result

---

## 4. Agent #3: PR #77 Doc Briefing (`pr77_doc_briefing.json`)

**7 docs from PR #77 branch analyzed: 5 new + 2 modified. Total: 373 lines.**

### What it found

**New documents (5):**

| Doc | Lines | Purpose | Key claims | Predicate coverage |
|---|---|---|---|---|
| `DOCUMENTATION_GAP_AUDIT.md` | 73 | Reconciliation of historical vs current state | PR #75 CLOSED, executor CLOSED, executor acceptance CLOSED (360 obs, N=0), protocol freeze CLOSED at 3510b8689, primary contrast OPEN/MUST CLOSE, blinding custody CLOSED FOR SYNTHETIC VERIFICATION, durable retention VERIFY/CLOSE, Hermes/expert-agent reports NOT PRESENT IN REPO | 1 (claims CLOSED for old runner), 5 (VERIFY items), 9 (Hermes/expert-agent NOT PRESENT IN REPO) |
| `FREEZE_MANIFEST_RECONCILIATION_2026-08-20.md` | 50 | Explicit reconciliation of historical freeze with corrected runner | 3 material runner defects found; historical freeze must NOT be reused; corrected runner is NEW candidate; new freeze gates listed; NOT GRANTED until gates close | 1 (historical superseded), 9 (NOT GRANTED) |
| `PDMAL_ANALYSIS_CONTROL_PLAN.md` | 51 | Repository-local analysis control record | sample_size.py planning utility (alpha=0.05, power=0.80, MDD=0.15, external SD); FFCR primary endpoint; seed unit; 50 seeds; 9,000 observations; paired-bootstrap; multiplicity required before unblinding; previously reported analysis plan docs NOT FOUND at expected paths | 7 (partial — planning basis, does NOT adjudicate contrast) |
| `POST_FREEZE_DOCUMENTATION_RECONCILIATION_2026-08-20.md` | 74 | Post-freeze doc reconciliation framework | Freeze commit 3510b8689; docs reconciled; FREEZE_MANIFEST.md NOT silently rewritten; Hermes/expert-agent NOT in repo; next doc should be consolidated Pre-Authorization Verification Record with 10 items | 5 (post-freeze reconciliation), 9 (Hermes/expert-agent evidence boundary) |
| `PRE_AUTHORIZATION_VERIFICATION_RECORD_2026-08-20.md` | 69 | Consolidated closure checklist | IMPLEMENTED: 9 gates (runner SHA binding, auth gate, blinding primitive, hidden condition, artifact hash, sidecar, task identity, runtime ceiling, blinding primitive). OPEN: 9 gates (env, smoke, CI, fingerprints, retention, contrast, analysis SHA, new freeze, authorization). "Corrected apparatus verified: NO; New freeze created: NO; Pilot authorized: NO; Empirical N: 0" | 1-9 (consolidated gate board) |

**Modified documents (2):**

| Doc | What changed | Predicate coverage |
|---|---|---|
| `docs/CURRENT_STATE.md` | Reframes historical freeze as SUPERSEDED; adds gate table with CANDIDATE status; OPEN for primary contrast; VERIFY for env/fingerprints/retention; 10 immediate next actions | 1, 5, 9 |
| `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | Re-points to corrected candidate; adds gate board entries for CANDIDATE items; acknowledges historical freeze superseded; 10 critical path items | 1-9 (gate board) |

### Internal consistency

All 7 docs consistent in core claims: (1) historical freeze RETAINED AS EVIDENCE for old runner, (2) corrected runner is NEW candidate at `fec7a6f`, (3) primary contrast OPEN and MUST CLOSE before authorization, (4) pilot authorization NOT GRANTED, (5) empirical N = 0.

**Most honest statement:** `PRE_AUTHORIZATION_VERIFICATION_RECORD_2026-08-20.md` — "Corrected apparatus verified: NO; New freeze created: NO; Pilot authorized: NO; Empirical N: 0. No combination of passing engineering tests changes authorization state. Authorization requires an explicit governance decision after the pre-authorization matrix is closed."

### What the docs do NOT establish
- Verification of any OPEN gate
- That the corrected runner has been independently verified end-to-end
- That a new freeze has been created
- That pilot authorization has been granted
- That any empirical data exists

### Coverage of sprint findings (13 findings)

| Finding | PR #77 Coverage | Status |
|---|---|---|
| #1 Freeze-SHA binding | ADDRESSED — runner SHA binding (`fec7a6f`), wrong-SHA test | Implemented |
| #2 Malformed commit prevention | ADDRESSED — auth gate, task identity, artifact hash, sidecar all IMPLEMENTED | Implemented |
| #3 Candidate integrity assertions | PARTIALLY — distinguishes IMPLEMENTED from VERIFIED; "verified: NO" | Partially addressed |
| #4 Documentation staleness | ADDRESSED — POST_FREEZE_RECONCILIATION documents stale statements | Addressed |
| #5 Post-freeze documentation reconciliation | ADDRESSED — framework provided; historical freeze NOT reused | Addressed |
| #6 Fresh evidence collection | PARTIALLY — VERIFY items listed; no fresh evidence collected (CI required) | Partially addressed |
| #7 Environment mismatch (Python) | PARTIALLY — VERIFY listed; pdmal-preauth-security.yml uses 3.12.0; fresh verification OPEN | Partially addressed |
| #8 Artifact schema not wired | PARTIALLY — NEW `pilot_artifact_schema.py` added; not wiring existing `artifact_schema.py` | Partially addressed |
| #9 pdmal-preauth-security.yml missing | ADDRESSED — added; Python 3.12.0, locked deps, 7-step workflow | Addressed |
| #10 Security test file missing | ADDRESSED — `test_security_controls.py` added; 6 adversarial tests; CI required | Addressed |
| #11 Durable retention uncommitted | NOT ADDRESSED — listed as VERIFY/OPEN; `durable_retention.py` on disk, not committed | Not addressed |
| #12 Primary contrast adjudication | NOT ADDRESSED (correctly) — OPEN; scientific/governance decision, not engineering fix | Not addressed (correctly) |
| #13 Historical freeze reconciliation | ADDRESSED — FREEZE_MANIFEST_RECONCILIATION explicitly reconciles; historical freeze RETAINED AS EVIDENCE, NOT REUSED | Addressed |

---

## 5. Agent #4: Independent Verification Design (`independent_verification_design.json`)

**10 verification layers, 10 CI-appropriate checks, 8 separate-audit checks, 8-step procedure.**

### What it found

**Verification layers:**

| Layer | Purpose | Method | Independence rationale |
|---|---|---|---|
| Frozen-commit gating | Verify HEAD == expected `PDMAL_FROZEN_COMMIT_SHA` | CI: code invariant (test_SHA_rejection). Separate audit: re-resolve SHA from artifact-producing tree, compare independently | CI proves `require_frozen_commit()` code correct; audit proves actual runner was at that SHA (P-EXP-5) |
| Protocol freeze authorization | Verify env vars set + key supplied out-of-band | CI: N/A (gating fail-closed). Separate audit: manual attestation + key custody verification | Key is secret — cannot be in CI. Audit verifies out-of-band supply (P-EXP-5) |
| Task substitution prevention | Pilot path uses `ConsensusTask`, not `ScriptedTask` | CI: AST parse check. Deterministic code invariant | Code-level check — CI sufficient. True independence needs separate AST checker from different toolchain |
| Blinding correctness | Distinct outputs per label, no label leakage, key-dependent unblinding | CI: crypto property tests. Separate audit (with key): recompute blinded IDs from labels, match artifact. Without key: structural check only (blind_ prefix, no label substring) | With key: distinct observation path (P-EXP-5). Without key: weaker structural independence |
| Runtime ceiling (fail-closed) | `SEED_RUNTIME_CEILING_SECONDS == 300.0`; `validate_seed_runtime()` rejects exceeding | CI: asserts constant + function. Separate audit: verify `runtime_seconds <= 300.0` in each artifact | Artifact runtime independently verifiable from artifact itself (P-EXP-5) |
| Artifact schema and integrity | Required fields, valid status, correct `artifact_sha256`, blinded ID, excluded/exclusion_reason consistency, sidecar SHA-256 matches | CI: `test_artifact_schema.py` + substitution detection. Separate audit: run `validate_artifact()` + `verify_sidecar()` on actual pilot artifacts | CI validates validator; audit validates actual artifacts from different context (P-EXP-5) |
| Artifact count (180/seed) | Each seed artifact has exactly 180 records | CI: `validate_artifact()` asserts count. Separate audit: independently count records in each artifact | Evidence verification on artifact (P-EXP-5) |
| Environment fingerprint consistency | `environment_fingerprint` present, consistent across records, derived from runtime versions | CI: field presence only. Separate audit: verify consistency + independently compute expected fingerprint | Requires auditor to know runtime versions (P-EXP-5) |
| Contract mode non-empirical | Contract mode exercises 2 seeds, reports `CONTRACT_MODE_PASS`, writes no pilot artifacts | CI: behavioral check (sufficient). Separate audit: marginal independence gain — CI is sufficient | Code-path behavioral check — CI sufficient |
| Artifact substitution detection | Tampering detectable via `artifact_sha256` mismatch | CI: tamper test. Separate audit: inherent in validation step — if `validate_artifact()` passes, substitution ruled out | Real independence payoff: CI proves detector correct; audit shows artifacts pass it |

**Evidence chain:**
- **Creation path:** Protocol freeze → SHA set → env vars + key → runner executes → artifacts with blinded IDs + SHA-256 + sidecars → CI tests source code
- **Verification path:** CI: pytest on source code (code invariants, schema tests, contract mode). Separate audit: independently resolve HEAD → compare SHA → verify env vars + key custody → recompute blinded IDs (if key) → validate actual artifacts → verify sidecars → check runtime ceiling → check record count → check fingerprint consistency → cross-check all SHA references
- **Independence gaps:** CI validates the validator but cannot verify actual production run's SHA, env vars, key supply, or artifact integrity. Without blinding key, auditor can only do structural checks. Environment fingerprint verification requires auditor to know runtime versions.

**What CI cannot provide (6 items):**
1. Proof of actual run's SHA (CI checks code that does the check, not actual HEAD at runtime)
2. Proof of env vars at runtime (CI monkeypatches for testing)
3. Proof of out-of-band key supply (key is secret, never in CI)
4. Proof that actual artifacts are untampered (CI validates synthetic tests, not real ones)
5. Proof of no artifacts from non-frozen window (CI runs on PR/push events, not production timeline)
6. Independent recomputation of blinded IDs (CI doesn't hold custody key)

**Freeze verification procedure (8 steps + final decision):**
1. Obtain declared `PDMAL_FROZEN_COMMIT_SHA`
2. Independently resolve HEAD from artifact-producing checkout; compare SHA
3. Verify runner source contains `require_frozen_commit()` + `require_pilot_authorization()`
4. Obtain blinding key from out-of-band supply (note gap if unavailable)
5. For each `pilot_seed_*.json`: run `validate_artifact()`, run `verify_sidecar()`, check fingerprint consistency, recompute blinded IDs (if key) or structural check (if not), cross-check SHAs
6. Validate `pilot_summary.json`
7. Verify no artifacts from non-frozen/non-authorized runs
8. Document verification: each artifact, each check, each result, key availability, gaps

**Final decision:** PASS if all 7 criteria met. FAIL if any check fails. INCONCLUSIVE if key unavailable and structural checks pass but full blinding verification is gap — document the gap.

---

## 6. Agent #5: Experimental Design Integrity (`experimental_design_integrity.json`)

**6 design dimensions analyzed — all covered by existing evidence.**

### What it found

| Dimension | Where covered | State |
|---|---|---|
| Topology/factor identity | FREEZE_MANIFEST.md sec 2 (pilot matrix: 4 conditions × 5 topologies × 9 failure counts) + protocol sec 4.2-4.3 (topology/condition descriptions) | COVERED — frozen values recorded; protocol documents matrix |
| Seed/RNG separation | Protocol sec 4.1 (deterministic given seed) + freeze manifest sec 5 (master seed 20260817, stream derivation, PCG64, Generator) | COVERED — deterministic derivation documented; master seed and RNG chain recorded |
| Trial ordering | FREEZE_MANIFEST.md sec 5 (topology order: ring → pdmal → random_regular → small_world → complete) | COVERED — topology order explicitly recorded |
| Exclusion rules | `artifact_schema.py` `validate_seed_record()` (excluded boolean + exclusion_reason) + `pilot_artifact_schema.py` `REQUIRED_RECORD_FIELDS` (both required) | COVERED — exclusion contract defined by artifact schema |
| Failure semantics | FREEZE_MANIFEST.md sec 8 (executor acceptance: failure at iteration 33, recovery at iteration 66) | COVERED — failure/recovery model recorded |
| Stopping rules | Protocol sec 4.5 (fixed 100 iterations, no convergence-based early stopping; consensus threshold < 0.01 is convergence criterion for task execution, not efficacy threshold) | COVERED — stopping rule explicitly documented |

### Conclusion: Fold into predicates 5 and 7. No 10th predicate needed.

All six design integrity dimensions are already covered by existing evidence in the frozen apparatus. No dimension represents a material failure mode not already covered by an existing control. The stopping rule (P-EXP-8) is satisfied.

---

### Corrected Scoring — 0/9 Unambiguously Closed

| Predicate | Canonical Name | State | PR #77 adds | Gap |
|---|---|---|---|---|
| P1 | **Candidate integrity** | PARTIAL (SHA identified ≠ verified) | Candidate `fec7a6f` + docs claiming closure | Full verification pending; new freeze BLOCKED |
| P2 | **Execution contract** | PARTIAL (gating exists, not CI-tested) | `require_frozen_commit()`, `require_pilot_authorization()` | CI execution required; env-var mechanism not fully specified |
| P3 | **Artifact contract** | PARTIAL (validation contract exists, runner doesn't call inline) | `pilot_artifact_schema.py` (new module, not wiring existing) | Inline validation missing; SHA methods may diverge; version confusion |
| P4 | **Security / blinding integrity** | PARTIAL (tests exist, not CI-executed) | `test_security_controls.py` (6 tests) + `pdmal-preauth-security.yml` | CI execution required; monkeypatching for env gates |
| P5 | **Provenance / reproducibility** | PARTIAL (recorded, env/sidecar not fully verified) | 5 new docs + 2 modified docs | Environment fingerprint not deeply tested; sidecar integrity for artifacts not verified |
| P6 | **Durable evidence custody** | OPEN (file on disk, not committed; archive root TBD) | NOT ADDRESSED | File still uncommitted; archive root still not set |
| P7 | **Scientific target specification** | PARTIAL (construct/estimand/endpoint specified; primary contrast OPEN) | NOT ADDRESSED (correctly) | 4 contrast candidates, none selected; success/falsification criteria not declared; analysis plan docs NOT FOUND |
| P8 | **Analysis lock** | OPEN (analysis implementation SHA not recorded; analysis plan docs NOT FOUND) | NOT ADDRESSED (correctly) | Requires primary contrast adjudicated + analysis implementation/configuration SHA frozen before unblinding |
| P9 | **Independent verification** | DEFINED (10-layer architecture designed) but NOT EXECUTED | NOT ADDRESSED (correctly) | Requires actual artifacts + artifact-producing tree + key custody; cannot execute until pilot data exists |

**Authorization = separate governance transition** (NOT a predicate). Requires P1–P8 verified closed + P9 independent verification complete + new freeze created + freeze verification passed.

---

### 8. Refined Roadmap

```
Current pre-freeze state

`3510b868...` is the historical superseded freeze; the corrected apparatus is PRE-FREEZE and
not yet frozen.

Loc...[truncated]
    ├── ENGINEERING CLOSURE (PR #77 as vehicle, not state transition)
    │   ├── Corrected runner (ConsensusTask) — PR #77 provides
    │   ├── Security controls (test_security_controls.py + CI) — PR #77 provides
    │   ├── Pilot artifact schema (pilot_artifact_schema.py) — PR #77 provides
    │   ├── Inline validation wiring — NOT in PR #77; REQUIRED
    │   ├── SHA computation consistency — NOT verified; REQUIRED
    │   ├── Schema version differentiation — NOT addressed; RECOMMENDED
    │   ├── test_execution_contract.py fix — NOT in PR #77; REQUIRED (test #5 will FAIL)
    │   ├── Durable retention — NOT in PR #77; REQUIRED (commit file, set archive root)
    │   └── Merge only when policy permits AND mainline consistent with candidate
    │
    ├── SCIENTIFIC CLOSURE (NOT in PR #77 scope — methodological decision)
    │   ├── Primary contrast adjudication (choose from 4 candidates; dgaf vs null most natural)
    │   ├── Specify exact estimand, direction, success/falsification criteria
    │   ├── Multiplicity family + correction strategy
    │   └── Record decision authority, date, protocol/manifest SHA
    │
    ├── OPERATIONAL EVIDENCE CLOSURE (COMPLETE — non-empirical)
    │   ├── Runtime characterization (Run #14) — COMPLETE
    │   ├── Blinding operational test (Run 32113226935) — COMPLETE (synthetic custody only)
    │   ├── Executor acceptance (2 seeds × 180 = 360 observations) — COMPLETE
    │   └── Topology fingerprints — COMPLETE (deterministic, recorded)
    │
    ▼
PREDICATE EVALUATION (derived control layer — NOT self-authorizing)
    │   Each predicate state derived from underlying evidence:
    │   - Git SHA → Git is authoritative
    │   - Governance decision → governance record is authoritative
    │   - Artifact hash → retained artifact + independently computed hash
    │   - Predicate state → derived from underlying evidence
    │   - Status file declaring closed → NOT authoritative by itself
    ▼
INDEPENDENT VERIFICATION (10-layer architecture: CI + separate audit)
    │   CI (10 deterministic checks) + Separate audit (8 evidence-level checks)
    │   Key gaps: without blinding key → structural checks only; env-var → manual attestation
    ▼
NEW FREEZE (new internally coherent snapshot — NOT amending 3510b86889)
    │   Must contain: protocol, task spec, executor, environment, dependency lock,
    │   topology definitions + fingerprints, failure model, artifact schema (resolved),
    │   retention/custody rules, blinding controls (with key custody procedure),
    │   analysis spec (with adjudicated primary contrast), security controls,
    │   freeze metadata (actual commit SHA, timestamp, author)
    │   Must NOT contain: unresolved placeholder as finalized state,
    │   claims of closure without underlying evidence
    ▼
FREEZE VERIFICATION (8-step procedure with PASS/FAIL/INCONCLUSIVE)
    ▼
AUTHORIZATION (separate governance decision)
    │   Explicitly assert required predicates satisfied
    │   Only then: PILOT AUTHORIZED
    ▼
AUTHORIZED PILOT (50 seeds → blinded observations → artifact validation →
                   provenance verification → retained dataset → unblinding →
                   pre-specified analysis → result)
    N becomes > 0
```

---

## 9. What This Report Does Not Claim

- **N > 0:** No empirical data collection has occurred. The 360 acceptance observations are executor/apparatus acceptance verification (N=0). The 72/72 characterization trials are operational verification (N=0).
- **Pilot authorization:** NOT GRANTED. This report does not authorize empirical execution.
- **Protocol freeze:** PRE-FREEZE. The protocol is not frozen. Primary contrast adjudication is OPEN.
- **PR #77 as verified closure:** PR #77 provides a candidate implementation. Its integrity as a "complete candidate" has NOT been independently verified end-to-end.
- **Efficacy:** No claims about DGAF effectiveness in any real-world setting. The construct is execution robustness characterization, not efficacy demonstration.
- **Historical evidence promotion:** The historical implementation freeze at `3510b86889` is retained as historical evidence. It is NOT promoted to current-head evidence.
- **Schema compatibility:** `artifact_schema.py` and `pilot_artifact_schema.py` sharing version "1.0" does NOT mean they are compatible. They are semantically incompatible.
- **Test #5 status:** The test asserts executor NOT implemented, and the executor IS implemented at local HEAD. But the test has NOT been updated, and PR #77 does NOT touch it.

---

## 10. QA Assertion Summary

### What is asserted (by evidence)

| Assertion | Evidence |
|---|---|
| `pilot_artifact_schema.py` is the canonical module for pilot artifacts | Agent #1; both modules share version "1.0" but are semantically incompatible |
| FFCR is the primary endpoint, per-condition per-seed, higher is better | Agent #2; confirmed in protocol and freeze manifest |
| Primary contrast is OPEN — 4 candidates, none selected | Agent #2; confirmed in PRIMARY_CONTRAST_ADJUDICATION.md |
| PR #77 provides a candidate implementation with 5 new docs + 2 modified docs | Agent #3; 7 docs read from PR #77 branch |
| PR #77 docs are internally consistent: historical freeze retained as evidence, corrected runner is new candidate, primary contrast OPEN, NOT GRANTED, N=0 | Agent #3; cross-document analysis |
| 10-layer independent verification architecture with CI (10 checks) + separate audit (8 checks) | Agent #4; designed from PR #77 runner, tests, schema, CI workflow |
| 6 experimental design dimensions all covered by existing evidence | Agent #5; all files read; no new predicate needed |
| 0/9 predicates unambiguously closed | Synthesis of all 5 agents; corrected scoring from expert-panel feedback |

### What is NOT asserted (governance boundary)

| Boundary | Reason |
|---|---|
| Pilot authorization | NOT GRANTED — separate governance decision |
| Protocol freeze | PRE-FREEZE — primary contrast OPEN |
| PR #77 as verified closure | Candidate SHA identified ≠ verified; "verified: NO" per PRE_AUTHORIZATION_VERIFICATION_RECORD |
| Efficacy | N=0 — no empirical data; construct is execution robustness, not efficacy |
| Historical evidence promotion | Historical freeze retained as evidence, NOT promoted to current-head |
| Schema compatibility | Both modules share "1.0" but are semantically incompatible |
| Test #5 status | Test asserts executor NOT implemented; executor IS implemented; test NOT updated |

---

## 11. QA Assertion Report — Conclusion

The DGAF/PDMAL pre-authorization completeness work has produced a candidate implementation (PR #77) and a comprehensive verification architecture (10-layer independent verification design). The candidate is implemented but not verified end-to-end. The scientific target specification is partially complete (construct, estimand, endpoint specified) but the primary contrast is unadjudicated. The predicate matrix stands at 0/9 unambiguously closed.

The refined roadmap replaces "merge PR #77 → schema → contrast → retention → analysis → audit → freeze → authorize → pilot" with a structured sequence: engineering closure (PR #77 as vehicle) → scientific closure (contrast adjudication) → operational evidence closure → predicate evaluation (derived layer) → independent verification (10-layer audit) → new freeze → freeze verification → authorization → authorized pilot (N > 0).

N = 0 throughout. Pilot authorization NOT GRANTED. `3510b868...` is the historical superseded freeze; the corrected apparatus is PRE-FREEZE and not yet frozen.

---

*Prepared from 5 agent-submitted artifacts + corrected sprint report analysis on 2026-08-21.*
