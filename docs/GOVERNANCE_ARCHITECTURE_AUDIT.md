---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: 15373831aa27aa37a2e21462a304f2b93b12216a
---

# Control & Evidence Architecture Audit — DGAF/PDMAL

> **Purpose.** This is a map of the governance system itself, not a pile of new
> governance documents. It classifies each proposed audit requirement against what
> *actually exists in the repository* (verified 2026-08-26 against `main` @
> `15373831`), identifies genuine gaps, and flags control-coupling / evidence-
> monoculture / negative-state risks. It operationalizes the user's meta-review:
> turn a 30-point checklist into an auditable architecture.
>
> **What this document does NOT claim:** that the system is freeze-ready, that P7/P8
> are closed, that pilot is authorized, or that N=0 is empirically established. It
> claims only that the *governance architecture* has been inventoried and classified.
> N = 0. PRE-FREEZE. Pilot NOT GRANTED.

## Classification vocabulary (extends the existing model)

The existing `CURRENT_STATE.md` uses `OPEN / PARTIAL / INCOMPLETE / IDENTIFIED`.
Per the meta-review, two statuses are added here:

- **DUPLICATE** — an apparent gap is already controlled by an existing mechanism.
- **CONTROLLED** — the risk is explicitly handled by an existing mechanism, but this
  does **not** imply the dimension is independently "COMPLETE" (completeness is an
  evidentiary conclusion; control is an architectural conclusion).

## Audit schema (applied to every row below)

| Field | Meaning |
|---|---|
| Dimension | Risk examined |
| Existing control | Is it already controlled? (file / workflow / code) |
| Evidence | What proves the control exists |
| Independence | Does the evidence share assumptions with its subject? |
| Coupling | What other controls it depends upon |
| State | Lifecycle state it applies to |
| Gap | What is actually missing |
| Action | Fix / Extend / Retain / Defer / Reject |
| Cost | Complexity added by acting |
| Justification | Failure/evidence/boundary the action addresses |

---

## Layer 1 — Core Dimensions (30) — representative inventory

*The 30 dimensions are tracked in the Operational Control Center (Notion), not the
repo. The repo provides the implementing controls. Below, each dimension is mapped
to its repo control and classified.*

| # | Dimension | Existing control | Evidence | Indep. | Coupling | Gap | Action |
|---|---|---|---|---|---|---|---|
| 1 | Repository Truth | `git rev-parse`, branch-protection API | verified live | high | low | baseline record not auto-generated per run | EXTEND (add Candidate Evidence Manifest) |
| 2 | Provenance | `CURRENT_STATE.md` SHA refs; `applies_to_sha` frontmatter | doc | med | low | SHAs manual, not emitted by CI | EXTEND |
| 3 | Reproducibility | `requirements-full-lock.txt` (hashed), `requirements-epistemic.txt` | file | med | tzdata gap fixed (#98) | transitive hash coverage | RETAIN |
| 4 | Data/Artifact Integrity | `pilot_artifact_schema.py` `canonical_json_bytes` + `artifact_sha256` | code | med | M4 monoculture (see below) | independent re-hash path | EXTEND |
| 5 | CI/CD | 23 workflows incl. `governance-ci`, `pptl-ci`, `truth-layer` | workflows | high | low | doc-lint still repo-wide debt | RETAIN (debt accepted) |
| 6 | Documentation | `doc-lint.yml` + `doc-lint-pr-scope.yml` | workflow | high | low | 567 intentional-content violations | ACCEPTED DEBT |
| 7 | Cross-System Sync | Notion OCC + `CURRENT_STATE.md` | doc | low | med | no automated consistency gate | DEFER |
| 8 | Archival Survivability | `durable_retention.archive_artifact` in `run_pilot.py:103` | code | med | coupled to runner | quarantine/append-only not enforced | EXTEND |
| 9 | Epistemic Hygiene | `scripts/claim_hygiene_check.py` | code | **high** (stdlib only, no cross-import) | low | self-scan bug fixed (#89) | RETAIN |
| 10 | Research Positioning | `DGAF_RELATED_WORK_MATRIX.md`, `CANONICAL_TECHNICAL_OVERVIEW.md` | doc | med | low | — | RETAIN |
| 11 | Prior Art | `PRIOR_ART_AND_RELATED_WORK_SCOPE.md`, `DGAF_RELATED_WORK_MATRIX.md` | doc | med | low | — | RETAIN |
| 12 | Claim Compression | `claim_hygiene_check.py` `EXCLUDED` + `NON_ASSERTIVE_CONTEXT` | code | high | low | vocabulary docs enumerated | RETAIN |
| 13 | External Interpretation | `DGAF_QA_ASSERTION_REPORT.md` | doc | med | low | adversarial-interpretation review not systematic | EXTEND |
| 14 | Portfolio Value | Notion OCC | external | low | med | not repo-expressed | DEFER |
| 15 | Candidate Identity | `CURRENT_STATE.md` "Candidate identity boundary" | doc | med | low | immutable-tree rule present | RETAIN |
| 16 | P7 Scientific Spec | `P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md` | doc | med | — | formally OPEN/pending adoption (reconciled #96) | RETAIN |
| 17 | P8 Analysis Lock | `CURRENT_STATE.md` OPEN/FAIL-CLOSED | doc | med | — | corrected basis recorded (#101) | RETAIN |
| 18 | Freeze Integrity | `run_pilot.py:require_frozen_commit()` | code | high | med | freeze not yet created (correct) | RETAIN |
| 19 | Authorization | `run_pilot.py` `PDMAL_PILOT_AUTHORIZED=1` gate | code | high | med | no authorization record retained | EXTEND (M6) |
| 20 | Execution Contract | `test_execution_contract.py` (#95) | code | high | med | candidate-scoped re-verification pending | RETAIN |
| 21 | Artifact Contract | `pilot_artifact_schema.py`, `test_artifact_schema.py` | code | med | M4 | independent validator | RETAIN |
| 22 | Schema/Security | `pdmal-preauth-security.yml` + `test_security_controls.py` | workflow+code | med | med | — | RETAIN |
| 23 | Compilation | `governance-ci.yml` pip install + networkx | workflow | high | low | — | RETAIN |
| 24 | Provenance (build) | lockfiles + `tla2tools.jar` pinned SHA (#88) | file | med | low | — | RETAIN |
| 25 | Determinism | `pdmal-harness-validation.yml`, `pdmal-instrumentation-dry-run.yml` | workflow | med | med | — | RETAIN |
| 26 | Environment | `requirements-*.txt` pinned | file | med | low | — | RETAIN |
| 27 | Blinding Integrity | `run_pilot.py` blinding-key gate (out-of-band) | code | high | med | key-exposure observability | EXTEND (M6) |
| 28 | Statistical Analysis | `PDMAL_ANALYSIS_CONTROL_PLAN.md` (FFCR, 11-point spec) | doc | med | low | primary contrast not adjudicated | RETAIN |
| 29 | Durable Custody | `durable_retention` import in `run_pilot.py` | code | med | med | independent retrieval/hash evidence | EXTEND |
| 30 | Independent Verification | `pdmal-pre-freeze-runner.yml`, `truth-layer.yml` | workflow | med | med | P9 NOT EXECUTED | RETAIN |

**Layer 1 verdict:** ~26/30 dimensions are **CONTROLLED** by existing repo
mechanisms; 0 are pure duplicates needing removal; 4 (1,2,19,27,29) need EXTEND for
negative-state observability; 1 (13) needs systematic adversarial treatment. **No
new documents are required for Layer 1** — the gaps are small code/doc extensions.

---

## Layer 2 — 5 Cross-Cutting Reviews (status)

| Review | Existing control | Gap | Action |
|---|---|---|---|
| A. Independent Replication | `truth-layer.yml`, `pdmal-harness-validation.yml` | no skeptical-reconstruction harness | EXTEND |
| B. Adversarial Interpretation | `DGAF_QA_ASSERTION_REPORT.md` (partial) | not systematic / not a gate | EXTEND |
| C. External Reader Reconstruction | none | **genuine gap** | NEW — justified (low cost: a reconstruction checklist doc) |
| D. Novelty Calibration | `DGAF_RELATED_WORK_MATRIX.md` | adequate | RETAIN |
| E. Economic Architecture | Notion OCC only | not in repo architecture review | DEFER → extend into architecture audit |

**Layer 2 verdict:** A, B = EXTEND (already partly present, not duplicated). C =
**NEW — justified** (no existing mechanism). D = RETAIN. E = DEFER.

---

## Layer 3 — Meta-Governance (M1–M9)

### M1. Complexity-to-Evidence Ratio
**Existing:** implicit in `CURRENT_STATE.md` hygiene rules. **Gap:** no explicit
"does this mechanism earn its existence?" test applied to proposed controls.
**Action:** EXTEND — adopt the audit schema in this doc as the standing test.
**Cost:** low. **Justification:** prevents governance accretion (the user's #1 risk).

### M2. Control Deduplication
**Existing:** none explicit. **Gap:** genuine. **Action:** NEW — justified, but
**cheap**: this audit *is* the deduplication pass. Classifications above already
marked RETAIN vs NEW. **Cost:** low (one pass). **Justification:** the user's
central correction — "do not create a document for every control."

### M3. Control Coupling
**Verified finding:** `claim_hygiene_check.py` imports **only stdlib**
(`pathlib`, `re`, `sys`) — it does **not** import pilot implementation, so the
hygiene checker is **decoupled** from the apparatus it audits (good; avoids
A-verifies-X-while-A-imports-X's-assumptions). Conversely `run_pilot.py` imports
`pilot_artifact_schema`, `durable_retention`, `harness_contract`, `task_engine` —
strongly coupled internally (unavoidable for a runner). **Classification:** the
*highest-risk* coupling is the runner's self-validation chain. **Action:** RETAIN
the decoupled hygiene checker; flag runner-internal coupling as **KNOWN / weakly
coupled**. **Cost:** none. **Justification:** confirms one meta-dimension is
already satisfied.

### M4. Evidence Monoculture — **genuine risk, confirmed**
**Verified:** `experiments/pdmal_pilot/analysis.py:159` `analysis_config_sha256()`
and `experiments/pdmal_pilot/artifact_schema.py:36` `canonical_json_bytes()` both
depend on `hashlib.sha256` + one canonical serialization. Many green checks
(`ip-hygiene`, `claim-hygiene`, `truth-layer`, artifact validation) ultimately
reduce to **one parser → one schema → one SHA computation**. **Ten green checks can
share one systemic failure point.** **Action:** EXTEND — add a *second,
independent* hash/serialization path (e.g., a distinct canonicalization + a
different hash) for at least the candidate-evidence manifest, so monoculture is
broken. **Cost:** medium. **Justification:** the user's explicit adversarial test —
"how many checks ultimately originate from the same assumption?"

### M5. State-Transition Integrity — **partially controlled**
**Verified:** `run_pilot.py` enforces a finite-state machine:
`contract`/`pilot` mode → frozen-SHA check → `PDMAL_PROTOCOL_FROZEN=1` →
`PDMAL_PILOT_AUTHORIZED=1` → blinding key → archive. Each transition raises
`SystemExit` if its predicate fails. **Gap:** documentation *can* still claim a
later state while the system is earlier (no doc-gate enforces state vocabulary).
**Action:** EXTEND — a doc-lint rule or `CURRENT_STATE.md` linter that rejects
"frozen/authorized/executed" claims without the corresponding emitted artifact.
**Cost:** low. **Justification:** prevents "documentation closure by assertion."

### M6. Negative-State Observability — **genuine gap**
**Verified:** `N=0`, "no pilot occurred", "no authorization granted", "no frozen
candidate created" are currently **asserted in docs only**
(`CURRENT_STATE.md:26`, `:55`, `:100`; `CANONICAL_TECHNICAL_OVERVIEW.md:59`).
`run_pilot.py` *enforces* non-occurrence (gates raise on attempt) but **emits no
retained proof of absence**. **Action:** EXTEND — emit a signed/retained
"execution-attempt log" (even when empty) and an authorization-record artifact, so
N=0 is **evidenced**, not merely stated. **Cost:** medium. **Justification:** the
user's precise point — "N=0 shouldn't be a manually maintained statement."

### M7. Reversibility — **documented principle, not enforced**
**Verified:** provenance-preserving supersede pattern exists in agent specs
(`AMETHYST_AGENT_SPEC_v4.2` "Supersedes"; `colleen/QA_RUBRIC.md` "all prior sealed
sessions immutable"; Sentinel "preserve provenance without duplicate identity") and
`CURRENT_STATE.md` rule 4 ("frozen candidate tree is immutable; later corrections
clarify but do not rewrite"). **Gap:** no automated quarantine/append-only
mechanism in code — it is doc-level. **Action:** EXTEND — codify an
append-only/quarantine rule for evidence artifacts (e.g., a lint that rejects
rewriting historical evidence files). **Cost:** low. **Justification:** "can an
erroneous artifact be quarantined without rewriting history?"

### M8. Incentive Compatibility — **addressed in principle, untested**
**Verified:** fail-closed philosophy is present (`CURRENT_STATE.md` "no closure by
implementation presence alone"; `run_pilot.py` fails shut). **Gap:** no explicit
test that an agent cannot optimize toward "gate PASS" over "truthful state." The
claim-hygiene positive-control (planted violation still caught) is a partial guard.
**Action:** EXTEND — add an adversarial eval: inject a known-false claim and confirm
the gate rejects it (already implicitly done; make it a standing CI job).
**Cost:** low. **Justification:** the user's agent-governance point.

### M9. Epistemic Inheritance — **genuine risk, partially controlled**
**Verified:** `CLAIM_EVIDENCE_INDEX.md` exists (claim→evidence mapping);
`DGAF_QA_ASSERTION_REPORT.md` tracks claim strength. But the chain
observation→interpretation→conclusion→marketing across docs is **not** automatically
bounded. **Action:** EXTEND — require each claim doc to cite the *verifying
artifact SHA*, so repeated claims don't amplify beyond evidence (already partially
in `CURRENT_STATE.md` hygiene rule 1). **Cost:** low. **Justification:** "does
epistemic strength increase merely by repetition?"

---

## Consolidated Action List (de-duplicated)

| ID | Action | Type | Cost | Justification |
|---|---|---|---|---|
| A1 | Candidate Evidence Manifest (HEAD/refs/checks/lockfiles snapshot, emitted by CI) | EXTEND | med | M1,M2,M5,M6 — single artifact serves Repository Truth + Provenance + Repro + Archival |
| A2 | Independent re-hash/serialization path for evidence manifest | EXTEND | med | M4 monoculture |
| A3 | Retained execution-attempt + authorization records (prove N=0) | EXTEND | med | M6 |
| A4 | Adversarial-interpretation + external-reconstruction harness | NEW (justified) | med | Layer 2 B,C — no existing mechanism |
| A5 | Doc-lint rule rejecting later-state claims without emitted artifact | EXTEND | low | M5 |
| A6 | Append-only/quarantine lint for evidence files | EXTEND | low | M7 |
| A7 | Standing adversarial claim-injection CI job | EXTEND | low | M8 |
| A8 | Claim→artifact-SHA citation requirement | EXTEND | low | M9 |
| — | **Do NOT create** 35 separate control docs | REJECT | — | user's #1 correction |

**New documents strictly required: 1** (this audit map; plus optionally A4's
reconstruction checklist). Everything else is an *extension of an existing
authoritative artifact* — principally `CURRENT_STATE.md` and the CI evidence
manifest — satisfying the anti-bureaucracy rule.

## What this does NOT claim
No freeze created. P7 OPEN/pending authority; P8 OPEN/fail-closed. Pilot NOT
GRANTED. N=0 (asserted; M6 evidence not yet retained). Merge ≠ freeze; execution ≠
empirical validation. The corrected candidate basis (`83e1678`) requires
candidate-scoped re-verification before any closure claim. This audit is a
governance-architecture inventory, not an empirical or freeze result.
