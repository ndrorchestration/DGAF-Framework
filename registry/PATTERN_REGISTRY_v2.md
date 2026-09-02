# Pattern Registry v2

**Maintained by:** COLLEEN (Institutional Memory, Archivist, Chief Librarian)  
**Enforced by:** Amethyst (Meta-Orchestrator, QA) + Sentinel-Phi (Constraint Enforcer)  
**Last updated:** 2026-09-02 — transversal dependency/agreement reconciliation  
**Registry family:** DGAF orchestration-pattern namespace; distinct from the NDR P-series.

> **Registry boundary:** This file governs DGAF orchestration patterns such as `P-SAGA-*`, `P-TX-*`, `P-COMP-*`, `P-DURABLE-*`, and `P-CB-*`. It is not the NDR unified registry. Shared terminology or similar mechanisms do not establish equivalence.

---

## Transversal Agreement Boundary

Pattern identity is distinct from experimental candidate identity, deployment identity, workflow identity, and evidence identity.

For any live candidate cycle that references this registry, the minimum cross-system identity tuple is:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

Cross-system projections in GitHub, Vercel, Notion, evidence registries, taxonomy/vocabulary registries, and Pattern Commons must use role-qualified identities.

Agreement classes:

- `ROLE DIFFERENCE` — intentionally distinct semantic roles.
- `HISTORICAL DIFFERENCE` — prior identity retained for provenance and explicitly non-closing.
- `TRANSVERSAL DRIFT` — incompatible live projections without an intentional role distinction.
- `BLOCKING CONTRADICTION` — discrepancy capable of invalid evidence transfer or governance transition.

A pattern registry entry does not itself establish implementation, verification, freeze, authorization, or empirical efficacy.

## P-35 / P-42 Relationship

`P-35` in the NDR namespace is **Procluding Premise Gate**. `P-42` in the NDR namespace is **Adaptive Harmonic Governance**. These IDs are not members of this DGAF `P-*` namespace unless explicitly registered here.

The current P-35 remediation requires an explicit `premise_check_fn` engineering dependency at the DGAF/TGL/ConsensusTask boundary. This is not a declaration of a PDMAL-specific constitutional premise policy.

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
3. Have the manifest signed off by Amethyst (QA) and archived by COLLEEN.

No pattern manifest → no execution. This is a hard gate enforced by Sentinel-Phi.

The co-orchestration contract must also preserve the transversal identity tuple when the workflow participates in candidate-bound experimental verification. A pattern manifest cannot substitute for candidate/deployment/evidence binding.

---

## KPI Summary (COLLEEN updates per run)

| Pattern | Success Rate | Rollback Freq | HITL Rate | Last Run |
|---|---|---|---|---|
| P-SAGA-001 | — | — | — | 2026-06-26 (registered) |
| P-TX-001 | — | — | — | 2026-06-26 (registered) |
| P-COMP-001 | — | — | — | 2026-06-26 (registered) |
| P-DURABLE-001 | — | — | — | 2026-06-26 (registered) |
| P-CB-001 | — | — | — | 2026-06-26 (registered) |

KPIs populate after first real workflow run. Baseline episode schema is in `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json`.
