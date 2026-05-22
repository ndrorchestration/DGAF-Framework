# Components — Runtime Index

> **Maintainer:** Agent Amethyst + COLLEEN  
> **Last updated:** S038 — 2026-05-22  
> **Governed by:** P-30 Apogee-Attestation-Gate — all components below are S-TIER attested

---

## Active Components

| Component | Version | Path | Purpose | Tier | Session |
|-----------|---------|------|---------|------|---------|
| KAPPA Dynamic Confidence Router | v3.6 | `KAPPA/dynamic_weight_router.py` | Category detection + confidence-gated weight selection (STRONG/BLENDED/fallback) | S-TIER 97.3% | S033/S034 |
| KAPPA Calibration | v3.6 | `KAPPA/calibration_v3_6.json` | Threshold calibration; `governance_clear` 100% | — | S034 |
| KAPPA Component Card | v3.5 | `KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` | CPU-compliant registry card (all 6 schema fields) | — | S034 |
| Evaluate Router | v1.0 | `evaluate_router.py` | Batch pipeline: raw_batch → detect → apply_weights → ranked report | S-TIER | S033 |
| Evaluate Router | v1.1 | `evaluate_router_v1_1.py` | Sentinel hooks (3 points) + P-10 deontic gate + EU AI Act Art.9 audit log | S-TIER 95.5% | S034 |
| Normative Constraint | v1.0 | `normative_constraint.py` | Deontic logic (permitted/obligated/forbidden/escalate) + score ceiling + epistemic integrity | S-TIER | S035 |

---

## Attestation Summary

| Component | Apogee 11Q Score | Attestation | Record |
|-----------|-----------------|-------------|-------|
| KAPPA v3.6 | 97.3% (S-TIER) | ✅ GRANTED | `docs/qa/APOGEE_11Q_S035.json` |
| Evaluate Router v1.1 | 95.5% (S-TIER) | ✅ GRANTED | `docs/qa/APOGEE_11Q_S035.json` |
| Normative Constraint v1.0 | S-TIER (Q11=10/10) | ✅ GRANTED | `docs/qa/APOGEE_11Q_S035.json` |

---

## P-10 Gate — Normative Constraint

`normative_constraint.py` is the active P-10 implementation. Call `run_normative_pass(records)` before weight selection in any evaluation pipeline.

```python
from components.normative_constraint import run_normative_pass
constrained = run_normative_pass(batch)
```

---

## Notes
- All components require P-30 attestation before canonical promotion.
- New components stage in `docs/drafts/` until P-11 11Q scoring ≥ 85%.
- CROSS_REF.md v3.3 is the authoritative ecosystem map.
