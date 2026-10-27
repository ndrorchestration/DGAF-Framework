# PDMAL-GR — Non-Author DDE Reproduction Handoff (v1)

**Status:** REQUEST FOR INDEPENDENT REVIEW — NO REVIEWER VERIFIED. Linked [issue #1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521), [draft PR #1518](https://github.com/ndrorchestration/DGAF-Framework/pull/1518). This is a deliberately isolated **four-node mathematical solver fixture**, not a DGAF governance efficacy experiment, dodecahedron comparison, or canonical blinded pilot.

## 1. Frozen input, independently usable

Read [PDMAL_DDE_EXTERNAL_REPLICATION_FIXTURE_V1.json](PDMAL_DDE_EXTERNAL_REPLICATION_FIXTURE_V1.json) directly as data. Its **canonical SHA-256** (Python: `hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()`) must equal:

`9c54d2a437593ff226e19f8e6a655bf692af37fdcb0c77f12740598734bd1d15`

The JSON is the **author's input specification**, not the independent reviewer's program. Its digest includes two **author-specific numerical solver controls** (`bootstrap_step_s`, `adaptive_max_step_s`); reviewers should preserve the physical inputs while independently choosing, recording, and varying their own numerical solver settings. Any changed physical input is **a new fixture version**, not a reproduction.

For undirected graph edges `(0,1), (1,2), (2,3), (3,0), (0,2)`, implement the directed delayed Kuramoto equation from first principles, **without importing, copying, or delegating to DGAF's `delay_sandbox.py`, `scipy_reference_probe.py` or `jitcdde_reference_probe.py`**:

```text
dθ_i(t)/dt = ω_i + [K / degree(i)] *
             SUM_{j neighbor of i} sin(θ_j(t − τ_{i,j}) − θ_i(t))
```

The first index of `τ_{i,j}` is the **receiver**, the second is the **sender**. Each directed entry in the JSON is `[receiver, sender, seconds]`. **Every other directed incidence along an edge has zero delay** (its neighbor contributes its *current* phase). History is the constant vector `θ(t)=θ(0)` for **all t ≤ 0**, including `t=0`. Phases are **unwrapped radians**, frequencies radians/second, directed delays seconds, coupling `K=1.1`, and degree is the **undirected vertex degree**, not the number of delayed incoming directions.

Expected observation grid is **t=0, 0.02, ..., 0.80 seconds inclusive: 41 timestamps, 4 phases per timestamp**. Do not interpolate or manufacture samples that an integration policy cannot actually provide; report unavailable points explicitly and separately. Do not silently wrap phases modulo `2π`.

## 2. Independent execution protocol

The reviewer, not the DGAF author, should choose, install and control an independently maintained **DDE** package (e.g., Julia/SciML MethodOfSteps, or an independently written JiTCDDE model). Use an environment with no DGAF secrets, write permission, paid service, protected data, or pilot access. Record the package source, exact version, runtime/compiler/toolchain versions, integration method, tolerances and discontinuity strategy.

**Before viewing author numerical output**, freeze the reviewer's own source commit/hash, constant-history implementation, full 41-time-grid result (or an explicit missing-times ledger), and exact numerical controls. Then compare against the separately published same-author benchmark artifacts from [GitHub run #40424843689](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40424843689). Provide both **signed phase residuals and maximum-absolute residuals**, not a summary-only "PASS".

Required challenge cases, clearly labeled **numerical software QA—not additional scientific samples**: check receiver/sender lag orientation and the default zero-lag directions; compare initial right derivatives; examine `t=0.02`, `t=0.04` and neighborhoods of all specified delays `0.04, 0.06, 0.08, 0.10, 0.12 s`; vary the integration resolution/starting method while holding *physical* inputs fixed; record whether a discontinuity-handling API advances past requested early samples; test that a deliberately reversed delay or non-constant history **fails fixture parity** rather than being silently accepted as an equivalent run.

**Accuracy acceptance is NOT preregistered.** Numerical execution, test coverage, a digest match and apparent trajectory similarity can support a reproducibility assessment but do **not** establish a ground-truth error bound without a justified convergence study and independent review. No fixed numeric tolerance should be retrospectively selected to turn these results green.

## 3. Reviewer return receipt

Submit a PR or comment to [issue #1521](https://github.com/ndrorchestration/DGAF-Framework/issues/1521) with:

1. **Reviewer provenance:** reviewer identifier and declaration of non-authorship/no implementation assistance, solver package and methods, code repository/commit/hash, execution date, exact environment and dependency manifest.
2. **Immutable input:** source of the standalone JSON, its canonical SHA-256, any numerical-only changes with their own variant hashes and reasons, and an explicit physical-fixture parity check.
3. **Full raw results:** timestamps, all four unwrapped phases per available time, missing-sample ledger with reason, error/status logs, initialization records, and reproducing command.
4. **Independent technical judgment:** initial derivative and history checks; delay-junction/discontinuity treatment; timestep/tolerance sensitivity; signed and absolute differences from the published author outputs; adverse failures, unresolved mismatches and a recommendation of **REPRODUCED / PARTIALLY REPRODUCED / NOT REPRODUCED / INDETERMINATE**, specifying exactly which numerical property was tested. This is **not** authorization of a research pilot.

The author will assess external evidence separately, preserving the reviewer's raw unmodified T0 output and subsequent discussion. A reviewer is free to disagree with or reject the model and to publish adverse results.

## 4. Existing evidence, not independence

Prior **author-operated** JiTCDDE 1.8.3 run [#40424843689](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/40424843689) saved all 41 points using blind bootstrap. A same-author constant-history ODE check is mathematically valid only until the first positive lag (`t=0.04 s`); the observed early JiTCDDE discrepancy decreases approximately twofold when blind bootstrap steps are halved. Alternative `step_on_discontinuities(propagations=1)` began at `t=0.40 s`, leaving **20 requested early points unobserved**. See [analytic first-window receipt](PDMAL_EARLY_WINDOW_ANALYTIC_RECEIPT_2026-10-26.json) and [experiment notes](PDMAL_DELAY_ROBUSTNESS_PROPOSAL_2026-10-26.md) **after independently freezing T0 output**.

**Canonical state is unchanged:** `SCIENTIFIC_N_INCREMENT=0`; `PILOT_AUTHORIZATION=NOT_GRANTED`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`; `DGAF_V1_RELEASE=HOLD`. PR #1518 remains research-only, draft and unmerged.
