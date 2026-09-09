# Audit Hallucination Corpus Intake Contract

## Purpose

This contract governs the intake and byte-level lock of the two future input
corpora required by EVAL-001 Task 4 (`audit_hallucination_rate`):

1. provenance-controlled ground-truth audit events; and
2. separately generated audit-event outputs.

It is an evaluator-governance and corpus-custody layer. It is **not** a model
evaluation, an independence attestation, or a performance result.

## Required corpus shape

Each corpus is UTF-8 JSONL containing exactly 100 JSON objects. Every object
must contain a unique non-empty string `sample_id`. The two corpora must have
exactly the same 100 sample IDs.

Ground-truth records must additionally contain all six non-null Task-4 fields:

- `role`
- `curvature`
- `contraction`
- `gate_result`
- `timestamp`
- `session_id`

Generated-output records are **not** required to contain correct or complete
Task-4 fields at intake. Missing/wrong generated fields are potential evaluation
failures, not corpus-custody failures. Intake therefore records generated-field
completeness but does not reject a structurally aligned output merely because
its audit content is poor.

## Provenance inputs

Each corpus has a separate JSON provenance object. The only structurally
required provenance field is an exact `corpus_role`:

- ground truth: `ground_truth`
- generated outputs: `generated_outputs`

Other provenance claims, including producer identity, generation process, and
claims that expected answers were unavailable, are retained verbatim and
hashed. They remain **claims** unless a separate accepted evidence record
independently verifies them.

The intake tool therefore always emits:

`generation_independence.status = NOT_VERIFIED`

A producer cannot self-promote this field by writing `independently_verified`
or similar metadata into its own provenance document.

## Exact-byte locking

`scripts/lock_audit_hallucination_corpus.py` computes SHA-256 over the exact
bytes of:

- ground-truth JSONL;
- generated-output JSONL;
- ground-truth provenance JSON; and
- generated-output provenance JSON.

It also hashes the canonical sorted aligned-sample-ID list and emits a
deterministic `DGAF_AUDIT_HALLUCINATION_CORPUS_LOCK_V1` manifest plus SHA-256
sidecar.

Any byte change, including non-semantic whitespace, changes the corresponding
corpus digest and requires a new lock manifest.

## Fail-closed conditions

Intake fails if either corpus:

- is not valid UTF-8 JSONL;
- contains a non-object record;
- has other than exactly 100 records;
- has a missing/blank `sample_id`;
- has duplicate sample IDs;
- has a sample-ID set different from the other corpus;
- or, for ground truth, lacks any required non-null Task-4 field.

Invalid/non-object provenance JSON or a mismatched `corpus_role` also fails
intake.

## Non-effects of a PASS

A lock PASS establishes only that exact corpus bytes satisfy the structural
intake contract and are mutually aligned by sample ID. It does **not** establish:

- generated-output independence from expected answers;
- truth or quality of the provenance claims;
- correctness of generated audit fields;
- BF16 execution provenance;
- model identity or model capability;
- Task-4 scoring authorization;
- an audit hallucination-rate result;
- Herald production readiness;
- DGAF efficacy;
- Track A scientific state; or
- High-Assurance authorization.

Accordingly every v1 lock manifest fixes:

- `generation_independence.status = NOT_VERIFIED`
- `task4_scoring_authorized = false`
- `performance_scoring_performed = false`
- `model_performance_result_exists = false`
- `track_a_state_effect = NONE`
- `canonical_dgaf_efficacy = NOT_ESTABLISHED`

## Handoff to Task 4

After both real corpora exist, the admissible sequence is:

1. independently preserve/prove the generation boundary so the output producer
   could not observe the expected answers;
2. lock the exact two corpus byte streams and provenance records with this tool;
3. independently retain/re-hash the lock manifest and source corpus identities;
4. create a separate acceptance record binding the verified independence
   evidence, exact corpus digests, model/runtime/precision identity, and intended
   Task-4 invocation;
5. only then load the already locked records into
   `run_audit_hallucination_rate(..., precision_mode="BF16")` and retain the
   resulting evaluation evidence.

The lock manifest itself can never satisfy step 1 or authorize step 5.

## Example

```bash
python scripts/lock_audit_hallucination_corpus.py \
  --ground-truth evidence/task4/ground_truth.jsonl \
  --generated-outputs evidence/task4/generated_outputs.jsonl \
  --ground-truth-provenance evidence/task4/ground_truth.provenance.json \
  --generated-outputs-provenance evidence/task4/generated_outputs.provenance.json \
  --output evidence/task4/audit_corpus_lock.json
```

No expected answers or generated audit contents are printed by the tool.
