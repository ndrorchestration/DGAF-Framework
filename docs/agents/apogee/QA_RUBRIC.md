# QA Rubric — Agent Apogee

**Agent:** Agent Apogee  
**Role Domain:** Evidence Governance  
**Formation:** Trio / Quintet  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Apogee's evidence scoring, source validation, and DGAF/PMP compliance verification outputs. Apogee is the artifact quality oracle — this rubric governs how Apogee itself is evaluated.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **11Q Gate Accuracy** | 25% | ≥ 0.90 | Each of the 11 questions scored correctly against artifact content. No false positives (passing a failing artifact). |
| D2 | **Source Validation Rigor** | 20% | ≥ 0.85 | Citation-to-claim traceability. No hallucinated sources. External refs verified. |
| D3 | **DGAF/PMP Compliance Check** | 20% | ≥ 0.88 | Framework alignment verified against current DGAF canon. PMP artifact structure validated. |
| D4 | **CERTIFICATION_INDEX Maintenance** | 15% | ≥ 0.90 | Index updated at every gate event. No stale entries. Schema valid. |
| D5 | **GAP-07 Content Ownership** | 10% | ≥ 0.85 | AGES content (GAP-07) complete, versioned, and Drive-synced. |
| D6 | **Score Traceability** | 10% | ≥ 0.88 | Every score output includes dimension breakdown + rationale. No opaque composite-only scores. |

**Composite Pass:** ≥ 0.87 routine; ≥ 0.92 for P-15 seal gate inputs.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **False positive gate pass** | 11Q returns PASS on artifact with D1 < 0.70 | Hard re-score; Amethyst holds commit pending re-evaluation |
| F2 | **Stale CERTIFICATION_INDEX** | Gate event occurs without index update | COLLEEN flags at P-02 of next session; Apogee must retroactively update |
| F3 | **Circular citation** *(non-obvious)* | Apogee validates a source that itself cites an Apogee prior output | Sentinel flags circular reference; external source required |

---

## Gate Ownership

| Gate | Apogee Role |
|------|-------------|
| P-11 | 11Q gate — primary owner; delivers composite score to Amethyst |
| P-15 | Evidence seal confirmation |

---

*Rubric authority: Amethyst-Conductor.*
