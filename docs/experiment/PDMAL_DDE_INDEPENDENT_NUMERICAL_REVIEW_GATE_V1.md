# PDMAL-GR — Independent Numerical Review Gate v1

**Status:** REVIEW PROTOCOL ONLY / NOT EXECUTED / NOT CERTIFIED. Companion to [draft PR #1518](https://github.com/ndrorchestration/DGAF-Framework/pull/1518), [review issue #1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521), and the [non-author handoff](PDMAL_DDE_NONAUTHOR_REPRODUCTION_HANDOFF_2026-10-26.md). This document does not authorize a pilot, merge, deployment or an efficacy claim.

## Scientific decision boundaries

A successful CI run establishes that the configured software checks executed; it **does not** establish numerical accuracy. An author's JiTCDDE run, even with complete SHA-bound receipts, **does not** constitute a non-author reproduction. A non-author run with matching outputs but no defensible numerical error analysis is **reproduction evidence**, not automatic accuracy certification. A 41/41 sample count is a completeness requirement, never an error tolerance.

Canonical restrictions: `SCIENTIFIC_N_INCREMENT=0`, `PILOT_AUTHORIZATION=NOT_GRANTED`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`, `DGAF_V1_RELEASE=HOLD`.

## T0: independent, blinded computation

1. The reviewer independently derives the DDE from the **data-only** frozen fixture `PDMAL_DDE_EXTERNAL_REPLICATION_FIXTURE_V1.json`; require canonical sorted/minified JSON SHA-256 `9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15`. Keep physical parameters, directed receiver/sender mapping, degree normalization, constant history for all t <= 0, unwrapped radians and the 41-point t=0..0.8 s observation grid invariant.
2. Do not import or transcribe the author's solver implementations. Record reviewer identity, independence declaration, source hash, executable command, OS/runtime/package versions, dependency manifest, DDE method, initial-discontinuity treatment, initial-step procedure, physical-unit scaling, absolute/relative tolerance and interpolation method. Freeze source and results **before** viewing author trajectories.
3. Export all four phases at each requested time or a precise missing-time ledger. Never backfill an unavailable early point by interpolation or by copying an author trace. Preserve stdout/stderr, exceptions and any solver warnings.
4. Before author comparisons, check the initial state and independently calculated right derivative. Check directionally asymmetric delays against their reverse directions, including zero-delay defaults.

## T1: numerical stability and fault investigations

The reviewer holds the same physical fixture and observation grid fixed while varying numerical controls, preferably across **at least three progressively tighter settings**. These are resolution variants, **not independent scientific samples**. Record per-time, per-node signed differences and maximum absolute differences between adjacent refinements. Report observed ratios only when their denominators are nonzero and their interpretation is mathematically justified; zero differences and nonmonotone differences do not establish convergence order.

Investigate t=0, 0.02, 0.04 and both sides of each distinct directed delay 0.04, 0.06, 0.08, 0.10 and 0.12 s. Explicitly determine whether a discontinuity policy advances the solver clock beyond requested grid points. If it does, mark those points missing rather than comparing late-only traces as full-coverage evidence.

Perform two *separately labeled invalid-input tests*: reversed receiver/sender lag orientation, and non-constant negative-time history. These tests intentionally break fixture parity and **must not be pooled with the canonical fixture**. Diagnose their impact without representing the altered trajectories as reproduction of frozen input.

A refinement study showing stability is not automatically a certified bound on error to the exact DDE solution. Discuss solver order, smoothness assumptions, propagation of derivative discontinuities, dense-output interpolation and any remaining uncertainty. No post-hoc threshold selection to classify a result as passing.

## T2: comparison after T0 freeze

Only after T0 source, environment and output are frozen should the reviewer inspect the author-operated receipts, including [workflow run #40424843689](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40424843689). Preserve the immutable T0 copy. Calculate signed residuals for all nodes and available aligned grid times, the max absolute residual per time and globally, the location of the maximum, and an explicit assessment of the bootstrap-dependent startup discrepancy. Distinguish author-to-reviewer difference, reviewer-to-reviewer refinement difference, and any independently justified error estimate; **none is interchangeable with the others**.

## Decision matrix

| Reviewer finding | Permitted conclusion | Not permitted |
| --- | --- | --- |
| Input parity/source provenance fail | INVALID INPUT OR INDETERMINATE | Numerical reproduction |
| Missing early samples, even if late results agree | PARTIALLY REPRODUCED or INDETERMINATE with missing ledger | Full-grid reproduction |
| All 41 points, independently derived dynamics, no convergence justification | REPRODUCTION EVIDENCE; ACCURACY NOT CERTIFIED | Verified numerical accuracy |
| All 41 points, independent method, defensible refinement and documented discrepancies | Qualified numerical reproduction assessment, subject to external review | Automatic pilot admission or scientific efficacy |
| Material unexplained disagreement or adverse tests fail | NOT REPRODUCED or INDETERMINATE, disclose raw evidence | Silent fixture or tolerance changes |

## Reviewer submission and governance

Return raw artifacts and the completed [unsubmitted reviewer template](PDMAL_DDE_NONAUTHOR_RETURN_TEMPLATE_V1.json) to issue #1521. The final reviewer conclusion must distinguish **REPRODUCED**, **PARTIALLY REPRODUCED**, **NOT REPRODUCED**, **INDETERMINATE**, with a separately written assessment of **NUMERICAL_ACCURACY_CERTIFIED / NOT_CERTIFIED** and the supporting methodology. No numerical accuracy certification is pre-granted by this document.

The PR author can verify the submission's custody and discuss discrepancies but **cannot self-sign as the non-author reviewer**. A genuine outside review is necessary before changing the independent-validation register; pilot and release authorizations require their own separate gates. Existing dependency advisory findings must remain visible and may not be waived by this protocol.
