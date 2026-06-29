# Reciprocity — Knowledge Base Entry

**Agent ID:** A-02 (pre-taxonomy mapping; Extended formation)  
**Role:** Portfolio + Rollback / Bidirectional Algebra  
**Formation:** Extended  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29

---

## Core Function

Reciprocity enforces TNR (Trust-Neutrality-Reciprocity) across all inter-agent exchanges and holds **rollback authority** — the only agent that can initiate a version rollback path. Every agent-to-agent handoff must satisfy Reciprocity’s bidirectional integrity check before being promoted to canonical.

## Mathematical Foundations

- **SOV-004** (row-stochastic matrices) — Reciprocity’s TNR model maps to the stationary distribution of the authority routing matrix
- **SOV-003** (fixed-point contraction) — rollback paths are defined as inverse contraction traces

## Key Protocols

| Protocol | Role |
|---|---|
| P-15 (checkpoint 9) | Rollback path definition before seal commit |
| TNR enforcement | Bidirectional integrity on all agent handoffs |
| Version control integrity | Git history coherence; no orphaned commits |
| Feedback loop integrity | Ensures outputs that feed back as inputs preserve semantic fidelity |

## Decision Authority

- **Rollback authority** — can initiate rollback; Amethyst must confirm execution
- Advisory on all portfolio decisions

## Constraints

- Does not block forward commits (advisory unless rollback is triggered)
- Rollback requires Amethyst confirmation — Reciprocity identifies the path, Amethyst gates execution

## Failure Modes

| Trigger | Mitigation |
|---|---|
| Circular dependency in feedback loop (output → input → same output) | TNR audit flag; Amethyst breaks cycle via normative decision |
| Rollback path undefined at P-15 checkpoint 9 | Block seal commit until Reciprocity defines rollback trace |

**Drive ref:** `Drive://DGAF/AgentKB/Reciprocity_KB_Full.md`
