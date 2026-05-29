# NDR Pattern — PDMAL Convergence Monitor v1.0

**Status:** Production  
**Version:** 1.0  
**Date:** 2026-05-29  
**Owner:** ndrorchestration / Andrew (Ender) Hensel  
**Governed by:** Agent Amethyst · DGAF-Framework  

---

## Summary

Structural health monitor for the PDMAL trust graph. Tracks the Frobenius norm of
edge-weight changes turn-over-turn (`‖ΔW‖_F`). Catches systemic graph drift — coordinated
weight shifts across multiple edges — that single-edge monitoring would miss. Operates
independently of semantic gating (DemiJoule) and temporal gating (Phi-Closure), providing
a third orthogonal safety axis.

---

## Specification

### Metric

```
‖ΔW‖_F = sqrt( Σ (w_t(i,j) − w_{t-1}(i,j))² )  over all edges (i,j)
```

### Alert Ladder

| Consecutive Turns > Alert Thresh | Status | Severity | Routing |
|----------------------------------|--------|----------|---------|
| 0 | STABLE | 0 | log |
| 1 | WATCH | 1 | log |
| 2 | WARN | 2 | log |
| 3+ | ALERT | 3 | `amethyst_alert` |

### Convergence Confirmation

`‖ΔW‖_F < CONV_THRESH (0.02)` for `N_CONSEC (3)` consecutive turns → `CONVERGED`

### Thresholds

| Parameter | Value | Rationale |
|-----------|-------|---------- |
| `ALERT_THRESH` | 0.08 | Catches rebalancing events; tuned to schema-drift pattern |
| `CONV_THRESH` | 0.02 | Symmetric with alert trigger |
| `N_CONSEC` | 3 | 3-turn window — matches Phi-closure alert window |

---

## Joint Escalation Rule

**PDMAL ALERT (severity ≥ 3) + Phi-Closure ESCALATE (severity ≥ 3)**  
→ Triggers DemiJoule deep re-scan with `tool_call=True`  
→ If deep scan returns `kill`, session is terminated before HPG

This catches coordinated attacks that manipulate both the trust graph structure
and the semantic content simultaneously.

---

## Placement

```
Step 2.5 in orchestrate_turn:
  [Post-PDMALGraph.reweight()] → PDMALConvergenceMonitor.check() → [Pre-DemiJoule]
```

---

## 60-Turn Simulation Results

- WATCH fired at T31, T40, T46 (schema-drift state caused single-turn edge rebalancing)
- 0 full ALERTs (3-consecutive requirement not met with this drift pattern)
- All WATCH events auto-resolved within 1 turn
- `‖ΔW‖_F` range during watches: 0.108 – 0.117

---

## Audit Output

Every check emits a `DivergenceEvent` with:
- `graph_norm_delta` — `‖ΔW‖_F`
- `max_edge` — (src, dst) pair with largest individual delta
- `convergence_snapshot` — full weight matrix at time of check
- `routing_action` — `log` or `amethyst_alert`

---

## Quick Check

```python
g   = AgentAmethyst._build_default_pdmal()
mon = PDMALConvergenceMonitor(g)
for i in range(5):
    ev = mon.check(f"T{i}")
assert mon.status in (ConvergenceStatus.STABLE, ConvergenceStatus.CONVERGED)
print(f"PDMAL stable: {mon.status.code}")
```

---

*Amethyst-governed · COLLEEN-archived · DemiJoule-safety-checked*
