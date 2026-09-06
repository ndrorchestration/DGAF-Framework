# DGAF Master Rubric Registry — Repository Inventory & Reconciliation
**Generated:** 2026-09-04  
**Source of truth for file verification:** this repository's disk inventory (live scan)  
**Notion overlay:** [MASTER RUBRIC REGISTRY & AUDIT — 2026-09-04](https://app.notion.com/p/3d1f5bad238b812d8e66c7d7f0747cde) (OPEN audit — lower bound, not claimed exhaustive)  
**Purpose:** Reconcile the Notion registry's "17 confirmed" provisional count against the live filesystem, correct the table, flag real gaps, and operationalize the registry as the governing index for the agent cohort measurement.

---

## 1. Live filesystem scan — QA_RUBRIC / rubric-bearing files (confirmed on disk)

### 1.1 Agent QA_RUBRIC files (25 files)

| Agent folder | QA_RUBRIC file | Present |
|---|---|---|
| `docs/agents/amethyst/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/apogee/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/clarion/` | `CLARION_QA_RUBRIC.md` | ✅ |
| `docs/agents/colleen/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/continuum/` | **(no QA_RUBRIC file)** | ❌ GAP |
| `docs/agents/cadence/` | **(no QA_RUBRIC file)** | ❌ GAP |
| `docs/agents/demi-joule/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/echolette/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/equilibrium/` | **(folder exists; no QA_RUBRIC file)** | ❌ GAP (folder present, file missing) |
| `docs/agents/herald/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/ionia/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/keystone/` | `KEYSTONE_QA_RUBRIC.md` | ✅ |
| `docs/agents/lyra/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/momentum/` | `MOMENTUM_QA_RUBRIC.md` | ✅ |
| `docs/agents/navigator/` | `NAVIGATOR_QA_RUBRIC.md` | ✅ |
| `docs/agents/nova/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/oracle/` | `ORACLE_QA_RUBRIC.md` | ✅ |
| `docs/agents/paragon/` | `PARAGON_QA_RUBRIC.md` | ✅ |
| `docs/agents/perigee/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/prof-prodigy/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/reciprocity/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/reson/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/sentinel/` | `QA_RUBRIC.md` + `SENTINEL_PHI_QA_RUBRIC.md` | ✅ (×2) |
| `docs/agents/synergy/` | **(folder exists; no QA_RUBRIC file)** | ❌ GAP (folder present, file missing) |
| `docs/agents/the-actualizer/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/the-auditor/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/the-librarian/` | `QA_RUBRIC.md` | ✅ |
| `docs/agents/vanguard/` | `VANGUARD_QA_RUBRIC.md` | ✅ |
| `docs/agents/zenith/` | `QA_RUBRIC.md` | ✅ |

**Agent QA_RUBRIC count:** 25 files present across 23 agent folders (sentinel has 2).  
**Agent folders with NO QA_RUBRIC file on disk:** `continuum`, `cadence`, `equilibrium`, `synergy` — 4 folders present without a QA_RUBRIC file.  
**Agent folders confirmed present (with or without rubric):** 23 folders total.

### 1.2 Non-agent rubric-bearing documents (5 files)

| Path | Type |
|---|---|
| `docs/qa/QA_RUBRIC.md` | Core framework rubric |
| `docs/DGAF_QA_ASSERTION_REPORT.md` | Assertion report (rubric-bearing) |
| `docs/governance/PUBLIC_SURFACE_QA_STANDARD.md` | Public-surface QA standard |
| `docs/ops/DRIVE_UPDATE_TEMPLATE_EVAL_RUBRICS.md` | Eval rubric template (ops) |
| `docs/STRUCT_QA_001_GAP3_EVIDENCE.md` | Structural QA evidence doc (rubric-bearing) |

---

## 2. Reconciliation against the Notion registry's "17 confirmed"

### 2.1 What the discrepancy is

The Notion registry's current table records **R-001 through R-017** as "Confirmed" — 17 rubric documents. The live filesystem scan confirms a **higher count of present rubric files** (25 agent QA_RUBRIC files + 5 non-agent rubric-bearing docs = 30 rubric-bearing files total, 25 of which are agent QA_RUBRICs).

The registry's "17 confirmed" is therefore a **provisional undercount** relative to the live filesystem, not an overcount. The most likely cause: the registry's table used a rendering artifact (`QA_[RUBRIC.md](http://RUBRIC.md)`) that may have collapsed multiple files or mis-encoded paths during the initial scan, producing a lower apparent count than what is actually present.

### 2.2 Which entries the registry should carry

The registry should carry **every QA_RUBRIC file present on disk**, not a subset. Each agent QA_RUBRIC is a distinct evaluation instrument with its own dimensions, and the registry's purpose is to be the governing index for all of them. The corrected agent-rubric count is **25 agent QA_RUBRIC files** (across 23 folders), not 16 agent rubrics.

### 2.3 The registration gap the registry flagged — corrected

The Notion registry's "New audit findings" section says:

> "Current targeted repository searches surfaced indirect evidence for **The Librarian, The Auditor, The Actualizer, and Perigee** saying a QA_RUBRIC is part of the standard six-layer inventory, but those searches did not return a dedicated rubric file for those agents. This is therefore a **verification gap**..."

**Correction:** The live filesystem scan confirms that `the-librarian/QA_RUBRIC.md`, `the-auditor/QA_RUBRIC.md`, `the-actualizer/QA_RUBRIC.md`, and `perigee/QA_RUBRIC.md` **are all present on disk**. The verification gap the registry flagged for those four agents does not exist in the current filesystem — their QA_RUBRIC files are present. The registry's gap flag for those four should be **closed as confirmed-present**.

### 2.4 The real gaps (folders present, QA_RUBRIC missing)

The actual verification gaps are different from what the registry flagged:

| Agent folder | Folder present? | QA_RUBRIC on disk? | Status |
|---|---|---|---|
| `continuum/` | ✅ | ❌ | **GAP — folder exists, no QA_RUBRIC file** |
| `cadence/` | ✅ | ❌ | **GAP — folder exists, no QA_RUBRIC file** |
| `equilibrium/` | ✅ | ❌ | **GAP — folder exists, no QA_RUBRIC file** |
| `synergy/` | ✅ | ❌ | **GAP — folder exists, no QA_RUBRIC file** |

Cadence and Continuum are the two seed agents from the current cohort (the Completion Diagnostic Quartet). Both have full six-layer specs on disk (SPEC, KB_SEED, PROTOCOL, MEMORY, INTEGRATION) but **no QA_RUBRIC file** — which is a real gap against the six-layer standard. Equilibrium and Synergy are folders that exist without a QA_RUBRIC file; their status depends on whether they are active agent seats or empty placeholder folders.

---

## 3. Six-layer completeness scan (agent folders)

The standard agent inventory is **6 layers per agent: SPEC, KB_SEED, PROTOCOL, QA_RUBRIC, INTEGRATION, MEMORY** (target: 27 agents / 162 files, per the AGENT_ECOSYSTEM_REGISTRY). The following scan checks each present agent folder for all six layers.

### 3.1 Agent folders with all 6 layers present

| Agent folder | SPEC | KB_SEED | PROTOCOL | QA_RUBRIC | INTEGRATION | MEMORY | Full 6-layer? |
|---|---|---|---|---|---|---|---|
| `amethyst/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `apogee/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `colleen/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `demi-joule/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `echolette/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `herald/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ionia/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lyra/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `nova/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `perigee/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `prof-prodigy/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `reciprocity/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `reson/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `sentinel/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `the-actualizer/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `the-auditor/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `the-librarian/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `vanguard/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `zenith/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `keystone/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `clarion/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Full 6-layer (21 agent folders):** amethyst, apogee, colleen, demi-joule, echolette, herald, ionia, lyra, nova, perigee, prof-prodigy, reciprocity, reson, sentinel, the-actualizer, the-auditor, the-librarian, vanguard, zenith, keystone, clarion.

### 3.2 Agent folders with 5 of 6 layers (QA_RUBRIC missing)

| Agent folder | SPEC | KB_SEED | PROTOCOL | QA_RUBRIC | INTEGRATION | MEMORY | Missing layer |
|---|---|---|---|---|---|---|---|
| `continuum/` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | QA_RUBRIC |
| `cadence/` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | QA_RUBRIC |

**Cadence and Continuum** are the only agent folders with 5 of 6 layers present — both missing only the QA_RUBRIC file. Both are seed agents from the current cohort. This is a targeted, real gap: two agents with complete specs, KB seeds, protocols, integrations, and memories, but no dedicated QA rubric.

### 3.3 Agent folders present but incomplete (fewer than 5 of 6 layers)

| Agent folder | Present layers | Missing layers | Interpretation |
|---|---|---|---|
| `equilibrium/` | (needs check) | — | Folder exists; layer completeness not yet scanned |
| `synergy/` | (needs check) | — | Folder exists; layer completeness not yet scanned |

Equilibrium and Synergy folders exist on disk but were not fully scanned for layer completeness in this pass. They may be active agent seats, placeholder folders, or partial seeds. Their layer inventory needs a dedicated scan.

---

## 4. Corrected registry table — agent rubrics (proposed replacement for R-002 through R-026)

The following corrects the Notion registry's R-002 through R-017 agent-rubric table with the actual filesystem inventory. Each entry carries: ID, canonical name, folder, file path, present status, and gap flag.

| ID | Agent | Folder | QA_RUBRIC file | Present | Gap flag |
|---|---|---|---|---|---|
| R-002 | Amethyst | `docs/agents/amethyst` | `QA_RUBRIC.md` | ✅ | — |
| R-003 | Apogee | `docs/agents/apogee` | `QA_RUBRIC.md` | ✅ | — |
| R-004 | Clarion | `docs/agents/clarion` | `CLARION_QA_RUBRIC.md` | ✅ | — |
| R-005 | Colleen | `docs/agents/colleen` | `QA_RUBRIC.md` | ✅ | — |
| R-006 | Continuum | `docs/agents/continuum` | **(none)** | ❌ | **GAP — folder present, no QA_RUBRIC** |
| R-007 | Cadence | `docs/agents/cadence` | **(none)** | ❌ | **GAP — folder present, no QA_RUBRIC** |
| R-008 | DemiJoule | `docs/agents/demi-joule` | `QA_RUBRIC.md` | ✅ | — |
| R-009 | Echolette | `docs/agents/echolette` | `QA_RUBRIC.md` | ✅ | — |
| R-010 | Equilibrium | `docs/agents/equilibrium` | **(none)** | ❌ | **GAP — folder present, no QA_RUBRIC (status TBD)** |
| R-011 | Herald | `docs/agents/herald` | `QA_RUBRIC.md` | ✅ | — |
| R-012 | Ionia | `docs/agents/ionia` | `QA_RUBRIC.md` | ✅ | — |
| R-013 | Keystone | `docs/agents/keystone` | `KEYSTONE_QA_RUBRIC.md` | ✅ | — |
| R-014 | Lyra | `docs/agents/lyra` | `QA_RUBRIC.md` | ✅ | — |
| R-015 | Momentum | `docs/agents/momentum` | `MOMENTUM_QA_RUBRIC.md` | ✅ | — |
| R-016 | Navigator | `docs/agents/navigator` | `NAVIGATOR_QA_RUBRIC.md` | ✅ | — |
| R-017 | Nova | `docs/agents/nova` | `QA_RUBRIC.md` | ✅ | — |
| R-018 | Oracle | `docs/agents/oracle` | `ORACLE_QA_RUBRIC.md` | ✅ | — |
| R-019 | Paragon | `docs/agents/paragon` | `PARAGON_QA_RUBRIC.md` | ✅ | — |
| R-020 | Perigee | `docs/agents/perigee` | `QA_RUBRIC.md` | ✅ | — |
| R-021 | Professor Prodigy | `docs/agents/prof-prodigy` | `QA_RUBRIC.md` | ✅ | — |
| R-022 | Reciprocity | `docs/agents/reciprocity` | `QA_RUBRIC.md` | ✅ | — |
| R-023 | Reson | `docs/agents/reson` | `QA_RUBRIC.md` | ✅ | — |
| R-024 | Sentinel | `docs/agents/sentinel` | `QA_RUBRIC.md` + `SENTINEL_PHI_QA_RUBRIC.md` | ✅ | — (×2 files) |
| R-025 | Synergy | `docs/agents/synergy` | **(none)** | ❌ | **GAP — folder present, no QA_RUBRIC (status TBD)** |
| R-026 | The Actualizer | `docs/agents/the-actualizer` | `QA_RUBRIC.md` | ✅ | — |
| R-027 | The Auditor | `docs/agents/the-auditor` | `QA_RUBRIC.md` | ✅ | — |
| R-028 | The Librarian | `docs/agents/the-librarian` | `QA_RUBRIC.md` | ✅ | — |
| R-029 | Vanguard | `docs/agents/vanguard` | `VANGUARD_QA_RUBRIC.md` | ✅ | — |
| R-030 | Zenith | `docs/agents/zenith` | `QA_RUBRIC.md` | ✅ | — |

**Corrected agent QA_RUBRIC count:** 25 files present across 23 folders (sentinel ×2).  
**Corrected verified-lower-bound agent-rubric count:** 23 confirmed-present folders, 2 confirmed-gap folders (continuum, cadence), 2 TBD folders (equilibrium, synergy).

---

## 5. Non-agent rubric-bearing documents (carry forward to registry)

| ID | Name | Path | Type | Present | Notes |
|---|---|---|---|---|---|
| R-001 | DGAF Core QA Rubric | `docs/qa/QA_RUBRIC.md` | Framework rubric | ✅ | Canonical core rubric |
| A-004 | Public-Surface QA Standard | `docs/governance/PUBLIC_SURFACE_QA_STANDARD.md` | Standard / rubric-like | ✅ | Confirmed on disk; inspect scoring semantics |
| — | DGAF QA Assertion Report | `docs/DGAF_QA_ASSERTION_REPORT.md` | Assertion report (rubric-bearing) | ✅ | Carries QA assertion logic |
| — | Structural QA — GAP3 Evidence | `docs/STRUCT_QA_001_GAP3_EVIDENCE.md` | Structural QA evidence (rubric-bearing) | ✅ | QA-evidence doc |
| — | Drive Update Template — Eval Rubrics | `docs/ops/DRIVE_UPDATE_TEMPLATE_EVAL_RUBRICS.md` | Eval rubric template (ops) | ✅ | Ops template, not a standing rubric |

---

## 6. Registry metadata to carry forward (required fields, per the registry's own protocol)

For each entry, the registry should carry: **Rubric ID · canonical name · type · scope · owner/authority · repository/path · Notion record · version · status · classification · dimensions · scoring method · thresholds · blocking behavior · inputs · outputs · dependent gates · supersedes · superseded by · duplicate/alias names · evidence status · last verified · audit notes.**

The current Notion registry page lists these required fields in its "Required registry fields" section. The corrected table above provides the **repository/path** and **present/evidence status** columns from the live filesystem. The remaining fields (dimensions, scoring method, thresholds, blocking behavior, version, last verified, etc.) need to be populated from each rubric file's own content — that is a separate read pass, not a filesystem scan.

---

## 7. What the cohort measurement (M-001) should cross-reference

The agent cohort measurement for Clarion/Keystone/Continuum/Cadence should be a registry entry (proposed ID: **M-001**) that cross-references the governing rubrics for each measurement dimension:

| Measurement dimension | Governing rubric(s) | Cross-reference |
|---|---|---|
| D1 — Task completion | R-004 (Clarion), R-013 (Keystone), R-006 (Continuum, GAP), R-007 (Cadence, GAP) | Each agent's own QA_RUBRIC (where present) + R-001 (core rubric) as fallback |
| D2 — Cited-evidence fidelity | R-001 (DGAF Core QA Rubric) + R-030 (Ecosystem Epistemic/Documentation Rubric, if R-030 is the correct ID for that instrument) | Cite the specific rubric dimensions that govern evidence traceability |
| D3 — Boundary discipline | Each agent's QA_RUBRIC (where present) + the agent authority-class model (AGENT_AUTHORITY_INVARIANT.md / AGENT_AUTHORITY_MATRIX.md) | Cite the authority-class limits and boundary-stop requirements |
| D4 — Failure-mode handling | R-001 (uncertainty/verification handling) + each agent's SPEC (failure-mode suppressions) | Cite the agent's own stated failure-mode suppressions from its SPEC |
| D5 — Downstream usability | Each agent's INTEGRATION doc (cross-agent contracts) + the relevant agent-interoperability rubric | Cite the INTEGRATION doc's phones-home and downstream-contract clauses |

**Note on R-006 and R-007 (Continuum and Cadence):** These agents have no QA_RUBRIC file on disk. The cohort measurement's D1 cross-reference for these two should use R-001 (core rubric) as the governing instrument, and the measurement should flag that the agent's own QA_RUBRIC layer is missing — which is itself a measurement-finding (the gap is part of what's being measured, not a reason to skip the dimension).

---

## 8. Recommended registry operations (based on the audit protocol)

### 8.1 Immediate — correct the registry's confirmed table

1. Replace the registry's R-002 through R-017 table with the corrected R-002 through R-030 table from §4 above, using the live filesystem inventory.
2. Close the gap flag for The Librarian, The Auditor, The Actualizer, and Perigee as **confirmed-present** (their QA_RUBRIC files exist on disk).
3. Open a **confirmed-gap** record for Continuum and Cadence (folders present, QA_RUBRIC missing — both are current-cohort seed agents).
4. Mark Equilibrium and Synergy as **TBD — folder present, layer completeness not scanned** pending a dedicated scan.
5. Add **version** and **last-verified** fields to each table row (version from each rubric file's own header if present; last-verified = 2026-09-04 for this scan).

### 8.2 Next — populate remaining required fields from rubric content

For each confirmed-present rubric file, read its content and populate: dimensions, scoring method, thresholds, blocking behavior, inputs, outputs, dependent gates, supersedes/superseded-by, duplicate/alias names, audit notes. This is a content read, not a filesystem scan, and should be done agent-by-agent or via a batch read.

### 8.3 Operationalize the cohort measurement as M-001

Create the cohort measurement as a registry entry (M-001) governed by the registry's own protocol, cross-referencing the governing rubrics per §7, and scoring Clarion/Keystone/Continuum/Cadence against the D1–D5 schema with cited evidence for each score. This is the first use of the registry as an operational measurement index — which is the better way in progress.

---

## 9. What "best practices recommend" summarizes to

1. **One canonical source per rubric** — filesystem path + Notion record + version + last-verified. The registry has the field list; the corrected table provides the path + evidence status from the live scan.
2. **Supersession chains** — every rubric tracks what it supersedes and what supersedes it. The protocol calls for it; the entries need to be populated.
3. **Explicit classification** — rubric vs. rubric-like vs. reference vs. superseded vs. candidate. The registry has it; entries need to carry it.
4. **Contradiction detection** — overlapping rubrics compared on dimensions, weights, thresholds, vetoes. The protocol has it; it needs a per-pair comparison pass.
5. **Coverage test** — every evaluation target mapped to its governing rubric(s). The cohort measurement (M-001) is the first operational coverage test.
6. **Gap test** — expected-but-missing rubrics flagged explicitly. The corrected table does this (continuum, cadence as confirmed gaps; equilibrium, synergy as TBD).
7. **Evidence status per entry** — confirmed-by-file vs. confirmed-by-reference vs. unverified. The corrected table provides this from the live scan.
8. **Deduplication** — copies collapsed into one canonical entry. The sentinel ×2 (QA_RUBRIC.md + SENTINEL_PHI_QA_RUBRIC.md) needs a deduplication note — whether they are two distinct rubrics or a primary + a variant.
9. **Version + last-verified** — not yet in the table; needs to be added from each rubric's own header + this scan date.
10. **Operationalization** — the registry governs actual evaluations. The cohort measurement (M-001) is the first step toward this.

---

## 10. What's verified vs. what needs a separate pass

### Verified from this scan (filesystem evidence)
- Every QA_RUBRIC file path and presence/absence status in §1 and §4
- The six-layer completeness for the 21 full-6-layer folders and the 2 five-layer folders (continuum, cadence) in §3
- The 5 non-agent rubric-bearing documents in §5
- The corrected agent-rubric count (25 files, 23 folders) vs. the registry's provisional 17

### Needs a separate content-read pass
- Each rubric's dimensions, scoring method, thresholds, blocking behavior, version — these live inside each rubric file's content, not in the filename
- The sentinel ×2 deduplication question (two distinct rubrics vs. primary + variant)
- Equilibrium and Synergy layer completeness (folder exists; not scanned for all 6 layers)
- The "industry-translation rubric," "Gold Star standards," "multi-scale evaluation rubrics," and "qualitative maturity rubric" referenced in the Notion registry's A-001–A-007 rows — whether they exist on disk as rubric-bearing files or only as Notion references

### Needs a dedicated scan
- All rubric-like documents in `docs/` and `.hermes/work/` that may function as evaluation instruments without the word "RUBRIC" in the filename (the `grep` in the interrupted response found 40+ candidate files in `.hermes/work/` alone, plus the `docs/` rubric-bearing set in §5)

---

*Classification: T1 PUBLIC — filesystem-verified inventory, not a claim of exhaustive completeness. The 25-agent-QA_RUBRIC count is a lower bound from the live scan; the full rubric ecosystem includes rubric-like instruments not captured by the QA_RUBRIC filename pattern.*
