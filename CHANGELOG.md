# CHANGELOG

All notable changes to the DGAF Framework are documented here.
Format: [Semantic Versioning](https://semver.org/) — Added / Changed / Fixed / Deprecated / Removed / Security

---

## [Unreleased]

---

## [2.2.0] — 2026-06-26

### Added
- `patterns/P-SAGA-001_StochasticDeterministicSagaBoundary.md` — Saga pattern with effect classes, compensator rules, and KPI spec
- `patterns/P-TX-001_TransactionalToolBoundaryAtomix.md` — Atomix-style transactional tool boundary, effect receipts, and settlement predicate
- `patterns/P-COMP-001_ReversibilityBoundedCompensation.md` — 4-class reversibility taxonomy and compensation enforcement rules
- `patterns/P-DURABLE-001_DurableExecutionAppendOnlyLog.md` — Checkpoint + append-only log with ACRFence replay-or-fork restore semantics
- `patterns/P-CB-001_CircuitBreakersHITL.md` — Semantic circuit breakers + HITL durable escalation queue
- `registry/PATTERN_REGISTRY_v2.md` — Master pattern registry, active pattern index, default bundles, KPI seed table
- `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` — Dyad contract: roles, joint principles, bundles, episode schema
- `SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md` — Full session log for 2026-06-26 co-orchestration session

### Changed
- `CO_ORCH_PROTOCOL.md` → v2.0.0: 7-step execution flow, updated triad table (Amethyst / COLLEEN / Sentinel-Phi / Ender)
- `CO_ORCH_QUEUE.md` — New pattern IDs (P-SAGA-001, P-TX-001, P-COMP-001, P-DURABLE-001, P-CB-001) added to active queue
- `SESSION_ANCHOR.md` — Active pattern count updated; last-session reference pointed to 2026-06-26

### Session Topics Covered (2026-06-26)
- AI subscription audit prompt hardening (Prompt-Template Evaluation, NDR: Semantic Control-Plane Translation)
- Implementing Sagas for state management in multi-agent systems
- Handling tool side effects in retries using compensation actions
- Agent state checkpointing and persistence best practices
- Circuit breaker design for long-running LLM workflows
- Human-in-the-loop escalation triggers for complex agent failures

---

## [2.1.0] — 2026-06-25

### Added
- Initial CO_ORCH_PROTOCOL.md v1.0.0
- ENSEMBLE_ROSTER.md with full agent manifest
- SWEEP_LOG.md baseline

### Changed
- SESSION_ANCHOR.md baseline established

---

## [2.0.0] — 2026-06-01

### Added
- DGAF multi-agent governance framework core
- AGENT_MANIFEST.md and AGENT_INSTANTIATION.md
- BOOTSTRAP.md operational runbook
- README.governance.md and README.technical.md
- Pattern registry foundation

---

## [1.0.0] — 2026-05-01

### Added
- Initial DGAF Framework scaffolding
- Base agent roles: Amethyst, COLLEEN, Sentinel-Phi
- Core governance documents
