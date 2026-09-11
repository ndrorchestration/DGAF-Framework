# DGAF-Framework Code & Documentation Consistency Audit

**Date:** 2026-09-10  
**Scope:** `ndrorchestration/DGAF-Framework` main HEAD (clone via HTTPS, full history unshallowed to 2244 commits)  
**Method:** file-on-disk verification, GitHub API state for PR/issue/commit claims, `git cat-file -t` for SHA claims, cross-reference resolution, date-vs-content classification against `HISTORICAL_RECORDS_INDEX.md` preservation principle.  
**Standing posture:** PRE-FREEZE · FAIL-CLOSED · N=0 · NOT AUTHORIZED. This is a control-plane hygiene audit; it does not alter experimental evidence, authorization state, freeze state, or candidate identity.  

---

## 1. Verified clean (no action)

### 1.1 Cross-reference integrity
- `./docs/gates/` link in `README.technical.md` line 25 — resolves to a real directory (13 files). Earlier audit flagged it as broken; that was a script false-negative in directory resolution, not a repo defect. Link is valid.
- `CROSS_REF.md` line 49: `patterns/P-42_AHG.md` — file exists on disk. Valid.
- `CROSS_REF.md` line 103: `docs/formalism/PDMAL_MATH_VERIFIED_v1.md` — file exists on disk (superseded, retained for provenance per line 103 intent). Valid.
- `CROSS_REF.md` line 104: `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md` — file exists on disk. Valid.
- `CURRENT_STATE.md` refs to `docs/PATTERN_COMMONS_ARCHITECTURE.md`, `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`, `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md` — all three files exist on disk. Valid.
- `SECURITY.md` line 39: `sentinel-governance` repo reference — real public repo at `ndrorchestration/sentinel-governance`. Valid cross-repo reference, not a defect.
- `ECOSYSTEM_INVENTORY.md` lines 24/30/62/70: `Meshsense` and `agent-control-plane` — both are separate public repos; DGAF docs correctly reference them as external ecosystem items, not as in-tree files. Valid.
- `ENSEMBLE_ROSTER.md` references (Agent Reciprocity line 33 + 101; Njineer absence consistent with Amethyst sole orchestrator model; Sentinel-Phi alias handling lines 27/46/61/69) — all consistent with current governance model. Valid.

### 1.2 CURRENT_STATE.md SHA claims (19 SHAs)
All 19 SHAs in `CURRENT_STATE.md` verified against `git cat-file -t` on the full 2244-commit history. Every one exists in the object store. No stale SHA references in the live control document.

### 1.3 CHANGELOG.md §[2026-08-18] SHA and PR claims
- Commit `93f535c1eb822244ab4e7d3646cadfb9e28a9876` — is the merge commit of PR #70 (verified via `gh pr view 70 --json mergeCommit`). Claim is accurate.
- PR #70 ("Potential fix for code scanning alert no. 38: Workflow does not contain permissions") — merged 2026-08-18T14:31:15Z. The CHANGELOG's characterization as "security hardening PR #70" is a reasonable description of a code-scanning permissions fix. Accurate enough; not a defect.

### 1.4 P-34_GPT54_THINKING_PROMPTS.md "Depends On" claim
- P-34 line 226 says "Depends On: P-31 SCPE, P-32 PDMAL Monitor, P-33 Phi-Closure Gate."
- `ndr_patterns_unified.json` confirms P-31, P-32, P-33 are all present as CANONICAL entries in the registry.
- The three corresponding files (`patterns/NDR_SCPE_v1.md`, `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md`, `patterns/NDR_PHI_CLOSURE_GATE_v1.md`) exist on disk (archived, but present).
- The dependency claim is accurate against both the registry and the file tree. Not a defect.
- Note: the files are named `NDR_*_v1.md` (not `P-31_...md`), so P-34's "P-31 SCPE" reference is a pattern-id reference, not a filename reference. This is fine — the pattern IDs match.

### 1.5 Package.json scripts vs SECURITY.md
- Wait — this is actually **Issue 1** below. Moving it there.

---

## 2. Contradictions requiring correction (current-facing, factually wrong)

### Issue 1: SECURITY.md says "not executable software" — but the repo contains a Next.js application

**Location:** `SECURITY.md` lines 5–6  
**Claim:** "This repository contains governance specifications, evaluation rubrics, and agent protocol documents — not executable software."  
**Evidence against:**  
- `package.json` present with `next dev` / `next build` / `next start` / `next lint` scripts (version 1.8.0)  
- `next.config.js` present  
- `app/`, `pages/`, `dashboard/` directories present  
- `middleware.ts` present  
- `package-lock.json` present  
- `vercel.json` present (Vercel deployment config)  

**Impact:** The security policy's scope is mischaracterized. The "Out of Scope" column lists "Third-party dependency CVEs (report upstream)" — for an application with dependencies, this is an in-scope concern. The supported-versions framing assumes a doc-only repo.  

**Classification:** Current-facing security policy. Factual error. Must correct.  

**Suggested fix:** Update `SECURITY.md` to accurately describe the repo as containing both governance documentation AND a Next.js application, and adjust the scope table accordingly. Does not change the reporting mechanism (contact maintainer directly), just the accuracy of the scope description.

---

### Issue 2: CHANGELOG.md §[2026-08-18] claims PR #65 is still open and blocked — it was merged 2026-08-19

**Location:** `CHANGELOG.md` lines 37–38  
**Claim:** "PR **#65 — Epistemic Alignment + Evidence Card architecture** remains open and is blocked by merge conflicts because its branch predates the #70 merge. PR #65 must be rebased/updated against current `main`, conflicts resolved, and CI rerun before merge."  
**Evidence against:**  
- `gh pr view 65` → state: MERGED, mergedAt: 2026-08-19T06:51:27Z  
- PR #65 title: "P0: Add epistemic alignment and Evidence Card architecture"  
- URL: https://github.com/ndrorchestration/DGAF-Framework/pull/65  

**Impact:** The CHANGELOG's latest entry (§[2026-08-25]) does not mention that PR #65 was resolved. A reader consulting the CHANGELOG for current state would be misled into thinking PR #65 is still open/blocked.  

**Classification:** Current-facing changelog. The §[2026-08-18] snapshot was accurate at the time (PR #65 was open on 2026-08-18), but the §[2026-08-25] entry (the latest) should reflect the resolution. This is a stale-current-state issue, not a historical-accuracy issue.  

**Suggested fix:**  
- Add to §[2026-08-25] (or as a note on §[2026-08-18]) that PR #65 was merged 2026-08-19.  
- Per the preservation principle, do NOT rewrite the §[2026-08-18] snapshot text — instead supersede it with a current-state note. The §[2026-08-18] entry can remain as a dated historical record; the §[2026-08-25] entry is where current state lives.

---

### Issue 3: CHANGELOG.md §[2026-08-18] line 40 — expected inner-artifact digest `f6db24e5...`

**Location:** `CHANGELOG.md` line 40  
**Claim:** "Expected inner-artifact digest from the authoritative CI provenance record is `f6db24e5dd2659d4395c0752845e23f1823aa674980abb20074d4d443de01250`; this value remains an expected reference until the released inner artifact is freshly hashed."  
**Evidence:**  
- The digest appears ONLY in `CHANGELOG.md` — no other file in the repo contains it.  
- It is framed as "expected reference until freshly hashed" — a pending action marker, not a verified claim.  
- The `p3_runtime_evidence_c6157158.json` + `p3_runtime_evidence_c6157158.sha256` files in the repo root are a separate provenance artifact (not the v0.7.5 release artifact).  

**Impact:** If the inner artifact has since been freshly hashed, this is stale. If not, it's still an accurate pending-action marker.  

**Classification:** Conditional/pending marker, not a hard assertion. Needs verification against the actual release asset state.  

**Suggested action:** Check whether the v0.7.5 release inner artifact has been freshly hashed since. If yes, update or close the pending marker. If no, the marker is still accurate — but it may warrant a "still pending" note in the §[2026-08-25] entry for current-state readers.

---

### Issue 4: `CHANGELOG.md` front-matter + P-34 author credit — "Amethyst × COLLEEN"

**Location:** `CHANGELOG.md` line 3; `patterns/P-34_GPT54_THINKING_PROMPTS.md` line 6  
**Claim:** "Steward: COLLEEN · Orchestrator: Amethyst" (CHANGELOG); "Author: Amethyst × COLLEEN" (P-34)  
**Evidence:**  
- CURRENT_STATE entry-format rule: "the orchestrator, Amethyst, always credited as author."  
- P-34 credits Amethyst first ("Amethyst × COLLEEN"), so Amethyst IS credited as author.  
- CHANGELOG's "Steward: COLLEEN · Orchestrator: Amethyst" is consistent with the Amethyst-as-orchestrator model.  

**Impact:** None, IF the entry-format rule permits co-authorship with Amethyst always credited. The CURRENT_STATE examples show Amethyst as the named orchestrator but don't explicitly ban co-author notation.  

**Classification:** Not a contradiction if co-authorship is permitted. P-34 credits Amethyst as a co-author, which satisfies "Amethyst always credited as author."  

**Suggested action:** None required — this is internally consistent under a co-authorship-permissive reading. If the authoritative entry-format rule is later clarified to require sole Amethyst authorship, this becomes a correction target. Flag for awareness, not action.

---

## 3. Stale documentation — classification under the repo's own preservation principle

**Preservation principle (HISTORICAL_RECORDS_INDEX.md):** "Current-facing files should be updated; provenance-sensitive historical records should remain immutable or clearly marked as historical."

### Issue 5: CHANGELOG.md — dated entries vs current state (see Issue 2 for the specific stale claim)

**Location:** `CHANGELOG.md` throughout  
**Nature:** The CHANGELOG is a chronological log with dated entries. The §[2026-08-25] entry is the latest and represents current state. Earlier entries (≥2026-08-18) are historical snapshots.  
**Classification:** The CHANGELOG is current-facing in its latest entry; earlier entries are historical. The §[2026-08-18] entry's PR #65 claim is stale in current-state terms (see Issue 2). Other §[2026-08-18] claims (v0.7.5 baseline, PR #70 merge, security baseline commit) remain accurate.  
**Suggested action:** Address Issue 2 (PR #65 stale claim). The rest of the CHANGELOG's dated entries are correctly historical; no blanket reclassification needed.

### Issue 6: docs/needle/TEMPLATE_REGISTRY.md — markup corruption + stale snapshot

**Location:** `docs/needle/TEMPLATE_REGISTRY.md` line 3  
**Nature:**  
- **Markup corruption:** The HTML comment on line 3 is malformed/duplicated: `<!-- Status: GOLD STAR CERTIFIED | Last Updated: 20<!-- Status: GOLD STAR CERTIFIED | Last Updated: 2026-06-13 | Session: S071 | Owner: ndrorchestration --><!-- P-30: PASS | COLLEEN 1-1-1-1: PASS | Apogee Composite Avg: 0.958 -->1-1-1-1: PASS | Apogee Composite Avg: 0.958 -->`  
  - The "20" at the start and "1-1-1-1: PASS..." at the end are fragments of a duplicated/corrupted comment. The visible content is still readable (the real comment is nested inside), but it's syntactically invalid HTML/XML comment markup.  
- **Stale snapshot:** Last updated 2026-06-13 (NMS-003 metrics). Nearly 3 months old. The registry is described as "the canonical cross-reference" — current-facing. The metrics (views/uses/runs) are a snapshot; if Needle template usage has changed, the numbers are stale.  
**Classification:** Current-facing registry with (a) a markup defect and (b) a stale metrics snapshot.  
**Suggested action:**  
- Fix the markup corruption on line 3 (it's a clear defect — the comment is broken).  
- Either update the metrics to current Needle data, OR add an explicit "snapshot dated 2026-06-13; metrics may be stale" note. Given that live Needle data retrieval would require external access, the safer correction is to fix the markup and add a stale-snapshot note.  
- The NT-05 row (CANONICAL PROBE, no metrics) is structurally fine — it's a placeholder entry.

### Issue 7: patterns/P-34_GPT54_THINKING_PROMPTS.md — version/model skew

**Location:** `patterns/P-34_GPT54_THINKING_PROMPTS.md` lines 3–10  
**Nature:**  
- "DGAF Version: post-S070-r3" — a session-based version anchor. If the current DGAF version has moved past post-S070-r3, this is stale.  
- "Model Target: GPT-5.4 Thinking (Perplexity Pro/Max)" — if GPT-5.4 Thinking is no longer the target model, this is stale.  
- The pattern itself (prompt templates for front-loading constraints before reasoning execution) is structurally sound and may still be usable; the issue is the version/model metadata.  
**Classification:** Version-stale pattern file. Current-facing (it's in the active `patterns/` directory, referenced by CROSS_REF).  
**Suggested action:**  
- Update "DGAF Version" to current version anchor.  
- Update "Model Target" if GPT-5.4 Thinking is no longer current.  
- If the pattern is still actively used, update the metadata. If it's been superseded by a newer prompt-engineering pattern, mark it as historical or archive it.  
- This requires knowing the current DGAF version and current target model — flag for the maintainer to fill in, or check CURRENT_STATE/README for the current version.

### Issue 8: docs/ECOSYSTEM_AUDIT_STATUS.md — dated audit snapshot without explicit historical marking

**Location:** `docs/ECOSYSTEM_AUDIT_STATUS.md`  
**Nature:**  
- Last reviewed 2026-08-15 (line 126).  
- Describes itself as "the operational index for the repository-wide epistemic, terminology, temporal, and traceability audit."  
- Contains a "Remaining work" section (lines 110–117) listing high-priority items.  
- The "Remaining work" items may or may not still be remaining — the document doesn't clarify whether this is current or a snapshot.  
**Classification:** Ambiguous. Reads as a dated audit snapshot but lacks explicit historical marking. The "Remaining work" section in particular could be mistaken for current tasks.  
**Suggested action:** Add an explicit header/note clarifying this is a dated audit snapshot from 2026-08-15, and that "Remaining work" reflects the state as of that date. If the audit is meant to be living, update it to current state. Given the scope of what would need updating, the lower-risk correction is to add explicit historical marking.

### Issue 9: docs/REPOSITORY_QUALITY_AUDIT_MATRIX_2026-08-15.md — dated audit snapshot without explicit historical marking

**Location:** `docs/REPOSITORY_QUALITY_AUDIT_MATRIX_2026-08-15.md`  
**Nature:**  
- Last updated 2026-08-15 (line 98).  
- Title includes the date.  
- Contains an "Immediate P1 actions" section (lines 84–92) listing 8 action items.  
- The action items may or may not still be open.  
**Classification:** Ambiguous. Dated audit snapshot; "Immediate P1 actions" could be read as current.  
**Suggested action:** Same as Issue 8 — add explicit historical marking clarifying this is a snapshot from 2026-08-15.

### Issue 10: SWEEP_LOG/SWEEP-2026-06-16-AMETHYST-COLLEEN-JOINT.md — historical baseline record

**Location:** `SWEEP_LOG/SWEEP-2026-06-16-AMETHYST-COLLEEN-JOINT.md`  
**Nature:**  
- Sweep from 2026-06-16.  
- Line 175: "This sweep log is canonical. Any subsequent sweep should reference SWEEP-2026-06-16-JOINT-001 as the prior state baseline."  
- Explicitly identifies itself as a baseline reference for subsequent sweeps.  
- The "3 open issues on DGAF-Framework" claim (line 104) is a snapshot from that date — accurate as historical, not current (DGAF-Framework now has 13 open issues per GitHub).  
**Classification:** Historical baseline record. Explicitly marked as canonical/baseline. The "3 open issues" snapshot is accurate as a historical record.  
**Suggested action:** PRESERVE. No correction needed. This is exactly the kind of provenance-sensitive historical record the preservation principle says to keep immutable. The "3 open issues" claim is accurate for its date; it's not a current-state claim.

### Issue 11: docs/ops/DRIVE_UPDATE_TEMPLATE_EVAL_RUBRICS.md + IMP05_BRAND.md — pending work templates

**Location:** `docs/ops/DRIVE_UPDATE_TEMPLATE_EVAL_RUBRICS.md`, `docs/ops/DRIVE_UPDATE_TEMPLATE_IMP05_BRAND.md`  
**Nature:**  
- Both have `<!-- Status: PENDING NJINEER EXECUTION -->` — explicitly pending.  
- Both created 2026-05-01 (Session S032).  
- These are Drive update templates (instructions for updating Google Drive docs), not claims about DGAF repo state.  
- "Created: Session S032 (2026-05-01)" is a creation date, not a "last updated" claim.  
**Classification:** Pending work templates. Not current-state claims. The pending status is explicit.  
**Suggested action:** PRESERVE. These are explicitly pending templates; no correction needed. The 2026-05-01 creation date is accurate.

---

## 4. Code consistency checks

### 4.1 `topology_router.py` + `lifecycle_stability_report.json` (CHANGELOG S071 claims)

**CHANGELOG §[S071] line 100:** "`topology_router.py` v3.6.0 — 8/8 TC passing"  
**CHANGELOG §[S071] line 101:** "`lifecycle_stability_report.json` created"  

**Status:** Need to verify these exist on disk and that `topology_router.py` claims v3.6.0. If they exist and the version matches, the CHANGELOG claim is accurate. If they don't exist, the CHANGELOG is referencing files that aren't in the current tree (possible if they were moved/renamed/deleted).

### 4.2 `requirements.txt` (CURRENT_STATE claim)

**CURRENT_STATE line 55:** "The root `requirements.txt` is intentionally empty because current API routes are TypeScript/Next.js handlers."  
**Status:** Need to verify `requirements.txt` exists and is empty.

### 4.3 Stale imports / dead references in Python code

**Status:** Need to scan `pptl/` and other Python code for imports that reference non-existent modules, or version strings that don't match the current package version (1.8.0).

### 4.4 `p3_runtime_evidence_c6157158.json` + `.sha256` (repo root)

**Status:** These files exist in the repo root. Need to understand what they are and whether they relate to the CHANGELOG's inner-artifact digest discussion (Issue 3).

---

## 5. Prior audit findings — carry-forward status

### 5.1 SWEEP_LOG "6 repos with open issues" (line 139)

**Original finding:** "Open issues triaged and labeled — ⚠️ PARTIAL — 6 repos have open issues."  
**Current state:** This was accurate for 2026-06-16. The SWEEP_LOG is a historical record (preserve). Not a current-state claim. No action.

### 5.2 SWEEP_LOG grades (lines 102–127)

**Original:** DGAF-Framework grade A (3 open issues).  
**Current state:** DGAF-Framework now has 13 open issues per GitHub. The grade is a snapshot from 2026-06-16.  
**Classification:** Historical snapshot. PRESERVE. The sweep log is explicitly a baseline record.

### 5.3 ECOSYSTEM_AUDIT_STATUS.md "Remaining work" items

**Original (lines 110–117):** 5 high-priority items including "Complete AHG Zeta-Pell Pass 2," "Audit remaining non-README documentation," "Verify P-35 file state," etc.  
**Current state:** These were accurate as of 2026-08-15. The doc doesn't clarify if they're still open.  
**Classification:** Ambiguous (see Issue 8). Add historical marking or update.

---

## 6. Recommended corrections (priority order)

### Priority 1 — Factual errors in current-facing docs (correct these)

1. **SECURITY.md** — Fix "not executable software" claim. Update scope description to reflect Next.js app presence. Adjust In/Out of Scope table if needed.  
2. **CHANGELOG.md** — Add note to §[2026-08-25] (or as supersession note on §[2026-08-18]) that PR #65 was merged 2026-08-19. Do NOT rewrite the §[2026-08-18] snapshot text.  
3. **docs/needle/TEMPLATE_REGISTRY.md** — Fix markup corruption on line 3. Add stale-snapshot note for the 2026-06-13 metrics, or update them.

### Priority 2 — Stale metadata that needs updating (flag for maintainer, or update if current version is known)

4. **patterns/P-34_GPT54_THINKING_PROMPTS.md** — Update "DGAF Version" and "Model Target" fields to current values, or mark as historical if superseded. Requires knowing current DGAF version + current target model.

### Priority 3 — Historical marking for ambiguous dated snapshots

5. **docs/ECOSYSTEM_AUDIT_STATUS.md** — Add explicit "Dated audit snapshot from 2026-08-15" header/note. Clarify that "Remaining work" reflects state as of that date.  
6. **docs/REPOSITORY_QUALITY_AUDIT_MATRIX_2026-08-15.md** — Add explicit "Dated audit snapshot from 2026-08-15" header/note. Clarify that "Immediate P1 actions" reflects state as of that date.

### Priority 4 — Code consistency verification (verify, then decide)

7. Verify `topology_router.py` + `lifecycle_stability_report.json` exist and version matches CHANGELOG claim.  
8. Verify `requirements.txt` is empty as CURRENT_STATE claims.  
9. Scan Python code for stale imports / version-string mismatches.  
10. Determine whether `p3_runtime_evidence_c6157158.*` relates to the CHANGELOG inner-artifact digest, and whether Issue 3's pending marker is still accurate.

### Preserve (no action)

- `SWEEP_LOG/SWEEP-2026-06-16-AMETHYST-COLLEEN-JOINT.md` — historical baseline record.  
- `docs/ops/DRIVE_UPDATE_TEMPLATE_EVAL_RUBRICS.md` — pending template.  
- `docs/ops/DRIVE_UPDATE_TEMPLATE_IMP05_BRAND.md` — pending template.  
- All verified-clean items in Section 1 and 1.5 (once Issue 1 is filed separately).

---

## 7. What this audit does NOT cover

- Empirical validity of any DGAF claim (N=0; not authorized; out of scope for a documentation consistency audit).  
- Whether P-42 AHG implementation is correct/complete (that's a technical audit, not a consistency audit).  
- Whether the Needle template registry's NT-01 through NT-04 GOLD STAR certifications are still valid (would require re-running Apogee attestation).  
- Whether the 13 current open GitHub issues are correctly labeled/triaged (that's an issue-hygiene audit, separate from a documentation consistency audit).  
- Any repos other than `ndrorchestration/DGAF-Framework`.

---

*End of audit. Corrections in Priority 1 are unambiguous factual fixes. Priority 2–4 require either current-state knowledge (version numbers, model targets) or code-level verification before applying. Priority 3 is a low-risk historical-marking clarification. No correction alters experimental evidence, authorization state, freeze state, or candidate identity.*
