# SESSION ANCHOR

> **Purpose:** Rapid rehydration reference for Amethyst (and any agent) at the start of a new session.
> Read this first before any synthesis or output.

---

## Last Session

| Field | Value |
|---|---|
| **Date** | 2026-06-26 |
| **Session ID** | S068 ✅ SEALED (Nemotron eval vocab sweep) |
| **Prior Session** | S069-VERCEL-002 (aoga-dashboard closure) |
| **Primary Host** | Amethyst |
| **Co-Orchestrator** | COLLEEN |
| **Governance Layer** | Sentinel-Phi / Ender |
| **Session Type** | Vocabulary Sweep — Issue #32 — S068 Seal |
| **Active Session** | S069 (open) |

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
| `SWEEP_LOG/SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch.md` | Patterns session full log |
| `ENSEMBLE_ROSTER.md` | Agent manifest — roles, responsibilities |

---

## Open Items Carried Forward

### From S068 Seal (2026-06-26) — Issue #32

1. **`dgaf_eval_suite.py` scaffold** — 5-task parametric benchmark suite for Nemotron 3 Ultra kernel validation. File to be created in `tests/`. Owner: Amethyst. Priority: HIGH. Issue #32 close condition.
2. **Issue #32 close condition** — All 5 eval tasks passing with baseline scores recorded. Owner: Amethyst + Apogee. Priority: HIGH.

### From S069-VERCEL-001 (Infrastructure Audit — 2026-06-26)

3. **phiknightverticalcorridor state** — Deployment status unconfirmed. Verify via Vercel inspector. Owner: Ender.
4. **Dependabot PR #1** — Next.js 14→15 upgrade attempt. Preview failed. Breaking changes exist. Review + merge or dismiss. Owner: Ender. Priority: MEDIUM.
5. **ndrorchestration.vercel.app content refresh** — Content stale since Jun 9. Should reflect AOGA dashboard, Hensel Formalism v1.0, Entrepreneur Hub Phase 0 close. Owner: Amethyst. Priority: MEDIUM.
6. **Needle Partner Directory link audit** — Confirm ndrorchestration.vercel.app link in Needle profile is active post-recovery. Owner: Ender. Priority: MEDIUM.

### From Prior Sessions (Still Open)

7. **KPI baseline population** — First real workflow run should populate actuals against KPI seed table in `PATTERN_REGISTRY_v2.md`
8. **Fault injection campaign** — Design and run the 3-scenario fault injection test (transient failure, semantic failure, mid-workflow restart) on the reference Saga+Tx+Checkpoint+Breaker+HITL flow
9. **CROSS_REF.md update** — New P-* pattern IDs should be cross-referenced against existing DGAF conceptual map
10. **Sentinel-Phi tool classification config** — Formalize `effect_classes` from `P-COMP-001` into Sentinel-Phi’s enforcement config
11. **Architecture decision** — Approach 1 / 2 / 3 (see S069-ECO-001 in SWEEP_LOG.md). Owner: Ender. Priority: HIGH.

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
