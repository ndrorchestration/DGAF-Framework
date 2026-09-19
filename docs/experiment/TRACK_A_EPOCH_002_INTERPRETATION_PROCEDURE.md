# Track A Epoch 002 Interpretation / Adjudication Procedure

Status: **PROSPECTIVE TOOLING / NO INTERPRETATION NOTE ADMITTED**

The locked primary analysis has executed locally, and the immutable content-addressed
`LOCKED_ANALYSIS_RESULT_RECORD` is established on protected `main` via PR #851.
This procedure governs the next separate stage: interpretation/adjudication of the
retained local result without copying the numerical result into GitHub or CI.

## Boundary

The interpretation stage is non-authorizing. It does not rerun analysis, alter the
frozen endpoint or estimand, pool historical epochs, increment scientific N,
establish canonical DGAF efficacy, establish independent validation, authorize
High-Assurance operation, or establish production readiness.

The confirmatory interpretation is limited to the preregistered question:

> Under the fixed reference neighbor-mean alpha-0.5 consensus algorithm, does the
> PDMAL topology yield higher failure-and-recovery success than the matched
> random-regular topology across the preregistered failure-count panel?

The single confirmatory contrast remains PDMAL versus random-regular using the
50 paired seed effects and the frozen two-sided 95% percentile bootstrap interval.
All other topology comparisons, failure-count-specific effects, and post-hoc
subgroups remain exploratory only.

## Two-layer custody model

The stage deliberately separates two artifacts.

1. The **local interpretation packet** remains outside the repository. It contains
   the retained estimate, confidence interval, preregistered classification, exact
   claim ceiling, uncertainty statement, and separation constraints.
2. The repository **`INTERPRETATION_NOTE`** contains only the SHA-256 of that local
   packet plus the accepted locked-result event identity.

This keeps the interpretation reproducible and content-addressed without turning
GitHub, CI, Notion, or chat into a storage surface for the numerical outcome.

## Fail-closed local preparation

Run the preparer only against the retained locked-analysis output whose SHA-256 is
already bound by the accepted result receipt.

```powershell
python scripts/prepare_track_a_epoch_002_interpretation_note.py `
  --analysis-output <external-retained-locked-analysis-output.json> `
  --interpretation-packet <external-new-interpretation-packet.json> `
  --output-record <candidate-TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json> `
  --parent-ref HEAD
```

The preparer:

1. revalidates the accepted locked-result history;
2. revalidates the retained analysis output against the frozen runtime/input/
   analysis identity;
3. requires the output SHA-256 to equal the digest already admitted by #851;
4. revalidates the exact Epoch 002 preregistration contract;
5. derives the interpretation only from the preregistered classification rule;
6. preserves the exact Track A claim ceiling;
7. rejects Epoch 001, Epoch 003, Epoch 004, structural-diagnostic, or exploratory
   pooling into the confirmatory interpretation;
8. writes the numerical interpretation packet outside the repository;
9. writes a separate repository-safe `INTERPRETATION_NOTE` candidate containing
   only the packet digest and accepted-result event identity.

The command prints the packet path and SHA-256 but does not print the estimate,
confidence interval, or classification.

## Repository event contract

A future interpretation-note admission event must be:

- exactly one parent;
- exactly one changed path:
  `docs/experiment/track_a_runs/TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json`;
- creation-only and first-and-only history for that path;
- based on the exact accepted protected-main parent;
- byte-preserving for the accepted locked-analysis result record;
- bound to the accepted locked-result event and the external interpretation
  packet SHA-256;
- `authorization_effect=NONE`;
- `empirical_n_increment=0`;
- `canonical_dgaf_efficacy=NOT_ESTABLISHED`;
- fully non-promotional for independent validation and High-Assurance state.

A PASS on a proposed note is `VALIDATED_PENDING_ACCEPTANCE`, not an efficacy
conclusion. Any later claim-state transition remains separately governed.
