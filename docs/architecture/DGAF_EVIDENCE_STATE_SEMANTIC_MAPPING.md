# DGAF Evidence and State Semantic Mapping

**Status:** ACTIVE_NON_AUTHORIZING / SEMANTIC ALIGNMENT / NON-AUTHORIZING

## Purpose

Prevent local implementation enums from being mistaken for repository-wide scientific/evidence states, and prevent runtime transaction states from being conflated with domain lifecycle states.

## Evidence mapping

DGAF currently has two intentionally different evidence vocabularies:

1. **Canonical repository evidence ladder** in `docs/EPISTEMIC_EVIDENCE_STANDARD.md`:
   `DEFINED → IMPLEMENTED → TESTED → VERIFIED → ATTESTED → VALIDATED → EMPIRICALLY SUPPORTED`.

2. **Capability-governance local strength enum** in `scripts/dgaf_capability_evidence.py`:
   `UNKNOWN → ASSERTED → CORROBORATED → VERIFIED → INDEPENDENTLY_VERIFIED`.

These are **not equivalent scales**.

### Local enum interpretation

| Capability enum | Canonical interpretation |
|---|---|
| `UNKNOWN` | No local evidence-strength claim. Does not imply canonical status. |
| `ASSERTED` | Local assertion only. Normally below canonical `VERIFIED`; may correspond to `DEFINED` or an unsupported assertion depending on context. |
| `CORROBORATED` | Multiple/supporting local signals. Does not automatically satisfy canonical `TESTED`, `VERIFIED`, or `VALIDATED`. |
| `VERIFIED` | Local verifier outcome for the bounded capability transaction. It maps to canonical `VERIFIED` **only when** the canonical required evidence record is present: exact claim, scope, source identity, execution method, environment, provenance, retained output, and limitations. |
| `INDEPENDENTLY_VERIFIED` | Local label asserting independent verification. It maps to canonical `VALIDATED` or any independent-validation claim **only after** independence itself is evidence-bearing and the canonical validation requirements are satisfied. |

### Rule

A capability enum value may constrain authority locally, but it must never promote a repository/public claim merely by name equality.

The function `evidence_authority_monotonic` remains a K8 authority-safety primitive, not a repository claim-promotion function.

## State-machine mapping

DGAF also has multiple state systems at different abstraction layers.

### Generic transaction state machine — K4

`scripts/dgaf_capability_state_machine.py` governs a consequential transaction lifecycle:

- proposal/canonicalization;
- evidence gathering/verification;
- approval/authorization;
- preparation/commit revalidation;
- execution;
- postconditions;
- containment/recovery;
- closure.

Its states answer: **"What is the governed execution state of this action?"**

### Workflow outcome state — K7

`scripts/dgaf_capability_workflow.py` classifies execution/postcondition/recovery outcomes such as:

- `EXECUTED`;
- `EXECUTION_OUTCOME_UNKNOWN`;
- `PARTIALLY_EXECUTED`;
- `VERIFIED / FAILED / INCONCLUSIVE` postconditions;
- rollback/compensation/containment choices.

These answer: **"What happened to the attempted effect, and what recovery is required?"**

### Domain lifecycle profiles

Track/Epoch, AOSS Stage A, Mode-T, PDMAL and external-review lanes define profile-specific states such as:

- dataset lock;
- collection authorization;
- unblinding;
- materialization;
- analysis authorization;
- external review;
- freeze/closure;
- independent validation.

These answer: **"What is the governed lifecycle state of this research/assurance program?"**

They are not aliases for K4 transaction states.

## Non-equivalence examples

- `TransactionState.VERIFIED` does not mean canonical DGAF efficacy is verified.
- `VERIFIED_POSTCONDITION` does not imply independent validation.
- A Track/Epoch `CLOSED` state does not mean a runtime action's postcondition is verified.
- AOSS `AUTHORIZED` collection state does not authorize arbitrary ACP execution.
- Capability `INDEPENDENTLY_VERIFIED` cannot establish independence unless reviewer/system independence has separately been proven.

## Architectural consequence

Use:

- K4 for generic consequential-action transitions;
- K7 for execution/postcondition/recovery outcomes;
- K8 for evidence/claim ceilings;
- profile-specific state machines for scientific, assurance, or experimental lifecycles.

Shared words may be retained for readability, but their **namespace and authority effect must remain explicit**.

## Non-effect

This mapping does not change any current state, evidence status, authorization, scientific N, efficacy, or High-Assurance boundary.
