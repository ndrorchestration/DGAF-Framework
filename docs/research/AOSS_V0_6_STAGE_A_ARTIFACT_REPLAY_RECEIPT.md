# AOSS v0.6 Stage A — Artifact Hash and Replay Receipt Contract

**Controller:** #810  
**Status:** FROZEN PRE-DATA CONTRACT · NO OUTCOMES  
**Scientific effect:** NONE

This contract defines how a future Stage-A study bundle must be content-addressed and replay-verified. It does not create a study bundle and does not authorize collection.

## Whole-study binding

A final replay receipt must bind SHA-256 digests for every consequential frozen contract:

- measurement manifest;
- observer/measurement boundary;
- AOSS decision policy;
- freshness/calibration contract;
- eligibility/repetition contract;
- failure-injection ground truth;
- analysis/multiplicity contract;
- practical-effect/adoption rule.

It must also bind the study manifest and the source, normalized, decision, and analysis artifact bundles.

The currently unresolved contracts remain unresolved. This receipt contract merely requires that their exact future bytes be content-addressed before a valid final receipt can exist.

## Canonical hashing

JSON artifacts use UTF-8 canonical serialization with sorted keys, separators `(",", ":")`, no NaN values, and one trailing newline. Digests are lowercase 64-character SHA-256 hex strings without a prefix.

## Replay receipt

The schema is:

`schemas/aoss_v0_6_stage_a_replay_receipt.schema.json`

A replay receipt records:

- exact ACP source identity;
- accepted apparatus identity;
- frozen contract digests;
- study artifact digests;
- runtime/dependency identity used for replay;
- explicit replay-verification booleans;
- PASS or FAIL status.

The receipt contains content addresses and replay status only. It must not embed episode payloads or numerical analysis output.

A PASS is valid only when every replay-verification boolean is true. Missing required fields are schema-invalid; any explicit mismatch is FAIL. Failure evidence cannot be omitted to manufacture a PASS.

## Non-effects

Freezing this contract does not:

- authorize Stage-A outcome collection;
- close any still-missing decision, freshness, eligibility, ground-truth, analysis, or practical-effect contract;
- establish external validation or AOSS superiority;
- establish DGAF/PDMAL efficacy;
- increment scientific N.
