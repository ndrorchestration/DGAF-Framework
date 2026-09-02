# P7 Binding Record — Scientific Target / Candidate Provenance (2026-09-02)

**Status:** EXACT-CANDIDATE BINDING RECORDED / PRE-FREEZE  
**Gate:** P7 — Scientific Target Binding  
**Selected candidate:** PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`  
**Candidate tree:** `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`  
**Corrected apparatus/source anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This record binds the already-adopted P7 scientific specification to the current exact candidate for provenance and freeze-readiness purposes. It does **not** create a new scientific decision, modify an adopted field, create a freeze, or authorize pilot execution.

## Authority inheritance

The scientific values below are carried forward from the prior P7 adjudication/binding records. This document changes only the candidate/provenance binding: no scientific field is newly selected here.

| # | Field | Adopted value |
|---|---|---|
| 1 | Primary contrast | `dgaf` vs `null` |
| 2 | Primary endpoint | FFCR (Fraction of Finished Cells-of-Success) |
| 3 | Statistical unit | Root seed (paired) |
| 4 | Aggregation | 5 topologies × 9 failure counts = 45 cells × 180 trials = 8,100 raw records per seed; 50 seeds planned |
| 5 | Paired seed estimand | `Δ_s = FFCR_{s(dgaf)} − FFCR_{s(null)}` |
| 6 | Population estimand | `Δ = E_s[Δ_s]` |
| 7 | Point estimator | `mean_s(Δ_s)` over the 50-seed panel |
| 8 | Inference | Two-sided 95% percentile paired-bootstrap CI (10,000 resamples, seed `20260823`) |
| 9 | Directional rule | Result supports if estimate > 0 and lower bound > 0 |
| 10 | Success criterion | `FFCR_{dgaf} > FFCR_{null}` with CI excluding 0 |
| 11 | Falsification criterion | CI includes 0, or `FFCR_{dgaf} ≤ FFCR_{null}` |
| 12 | Secondary contrast family | Per-topology and per-failure-count FFCR deltas (exploratory, not confirmatory) |

## Exact binding

The adopted specification is now explicitly associated with candidate `58ba9a…` and tree `abdbc9b…` for the September 2 control-plane reconciliation. The binding remains **pre-freeze**: it becomes the authoritative frozen-apparatus identity only through the later immutable freeze procedure.

The selected candidate's successful September 2 GitHub Actions wave does not itself satisfy runtime/deployment, durable custody, final independent verification, freeze, or authorization predicates.

## Provenance references

- Prior P7 scientific binding record: `docs/GOVERNANCE/P7_BINDING_RECORD_2026-08-30.md` (historical candidate `c6157158…`).
- P7 primary-contrast adjudication packet and scientific traceability matrix remain the source of the adopted values.
- Current exact candidate: PR #192 / `58ba9a…`.

## Non-authorizing boundary

**P7 exact-candidate provenance binding: RECORDED.**  
**P7 scientific values: UNCHANGED.**  
**Freeze: NOT CREATED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
