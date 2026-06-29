# QA Rubric — Agent DemiJoule

**Agent:** Agent DemiJoule  
**Role Domain:** Energy + Optimization  
**Formation:** Extended  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for DemiJoule's token cost analysis, compute efficiency gating, and quality-gating weight calibration. DemiJoule is advisory — efficiency scores inform but do not veto unless combined with Apogee 11Q failure.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **Token Cost Accuracy** | 30% | ≥ 0.88 | Token estimates within ±15% of actual usage. Estimates traceable to model pricing at time of analysis. |
| D2 | **Compute Efficiency Gate (P-11 Gate 17)** | 25% | ≥ 0.85 | Efficiency score at P-11 gate 17 reflects actual compute load. No over-reporting of efficiency. |
| D3 | **Weight Calibration Quality** | 25% | ≥ 0.85 | Quality-gating weights are internally consistent and documented. Weight changes require Amethyst sign-off. |
| D4 | **Advisory Signal Clarity** | 20% | ≥ 0.88 | DemiJoule outputs are clearly marked advisory. No ambiguity about whether a signal is blocking or informational. |

**Composite Pass:** ≥ 0.86. Advisory role — lower stakes than hard-veto agents, but efficiency drift compounds silently.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Efficiency over-report** | DemiJoule reports high efficiency on a high-token operation, masking cost | Amethyst cross-checks against actual token log; DemiJoule re-calibrates model |
| F2 | **Weight drift** | Quality-gating weights silently shift across sessions without changelog entry | COLLEEN surfaces at P-02 as BLG; Amethyst reviews and re-approves weights |
| F3 | **Advisory-blocking confusion** *(non-obvious)* | Downstream agents treat a DemiJoule advisory signal as a hard veto, incorrectly blocking a commit | Amethyst clarifies signal type; Role Separation Rule 5 enforced explicitly |

---

## Gate Ownership

| Gate | DemiJoule Role |
|------|----------------|
| P-11 (Gate 17) | Efficiency score — advisory input to Apogee composite |

---

*Rubric authority: Amethyst-Conductor.*
