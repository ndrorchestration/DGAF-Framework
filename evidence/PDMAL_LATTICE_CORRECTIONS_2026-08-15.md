# PDMAL Lattice Corrections — 2026-08-15

## Purpose

This note records independently reproduced corrections from the lattice formalization pass. It is an evidence record, not a claim of convergence or system-level validation.

## Reproduced results

Using the supplied `lattice_harness.py`:

- Plastic constant (real root of `x^3 = x + 1`): `1.3247179572447454`.
- Dodecahedral base graph: 20 vertices, 30 edges, 3-regular, vertex connectivity 3.
- Exact Cheeger constant for the dodecahedral graph: `h(G) = 0.6`.
- Unweighted Forman-Ricci curvature: `-2` on every edge, hence zero variance and no discriminating signal on the current unweighted topology.
- Contraction monitor is an empirical local proxy only; sampled `P(L >= 1) = 0` in the synthetic contracting demo and does not establish a global Banach contraction.
- Admission threshold calibration is demonstrated from synthetic healthy-run samples only; it is not evidence that the threshold transfers to production or real Quintet traces.

## Evidence boundaries

These computations correct source-document constants and demonstrate reproducibility under the supplied harness. They do **not** establish:

- convergence of PDMAL in general,
- global contraction of a composed service map,
- production performance,
- security properties,
- superiority to a baseline,
- validity of a Forman-Ricci audit signal on an unweighted dodecahedral graph.

## Required follow-up

1. Define real edge weights before treating Forman-Ricci as an operational audit signal.
2. Calibrate `D_a` against real healthy traces and test against held-out/adversarial cases.
3. Run a baseline comparison for the PDMAL topology claim.
4. Preserve the corrected plastic constant and Cheeger constant in all downstream documentation.

Source artifacts: `lattice_harness.py` and `lattice_formalization_corrected.md` supplied for the 2026-08-15 quality pass.
