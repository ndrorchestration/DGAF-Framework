# P8 Analysis Lock Record

**Candidate SHA:** `c6157158bf0ee4840e99a381a4b99bd2febe2302`
**Status:** CLOSED / VERIFIED

## Analysis Binding
The executable primary analysis implementation and its configuration are cryptographically bound to the designated candidate.

| Component | Identity / Value | Verification State |
|---|---|---|
| **Analysis Implementation** | `experiments/pdmal_pilot/analysis.py` | **VERIFIED** (SHA256: `463c70eee5ee56cc63455831a605d79a927a3089514d9de3c1d9dbea4b5dd3db`) |
| **Analysis Configuration** | `analysis_config_sha256()` | **VERIFIED** (SHA256: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`) |
| **Candidate Binding** | `c6157158bf0ee4840e99a381a4b99bd2febe2302` | **LOCKED** |

## Primary Contrast Specification
The scientific target for the primary analysis is fixed and bound to the P8 lock.

- **Primary Contrast:** `dgaf` vs `null`
- **Primary Endpoint:** FFCR (Fraction of Finished Cells-of-Success)
- **Estimand:** Mean paired seed-level FFCR difference (`Δ_s = FFCR_{s(dgaf)} − FFCR_{s(null)}`)
- **Statistical Unit:** Root seed (paired)
- **Analysis Method:** Two-sided 95% percentile paired-bootstrap CI (10,000 resamples, seed `20260823`)
- **Decision Rule:** Result **SUPPORTS** if `estimate > 0` and `lower bound > 0`.

## Verification Evidence
- **Candidate Integrity:** Verified via `git rev-parse` and `git rev-list` (HEAD matches candidate, no substantive post-candidate changes).
- **Implementation Integrity:** File SHA256 verified against candidate tree.
- **Configuration Integrity:** Runtime `analysis_config_sha256()` matches the selected lock value.
- **Contractual Alignment:** Analysis implementation verified to consume `ffcr_success`, `topology`, and `failure_count` as required artifact fields.

---
**Closure Authority:** Hermes Agent / Ndr Orchestration
**Date:** 2026-08-30
**Posture:** FAIL-CLOSED (Any substantive change to analysis/configuration invalidates this lock).
