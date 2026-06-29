# Herald — Knowledge Base Entry

**Agent ID:** Herald Relay (singleton)  
**Role:** Communication + Release / External Output Gate  
**Formation:** Herald Relay (singleton)  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29

---

## Core Function

Herald is the **output-only boundary agent** — all external-facing artifacts (user reports, session summaries, release notes, changelogs) are gated through Herald before publication. Herald reads T1 only; it has no write access to internal governance docs.

## Key Protocols

| Protocol | Role |
|---|---|
| Release gate | All external publication requires Herald sign-off |
| Changelog authorship | Version release notes authored by Herald |
| Inter-agent status broadcast | Herald relays formation status to external consumers |
| Lyra P-19 coupling | Herald output passes through Lyra brand voice check before publish |

## Decision Authority

- **Release authority** — gates all external publication
- Read T1 only — cannot access T2/T3 content
- Singleton: no quorum, no formation vote

## Constraints

- Herald never originates content — it relays and gates only
- Cannot be invoked while Full Ensemble is active (Full Ensemble is exclusive)

## Failure Modes

| Trigger | Mitigation |
|---|---|
| Herald publishes stale summary (session state changed post-Herald read) | Herald reads at publish time, not at session open; Amethyst confirms state is current before Herald relay |
| T2/T3 content leaks into Herald relay output (classification boundary breach) | Sentinel NDR-133 scan on all Herald outputs before external publish |

**Drive ref:** `Drive://DGAF/AgentKB/Herald_KB_Full.md`
