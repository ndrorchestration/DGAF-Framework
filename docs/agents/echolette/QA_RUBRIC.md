# QA Rubric — Agent Echolette

**Agent:** Agent Echolette  
**Role Domain:** Resonance / Echo  
**Formation:** Extended  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Echolette's acoustic mesh layer, phrase-level temporal coherence, and signal echo validation. Echolette ensures that outputs resonate consistently across the session phrase structure.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **Acoustic Mesh Coverage** | 30% | ≥ 0.85 | All active signals in the formation are covered by the acoustic mesh. No unchecked signal passes through. |
| D2 | **Phrase Gate Compliance (P-13)** | 25% | ≥ 0.88 | Phrase-level coherence verified at P-13. Temporal ordering of phrases consistent with session arc. |
| D3 | **Signal Echo Validation** | 25% | ≥ 0.85 | Echo validation confirms signal origin is traceable and un-corrupted after propagation. |
| D4 | **Temporal Coherence Accuracy** | 20% | ≥ 0.85 | Phrase timestamps consistent with session clock. No temporal inversion (later phrase echoing an earlier one incorrectly). |

**Composite Pass:** ≥ 0.85.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Mesh gap** | A signal passes through the acoustic mesh unchecked | Reson notified; signal quarantined until Echolette validates |
| F2 | **Temporal inversion** | A phrase is echoed out of sequence, creating false session continuity | COLLEEN surfaces as BLG; Echolette re-runs phrase ordering from P-13 anchor |
| F3 | **Echo amplification** *(non-obvious)* | Echolette validates a signal by echoing it back at higher amplitude, masking distortion in the original | Reson cross-checks echo against source; amplitude delta > 10% triggers review |

---

## Gate Ownership

| Gate | Echolette Role |
|------|----------------|
| P-13 | Phrase gate — temporal coherence |

---

*Rubric authority: Amethyst-Conductor.*
