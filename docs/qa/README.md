# QA & Attestation Index

> **Authority:** Agent Apogee (Evidence Governor)  
> **Gate:** P-30 Apogee-Attestation-Gate — P-11 11Q scoring; S-TIER (≥95%) or A-TIER (≥85%) with BLGs  
> **Last updated:** S038 — 2026-05-22

---

## Attestation Records

| File | Session | Components Scored | Result |
|------|---------|-------------------|-------|
| `APOGEE_11Q_S034.json` | S034 | KAPPA v3.6, Evaluate Router v1.1 | A-TIER (pre-NormativeConstraint) |
| `APOGEE_11Q_S035.json` | S035 | KAPPA v3.6, Evaluate Router v1.1 (post-NormativeConstraint) | S-TIER ✅ P-30 GRANTED |

---

## What P-30 Requires

| Condition | Score Threshold | Action |
|-----------|----------------|-------|
| S-TIER grant | ≥95% AND Q11 ≥9/10 | Attestation GRANTED; canonical promotion authorized |
| A-TIER with BLGs | ≥85%, Q11 <9/10 | Attestation CONDITIONAL; carry-forward BLGs required |
| Below A-TIER | <85% | Attestation DENIED; component stays in staging |

---

## Notes
- Q11 (Normative Constraint wiring) is a hard floor for S-TIER.
- `normative_constraint.py` is the canonical Q11 implementation.
- New attestation records follow naming convention: `APOGEE_11Q_S{NNN}.json`
