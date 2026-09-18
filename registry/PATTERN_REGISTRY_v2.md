# Pattern Registry v2

**Maintained by role:** `role.continuity-archive-coordinator`  
**Governance review:** `role.governance-orchestrator` + `role.evidence-verification-reviewer`  
**Scoped containment:** `role.security-containment-gate`  
**Identity provenance:** historical persona labels and legacy filenames resolve through `governance/persona_role_lineage.v1.json`; they do not grant authority.  
**Last updated:** 2026-06-26  

---

## Active Patterns

| ID | Name | Domain | Status | File |
|---|---|---|---|---|
| P-SAGA-001 | StochasticDeterministicSagaBoundary | Multi-agent orchestration | Active | `patterns/P-SAGA-001_StochasticDeterministicSagaBoundary.md` |
| P-TX-001 | TransactionalToolBoundaryAtomix | Tool safety | Active | `patterns/P-TX-001_TransactionalToolBoundaryAtomix.md` |
| P-COMP-001 | ReversibilityBoundedCompensation | Side-effect recovery | Active | `patterns/P-COMP-001_ReversibilityBoundedCompensation.md` |
| P-DURABLE-001 | DurableExecutionAppendOnlyLog | State persistence | Active | `patterns/P-DURABLE-001_DurableExecutionAppendOnlyLog.md` |
| P-CB-001 | CircuitBreakersHITL | Resilience + governance | Active | `patterns/P-CB-001_CircuitBreakersHITL.md` |
| P-PIER-001 | PlanExecuteInspectReplan | Reasoning flow | Active | (prior registry) |
| P-MEM-001 | TieredContextAgenticMemory | Memory architecture | Active | (prior registry) |
| P-POL-001 | PolicyAwareToolGuards | Governance gates | Active | (prior registry) |

---

## Default Bundles

### low_risk_retrieval_flow

`P-PIER-001`, `P-DURABLE-001`, `P-MEM-001`

### medium_risk_workflow

`P-SAGA-001`, `P-DURABLE-001`, `P-CB-001`

### high_risk_state_mutation

`P-SAGA-001`, `P-TX-001`, `P-COMP-001`, `P-DURABLE-001`, `P-CB-001`, `P-POL-001`

---

## Co-Orchestration Contract

All workflows must:

1. Select a bundle or explicit pattern list from this registry before execution.
2. Produce a pattern manifest (see `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` for schema).
3. Have the manifest reviewed under the applicable `role.evidence-verification-reviewer` / `role.governance-orchestrator` contract and archived by `role.continuity-archive-coordinator`.

No required pattern manifest → no execution where the governing contract makes the manifest a prerequisite. Fail-closed containment is scoped to `role.security-containment-gate`; this registry does not create additional authority by itself.

---

## KPI Summary (`role.continuity-archive-coordinator` updates per run)

| Pattern | Success Rate | Rollback Freq | HITL Rate | Last Run |
|---|---|---|---|---|
| P-SAGA-001 | — | — | — | 2026-06-26 (registered) |
| P-TX-001 | — | — | — | 2026-06-26 (registered) |
| P-COMP-001 | — | — | — | 2026-06-26 (registered) |
| P-DURABLE-001 | — | — | — | 2026-06-26 (registered) |
| P-CB-001 | — | — | — | 2026-06-26 (registered) |

KPIs populate after first real workflow run. Baseline episode schema is in `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json`.

## Current authority boundary

The legacy filename `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` is retained for compatibility/provenance. Its persona-bearing filename does not supersede `governance/role_capability_registry.v1.json` or create a current authority seat.
