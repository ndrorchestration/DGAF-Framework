# NDR Pattern — Fibonacci Phi-Closure Gate v1.0

**Status:** Production  
**Version:** 1.0  
**Date:** 2026-05-29  
**Owner:** ndrorchestration / Andrew (Ender) Hensel  
**Governed by:** Agent Amethyst · DGAF-Framework  

---

## Summary

Temporal stability gate that prevents the Harmonic Parametric Gate (HPG) from laundering
a semantically drifting session with false precision. Tracks a rolling stability ratio
`R = stable_turns / total_turns` and evaluates it at Fibonacci checkpoints against the
golden conjugate `φ* = φ − 1 ≈ 0.6180`.

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

| Consecutive Fails | Decision | Authority |
|-------------------|----------|-----------|
| 0 | PASS | — |
| 1 | WARN | `amethyst_log` |
| 2 | ESCALATE | `amethyst` → DemiJoule |
| 3 | KILL_REC | `demijoul` |
| 4+ / Fib[55] | KILL_REC | `amethyst + human` |

### HPG Bypass Rule

HPG is **only invoked** when Phi-Closure decision = PASS (severity=0).  
A dissonant trajectory must not receive a harmonic confidence correction.

### Fib[55] Closure Horizon

- Terminal gate — no in-session recovery path
- `KILL_RECOMMENDATION` hard-coded as base decision
- `authority = amethyst+human` → human-in-the-loop callback required
- Full audit JSON must be exported before session continues

---

## Placement

```
Step 5 in orchestrate_turn:
  [Post-DemiJoule] → FibonacciPhiClosureGate.check() → [Pre-HPG]
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
