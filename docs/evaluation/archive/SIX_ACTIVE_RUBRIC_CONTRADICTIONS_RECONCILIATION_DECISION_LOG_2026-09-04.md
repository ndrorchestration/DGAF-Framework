# Six Active Rubric Contradictions — Reconciliation Decision Log

**Generated:** 2026-09-04  
**Source:** Notion SSOT (`MASTER RUBRIC REGISTRY & AUDIT — 2026-09-04`) + independent on-disk verification  
**Canonical home:** `docs/evaluation/`  
**Cross-reference:** Notion page `https://app.notion.com/p/3d1f5bad238b812d8e66c7d7f0747cde?pvs=204`  
**Governance linkage:** `docs/evaluation/CANONICAL_INSTRUMENT_RECONCILIATION_MATRIX_2026-09-04.md` (full instrument-ontology layer) · `docs/agents/GOVERNANCE_LINKS.md`  
**Standing posture:** PRE-FREEZE · FAIL-CLOSED · N=0 · NOT AUTHORIZED — no contradiction resolution advances authorization or empirical execution

---

## Purpose

This log records the six active rubric contradictions identified during the transversal audit, their reconciled disposition per the Notion SSOT, and the on-disk evidence that supports or qualifies each disposition. Each contradiction is treated as a **well-defined, evidence-backed exception class with explicit closure conditions** — not an ambiguous "contradiction" label.

The governing principle (from the SSOT): **reconciliation does not mean falsely marking them CONFIRMED.** A contradiction that is identified and bounded is not a contradiction that is resolved. The 25-document count stands as `19 CONFIRMED + 6 CONTRADICTION`, where CONTRADICTION means "the instrument's identity, authority, scope, or mathematics is in conflict with the canonical record and has not been reconciled to a single authoritative interpretation."

---

## Reconciliation framework

The reconciliation does **not** assert that any contradictory instrument is wrong, deprecated, or invalid. It asserts that:

1. The instrument's on-disk identity, authority claim, scope, or mathematics is in conflict with another authoritative source.
2. The conflict has a specific type (identity/authority, mathematical, specification, threshold-scope).
3. The closure condition for each conflict is explicit — i.e., what would constitute resolution.
4. Until closure, the instrument must not be used as an authoritative predicate without its conflict explicitly flagged.

**Conflict types used:**

| Type | Meaning |
|---|---|
| **Specification conflict** | Two instruments claim the same canonical specification but implement different formulas, dimensions, or scoring methods. |
| **Mathematical defect** | An instrument's published weights, formula, or thresholds are internally inconsistent (e.g., weights don't sum to 1.00, formula doesn't reach stated range). |
| **Identity/authority conflict** | An agent ID, classification, or authority claim conflicts with the canonical roster, formation topology, or taxonomy document. |
| **Threshold-scope conflict** | Multiple threshold values for the same named predicate exist across artifacts, and it is not established whether they are the same predicate or different ones. |

---

## The six contradictions

### 1. Apogee AXIS — Specification conflict

**Notion disposition:** Specification conflict — distinct 7D QA rubric, not the canonical AXIS implementation.

**On-disk evidence (verified this session):**

- `docs/agents/apogee/QA_RUBRIC.md` header (line 5): "Source: AXIS_METRIC_SPEC.md v1.2 (Njineer ratified 2026-06-27)"
- `docs/agents/apogee/QA_RUBRIC.md` line 12: "evaluates formation health across **7 orthogonal dimensions**... Composite score is the **weighted sum**"
- `docs/agents/apogee/QA_RUBRIC.md` line 18: D1 through D7, weights starting at 0.20 (D1), continuing through D7
- Canonical AXIS (from `docs/qa/AXIS_METRIC_SPEC.md`): **4 × 0–100 weakest-link** — completely different structure (4 dimensions, not 7; 0–100 scale, not 0–1 weighted sum; weakest-link, not weighted sum)

**Conflict type:** Specification conflict — the Apogee rubric claims lineage to `AXIS_METRIC_SPEC.md` (v1.2, Njineer ratified) but its 7-dimension weighted-sum structure does not match the canonical AXIS (4 × 0–100 weakest-link). The lineage claim and the implementation are in conflict.

**Closure condition:** Establish whether the canonical `docs/qa/AXIS_METRIC_SPEC.md` is the authoritative AXIS (in which case Apogee's rubric should be reclassified as a separate instrument that incorrectly claims AXIS lineage, or should be corrected to implement canonical AXIS); or establish that a different version of AXIS_METRIC_SPEC.md (e.g., v1.2 vs the current v1.2) is the one Apogee actually sources from. Either way, the instrument ID and the lineage claim must be reconciled to a single authoritative interpretation.

**Verification status:** Partially verified. The on-disk conflict between Apogee's 7D weighted sum and canonical 4×0–100 weakest-link is confirmed. The question of whether `docs/qa/AXIS_METRIC_SPEC.md` is the canonical spec Apogee claims to source from (and whether v1.2 is the same file) has not been fully resolved — the "specification conflict" labeling depends on confirming that the canonical spec is the one the lineage claim points to.

---

### 2. Core DGAF Rubric — Mathematical defect

**Notion disposition:** Mathematical defect — published weights total 1.50 while the formula divides by 11, making the stated threshold unreachable.

**On-disk evidence (independently verified this session):**

From `docs/qa/QA_RUBRIC.md`:

**Weight structure (lines 62–105):**

- Domain A (Q1–Q3): 0.20 each → 0.20 × 3 = 0.60
- Domain B (Q4–Q6): 0.15 each → 0.15 × 3 = 0.45
- Domain C (Q7–Q9): 0.10 each → 0.10 × 3 = 0.30
- Domain D (Q10–Q11): 0.075 each → 0.075 × 2 = 0.15
- **Sum = 1.50** (not 1.00)

**Composite formula (line 239):**

```text
S_{11Q} = (1/11) Σ w_i · Q_i
```text
where each Q_i ∈ [0,1] and Σ w_i = 1.50.

**Reachable range under literal execution:**
- If all Q_i = 1.0: S_11Q = (1/11) × 1.50 = 0.1364 — not 1.00
- If all Q_i = 0.0: S_11Q = 0.0
- Reachable range under literal execution: [0, 0.136], not [0, 1.0]

**Thresholds stated in the document:**
- Q10: "Blocking threshold: score < 0.70" (line 167)
- Q11: "Blocking threshold: score < 0.60" (line 183)
- Composite pass: "≥ 0.70" (referenced in gating language)

**Conflict:** The stated 0.70 threshold for Q10 is unreachable under the published formula (max reachable = 0.136). Either the formula is wrong, the weights are wrong, or the threshold language is wrong. The instrument cannot function as an authoritative scoring predicate without reconciling which of these is authoritative.

**Additional defect (verified):** Two of the six weighted-average rows in Section 1 do not sum to 1.00:
- Domain B (lines 68–71): 0.45
- Domain C (lines 75–78): 0.30

These are additional mathematical defects within the same instrument, confirming the defect is not isolated to the top-level composite formula.

**Closure condition:** Reconcile the instrument so that:
1. Either the weights sum to 1.00 (with the 1/11 divisor intact), or
2. The divisor is corrected to Σ w_i (i.e., 1.50), making the formula a proper weighted average, or
3. The weights, formula, and thresholds are all corrected to a single internally consistent specification.

The closure condition must name which of the three (or a fourth option) is authoritative, and must be traceable to an authoritative source (Njineer ratification, governance artifact, or explicit reconciliation decision).

**Verification status:** Fully verified on disk. The weights, formula, and reachable range are all computed from the published source. The conflict is real and the closure condition is explicit.

---

### 3. Ionia — Identity/authority conflict

**Notion disposition:** Identity/authority conflict — A-13 in the roster versus 0Hz STATE in formation topology.

**On-disk evidence (verified this session):**

From `docs/agents/ionia/QA_RUBRIC.md` (line 3): "**Agent:** Ionia (A-13)"
From `docs/agents/AGENT_ROSTER.md` (line 55): "| **Agent Ionia** | A-13 | Modal Lock | Ionian Harmonic (0Hz) lock; system harmonious/intuitive/audit-ready; NDR-Protocol-01 State Sync coupling with Reson | Modal tuning advisory |"
From `docs/AGENT_ARCHITECTURE_ASSESSMENT.md` (line 22): "| ionia | A-13 | (≥5) | ✓ | — | — | — | T2 FRAMEWORK — **system STATE, not functional agent** |"
From `docs/AGENT_ARCHITECTURE_ASSESSMENT.md` (line 126): "Ionia | A-13 | ✓ (v1.1) | — | — | — | — | **CONCEPTUAL (T2 FRAMEWORK — system STATE, not an agent to instantiate)** |"
From `docs/agents/ionia/QA_RUBRIC.md` line 9: "D-1: Lock Accuracy — Did Ionia correctly lock to **0Hz** when Reson score ≥ 0.75..."

**Conflict:** Ionia is listed as `A-13` in the agent roster (an agent seat in the 20-agent formation). But the canonical architecture assessment classifies Ionia as a **system STATE, not a functional agent** (T2 FRAMEWORK, conceptual, "not an agent to instantiate"). The QA rubric and formation topology describe Ionia's function (0Hz modal lock, harmonic tuning advisory) as if it were an agent seat, but the architecture assessment says it's a conceptual state — a property of the system, not an agent that acts.

**Closure condition:** Establish whether Ionia is:
1. An agent seat (A-13 in the roster, with QA rubric, QA-scoring capability, and formation role), or
2. A system STATE (a property/tuning of the system, not an agent that acts or scores)

and reconcile the QA rubric, the roster entry, and the architecture assessment to a single authoritative interpretation. If Ionia is a system state, the QA rubric treating it as a scorable agent creates a category error. If Ionia is an agent, the architecture assessment's "system STATE" classification was wrong.

**Verification status:** Verified on disk. The conflict between the roster/QA-rubric treatment (agent seat) and the architecture assessment (system STATE, conceptual, not to be instantiated) is confirmed. The "0Hz STATE in formation topology" phrasing in the Notion disposition is an accurate description of the conflict.

---

### 4. Oracle — Identity/authority conflict

**Notion disposition:** Identity/authority conflict — A-20 exists in Oracle/topology documentation but is outside the sovereign roster's established operational set.

**On-disk evidence (verified this session):**

From `docs/agents/oracle/ORACLE_QA_RUBRIC.md` (line 4): "**Agent ID:** A-20" — confirmed across all 6 Oracle artifacts (SPEC, KB_SEED, PROTOCOL, INTEGRATION, QA_RUBRIC, MEMORY), each line 4: "A-20"
From `docs/agents/AGENT_ROSTER.md`: The roster covers "A-00 through A-13" (T1/T2 operational layer) and "A-14 through A-19" (T3 SOVEREIGN stubs). **A-20 is absent from the roster.**
From `docs/AGENT_ECOSYSTEM_REGISTRY.md` (line 6): "This file is the single source of truth for agent names, roles, and duty assignments across the T1/T2 operational layer (A-00 through A-13)."

**Conflict:** Oracle's six artifact files (SPEC, KB_SEED, PROTOCOL, INTEGRATION, QA_RUBRIC, MEMORY) are all present on disk and uniformly identify the agent as **A-20, T1 PUBLIC**. But Oracle/A-20 is outside the established operational roster (A-00→A-13 operational, A-14→A-19 T3 stubs). The roster's stated scope (T1/T2 operational layer, A-00 through A-13) does not include A-20.

**Closure condition:** Establish whether:
1. A-20 is an intended operational agent that the roster should be extended to include, or
2. A-20 is an out-of-scope or deprecated agent ID whose artifacts should not be treated as part of the operational inventory, or
3. The roster's scope statement ("A-00 through A-13") is incomplete and should be expanded

and reconcile the Oracle artifacts' A-20 identity with the roster's operational scope. The conflict is that Oracle claims an agent ID (A-20) and a full artifact set (SPEC, KB, PROTOCOL, QA, INTEGRATION, MEMORY) that is not reflected in the canonical roster's operational set.

**Verification status:** Verified on disk. Oracle's A-20 identity is confirmed across all six artifacts. A-20's absence from the roster is confirmed. The conflict is real.

---

### 5. Reson — Threshold-scope conflict

**Notion disposition:** Threshold-scope conflict — 0.75, 0.85, and 0.90 are now explicitly treated as potentially different predicates rather than one interchangeable threshold.

**On-disk evidence (verified this session):**

From `docs/agents/reson/RESON_KB.md`:
- Line 51: "Gate (AX-06): **≥0.75** required for Apogee Pillar C PASS"
- Line 57: "≥0.75: PASS → route to Apogee as Pillar C input"
- Line 58: "<0.75: FAIL → route to Apogee as Pillar C fail; surface to Amethyst"

From `docs/agents/reson/KB.md`:
- Line 47: "**Floor for seal:** 0.85 · **Target:** ≥ 0.90 (Ionian sustained)"

From `docs/agents/reson/MEMORY.md`:
- Line 13: "| Harmonic gate (AX-06) | **≥0.75** | 2026-06-29 |"

From `docs/agents/reson/PROTOCOL.md`:
- Line 50: "| ≥ **0.90** | Ionian sustained | Emit score, no action needed |"
- Line 59: "Reson is **non-blocking by default** — scores below **0.90** generate advisories, not hard blocks (exception: Phrygian dissonance at **< 0.70** blocks seal)."

From `docs/agents/reson/QA_RUBRIC.md`:
- Line 69: "**Seal floor:** 0.85 · **Ionian sustained target:** ≥ 0.90"
- Line 78: "| ≥ **0.90** | Ionian sustained | Emit score | Proceed to seal |"

**Three distinct predicates using the same word "threshold":**
1. **0.75** — AX-06 gate (Apogee Pillar C input) — from KB.md, RESON_KB.md, MEMORY.md. This is a **gate predicate**: score above 0.75 routes to Apogee as PASS; below routes as FAIL.
2. **0.85** — Seal floor — from KB.md line 47, QA_RUBRIC.md line 69. This is a **seal predicate**: the floor for seal eligibility.
3. **0.90** — Ionian sustained target — from KB.md line 47, PROTOCOL.md line 50, QA_RUBRIC.md line 69/78. This is a **target predicate**: the goal for sustained Ionian mode.

**Conflict:** The word "threshold" is used for all three predicates, but they are structurally different (gate floor vs. seal floor vs. sustained target). Treating them as one interchangeable threshold would conflate a pass/fail routing gate (0.75) with a seal eligibility floor (0.85) with a quality target (0.90). The policy that says "Reson score must reach 0.75 for seal" is ambiguous: does that mean the AX-06 gate (0.75) or the seal floor (0.85) or the target (0.90)?

**Closure condition:** Establish whether 0.75, 0.85, and 0.90 refer to:
1. Three distinct predicates (AX-06 gate, seal floor, Ionian-sustained target) — in which case each must be labeled by its predicate name, not by the generic word "threshold," and
2. The policy language across artifacts must be reconciled so that seal decisions cite the correct predicate (seal floor = 0.85, not the AX-06 gate = 0.75) and routing decisions cite the correct predicate (AX-06 gate = 0.75).

The NOTION disposition (treating them as potentially different predicates) is the correct epistemic posture until the predicate mapping is explicitly established.

**Verification status:** Fully verified on disk. All three threshold values and their predicate contexts are confirmed from the source files. This is the strongest of the six conflicts: three distinct predicates, all using the word "threshold," across multiple artifacts.

---

### 6. Sentinel-Phi — Identity/authority conflict

**Notion disposition:** Identity/authority conflict — `variant_of → Sentinel` is established, but A-12 versus A-12-φ remains unresolved.

**On-disk evidence (verified this session):**

From `docs/agents/sentinel/SENTINEL_PHI_QA_RUBRIC.md` (line 4): "**[Agent ID:** A-12-φ**]** — confirmed in all Sentinel-Phi artifacts.
From `docs/agents/sentinel/`: Sentinel-Phi has five artifacts (SENTINEL_PHI_QA_RUBRIC.md, SENTINEL_PHI_PROTOCOL.md, SENTINEL_PHI_INTEGRATION.md, SENTINEL_PHI_MEMORY.md, SENTINEL_PHI_UPGRADE.md), each with `A-12-φ`.
From `docs/agents/sentinel/SPEC.md` (base Sentinel): No reference to Sentinel-Phi or A-12-φ.
From `docs/agents/sentinel/KB.md` (base Sentinel): No reference to Sentinel-Phi.
From `docs/agents/sentinel/QA_RUBRIC.md` (base Sentinel): No reference to Sentinel-Phi.
From `docs/agents/sentinel/AGENT_ROSTER.md`: No reference to A-12-φ or variant_of language.
From `docs/AGENT_ECOSYSTEM_REGISTRY.md`: No `variant_of` or lineage language connecting Sentinel-Phi to base Sentinel.

**What is established on disk:**
- Sentinel-Phi exists as a distinct agent with ID `A-12-φ`, T1 PUBLIC, with its own five-artifact set.
- Sentinel-Phi's QA rubric (D1–D5, weights 0.35/0.25/0.20/0.15/0.05) is structurally different from base Sentinel's QA rubric.
- The filename and artifact naming (`SENTINEL_PHI_*`) suggests a relationship to base Sentinel, but no on-disk language establishes `variant_of → Sentinel`.

**What is NOT established on disk:**
- No `variant_of`, `derived_from`, `supersedes`, `parent`, or `base` language anywhere in any Sentinel-Phi artifact.
- No cross-reference from base Sentinel artifacts to Sentinel-Phi.
- The "variant_of → Sentinel is established" claim in the Notion disposition is **not supported by on-disk evidence** as of this verification.

**Conflict (re-scoped from the Notion disposition):**
The original Notion disposition said "`variant_of → Sentinel` is established, but A-12 versus A-12-φ remains unresolved." The "variant_of established" half is not supported by on-disk evidence — there is no artifact that states Sentinel-Phi is a variant of Sentinel. The "A-12 vs A-12-φ unresolved" half is accurate: Sentinel-Phi has ID `A-12-φ`, base Sentinel has ID `A-12`, and the relationship between them is not explicitly defined in the canonical documents.

**Correction to SSOT disposition:** The disposition's first clause ("`variant_of → Sentinel` is established") should be treated as a verification gap. If the SSOT has a Notion-side record establishing the variant relationship that is not yet reflected in the repository artifacts, that record should be cited as the establishing authority and should be backported into the Sentinel-Phi artifacts (or at minimum referenced from them). Until then, the on-disk conflict is: A-12-φ exists as a distinct agent with a structurally different QA rubric, and the A-12 / A-12-φ relationship is not explicitly defined in the canonical documents.

**Revised closure condition:** Establish whether:
1. Sentinel-Phi is a variant/derivative of base Sentinel (A-12 → A-12-φ), in which case the `variant_of` relationship must be explicitly documented in the artifacts (currently absent), or
2. Sentinel-Phi is an independent agent (A-12-φ as a distinct seat, not a variant), in which case the naming convention (`SENTINEL_PHI_*` files in the `sentinel/` directory) is misleading and should be clarified.

The conflict is real — A-12 and A-12-φ coexist, Sentinel-Phi's artifacts are structurally distinct, and the `variant_of` claim in the Notion disposition is not backed by on-disk evidence.

**Verification status:** Partially verified, with correction. The "A-12 vs A-12-φ unresolved" half is confirmed. The "variant_of → Sentinel is established" half is **not** supported by on-disk evidence — the disposition's first clause should be flagged as an open verification gap. The Notion SSOT may have additional context (e.g., a Notion page or record that establishes the variant relationship) that is not yet reflected in the repository artifacts.

---

## Summary table

| # | Rubric | Conflict type | Closure condition summary | Verified on disk? |
|---|---|---|---|---|
| 1 | Apogee AXIS | Specification conflict (7D weighted sum ≠ canonical 4×0–100 weakest-link) | Reconcile lineage claim to authoritative spec version; reclassify or correct | Partially (conflict confirmed; spec version reconciliation pending) |
| 2 | Core DGAF | Mathematical defect (weights = 1.50, formula ÷ 11, threshold unreachable) | Reconcile weights/formula/thresholds to single consistent spec | ✅ Fully verified |
| 3 | Ionia | Identity/authority (A-13 roster seat vs T2 system STATE) | Establish agent vs system-state; reconcile roster + QA rubric + architecture assessment | ✅ Fully verified |
| 4 | Oracle | Identity/authority (A-20 outside roster scope A-00→A-19) | Establish whether A-20 is in-scope operational agent or out-of-scope; reconcile roster | ✅ Fully verified |
| 5 | Reson | Threshold-scope (0.75/0.85/0.90 are three distinct predicates) | Label each predicate by name, not generic "threshold"; reconcile seal/routing policy language | ✅ Fully verified (strongest) |
| 6 | Sentinel-Phi | Identity/authority (A-12-φ distinct from A-12; `variant_of` claim not on-disk verified) | Establish variant relationship or independence; correct naming if misleading | ⚠️ Partially — "A-12 vs A-12-φ unresolved" confirmed; "variant_of established" NOT on-disk verified |

---

## Reconciliation status

**40 instruments → 25 active rubrics → 19 CONFIRMED + 6 CONTRADICTION.**

The six contradictions are now recorded as well-defined, evidence-backed exception classes with explicit closure conditions. They are NOT resolved — they are identified and bounded. The reconciliation does not assert that any contradictory instrument is wrong, deprecated, or invalid. It asserts that each has a specific conflict type and a specific closure condition, and that until closure, the instrument must not be used as an authoritative predicate without its conflict explicitly flagged.

**Scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. Reconciling contradictions is a documentation and instrument-identity activity — it does not change the authorization state, the freeze state, or the empirical execution state.

---

## Cross-reference to instrument-ontology layer

See `docs/evaluation/CANONICAL_INSTRUMENT_RECONCILIATION_MATRIX_2026-09-04.md` for the full instrument-ontology layer that underlies this reconciliation:
- INST-QA-001 (DGAF Core QA Rubric) — carries the mathematical defect (Finding CX-02)
- INST-APOGEE-7Q (Apogee QA Rubric) — carries the specification conflict (Finding CX-01)
- INST-IONIA-13Q (Ionia QA Rubric) — carries the identity/authority conflict (Finding CX-03)
- INST-ORACLE-20Q (Oracle QA Rubric) — carries the identity/authority conflict (Finding CX-04)
- INST-RESON-4Q (Reson Harmonic Scoring Rubric) — carries the threshold-scope conflict (Finding CX-05)
- INST-SENTINEL-PHI-5Q (Sentinel-Phi QA Rubric) — carries the identity/authority conflict (Finding CX-06)

---

Classification: T1 PUBLIC — reconciliation record, not authoritative resolution. Six contradictions identified, bounded, with closure conditions — not resolved. Notion SSOT is the master registry; this repo artifact is the governed sidecar for on-disk evidence.
