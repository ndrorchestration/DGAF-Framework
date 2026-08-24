# DGAF OpenAI Evidence Evaluator

## Purpose

The DGAF OpenAI Evidence Evaluator provides a model-assisted semantic review of DGAF/PDMAL evidence artifacts. It is intentionally downstream of the governance system and does not replace deterministic gates.

The evaluator performs two layers:

1. **Local deterministic integrity checks** for required fields, protocol state, empirical-data declarations, and basic provenance shape.
2. **OpenAI Responses API semantic evaluation** using Structured Outputs so the assessment is returned under a fixed JSON schema.

OpenAI's Responses API supports structured JSON-schema output; the implementation uses that capability rather than parsing free-form prose. The OpenAI API is accessed with `OPENAI_API_KEY`, which must remain outside source control.

## Epistemic boundary

The evaluator can assess whether an artifact is coherent for its claimed evidence level. It cannot establish DGAF efficacy by itself.

In particular:

- implementation evidence is not efficacy evidence;
- CI evidence is not efficacy evidence;
- characterization is not empirical execution;
- contract tests are not empirical execution;
- a model-generated `PASS` is not pilot authorization;
- `N=0` remains `N=0` until actual observations are retained and provenance-linked;
- the evaluator cannot modify freeze or authorization state.

This boundary is consistent with the current DGAF control-plane state: PRE-FREEZE, no pilot authorization, and empirical N=0.

## Inputs

The evaluator accepts a JSON artifact. It expects at minimum:

- `seed`
- `protocol_status` (`PRE-FREEZE` or `FROZEN`)
- `empirical_data_collection` (boolean)

Optional fields such as `empirical_n` and `provenance` are used when present.

## Outputs

The evaluator writes a provenance-bearing JSON result containing:

- evaluator version;
- model identifier;
- evaluation timestamp;
- SHA-256 of the normalized input artifact;
- deterministic check failures;
- structured semantic decision (`PASS`, `REVIEW`, or `FAIL`);
- semantic score;
- strengths, concerns, and recommended actions;
- explicit epistemic boundary.

Deterministic failures always override a model `PASS`.

## Configuration

```text
OPENAI_API_KEY=<secret>
DGAF_EVAL_MODEL=gpt-5.6-luna   # optional
```

The default model is `gpt-5.6-luna`, selected as a cost-sensitive evaluator. The model can be changed through `DGAF_EVAL_MODEL` without changing the evaluator source.

## Usage

```bash
python tools/dgaf_openai_evaluator.py path/to/artifact.json --output evaluation.json
```

A missing API key fails closed. The key must never be committed to Git, placed in a JSON artifact, or embedded in a workflow file.

## Integration boundary

This evaluator should be treated as an **evaluation service**, not as an experimental executor. It may be invoked after contract/characterization outputs exist to assess evidence quality, but it must not be wired to silently bypass:

- protocol freeze;
- explicit pilot authorization;
- exact freeze-SHA binding;
- blinding controls;
- retention controls;
- the genuine PDMAL experimental task executor.

The current `experiments/pdmal_pilot/run_pilot.py` remains fail-closed for pilot execution until the genuine experimental executor is implemented and separately verified.
