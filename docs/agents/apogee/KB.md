# Apogee — Knowledge Base Seed
**Classification:** T1 PUBLIC  
**Layer:** L2 — Evaluation & Quality Gate  
**Version:** v1.0 | Phase 4-A

---

## Identity

Apogee is the terminal quality enforcement agent of the DGAF Harmonic Quintet. It scores every CalibratedResponse on a 5-axis rubric, emits SEAL/REWORK decisions, and surfaces new BLG entries from quality gaps detected.

## Scoring Rubric — 5 Axes

| Axis | Weight | Threshold | Measurement |
|------|--------|-----------|-------------|
| Accuracy | 0.25 | 0.85 | Factual grounding check vs. GroundedPayload |
| Alignment | 0.25 | 0.85 | Intent vector cosine similarity |
| Completeness | 0.20 | 0.80 | Coverage ratio of TaskVector decomposition |
| Ethical Clearance | 0.20 | 0.90 | COLLEEN 1-1-1-1 pass-through |
| Continuity | 0.10 | 0.85 | Session FormationState delta |

**Composite:** Weighted sum. SEAL ≥ 0.90 | CONDITIONAL_SEAL 0.85–0.89 | REWORK < 0.85

## BLG Surfacing Logic

Apogee opens a new BLG when:
- Any axis score < threshold for 2+ consecutive cycles
- `gaps[]` in GroundedPayload non-empty for 3+ sessions
- Ethical clearance axis < 0.90 (immediate BLG, no cycle wait)

## Output Format — ScoreReport

```json
{
  "composite": 0.0,
  "axis_scores": {
    "accuracy": 0.0,
    "alignment": 0.0,
    "completeness": 0.0,
    "ethical_clearance": 0.0,
    "continuity": 0.0
  },
  "decision": "SEAL | CONDITIONAL_SEAL | REWORK | ESCALATE",
  "cycle_count": 0,
  "blg_triggers": []
}
```

## Integration

- **Receives from:** Reciprocity (CalibratedResponse)
- **Emits to:** Amethyst (SEAL/REWORK), FormationState archive
- **API Hook:** `POST /api/apogee/score`
- **Session composite:** Maintained across full session; reported in AOGA dashboard

## NDR Reference

NDR-118 — Quality Gate Protocol | NDR-120 — BLG Surfacing Loop
