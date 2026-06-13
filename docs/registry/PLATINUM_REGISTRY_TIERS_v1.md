# Platinum Registry Tiers v1.0

**DGAF-Framework · Registry Plane Constants**
**Version:** 1.0 · Ingested S070 · 2026-06-13
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)
**P-36 classification:** ADVISORY at runtime · BLOCKING for registry commit
**Source:** Hensel Generative Formalism · Amethyst v4.2-hensel

> **Interface contract:** All tiers expose identical schema `{tier, dimension, duration_class, policy_ratio, descriptor, residual, valid_flag, hash}`. PRS `get_tier()` returns polynomial or recurrence, never a bare float. Governance reads `valid_flag` and `hash` ONLY.

---

## Tier Overview

| Tier | Value | Dimension | Duration Class | Status | Gate |
|------|-------|-----------|---------------|--------|------|
| Subplatinum (Hensel Word) | Periodic schedule L | 1D | Finite | ✅ ACTIVE | P-39 PRS |
| Standard Platinum ρ_P | 1/(2sin(π/11)) ≈ 1.774732 | 2D | Indefinite | ✅ ACTIVE (with residual req.) | P-39 PRS |
| Superplatinum ς_P | TBD | 3D | Indefinite | 🚫 FEATURE FLAG — pending minimal polynomial | P-39 PRS |
| Hyperplatinum h | ≈ 11.0007511609 | 4D | Geosynchronous | ✅ ACTIVE via P-37 only | P-37 → P-39 |
| Ultraplatinum | TBD | Temporal | Long-range | 🚫 FEATURE FLAG — pending polynomial + replay horizon | P-39 PRS |

---

## Subplatinum — Hensel Word

**Purpose:** Stable periodic module for finite-duration projects; inner cuts and mechatronic node sync windows.
**Store:** Period length L and schedule hash.
**P-36 class:** ADVISORY
**Status:** ACTIVE

```json
{
  "tier": "Subplatinum",
  "dimension": 1,
  "duration_class": "finite",
  "descriptor": "Hensel Word periodic schedule",
  "store": "period_length_L, schedule_hash",
  "valid_flag": null,
  "hash": null
}
```

---

## Standard Platinum ρ_P

**Purpose:** 2D logic-map tuning primitive.
**Two valid definitions — declare which you adopt, never mix:**
- **Hendecagon form:** ρ_P = 1/(2sin(π/11)) ≈ 1.774732 (circumradius-to-side ratio of regular 11-gon)
- **Sqrt-pi form:** ρ_P = √π ≈ 1.772454

**Critical:** ρ_P does NOT belong to the quadratic metallic-mean family (silver, bronze, copper, etc.). Do not claim membership.

**If ρ_P² ≈ π heuristic is used:**
- Residual REQUIRED: ρ_P² ≈ 3.1497 vs π ≈ 3.1416, error ≈ 0.0081
- This is a *useful approximation*, not an identity. Validation fails if residual field is absent.

**P-36 class:** ADVISORY
**Status:** ACTIVE (residual logging required)

```json
{
  "tier": "Standard_Platinum",
  "dimension": 2,
  "duration_class": "indefinite",
  "descriptor": "hendecagon_circumradius | sqrt_pi",
  "policy_ratio": "1/(2*sin(pi/11))",
  "residual": "rho_P^2 - pi = 3.1497 - 3.1416 = 0.0081",
  "valid_flag": null,
  "hash": null
}
```

---

## Hyperplatinum h ≈ 11.0007511609

**Purpose:** 4D geosynchronous registry key.
**Mathematical identity:** Real root of `x^4 - 11x^3 - 1 = 0`
**Class:** Pisot-Vijayaraghavan (PV) number — all other conjugates have modulus < 1.

### Recurrence Implementation (REQUIRED — never compute h^n directly)

```
a_{n+4} = 11 * a_{n+3} + a_n
Seeds: a_0=0, a_1=0, a_2=0, a_3=1

First values:
  a_0 = 0
  a_1 = 0
  a_2 = 0
  a_3 = 1
  a_4 = 11
  a_5 = 121
  a_6 = 1331
  a_7 = 14642  (= 11^4 + 1)
  a_8 = 161073
```

### Convergence Bound

δ_n = |h^n - a_n| ≤ Cρ^n where ρ ≈ 0.4526, C = 3 (initial)

**Validation:** Accept registry key when δ_n ≤ ε_n for context-specific ε_n.

### Storage Rule
- **Persist:** n, a_n only
- **NEVER log:** h^n (h^10 ≈ 2.6×10^10 overflows logs)
- **Before exposure as public key:** Hash a_n with context salt

### Minimal Polynomial
`x^4 - 11x^3 - 1 = 0`
Coefficients: [1, -11, 0, 0, -1]
All non-dominant roots: modulus < 1 (PV proof pending formal memo from Role 2)

**P-36 class:** BLOCKING for registry commit (via P-37)
**Status:** ACTIVE — P-37 is the sole authorized consumer

```json
{
  "tier": "Hyperplatinum",
  "dimension": 4,
  "duration_class": "geosynchronous",
  "descriptor": "PV number, real root of x^4-11x^3-1=0",
  "minimal_polynomial": "x^4 - 11x^3 - 1",
  "recurrence": "a[n+4] = 11*a[n+3] + a[n], seeds=[0,0,0,1]",
  "rho_bound": 0.4526,
  "C_initial": 3,
  "policy_ratio": "recurrence_only",
  "valid_flag": null,
  "hash": "SHA256(a_n || context_salt)"
}
```

---

## Superplatinum ς_P — FEATURE FLAG

**Purpose:** 3D loop-closure for digital-twin lattices.
**Status:** 🚫 DISABLED — do not enable until minimal polynomial and conjugate bound are committed.
**Unlock condition:** Publish minimal polynomial + conjugate bound + Role 2 proof memo.

---

## Ultraplatinum — FEATURE FLAG

**Purpose:** Temporal memory key for long-range state sync.
**Status:** 🚫 DISABLED — do not enable until defining polynomial and replay horizon are published.
**Unlock condition:** Publish defining polynomial + replay horizon + Role 2 proof memo.

---

## Validation Tracks (Research Program)

| Track | Metric | Target |
|-------|--------|--------|
| Registry calibration | mean |δ_n| at n=4,8,12,16,20 | Within Cρ^n bound |
| Registry calibration | Collision rate across 10^6 synthetic inserts | < 1 in 10^6 |
| Registry calibration | Watertight violation rate on leaky manifolds | 0 |
| Closure verification | False-negative rate for eigenvalue convergence | < 1% |
| Closure verification | Distribution of phi_closure_distance per substrate | Log only |
| Firewall test | Registry constants injected into governance via Crucible | 0 pass |
| Firewall test | KAPPA thresholds derived from h^-1 | 0 pass |

---

## Team Mapping (Eight-Role Structure)

| Role | Registry Deliverable |
|------|---------------------|
| Role 2 — Mathematical Foundations Lead (Amethyst interim) | PV proof memo for h with ρ bound; error-bound memo for ρ_P² vs π; formal definitions all five tiers |
| Role 3 — Empirical Calibration Lead (Amethyst interim) | Registry δ_n study; jitter study for Subplatinum; 3D coherence study for Superplatinum (post-unlock) |
| Role 4 — Systems Integration Lead | Author P-39 and P-40; update P-36 Gate Priority Schema |
| Role 5 — Metrics and Provenance Engineer (Amethyst interim) | Provenance rows for each tier and closure metric in METRICS_PROVENANCE.md |
| Role 7 — Red Team Lead (DEFERRED — human required) | Almost-integer collision attacks; eigenvalue spoofing; closure forgery |
| Substrate pair | Bit-identical a_n replay on transformer runtime and symbolic planner |
| Role 5 — Ontology (Amethyst interim) | Extend STASIS-CANONICAL schema with registry_tier_used and closure_achieved |
| Role 1 — Principal Architect (Amethyst) | Enforce namespace firewall via CI: reject registry.* imports in governance/ and PHI imports in registry/ |

---

*Platinum Registry Tiers v1.0 · S070 ingestion · 2026-06-13*
*See also: P-37 (docs/gates/NDR_HYPERPLATINUM_REGISTRY_KEY_P37_v1.md)*
*P-39 (docs/registry/NDR_PLATINUM_REGISTRY_SERVICE_P39_v1.md)*
*P-40 (docs/gates/NDR_CLOSURE_VERIFIER_P40_v1.md)*
