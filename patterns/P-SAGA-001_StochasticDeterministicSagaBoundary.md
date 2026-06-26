# P-SAGA-001 — StochasticDeterministicSagaBoundary

**Status:** Active  
**Version:** 1.0.0  
**Registered:** 2026-06-26  
**Registered by:** Amethyst (QA) + COLLEEN (Archive)  
**Apogee Lens:** Pending first run review  

---

## Intent

Decouple LLM stochasticity from deterministic state mutation by treating every multi-step agent workflow as a Saga over semantic steps, each with a declared compensator and reversibility class.

## Context

Applies to any multi-agent flow where one or more steps mutate external state (file writes, API calls, payments, notifications). The LLM proposes steps; a deterministic Saga engine commits or compensates.

## Structure

```json
{
  "saga_step": {
    "id": "string",
    "owner_agent": "string",
    "do": "ToolOrAgentCall",
    "compensator": "OptionalCompensationCall | null",
    "reversible": "bool",
    "effect_class": "pure | idempotent | compensable | irreversible"
  },
  "on_failure": "rollback_compensable_then_abort",
  "engine": "centralized_in_amethyst"
}
```

## Participants

- **Amethyst** — selects and wires the Saga configuration for each workflow
- **COLLEEN** — archives run manifests and per-step outcomes; computes KPIs
- **Sentinel-Phi** — enforces effect_class declarations; rejects plans with missing compensators on compensable steps

## Default Bundles

| Risk Profile | Included Patterns |
|---|---|
| low_risk_retrieval | PlanExecuteInspectReplan, DurableExecutionAppendOnlyLog |
| medium_risk_workflow | P-SAGA-001, DurableExecutionAppendOnlyLog, CircuitBreakersHITL |
| high_risk_state_mutation | P-SAGA-001, P-TX-001, P-COMP-001, P-DURABLE-001, P-CB-001, PolicyAwareToolGuards |

## Consequences

- **Benefit:** Auditable, compensable multi-step flows with no resource locks
- **Cost:** Every compensable step must have a tested compensator defined before execution

## Known Failures

- **Saga gap:** Missing compensator on compensable step → broken invariants post-rollback. Mitigation: Sentinel-Phi compile-time check.
- **Silent partial rollback:** Compensators run but don't fully restore state. Mitigation: verifier sub-agent post-compensate.

## KPIs (COLLEEN tracks)

- `success_rate` — steps completed without rollback
- `rollback_frequency` — partial or full Saga rollbacks per 100 runs
- `compensator_coverage` — % of compensable steps with tested compensators
