# AOSS v0.6 Stage A — Prospective Decision Policy Freeze

**Controller:** #810  
**Status:** FROZEN PRE-DATA CONTRACT / NON-AUTHORIZING  
**Policy:** `AOSS_V0_6_STAGE_A_POLICY_V1`

The historical v0.5 executable decision-policy source was not located. This contract therefore does **not** claim to recover v0.5 implementation behavior. It prospectively freezes a new v0.6 Stage-A policy before any Stage-A outcome collection.

The design basis is the canonical AOSS research workstream's pre-data reference decision table and governing semantics. The executable implementation is:

- `scripts/aoss_v0_6_stage_a_decision_policy.py`
- Git blob: `dd03a34fe17579c57dcf386abac9f1f5e7eb23de`
- entrypoint: `evaluate_policy(PolicyInput) -> PolicyResult`

## Frozen precedence

1. `TERMINAL → RECORD_OUTCOME`
2. `BLOCKED → ESCALATE_BLOCK`
3. `DEADLOCK_CANDIDATE → PERTURB`
4. `CONFLICTED → ESCALATE_CONFLICT`
5. `UNCERTAIN → REQUEST_EVIDENCE`
6. `AUTHORIZED ∧ VALIDATED ∧ PROVENANCE_VALID ∧ no required predicate INCONCLUSIVE → EXECUTE`
7. `VALIDATED ∧ ¬AUTHORIZED → REQUEST_AUTHORIZATION`
8. any required predicate `INCONCLUSIVE → HOLD`
9. otherwise → `HOLD`

Only `EXECUTE` is execution-bearing. Invalid inputs fail closed to `HOLD`. `EXECUTE` is impossible unless authorization, validation, and provenance are all explicitly `TRUE` and no required predicate is inconclusive.

## Boundary

This is a Stage-A research decision policy, not a DGAF authorization mapping and not production authority. It does not authorize data collection, establish external validation, establish efficacy or superiority, increment scientific N, or resolve the separate ACP→`(O,M,R)` comparator-input derivation gap.

Machine-readable contract:

- `registry/aoss_v0_6_stage_a_decision_policy_v1.json`
