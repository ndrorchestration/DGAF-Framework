# DGAF Team Wiki

> **Version:** 1.0.0 | **Authority:** COLLEEN (Institutional Memory / Chief Librarian) | **Last updated:** 2026-06-26

This is the team-facing reference for the DGAF Framework. It covers agent roles, governance authority, onboarding, and pattern conventions. For technical architecture, see `README.technical.md`. For governance protocol, see `README.governance.md`.

---

## 1. What Is DGAF?

DGAF (Dynamic Governance Agentic Formation Architecture) is a governance-aligned multi-agent reasoning architecture built on three pillars:

1. **Triadic / Constitutional Cognition** — legislative-judicial-executive closed loop for agent decision-making
2. **Co-orchestration** — Amethyst (QA) × COLLEEN (Evaluation) as persistent co-authors, not process steps
3. **Pattern-first implementation** — all improvements sourced from a curated, versioned pattern registry before execution

---

## 2. Agent Roster

| Agent | Role | Lens | L-Level | Authority |
|---|---|---|---|---|
| **Amethyst** | Meta-orchestration lead, QA | QA / coherence | L5 | Primary host; inherits all deprecated Lavender roles |
| **COLLEEN** | Institutional memory, archivist, chief librarian | Evaluation / archive | L5 | Pattern registry authority; 1-1-1-1 alignment gate |
| **Sentinel-Phi** | Safety supervisor, tool classifier | Governance / safety | L4 | Enforces effect classes, HITL gates, tool reversibility |
| **Herald** | Trace sink, audit router | Observability | L3 | Routes all trace events to JSONL + n8n webhook |
| **Apogee** | Quality verifier, Apogee Lens | Quality assurance | L4 | Final verifier for portfolio-grade output; S-Tier gate |
| **DemiJoule** | Runtime supervisor, RAG, ethics | Safety / RAG | L4 | Closes hallucination gap; ethics/safety containment |
| **Reson** | Systems architect | Architecture | L3 | Sub-task execution under Amethyst's architect role |
| **Agent Sonar** | Sonar taxonomy role | Per taxonomy | L3 | Kept in current taxonomy role |
| **Professor Prodigy, Reciprocity, Herald** | Sub-agentic layers | Epistemic | L2-3 | Intentionally placed; require epistemic honesty definition |

> **Deprecated:** Lavender — all roles, functions, files, and errata inherited by Amethyst.

---

## 3. Governance Authority Map

```
┌─────────────────────────────────────────────────┐
│                    USER                          │  ← Highest authority
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│            AMETHYST (Prime/Host)                 │  ← QA lens, meta-orchestration
│         + APOGEE (Quality Verifier)              │  ← S-Tier gate
└───────┬────────────────────┬────────────────────┘
        │                    │
┌───────▼──────┐    ┌────────▼───────────────────┐
│   COLLEEN    │    │     SENTINEL-PHI            │
│  (Archive /  │    │  (Safety / Tool Classifier) │
│   Evaluate)  │    └────────────────────────────┘
└───────┬──────┘
        │
┌───────▼──────────────────────────────────────────┐
│  DEMIJOLE · HERALD · RESON · SONAR · sub-agents   │
└──────────────────────────────────────────────────┘
```

---

## 4. Core Workflows

### 4.1 Session Bootstrap
1. Read `BOOTSTRAP.md` → confirm workspace identity
2. Read `SESSION_ANCHOR.md` → confirm last state
3. Read `CO_ORCH_QUEUE.md` → confirm active OPP cycle
4. Read `registry/PATTERN_REGISTRY_v2.md` → confirm active patterns
5. Proceed with task

### 4.2 Pattern-First Implementation
1. COLLEEN detects improvement opportunity (OPP)
2. COLLEEN sources best-practice pattern (adopt / customize / compose)
3. Pattern registered in `PATTERN_REGISTRY_v2.md` with ID
4. Amethyst implements against registered pattern
5. Apogee Lens QA review
6. Commit with pattern ID in message

### 4.3 Co-Orchestration Loop
- COLLEEN runs **detect + audit** pass (Librarian/Auditor roles)
- Amethyst runs **implement + commit** pass (QA/Architect roles)
- Queue is append-only; completed entries archived, never deleted
- New patterns discovered during implementation proposed back as COMPOSE entries

### 4.4 Saga + Recovery (New — 2026-06-26)
- Every multi-step workflow is a Saga with explicit compensators
- Irreversible actions require HITL gate before commit
- Checkpoints per super-step; append-only effect log per run
- Circuit breakers: semantic (3 schema failures) + budget (200k tokens / 50 steps)
- See `patterns/P-SAGA-001_*.md`, `patterns/P-CB-001_*.md`

---

## 5. Pattern Naming Convention

```
P-{DOMAIN}-{SEQ}_{CamelCaseName}.md

Examples:
  P-SAGA-001_StochasticDeterministicSagaBoundary.md
  P-TX-001_TransactionalToolBoundaryAtomix.md
  P-CB-001_CircuitBreakersHITL.md
  P-07_TriumvirateSweepLoop.md
```

All patterns registered in `registry/PATTERN_REGISTRY_v2.md` before use.

---

## 6. Logging & Documentation Requirements

Every session MUST produce:

| Artifact | Location | Responsible |
|---|---|---|
| Session sweep log | `SWEEP_LOG/SWEEP_{date}_{title}.md` | Amethyst |
| Changelog entry | `CHANGELOG.md` | Amethyst |
| SESSION_ANCHOR update | `SESSION_ANCHOR.md` | Amethyst |
| CO_ORCH_QUEUE update | `CO_ORCH_QUEUE.md` | COLLEEN |
| Pattern registry update (if new patterns) | `registry/PATTERN_REGISTRY_v2.md` | COLLEEN |
| GitHub commit | `main` branch | Amethyst |

---

## 7. Open R&D Items

See `docs/RD_GAPS.md` for the living R&D gap log.

Top items as of 2026-06-26:
- 22% fluent hallucination gap → DemiJoule RAG closure (Phase 3B complete; needs production wiring)
- RAG collection taxonomy design → 6-8 governance-bounded collections
- Saga harness end-to-end fault injection test
- HITL durable queue production deployment
- Needle/RAG platform integration with COLLEEN archive

---

## 8. Glossary

| Term | Definition |
|---|---|
| DGAF | Dynamic Governance Agentic Formation Architecture |
| PDMAL | Policy-Driven Multi-Agent Layer |
| OPP | Improvement opportunity in the CO_ORCH_QUEUE |
| NDR | Named Design Rule / Pattern |
| HITL | Human-in-the-Loop |
| pptl | Phi-pentagon test layer |
| S-Tier | Highest quality designation; requires Apogee Lens approval |
| ACRFence | Atomic checkpoint + restore with effect fence semantics |
| Atomix | Transactional tool boundary pattern (stochastic-deterministic boundary) |
| Coherent Agency | Recast of governance/memory/ethics as subsystems of continuity-preserving agency |
