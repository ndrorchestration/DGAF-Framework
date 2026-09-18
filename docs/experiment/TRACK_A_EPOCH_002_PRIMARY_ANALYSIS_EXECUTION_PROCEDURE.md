# Track A Epoch 002 Locked Primary Analysis Execution Procedure

Status: **PROSPECTIVE TOOLING / EXECUTION REQUIRES ACCEPTED PRIMARY-ANALYSIS AUTHORIZATION**

This procedure governs the local execution of the already-frozen Track A Epoch 002 primary analysis. It does not modify the preregistration, analysis implementation, materialized input, or authorization record.

## Preconditions

Execution is admissible only when all of the following are true:

1. The canonical `PRIMARY_ANALYSIS_AUTHORIZATION_RECORD` exists on protected `main` as a creation-only immutable event.
2. The authorization record validates against the accepted `MATERIALIZATION_RECEIPT`.
3. The frozen analysis blob remains `d4495f7cdf211b974039ec0e66292dc62ea0881f`.
4. The frozen analysis configuration SHA-256 remains `a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73`.
5. The requirements lock blob remains `00c1f779e97030f9b25ae494642edb31b5b09de5`.
6. The local runtime exactly matches the analysis lock: Python `3.12.0` and NumPy `2.5.1`.
7. The external materialized input SHA-256 exactly matches the admitted materialization evidence.
8. No canonical locked-analysis result record already exists.

Any failed precondition stops execution.

## Local preflight

After the authorization event has been accepted on protected `main`, use the exact locked analysis environment and run:

```text
python scripts/run_track_a_epoch_002_locked_primary_analysis.py --preflight-only
```

Preflight does not read the materialized input and does not execute the analysis.

## Local execution

The retained materialized input remains outside the repository. Execute:

```text
python scripts/run_track_a_epoch_002_locked_primary_analysis.py \
  --input <external-track_a_epoch_002_unblinded_analysis_input.json> \
  --output-dir <external-empty-result-directory>
```

The runner refuses repository-local input/output paths and refuses to overwrite an existing result.

The local output bundle contains:

- the exact authorization-event identity;
- the admitted materialized-input digest;
- frozen analysis/config identities;
- exact runtime versions;
- the locked primary estimate, confidence interval, and preregistered classification;
- explicit non-promotion fields preserving canonical DGAF efficacy, independence, and High-Assurance boundaries.

The runner prints only the output path and SHA-256, not the statistical result.

## Post-execution boundary

Execution does **not** by itself establish canonical DGAF efficacy, independent validation, or High-Assurance authorization. The local output must next be admitted through a separate, content-addressed `LOCKED_ANALYSIS_RESULT_RECORD` event before interpretation.

No exploratory comparison may be relabeled confirmatory after outcome inspection.
