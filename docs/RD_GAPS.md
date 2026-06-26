# R&D Gap Log

> **Authority:** COLLEEN (Evaluation lens) | **QA:** Amethyst | **Last updated:** 2026-06-26
>
> This is the living log of open R&D gaps, hypotheses, and closure status. Every gap has an owner, a closure condition, and a link to evidence. Gaps are never deleted — closed gaps are marked CLOSED with date and commit.

---

## Gap Registry

### GAP-001 — Fluent Hallucination Closure (22% residual)

| Field | Value |
|---|---|
| Status | 🟡 PARTIAL — Phase 3B closed in harness; production wiring pending |
| First detected | 2026-05-27 Phase 2C |
| Evidence | Pattern-matching and LLM judge plateau at 78% on fluent fabricated citations |
| Root cause | "Recent peer review" and "ISO-9201 committee" semantically blend with legitimate references — rule-based systems cannot distinguish |
| Proposed closure | DemiJoule RAG grounding: every "according to X" claim verified against retrieval index before hallucination judge scores it |
| Projected closure rate | 78% → 98% (Phase 3B demonstrated in harness) |
| Closure condition | RAG grounding deployed in production Sentinel-Phi pipeline; re-benchmark confirms ≥96% detection |
| Assigned | DemiJoule + Sentinel-Phi |
| Commit evidence | Phase 3B harness commit |

---

### GAP-002 — RAG Collection Taxonomy (COLLEEN Archive → Needle Integration)

| Field | Value |
|---|---|
| Status | 🔴 OPEN |
| First detected | 2026-06-26 |
| Evidence | COLLEEN's archive lacks queryable retrieval layer; governance docs not grounded in RAG pipeline |
| Root cause | No collection taxonomy defined; risk of retrieval drift and governance confusion if single undifferentiated corpus used |
| Proposed closure | 6–8 governance-bounded collections: canon, active-context, governance-policy, architecture-patterns, evaluations, legal-compliance |
| Closure condition | Collections defined, indexed, and COLLEEN wired as query authority |
| Assigned | COLLEEN + Reson |
| Reference | Conversation 2026-06-26: NDR-03 Collections as Governance Boundaries |

---

### GAP-003 — Saga Harness End-to-End Fault Injection

| Field | Value |
|---|---|
| Status | 🔴 OPEN |
| First detected | 2026-06-26 |
| Evidence | Saga patterns (P-SAGA-001, P-TX-001, P-COMP-001, P-DURABLE-001, P-CB-001) defined but no fault injection test suite exists |
| Root cause | Patterns were spec'd from theory + conversation; no adversarial test harness yet |
| Proposed closure | Build fault injection campaign: transient tool failures (HTTP 5xx), semantic failures (bad config), mid-workflow restarts (kill + resume from checkpoint) |
| Closure condition | All 4 failure modes (Saga gap, semantic rollback attack, circuit-breaker blindness, HITL deadlock) tested and passing |
| Assigned | Amethyst + pptl harness |

---

### GAP-004 — HITL Durable Queue Production Deployment

| Field | Value |
|---|---|
| Status | 🔴 OPEN |
| First detected | 2026-06-26 |
| Evidence | HITL escalation spec'd in P-CB-001 and recovery policy JSON; no durable queue wired to production workflow engine |
| Root cause | Workflow state persistence (Temporal / LangGraph interrupted threads) not yet deployed |
| Proposed closure | Wire HITL approval as external event (Temporal signal or LangGraph interrupt); define SLA + escalation route; test deadlock scenario |
| Closure condition | HITL request survives process restart and resumes cleanly with correct checkpoint |
| Assigned | Reson + Amethyst |

---

### GAP-005 — Circuit Breaker Semantic Quality Metrics (Non-HTTP)

| Field | Value |
|---|---|
| Status | 🟡 PARTIAL — spec in P-CB-001; not yet instrumented |
| First detected | 2026-06-26 |
| Evidence | Current circuit breakers only trip on transport-level errors; semantic failures (looping, near-identical outputs, schema violations) not tracked |
| Root cause | Quality-based metrics (repeated identical tool calls, similarity threshold, schema failure count) not instrumented in Herald trace sink |
| Proposed closure | Add semantic quality metrics to Herald trace schema; threshold: 3 consecutive schema failures or 5 near-identical iterations → open breaker → fallback model or HITL |
| Closure condition | Metrics instrumented, breaker opens on semantic failures in fault injection test |
| Assigned | Herald + Sentinel-Phi |

---

### GAP-006 — Coherent Agency Formal Spec

| Field | Value |
|---|---|
| Status | 🔴 OPEN — architectural north star, not yet formalized |
| First detected | 2026-06-01 |
| Evidence | ChatGPT critique + Amethyst analysis identified that DGAF may be pointing toward a general theory of coherent agency, with governance as one subsystem |
| Root cause | Current spec mixes governance, memory, learning, and ethics without a unifying continuity-preserving agency primitive |
| Proposed closure | Formalize coherent agency model: identity continuity, policy enforcement, adaptive learning, ethical constraint as four subsystems; validate every major failure can be explained without new primitives |
| Closure condition | Formal spec published in `docs/COHERENT_AGENCY_SPEC.md`; Apogee Lens review passed |
| Assigned | Amethyst + COLLEEN |

---

## Closure Log

| Gap ID | Title | Closed | Commit |
|---|---|---|---|
| — | — | — | — |

---

## Gap Intake Template

```markdown
### GAP-{N} — {Title}

| Field | Value |
|---|---|
| Status | 🔴 OPEN / 🟡 PARTIAL / 🟢 CLOSED |
| First detected | YYYY-MM-DD |
| Evidence | ... |
| Root cause | ... |
| Proposed closure | ... |
| Closure condition | ... |
| Assigned | ... |
```
