# PDMAL Lattice Harness Reproduction — 2026-08-28

## Scope

This record documents direct execution of the supplied `lattice_harness.py` artifact during the 2026-08-28 DGAF quality pass. It is reproducibility evidence for the supplied mathematical/structural computations only. It does not create PDMAL efficacy, convergence, robustness, security, or baseline-superiority evidence.

## Source artifacts

- `lattice_harness.py`
  - SHA-256: `f8382b68bbf155fe574bd76118db6fc2142c558c21d0f109e3b92103a1611216`
- `lattice_formalization_corrected.md`
  - SHA-256: `61bfffa327694b2a18d4beac61866aba7ec345753002036386ee3baed932c30f`

## Direct execution

Command: `python3 lattice_harness.py`

Exit status: `0`.

Observed output:

- φ = `1.6180339887` (golden ratio).
- ρ = `1.3247179572` (plastic number; real root of x^3 = x + 1).
- Synthetic contraction demo: `n=2000`, `mean_L=0.1082460436`, `p95_L=0.1507066772`, `P(L>=1)=0.0`; verdict explicitly reports **proxy only, not proven**.
- Synthetic admission calibration: `200` healthy-run samples, τ = `0.1122`; noisier synthetic test `D_a=0.6912` → `REJECT`.
- Dodecahedral base graph: `20` nodes, `30` edges, degree set `{3}`, vertex connectivity `3`.
- Exact Cheeger constant: `h(G)=0.6`.
- Unweighted Forman-Ricci: minimum `-2`, mean `-2.0`, with all 30 edges satisfying the default `<= -2` flag condition.

## Interpretation boundary

The mathematical corrections are reproduced. The unweighted Forman-Ricci result has zero variance on the current regular dodecahedral graph and therefore provides no discriminating health signal in this configuration. The supplied harness nevertheless reports every edge as `flagged_edges` under its current default floor; this is a presentation/semantics issue for the audit helper and must not be interpreted as evidence of 30 detected anomalies.

The contraction result is a sampled local Lipschitz proxy for the synthetic contracting map and does not establish a global Banach contraction. The admission threshold is synthetic and does not establish transfer to real Quintet traces.

## Status

**REPRODUCED / BOUNDED / NO SYSTEM-LEVEL EFFICACY CLAIM.**

Related issue: #72 (weighted Forman-Ricci replication and anomaly-threshold falsification).
