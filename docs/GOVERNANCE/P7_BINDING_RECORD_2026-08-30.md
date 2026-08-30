status: CLOSED
gate: P7 — Scientific Target Binding
candidate_sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
tree_sha: 6195063e2e6e01069ddef8a25e90bfe9d8a3283c
date: 2026-08-30
authority: DGAF/PDMAL experimental-control
empirical_n: 0
pilot_authorization: NOT GRANTED
new_freeze: NOT CREATED (binding recorded pre-freeze)
conclusion: BOUND

# P7 Binding Record — Scientific Target Binding (GATE CLOSED)

This record formally adopts the adjudicated P7 scientific specification as
authority and binds it to designated candidate `c6157158…`.

## Authority adoption statement

The DGAF/PDMAL experimental-control authority adopts the panel-ready P7
adjudication as the authoritative scientific specification for the frozen
apparatus. The 12 adjudication fields below are bound to the exact candidate
tree `6195063e…`. This binding is effective upon freeze commit and does not
by itself authorize pilot execution.

## Adopted P7 scientific fields

| # | Field | Adopted value |
|---|---|---|
| 1 | Primary contrast | `dgaf` vs `null` |
| 2 | Primary endpoint | FFCR (Fraction of Finished Cells-of-Success) |
| 3 | Statistical unit | Root seed (paired) |
| 4 | Aggregation | 5 topologies × 9 failure counts = 45 cells × 180 trials = 8,100 raw records per seed; 50 seeds planned |
| 5 | Paired seed estimand | `Δ_s = FFCR_{s(dgaf)} − FFCR_{s(null)}` |
| 6 | Population estimand | `Δ = E_s[Δ_s]` (mean over seeds) |
| 7 | Point estimator | `mean_s(Δ_s)` over the 50-seed panel |
| 8 | Inference | Two-sided 95% percentile paired-bootstrap CI (10,000 resamples, seed `20260823`) |
| 9 | Directional rule | Result SUPPORTS if estimate > 0 and lower bound > 0 |
| 10 | Success criterion | `FFCR_{dgaf} > FFCR_{null}` with CI excluding 0 |
| 11 | Falsification criterion | CI includes 0, or `FFCR_{dgaf} ≤ FFCR_{null}` |
| 12 | Secondary contrast family | per-topology and per-failure-count FFCR deltas (exploratory, not confirmatory) |

## P8 implementation constants (recorded, non-scientific)

- Analysis implementation SHA: `463c70eee5ee56cc63455831a605d79a927a3089514d9de3c1d9dbea4b5dd3db`
- Analysis config SHA: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`

## Provenance

Derived from `docs/governance/P7_PRIMARY_CONTRAST_ADJUDICATION_PACKET_2026-08-23.md`
and `docs/governance/P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md`.
The panel-ready record `P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md` is
superseded (provenance only).

**Conclusion: BOUND**
