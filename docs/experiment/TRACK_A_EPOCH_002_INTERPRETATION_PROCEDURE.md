# Track A Epoch 002 — Interpretation / Adjudication Procedure

**Status:** PROSPECTIVE TOOLING · FAIL-CLOSED · RESULT RECEIPT REQUIRED  
**Controller:** #719  
**Scientific effect of tooling:** NONE

## Purpose

Create the first governed interpretation of the accepted Track A Epoch 002 locked primary result without turning interpretation into authorization, independent validation, or a broad DGAF efficacy claim.

The numerical estimate, confidence interval, and classification remain in an operator-local interpretation artifact. The repository admits only a creation-only `INTERPRETATION_NOTE` containing the local artifact's SHA-256 and the accepted locked-result event binding.

## Preconditions

1. Protected `main` contains exactly one immutable `LOCKED_ANALYSIS_RESULT_RECORD`.
2. The retained local locked-analysis output is available outside the repository.
3. Its exact bytes revalidate against the frozen analysis/runtime/input contract.
4. Its SHA-256 equals the digest admitted by the accepted locked-result receipt.
5. No `INTERPRETATION_NOTE` already exists.

If any predicate is false or unknown, stop.

## Local preparation

Run from an exact clean checkout of accepted protected `main`:

```text
python scripts/prepare_track_a_epoch_002_interpretation_note.py \
  --analysis-output <external-retained-locked-analysis-output.json> \
  --local-interpretation-output <external-new-interpretation-artifact.json> \
  --output-record <external-new-INTERPRETATION_NOTE.json> \
  --parent-ref HEAD
```

Both output paths are creation-only. The local interpretation artifact must remain outside the repository.

The preparer prints only content addresses and paths. It does not print the estimate, interval, or classification.

## Frozen confirmatory interpretation

The local interpretation artifact preserves:

- primary topology: `pdmal`;
- primary comparator: `random_regular`;
- paired-seed count: 50;
- estimand: `estimate_pdmal_minus_random_regular`;
- interval: frozen two-sided 95% percentile bootstrap interval;
- alpha: 0.05;
- bootstrap resamples: 10,000;
- bootstrap seed: 20270251;
- exactly one confirmatory primary comparison;
- the preregistered classification rule already enforced by the locked-result validator.

No exploratory analysis may be relabeled as confirmatory.

## Mandatory limitations

The local interpretation must preserve all of the following:

- same-system / nonindependent evidence classification;
- no Epoch 001 pooling;
- no Epoch 004 substitution;
- no automatic topology-general, task-general, production, causal, or external-validity claim;
- no canonical DGAF efficacy claim;
- no independent-validation claim;
- no High-Assurance authorization claim;
- material competing interpretations appropriate to the observed classification.

## Repository admission

Only the generated `INTERPRETATION_NOTE` candidate may be copied to:

`docs/experiment/track_a_runs/TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json`

The admission event must be:

- one parent;
- one changed file;
- creation-only;
- bound to the exact accepted locked-result event;
- content-addressed to the local interpretation artifact;
- non-authorizing;
- `SCIENTIFIC_N_INCREMENT=0`;
- canonical efficacy `NOT_ESTABLISHED`.

The numerical local interpretation artifact remains outside GitHub, Notion, Drive, chat, CI inputs, workflow logs, and general projections.

## Adversarial rejection requirements

Fail closed on:

- missing or altered retained result bytes;
- result digest mismatch;
- result-event substitution;
- estimate/interval/classification inconsistency;
- modified frozen analysis identity;
- modified frozen runtime identity;
- altered confirmatory endpoint/estimand/alpha/bootstrap contract;
- exploratory relabeling;
- omitted same-system/nonindependent classification;
- omitted scope limitations;
- claim inflation;
- Epoch 001 pooling;
- Epoch 004 substitution;
- an existing interpretation note;
- multi-file admission;
- replacement or mutation of an accepted interpretation note.

## State ceiling

Acceptance of an `INTERPRETATION_NOTE` records a bounded interpretation only.

It does **not** establish canonical DGAF efficacy, independent validation, production readiness, certification, High-Assurance authorization, or a scientific-N increment.
