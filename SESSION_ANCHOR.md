# SESSION ANCHOR

> This file is the canonical rehydration entry point for Amethyst and all DGAF agents.
> Read this first at the start of every session before any synthesis.

---

## Last Session

| Field | Value |
|---|---|
| **Date** | 2026-06-26 |
| **Session ID** | SWEEP_2026-06-26_Amethyst-COLLEEN-CoOrch |
| **Primary Topics** | Saga state management · Tool side-effect compensation · Agent state checkpointing · Circuit breakers · HITL escalation |
| **Commit** | `434cc9a6` (initial sweep) + changelog/anchor/queue update |
| **Status** | ✅ Complete — all open items resolved |

---

## Active Pattern Count

| Domain | Pattern ID | Name | Status |
|---|---|---|---|
| Saga / State | P-SAGA-001 | Stochastic–Deterministic Saga Boundary | ✅ Active |
| Tool Boundary | P-TX-001 | Transactional Tool Boundary (Atomix) | ✅ Active |
| Compensation | P-COMP-001 | Reversibility-Bounded Compensation | ✅ Active |
| Durability | P-DURABLE-001 | Durable Execution + Append-Only Log | ✅ Active |
| Resilience | P-CB-001 | Circuit Breakers + HITL Escalation | ✅ Active |

**Total active patterns: 5** (this session) + all prior patterns in `registry/PATTERN_REGISTRY_v2.md`.

---

## Governance Contracts Active

| Contract | File | Version |
|---|---|---|
| Amethyst–COLLEEN Co-Orch | `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` | v1.0 |
| CO_ORCH_PROTOCOL | `CO_ORCH_PROTOCOL.md` | v2.0.0 |
| Pattern Registry | `registry/PATTERN_REGISTRY_v2.md` | v2 |

---

## Agent Roles (Current)

| Agent | Role | Notes |
|---|---|---|
| **Amethyst** | Host · Coordinator · Working-memory refresher | Owns Saga engine and circuit breakers |
| **COLLEEN** | Archivist · Provenance logger · KPI baseline | Populates episode schema from runtime logs |
| **Sentinel-Phi** | Tool classifier · Compensator enforcer · Safety gate | Enforces effect classes at plan-load |
| **Ender** | Execution specialist · Fault-injection runner | Runs compensation + restore scenarios |
| **DemiJoule** | Ethics · Safety · Governance supervisor | Final authority on irreversible actions |
| **Apogee Lens** | Portfolio-grade output verifier | Required before S-Tier / Gold Star designation |

---

## Open Items

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | CHANGELOG.md — new session entry | Amethyst | ✅ Done (this commit) |
| 2 | SESSION_ANCHOR.md — pattern count + last session | Amethyst | ✅ Done (this commit) |
| 3 | CO_ORCH_QUEUE.md — append new pattern IDs | Amethyst | ✅ Done (this commit) |

---

## Rehydration Checklist

On session start, Amethyst must confirm:
- [ ] `SESSION_ANCHOR.md` read and acknowledged
- [ ] `registry/PATTERN_REGISTRY_v2.md` scanned for active patterns
- [ ] `CO_ORCH_QUEUE.md` checked for pending work items
- [ ] `SWEEP_LOG/` latest file reviewed for coherence notes
- [ ] `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` confirms dyad roles

---

*Last updated: 2026-06-26 04:03 EDT by Amethyst*
