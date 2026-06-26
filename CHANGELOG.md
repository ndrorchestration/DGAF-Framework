# CHANGELOG

All notable changes to DGAF-Framework are documented here.
Format: `[VERSION] YYYY-MM-DD — description`

---

## [Unreleased]

---

## [2.3.0] 2026-06-26 — Cycle 4 Close: Saga Patterns + Bootstrap + Team Wiki + R&D Gap Log

### Added
- `BOOTSTRAP.md` — single-file workspace quickstart for sessions and agents
- `docs/TEAM_WIKI.md` — team onboarding, agent roles, governance authority map, glossary
- `docs/RD_GAPS.md` — living R&D gap log with 6 open items, evidence, closure conditions
- `patterns/P-SAGA-001_StochasticDeterministicSagaBoundary.md`
- `patterns/P-TX-001_TransactionalToolBoundaryAtomix.md`
- `patterns/P-COMP-001_ReversibilityBoundedCompensation.md`
- `patterns/P-DURABLE-001_DurableExecutionAppendOnlyLog.md`
- `patterns/P-CB-001_CircuitBreakersHITL.md`
- `registry/PATTERN_REGISTRY_v2.md` — master pattern registry v2
- `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` — Amethyst×COLLEEN dyad contract
- `SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md`
- `SWEEP_LOG/SWEEP_2026-06-26_Saga-HITL-Bootstrap-WikiGapClose.md`

### Updated
- `CO_ORCH_PROTOCOL.md` → v2.0.0 (7-step execution flow, triad table)
- `SESSION_ANCHOR.md` → stamped 2026-06-26, Cycle 4 closed
- `CO_ORCH_QUEUE.md` → Cycle 4 closed, Cycle 5 seeded with GAP-derived OPPs

### Patterns (Saga Cluster)
- P-SAGA-001: Stochastic-Deterministic Saga Boundary
- P-TX-001: Transactional Tool Boundary (Atomix-style)
- P-COMP-001: Reversibility-Bounded Compensation
- P-DURABLE-001: Durable Execution + Append-Only Log (ACRFence)
- P-CB-001: Semantic Circuit Breakers + HITL Escalation

### R&D Gaps Logged
- GAP-001: Fluent hallucination closure (PARTIAL — Phase 3B in harness, production pending)
- GAP-002: RAG collection taxonomy (OPEN)
- GAP-003: Saga fault injection test (OPEN)
- GAP-004: HITL durable queue production (OPEN)
- GAP-005: Semantic circuit breaker metrics (PARTIAL)
- GAP-006: Coherent Agency formal spec (OPEN)

---

## [2.2.0] 2026-06-01 — S043 + Coherent Agency Framing + Triumvirate Sweep

### Added
- S043 module: constitutional cognition + triadic reasoning formalization
- Coherent Agency framing pattern
- COLLEEN × Amethyst persistent co-orchestration loop
- CO_ORCH_QUEUE Cycle 2 + Cycle 3 OPP batches
- EvidenceVerifierProtocol + adapters
- Cross-repo coherence sweep (10 repos, QA/consistency/coherence axes)

### Updated
- CROSS_REF.md — 10-repo alignment map updated
- ENSEMBLE_ROSTER.md — all agent L-levels confirmed

---

## [2.1.0] 2026-05-27 — S042 Graduation + Cycle 1 Close

### Added
- Phase 3A: live LLM wiring (phi-pentagon + Triad-C stack)
- Phase 3B: DemiJoule RAG wiring — fluent hallucination 78% → 98%
- Phase 3C: Herald trace sink → n8n webhook
- S042 graduation commit
- CO_ORCH_QUEUE Cycle 1 (OPP-001 through OPP-008, all DONE)
- PDMAL Triumvirate pattern (P-07 + P-08)

### Updated
- SESSION_ANCHOR.md — S042 sealed
- CHANGELOG.md

---

## [2.0.0] 2026-05-27 — Phase 2 Ablation + Silent Failure Audit

### Added
- Phase 2A: smoke test (8 trace events, all 3 DGAF gates)
- Phase 2B: silent failure audit — 22% fluent hallucination gap quantified
- Phase 2C: detection architecture + chart artifacts
- CO_ORCH_QUEUE initial (Cycle 0)
- COLLEEN×Amethyst co-orchestration pattern

---

## [1.0.0] 2026-05-21 — Initial DGAF Framework

### Added
- DGAF constitutional cognition architecture
- Agent roster: Amethyst, COLLEEN, Sentinel-Phi, Herald, DemiJoule, Reson
- pptl phi-pentagon test layer
- pytest governance harness
- README.md, README.governance.md, README.technical.md
- AGENT_MANIFEST.md, AGENT_INSTANTIATION.md
- ENSEMBLE_ROSTER.md
- SECURITY.md, CONTRIBUTING.md, LICENSE
