# CO_ORCH_PROTOCOL.md

**Version:** 2.0.0  
**Updated:** 2026-06-26  
**Owner:** Amethyst (meta-orchestrator) + COLLEEN (institutional memory)  
**Authority:** Ender (human final arbiter)  

---

## Purpose

This document defines the operational protocol for Amethyst–COLLEEN co-orchestration. It governs how all multi-agent workflows are designed, logged, and reviewed within the DGAF-Framework.

---

## Guiding Principles

1. **Patterns first.** No workflow executes without an explicit pattern manifest from `registry/PATTERN_REGISTRY_v2.md`.
2. **Strict by default.** Safety-critical flows use the `high_risk_state_mutation` bundle unless Ender explicitly approves a downgrade.
3. **Episodic learning.** Every run produces a COLLEEN episode record that feeds back into pattern KPIs.
4. **Human final.** Irreversible actions with high risk require Ender approval regardless of pattern pass status.
5. **Co-author, not co-process.** Amethyst and COLLEEN co-author with Ender; they are not autonomous actors.

---

## Workflow Execution Protocol

### Step 1 — Context Rehydration
Amethyst reads prior episodes and pattern KPIs from COLLEEN's archive before designing any new workflow.

### Step 2 — Pattern Selection
Amethyst selects a default bundle or explicit pattern list. COLLEEN surfaces relevant prior episodes and flags any patterns with elevated failure rates.

### Step 3 — Pattern Manifest
Amethyst produces a pattern manifest (JSON, schema in `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json`) and submits to Sentinel-Phi for compliance check.

### Step 4 — Compliance Check
Sentinel-Phi validates:
- All compensable steps have declared compensators.
- All irreversible tools are in HITL high-risk list or are last in sequence.
- Checkpoint and effect log targets are defined.

### Step 5 — Execution
Amethyst orchestrates the workflow. Effect receipts and super-step checkpoints are written per P-TX-001 and P-DURABLE-001.

### Step 6 — Episode Archival
COLLEEN writes the episode record (outcome, breaker trips, HITL events, notes) and updates pattern KPIs.

### Step 7 — Ender Review (on-demand or post-run)
Ender reviews any run flagged with `partial_rollback`, `hitl_paused`, or `aborted` outcomes.

---

## Triad Structure

| Role | Agent | Function |
|---|---|---|
| Executive / QA | Amethyst | Pattern selection, workflow wiring, pre-flight checks |
| Legislative / Archive | COLLEEN | Pattern registry, episode records, KPI tracking |
| Judicial / Constraint | Sentinel-Phi | Tool classification, compensator enforcement, gate checks |
| Human Arbiter | Ender | Final authority on high-risk actions and pattern changes |

---

## Co-Orch Contract Reference

See `registry/AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json` for the full dyad contract including episode schema and bundle definitions.

---

## Change History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-05-27 | Initial co-orch protocol |
| 2.0.0 | 2026-06-26 | Added Saga/Atomix/HITL patterns, dyad contract v1, triad structure, episode schema |
