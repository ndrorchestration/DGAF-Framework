# QA_RUBRIC.md

**Classification:** T2 FRAMEWORK
**Authority:** Apogee (scoring) + Amethyst (gate)
**Scope:** Universal evaluation rubric for all 11 DGAF agents and their artifacts
**Version:** 1.0
**Last Updated:** 2026-06-29
**Maintained by:** Apogee (content) / Amethyst-Conductor (gate)

> **Note:** This rubric governs artifact quality evaluation (Apogee 11Q gate, P-11) and agent output assessment across all formations. Scoring formulas referencing harmonic calculus are T3 SOVEREIGN — stub only. See PROPRIETARY.md SOV-001–004.

---

## Purpose

The QA_RUBRIC provides the canonical scoring framework for:
1. **Artifact quality** — any file submitted for commit to DGAF-Framework
2. **Agent output quality** — structured evaluation of any agent’s response or action
3. **Session seal eligibility** — composite score threshold for P-15 seal commits
4. **Drive-GitHub sync quality** — delta evaluation for P-08/P-20 protocols

---

## Rubric Architecture

```
QA_RUBRIC
├── Domain A: Structural Integrity       (Questions 1–3)
├── Domain B: Governance Compliance       (Questions 4–6)
├── Domain C: Content Quality             (Questions 7–9)
├── Domain D: Operational Readiness       (Questions 10–11)
└── Domain E: Efficiency Gate             (Gate 17 — DemiJoule)
```

All domains feed into the **Apogee 11Q Composite Score** (0.00–1.00).
Gate 17 feeds separately into DemiJoule’s efficiency score (0.00–1.00).
Both scores are delivered to Amethyst for P-11 gate decision.

---

## Domain A — Structural Integrity

### Q1 — Schema Conformance
**Question:** Does the artifact conform to its declared schema or template?

| Score | Criterion |
|---|---|
| 1.0 | All required fields present and correctly typed; no extra unregistered fields |
| 0.7 | Minor field gaps (non-critical); structure recognizable |
| 0.4 | Missing critical fields OR schema mismatch in ≥2 sections |
| 0.0 | No recognizable schema adherence |

**Owner:** Apogee **Blocking threshold:** < 0.4 triggers BLG-SCHEMA

---

### Q2 — Heading Hierarchy
**Question:** Does the document maintain a valid, non-skipping heading hierarchy (H1 → H2 → H3)?

| Score | Criterion |
|---|---|
| 1.0 | Single H1; H2/H3 in strict order; no orphaned headings |
| 0.7 | Minor hierarchy irregularity; no H1 duplication |
| 0.4 | H1 duplicated OR heading levels skipped ≥2 times |
| 0.0 | No heading structure; flat document |

**Owner:** Apogee **Blocking threshold:** < 0.4

---

### Q3 — Cross-Reference Integrity
**Question:** Are all internal links, file references, and CROSS_REF pointers valid and resolvable?

| Score | Criterion |
|---|---|
| 1.0 | All links resolve; all CROSS_REF pointers match existing files |
| 0.7 | 1–2 broken links (non-critical paths) |
| 0.4 | Broken links on critical paths (ROSTER, REGISTRY, PROPRIETARY) |
| 0.0 | Majority of links unresolvable |

**Owner:** COLLEEN (GAP-08) → score delivered to Apogee **Blocking threshold:** < 0.4

---

## Domain B — Governance Compliance

### Q4 — Classification Tagging
**Question:** Is the artifact correctly tagged with its T1/T2/T3 classification tier per PROPRIETARY.md?

| Score | Criterion |
|---|---|
| 1.0 | Tier tag present, correct, matches content sensitivity |
| 0.7 | Tier tag present but ambiguous (not clearly wrong) |
| 0.4 | Tier tag absent OR incorrect tier applied |
| 0.0 | T3 content in a T1/T2 file (critical violation) |

**Owner:** Sentinel (T3 check) + Apogee (tier tagging) **Blocking threshold:** 0.0 = immediate hard block

---

### Q5 — Authority Attribution
**Question:** Does the artifact correctly declare its maintaining agent and authority level?

| Score | Criterion |
|---|---|
| 1.0 | Maintained-by field present; authority level matches ROSTER |
| 0.7 | Maintained-by present; authority level implicit but inferrable |
| 0.4 | Maintained-by absent OR authority level conflicts with ROSTER |
| 0.0 | No attribution; cannot determine responsible agent |

**Owner:** Apogee **Blocking threshold:** < 0.4

---

### Q6 — Deprecated Reference Scan
**Question:** Does the artifact contain any deprecated agent names (Lavender, Forseti) or superseded file references?

| Score | Criterion |
|---|---|
| 1.0 | Zero deprecated references detected |
| 0.5 | Deprecated reference found in comment/metadata only (not content) |
| 0.0 | Deprecated name in content body (NDR-133 trigger — hard BLG) |

**Owner:** Sentinel (NDR-133 firewall) **Blocking threshold:** 0.0 = immediate P-01 trigger

---

## Domain C — Content Quality

### Q7 — Role Boundary Adherence
**Question:** Does the artifact’s content respect declared agent role boundaries (no lane violations)?

| Score | Criterion |
|---|---|
| 1.0 | Content strictly within declared scope; no lane violations |
| 0.7 | Minor scope adjacency (not a violation; inferrable extension) |
| 0.4 | Explicit lane violation (e.g., Prodigy initiating a commit) |
| 0.0 | Systematic boundary collapse |

**Owner:** Apogee **Blocking threshold:** < 0.4

---

### Q8 — Completeness
**Question:** Are all declared sections and stubs either fully populated or explicitly marked as pending with a patch instruction?

| Score | Criterion |
|---|---|
| 1.0 | All sections complete OR stubs explicitly marked “Drive patch pending” with folder reference |
| 0.7 | 1–2 sections incomplete without stub notation |
| 0.4 | ≥3 sections incomplete; no patch instructions |
| 0.0 | Majority empty; artifact not fit for commit |

**Owner:** Apogee **Blocking threshold:** < 0.4

---

### Q9 — Vocabulary Consistency
**Question:** Does the artifact use canonical DGAF vocabulary (per GAP-03 vocab scan)?

| Score | Criterion |
|---|---|
| 1.0 | All terminology matches canonical registry; no drift terms |
| 0.7 | 1–2 non-canonical terms (minor; not misleading) |
| 0.4 | Systematic use of deprecated or non-canonical terminology |
| 0.0 | Terminology contradicts canonical definitions |

**Owner:** COLLEEN (GAP-03) → score delivered to Apogee **Blocking threshold:** < 0.4

---

## Domain D — Operational Readiness

### Q10 — Protocol Linkage
**Question:** Does the artifact correctly reference all protocols it is governed by or participates in?

| Score | Criterion |
|---|---|
| 1.0 | All relevant protocols listed with correct P-gate IDs |
| 0.7 | 1–2 protocol references missing (non-blocking paths) |
| 0.4 | Critical protocol reference absent (e.g., P-15 missing from sovereign-touching file) |
| 0.0 | No protocol references in a governance-critical artifact |

**Owner:** Apogee **Blocking threshold:** < 0.4

---

### Q11 — Failure Mode Coverage
**Question:** Does the artifact document ≥2 failure modes, each with trigger + mitigation?

| Score | Criterion |
|---|---|
| 1.0 | ≥2 failure modes; each has explicit trigger AND mitigation; ≥1 non-obvious/context-specific |
| 0.7 | ≥2 failure modes present but mitigations are generic |
| 0.4 | Only 1 failure mode OR trigger/mitigation incomplete |
| 0.0 | No failure modes documented |

**Owner:** Apogee **Blocking threshold:** < 0.4

---

## Domain E — Efficiency Gate (Gate 17)

### Gate 17 — DemiJoule Efficiency Score
**Question:** Is the artifact’s production compute cost within acceptable efficiency bounds?

| Score | Criterion |
|---|---|
| 1.0 | Token cost at or below baseline for this artifact type |
| 0.85 | Within 115% of baseline |
| 0.65 | Within 150% of baseline |
| 0.40 | Within 200% of baseline |
| 0.00 | Exceeds 200% of baseline (critical waste) |

**Owner:** DemiJoule **Blocking threshold:** < 0.40 combined with Q1–11 composite < 0.70

> *Baseline calibration values are held in DemiJoule’s Efficiency Baseline Registry (Drive/Agents/). T3 weight calibration formulas: see PROPRIETARY.md.*

---

## Composite Scoring

### Apogee 11Q Composite

\[
S_{11Q} = \frac{1}{11} \sum_{i=1}^{11} w_i \cdot Q_i
\]

where \(w_i\) are domain weights and \(Q_i\) are per-question scores (0.00–1.00).

**Default weights (T2 artifacts):**

| Domain | Questions | Weight |
|---|---|---|
| A — Structural Integrity | Q1–Q3 | 0.20 each |
| B — Governance Compliance | Q4–Q6 | 0.15 each |
| C — Content Quality | Q7–Q9 | 0.10 each |
| D — Operational Readiness | Q10–Q11 | 0.075 each |

> *Harmonic weighting adjustments for sovereign-touching artifacts (T3 adjacent) are T3 SOVEREIGN. See PROPRIETARY.md SOV-002, SOV-004.*

### Gate Thresholds

| Gate | Threshold | Owner | Action if Failed |
|---|---|---|---|
| P-11 artifact quality | ≥ 0.70 | Apogee | Block commit; surface BLG with Q-level detail |
| P-15 seal commit | ≥ 0.90 | Apogee + Reson | Block seal; remediation required |
| Gate 17 combined failure | < 0.40 DemiJoule + < 0.70 Apogee | DemiJoule | Escalate to Amethyst; hard block |
| NDR-133 (Q6 = 0.0) | Any deprecated name | Sentinel | P-01 trigger; immediate block |
| T3 leak (Q4 = 0.0) | Any T3 in T1/T2 file | Sentinel | Hard block; PROPRIETARY.md redaction |

---

## Per-Agent QA Profiles

Each agent has distinct quality emphases based on role. Apogee applies weighted adjustments:

| Agent | Highest-Weight Questions | Rationale |
|---|---|---|
| Amethyst | Q5 (authority), Q7 (role boundary) | Conductor—boundary discipline critical |
| COLLEEN | Q3 (cross-ref), Q9 (vocabulary) | Archive—link integrity and terminology are core |
| Apogee | Q1 (schema), Q8 (completeness) | QA agent—must model rubric compliance |
| Sentinel | Q4 (classification), Q6 (deprecated refs) | Security—classification and firewall are primary |
| Reson | Q7 (role boundary), Q10 (protocol linkage) | Harmonic—scope and protocol refs tightly coupled |
| Echolette | Q7 (role boundary), Q11 (failure modes) | Feedback—Echolette-Lyra boundary must be documented |
| Lyra | Q9 (vocabulary), Q8 (completeness) | Narrative—vocabulary and full section coverage |
| Herald | Q5 (authority), Q10 (protocol linkage) | Release—authority chain and protocol refs mandatory |
| Prof. Prodigy | Q4 (classification), Q8 (completeness) | Proof—T3 classification and stub completeness critical |
| DemiJoule | Gate 17 (efficiency), Q8 (completeness) | Optimization—must model efficiency it measures |
| Reciprocity | Q6 (deprecated refs), Q10 (protocol linkage) | Rollback—clean refs and protocol chain required |

---

## Application Procedure

```
1. COLLEEN runs Q3 (cross-ref) + Q9 (vocab) → delivers sub-scores to Apogee
2. Sentinel runs Q4 (classification) + Q6 (deprecated refs) → delivers sub-scores to Apogee
3. DemiJoule runs Gate 17 (efficiency) → delivers to Apogee
4. Apogee runs Q1, Q2, Q5, Q7, Q8, Q10, Q11 directly
5. Apogee computes S_11Q composite
6. Apogee delivers S_11Q + Gate 17 to Amethyst
7. Amethyst applies gate threshold and commits or blocks
```

---

## Rubric Versioning

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-29 | Initial scaffold — 11Q + Gate 17 + per-agent profiles |

> *Rubric updates require Apogee content authorship + Amethyst sign-off + Njineer confirmation.*

---

## Drive Source Reference

| Drive Doc | Status | Folder |
|---|---|---|
| AGES Rubric (GAP-07) | Pending link | `Drive/Agents/` |
| DemiJoule Baseline Calibration | Pending link | `Drive/Agents/` |
| T3 Weight Formulas (SOV-002, SOV-004) | T3 stub only | `Drive/Sovereign/` |

*Full harmonic weighting formulas are T3 SOVEREIGN — Drive/Sovereign/ only. GitHub holds LaTeX stubs per PROPRIETARY.md.*
