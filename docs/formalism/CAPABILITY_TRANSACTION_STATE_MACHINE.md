# DGAF Capability Transaction State Machine

> **Status:** PROSPECTIVE / NON-AUTHORIZING  
> **Implementation:** `scripts/dgaf_capability_state_machine.py`  
> **Parent formalism:** `AGENT_GOVERNANCE_TRANSITION_SPEC.md`

## Purpose

This bounded finite-state model makes the capability-governance transaction order and guard obligations executable.

It does not replace the broader agent-governance formalism. It is a reference model for the provider-neutral capability path on draft PR #1041.

## Nominal path

```text
PROPOSED
 -> CANONICALIZED
 -> EVIDENCE_GATHERING
 -> VERIFICATION_PENDING
 -> VERIFIED
 -> APPROVAL_PENDING
 -> AUTHORIZED
 -> PREPARED
 -> COMMIT_REVALIDATION
 -> COMMIT_REVALIDATED
 -> EXECUTING
 -> EXECUTED
 -> POSTCONDITION_PENDING
 -> VERIFIED_POSTCONDITION
 -> CLOSED
```

When policy does not require a separate approval event, `VERIFIED -> AUTHORIZED` is permitted only if the authorization guards themselves are satisfied.

## Refusal and uncertainty paths

Verification may become `INCONCLUSIVE`, followed only by rejection or escalation.

Execution may become `EXECUTION_OUTCOME_UNKNOWN`. That state does not permit direct retry or historical rewriting. It routes to containment/reconciliation or escalation.

Postconditions may become `POSTCONDITION_FAILED` or `POSTCONDITION_INCONCLUSIVE` without erasing the prior `EXECUTED` state.

## Recovery paths

```text
EXECUTED / POSTCONDITION_* / EXECUTION_OUTCOME_UNKNOWN
 -> CONTAINMENT
 -> ROLLBACK_PENDING | COMPENSATION_PENDING | ESCALATED
 -> ROLLED_BACK | COMPENSATED | RECOVERY_FAILED
 -> CLOSED | ESCALATED
```

Recovery mode must be explicit. Compensation is a new governed action and is not equivalent to erasing the original execution.

## Guard obligations

The executable model binds representative guards to transition targets:

- canonicalization must exist before `CANONICALIZED`;
- required evidence must exist before verification begins;
- failed or inconclusive required verification cannot become `VERIFIED`;
- `AUTHORIZED` requires independent active/scoped authorization, non-widening delegation, and any required exact-action approval;
- `COMMIT_REVALIDATED` requires active/unconsumed authority, unchanged digest, passing state guards, and replay-safe idempotency state;
- `EXECUTING` is reachable only from `COMMIT_REVALIDATED`;
- `EXECUTED` requires execution-receipt evidence;
- unknown outcome is explicit and distinct from failure;
- postcondition result is independently represented;
- closure requires a terminal/settled state plus an audit record.

## Evidence boundary

Passing this finite model establishes only bounded state/guard consistency for the modeled transitions. It does not prove distributed correctness, production security, provider honesty, independent validation, scientific efficacy, or High-Assurance authorization.
