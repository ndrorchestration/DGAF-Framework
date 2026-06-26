# P-COMP-001 — ReversibilityBoundedCompensation

**Status:** Active  
**Version:** 1.0.0  
**Registered:** 2026-06-26  
**Registered by:** Amethyst (QA) + COLLEEN (Archive)  

---

## Intent

Classify every tool side effect by reversibility class and enforce that compensation logic exists before a flow is allowed to commit. Irreversible effects must be last-in-sequence or gated by HITL.

## Effect Classes

| Class | Description | Retry? | Compensate? |
|---|---|---|---|
| `pure` | No side effect | Yes | N/A |
| `idempotent` | Safe to repeat | Yes | N/A |
| `compensable` | Has defined inverse | With idempotency key | Yes |
| `irreversible` | No algorithmic undo | Never retry blind | HITL gate required |

## Rules

1. `compensable` steps must declare a `compensator_handle` before execution.
2. `irreversible` steps must be either last in the Saga or gated by `P-CB-001` HITL.
3. Compensators run exactly once per effect in reverse Saga order.
4. On restore from checkpoint, irreversible effects are forked (not replayed) per P-DURABLE-001.

## Participants

- **Sentinel-Phi** — enforces classification at plan time; rejects flows with undeclared compensators
- **Amethyst** — sequences steps so irreversible effects are appropriately positioned
- **COLLEEN** — logs compensation execution outcomes and failure modes for pattern KPI updates

## KPIs (COLLEEN tracks)

- `compensation_success_rate`
- `irreversible_without_hitl_incidents`
- `compensator_coverage_pct`
