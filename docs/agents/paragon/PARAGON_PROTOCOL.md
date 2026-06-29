# Paragon — PROTOCOL v1.0

**Agent:** Paragon
**Agent ID:** A-24
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Procedure 1 — Quality Baseline

**Trigger:** New output submitted for quality evaluation.

1. Identify which excellence standard applies to the output type
2. If no standard exists for this output type: trigger Procedure 4 to define standard first
3. Score output against each dimension of the relevant standard
4. Calculate composite quality score
5. Identify all gaps (dimensions scoring < 0.75)
6. If composite ≥ 0.75 AND no critical fails: issue GATE_CLEAR
7. If composite < 0.75 OR critical fail: issue GATE_HOLD with:
   - Specific gap identification
   - Root cause for each gap
   - Remediation path
8. Log evaluation in PARAGON_MEMORY.md
9. Check recurring gap archive: is this gap appearing for the 3rd time?
   - Yes: trigger systemic failure escalation to Amethyst

---

## Procedure 2 — Gap Analysis

**Trigger:** GATE_HOLD issued, OR Amethyst requests quality deep-dive.

1. Identify all gaps in the evaluated output
2. For each gap:
   a. Classify root cause: agent capability, process design, input quality, standard ambiguity
   b. Assess whether gap is isolated or systemic
3. Prioritize gaps by impact on target state achievement
4. Generate remediation path for each gap:
   - Agent capability: route to agent's training / KB update
   - Process design: route to Navigator for procedure revision
   - Input quality: route upstream to source agent
   - Standard ambiguity: trigger Procedure 4 to update standard
5. Log gap analysis in PARAGON_MEMORY.md

---

## Procedure 3 — Gold Star Prerequisite Check

**Trigger:** Submission for Gold Star designation received.

1. Verify the submission has passed Reson harmonic scoring (score ≥ 0.75 required)
2. Evaluate submission against all relevant excellence standards
3. Verify: zero critical fails; composite ≥ 0.90 (Gold Star threshold is higher than standard gate)
4. If PASS: submit Paragon prerequisite evaluation to Apogee with:
   - Dimension scores
   - Reson harmonic score (received from Reson)
   - Paragon composite score
   - Recommendation: GOLD_STAR_ELIGIBLE
5. If FAIL: issue GATE_HOLD; Gold Star designation deferred
6. Log evaluation in PARAGON_MEMORY.md Gold Star archive

---

## Procedure 4 — Excellence Standard Update

**Trigger:** New output type encountered with no standard, OR standard ambiguity causing inconsistent evaluations.

1. Draft new or revised excellence standard:
   - Define 5 evaluation dimensions
   - Assign weights (must sum to 1.0)
   - Define score criteria for each dimension (0.0, 0.25, 0.50, 0.75, 1.0)
   - Identify critical fail conditions
2. Submit draft to Prof Prodigy for rigor verification
3. On PASS: register in PARAGON_MEMORY.md Excellence Standard Registry
4. On FAIL: revise and resubmit
5. Notify Apogee of new standard (for evidence gate calibration)

---

*Classification: T1 PUBLIC*
