# P-TX-001 — TransactionalToolBoundaryAtomix

**Status:** Active  
**Version:** 1.0.0  
**Registered:** 2026-06-26  
**Registered by:** Amethyst (QA) + COLLEEN (Archive)  
**Apogee Lens:** Pending first run review  

---

## Intent

Insert a transactional shim at the stochastic–deterministic boundary. The LLM proposes tool calls; the deterministic layer groups them into effect sets, logs receipts, retries transient failures, and applies Saga-style compensation if a later step fails.

## Context

Applies wherever LLM-generated tool calls touch external systems. Prevents leaked side effects during speculative LLM branches, duplicate actions on retries, and untracked mutations.

## Structure

```json
{
  "tool_boundary": {
    "transactional": true,
    "log_effects": true,
    "idempotency_keys": true,
    "settlement": {
      "mode": "delayed_commit",
      "predicate": "all_prior_steps_pass_verifier"
    },
    "effect_receipt": {
      "fields": ["effect_id", "resource", "parameters", "effect_class", "reversible", "compensator_handle", "timestamp"]
    }
  }
}
```

## Participants

- **Amethyst** — configures settlement predicate and effect class mapping per workflow
- **COLLEEN** — archives effect receipts and retains them for replay-or-fork decisions on checkpoint restore
- **Sentinel-Phi** — classifies tool effect classes; gates irreversible tools behind HITL or frontier checks

## Consequences

- **Benefit:** No duplicate side effects on retry; speculative branches don't leak; full audit trail
- **Cost:** Adapter overhead per tool; delayed commit adds latency for irreversible actions

## Known Failures

- **Semantic rollback attack:** Checkpoint restore replays tool calls without checking effect log → double effects. Mitigation: P-DURABLE-001 ACRFence replay-or-fork.
- **Settlement predicate mismatch:** Predicate passes but downstream validator fails post-commit. Mitigation: make predicate include verifier sign-off.

## KPIs (COLLEEN tracks)

- `duplicate_effect_rate` — duplicate tool executions per 1000 calls
- `settlement_latency_p95` — time from last step pass to commit
- `effect_log_coverage` — % of tool calls with receipts
