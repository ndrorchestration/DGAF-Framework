# Matched Composition and Recovery — Paired Falsification Result

> **Evidence class:** SYNTHETIC PAIRED-IMPLEMENTATION FALSIFICATION EVIDENCE  
> **Scope:** merged DGAF reference APIs versus a stateful conventional-policy comparator  
> **Scientific effect:** NONE

## Question

After decision, semantic-equivalence, and configuration-scaling parity, does DGAF
retain a unique behavioral advantage on composition and recovery when the
conventional comparator is allowed ordinary stateful engineering primitives?

## Fairness constraints

The conventional comparator receives:

- workflow context and sensitivity propagation;
- composition authorization state;
- idempotency state;
- unknown-outcome state;
- reconciliation state;
- structured recovery decisions.

DGAF receives no hidden oracle input unavailable to the comparator.

## Bound DGAF implementation

This benchmark exercises the merged protected-main reference APIs from:

- `scripts/dgaf_capability_workflow.py`;
- `scripts/dgaf_capability_idempotency.py`.

The compared behaviors include:

- composition authorization;
- protected egress blocking;
- unknown provider outcomes;
- reversible partial execution;
- compensatable partial execution;
- irreversible partial execution;
- failed postconditions;
- idempotency retry blocking;
- reconciliation before retry.

## Result

Across 11 paired synthetic cases:

- parity: **11/11**;
- differences: **0**;
- wrong-authority continuations: **0 for both**;
- stale-retry continuations: **0 for both**;
- explicit reconcile/escalation cases: **2**.

Observed outcome:

`NO_UNIQUE_COMPOSITION_OR_RECOVERY_ADVANTAGE_IN_MATCHED_SEMANTICS_CASES`

This is a falsification-friendly result. It weakens any claim that the current
bounded composition/recovery semantics are inherently unique to DGAF when a
conventional policy system is permitted comparable state, workflow context,
idempotency, and reconciliation mechanisms.

## What remains open

This benchmark does not measure:

- real provider failures;
- durable provenance custody across independent systems;
- operator time or ambiguity;
- implementation complexity;
- schema migration burden;
- incomplete observability;
- concurrent races across distributed components;
- real compensation/rollback side effects.

Those are better next candidates for discriminating architecture behavior.

## Claim ceiling

Unchanged:

- `SCIENTIFIC_N_INCREMENT=0`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `STATE_OF_THE_ART=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`
