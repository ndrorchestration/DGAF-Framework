# Six Active Rubric Records — Reconciliation Decision Log (6 → 5+1 reclassification)
**Generated:** 2026-09-04  
**Source:** Notion SSOT (`MASTER RUBRIC REGISTRY & AUDIT — 2026-09-04`) + independent on-disk verification  
**Canonical home:** `docs/evaluation/`  
**Cross-reference:** Notion page `https://app.notion.com/p/3d1f5bad238b812d8e66c7d7f0747cde?pvs=204`  
**Governance linkage:** `docs/evaluation/CANONICAL_INSTRUMENT_RECONCILIATION_MATRIX_2026-09-04.md` (full instrument-ontology layer) · `docs/agents/GOVERNANCE_LINKS.md`  
**Standing posture:** PRE-FREEZE · FAIL-CLOSED · N=0 · NOT AUTHORIZED — no contradiction resolution advances authorization or empirical execution  

---

## Purpose

This log records the six active rubric records identified during the transversal audit, their reconciled disposition per the Notion SSOT, and the on-disk evidence that supports or qualifies each record. The six records have been reclassified from a prior "6 CONTRADICTION" framing into a more precise **5 internally-coherent-rubric + 1 genuine-intrinsic-contradiction** structure.

The governing principle (from the SSOT): **reconciliation does not mean falsely marking them CONFIRMED.** A record that is identified and bounded is not a record that is resolved. The 25-document count now stands as **24 CONFIRMED + 1 CONTRADICTION**, where:

- **CONFIRMED** = the rubric artifact is internally coherent (weights sum correctly, formula is self-consistent, thresholds are defined) and its only remaining issues are external dependencies (authority, lineage, identity, scope-binding) — not intrinsic contradictions.
- **CONTRADICTION** = the rubric's own published weights and formula are mutually inconsistent; the instrument itself is broken under literal execution and cannot produce a valid score without authoritative correction.

---

## Reclassification rationale

The prior "6 CONTRADICTION" framing blurred two distinct failure-mode classes:

| Failure mode | Meaning | Count in this set |
|---|---|---|
| **Intrinsic contradiction (instrument broken)** | The rubric's own published weights and formula are mutually inconsistent; no valid score can be computed under literal execution | **1** — Core DGAF (RUB-CORE-001) |
| **External dependency/authority conflict (instrument coherent)** | The rubric's own weights and formula are internally coherent; the only unresolved issues are external to the rubric: authority claims, lineage attribution, identity classification, or scope-binding to other instruments | **5** — Apogee AXIS, Ionia, Oracle, Reson, Sentinel-Phi |

The distinction matters because the remediation tracks are different:

- The **1 intrinsic contradiction** requires authoritative correction of weights/formula/thresholds to a single internally consistent specification before any score can be valid.
- The **5 external-dependency records** require external reconciliation (roster updates, lineage documentation, authority disambiguation, scope-binding cleanup) — the rubrics themselves do not need correction.

---

## Current registry state

**40 total instruments → 25 ACTIVE rubrics → 24 CONFIRMED + 1 CONTRADICTION.**

The six-record exception set is now properly differentiated:

| # | Record | Instrument ID | Disposition | Type |
|---|---|---|---|---|
| 1 | Apogee AXIS | INST-APOGEE-7Q | Confirmed as a distinct 7D Apogee rubric; AXIS equivalence remains a dependency | External dependency (lineage) |
| 2 | Ionia | INST-IONIA-13Q | Confirmed as a rubric; seat-versus-STATE semantics remain an identity dependency | External dependency (identity) |
| 3 | Oracle | INST-ORACLE-20Q | Confirmed as a rubric; A-20 authority remains an identity dependency | External dependency (authority) |
| 4 | Reson | INST-RESON-4Q | Confirmed as a rubric; 0.75/0.85/0.90 remain separate predicates pending the P-15 contract | External dependency (scope-binding) |
| 5 | Sentinel-Phi | INST-SENTINEL-PHI-5Q | Confirmed as a distinct variant-lineage rubric; A-12/A-12-φ authority remains unresolved | External dependency (authority) |
| 6 | Core DGAF | INST-QA-001 | Remains the **one genuine intrinsic contradiction** because the published 11Q weighting equation is mathematically inconsistent | **Intrinsic contradiction** |

---

## Notion changes completed

The master registry now carries the normalized **24/1** state and explicitly distinguishes artifact confirmation from authority, runtime, or experimental authorization.

The six-record reconciliation log has been updated with the new classification model (this document).

The **Current Rubrics — Active** view now has the exact `Type=RUBRIC AND Lifecycle Status=ACTIVE` filter.

The **Rubric Contradictions — Intrinsic** view now isolates only genuinely contradictory active rubric artifacts.

A closure queue was added covering the four remaining upstream workstreams:

1. Core 11Q correction (intrinsic contradiction resolution — authoritative weights/formula/thresholds)
2. Agent-ID authority (Ionia seat-vs-STATE, Oracle A-20, Sentinel-Phi A-12/A-12-φ)
3. P-15 predicate binding (Reson 0.75/0.85/0.90 scope-binding to the P-15 contract)
4. Apogee/AXIS bridge (Apogee 7D lineage to canonical AXIS)

The scientific boundary remains unchanged: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.**

---

## Per-record detail

### 1. Apogee AXIS — Confirmed distinct rubric + AXIS lineage dependency

**Instrument ID:** INST-APOGEE-7Q  
**Internal coherence:** ✓ Confirmed. D1–D7, weights 0.20/0.15/0.15/0.15/0.15/0.10/0.10 sum to 1.00; clean weighted-sum composite (matrix lines 223–227).  
**External dependency:** The rubric cites `AXIS_METRIC_SPEC.md v1.2` as source but implements a 7×0–1 weighted-sum instrument that is structurally different from canonical AXIS (4 invariants I/P/A/E, each 0–100, weakest-link `min()`, composite 0–100). The "AXIS floor ≥ 0.75" name within the rubric collides with INST-AXIS as both cited source and score name.  
**Disposition:** The rubric is CONFIRMED as a distinct 7D Apogee instrument. The AXIS lineage claim is the external dependency — it either needs an explicit bridge specification (distinct instrument with lineage note) or reclassification as an instrument that does not implement canonical AXIS.  
**Closure queue:** #4 — Apogee/AXIS bridge.  
**Matrix cross-reference:** CX-03, CX-14.

---

### 2. Ionia — Confirmed rubric + seat-vs-STATE identity dependency

**Instrument ID:** INST-IONIA-13Q  
**Internal coherence:** ✓ Confirmed. QA rubric evaluates lock accuracy coherently; dimensions D-1 through D-7+ present (matrix lines 253–257).  
**External dependency:** The rubric is listed as agent `A-13` (QA rubric header, AGENT_ROSTER.md line 55) with a full QA rubric that evaluates agent behavior, but `AGENT_ARCHITECTURE_ASSESSMENT.md` (lines 22, 126) classifies Ionia as **T2 FRAMEWORK — system STATE, not a functional agent** — "CONCEPTUAL (T2 FRAMEWORK — system STATE, not an agent to instantiate)."  
**Disposition:** The rubric is CONFIRMED as an internally coherent evaluation instrument. The seat-vs-STATE semantics are the external identity dependency — either Ionia is an agent seat (treat QA rubric as a live instrument) or a system STATE (reclassify QA rubric as a conceptual evaluation document).  
**Closure queue:** #2 — agent-ID authority (Ionia).  
**Matrix cross-reference:** CX-11.

---

### 3. Oracle — Confirmed rubric + A-20 authority dependency

**Instrument ID:** INST-ORACLE-20Q  
**Internal coherence:** ✓ Confirmed. All six Oracle artifacts uniformly identify the agent as `A-20, T1 PUBLIC`; the artifact set is structurally complete and consistent (matrix lines 277–283).  
**External dependency:** A-20 is absent from the operational roster. AGENT_ROSTER.md's stated scope is "T1/T2 operational layer (A-00 through A-13)" with "T3 SOVEREIGN agents (A-14 through A-19) are stubs." A-20 falls outside both the operational layer (A-00→A-13) and the T3 stub range (A-14→A-19). AGENT_ECOSYSTEM_REGISTRY.md (line 6) reinforces: "single source of truth for agent names, roles, and duty assignments across the T1/T2 operational layer (A-00 through A-13)."  
**Disposition:** The rubric is CONFIRMED as an internally coherent instrument. The A-20 authority is the external identity dependency — either A-20 is an intended operational agent the roster should extend to include, or it is an out-of-scope/deprecated agent ID whose artifacts should not be counted in the operational inventory.  
**Closure queue:** #2 — agent-ID authority (Oracle).  
**Matrix cross-reference:** CX-12.

---

### 4. Reson — Confirmed rubric + P-15 scope-binding dependency

**Instrument ID:** INST-RESON-4Q  
**Internal coherence:** ✓ Confirmed. H1–H4, weights 0.30/0.25/0.25/0.20 sum to 1.00; clean weighted-average composite (matrix lines 345–347).  
**External dependency:** Three distinct predicates are all referred to with the generic word "threshold" across the Reson artifacts:
- 0.75 = AX-06 gate (Apogee Pillar C routing pass/fail) — from KB.md lines 47/51, RESON_KB.md line 51, MEMORY.md line 13
- 0.85 = seal floor (seal eligibility) — from KB.md line 47, QA_RUBRIC.md line 69
- 0.90 = Ionian sustained target (quality target, advisory below) — from KB.md line 47, PROTOCOL.md line 50, QA_RUBRIC.md lines 69/78

Amethyst SPEC §5 line 91 cites "Reson harmonic score ≥ 0.75" as a P-15 seal pre-condition — which is the AX-06 gate value, not the seal floor (0.85) from Reson's own QA rubric.

**Disposition:** The rubric is CONFIRMED as an internally coherent instrument. The P-15 scope-binding is the external dependency — the word "threshold" is ambiguous across three structurally different predicates, and the P-15 pre-condition citation needs to specify which predicate it means. The three predicates need to be labeled by name (AX-06 gate, seal floor, Ionian sustained target) rather than by the generic word "threshold," and the P-15 contract needs to bind to a specific predicate.  
**Closure queue:** #3 — P-15 predicate binding.  
**Matrix cross-reference:** CX-06.

---

### 5. Sentinel-Phi — Confirmed distinct variant-lineage rubric + A-12/A-12-φ authority unresolved

**Instrument ID:** INST-SENTINEL-PHI-5Q  
**Internal coherence:** ✓ Confirmed. D1–D5, weights 0.35/0.25/0.20/0.15/0.05 sum to 1.00; clean weighted-sum formula (matrix lines 314–315).  
**External dependency:** Sentinel-Phi exists as a distinct on-disk agent with ID `A-12-φ` and five artifacts. Base Sentinel has ID `A-12`. The two IDs are structurally similar (A-12 vs A-12-φ) suggesting a variant/derivative relationship. **However, no on-disk language establishes `variant_of → Sentinel`**: no `variant_of`, `derived_from`, `supersedes`, `parent`, or `base` field in any Sentinel-Phi artifact; no cross-reference from base Sentinel artifacts (SPEC.md, KB.md, QA_RUBRIC.md) to Sentinel-Phi.  
**Disposition:** The rubric is CONFIRMED as an internally coherent, distinct variant-lineage instrument. The A-12/A-12-φ authority relationship is the external dependency — either the `variant_of → Sentinel` relationship needs to be explicitly documented in the artifacts (add `variant_of: Sentinel (A-12)` or equivalent), or Sentinel-Phi is established as an independent agent seat (A-12-φ as a distinct entity, with the naming convention `SENTINEL_PHI_*` clarified as a directory/convention choice rather than a lineage claim).  
**Closure queue:** #2 — agent-ID authority (Sentinel-Phi).  
**Matrix cross-reference:** CX-13.  
**Correction note:** The Notion SSOT's prior disposition stated "`variant_of → Sentinel` is established, but A-12 versus A-12-φ remains unresolved." The "variant_of established" half was NOT supported by on-disk evidence — no artifact in `docs/agents/sentinel/` contains `variant_of`/`derived_from`/`supersedes`/`parent`/`base` language linking Sentinel-Phi to base Sentinel. The current record treats Sentinel-Phi as CONFIRMED as a distinct rubric with an unresolved A-12/A-12-φ authority dependency, which is the more accurate framing. If the SSOT has a Notion-side record establishing the variant relationship, it should be cited and backported into the Sentinel-Phi artifacts.

---

### 6. Core DGAF — One genuine intrinsic contradiction

**Instrument ID:** INST-QA-001  
**Internal coherence:** ✗ **BROKEN.** Weights sum to 1.50 (0.60 + 0.45 + 0.30 + 0.15), not 1.00. Formula `S_11Q = (1/11) Σ w_i · Q_i` with Σw_i = 1.50 and Q_i ∈ [0,1] produces a maximum of (1/11) × 1.50 = 0.13636, not 1.00. The stated P-11 ≥ 0.70 and P-15 ≥ 0.90 thresholds are unreachable under literal execution. Two of the six weighted-average rows (Domain B = 0.45, Domain C = 0.30) also don't sum to 1.00.  
**External dependencies:** None applicable — this is an intrinsic contradiction in the rubric's own published mathematics.  
**Disposition:** This is the **one genuine intrinsic contradiction** in the 25 active rubrics. The rubric's weights and formula are mutually inconsistent; no valid score can be computed under literal execution without authoritative correction.  
**Required remediation:** Authoritative decision on weight semantics — either (a) normalize Σw_i to 1.00 and keep the 11Q 0–1 composite, or (b) correct the formula to `S = Σ(w_i·Q_i) / Σw_i` (weighted average) with Σw_i = 1.50 as denominator, or (c) restate the weights to sum to 1.00. All dependent documents (agent QA rubrics, gate records citing P-11) must reference the corrected version. No silent normalization.  
**Closure queue:** #1 — Core 11Q correction.  
**Matrix cross-reference:** CX-08.

---

## Reconciliation summary

**40 total instruments → 25 ACTIVE rubrics → 24 CONFIRMED + 1 CONTRADICTION.**

Of the 24 CONFIRMED active rubrics, 5 carry external dependency/authority issues that require reconciliation but do not require correction of the rubric itself:

| External dependency class | Records |
|---|---|
| Lineage dependency (rubric cites a canonical spec but implements a different instrument) | Apogee AXIS |
| Identity dependency (rubric's governed entity is disputed: agent seat vs system state) | Ionia |
| Authority dependency (rubric's agent ID is absent from operational roster) | Oracle, Sentinel-Phi |
| Scope-binding dependency (rubric-local thresholds ambiguous across predicates; P-15 contract needs to bind to specific predicate) | Reson |

The 1 CONTRADICTION record (Core DGAF) is the only active rubric whose own published mathematics are internally inconsistent. Resolution of the external dependencies does not resolve the intrinsic contradiction — the Core 11Q correction is a separate, prior-closed workstream.

**Notion SSOT is the master registry.** This log is the governed sidecar for on-disk evidence and the reclassification rationale. The Notion views now reflect the 24/1 state with the exact `Type=RUBRIC AND Lifecycle Status=ACTIVE` filter and the **Rubric Contradictions — Intrinsic** view isolating only genuinely contradictory active rubric artifacts.

---

*Classification: T1 PUBLIC — reconciliation record, not authoritative resolution. 24 CONFIRMED active rubrics (5 with external dependencies, 19 cleanly confirmed) + 1 CONTRADICTION (Core DGAF intrinsic). Reconciliation does not advance authorization, freeze, or empirical execution. Scientific boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.*
