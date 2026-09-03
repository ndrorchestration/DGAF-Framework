# Components — Runtime Index

> **Maintainer:** Agent Amethyst + COLLEEN  
> **Last reviewed:** 2026-09-02  
> **Evidence boundary:** The attestation records below are dated project-local QA records. They do not by themselves establish current external certification, universal fitness, production readiness, or independent validation.

---

## Active Components

| Component | Version | Path | Purpose | Historical / project-local record | Session |
|-----------|---------|------|---------|-----------------------------------|---------|
| KAPPA Dynamic Confidence Router | v3.6 | `KAPPA/dynamic_weight_router.py` | Category detection + confidence-gated weight selection (STRONG/BLENDED/fallback) | S-TIER 97.3% in recorded Apogee review | S033/S034 |
| KAPPA Calibration | v3.6 | `KAPPA/calibration_v3_6.json` | Threshold calibration; `governance_clear` 100% in recorded artifact | Recorded calibration value; current fitness requires re-evaluation | S034 |
| KAPPA Component Card | v3.5 | `KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` | Registry card and schema fields | Project-local registry artifact | S034 |
| Evaluate Router | v1.0 | `evaluate_router.py` | Batch pipeline: raw_batch → detect → apply_weights → ranked report | S-TIER in recorded Apogee review | S033 |
| Evaluate Router | v1.1 | `evaluate_router_v1_1.py` | Sentinel hooks + P-10 deontic gate + audit-log support | S-TIER 95.5% in recorded Apogee review | S034 |
| Normative Constraint | v1.0 | `normative_constraint.py` | Deontic logic + score ceiling + epistemic-integrity checks | S-TIER / Q11=10/10 in recorded Apogee review | S035 |

## Attestation Summary

The records below preserve what the project-local Apogee review documented at the time. They should be cited as historical/project-local attestation records, not as current independent certification.

| Component | Apogee 11Q Score | Recorded Result | Record |
|-----------|-----------------|----------------|-------|
| KAPPA v3.6 | 97.3% (S-TIER) | GRANTED in S035 record | `docs/qa/APOGEE_11Q_S035.json` |
| Evaluate Router v1.1 | 95.5% (S-TIER) | GRANTED in S035 record | `docs/qa/APOGEE_11Q_S035.json` |
| Normative Constraint v1.0 | S-TIER (Q11=10/10) | GRANTED in S035 record | `docs/qa/APOGEE_11Q_S035.json` |

## P-10 Gate — Normative Constraint

`normative_constraint.py` is the recorded P-10 implementation. Use current tests and evidence to establish present behavior before making a current performance, security, or production-readiness claim.

```python
from components.normative_constraint import run_normative_pass
constrained = run_normative_pass(batch)
```

## Notes

- P-30 and related tiers are project-local governance mechanisms.
- Historical attestations remain useful provenance but expire as evidence of current state when implementation or requirements change.
- New components should receive repository-defined review before promotion.
- `CROSS_REF.md` is the project ecosystem map; cross-repository presence does not establish mutual validation.
