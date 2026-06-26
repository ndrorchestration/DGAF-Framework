# Changelog

All notable changes to DGAF-Framework are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [2026-06-26] — Session: Saga / Tx / Checkpoint / CB / HITL Sweep

### Added
- `patterns/P-SAGA-001_StochasticDeterministicSagaBoundary.md` — Saga pattern for multi-agent state management; effect class taxonomy (pure/idempotent/compensable/irreversible); compensator contract enforcement rules; Amethyst-as-Saga-engine specification.
- `patterns/P-TX-001_TransactionalToolBoundaryAtomix.md` — Atomix-style transactional shim at the stochastic–deterministic boundary; effect receipts; idempotency keys; delayed-commit settlement predicate.
- `patterns/P-COMP-001_ReversibilityBoundedCompensation.md` — 4-class reversibility taxonomy; compensation action spec; Sentinel-Phi enforcement of compensator completeness at plan-load time.
- `patterns/P-DURABLE-001_DurableExecutionAppendOnlyLog.md` — Per-run checkpoint + append-only event log; ACRFence replay-or-fork restore semantics for irreversible effects; resume-without-replay guarantee.
- `patterns/P-CB-001_CircuitBreakersHITL.md` — Semantic circuit breakers (schema failure threshold, loop detection, budget breaker); HITL durable escalation queue; SLA + escalation-route specification; persist-then-pause-then-resume flow.
- `registry/PATTERN_REGISTRY_v2.md` — Master pattern registry; all five new patterns indexed; default bundles (Minimal, Standard, Full); KPI seed table for COLLEEN baseline population.
- `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` — Dyad contract; Amethyst + COLLEEN roles; joint operating principles; pattern bundles; episode schema for runtime provenance logging.
- `SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md` — Full session log: topics covered, files created/updated, coherence notes, open items at session close.

### Updated
- `CO_ORCH_PROTOCOL.md` → v2.0.0 — 7-step execution flow; triad table (Amethyst / COLLEEN / Sentinel-Phi / Ender); Saga + Tx layer integrated into step definitions.
- `CHANGELOG.md` — This entry.
- `SESSION_ANCHOR.md` — Active pattern count, last session reference, open item resolution status.
- `CO_ORCH_QUEUE.md` — New pattern IDs appended to active queue; session sweep marked complete.

### Governance Notes
- All five patterns reviewed under Apogee Lens criteria: source-grounded, uncertainty-bounded, auditable.
- DemiJoule safety check applied: no irreversible-by-default tool patterns; all HITL gates are durable.
- Pattern IDs follow `P-{DOMAIN}-{SEQ}` convention established in PATTERN_REGISTRY_v2.
- COLLEEN episode schema is now authoritative for runtime KPI population; see `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json`.

---

## [2026-06-25] — Prior Session Reference

> See `SWEEP_LOG.md` for earlier session history predating this changelog entry.

---

## Format Reference

- **Added** — new files, features, patterns, agents
- **Updated** — changes to existing files
- **Removed** — deprecated or deleted items
- **Fixed** — corrections to prior entries
- **Governance Notes** — Apogee Lens / DemiJoule review outcomes
