# Orchestration Patterns Log — DGAF/PDMAL Completion Session 2026-08-21

**Session:** DGAF/PDMAL Execution Readiness — Corrected Assessment  
**Date:** 2026-08-21  
**HEAD:** `3510b86889cd341f7a7cf9ab684fd37b2fafd758` (main)  
**PR #77 branch:** `chore/preauth-completeness-2026-08-20`, head `94fb6fd`  
**N = 0 throughout.** Pilot authorization NOT GRANTED.  
**Prepared from:** 5 agent-submitted artifacts + expert-panel corrections (~90% agreement, 8 material corrections)  

---

## 1. Session Overview

This session resolved the DGAF/PDMAL execution readiness assessment by integrating five surgical subagent artifacts with an expert-panel structured critique. The sprint report (`DGAF_3NODE_META_ORCHESTRATION_SPRINT_2026-08-21.md`) was superseded by a corrected document incorporating validated expert corrections and agent findings. All orchestration patterns observed during this session are logged below for the pattern registry.

**Key outcomes:**

- Sprint report scored 9/10 by expert panel; corrected document fully supersedes it
- Predicate scoring corrected from 1/9 to 0/9 unambiguously closed
- 8 material expert corrections identified, validated, and applied
- 5 agent artifacts (JSONs on disk) integrated into corrected assessment
- 3 unsupported claims flagged; 5 missing content items identified

---

## 2. Pattern 1 — Subagent Path Resolution

**Observed:** All 5 post-sprint agents dispatched from this session resolved file paths to `D:/DGAF-Framework-LEGACY/...` instead of `D:/DGAF-Framework/...`. This caused agents to read files from the wrong directory and hit max_iterations while searching for files that exist at the correct path.

**Root cause:** Path resolution defaults diverged from the working directory specification. Agents relying on relative paths or auto-derived workspace paths landed on a legacy directory that no longer held the current repository state.

**Fix applied:** Specify `--git-dir=D:/DGAF-Framework/.git --work-tree=D:/DGAF-Framework` in all git commands. Specify `D:/DGAF-Framework` explicitly in all `read_file` paths. Agents that used these explicit paths succeeded; agents that relied on relative or auto-derived paths failed.

**Lesson:** Path disambiguation is a first-order operational concern for multi-agent sessions. The workspace root must be explicit in every tool call that performs file I/O or git operations, not inferred.

**When to apply:** Any multi-agent session where agents operate across potentially ambiguous directory structures. Always pass explicit `--git-dir` and `--work-tree` flags to git, and use absolute paths in file reads.

---

## 3. Pattern 2 — JSON Output Before Max-Iterations

**Observed:** Agents that need to read many files AND write structured JSON output should write the output before the iteration budget is exhausted. At approximately 70% of the iteration budget, if research is incomplete, write what you have — a partial JSON that exists on disk is better than no JSON.

**Rationale:** A partial artifact preserves the agent's findings up to that point and allows the orchestrating session to assess completeness. An agent that exhausts its iteration budget without writing anything yields zero evidence and forces re-dispatch.

**When to apply:** Any agent task that involves file reading/research AND structured output generation (JSON, markdown tables, evidence cards). Structure the task so the write path is reachable early, before the full research budget is consumed.

**Variant observed:** The 5 surgical subagents each produced a JSON artifact. Those that completed within budget wrote complete JSONs (5/5 on disk). The pattern is: write incrementally or write early with a completeness flag rather than waiting for full coverage.

---

## 4. Pattern 3 — Expert-Panel Correction Integration

**Observed:** When an expert panel provides structured critique, the correction process follows a defined seven-step sequence:

1. **Read the critique in full** — consume the entire expert panel output before approaching individual corrections
2. **Identify each material correction** — extract every numbered correction with its category (critical/moderate/supportive)
3. **Verify each correction against source files** — grep, read, and confirm the correction is factually grounded in repository state
4. **Apply corrections that are validated** — implement corrections where source evidence supports them
5. **Document which corrections were applied and why** — maintain a correction application table with status (applied/not applied) and rationale
6. **Note any corrections that could not be applied** — record reason for each non-applied correction (e.g., out of scope, not verifiable at N=0)
7. **Produce a refined document that supersedes the original** — the corrected document replaces, not patches, the original

**Expert corrections applied in this session (C1–C8):**
| # | Category | Correction | Applied |
|---|---|---|---|
| C1 | Critical | Predicate matrix NOT self-authorizing; derived control layer, different facts have different authorities | ✅ |
| C2 | Critical | 0/9 not 1/9; no predicate unambiguously closed | ✅ |
| C3 | Moderate | Documentation preservation not aggressive consolidation; merge only when same authority/temporal scope/purpose | ✅ |
| C4 | Corrective | Test hierarchy tied to candidate, not main | ✅ |
| C5 | Critical | Candidate mechanism (#1–#3) before PR #77 merge; PR #77 as engineering vehicle inside architecture | ✅ |
| C6 | Corrective | Expand scientific spec to full estimand chain (construct → estimand → endpoint → contrast → direction → success → falsification → unit → multiplicity) | ✅ |
| C7 | Corrective | Augmented anti-yellow-tape decision function: + explicit "Does this control provide independent information?" test | ✅ |
| C8 | Corrective | CI vs separate audit distinction: CI for deterministic, separate audit for independence-distinct; CI cannot provide 6 items | ✅ |

**Lesson:** Expert critique is a structured input, not a veto. Each correction must be verified against source evidence before acceptance. The correction application record is itself an evidence artifact.

---

## 5. Pattern 4 — Surgical Subagent Dispatch

**Observed:** Five subagents were dispatched post-sprint, each with a distinct analytical domain:

1. **Schema Resolution** — `artifact_schema.py` vs `pilot_artifact_schema.py` compatibility, inline validation wiring gap
2. **Estimand Chain** — FFCR construct, estimand, endpoint, primary contrast (3 candidates, none selected), missing items
3. **PR #77 Doc Briefing** — 7 docs (5 new + 2 modified), 373 lines, predicate coverage mapping
4. **Independent Verification Design** — 7-layer CI + separate audit architecture, 10-step freeze verification procedure
5. **Experimental Design Integrity** — 6 dimensions, all covered by existing evidence; recommendation against creating 10th predicate

**Dispatch pattern:** Each agent receives a bounded scope (one document or one analytical dimension), a clear deliverable format (JSON with specific fields), and an explicit epistemic boundary (N=0, no empirical claims). The orchestrating session integrates the outputs.

**When to apply:** Complex assessments spanning multiple independent analytical dimensions. Dispatch surgical agents rather than attempting monolithic analysis. Each agent's JSON output becomes a citable evidence artifact.

---

## 6. Pattern 5 — 9-Predicate Model Abstraction

**Observed:** The 9-predicate model turns 30+ individual checks into 9 material invariants. This abstraction was validated by the expert panel as the right organizational structure.

**The 9 predicates:**
| # | Predicate | Score (corrected) |
|---|---|---|
| P1 | Candidate Integrity | PARTIAL — SHA identified, full verification pending |
| P2 | Execution Governance | PARTIAL — gating functions exist, CI not executed |
| P3 | Artifact Integrity | PARTIAL — schema exists, inline validation NOT wired |
| P4 | Security/Blinding Integrity | PARTIAL — tests exist (6 adversarial), CI not executed |
| P5 | Provenance/Reproducibility | PARTIAL — provenance recorded, env/sidecar not fully verified |
| P6 | Durable Evidence Custody | OPEN — file committed at local HEAD, absent from candidate branch |
| P7 | Scientific Target Specification | PARTIAL — construct/estimand/endpoint specified, contrast OPEN |
| P8 | Analysis Lock | OPEN — analysis SHA not recorded, plan certificate is planning-record only |
| P9 | Independent Verification | NOT EXECUTED — 7-layer architecture designed, not executed, N=0 |

**Lesson:** Predicate models are derived control layers, not replacements for underlying authorities. Each predicate score must be traceable to specific evidence, not asserted by a status file. The 9-predicate structure provides a tractable closure roadmap without collapsing the underlying evidentiary complexity.

---

## 7. Pattern 6 — Different Authorities for Different Facts

**Observed:** The corrected execution readiness document establishes a layered authority model:

```
                AUTHORITATIVE FACTS
                /       |        \
             Git     Governance   Evidence
               \        |        /
                \       |       /
                 ↓      ↓      ↓
             PREDICATE EVALUATOR (derived control layer)
                      ↓
                 FREEZE READINESS
```

**Authority assignments:**

- **Git SHA** → Git is authoritative
- **Governance decision** → governance record is authoritative
- **Artifact hash** → retained artifact + independently computed hash
- **Predicate state** → derived from underlying evidence, NOT from a status file declaring it closed

**Critical principle:** If a YAML file's status field can close a predicate, configuration becomes evidence. This violates P-EXP-2: Configuration must not become evidence.

**Verification:** `run_pilot.py` at PR #77 head does NOT import `artifact_schema` or `pilot_artifact_schema` (grep count: 0). The runner's SHA computation path is independent of the schema module's `canonical_json_bytes()`. This confirms schema status files are NOT self-authorizing.

**When to apply:** Any governance or closure model where status declarations could be mistaken for evidence. Always identify which authority governs each fact type, and ensure predicate state is derived, not declared.

---

## 8. Pattern 7 — Historical Freeze Retention as Evidence

**Observed:** The historical freeze at `3510b86889` is RETAINED AS HISTORICAL EVIDENCE for the old runner. It is NOT reused as the current freeze. The corrected apparatus is PRE-FREEZE and not yet frozen.

**Evidence chain:** `3510b86889` (historical freeze) → retained as evidence that the old runner was frozen at that commit → corrected runner at `4983f44a` is a NEW candidate → new freeze gates must close before a new freeze is created.

**Key distinction:** `FREEZE_MANIFEST.md` committed version says FROZEN (HISTORICAL). Working-tree version says PRE-FREEZE. Both are valid at their respective layers — the committed version is historical evidence; the working-tree version is current state. They answer different questions at different times.

**Lesson:** Superseded states should be preserved as historical evidence, not silently overwritten. Temporal separation is legitimate when the documents answer different questions (what was frozen when vs what is the current state).

---

## 9. Pattern 8 — Temporal/Provenance Documentation Preservation

**Observed:** The expert panel corrected the sprint report's proposal for "retrospective document consolidation" — collapsing CURRENT_STATE.md, PROJECT_STATUS.md, PDM_CURRENT_CONTROL_STATE.md, FROZEN_STATE_COMMIT.md, etc.

**Correction:** Merge documents only when they represent the same authority, same temporal scope, and same purpose — not merely because they contain overlapping text. Some apparent redundancy is legitimate temporal/provenance separation.

**Document classification applied:**
| Document | Authority | Temporal scope | Purpose | Action |
|---|---|---|---|---|
| `CURRENT_STATE.md` | Repository state | Current | Canonical state snapshot | Preserve |
| `FREEZE_MANIFEST.md` | Experimental identity | Freeze-time + ongoing | Immutable identity | Preserve as immutable |
| `PRIMARY_CONTRAST_ADJUDICATION.md` | Scientific decision | Adjudication-time | Scientific gate | Preserve |
| `PROJECT_STATUS.md` | Project management | Current | Public/project status | Preserve |
| `PDMAL_CURRENT_CONTROL_STATE.md` | Control plane | Current | Control state tracking | Preserve |
| `FROZEN_STATE_COMMIT_2026-08-20.md` | Historical | Historical | Frozen state snapshot | Preserve as immutable evidence |

**Anti-yellow-tape rule:** Consolidation is justified only when it reduces uncertainty or prevents a material failure mode not already covered. Aggressive consolidation that destroys historical traceability is a failure mode, not a hygiene improvement.

---

## 10. Pattern 9 — CI vs Separate Audit Distinction

**Observed:** Independent verification requires distinguishing deterministic CI checks from evidence-level separate audit. Same CI creating and verifying artifacts provides weaker independence than a distinct observation path.

**Architecture (from Agent #4):**
| Layer | CI (deterministic) | Separate audit (evidence-level) |
|---|---|---|
| 1. Frozen-commit gating | `require_frozen_commit()` code invariant | Independently re-resolve SHA; verify match |
| 2. Protocol freeze authorization | N/A | Manual attestation of env var state + key custody |
| 3. Task substitution prevention | AST parse: ConsensusTask present, ScriptedTask absent | Sufficient by itself if AST check is sound |
| 4. Blinding correctness | Crypto property tests | With key: recompute and compare; without key: structural checks only |
| 5. Runtime ceiling | Constant + function check | Verify each artifact's runtime_seconds ≤ 300.0 |
| 6. Artifact schema and integrity | Schema tests on hand-constructed documents | Validate actual artifacts with `validate_artifact()` + `verify_sidecar()` |
| 7. Artifact count and completeness | Test asserts 180 records per seed | Count records independently from actual artifact file |
| 8. Environment fingerprint consistency | Field presence check only | Recompute fingerprint from runtime versions |
| 9. Contract mode non-empirical | Behavioral check | Inherent in separate audit |
| 10. Artifact substitution detection | Tamper detection test | Inherent in separate audit validation |

**6 items CI cannot provide:**

- Proof of actual run's SHA
- Proof of env vars at runtime
- Proof of out-of-band key supply
- Proof that actual artifacts are untampered
- Proof of no artifacts from non-frozen window
- Independent recomputation of blinded IDs

**Lesson:** CI validates the validator. Separate audit validates the evidence. The distinction matters for independence claims and must be explicit in any verification architecture.

---

## 11. Pattern 10 — Candidate Mechanism Before Merge

**Observed:** The sprint report's roadmap began with merge steps before schema authority and contrast adjudication. The expert panel corrected this: the candidate mechanism (#1–#3) must be implemented BEFORE the final freeze candidate is created.

**Candidate mechanism triad:**

1. **Immutable candidate** — create fixed reference; manifest SHA = candidate identity
2. **Separate development HEAD** — main is development state, not experimental identity
3. **Candidate manifest** — machine-readable, versioned, cryptographically bound JSON/YAML

**Corrected sequencing:**

```
ENGINEERING HARDENING (Phase A) — BEFORE final freeze candidate
    ├── #1–#3 Candidate mechanism (MUST exist before final freeze candidate)
    ├── #4–#5 P2 candidate-bound + runtime authentication
    ├── #10–#15 P1 improvements (FLAG-02 migration, propagation checking, etc.)
    │
    ├── PR #77 as engineering vehicle INSIDE this architecture
    │   (NOT the first unconditional step)
    │
    ▼
EVIDENCE MACHINERY (Phase B) → TEST CLOSURE (Phase C) → SCIENTIFIC LOCK (Phase D)
    → INDEPENDENT VERIFICATION (Phase E) → EMPIRICAL EXPERIMENT (Phase F)
```

**Lesson:** Merging PR #77 before the candidate mechanism exists "will simply add another layer of ambiguity." The candidate mechanism is the identity anchor for the entire closure sequence and must precede the final freeze candidate.

---

## 12. Pattern 11 — Full Estimand Chain Specification

**Observed:** The sprint report discussed FFCR and primary contrast but did not specify the full estimand chain. The expert panel corrected this to require the complete chain:

```
Construct → Estimand → Endpoint → Contrast → Direction → Success criterion
    → Falsification criterion → Statistical unit → Multiplicity treatment
```

**Status from Agent #2:**

- Construct (FFCR — execution robustness, NOT efficacy claim) ✅ Specified
- Estimand (E[FFCR(T) − FFCR(R)], paired differences) ✅ Specified
- Primary endpoint (FFCR per-condition per-seed, 180 trials/seed) ✅ Specified
- Primary contrast (3 candidates: dgaf vs null, PDMAL vs Ring, combined) ✗ NONE SELECTED
- Direction ✗ NOT YET DECLARED per candidate
- Success criterion ✗ NOT YET DECLARED
- Falsification criterion ✗ NOT YET DECLARED
- Statistical unit (one seed) ✅ Confirmed
- Multiplicity treatment ✗ NOT YET CLOSED

**Lesson:** Scientific target specification requires the full chain, not just construct + contrast. Missing chain elements are scientific-target choices that block protocol freeze and authorization. They cannot be resolved by engineering changes.

---

## 13. Pattern 12 — N=0 Epistemic Discipline

**Observed throughout:** Every artifact, every correction, every assessment carries the explicit N=0 qualifier. No empirical claims are made. Pilot authorization is NOT GRANTED. The corrected apparatus is PRE-FREEZE.

**Discipline applied:**

- Every "Does NOT establish" caveat attached to agent findings
- Every predicate score includes the evidence basis and what remains unverified
- Expert corrections validated against source files, not accepted on authority
- Unsupported claims from the sprint report explicitly flagged (3 items)
- Missing content items identified (5 items) rather than silently omitted

**Epistemic ladder reference:** DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED. Project-local approval labels do not automatically upgrade claims on this ladder.

---

## 14. Summary — Patterns for the Registry

| # | Pattern name | Category | When to apply |
|---|---|---|---|
| 1 | Subagent path resolution | Operational | Multi-agent sessions with potentially ambiguous directory structures |
| 2 | JSON output before max-iterations | Operational | Agent tasks involving research + structured output |
| 3 | Expert-panel correction integration | Governance | Any session receiving structured expert critique |
| 4 | Surgical subagent dispatch | Orchestration | Complex assessments spanning multiple independent dimensions |
| 5 | 9-predicate model abstraction | Governance | Closure assessments with 30+ individual checks |
| 6 | Different authorities for different facts | Governance | Any closure model where status could be mistaken for evidence |
| 7 | Historical freeze retention as evidence | Provenance | Superseded states that must be preserved, not overwritten |
| 8 | Temporal/provenance documentation preservation | Documentation | Document consolidation proposals |
| 9 | CI vs separate audit distinction | Verification | Independent verification architecture design |
| 10 | Candidate mechanism before merge | Sequencing | Freeze candidate creation sequencing |
| 11 | Full estimand chain specification | Scientific | Scientific target specification |
| 12 | N=0 epistemic discipline | Epistemic | All pre-authorization, pre-freeze sessions |

**Cross-references:** `docs/DGAF_PDMAL_EXECUTION_READINESS_REFINED_2026-08-21.md` (corrected assessment), `docs/experiment/` (agent JSON artifacts), `registry/PATTERN_REGISTRY_v2.md` (master pattern registry), `BOOTSTRAP.md` (evidence ladder, non-negotiables).

---

*Logged 2026-08-21. N=0 throughout. Pilot authorization NOT GRANTED.*
