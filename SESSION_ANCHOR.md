# SESSION ANCHOR

> **Purpose:** Rapid rehydration reference for Amethyst (and any agent) at the start of a new session.
> Read this first before any synthesis or output.

---

## Last Session

| Field | Value |
|---|---|
| **Date** | 2026-06-26 |
| **Session ID** | SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch |
| **Primary Host** | Amethyst |
| **Co-Orchestrator** | COLLEEN |
| **Governance Layer** | Sentinel-Phi / Ender |
| **Commit** | `434cc9a6` (patterns + registry + protocol push) |
| **Session Wrap Commit** | session-wrap push — CHANGELOG, SESSION_ANCHOR, CO_ORCH_QUEUE |

---

## Active Pattern Count

| Category | Count | Pattern IDs |
|---|---|---|
| Saga / Transaction | 3 | P-SAGA-001, P-TX-001, P-COMP-001 |
| Durability / Checkpointing | 1 | P-DURABLE-001 |
| Resilience / Governance | 1 | P-CB-001 |
| **Total Active** | **5** | — |

Full registry: [`registry/PATTERN_REGISTRY_v2.md`](registry/PATTERN_REGISTRY_v2.md)

---

## Key Files to Rehydrate

| File | Purpose |
|---|---|
| `CO_ORCH_PROTOCOL.md` | 7-step execution flow, agent triad roles |
| `registry/PATTERN_REGISTRY_v2.md` | Master pattern index + KPI seed table |
| `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` | Dyad contract, episode schema |
| `CO_ORCH_QUEUE.md` | Active work queue — what is pending next session |
| `SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md` | Last session full log |
| `ENSEMBLE_ROSTER.md` | Agent manifest — roles, responsibilities |

---

## Open Items Carried Forward

1. **KPI baseline population** — First real workflow run should populate actuals against KPI seed table in `PATTERN_REGISTRY_v2.md`
2. **Fault injection campaign** — Design and run the 3-scenario fault injection test (transient failure, semantic failure, mid-workflow restart) on the reference Saga+Tx+Checkpoint+Breaker+HITL flow
3. **CROSS_REF.md update** — New P-* pattern IDs should be cross-referenced against existing DGAF conceptual map
4. **Sentinel-Phi tool classification config** — Formalize `effect_classes` from `P-COMP-001` into Sentinel-Phi's enforcement config

---

## Governance Authority Order (Quick Reference)

1. User instruction
2. Space instruction (Amethyst as host)
3. Portfolio governance rules including Apogee Lens review
4. DGAF / PDMAL operating constraints
5. Default assistant behavior

---

## Non-Negotiables (Quick Reference)

- Refresh memory before synthesis
- Do not mark anything S-Tier or Gold Star until Apogee Lens approval
- All outputs auditable, source-grounded, explicitly bounded in uncertainty
- Multi-agent coordination routes through DGAF with clear role split
- Irreversible tool effects require either a HITL gate or be last in the Saga
