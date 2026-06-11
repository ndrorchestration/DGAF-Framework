#!/usr/bin/env python3
# scripts/quick_check.py
# 60-second local integration check (no network required).
# Run: python3 scripts/quick_check.py
from __future__ import annotations
import sys, math, time, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from resonant_decay import (
    StructuralContextPruningEngine, ContextToken, Tier
)
from resonant_decay.phi_gate import PhiClosureGate
from resonant_decay.math_core import PSI, PHI_STAR, psi_cubic_check
from resonant_decay.governance import lock_token, validate_token

ERRORS = []

def chk(name, cond, msg=""):
    icon = "✓" if cond else "✗"
    print(f"  {icon} {name}" + (f": {msg}" if msg else ""))
    if not cond: ERRORS.append(name)

print("[DGAF] Quick Check — resonant_decay package v1.7.0")
print("─" * 60)

# 1. PSI cubic
chk("PSI cubic invariant", psi_cubic_check(),
    f"PSI={PSI:.10f}")

# 2. PHI_STAR
chk("PHI_STAR value", abs(PHI_STAR - 0.6180339887) < 1e-8,
    f"phi_star={PHI_STAR:.10f}")

# 3. T0 axiom guard
eng = StructuralContextPruningEngine(threshold=0.99)
ax = ContextToken("ax0", "governance rule", Tier.AXIOM,
                  inserted_at=time.time() - 1000)
ex = ContextToken("ex0", "cot noise",       Tier.EXPLORATORY,
                  inserted_at=time.time() - 1000)
eng.ingest(ax); eng.ingest(ex)
s = eng.prune()
chk("T0 axiom guard",     s["axiom_count"]       == 1)
chk("T3 fully pruned",    s["exploratory_count"] == 0)
chk("compression <= 1",   s["compression_ratio"] <= 1.0)

# 4. Hash lock / validate
tok = ContextToken("t1", "locked content", Tier.STRUCTURAL)
tok = lock_token(tok)
chk("Hash lock valid",    validate_token(tok))
tok.content = "tampered"
chk("Hash tamper detect", not validate_token(tok))

# 5. Phi-Closure Gate — 13 clean turns → PASS
gate = PhiClosureGate(tolerance=0.05)
# 8 stable + 5 unstable -> R = 8/13 ≈ phi* at Fibonacci checkpoint T13
    _phi_stable = {1, 2, 3, 5, 6, 8, 10, 12}
    for i in range(1, 14):
            result = gate.record(stable=(i in _phi_stable))
chk("Phi gate T13 PASS",  result["checkpoint"] and result["decision"] == "PASS",
    f"R={result['R']:.4f} delta={result['delta']}")

# 6. Phi-Closure Gate — adversarial drift → REPROMPT
gate2 = PhiClosureGate(tolerance=0.05)
for i in range(1, 10):  gate2.record(stable=True)
for i in range(10, 14): gate2.record(stable=False)  # 4 DGAF kills
res2 = gate2.events[-1]
chk("Phi gate adversarial REPROMPT",
    res2.decision in ("REPROMPT", "KILL_RECOMMENDATION"),
    f"decision={res2.decision}")

# 7. Adapter imports
try:
    from resonant_decay.adapters.raw      import scpe_middleware
    from resonant_decay.adapters.langgraph import make_scpe_node
    from resonant_decay.adapters.crewai    import scpe_kickoff_wrapper
    chk("Adapter imports", True)
except ImportError as e:
    chk("Adapter imports", False, str(e))

# 8. 30-turn local simulation
from resonant_decay.simulations.drift_v17 import run as drift_run
results = drift_run(n_turns=30)
kills = [r for r in results if r["dgaf_decision"] == "KILL"]
chk("30-turn: 3 DGAF kills",        len(kills) == 3,     f"{len(kills)} kills")
chk("30-turn: T0 never drops",
    all(r["axiom_count"] == results[0]["axiom_count"] for r in results))
chk("30-turn: seal hashes present",
    all(len(r["seal_hash"]) == 16 for r in results))

print("─" * 60)
if ERRORS:
    print(f"  ✗ FAILED — {len(ERRORS)} check(s): {ERRORS}")
    sys.exit(1)
else:
    print("  ✓ ALL CHECKS PASSED — resonant_decay v1.7.0 is regression-clean.")
