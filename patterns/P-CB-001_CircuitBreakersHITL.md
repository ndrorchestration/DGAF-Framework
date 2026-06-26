# P-CB-001 — CircuitBreakersHITL

**Status:** Active  
**Version:** 1.0.0  
**Registered:** 2026-06-26  
**Registered by:** Amethyst (QA) + COLLEEN (Archive)  

---

## Intent

Prevent runaway loops, cost explosions, and catastrophic irreversible actions by opening circuit breakers on semantic failures (not just HTTP errors) and routing high-risk actions through a durable human-in-the-loop approval queue.

## Structure

```json
{
  "circuit_breakers": {
    "quality_breaker": {
      "schema_failures_threshold": 3,
      "loop_detection": {
        "max_similar_calls": 3,
        "max_similar_outputs": 3
      },
      "on_open": "switch_to_fallback_model_or_simplified_mode"
    },
    "budget_breaker": {
      "max_tokens_per_run": 200000,
      "max_steps_per_run": 50,
      "on_open": "abort_and_alert"
    }
  },
  "hitl": {
    "high_risk_tools": [
      "tool.send_email",
      "tool.execute_payment",
      "tool.delete_production_data",
      "tool.modify_infrastructure"
    ],
    "confidence_threshold": 0.7,
    "escalation_queue": "durable_queue",
    "on_escalate": "persist_state_and_pause",
    "on_decision": "resume_from_checkpoint",
    "sla_hours": 24,
    "on_sla_breach": "auto_cancel_saga_and_alert"
  }
}
```

## Participants

- **Amethyst** — configures breaker thresholds and HITL tool list per workflow; monitors live quality metrics
- **COLLEEN** — logs every breaker trip and HITL event with context; surfaces patterns of repeated breaker trips for root cause review
- **Sentinel-Phi** — enforces `high_risk_tools` classification; prevents unlisted tools from bypassing HITL gate

## Known Failures

- **Breaker blindness:** Only transport-level errors tracked; semantic loops undetected. Mitigation: quality metrics must include loop detection and schema validation rates.
- **HITL deadlock:** Approval queue receives event but workflow state not persisted → system blocks. Mitigation: persist state atomically before emitting HITL request.

## KPIs (COLLEEN tracks)

- `breaker_trip_rate_per_100_runs`
- `hitl_approval_latency_p95`
- `hitl_deadlock_incidents`
- `false_positive_breaker_trips`
