# Synthesis Briefing — DGAF/PDMAL Completion Journey

**Compiled:** 2026-08-21  
**Sources:** 12 source documents synthesized  
**Status:** BRIEFING COMPLETE — NOT YET SYNTHESIZED INTO FINAL REPORT

---

## Source Inventory

### What Exists

| Source | Location | Lines/Size | What It Covers |
|---|---|---|---|
| Sprint fragment (`.broken`) | `/OneDrive/Desktop/DGAF_3NODE_META_ORCHESTRATION_SPRINT_2026-08-21.md.broken` | 154 lines | Sections 10.5-13: GitHub verification, sprint finding mapping, verification basis, corrected user claims, meta-orchestration assessment, conclusion. Missing sections 1-10.4. |
| Corrected report | `docs/DGAF_PDMAL_EXECUTION_READINESS_REFINED_2026-08-21.md` | 409 lines, 36,758 bytes | Full corrected assessment. 8 expert corrections applied. 0/9 scoring. Full estimand chain. 6-phase 25-point plan. N=0 throughout. Supersedes sprint fragment. |
| Expert review JSON | `/tmp/pri_report_expert_review.json` (or `AppData/Local/Temp/`) | 236 lines, 40,235 bytes | 8 corrections (C1-C8). 3 unsupported claims flagged. 5 missing content items. Overall: ADOPT WITH CORRECTIONS. |
| schema_resolution.json | `/tmp/schema_resolution.json` | ~6,388 chars | Canonical module analysis. artifact_schema.py (PRE-FREEZE) vs pilot_artifact_schema.py (FROZEN). 5 recommendations. N=0. |
| estimand_chain.json | `/tmp/estimand_chain.json` | ~10,041 chars | Construct (FFCR), estimand, endpoint, 4 contrast candidates (none selected), statistical unit, multiplicity NOT CLOSED. 12 items missing. N=0. |
| pr77_doc_briefing.json | `/tmp/pr77_doc_briefing.json` | ~2,189+ chars | 5 new docs + 2 modified. 9 IMPLEMENTED + 9 OPEN gates. Most honest doc: PRE_AUTHORIZATION_RECORD. 13 sprint findings mapped. N=0. |
| independent_verification_design.json | `/tmp/independent_verification_design.json` | ~5,000+ chars | 10 verification layers. 10 CI + 8 separate audit checks. Evidence chain. 6 items CI cannot provide. 8-step freeze verification. N=0. |
| experimental_design_integrity.json | `/tmp/experimental_design_integrity.json` | ~3,000+ chars | 6 design dimensions covered by existing evidence. Fold into P5+P7. No 10th predicate. Stopping rule satisfied. N=0. |
| CURRENT_STATE.md (local HEAD) | `docs/CURRENT_STATE.md` | 109 lines | Protocol state: PRE-FREEZE. Executor state: OPEN. Empirical: 0. |
| FREEZE_MANIFEST.md (local HEAD) | `docs/experiment/FREEZE_MANIFEST.md` | 234 lines | Status: FROZEN (frontmatter). Body: PRE-FREEZE. Primary contrast: OPEN. N=0. Auth: NOT GRANTED. |
| PRIMARY_CONTRAST_ADJUDICATION.md | `docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` | 37 lines | Status: OPEN. State: PRE-FREEZE. 4 contrast candidates. |
| PDM_CURRENT_CONTROL_STATE.md (local HEAD) | `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | 79 lines | Protocol freeze: BLOCKED. Pilot auth: NOT GRANTED. Empirical: 0. |
| PDM_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md (local HEAD) | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` | 76 lines | Status: APPROVED PENDING PANEL RECORD. State: PRE-FREEZE AMENDMENT. |
| PDM_EXPERIMENT_PROTOCOL.md (local HEAD) | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | 86 lines | Status: ACTIVE. State: PRE-FREEZE. FFCR definition. Topology matrix. |
| Baseline snapshot | `/tmp/baseline_snapshot.json` | 219 lines | Local HEAD + PR #77 local + GitHub live state. SHA discrepancy documented. |

### What's Missing

- Full sprint report (sections 1-10.4) — only `.broken` fragment (sections 10.5-13) exists
- `PDMAL_STATISTICAL_ANALYSIS_PLAN.md` — not found at any path
- `PDMAL_PIPELINE_SPEC.md` — not found at any path
|- `PDMAL_ANALYSIS_PLAN_CERTIFICATE.md` — not found at any path
|- `pdmal-freeze-preparation.yml` — EXISTS at PR #77 (blob `4b6a1e45`, Python 3.12.0, installs `requirements-full-lock.txt`, runs `test_security_controls.py` + `test_artifact_schema.py`); NOT executed; same false-green risks as `pdmal-preauth-security.yml`. NOTE: corrected from earlier "NOT FOUND" claim after git ls-tree verification.
|- `durable_retention.py` at PR #77 — not found (only on disk at local HEAD)
- Hermes/expert-agent reports — not present in repository (external evidence boundary)

---

## Claim-to-Source Mapping

### Corrected Report Claims — Verified Against Sources

| Claim | Source | Status |
|---|---|---|
| HEAD = 3510b86889cd341f7a7cf9ab684fd37b2fafd758 | `git rev-parse HEAD` | ✅ CONFIRMED |
| PR #77 local head = 4983f44a | `git ls-tree pr-77-head` | ✅ CONFIRMED |
| PR #77 GitHub head = b25a914c | GitHub API | ✅ CONFIRMED |
| artifact_schema.py blob = 41a9048 at HEAD | `git ls-tree HEAD` | ✅ CONFIRMED |
| artifact_schema.py blob = 41a9048 at PR #77 | `git ls-tree 4983f44a` | ✅ CONFIRMED (unchanged) |
| pilot_artifact_schema.py blob = 2918a9d at PR #77 | `git ls-tree 4983f44a` | ✅ CONFIRMED |
| run_pilot.py blob = 184f4aa7 at PR #77 | `git ls-tree 4983f44a` | ✅ CONFIRMED |
| test_security_controls.py blob = ddc59571 at PR #77 | `git ls-tree 4983f44a` | ✅ CONFIRMED (actual: ddc59571, not injected 5edd3a6c) |
| pdmal-preauth-security.yml blob = 9cff92a5 at PR #77 | `git ls-tree 4983f44a` | ✅ CONFIRMED (actual: 9cff92a5, not injected 4ffe0d53) |
| run_pilot.py does NOT import schema modules | `grep` on `run_pilot.py` | ✅ CONFIRMED (grep: 0) |
| PRE_AUTHORIZATION_RECORD: "verified: NO" | `git show 4983f44a:.../PRE_AUTHORIZATION...` | ✅ CONFIRMED |
| PRIMARY_CONTRAST_ADJUDICATION: status=OPEN, state=PRE-FREEZE | file read | ✅ CONFIRMED |
| PDM_PROTOCOL_MATRIX_AMENDMENT: status=APPROVED PENDING PANEL RECORD | file read | ✅ CONFIRMED |
| PDM_ANALYSIS_PLAN_CERTIFICATE.md: NOT FOUND | `git ls-tree 4983f44a` | ✅ CONFIRMED |
| durable_retention.py: NOT at PR #77 | `git ls-tree 4983f44a` | ✅ CONFIRMED (only on disk at local HEAD) |
|| pdmal-freeze-preparation.yml: EXISTS at PR #77 (blob `4b6a1e45`) | `git ls-tree 4983f44a` | ✅ CONFIRMED |
| PDM_CURRENT_CONTROL_STATE: protocol_freeze=BLOCKED, pilot_auth=NOT GRANTED, empirical=0 | file read | ✅ CONFIRMED |
| CURRENT_STATE: protocol_state=PRE-FREEZE, executor_state=OPEN, empirical=0 | file read | ✅ CONFIRMED |
| FREEZE_MANIFEST: primary_contrast=OPEN, N=0, auth=NOT GRANTED | file read | ✅ CONFIRMED |
| PDM_EXPERIMENT_PROTOCOL: 86 lines, status=ACTIVE, state=PRE-FREEZE | file read | ✅ CONFIRMED |
| Sprint fragment: "I cannot verify that PR #77's code changes functionally close each finding" | `.broken` line 53 | ✅ CONFIRMED |
| PDMAL_CURRENT_CONTROL_STATE: executor_state=OPEN/IMPLEMENTED | file read (line 18) | ✅ CONFIRMED |

### Discrepancies Between Injected Values and Actual Git State

| Injected Value | Actual Value | Significance |
||---|---|---|
|| test_security_controls.py blob: ddc59571 | ddc59571 | MATCH — blob SHA correct. |
|| pdmal-preauth-security.yml blob: 9cff92a5 | 9cff92a5 | MATCH — blob SHA correct. |
|| durable_retention.py at PR #77: NOT FOUND | NOT FOUND at PR #77 | MATCH — file NOT at PR #77 (only on disk at local HEAD). Corrected from earlier "present" claim. |
|| pdmal-freeze-preparation.yml at PR #77: EXISTS (blob 4b6a1e45) | EXISTS at PR #77 | MATCH — corrected from earlier "NOT FOUND" claim. See source inventory note. |

These discrepancies do NOT affect the corrected report's core claims (which used actual git ls-tree values for the key blobs). They affect only the injected content that agents would have used.

---

## Consistency Check

### Do All Sources Agree on N=0, NOT GRANTED, PRE-FREEZE, OPEN Primary Contrast?

**YES.** Every source document consistently states:

| Invariant | Sources |
|---|---|
| N = 0 | FREEZE_MANIFEST.md (line 234), PRE_AUTHORIZATION_RECORD (line: "Empirical N: 0"), PDM_CURRENT_CONTROL_STATE.md (gate board: "Empirical data: 0"), CURRENT_STATE.md (gate board: "Empirical data: 0"), estimand_chain.json ("N=0 throughout"), corrected report (throughout) |
| Pilot authorization NOT GRANTED | FREEZE_MANIFEST.md (line 20, 210), PDM_CURRENT_CONTROL_STATE.md (gate board), PRE_AUTHORIZATION_RECORD ("Pilot authorized: NO"), corrected report (throughout) |
| Protocol PRE-FREEZE | CURRENT_STATE.md (line 33), FREEZE_MANIFEST.md (body text), PRIMARY_CONTRAST_ADJUDICATION.md (frontmatter), PDM_CURRENT_CONTROL_STATE.md (status) |
| Primary contrast OPEN | FREEZE_MANIFEST.md (line 39, 207), PRIMARY_CONTRAST_ADJUDICATION.md (frontmatter), estimand_chain.json (4 candidates, none selected) |

### Any Source Disagreement?

**No material disagreement.** The only apparent tension is:

- **DOCUMENTATION_GAP_AUDIT.md (PR #77)** claims "Protocol freeze CLOSED" — but this refers to the historical freeze for the old runner, not the corrected apparatus. The FREEZE_MANIFEST_RECONCILIATION.md clarifies that the historical freeze is retained as evidence and the corrected runner needs a NEW freeze. When read correctly, there is no contradiction.

- **Sprint fragment (section 13)** says "PR #77 merges. Post-merge verification confirms functional closure." — but the sprint itself qualifies this with "I cannot verify that PR #77's code changes functionally close each finding." The sprint's own words limit the claim.

---

## Unresolved Tensions

### 1. Local vs GitHub PR #77 divergence

Local `pr-77-head` = `4983f44a`. GitHub PR #77 head = `b25a914c`. The GitHub head has moved forward with additional commits not yet fetched locally. This means:
- The corrected report's claims about PR #77 contents are based on `4983f44a`, which may be stale relative to GitHub.
- Before any Gate 3 work, the repo must be synced (`git fetch origin pull/77/head`).
- The baseline snapshot documents this discrepancy.

### 2. Sprint fragment incompleteness

The only available sprint report is the `.broken` fragment (sections 10.5-13, 154 lines). Sections 1-10.4 are missing. This means:
- The sprint's findings #1-13 are documented in the fragment's section 11 (finding mapping), but the full context of each finding (sections 1-10.4) is not available.
- The corrected report's claim about what the sprint found is based on the fragment + the 5 agent JSONs + the expert review, not on the full sprint report.

### 3. Injected content staleness

The injected blob SHAs for test_security_controls.py and pdmal-preauth-security.yml were stale. The actual values differ. This means:
- Any agent using the injected values for those SHAs would produce incorrect output.
- The corrected report's claims about those blobs are based on actual git ls-tree, which is correct.

### 4. What's "in PR #77" vs "on disk" vs "at HEAD"

Several files have confusing provenance:
- `durable_retention.py`: on disk at local HEAD, committed at local HEAD, but NOT at PR #77.
- `PDMAL_EXPERIMENT_PROTOCOL.md`: at PR #77 (blob `2650e4362432a60e750bdad2da83c89cd6c81811`) AND at local HEAD (blob `f9cca61f6c5158c99af6822991866583712e9caa`).
- `PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md`: at PR #77 (blob `a686366c56e61f873908e95fd2c05bfe42bac31e`) AND at local HEAD (blob `a686366c56e61f873908e95fd2c05bfe42bac31e`).
- `pdmal-freeze-preparation.yml`: EXISTS at PR #77 (blob `4b6a1e45616a7794375700f4881a8997c71f2894`), NOT at local HEAD.

The corrected report handles these correctly by specifying which files are at which location.

### 5. Expert panel verdict vs. corrected report scoring

The expert panel scored the sprint report 9/10 and said the corrections are sound. The corrected report scores 0/9 predicates as unambiguously closed. These are NOT contradictory:
- The expert panel assessed the sprint report's quality and the corrections' soundness.
- The corrected report assesses the current verification state (0/9 closed).
- A well-written document can correctly conclude that nothing is verified yet.

---

## Recommendations for What to Verify Before Proceeding

### High Priority

1. **Sync the repo:** `git fetch origin pull/77/head` to get `b25a914c` locally. Verify that the additional commits between `4983f44a` and `b25a914c` don't change the candidate materially.

2. **Verify the 6 adversarial tests:** Read `test_security_controls.py` (blob `ddc59571`) and enumerate the exact tests. Verify they cover the claimed surfaces.

3. **Verify SHA computation consistency:** Test whether `run_pilot.py`'s `_compute_artifact_sha256` produces the same result as `pilot_artifact_schema.py`'s `canonical_json_bytes()`. This is a critical gap.

4. **Execute the CI workflow:** Trigger `pdmal-preauth-security.yml` against the candidate SHA. Record the run ID, SHA, and result.

### Medium Priority

5. **Read the full sprint report if it can be located:** The `.broken` fragment is missing sections 1-10.4. If the full report exists elsewhere, read it.

6. **Verify the 5 agent JSONs are consistent with the corrected report:** Cross-check each agent's claims against the corrected report and source files.

7. **Verify the topology component SHAs:** The freeze manifest appendix lists SHAs for topology files at `915e454e`. Verify these against `git ls-tree 915e454e`.

### Low Priority

8. **Locate the full sprint report:** Search all drives for `DGAF_3NODE_META_ORCHESTRATION_SPRINT_2026-08-21.md` (not the `.broken` fragment).

9. **Verify the lockfile SHA:** Confirm `requirements-full-lock.txt` blob `3ac4bd28` matches the freeze manifest's recorded SHA.

10. **Verify the environment fingerprint derivation:** Check that the runner's environment fingerprint computation matches what the verifier expects.

---

## N=0 Invariant

**N = 0 throughout. Pilot authorization NOT GRANTED. Protocol PRE-FREEZE.**

This briefing synthesizes available sources. It does NOT constitute verification of any claim beyond what the source files directly support. All claims are traceable to source files or flagged as unverified.
