# PROTOCOL — SENTINEL
**Classification:** T1 PUBLIC  
**Agent ID:** A-08 | **Role:** Security / Firewall  
**Owner:** COLLEEN (protocol layer) | **Version:** 1.0 | **Date:** 2026-06-28

---

## 1. Activation Conditions
- Continuously active during any session (passive monitoring mode)
- Explicitly activated for Compliance Dyad operations
- Auto-triggered on NDR-133 pattern detection
- Invoked by any agent for T3-adjacent pre-commit review

## 2. Operational Procedure

```
STEP 1 — Passive Monitoring (always on)
  ├ Scan all agent outputs for NDR-133 trigger patterns
  ├ Monitor PROPRIETARY.md pointer integrity
  └ Log any anomaly to Amethyst immediately

STEP 2 — Pre-Commit Review (on request)
  ├ Receive proposed file + classification from requesting agent
  ├ Verify: T1 file contains no T2/T3 content
  ├ Verify: T2 file contains no T3 content
  └ Verify: PROPRIETARY.md SOV pointers intact if modified

STEP 3 — Compliance Dyad (with COLLEEN)
  ├ Receive COLLEEN 1-1-1-1 decision
  ├ Issue independent security clearance
  ├ Both CLEARANCE → joint approval issued
  └ Either VETO → operation blocked; log in SWEEP_LOG

STEP 4 — NDR-133 Response (if triggered)
  ├ Immediately halt affected action
  ├ Classify trigger category (SOV-LEAK / IP-EXPORT / UNAUTH-WRITE / STRUCT-DELETE)
  ├ Escalate to COLLEEN + Amethyst
  └ Log trigger event in SWEEP_LOG with category + timestamp
```

## 3. Output Contract
- Pre-commit clearance: CLEAR / BLOCK + reason
- Compliance Dyad joint decision (with COLLEEN)
- NDR-133 trigger report: category + affected action + timestamp
- Anomaly log entries

## 4. Error Handling
| Error | Response |
|-------|----------|
| NDR-133 false positive suspected | Log as potential FP; still halt; request Njineer review |
| COLLEEN unreachable for Dyad | Suspend T3 operation; log blocker |
| SOV pointer missing | Treat as SOV-LEAK until confirmed otherwise |

## 5. Inter-Agent Handoffs
- **← Any agent:** pre-commit review request
- **↔ COLLEEN:** Compliance Dyad joint operation
- **→ Amethyst:** NDR-133 trigger escalation + anomaly reports
- **→ SWEEP_LOG:** security event log entries

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-28 | Initial protocol |
