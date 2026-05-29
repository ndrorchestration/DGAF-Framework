# resonant_decay/math_core.py
# Supergolden / tribonacci constant and resonant decay curve.
import math

# Tribonacci constant — real root of x^3 = x^2 + x + 1
# ψ ≈ 1.8392867552141612  (tribonacci)
# For decay purposes we use the supergolden root of x^3 = x^2 + 1
PSI: float = 1.4655712318767682   # supergolden ratio
PHI: float = (1 + math.sqrt(5)) / 2
PHI_STAR: float = PHI - 1          # = 0.6180339887…  conjugate in [0,1]

# Fibonacci sequence up to index 55
FIBONACCI = [0, 1]
while FIBONACCI[-1] < 1_000_000:
    FIBONACCI.append(FIBONACCI[-1] + FIBONACCI[-2])
FIB_CHECKPOINTS = [13, 21, 34, 55]


def resonant_decay(delta_t: float, psi: float = PSI) -> float:
    """R(t) = ψ^(−Δt)  — resonant exponential decay."""
    if delta_t <= 0:
        return 1.0
    return psi ** (-delta_t)


def tier_base_weight(tier: "Tier") -> float:  # type: ignore[name-defined]
    return {0: float("inf"), 1: 5.0, 2: 3.0, 3: 1.0}.get(tier.value, 1.0)


def tif_multiplier(has_trust_edge: bool) -> float:
    """Topological Invariant Factor boost from PDMAL trust edge."""
    return 2.0 if has_trust_edge else 1.0


def psi_cubic_check(psi: float = PSI, tol: float = 1e-10) -> bool:
    """Assert PSI satisfies x^3 = x^2 + 1."""
    return abs(psi**3 - (psi**2 + 1)) < tol
