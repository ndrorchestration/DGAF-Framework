# QA Rubric — Agent Reson

**Agent:** Agent Reson  
**Role Domain:** Harmonic Coherence  
**Formation:** Quintet  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Reson's harmonic coherence scoring, drift warnings, and dissonance hard-stop triggers. Reson scores are binding for seal commits (P-15) and sovereign file touches.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **Score Accuracy (0.00–1.00)** | 30% | ≥ 0.90 | Harmonic coherence score correctly reflects formation alignment, signal chain integrity, and session-state consistency. |
| D2 | **Threshold Enforcement** | 25% | ≥ 0.95 | ≥ 0.75 enforced for seal commits. 0.50–0.74 triggers drift warning (not stop). < 0.50 triggers hard stop. No threshold mis-application. |
| D3 | **Signal Chain Integrity** | 20% | ≥ 0.88 | All agent signals in the formation accounted for before scoring. No scoring on incomplete formations. |
| D4 | **Dissonance Source Identification** | 15% | ≥ 0.85 | When score < 0.75, Reson identifies the specific dissonance source (agent, file, or decision). |
| D5 | **NDR-133 Firewall Activation** | 10% | ≥ 0.92 | NDR-133 pattern triggers Sentinel notification within the same turn. |

**Composite Pass:** ≥ 0.88 routine; ≥ 0.92 for P-15 inputs.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Threshold mis-application** | Reson applies seal threshold (0.75) to a non-seal commit, blocking valid work | Amethyst clarifies commit type; Reson re-evaluates with correct threshold scope |
| F2 | **Score without full formation** | Reson scores while formation is incomplete (e.g., Sentinel not yet activated) | Score voided; Amethyst completes formation; Reson re-scores |
| F3 | **Score laundering** *(non-obvious)* | Reson absorbs a dissonant signal from one agent by averaging across others, masking a real problem with a passing composite | Amethyst requires dimension-level breakdown; any single-dimension score < 0.50 triggers review regardless of composite |

---

## Gate Ownership

| Gate | Reson Role |
|------|------------|
| P-15 | Harmonic coherence score — required ≥ 0.75 for seal |

---

*Rubric authority: Amethyst-Conductor.*
