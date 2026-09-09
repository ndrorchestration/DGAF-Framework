# PDMAL Weighted Forman–Ricci Replication Protocol — 2026-09-09

**Issue:** #72  
**Classification:** prospective synthetic falsification study  
**Scientific-state effect:** NONE  
**Canonical DGAF efficacy:** NOT ESTABLISHED

## Research question

Does assigning controlled positive edge weights to the otherwise 3-regular dodecahedral PDMAL graph consistently restore edge-curvature variance, and how reliably do predeclared anomaly-selection rules recover the intentionally perturbed edges?

This protocol tests a bounded mathematical/measurement hypothesis. It is not a Track A experiment and cannot change freeze, custody, authorization, primary-analysis, efficacy, or High-Assurance state.

## Curvature definition

Use the weighted undirected Forman–Ricci edge curvature introduced for complex networks by Sreejith, Mohanraj, Jost, Saucan, and Samal (2016), *Forman curvature for complex networks*, arXiv:1603.00386.

For edge `e=(u,v)` with positive edge weight `w_e`, positive vertex weights `w_u,w_v`, and incident edges excluding `e`:

```text
F(e) = w_e [ w_u/w_e + w_v/w_e
             - sum_{e_u~e} w_u/sqrt(w_e w_eu)
             - sum_{e_v~e} w_v/sqrt(w_e w_ev) ]
```

All vertex weights are fixed to `1.0`. With all edge weights equal to `1.0`, this reduces exactly to `4 - deg(u) - deg(v)`, hence `-2` on every edge of the canonical dodecahedral graph.

## Fixed graph and perturbation matrix

- Graph: repository canonical 20-node / 30-edge dodecahedral edge set.
- Baseline edge weight: `1.0`.
- Healthy curvature reference: `-2.0`.
- Perturbed-edge counts: `1, 3, 5, 10`.
- Exact target edge weights:
  - decreases: `0.1, 0.3, 0.5, 0.7`;
  - increases: `1.3, 2.0`.
- Twenty deterministic edge selections per `(perturbed_count, target_weight)` cell.
- Master seed: `20260909`; each cell/replicate derives and records its own deterministic selection seed.
- Replicates `0..9`: calibration only.
- Replicates `10..19`: held-out evaluation only.
- Total graphs: `4 × 6 × 20 = 480`.
- Calibration graphs: `240`.
- Held-out graphs: `240`.

The original issue wording listed the six numeric perturbation values and separately said “both directions.” Because the listed values already occur on both sides of baseline `1.0`, this protocol treats them as exact target weights rather than crossing them with another sign factor. That avoids undefined negative weights and duplicate reciprocal interpretations while preserving every predeclared numeric value.

## Ground truth and spillover

The truth set is exactly the set of intentionally perturbed edges. Weighted Forman curvature is local: changing one edge can also change curvature on neighboring unperturbed edges. Such spillover is part of the test. If a detector selects an unperturbed neighbor, that selection is counted as a false positive rather than silently relabeled as truth.

## Predeclared anomaly score

For detectors that operate on a scalar anomaly score:

```text
score(e) = |F_weighted(e) - (-2)|
```

The `-2` reference is fixed by the all-weight-1 healthy graph and is not estimated from perturbed trials.

## Detector matrix

1. **Mean + 3σ score** — flag `score > mean(score) + 3σ(score)` within each graph.
2. **Two-sided 3σ raw curvature** — flag raw curvature outside `mean(F) ± 3σ(F)`.
3. **MAD modified-z** — flag `|0.6745 (F - median(F)) / MAD| > 3.5`; when MAD is exactly zero, only values unequal to the median are flagged.
4. **90th-percentile score** — flag positive scores at or above the deterministic linearly interpolated 90th percentile within each graph.
5. **Rank top-k oracle** — select exactly the `k` largest scores, where `k` is the injected perturbation count. This is explicitly an oracle comparator, not an operational detector.
6. **Calibrated global score threshold** — choose one scalar score threshold using calibration replicates only to maximize mean trial F1 across all calibration cells. Ties select the larger threshold. Freeze that scalar before scoring held-out replicates.

No threshold may be changed after held-out results are observed in this execution lineage.

## Required metrics

For every held-out graph and detector:

- true positives / false positives / false negatives / true negatives;
- TPR;
- FPR;
- precision;
- recall;
- worst rank occupied by a true perturbed edge in the global score ordering.

Also record per-graph curvature variance and aggregate:

- fraction of all 480 perturbed graphs with variance greater than `1e-15`;
- minimum and maximum curvature variance;
- held-out mean metrics for every detector.

## Prior reproduction check

The implementation test fixes three edges `(3,4)`, `(5,6)`, `(5,15)` at weight `0.3`, leaving all others at `1.0`. Under the weighted formula above, population curvature variance must reproduce:

```text
0.5799847018687604
```

This is a mathematical regression check against the earlier single-configuration observation. It is not evidence of general reliability.

## Evidence discipline

The executable output schema is `PDMAL_WEIGHTED_FORMAN_REPLICATION_V1` and must bind the executing Git commit/run. The result artifact and SHA-256 sidecar are retained from the exact PR head.

Permitted result labels:

- variance restoration: COMPUTED/SYNTHETIC for this matrix;
- threshold behavior: COMPUTED/SYNTHETIC for this matrix;
- general weighted-curvature reliability: NOT ESTABLISHED;
- production detector selection: NOT SELECTED;
- canonical DGAF efficacy: NOT ESTABLISHED.

A positive sweep does not by itself upgrade weighted Forman–Ricci to VERIFIED operational usefulness. Any such promotion requires separate review and, where relevant, realistic held-out traces or perturbations beyond this synthetic graph study.
