# QA & Attestation Index

> **Status boundary:** This index records project-local QA/attestation records. It is not an external certification register. Scores and grants below are historical records of the named sessions and must not be treated as current certification without a fresh, evidence-backed review.
> **Last reconciled:** 2026-09-02

---

## Attestation Records

| File | Session | Components Scored | Recorded Result |
|------|---------|-------------------|-----------------|
| `APOGEE_11Q_S034.json` | S034 | KAPPA v3.6, Evaluate Router v1.1 | A-TIER (pre-NormativeConstraint) |
| `APOGEE_11Q_S035.json` | S035 | KAPPA v3.6, Evaluate Router v1.1 (post-NormativeConstraint) | S-TIER / P-30 GRANTED in recorded session |

## What P-30 Defines

| Condition | Project-local threshold | Recorded action |
|-----------|-------------------------|-----------------|
| S-TIER | ≥95% and Q11 ≥9/10 | Project-local attestation grant; promotion according to repository procedure |
| A-TIER with BLGs | ≥85%, Q11 <9/10 | Project-local conditional attestation |
| Below A-TIER | <85% | Project-local denial / staging |

These thresholds define a repository-local review procedure. They are not independently validated certification criteria.

## Current Interpretation

- The S034/S035 records establish that those project-local reviews occurred as documented.
- They do not establish current production readiness, external certification, statistical validity, security assurance, or universal fitness.
- Current claims require current implementation evidence, dated test results, and the applicable independent evidence for the claim being made.

## Notes

- Q11 (Normative Constraint wiring) is a project-local gate criterion.
- `normative_constraint.py` is the recorded implementation referenced by the S035 review.
- New attestation records follow `APOGEE_11Q_S{NNN}.json`.
