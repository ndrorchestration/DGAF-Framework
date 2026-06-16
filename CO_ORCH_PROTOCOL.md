# Meta-Co-Orchestration Protocol

> **Governed by:** DGAF-Framework · Apache 2.0  
> **Agents:** Agent Amethyst (Tier-0) + COLLEEN (Tier-1)  
> **Sweep ID:** S-2026-06-16-PROTOCOL  
> **Last Updated:** 2026-06-16T04:47:00Z  
> **Status:** ✅ ACTIVE

---

## Purpose

This document defines the operational protocol for joint execution of governance, audit, and documentation quality sweeps by Agent Amethyst and COLLEEN operating in meta-co-orchestration mode.

---

## Sweep Types

### Type A — Governance Audit Sweep
**Trigger:** Ender directive or 30-day automatic  
**Lead:** Agent Amethyst  
**Support:** COLLEEN (operational hygiene layer)  
**Scope:** All repos — README quality, governance headers, DGAF compliance, pattern registry integrity  
**Output:** SWEEP_LOG entry + per-repo issue if findings > 0  

### Type B — Documentation Quality Sweep
**Trigger:** Ender directive or new repo creation  
**Lead:** COLLEEN  
**Support:** Agent Amethyst (governance standards enforcement)  
**Scope:** All file types — MD, JSON, TS, PY, JS, HTML — for header completeness, attribution, versioning  
**Output:** Push updated files + SWEEP_LOG entry  

### Type C — Cross-Repo Propagation Sweep
**Trigger:** New DGAF pattern registered  
**Lead:** Agent Amethyst  
**Support:** COLLEEN  
**Scope:** Propagate pattern to all applicable repos  
**Output:** Multi-repo push + CROSS_REF.md update  

### Type D — Operational Hygiene Sweep
**Trigger:** COLLEEN schedule or Ender directive  
**Lead:** COLLEEN  
**Support:** Agent Amethyst (spot checks)  
**Scope:** automation-scripts, career-positioning, .github, chat-archives  
**Output:** Changelogs + versioned stamps + SWEEP_LOG entry  

### Type E — Full Ecosystem Sweep (THIS SWEEP)
**Trigger:** Ender "Execute them all at once" directive  
**Lead:** Amethyst + COLLEEN jointly  
**Scope:** All 24 repos — governance headers, documentation quality, AGENT_MANIFEST updates, SWEEP_LOG entries, CO_ORCH_QUEUE resolution  
**Output:** Bulk push to all priority repos + master SWEEP_LOG entry  

---

## Commit Signature Standard

All co-orchestrated commits must use:

```
feat(sweep): <description> — Sweep ID: <ID>

Co-authored-by: Agent-Amethyst <amethyst@ndrorchestration>
Co-authored-by: COLLEEN <colleen@ndrorchestration>
```

Single-agent commits use the responsible agent's tag only.

---

## Documentation Quality Standards (Non-Negotiable)

Every file pushed by either agent must meet:

### For Markdown files
```markdown
> **Governed by:** [framework] · [license]  
> **Agent:** [Amethyst | COLLEEN | Both]  
> **Sweep ID:** [S-YYYY-MM-DD-TYPE]  
> **Last Updated:** [ISO 8601 timestamp]  
```

### For code files (Python, TypeScript, JavaScript)
```
# Governed by: DGAF-Framework
# Agent: [Amethyst | COLLEEN]
# Sweep ID: [S-YYYY-MM-DD-TYPE]
# Last Updated: [ISO 8601]
```

### For JSON/config files
```json
{
  "_governance": {
    "governed_by": "DGAF-Framework",
    "agent": "[Amethyst | COLLEEN]",
    "sweep_id": "[S-YYYY-MM-DD-TYPE]",
    "last_updated": "[ISO 8601]"
  }
}
```

---

## Audit Findings Table Format

All audit outputs must use this table:

| Repo | File/Area | Finding | Severity | Status | Action |
|---|---|---|---|---|---|
| `repo-name` | `path/file` | Description | HIGH/MED/LOW | ✅ PASS / ⚠️ WARN / ❌ FAIL | Applied / Pending |

---

## Escalation Path

```
Level 1: COLLEEN handles → operational/workflow issues
Level 2: Amethyst handles → governance/architecture issues  
Level 3: Joint session → systemic issues requiring both
Level 4: Ender override → any issue requiring human judgment
```

---

## Active Sweep Queue

See [CO_ORCH_QUEUE.md](./CO_ORCH_QUEUE.md) for current queue state.

---

*Protocol version: 1.0.0 · Established 2026-06-16 · Both agents co-signed*
