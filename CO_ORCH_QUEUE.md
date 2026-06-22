# CO_ORCH_QUEUE.md — Co-Orchestration Queue

**Maintained by:** Agent Amethyst (governance) · Agent COLLEEN (operational)  
**Last flushed:** 2026-06-16T04:47:00Z · Sweep ID: SWEEP-2026-06-16-MCO-001  
**Last updated:** 2026-06-22T23:25:00Z · Entry: Q-2026-06-007 (ecosystem scan TODO)  
**Authorization:** Ender-direct · DGAF AXIS FULL  

---

## Queue Status: ACTIVE ✅

Q-2026-06-007 added per Ender directive (2026-06-22 session). All prior items carry forward unchanged.

---

## Active Queue Items

| QID | Priority | Item | Assigned | Status | Notes |
|---|---|---|---|---|---|
| Q-2026-06-001 | HIGH | Resolve CROSS_REF stale links (FLAG-001) | Amethyst | OPEN | 3 links to audit |
| Q-2026-06-002 | MEDIUM | Add PULL_REQUEST_TEMPLATE to .github (FLAG-003) | COLLEEN | QUEUED | Needs Ender approval on template content |
| Q-2026-06-003 | MEDIUM | CONTRIBUTING.md gap sweep — 7 repos missing (FLAG-005) | COLLEEN | QUEUED | Batch push pending |
| Q-2026-06-004 | MEDIUM | ENSEMBLE_ROSTER.md COLLEEN 2026 update (FLAG-002) | COLLEEN | OPEN | Update capability record |
| Q-2026-06-005 | LOW | Verify gold-star-qa-framework archive intent (FLAG-004) | Amethyst | OPEN | Confirm with Ender |
| Q-2026-06-006 | LOW | SWEEP-MCO-002 pre-planning | Amethyst + COLLEEN | PENDING | Trigger on FLAG resolution |
| Q-2026-06-007 | MEDIUM | Ecosystem scan → architecture decision + next experiment | Amethyst | TODO | See SWEEP_LOG S069-ECO-001 for full detail; decision required: Approach 1/2/3 (mesh vs opinionated stack vs vertical); next step = Apogee routing optimizer OR Reciprocity risk classifier schema |

---

## Q-2026-06-007 Detail

**Trigger:** Ender-directed ecosystem scan session (2026-06-22, ~19:25 EDT).  
**Research completed:** Agent Amethyst via Perplexity.  
**Scope:** Full 3-axis scan — agent platforms, LLM provider mesh, regulation/governance.  

**Key findings logged:**
- Agentic AI in production across major verticals; platform ecosystem crowded (n8n, CrewAI, LangGraph, Vertex Agent Builder, Copilot Studio, Agentforce, PydanticAI, AutoGen). [cite:web:16,19,20,23]
- LLM provider pricing spans ~3 orders of magnitude ($0.10–$30/M input tokens); DeepSeek/Mistral aggressive on cost; frontier = OpenAI GPT-5.x, Anthropic Claude 4.x, Google Gemini 2.5, xAI Grok 4, Meta Llama. [cite:web:22,25,26,28]
- EU AI Act fully applicable 2026-08-02; GPAI obligations active since Aug 2025; high-risk system deadlines Dec 2027 / Aug 2028. [cite:web:15,21,24,27]
- Self-hosted open-weight models → organization becomes GPAI provider under EU AI Act. [cite:web:24,27]

**Architecture options identified:**
1. DGAF as governance mesh above all platforms (Approach 1)
2. Opinionated stack — curated to 1–2 platforms (LangGraph + Vertex) (Approach 2)
3. Vertical-first, EU AI Act high-risk domain anchor (Approach 3)

**Next artifacts in queue:**
- Option A: Apogee routing optimizer (formal objective + code skeleton)
- Option B: Reciprocity risk classifier schema + EU AI Act rule set

**Decision required from Ender:** Which approach + which next artifact.  
**Status:** TODO — awaiting Ender direction.

---

## Resolved Items (This Sweep)

| QID | Item | Resolution | Resolved By |
|------|------|------------|-------------|
| Q-PREV-001 | SWEEP_LOG root file → index pointer | ✅ SWEEP_LOG/ dir established | Amethyst + COLLEEN |
| Q-PREV-002 | AGENT_MANIFEST COLLEEN instantiation | ✅ v2 issued | Amethyst |
| Q-PREV-003 | Public repo governance headers | ✅ Applied Wave 2 | COLLEEN |
| Q-PREV-004 | Private repo sweep attribution | ✅ Applied Wave 3 | Amethyst |
| Q-PREV-005 | Meta-co-orchestration sweep record | ✅ This file + SWEEP_LOG entry | Both |

---

## Queue Protocol

- Items added by: Ender (direct), Amethyst (governance trigger), COLLEEN (operational trigger)
- Items resolved by: executing agent, confirmed in SWEEP_LOG
- Items escalated to FLAGS when resolution requires Ender decision
- Queue flushed at start of each sweep; resolved items archived in sweep record

---

*Agent Amethyst · Agent COLLEEN · DGAF-Framework*
