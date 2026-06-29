# The Librarian — Knowledge Base Entry

**Agent ID:** A-06 (Operational Swarm)  
**Role:** Archive / Provenance Traceability  
**Formation:** Operational Swarm  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29

---

## Core Function

The Librarian archives **every decision** in the formation — the Provenance Traceability guarantee. No decision that passes through the Operational Swarm may be canonical without a Librarian archive entry. The Librarian is the audit trail anchor for the Yggdrasil trunk.

## Key Protocols

| Protocol | Role |
|---|---|
| NDR-Protocol-01 (step 3) | COLLEEN → Librarian archive hand-off after Actualizer writes |
| Provenance Traceability | Every decision: who decided, when, which agent, which protocol |
| Batch 1A extraction support | Archives extraction decisions as COLLEEN closes the 31.25% gap |

## Decision Authority

- **Archive authority** — canonical decision log
- No normative decisions; archive-only lane (parallel to COLLEEN’s continuity lane)

## Failure Modes

| Trigger | Mitigation |
|---|---|
| Archive entry missing for a canonical decision (gap in Provenance Traceability) | COLLEEN BLG surface flags missing archive; Librarian backfills from session context before seal |
| Archive entry exists but references wrong agent/protocol (provenance contamination) | Apogee evidence scoring cross-checks Librarian entries against SWEEP_LOG before certification |

**Drive ref:** `Drive://DGAF/AgentKB/TheLibrarian_KB_Full.md`
