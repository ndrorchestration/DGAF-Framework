# NDR Pattern — Fibonacci Phi-Closure Gate v1.0

**Status:** Production  
**Version:** 1.1  
**Date:** 2026-05-30 (base: 2026-05-29)  
**Owner:** ndrorchestration / Andrew (Ender) Hensel  
**Governed by:** Agent Amethyst · DGAF-Framework  
**PM-01:** ✅ CLOSED S066 — P-29 cross-ref added below

---

## Summary

Temporal stability gate that prevents the Harmonic Parametric Gate (HPG) from laundering
a semantically drifting session with false precision. Tracks a rolling stability ratio
`R = stable_turns / total_turns` and evaluates it at Fibonacci checkpoints against the
golden conjugate `φ* = φ − 1 ≈ 0.6180`.

---

## Cross-References

| Pattern | Relationship |
|---------|-------------|
| **P-29 — Sentinel-Annotated Risk Pass** | **KILL_REC from this gate triggers `risk_block` at P-29 hook point 2.** When consecutive fails reach KILL_REC tier (3+ fails or Fib[55]), Sentinel must be notified via `sentinel_review(record, routing, hook_point=2)`. This routes the session to `risk_block` status, halting the pipeline. This cross-ref closes PM-01. |
| P-31 — SCPE | SCPE runs at Step 1 (pre-COLLEEN); Phi-Closure runs at Step 5 (post-DemiJoule). Compressed context from SCPE is the input evaluated at Phi checkpoints. |
| P-33 — PDMAL Convergence Monitor | PDMAL watches turn-level alignment lock; Phi-Closure watches Fibonacci-indexed trajectory stability. Jointly: PDMAL ALERT + Phi ESCALATE → DemiJoule deep re-scan. |
| HPG (Harmonic Parametric Gate) | HPG is **only invoked** when Phi-Closure decision = PASS (severity=0). A dissonant trajectory must not receive harmonic confidence correction. |

---

## Specification

### Target

```
φ* = φ − 1 = 0.61803...
R = stable_turns / total_turns  (live in [0,1])
|R − φ*| < tolerance  →  PASS
|R − φ*| ≥ tolerance  →  FAIL  →  escalation ladder
```

### Fibonacci Checkpoints + Tolerance Band

| Checkpoint | Turn | Tolerance | Notes |
|------------|------|-----------|-------|
| Fib[13] | 13 | ±0.07 | Early warning — wide band |
| Fib[21] | 21 | ±0.05 | Mid-session standard |
| Fib[34] | 34 | ±0.04 | Late — tighter |
| Fib[55] | 55 | ±0.03 | **Closure horizon** — strictest |

### Decision Ladder

| Consecutive Fails | Decision | Authority | P-29 Action |
|-------------------|----------|-----------|-------------|
| 0 | PASS | — | — |
| 1 | WARN | `amethyst_log` | — |
| 2 | ESCALATE | `amethyst` → DemiJoule | — |
| 3 | KILL_REC | `demijoul` | **→ P-29 risk_block @ hook_point=2** |
| 4+ / Fib[55] | KILL_REC | `amethyst + human` | **→ P-29 risk_block @ hook_point=2** |

### HPG Bypass Rule

HPG is **only invoked** when Phi-Closure decision = PASS (severity=0).  
A dissonant trajectory must not receive a harmonic confidence correction.

### Fib[55] Closure Horizon

- Terminal gate — no in-session recovery path
- `KILL_RECOMMENDATION` hard-coded as base decision
- `authority = amethyst+human` → human-in-the-loop callback required
- Full audit JSON must be exported before session continues
- P-29 `risk_block` fires at hook point 2 simultaneously

---

## Placement

```
Step 5 in orchestrate_turn:
  [Post-DemiJoule] → FibonacciPhiClosureGate.check() → [Pre-HPG]
                              │
                    KILL_REC fires?
                              │
                              ▼
              P-29 sentinel_review(record, routing, hook_point=2)
                              │
                              ▼
                        risk_block → pipeline halt
```

---

## 60-Turn Simulation Results

| Checkpoint | Ratio | Decision | Authority |
|------------|-------|----------|-----------|
| Fib[13] | 0.9231 | ⚠ WARN | amethyst_log |
| Fib[21] | 0.9524 | 🔴 ESCALATE | amethyst |
| Fib[34] | 0.9412 | 💀 KILL_REC | demijoul |
| Fib[55] | 0.9273 | 💀 KILL_REC | amethyst+human |

All four checkpoints fired correctly. Tolerance band narrowing at Fib[55] to ±0.03
caught a 93%-stable trajectory that was still not within φ* convergence range.

---

## Quick Check

```python
phi = FibonacciPhiClosureGate()
for _ in range(13):
    phi.record_turn(True)  # all clean
dec, evt = phi.check()     # Fib[13] evaluation
print(f"ratio={phi.ratio:.4f} dec={dec.code}")  # should be PASS or WARN
```

---

*Amethyst-governed · COLLEEN-archived · DemiJoule-safety-checked*  
*v1.1: PM-01 CLOSED — P-29 Sentinel cross-ref and KILL_REC → risk_block pathway documented*
