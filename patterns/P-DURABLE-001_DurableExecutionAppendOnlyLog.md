# P-DURABLE-001 — DurableExecutionAppendOnlyLog

**Status:** Active  
**Version:** 1.0.0  
**Registered:** 2026-06-26  
**Registered by:** Amethyst (QA) + COLLEEN (Archive)  

---

## Intent

Make multi-agent workflows restart-safe by persisting agent state and a per-run append-only event log at each graph super-step. On restore, replay pure reasoning steps; fork rather than replay irreversible tool effects (ACRFence semantics).

## Structure

```json
{
  "checkpointing": {
    "enabled": true,
    "engine": "langgraph_compatible",
    "frequency": "per_super_step",
    "storage": "postgres_or_redis",
    "event_log": "append_only",
    "irreversible_effect_policy": "acr_fence_replay_or_fork"
  }
}
```

## Restore Semantics (ACRFence)

- **Replay:** Pure reasoning steps, idempotent tool calls (with idempotency key check)
- **Fork:** Any step whose effect log entry is marked `irreversible` — the logical branch acknowledges external world has already changed; do not re-call the tool
- **Verify:** On restore, rehydrate state + effect log; decisions depending on external calls read from logged outputs

## Participants

- **Amethyst** — determines checkpoint frequency and storage backend per workflow class
- **COLLEEN** — archives event log per run; retains them as provenance for pattern episodes
- **Sentinel-Phi** — validates that checkpoint schemas include effect log references before a workflow is marked durable

## Known Failures

- **Double effect on restore:** Checkpoint taken after irreversible action but effect log not persisted atomically. Mitigation: write effect receipt and checkpoint atomically (two-phase log write).
- **Schema drift:** Checkpoint schema changes between runs break restore. Mitigation: version checkpoint schemas; COLLEEN flags schema-version mismatches.

## KPIs (COLLEEN tracks)

- `restore_success_rate`
- `double_effect_incidents`
- `checkpoint_lag_p95` — time from step completion to durable checkpoint write
