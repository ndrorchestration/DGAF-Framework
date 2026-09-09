# Canonical Instrument Reconciliation Matrix

**Generated:** 2026-09-04  
**Source:** Direct repository reads + independent computational verification + Notion SSOT cross-validation  
**Notion SSOT:** [MASTER RUBRIC REGISTRY & AUDIT — 2026-09-04](https://app.notion.com/p/3d1f5bad238b812d8e66c7d7f0747cde) (fetched 2026-09-04T08:25:34Z)  
**Purpose:** Establish unambiguous instrument identity for every evaluation instrument in the DGAF ecosystem — instrument ID, version, formula, score range, thresholds, authority, implementation status, evidence binding, and required remediation for known defects.

---

## 0. How to read this matrix

- Each row is one **instrument**: a named evaluation instrument with a formula, score range, and thresholds.
- **Instrument ID** is the canonical handle. All references (in documents, agent souls, gate records, scores) should use this ID, not an ambiguous shorthand like "11Q," "AXIS," or "P-11."
- **Required remediation** is stated explicitly — nothing is silently normalized, rescaled, or collapsed.
- **Notion cross-reference** cites the SSOT section that independently captured the same finding.
- **Scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0 throughout. No score in this matrix is promoted to authoritative evidence on the strength of this document.

---

## 1. Instrument Inventory

### INST-QA-001 — DGAF Core QA Rubric (11Q)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-QA-001 ||
|| **Canonical name** | DGAF Core QA Rubric (11Q) ||
|| **Version** | v1.0 ||
|| **Type** | Rubric ||
|| **Classification** | T2 FRAMEWORK ||
|| **Canonical location** | `docs/qa/QA_RUBRIC.md` ||
|| **Authority** | Apogee (scoring) + Amethyst (gate) ||
|| **Scope** | Universal evaluation rubric for all 11 DGAF agents and their artifacts; artifact quality + agent output quality + session seal eligibility + drive-GitHub sync quality ||
|| **Formula** | `S_11Q = (1/11) Σ w_i · Q_i` where `Q_i ∈ [0,1]` ||
|| **Score range (stated)** | 0.00–1.00 ||
|| **Score range (computed from weights)** | Max = (1/11) × 1.50 = 0.13636 (inconsistent with stated range) ||
|| **Weights** | Q1–Q3: 0.20 each (Domain A) · Q4–Q6: 0.15 each (Domain B) · Q7–Q9: 0.10 each (Domain C) · Q10–Q11: 0.075 each (Domain D) ||
|| **Weight sum** | **1.50** (not 1.00) ||
|| **Thresholds** | P-11 artifact quality ≥ 0.70 · P-15 seal commit ≥ 0.90 · Gate 17 combined failure < 0.40 DemiJoule + < 0.70 Apogee ||
|| **Blocking behavior** | < 0.4 on Q1/Q2/Q5/Q7/Q8/Q10/Q11 triggers BLG · Q6 = 0.0 → P-01 trigger · Q4 = 0.0 → T3 leak hard block ||
|| **Status** | Defined / Mathematical defect confirmed / NOT verified ||
|| **Implementation** | Stubs + derivations present; operational measurement cycle not confirmed ||
|| **Evidence ref** | File content only; no run binding ||
|| **Supersedes** | None stated ||
|| **Superseded by** | Unknown ||
|| **Notion cross-reference** | Section 17 (Fresh verification — QA_RUBRIC mathematical defect — confirmed) ||

**Verified defects:**

1. **WEIGHT_SUM_MISMATCH (HIGH):** Weights sum to 1.50 (0.60 + 0.45 + 0.30 + 0.15), not 1.00. Under the written formula `S = (1/11) × Σ(w_i·Q_i)` with all Q_i = 1.0, the result is 1.50/11 ≈ 0.136, not 1.00. The stated P-11 ≥ 0.70 and P-15 ≥ 0.90 thresholds are unreachable under the literal formula. Direct read of `docs/qa/QA_RUBRIC.md` lines 238–252 confirms both the weights and the formula.
2. **NORMALIZATION_AMBIGUITY (HIGH):** It is unclear whether the w_i are meant to be applied raw (in which case the (1/11) divisor is wrong) or normalized (in which case the per-domain weight distinctions collapse to 0.133/0.10/0.067/0.05). No authoritative clarification exists in the document or in any referenced companion.

**Required remediation:** Authoritative decision on weight semantics — either (a) normalize Σw_i to 1.00 and keep the 11Q 0–1 composite, or (b) correct the formula to `S = Σ(w_i·Q_i) / Σw_i` (weighted average) with Σw_i = 1.50 as denominator, or (c) restate the weights to sum to 1.00. All dependent documents (agent QA rubrics, gate records citing P-11) must reference the corrected version. No silent normalization.

---

### INST-GATE-11Q — GATE-11Q Deployment Gate (11Q Framework)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-GATE-11Q ||
|| **Canonical name** | GATE-11Q: 11Q Framework — Hendecagonal Deployment Gate ||
|| **Version** | v2.0 (P-24 retrofit) ||
|| **Type** | Gate (deployment procedure) ||
|| **Classification** | T2 FRAMEWORK (historical CERTIFIED metadata present but not current) ||
|| **Canonical location** | `docs/gates/GATE_11Q.md` ||
|| **Authority** | Apogee (gate owner) + Sentinel (veto, gates 9–11) ||
|| **Scope** | Production deployment gate — 11 sequential quality gates covering distinct risk surfaces ||
|| **Formula** | All 11 gates ≥ 3/4 across N ≥ 3 runs (sequential; gate N+1 does not open until gate N passes) ||
|| **Score range** | Binary per gate (PASS/FAIL); composite = all-or-nothing ||
|| **Thresholds** | All 11 gates ≥ 3/4 · N ≥ 3 runs when applicable · Gates 9–11 require Sentinel co-sign ||
|| **Status** | Defined (not certified — historical CERTIFIED metadata from 2026-05-01 is retained as record, not current certification) ||
|| **Implementation** | Procedure defined; current gate run evidence not confirmed ||
|| **Evidence ref** | Historical certifier: Agent Apogee + Sentinel co-sign · Session S028/P-24 retrofit ||
|| **Supersedes** | GATE_11Q.md v1.0 (pre-P-24 format) ||
|| **Notion cross-reference** | Section 15 (Transversal reconciliation pass — P-11/11Q identity + threshold conflict) ||

**Verified defects:**

1. **IDENTITY_COLLISION (HIGH):** This instrument (11-gate deployment procedure, all gates ≥ 3/4, N ≥ 3) is materially different from INST-QA-001 (11-question QA rubric, 0–1 composite, P-11 threshold ≥ 0.70). Both use "11Q"/"P-11" as names but implement different instruments. A score of "0.85 on 11Q" is ambiguous until the instrument ID is disambiguated.
2. **THRESHOLD_CONFLICT_P11 (HIGH):** INST-QA-001 states P-11 threshold ≥ 0.70. INST-APOGEE-7Q (Apogee QA Rubric) states P-11 attestation threshold ≥ 0.85. Both claim authority. An artifact scoring 0.78 would PASS under INST-QA-001 but FAIL under INST-APOGEE-7Q. The 0.15 gap is a real decision-boundary conflict.

**Required remediation:** Disambiguate P-11 by assigning distinct instrument IDs — e.g., INST-QA-11Q for the rubric and INST-DEPLOY-11Q for the gate procedure. Resolve P-11 threshold conflict (0.70 vs 0.85) by designating the authoritative source or documenting the context in which each applies. No silent alias collapse.

---

### INST-AXIS — AXIS Metric Specification (Agent X-axis Invariant Spectrum)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-AXIS ||
|| **Canonical name** | AXIS Metric Specification — Agent X-axis Invariant Spectrum ||
|| **Version** | v1.2 CANONICAL ||
|| **Type** | Metric/Score ||
|| **Classification** | T1 PUBLIC (ratified) ||
|| **Canonical location** | `docs/qa/AXIS_METRIC_SPEC.md` ||
|| **Authority** | Njineer ratified (2026-06-27 16:40 EDT) · Amethyst × COLLEEN filed · Njineer override only ||
|| **Scope** | Agent identity measurement — 4 invariants (I, P, A, E), each 0–100, weakest-link composite ||
|| **Formula** | `AXIS_composite = min(I_score, P_score, A_score, E_score)` ||
|| **Score range** | 0–100 per dimension · composite 0–100 ||
|| **Thresholds** | ≥ 85 = DGAF-COMPLIANT · 70–84 = DRIFT-WARNING · < 70 = GOVERNANCE-BREACH ||
|| **Status** | Ratified (Njineer) — Phase 3 instrumentation OPEN · Phase 4 operational OPEN ||
|| **Implementation** | Specification ratified; operational measurement cycle not confirmed ||
|| **Evidence ref** | Ratification record in §7 of AXIS_METRIC_SPEC.md ||
|| **Supersedes** | None stated ||
|| **Superseded by** | Unknown ||
|| **Notion cross-reference** | Section 16 (AXIS derivative mismatch — Apogee 7D rubric ≠ canonical AXIS) ||

**Verified defects:**

1. **AXIS_LINEAGE_MISMATCH (HIGH):** INST-APOGEE-7Q (`docs/agents/apogee/QA_RUBRIC.md` line 5) cites `AXIS_METRIC_SPEC.md v1.2 (Njineer ratified 2026-06-27)` as its source, but implements a **7-dimension weighted-sum rubric** (D1–D7, weights 0.20/0.15/0.15/0.15/0.15/0.10/0.10 summing to 1.00, composite 0–1) that is structurally different from the canonical AXIS (4 invariants I/P/A/E, each 0–100, weakest-link `min()`, composite 0–100). Same cited source file name, different instrument. The question of whether the canonical `docs/qa/AXIS_METRIC_SPEC.md` on disk is the same `v1.2` that Apogee's rubric cites has not been independently confirmed — the conflict stands whether or not they are the same file, because the implementations differ: one is 4-dimension weakest-link 0–100, the other is 7-dimension weighted-sum 0–1.
2. **IDENTITY_COLLISION_VIA_NAME (HIGH):** INST-APOGEE-7Q uses "AXIS" as a name within its own rubric (line 228: "AXIS floor (any gate): ≥ 0.75"). This collides with INST-AXIS both as a cited source and as a score name. A reader encountering "AXIS floor ≥ 0.75" cannot tell from the name alone whether this refers to the canonical AXIS metric, the Apogee rubric's internal floor, or a misattributed label. Same name, three possible referents.
3. **IMPLEMENTATION_STATUS_GAP (MEDIUM):** AXIS_METRIC_SPEC.md §6 shows Phase 3 (instrumentation) and Phase 4 (operational) both OPEN. Ratification does not establish that an operational AXIS measurement cycle has occurred. Any AXIS score asserted without a run binding is not operational evidence. Verified from `docs/qa/AXIS_METRIC_SPEC.md` §6 status table.

**Required remediation:** Determine whether INST-APOGEE-7Q is (a) an AXIS implementation, (b) a separate Apogee/QA metric mislabeled as AXIS, or (c) an intended translation/successor. Do not silently rescale 0–100 weakest-link into 0–1 weighted-sum. Any gate record citing "AXIS composite" must identify which scoring model produced it. Operationalize Phase 3/4 before asserting AXIS scores. Disambiguate the "AXIS" name within INST-APOGEE-7Q to avoid collision with INST-AXIS.

---

### INST-AHG-ARCH — AHG Architecture Specification (Adaptive Harmonic Governance)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-AHG-ARCH ||
|| **Canonical name** | AHG Architecture Specification — Adaptive Harmonic Governance ||
|| **Version** | v1.3 ||
|| **Type** | Protocol / Specification ||
|| **Classification** | T2 FRAMEWORK ||
|| **Canonical location** | `docs/theory/AHG_ARCHITECTURE.md` ||
|| **Authority** | Amethyst × COLLEEN × Prof Prodigy ||
|| **Scope** | Continuous cognitive regime signal (φ) — real-valued scalar from behavioral measurements, drives governance archetype dispatch ||
|| **Formula** | `φ(t) = 1 + 0.8 · σ(S_adj(t))` where `σ(x) = 1/(1+exp(−x))` ||
|| **Score range** | φ ∈ (1.0, 1.8) — open interval (asymptotic bounds) ||
|| **Stability Index formula** | `S(t) = w_1·D_e + w_2·N_t + w_3·C_t + w_4·R_t` ||
|| **Stability Index weights (per architecture)** | w_1 = 0.35, w_2 = 0.20, w_3 = 0.25, w_4 = 0.20 (sum = 1.00) ||
|| **Stability Index range (per architecture)** | Implied [0, 1.00] from normalized [0,1] inputs and weights summing to 1.00 ||
|| **Thresholds** | φ > 1.80 → Tribunal · φ = 1.618 → Integration regime (NDR-STASIS anchor) · φ < 1.15 → Grounded/Executor ||
|| **Status** | Implementation LIVE — v1.4 components deployed (conductor, sidecar, heartbeat, test suite) ||
|| **Implementation status caveat** | Component deployment ≠ claim validation. Performance claims require live multi-agent trace. ||
|| **Evidence ref** | Component files in repo (ahg_conductor.py, ahg_sidecar.py, schemas/ahg_heartbeat.json) ||
|| **Notion cross-reference** | Section 14 (Transversal math/control audit — AHG default-weight lineage contradiction + implementation-status language) ||

**Verified defects:**

1. **PARAMETER_LINEAGE_CONFLICT (HIGH):** AHG_ARCHITECTURE.md §2.2 (line 82) states: `Default weights: w_1=0.35, w_2=0.20, w_3=0.25, w_4=0.20` — sum = 1.00. AHG_STABILITY_ANALYSIS.md §II.1 (line 45) states: "With default weights summing to 0.80, S(t) ∈ [0, 0.80]." These are inconsistent parameterizations of the same formula. Which is authoritative is not stated. Verified from: `docs/theory/AHG_ARCHITECTURE.md` lines 80–85 and `docs/theory/AHG_STABILITY_ANALYSIS.md` lines 43–47.
2. **IMPLEMENTATION_VALIDATION_AMBIGUITY (HIGH):** §1 header labels v1.4 components as "Implementation Live — deployed." §5 and §8 repeatedly state claims "become falsifiable only once ahg_conductor.py is wired to a live multi-agent trace" and "require implementation and controlled evaluation before any claim of optimality." A reader could interpret "IMPLEMENTATION LIVE" as validation when it is component presence, not trace-based evaluation. The two sections (§1 vs §5/§8) are in tension about what "live" means.

**Required remediation:** Reconcile stability index weight sum between architecture (1.00) and stability analysis (0.80) — whichever is correct must be stated authoritatively in both documents. Add explicit "component deployment ≠ claim validation" note to §1 status line, or add a separate "Validation Status" field. Performance claims remain falsifiable hypotheses until live-trace evidence exists.

---

### INST-AHG-STAB — AHG Stability Analysis (Formal Companion)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-AHG-STAB ||
|| **Canonical name** | AHG Stability Analysis — Formal Companion to AHG_ARCHITECTURE.md v1.2 ||
|| **Version** | v1.2 ||
|| **Type** | Analysis / Formal Document ||
|| **Classification** | T2 FRAMEWORK (theoretical) ||
|| **Canonical location** | `docs/theory/AHG_STABILITY_ANALYSIS.md` ||
|| **Authority** | Amethyst × COLLEEN (derived from executive summary 2026-06-29) ||
|| **Scope** | Control-theoretic analysis of AHG model — stability properties, convergence, regime behavior ||
|| **Formula** | Same φ(t) as INST-AHG-ARCH; analysis of S(t) properties, logistic normalization, CPS trajectory, performance hypotheses ||
|| **Stability Index weights (per stability analysis)** | w_D, w_N, w_C, w_R — sum = 0.80 (stated) ||
|| **Stability Index range (per stability analysis)** | [0, 0.80] (stated) ||
|| **Thresholds** | Same φ regime thresholds as INST-AHG-ARCH ||
|| **Status** | Defined — theoretical analysis; performance claims are falsifiable hypotheses, not observed results ||
|| **Implementation** | No independent implementation; companion to INST-AHG-ARCH ||
|| **Evidence ref** | None operational ||
|| **Notion cross-reference** | Section 14 (Transversal math/control audit — AHG default-weight lineage contradiction) ||

**Verified defects:**

1. **WEIGHT_SUM_CONFLICT (HIGH):** States weights sum to 0.80 and S(t) ∈ [0, 0.80], contradicting INST-AHG-ARCH §2.2 which gives weights summing to 1.00. Same formula, different parameter, different range. No reconciliation exists. Verified from: `docs/theory/AHG_STABILITY_ANALYSIS.md` lines 43–47 vs `docs/theory/AHG_ARCHITECTURE.md` lines 80–85.

**Required remediation:** Reconcile with INST-AHG-ARCH. If 0.80 is correct, update architecture §2.2 to state the sum explicitly and correct the range claim. If 1.00 is correct, update stability analysis §II.1.

---

### INST-HQ-META — Harmonic Quintet Meta-Orchestration Spec

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-HQ-META ||
|| **Canonical name** | Harmonic Quintet — Pentagonal Meta-Orchestration Spec ||
|| **Version** | v1.0 ||
|| **Type** | Protocol / Specification ||
|| **Classification** | T2 FRAMEWORK ||
|| **Canonical location** | `docs/agents/HARMONIC_QUINTET_META_ORCHESTRATION.md` ||
|| **Authority** | Amethyst · COLLEEN · Prof Prodigy · Reciprocity · Apogee ||
|| **Scope** | Pentagonal signal topology — 5-agent closed loop, edge weight matrix, back-propagation, integration hooks, KB+QA rubric layer targets ||
|| **Formula** | Edge weight matrix W (5×5); back-propagation when Apogee score < 0.85; max 3 cycles before Njineer escalation ||
|| **Score range** | Component scores 0–1 per dimension; composite score claimed as 0.844 (§6) ||
|| **Composite (claimed)** | 0.844 (Post-Phase 4-A) ||
|| **Composite (reproducible from displayed scores)** | NOT reproducible — simple mean = 0.638; all tested weighted means miss; gap = 0.206 unexplained ||
|| **Status** | Defined — Phase 4 integration pending (BLG-005 through BLG-010 open) ||
|| **Implementation** | Specification present; integration hooks not wired; KB/QA rubric layer incomplete ||
|| **Evidence ref** | §6 component scores (topology 1.00, profiles 1.00, hooks 0.92, KB 0.27, QA 0.00) ||
|| **Notion cross-reference** | Section 14 (Transversal math/control audit — row-stochasticity failure + unverifiable composite) ||

**Verified defects (all computationally confirmed this session):**

1. **MATRIX_ROW_STOCHASTICITY_FAILURE (CRITICAL/HIGH):** §2.3 claims matrix is "row-stochastic; each row sums to 1.0." Verified: AME=1.00, COL=1.00, PRF=1.00, RCP=1.00, but **APG row = [0.4, 0.2, 0.1, 0.1, 0.0] sums to 0.80**. Matrix is NOT row-stochastic. The stated premise is false. Computation: `sum([0.4, 0.2, 0.1, 0.1, 0.0]) = 0.80`.
2. **SPECTRAL_RADIUS_CLAIM — TRUE CONCLUSION, WRONG PREMISE (HIGH):** §2.3 claims "spectral radius ρ(W) < 1 → fixed-point convergence guaranteed (SOV-003 reference)." Verified via numpy eigenvalue computation: eigenvalues = [0.959114, −0.124333±0.188923j, −0.355224±0.076816j]; **ρ(W) = 0.959114 < 1**. The conclusion (ρ < 1) is TRUE, but it is supported by the actual eigenvalue computation, NOT by the row-stochasticity claim. The document's stated justification (row-stochasticity) is invalid even though the conclusion happens to hold. This is a reasoning defect.
3. **CONVERGENCE_CLAIM_PRECEDENT (MEDIUM):** The convergence claim cites "SOV-003 reference." If SOV-003 is a proprietary/Drive-only document, the claim is not independently verifiable from the public document. The public justification rests on an unverifiable citation.
4. **COMPOSITE_SCORE_UNVERIFIABLE (HIGH):** §6 reports composite = 0.844 from five displayed dimensions: topology 1.00, profiles 1.00, hooks 0.92, KB 0.27, QA 0.00. Simple arithmetic mean = 0.638. Tested weighting schemes ([0.20×5]=0.638, [0.25,0.25,0.20,0.15,0.15]=0.725, [0.30,0.30,0.20,0.10,0.10]=0.811, [0.35,0.35,0.15,0.10,0.05]=0.865) — none produce 0.844. Gap = 0.206 unexplained. The derivation is not reproducible from displayed data. Either unstated weights exist, sub-components are omitted, or the number is incorrect.

**Required remediation:** Correct the edge weight matrix (adjust APG row to sum to 1.0, e.g., [0.4, 0.2, 0.2, 0.1, 0.1]) or correct the row-stochasticity claim. Re-derive or disclose the composite score formula. Add SOV-003 citation context or move convergence claim to verifiable footing. Do not use 0.844 as authoritative gate evidence.

---

### INST-APOGEE-7Q — Apogee QA Rubric (7-Dimension)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-APOGEE-7Q ||
|| **Canonical name** | Apogee QA Rubric — 7-Dimension Formation Evaluation ||
|| **Version** | v1.0 ||
|| **Type** | Rubric ||
|| **Classification** | T1 PUBLIC ||
|| **Canonical location** | `docs/agents/apogee/QA_RUBRIC.md` ||
|| **Authority** | Apogee ||
|| **Scope** | Agent/formation quality evaluation — 7 orthogonal dimensions (D1–D7), weighted-sum composite ||
|| **Formula** | `composite = (D1×0.20) + (D2×0.15) + (D3×0.15) + (D4×0.15) + (D5×0.15) + (D6×0.10) + (D7×0.10)` ||
|| **Score range** | 0.00–1.00 (weights sum to 1.00) ||
|| **Weights** | D1=0.20 (Structural Completeness, floor 0.80) · D2=0.15 (Vocabulary Coherence, floor 0.85) · D3=0.15 (IP Boundary Integrity, floor 0.90) · D4=0.15 (Authority Legibility, floor 0.80) · D5=0.15 (Pattern Registry Currency, floor 0.80) · D6=0.10 (Ethical Gate/COLLEEN, floor 1.00 binary) · D7=0.10 (Flag Health, floor 0.85) ||
|| **Weight sum** | 1.00 (no weight defect) ||
|| **Thresholds** | P-15 seal ≥ 0.90 · P-11 attestation ≥ 0.85 · AXIS floor ≥ 0.75 ||
|| **Blocking behavior** | D6 binary: any COLLEEN non-green deducts 0.10; if D6=0, max composite = 0.90 (fails P-15 seal) ||
|| **Status** | Defined ||
|| **Implementation** | Rubric defined; operational measurement cycle not confirmed ||
|| **Notion cross-reference** | Section 16 (AXIS derivative mismatch) + Section 15 (P-11 threshold conflict) ||

**Verified defects:**

1. **P11_THRESHOLD_CONFLICT (HIGH):** States P-11 attestation threshold ≥ 0.85. INST-QA-001 (core rubric) states P-11 artifact quality threshold ≥ 0.70. Both claim P-11 authority. 0.15 gap. An artifact scoring 0.78 passes under INST-QA-001 but fails under INST-APOGEE-7Q.
2. **AXIS_NAME_COLLISION (HIGH):** References "AXIS floor (any gate): ≥ 0.75." This uses "AXIS" as a name for a floor threshold within this rubric, colliding with INST-AXIS (the canonical 4-invariant 0–100 weakest-link metric). Same name, different instrument.
3. **D6_BINARY_WITH_WEIGHT (MEDIUM):** D6 is binary (1.0 or 0.0) with weight 0.10. If D6 = 0, maximum possible composite = 0.90, which is exactly the P-15 seal threshold. So COLLEEN non-green makes P-15 seal mathematically impossible under this rubric. This interaction is not explicitly documented.

**Required remediation:** Reconcile P-11 threshold with INST-QA-001 (0.85 vs 0.70). Rename or disambiguate "AXIS floor" to avoid collision with INST-AXIS. Document the D6/P-15 mathematical interaction explicitly (if COLLEEN is not FULL GREEN, P-15 seal is impossible under this rubric).

---

### INST-IONIA-13Q — Ionia QA Rubric (A-13, 0Hz Modal Lock)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-IONIA-13Q ||
|| **Canonical name** | Ionia QA Rubric — 0Hz Modal Lock Evaluation ||
|| **Version** | v1.0 ||
|| **Type** | Rubric ||
|| **Classification** | T2 FRAMEWORK — system STATE, not functional agent ||
|| **Canonical location** | `docs/agents/ionia/QA_RUBRIC.md` ||
|| **Authority** | System STATE (modal tuning advisory); agent seat disputed ||
|| **Scope** | 0Hz modal lock evaluation — did Ionia correctly lock to 0Hz when Reson score ≥ 0.75, and correctly withhold when score < 0.75 ||
|| **Formula** | Evaluation dimensions (D-1 through D-7+) — exact composite formula not specified in read range ||
|| **Score range** | 0–1 per dimension (inferred from QA rubric structure) ||
|| **Thresholds** | Reson ≥ 0.75 → lock to 0Hz · Reson < 0.75 → withhold lock ||
|| **Status** | Defined / IDENTITY CONFLICT — agent vs system-state not resolved ||
|| **Implementation** | Rubric defined; operational measurement cycle not confirmed ||
|| **Evidence ref** | File content only; no run binding ||
|| **Supersedes** | Unknown ||
|| **Superseded by** | Unknown ||
|| **Notion cross-reference** | Section 18 (Ionia — A-13 in roster vs 0Hz STATE in formation topology) ||

**Verified defects:**

1. **IDENTITY_AUTHORITY_CONFLICT (HIGH):** Listed as agent `A-13` (QA rubric header, AGENT_ROSTER.md line 55) with a full QA rubric that evaluates agent behavior (lock accuracy, scoring of agent actions). But `AGENT_ARCHITECTURE_ASSESSMENT.md` (lines 22, 126) classifies Ionia as **T2 FRAMEWORK — system STATE, not a functional agent** — "CONCEPTUAL (T2 FRAMEWORK — system STATE, not an agent to instantiate)." An instrument that evaluates an agent's behavior exists for an entity the canonical architecture assessment says is not an agent. The conflict is real on disk: roster + QA rubric treat Ionia as a scorable agent seat; architecture assessment treats Ionia as a conceptual system state.

**Required remediation:** Establish whether Ionia is an agent seat (treat QA rubric as a live instrument) or a system STATE (reclassify QA rubric as a conceptual evaluation document, not a scorable agent instrument). Reconcile AGENT_ROSTER.md, AGENT_ARCHITECTURE_ASSESSMENT.md, and the QA rubric to a single authoritative interpretation. Until resolved, do not use INST-IONIA-13Q as an authoritative agent-evaluation predicate.

---

### INST-ORACLE-20Q — Oracle QA Rubric (A-20)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-ORACLE-20Q ||
|| **Canonical name** | Oracle QA Rubric — Out-of-Roster Agent Evaluation ||
|| **Version** | v1.0 (inferred from artifact set) ||
|| **Type** | Rubric ||
|| **Classification** | T1 PUBLIC (per artifact headers) ||
|| **Canonical location** | `docs/agents/oracle/` (6 artifacts: ORACLE_SPEC.md, ORACLE_KB_SEED.md, ORACLE_PROTOCOL.md, ORACLE_INTEGRATION.md, ORACLE_QA_RUBRIC.md, ORACLE_MEMORY.md) ||
|| **Authority** | Agent Oracle (A-20) per artifact headers; absent from operational roster ||
|| **Scope** | Oracle-specific evaluation dimensions (exact dimensions not read in this pass) ||
|| **Formula** | Not read — QA rubric content not yet extracted ||
|| **Score range** | Not read ||
|| **Thresholds** | Not read ||
|| **Status** | Defined / IDENTITY CONFLICT — A-20 absent from operational roster ||
|| **Implementation** | Full 6-artifact set on disk; operational measurement cycle not confirmed ||
|| **Evidence ref** | File content only; no run binding ||
|| **Supersedes** | Unknown ||
|| **Superseded by** | Unknown ||
|| **Notion cross-reference** | Section 19 (Oracle — A-20 exists in Oracle/topology but outside sovereign roster operational set) ||

**Verified defects:**

1. **IDENTITY_AUTHORITY_CONFLICT (HIGH):** All six Oracle artifacts uniformly identify the agent as `A-20, T1 PUBLIC`. But AGENT_ROSTER.md's stated scope is "T1/T2 operational layer (A-00 through A-13)" with "T3 SOVEREIGN agents (A-14 through A-19) are stubs." **A-20 is absent from the roster** — it falls outside both the operational layer (A-00→A-13) and the T3 stub range (A-14→A-19). The roster's AGENT_ECOSYSTEM_REGISTRY.md (line 6) reinforces: "single source of truth for agent names, roles, and duty assignments across the T1/T2 operational layer (A-00 through A-13)." Oracle/A-20 claims a full agent seat (SPEC + KB_SEED + PROTOCOL + INTEGRATION + QA_RUBRIC + MEMORY) with an ID that the canonical roster does not recognize as operational.

**Required remediation:** Establish whether A-20 is (a) an intended operational agent that the roster should extend to include, (b) an out-of-scope/deprecated agent ID whose artifacts should not be counted in the operational inventory, or (c) a documentation artifact whose scope statement needs updating. Reconcile the Oracle artifact set's A-20 identity with AGENT_ROSTER.md's operational scope. Until resolved, INST-ORACLE-20Q is an on-disk instrument with an unrecognized agent ID — usable as a document but not as an authoritative operational evaluation instrument.

---

### INST-SENTINEL-PHI-5Q — Sentinel-Phi QA Rubric (A-12-φ)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-SENTINEL-PHI-5Q ||
|| **Canonical name** | Sentinel-Phi QA Rubric — Risk-Model QA Evaluation ||
|| **Version** | v1.0 ||
|| **Type** | Rubric ||
|| **Classification** | T1 PUBLIC ||
|| **Canonical location** | `docs/agents/sentinel/SENTINEL_PHI_QA_RUBRIC.md` ||
|| **Authority** | Sentinel-Phi (A-12-φ); variant/derivative relationship to base Sentinel (A-12) NOT established on disk ||
|| **Scope** | Risk-model QA evaluation — 5 dimensions (D1–D5), weights 0.35/0.25/0.20/0.15/0.05 ||
|| **Formula** | `Sentinel-Phi QA Score = D1×0.35 + D2×0.25 + D3×0.20 + D4×0.15 + D5×0.05` (line 60 of SENTINEL_PHI_QA_RUBRIC.md) ||
|| **Score range** | 0.00–1.00 (weights sum to 1.00) ||
|| **Thresholds** | Not read in this pass (QA rubric has pass thresholds per dimension) ||
|| **Status** | Defined / IDENTITY CONFLICT — A-12-φ vs A-12 relationship unverified on disk ||
|| **Implementation** | QA rubric + 4 companion artifacts (PROTOCOL, INTEGRATION, MEMORY, UPGRADE) on disk; operational measurement cycle not confirmed ||
|| **Evidence ref** | File content only; no run binding ||
|| **Supersedes** | Unknown ||
|| **Superseded by** | Unknown ||
|| **Notion cross-reference** | Section 20 (Sentinel-Phi — `variant_of → Sentinel` claimed but A-12 vs A-12-φ unresolved) ||

**Verified defects:**

1. **IDENTITY_AUTHORITY_CONFLICT (HIGH):** Sentinel-Phi exists as a distinct on-disk agent with ID `A-12-φ` and five artifacts. Base Sentinel has ID `A-12`. The two IDs are structurally similar (A-12 vs A-12-φ) suggesting a variant/derivative relationship. **However, no on-disk language establishes `variant_of → Sentinel`**: no `variant_of`, `derived_from`, `supersedes`, `parent`, or `base` field in any Sentinel-Phi artifact; no cross-reference from base Sentinel artifacts (SPEC.md, KB.md, QA_RUBRIC.md) to Sentinel-Phi. The Notion SSOT's disposition states "`variant_of → Sentinel` is established," but this claim is NOT supported by on-disk evidence as of this verification. The relationship between A-12 and A-12-φ remains unresolved.
2. **STRUCTURAL_DISTINCTNESS (MEDIUM):** Sentinel-Phi's QA rubric (D1–D5, weights 0.35/0.25/0.20/0.15/0.05) is structurally different from base Sentinel's QA rubric (different dimension count and weights). If Sentinel-Phi is a variant of base Sentinel, a variant with a different QA rubric structure raises the question of whether the variant is a specialized sub-type or an independently-scoped instrument.

**Required remediation:** Establish the variant/derivative relationship explicitly in the artifacts (add `variant_of: Sentinel (A-12)` or equivalent to Sentinel-Phi's metadata, or document base Sentinel's relationship to Sentinel-Phi), OR establish that Sentinel-Phi is an independent agent seat (A-12-φ as a distinct entity, with the naming convention `SENTINEL_PHI_*` clarified as a directory/convention choice rather than a lineage claim). Reconcile the A-12 / A-12-φ ID space. The Notion SSOT's "variant_of established" claim should be verified against on-disk evidence — if the SSOT has a Notion-side record establishing the variant relationship that is not yet reflected in the repo artifacts, that record should be cited as the establishing authority.

---

### INST-RESON-4Q — Reson Harmonic Scoring Rubric (4 Sub-Dimensions)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-RESON-4Q ||
|| **Canonical name** | Reson Harmonic Scoring Rubric — 4 Sub-Dimension Weighted Average ||
|| **Version** | v1.0 (Seeded S073, 2026-06-29) ||
|| **Type** | Rubric / Scoring Instrument ||
|| **Classification** | T1 PUBLIC ||
|| **Canonical location** | `docs/agents/reson/QA_RUBRIC.md` (primary) + `docs/agents/reson/KB.md` + `docs/agents/reson/RESON_KB.md` + `docs/agents/reson/PROTOCOL.md` + `docs/agents/reson/MEMORY.md` ||
|| **Authority** | Reson (Augmenter 1 / Harmonic Integrity Monitor) ||
|| **Scope** | Harmonic evaluation — 4 sub-dimensions (H1–H4), weighted-average composite ||
|| **Formula** | `composite = H1×0.30 + H2×0.25 + H3×0.25 + H4×0.20` (weights sum to 1.00) ||
|| **Score range** | 0.00–1.00 (each sub-dimension 0–1, weights sum to 1.00) ||
|| **Thresholds (three distinct predicates, all using the word "threshold")** | (1) **AX-06 gate:** ≥ 0.75 — from KB.md line 47/51, RESON_KB.md line 51, MEMORY.md line 13. Score ≥ 0.75 routes to Apogee as Pillar C PASS; < 0.75 routes as FAIL. (2) **Seal floor:** ≥ 0.85 — from KB.md line 47, QA_RUBRIC.md line 69. Floor for seal eligibility. (3) **Ionian sustained target:** ≥ 0.90 — from KB.md line 47, PROTOCOL.md line 50, QA_RUBRIC.md lines 69/78. Target for sustained Ionian mode; scores below 0.90 generate advisories, not hard blocks (exception: Phrygian dissonance < 0.70 blocks seal per PROTOCOL.md line 59). ||
|| **Blocking behavior** | Non-blocking by default (scores below 0.90 → advisories); Phrygian dissonance < 0.70 → hard block on seal (PROTOCOL.md line 59) ||
|| **Status** | Defined / THRESHOLD-SCOPE CONFLICT — three predicates share the word "threshold" ||
|| **Implementation** | Rubric defined; operational measurement cycle not confirmed ||
|| **Evidence ref** | File content only; no run binding ||
|| **Supersedes** | Unknown ||
|| **Superseded by** | Unknown ||
|| **Notion cross-reference** | Section 17 (Reson — 0.75, 0.85, and 0.90 treated as potentially different predicates) ||

**Verified defects:**

1. **THRESHOLD_SCOPE_CONFLICT (HIGH):** Three distinct predicates are all referred to with the generic word "threshold" across the Reson artifacts:
   - 0.75 = AX-06 gate (Apogee Pillar C routing pass/fail)
   - 0.85 = seal floor (seal eligibility)
   - 0.90 = Ionian sustained target (quality target, advisory below)

   Policy language that says "Reson score must reach [X] for seal" is ambiguous: does X mean the AX-06 gate (0.75), the seal floor (0.85), or the target (0.90)? The three predicates are structurally different (routing gate vs. eligibility floor vs. quality target) and should not be treated as one interchangeable threshold. Verified from: KB.md lines 47/51, RESON_KB.md lines 51/57/58, MEMORY.md line 13, PROTOCOL.md lines 50/59, QA_RUBRIC.md lines 69/78.

2. **POLICY_LANGUAGE_AMBIGUITY (MEDIUM):** The same word "threshold" is used for all three predicates in different artifacts without distinguishing them by predicate name. This makes cross-artifact policy statements ambiguous unless each is read in the specific context of the artifact that contains it.

**Required remediation:** Renaming/labeling: label each predicate by its distinct name (AX-06 gate, seal floor, Ionian sustained target) rather than by the generic word "threshold." Reconcile policy language so that seal decisions cite the seal floor (0.85) and routing decisions cite the AX-06 gate (0.75). Do not collapse the three predicates into one interchangeable threshold. Until reconciled, any policy statement citing a single "Reson threshold" is ambiguous and must be disambiguated by context.

---

### INST-KAPPA — KAPPA Composite (5-Dimensional Evaluator)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-KAPPA ||
|| **Canonical name** | KAPPA Composite — 5-Dimensional Evaluator ||
|| **Version** | Unknown — not located as standalone document in current DGAF-Framework tree ||
|| **Type** | Metric/Score ||
|| **Classification** | TBD ||
|| **Canonical location** | TBD — referenced in finding 11 and in Notion SSOT; not found in `docs/`, `components/`, or GitHub repos checked ||
|| **Authority** | TBD ||
|| **Scope** | Separate 5-dimensional evaluator — must not be confused with AXIS/11Q/Harmonic scores ||
|| **Formula** | TBD — not accessible ||
|| **Score range** | TBD ||
|| **Thresholds** | TBD ||
|| **Status** | UNLOCATED — requires discovery ||
|| **Implementation** | TBD — `components/evaluate_router.py` computes a KAPPA-routed weighted average over 5 dimensions (accuracy, false_blocked, adversarial, ambiguous, malformed) per Notion SSOT section 14, but the canonical KAPPA rubric document is not located ||
|| **Evidence ref** | `components/evaluate_router.py` (score computation present) — canonical rubric source unknown ||
|| **Notion cross-reference** | Section 14 (score-family separation is incomplete — KAPPA-routed weighted average) ||

**Verified defects:**

1. **REGISTRY_CONTROL_NEEDED (MEDIUM/HIGH):** Named in finding 11 and in Notion SSOT as "a separate five-dimensional evaluator that must not be confused with AXIS/11Q/Harmonic scores." The score computation exists in `components/evaluate_router.py` but the canonical rubric document was not located in the current tree. If KAPPA exists as a document elsewhere (dgaf-ops, ndrorchestration/ndrorchestration, or Gold-star-standards), it needs an instrument ID and must be kept distinct from AXIS/11Q/Harmonic in the registry.

**Required remediation:** Locate the KAPPA canonical document (if it exists) in the repo or other ndrorchestration repos. If found, assign instrument ID, add to registry, and ensure non-ambiguous naming. If not found, document as unresolved reference. Do not allow "composite score" to be mistaken for a governance score without explicit instrument ID binding.

---

### INST-GATE-SPECS — Yggdrasil Gate Stack — Master Specification (Historical)

|| Field | Value ||
||---|---|---|
|| **Instrument ID** | INST-GATE-SPECS ||
|| **Canonical name** | GATE_SPECS.md — Yggdrasil Gate Stack Master Specification ||
|| **Version** | SYS-UPDATE-v53.1 (HISTORICAL) ||
|| **Type** | Historical / Reference ||
|| **Classification** | T2 FRAMEWORK (historical) ||
|| **Canonical location** | `docs/gates/GATE_SPECS.md` ||
|| **Authority** | Agent Amethyst (historical QA Orchestrator); Architect: Hensel, Andrew Vance ||
|| **Scope** | Historical gate hierarchy: 1-1-1-1 Gate, 11Q Framework, Telescopic Lens, Acoustic Time Gates, operational & defensive gates ||
|| **Formula** | N/A — historical reference ||
|| **Status** | HISTORICAL / LEGACY — explicitly not authoritative for current state ||
|| **Implementation** | N/A — historical ||
|| **Evidence ref** | §1 current-state boundary disclaimer present ||
|| **Notion cross-reference** | Section 2 (Second-order agent-architecture reconciliation — GATE_SPECS as seed) ||

**Verified defects:** None — correctly self-identifies as HISTORICAL/LEGACY with current-state boundary disclaimer. This is the correct pattern for preserved historical instruments.

**Required remediation:** None. Should be cross-referenced by any instrument claiming lineage to it, with explicit notation that the lineage is historical, not current.

---

## 2. Cross-Instrument Conflicts (consolidated)

These are the conflicts that prevent any instrument from being treated as unambiguous canonical authority without reconciliation:

|| Conflict ID | Instruments involved | Nature | Severity | Resolution status ||
||---|---|---|---|---|---|
|| CX-01 | INST-QA-001 vs INST-APOGEE-7Q | P-11 threshold: 0.70 vs 0.85 | HIGH | Unresolved ||
|| CX-02 | INST-QA-001 vs INST-GATE-11Q | Identity collision: 11Q rubric vs 11Q deployment gate — different instruments, same name | HIGH | Unresolved ||
|| CX-03 | INST-AXIS vs INST-APOGEE-7Q | AXIS lineage mismatch: 4×0–100 weakest-link vs 7×0–1 weighted sum — same cited source, different implementation | HIGH | Unresolved ||
|| CX-04 | INST-HQ-META vs itself | Harmonic Quintet composite 0.844 not reproducible from displayed scores | HIGH | Unresolved ||
|| CX-05 | INST-AHG-ARCH vs INST-AHG-STAB | Stability Index weight sum: 1.00 vs 0.80 — companion documents disagree | HIGH | Unresolved ||
|| CX-06 | INST-RESON-4Q vs INST-QA-001 vs INST-APOGEE-7Q | Reson threshold-scope conflict: AX-06 gate ≥ 0.75 (KB.md, RESON_KB.md, MEMORY.md) vs seal floor ≥ 0.85 (KB.md, QA_RUBRIC.md) vs Ionian sustained target ≥ 0.90 (KB.md, PROTOCOL.md, QA_RUBRIC.md); plus cross-instrument P-15 threshold: 0.75 in Amethyst QA rubric seal pre-condition vs 0.85 in Reson QA rubric seal floor | HIGH | Unresolved ||
|| CX-07 | INST-AXIS vs INST-APOGEE-7Q | AXIS name collision: canonical metric vs QA rubric's "AXIS floor" reference | MEDIUM | Unresolved ||
|| CX-08 | INST-QA-001 internal | Weights sum to 1.50, formula divides by 11 — 0–1 range unreachable under literal execution | HIGH | Unresolved (mathematical) ||
|| CX-09 | INST-HQ-META internal | Row-stochasticity claim false (APG row = 0.80) — convergence claim has true conclusion but wrong justification | HIGH | Unresolved ||
|| CX-10 | INST-APOGEE-7Q internal | D6 binary + weight 0.10 → COLLEEN non-green makes P-15 seal mathematically impossible — not explicitly documented | MEDIUM | Unresolved ||
|| CX-11 | INST-IONIA-13Q internal | Identity conflict: agent seat A-13 vs system STATE — QA rubric evaluates an agent the architecture assessment says does not exist | HIGH | Unresolved ||
|| CX-12 | INST-ORACLE-20Q internal | Identity conflict: A-20 artifact set on disk vs A-20 absent from operational roster (A-00→A-13 + T3 stubs A-14→A-19) | HIGH | Unresolved ||
|| CX-13 | INST-SENTINEL-PHI-5Q internal | Identity conflict: A-12-φ distinct on disk from A-12; `variant_of → Sentinel` claim NOT supported by on-disk evidence | HIGH | Unresolved ||
|| CX-14 | INST-AXIS vs INST-APOGEE-7Q (name collision variant) | "AXIS floor ≥ 0.75" in Apogee rubric collides with INST-AXIS as both cited source and score name | MEDIUM | Unresolved ||

---

## 3. Instrument Registry Schema (as called for by Notion SSOT §9)

The Notion SSOT already upgraded the registry schema to require these fields per instrument. This matrix implements that schema:

|| Field | Definition ||
||---|---|
|| `instrument_id` | Unique canonical handle (INST-XXX-NNN) ||
|| `instrument_type` | Rubric / Gate / Standard / Checklist / Acceptance Test / Metric-Score / Protocol / Attestation / Evidence-Report / Registry-Index / Template / Historical Lineage ||
|| `canonical_source` | File path or record ID of the authoritative source ||
|| `version` | Version identifier ||
|| `formula` | Scoring formula, algorithm, or decision procedure ||
|| `score_range` | Nominal range of scores/outputs ||
|| `thresholds` | Pass/fail thresholds, gate predicates, or decision boundaries ||
|| `authority` | Who owns/authorizes this instrument ||
|| `binding_strength` | Advisory / Expected / Gating / Sovereign ||
|| `scope` | What the instrument governs or evaluates ||
|| `implementation` | Component deployment status vs. operational validation status (distinct fields) ||
|| `evidence_ref` | Run ID, artifact binding, or citation for any asserted score/result ||
|| `status` | Epistemic status: Defined / Implemented / Tested / Verified / Validated / Adopted / Authorized / Historical / Superseded / Blocked / Fail-Closed / Not Executed / Unverified ||
|| `supersedes` | Instrument(s) this replaces, if any ||
|| `superseded_by` | Instrument(s) that replace this, if any ||
|| `duplicate_alias_names` | Other names that refer to this instrument (with disambiguation notes) ||
|| `last_verified` | When the instrument's content/formula was last directly checked ||
|| `audit_notes` | Known defects, open questions, reconciliation requirements ||

---

## 4. What this matrix establishes — and what it deliberately does not

**Establishes:**

- Unambiguous instrument IDs for 13 instruments (11 located + 2 unlocated: KAPPA canonical doc, Oracle QA rubric formula unextracted).
- Explicit disconfirmation of 14 cross-instrument/internal conflicts with verbatim source references.
- Computational verification of the Harmonic Quintet matrix claims (ρ = 0.959114, APG row = 0.80) and the QA_RUBRIC weight defect (1.50).
- On-disk verification of all six Notion SSOT contradiction dispositions (Ionia, Oracle, Reson, Sentinel-Phi, Apogee AXIS, Core DGAF) — with one correction: the Sentinel-Phi "variant_of established" claim is NOT supported by on-disk evidence.
- **Final reclassification verified on disk:** 5 of 6 records are internally coherent rubrics whose remaining issues are external dependencies (authority, lineage, identity, scope-binding). Only Core DGAF (RUB-CORE-001) is a genuine intrinsic contradiction — its published 11Q weights sum to 1.50 while the formula divides by 11, making the stated thresholds mathematically unreachable under literal execution.
- The required remediation for each defect — stated explicitly, not silently normalized.
- Cross-reference to the Notion SSOT for every finding, confirming independent dual-source validation where both exist.

**Deliberately does NOT:**

- Promote any score to authoritative evidence. Every instrument is "Defined / NOT verified" unless it has an evidence_ref with a run binding.
- Resolve any conflict by fiat. Each conflict is listed as "Unresolved" with the resolution requirements stated.
- Infer missing KAPPA content. INST-KAPPA is listed as UNLOCATED with its formula/score_range/thresholds marked TBD.
- Claim that any instrument is implemented-and-validated. AHG has components deployed but validation is explicitly pending live-trace evidence.
- Assert a canonical agent count or seat count. The instrument matrix is instrument-identity, not agent-identity.
- Assert that the Notion SSOT's "variant_of → Sentinel" claim is on-disk verified — it is flagged as a verification gap.

---

## 5. Next reconciliation steps (in priority order)

1. **QA_RUBRIC.md weight reconciliation (INST-QA-001):** Authoritative decision on weight semantics. This is the highest-impact defect because INST-QA-001 is the "universal" rubric and its formula is mathematically broken under literal execution. All agent QA rubrics, gate records citing P-11, and any score asserting 11Q compliance depend on this.
2. **P-11 disambiguation (CX-01 + CX-02):** Assign distinct instrument IDs for the 11Q rubric and the 11Q deployment gate. Resolve the 0.70 vs 0.85 threshold conflict with an authoritative designation.
3. **AXIS reconciliation (CX-03 + CX-07 + CX-14):** Determine whether INST-APOGEE-7Q is an AXIS implementation or a separate metric mislabeled as AXIS. Disambiguate the "AXIS" name in the Apogee rubric. Add explicit bridge specification or correction.
4. **AHG weight reconciliation (CX-05):** Determine whether stability index weights sum to 1.00 or 0.80. Authoritatively state in both documents.
5. **Harmonic Quintet matrix correction (INST-HQ-META):** Correct the APG row or the row-stochasticity claim. Re-derive or disclose the 0.844 composite formula.
6. **P-15 Reson threshold resolution (CX-06):** Designate whether Reson seal floor is 0.75 or 0.85. Label each predicate by name. Document which artifact controls.
7. **Ionia identity reconciliation (CX-11):** Establish agent-vs-system-state for A-13. Reconcile roster, architecture assessment, and QA rubric.
8. **Oracle roster reconciliation (CX-12):** Establish whether A-20 is an intended operational agent, an out-of-scope artifact, or a documentation gap. Extend or clarify the roster.
9. **Sentinel-Phi variant relationship (CX-13):** Establish `variant_of → Sentinel` explicitly in artifacts, or classify Sentinel-Phi as independent. Reconcile A-12 / A-12-φ ID space.
10. **KAPPA location (INST-KAPPA):** Locate canonical document or document as unresolved reference.
11. **Instrument-ontology operationalization:** Once instruments have reconciled IDs, formulas, and thresholds, agent souls and gate records should reference these IDs rather than ambiguous shorthand.

---

## 6. Notion SSOT cross-validation summary

This matrix was cross-validated against the Notion SSOT (`MASTER RUBRIC REGISTRY & AUDIT — 2026-09-04`, fetched 2026-09-04T08:25:34Z). All six contradiction dispositions in the SSOT were independently verified on disk:

| Rubric | SSOT disposition | On-disk verification | Match? |
|---|---|---|---|
| Apogee AXIS | Specification conflict — distinct 7D QA rubric, not canonical AXIS | 7D weighted-sum vs 4×0–100 weakest-link confirmed | ✅ Match |
| Core DGAF | Mathematical defect — weights 1.50, formula ÷ 11, threshold unreachable | 1.50 weight sum + 1/11 formula + unreachable thresholds confirmed | ✅ Match |
| Ionia | Identity/authority conflict — A-13 roster vs 0Hz STATE | A-13 QA rubric + AGENT_ROSTER vs T2 system STATE assessment confirmed | ✅ Match |
| Oracle | Identity/authority conflict — A-20 outside roster operational set | A-20 across 6 artifacts vs A-00→A-13 + A-14→A-19 roster confirmed | ✅ Match |
| Reson | Threshold-scope conflict — 0.75/0.85/0.90 as potentially different predicates | Three distinct predicates confirmed on disk | ✅ Match |
| Sentinel-Phi | `variant_of → Sentinel` established, A-12 vs A-12-φ unresolved | A-12-φ on disk confirmed; `variant_of` language NOT found on disk | ⚠️ Partial — disposition's first clause not on-disk verified |

One correction is recorded: the SSOT's Sentinel-Phi disposition states "`variant_of → Sentinel` is established," but no on-disk artifact in `docs/agents/sentinel/` contains `variant_of`, `derived_from`, `supersedes`, `parent`, or `base` language linking Sentinel-Phi (A-12-φ) to base Sentinel (A-12). The "A-12 vs A-12-φ unresolved" half is verified; the "variant_of established" half is flagged as a verification gap requiring either on-disk artifact addition or citation of the establishing authority (possibly a Notion-side record not yet reflected in repo artifacts).

---

## 7. Six Active Rubric Contradictions — cross-reference to Decision Log

See `docs/evaluation/SIX_ACTIVE_RUBRIC_CONTRADICTIONS_RECONCILIATION_DECISION_LOG_2026-09-04.md` for the detailed per-contradiction reconciliation record, including verbatim source lines, on-disk evidence citations, and explicit closure conditions for each of the six contradictions.

This matrix provides the instrument-ID layer (INST-XXX-NNN) for each contradiction instrument. The Decision Log provides the disposition, evidence, and closure-condition layer.

|| Contradiction | Instrument ID | Decision Log section |
||---|---|---|
|| Apogee AXIS | INST-APOGEE-7Q / INST-AXIS | §1 |
|| Core DGAF | INST-QA-001 | §2 |
|| Ionia | INST-IONIA-13Q | §3 |
|| Oracle | INST-ORACLE-20Q | §4 |
|| Reson | INST-RESON-4Q | §5 |
|| Sentinel-Phi | INST-SENTINEL-PHI-5Q | §6 |

---

Classification: T1 PUBLIC — instrument identity and defect registry, not a claim of authoritative scores or resolved conflicts. All statuses are stated explicitly; no silent normalization has been performed. Scientific boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
