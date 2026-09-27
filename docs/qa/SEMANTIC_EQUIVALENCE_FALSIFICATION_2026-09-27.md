# Bounded Semantic Equivalence Falsification — 2026-09-27

> **Evidence class:** SYNTHETIC EXHAUSTIVE BOUNDED FALSIFICATION EVIDENCE  
> **Scope:** Current declared Boolean/categorical governance input schema only  
> **Scientific effect:** NONE

## Question

Was the 13/13 parity between `C3_STRONG_POLICY_AS_CODE_V1` and the bounded
DGAF decision function merely an artifact of the selected fixed fixtures?

## Enumeration

The test exhaustively enumerates the current bounded schema:

- action states: 8;
- authority-context states: 33, including absence;
- claim states: 17, including absence;
- flow states: 25, including absence;
- total generated cases: **112,200**.

Every generated state is evaluated by both the frozen C3 strong-policy
comparator and the bounded DGAF decision function.

## Result

- total states: **112,200**
- parity: **112,200 / 112,200**
- differences: **0**
- C3 allow states: **88**
- DGAF allow states: **88**
- bounded result:
  `SEMANTICALLY_EQUIVALENT_ON_ENUMERATED_SCHEMA=true`

## Interpretation

Within the exact enumerated input schema, the current C3 conventional policy
rules reproduce the bounded DGAF function's allow/deny decisions.

This is a stronger falsification of any claim that the current decision behavior
is intrinsically unique to DGAF. The differentiating research question must now
move above simple decision-rule expressibility.

This result does **not** establish:

- architectural equivalence;
- equivalent provenance custody or evidence lifecycle;
- equivalent recovery/reconciliation semantics;
- equivalent scaling or change-management burden;
- equivalent human-oversight affordances;
- equivalent production security;
- efficacy, independent validation, compliance, certification, or SOTA status.

## Next differentiating tests

Future comparative work should focus on properties not collapsed by decision
equivalence:

1. configuration and maintenance growth under schema/rule expansion;
2. evidence-state evolution, conflict, staleness, and UNDETERMINED handling;
3. cross-workflow composition and authority laundering;
4. recovery and reconciliation after partial execution;
5. operator intervention and explanation burden;
6. provenance/receipt custody and replay across time.

Parity remains an acceptable outcome.

## Claim ceiling

Unchanged:

- `SCIENTIFIC_N_INCREMENT=0`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `STATE_OF_THE_ART=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`
