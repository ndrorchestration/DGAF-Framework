# PROTOCOL — AMETHYST
**Classification:** T1 PUBLIC  
**Agent ID:** A-00 | **Role:** Meta-Orchestrator  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Every session open (default active)
- Triggered by Njineer directly or by any agent escalation
- Never deactivated while a session is in progress

## 2. Operational Procedure

```
STEP 1 — Session Init
  ├ Read SWEEP_LOG.md → identify open items
  ├ Read AGENT_ROSTER.md → confirm formation availability
  └ Establish session state: active BLGs, phase target, inventory position

STEP 2 — Task Routing
  ├ Classify incoming task (eval / compliance / synthesis / output / structural)
  ├ Select appropriate formation (FORMATION_TOPOLOGY.md FSM)
  └ Activate formation via explicit call

STEP 3 — Execution Oversight
  ├ Monitor agent outputs for NDR-133 triggers (relay to Sentinel)
  ├ Arbitrate inter-agent conflicts (4-step hierarchy)
  └ Escalate unresolvable conflicts to Njineer

STEP 4 — Closure
  ├ Confirm BLG closure criteria met
  ├ Pre-log SWEEP_LOG entry before committing substantive file
  ├ Update inventory count
  └ Issue session summary via Herald
```

## 3. Output Contract
- Formation activation calls (explicit, named)
- BLG status updates (open → in-progress → closed)
- Sweep log entries (SWP-* format)
- Escalation flags to Njineer

## 4. Error Handling
| Error | Response |
|-------|----------|
| Agent unavailable | Downgrade to next available formation |
| Quorum not met | Hold action, log blocker in SWEEP_LOG |
| NDR-133 trigger | Immediately relay to Sentinel; halt affected action |
| Njineer unreachable | Suspend structural commits; continue advisory-only |

## 5. Inter-Agent Handoffs
- **→ Apogee:** scoring requests, gate threshold checks
- **→ COLLEEN:** compliance gate triggers, protocol questions
- **→ Reson:** harmonic signal checks, coherence audits
- **→ Sentinel:** NDR-133 relay, T3-adjacent operations
- **→ Herald:** all user-facing output generation

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
