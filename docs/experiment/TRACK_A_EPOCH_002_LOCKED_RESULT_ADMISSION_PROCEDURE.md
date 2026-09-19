# Track A Epoch 002 Locked Result Admission Procedure

Status: **ACCEPTED RESULT / HISTORICAL ADMISSION PROCEDURE**

This procedure governed the repository admission of the content-addressed output from the frozen Track A Epoch 002 primary analysis. The governed event is now accepted: PR #851 merged as `c0690e599d25304f1d920d5235adff04ba76094a`, creating the canonical result record. The procedure does not execute analysis, expose numerical outcomes in the repository record, interpret the result, increment scientific N, establish canonical DGAF efficacy, establish independent validation, or authorize High-Assurance operation.

## Sequence

1. An accepted creation-only `PRIMARY_ANALYSIS_AUTHORIZATION_RECORD` must already exist on protected `main`.
2. The local locked-analysis runner executes outside GitHub against the retained materialized input.
3. The retained local output is validated against the frozen Track A analysis identity, exact runtime, exact materialized-input digest, and preregistered classification rule.
4. The local preparer computes the exact SHA-256 of that validated output and creates a candidate `LOCKED_ANALYSIS_RESULT_RECORD`.
5. The candidate record contains the authorization-event commit and the local output SHA-256, but not the numerical estimate, confidence interval, or classification.
6. The result record is admitted only through a separate one-parent, one-file, creation-only protected-main event.
7. Interpretation remains a later, separate `INTERPRETATION_NOTE` stage.

## Accepted event

The accepted creation-only event is:

- PR: `#851`;
- commit: `c0690e599d25304f1d920d5235adff04ba76094a`;
- accepted parent: `4cfa8e18779d5788d739f37e47892ad43d51cd8d`;
- retained output SHA-256: `966fe9f1c218d8f64eae8465288a5e23b332555484eac2602c3764c3172336da`;
- authorization-event binding: `e87917e644d71de7351c5983fa7ed89d9231962f`;
- numerical estimate, confidence interval, and classification: **not copied into the repository record**.

The canonical result-record path has exactly one history event. The current downstream frontier is the separate `INTERPRETATION_NOTE` stage governed by #719.

## Canonical result record

The only repository path for this event is:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json`

The record uses the already accepted shared Epoch 002 result-record schema and the `OBSERVATIONAL_PASS` semantic profile. Therefore it carries:

- `authorization_effect=NONE`;
- the full non-authorization/non-promotion ceiling;
- `SCIENTIFIC_N_INCREMENT=0`;
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`;
- no independent-validation or High-Assurance transition.

## Local preparation

After authorized local execution, run the preparer with the retained output and a candidate destination outside or inside an isolated result-admission worktree:

```text
python scripts/prepare_track_a_epoch_002_locked_analysis_result_record.py \
  --analysis-output <external-track_a_epoch_002_locked_primary_analysis_output.json> \
  --output-record <candidate-TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json> \
  --parent-ref HEAD
```

The preparer validates the local output before hashing it. It does not print or copy the estimate, confidence interval, or classification.

## Event validation

For a proposed result-record commit, the validator requires:

- exactly one parent;
- exactly one changed path, the canonical result record;
- creation-only, first-and-only history for that path;
- the parent to equal the accepted protected-main parent;
- the accepted primary-analysis authorization to remain byte-identical;
- the authorization itself to remain a valid one-file, creation-only event;
- the result record to bind the exact authorization event and a syntactically valid SHA-256 of the retained local output;
- the shared schema and observational semantic profile to remain unchanged.

A validation PASS on a PR head is `VALIDATED_PENDING_ACCEPTANCE`, not a scientific conclusion.

## Post-admission boundary

The result record now exists on protected `main` and must be treated as an immutable historical event rather than recreated or replaced. Later tooling validates that accepted history and, when explicitly invoked with the retained operator-local output, may prepare a separate `INTERPRETATION_NOTE` candidate. Numerical interpretation remains downstream and separately governed. No exploratory analysis becomes confirmatory by virtue of result admission, and the accepted receipt does not promote scientific N, canonical DGAF efficacy, independent validation, or High-Assurance authorization.
