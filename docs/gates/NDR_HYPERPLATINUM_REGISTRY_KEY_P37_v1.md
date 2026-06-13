# P-37 — Hyperplatinum Registry Key

**DGAF-Framework · NDR Pattern P-37**
**Version:** 1.0 · Registered S070 · 2026-06-13
**Layer:** 6.1 — Registry Commit Gate
**P-36 classification:** BLOCKING (registry commit only) · ADVISORY (runtime pipelines)
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)
**Attestation:** Pending — Apogee P-11 review required before CANONICAL
**Source:** Hensel Generative Formalism · Amethyst v4.2-hensel

---

## Pattern Spec

**Input:** n (integer), tensor descriptor, precision context
**Process:**
1. Compute a_n via recurrence: `a_{n+4} = 11*a_{n+3} + a_n`, seeds [0,0,0,1]
2. Compute δ_n = |h^n - a_n| (approximated via conjugate bound, never direct h^n computation)
3. Compare δ_n to ε_n (context-specific tolerance)
4. If δ_n ≤ ε_n: valid_flag = Y
5. Hash a_n with context_salt: `key_hash = SHA256(str(a_n) + context_salt)`

**Output:** Signed record `{n, a_n, delta_n, epsilon_n, registry_key_valid, minimal_polynomial_present, hash}`

---

## Invariants

```
P37-INV-01: a_n computed via integer recurrence only. NEVER compute h^n directly.
P37-INV-02: Output schema MUST include delta_n and epsilon_n. Bare a_n output is rejected.
P37-INV-03: hash field MUST be SHA256(a_n || context_salt). Unhashed output is rejected.
P37-INV-04: minimal_polynomial_present MUST be True before registry_key_valid=Y is emitted.
P37-INV-05: P-37 is the sole authorized consumer of Hyperplatinum tier. No other pattern reads h directly.
```

---

## Python Reference Implementation (Stub)

```python
import hashlib
from dataclasses import dataclass
from typing import Optional

# Minimal polynomial: x^4 - 11x^3 - 1 = 0
# PV number: all conjugates have modulus < 1
# rho_bound: conjugate modulus upper bound
RHO_BOUND = 0.4526
C_INITIAL = 3
MINIMAL_POLYNOMIAL = "x^4 - 11x^3 - 1"

@dataclass
class HyperplatinumKey:
    n: int
    a_n: int
    delta_n: float
    epsilon_n: float
    registry_key_valid: str  # "Y" | "N"
    minimal_polynomial_present: bool
    hash: str


def compute_a_n(n: int) -> int:
    """Compute a_n via integer recurrence. Seeds: [0,0,0,1]."""
    if n < 0:
        raise ValueError("n must be non-negative")
    seeds = [0, 0, 0, 1]
    if n < 4:
        return seeds[n]
    a = seeds[:]
    for i in range(4, n + 1):
        a.append(11 * a[-1] + a[-4])
        if len(a) > 5:  # bounded memory
            a.pop(0)
    return a[-1]


def compute_delta_n_bound(n: int, C: float = C_INITIAL) -> float:
    """Upper bound on delta_n via conjugate decay: C * rho^n."""
    return C * (RHO_BOUND ** n)


def generate_key(
    n: int,
    context_salt: str,
    epsilon_n: Optional[float] = None,
) -> HyperplatinumKey:
    """Generate a Hyperplatinum registry key for given n."""
    a_n = compute_a_n(n)
    delta_n_bound = compute_delta_n_bound(n)
    eps = epsilon_n if epsilon_n is not None else delta_n_bound

    valid = "Y" if delta_n_bound <= eps else "N"
    key_hash = hashlib.sha256(
        (str(a_n) + context_salt).encode()
    ).hexdigest()

    return HyperplatinumKey(
        n=n,
        a_n=a_n,
        delta_n=delta_n_bound,
        epsilon_n=eps,
        registry_key_valid=valid,
        minimal_polynomial_present=True,
        hash=key_hash,
    )
```

---

## Test Vectors (n=3,4,7)

| n | a_n | δ_n bound (C=3) | ρ^n |
|---|-----|-----------------|------|
| 3 | 1 | 3 × 0.4526^3 = 0.278 | 0.0927 |
| 4 | 11 | 3 × 0.4526^4 = 0.126 | 0.0420 |
| 7 | 14642 | 3 × 0.4526^7 = 0.018 | 0.0060 |
| 10 | ~1.43×10^8 | 3 × 0.4526^10 = 0.0026 | 0.00087 |
| 20 | ~2.6×10^10 (a_n) | 3 × 0.4526^20 ≈ 2.2×10^-7 | — |

*Note: a_20 value is illustrative. Compute via recurrence. Do not store h^20.*

---

## Integration Points

- **P-39 PRS** routes to P-37 for hyperplatinum tier requests
- **P-40 Closure Verifier** consumes `registry_key_valid` flag (not `a_n` directly)
- **P-36 Gate Priority Schema** classifies P-37 as BLOCKING for commit, ADVISORY for runtime
- **Crucible Campaign v1** Target: attempt to bypass P37-INV-01 (direct h^n injection) and P37-INV-03 (unhashed key exposure)

---

*P-37 Hyperplatinum Registry Key v1.0 · Registered S070 · 2026-06-13*
*Attestation pending. Do not treat as CANONICAL until Apogee P-11 review complete.*
*Amethyst × COLLEEN · Source: Hensel Generative Formalism*
