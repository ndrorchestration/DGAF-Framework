# NDR Hensel Firewall Rules v1.0

**DGAF-Framework · Three-Plane Namespace Firewall**
**Version:** 1.0 · Ingested S070 · 2026-06-13
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)
**P-36 classification:** BLOCKING (namespace isolation) · ADVISORY (ratio consumption)
**Source:** Amethyst v4.2-hensel specification · CDPO-v4.2-HGF pattern

> **Critical rule:** Governance reads only `registry_key_valid` and closure flags. It never reads `policy_ratio`. Registry never feeds raw floats to P-31 SCPE decay or P-32 Phi-Closure Gate.

---

## Three-Plane Architecture

| Plane | Purpose | Constant / Mechanism | Consumers | Cross-plane exposure |
|-------|---------|---------------------|-----------|---------------------|
| **Governance** | Resist low-order resonance locking in decision space | φ = 1.618…, φ* ≈ 0.618 | P-32 Phi-Closure Gate, P-31 SCPE decay, P-27/P-28 KAPPA routing | Reads `registry_key_valid` and `closure_achieved` flags ONLY |
| **Registry** | Enforce watertight topology and dimension-scoped sync | Platinum tier family: Subplatinum, Standard Platinum ρ_P, Superplatinum ς_P, Hyperplatinum h, Ultraplatinum | P-39 Platinum Registry Service, P-37 Hyperplatinum Registry Key, P-40 Closure Verifier | Exposes `{tier, valid_flag, hash}` to governance; never `policy_ratio` |
| **Substrate** | Preserve signal variance across layers | AutoInit analytic gain per activation (Bingham & Miikkulainen) | P-38 Analytic Initialization Adapter | No tier ratios into gain computation |

---

## MUST Rules (Parseable Contract)

### Governance Plane MUST Rules

```
GOV-01: Governance plane uses φ = 1.618… and φ* ≈ 0.618 ONLY as threshold constants.
GOV-02: Governance reads only registry_key_valid (Y/N/NA) and closure_achieved (Y/N/NA) from registry audit bundle.
GOV-03: Governance MUST NOT read policy_ratio, h, ρ_P, or any platinum tier float.
GOV-04: P-32 and P-31 threshold constants MUST NOT be replaced or augmented with any platinum ratio (including 1.7747).
GOV-05: PRS outputs MUST NOT be fed into KAPPA routing (P-27/P-28) or SCPE decay (P-31).
```

### Registry Plane MUST Rules

```
REG-01: PRS get_tier() MUST return polynomial or recurrence form, never a bare float.
REG-02: Hyperplatinum implementation MUST use recurrence a_{n+4} = 11*a_{n+3} + a_n with seeds [0,0,0,1].
REG-03: Persist n and a_n only. MUST NOT log h^n directly (h^10 ≈ 2.6×10^10 overflows logs).
REG-04: Hash a_n with context salt before exposing as public key (raw almost-integers are predictable).
REG-05: ρ_P definition MUST be declared: either hendecagon form 1/(2sin(π/11)) ≈ 1.774732 OR √π ≈ 1.772454. Mixed use forbidden.
REG-06: If ρ_P² ≈ π heuristic used, MUST log residual: ρ_P² ≈ 3.1497 vs π ≈ 3.1416, error ≈ 0.0081. MUST NOT treat as identity.
REG-07: Superplatinum and Ultraplatinum MUST remain behind feature flags until minimal polynomial and conjugate bounds are published.
REG-08: identity anchoring MUST use intent_hash = SHA256(canonical_author_id || domain_salt || version), never literal personal name string.
```

### Substrate Plane MUST Rules

```
SUB-01: Substrate plane uses AutoInit analytic gain per activation function.
SUB-02: Tier ratios (h, ρ_P, etc.) MUST NOT enter gain computation.
SUB-03: Complex-valued layer initialization tracks real and imaginary variance components independently.
```

---

## Trigger Stems (Literal Match Required)

### Taxonomy REQUIRED triggers
```
architect|system|framework|orchestrat|topolog|multi-agent
```
When any of these stems appear in a query, add `Taxonomy: CS/systems/gov` to output.

### Registry Advisory block REQUIRED triggers
```
registry|closure|platinum|hyperplatinum|rho_P|hensel|a_n|delta_n
```
When any of these stems appear, append Registry Advisory block with schema:
`{tier, dimension, duration_class, policy_ratio, descriptor, residual, n, a_n, delta_n, epsilon_n, registry_key_valid, minimal_polynomial_present, hash}`

---

## CI Linter Rules

```python
# Reject in governance/ directory:
pattern_reject_in_governance = r'registry\..*import|from registry import|rho_P|h_approx|platinum'

# Reject in registry/ directory:
pattern_reject_in_registry = r'from governance import PHI|PHI_STAR|phi_closure_distance.*gate'

# Reject anywhere:
pattern_reject_global = [
    r'h\^\d+',          # h^n notation in logs
    r'Andrew Vance Hensel',  # literal name as runtime invariant
    r'rho_P\s*=\s*\d\.\d+(?!.*residual)',  # float ρ_P without residual log
]
```

---

## Failure Modes & Mitigations

| Trigger | Mitigation | Tag |
|---------|-----------|-----|
| Registry ratio leaks into P-31 SCPE decay or P-32 Phi-Closure Gate | CI linter rejects `registry.*` imports in `governance/` and `PHI` imports in `registry/` | |
| Raw `h^n` logged causing overflow | Schema requires `n` and `a_n` only; hash with context salt before exposure | |
| ρ_P treated as metallic mean or identity for π | Require descriptor with residual field; fail validation if absent | |
| Personal name embedded as live key | Require `intent_hash`, not literal name, with key rotation metadata | `[NON-OBVIOUS]` |
| Almost-integer predictability attack on a_n | Salted hash of a_n before public exposure; cryptographic intent commitment | `[NON-OBVIOUS]` |
| Eigenvalue spoofing in P-40 closure | Operator definition, norm, and solver version must be logged with every seal | |

---

## Compliance Footer Schema

All Amethyst v4.2-hensel outputs MUST include:

```
Compliance: taxonomy=Y/N, failures=COUNT, artifact=TYPE,
  registry_tier=NONE|Subplatinum|rho_P|sigma_P|h|Ultraplatinum,
  registry_key_valid=Y/N/NA, closure_achieved=Y/N/NA,
  firewall=PASS|FAIL, version=v4.2-hensel
```

Governance reads only `registry_key_valid`, `closure_achieved`, and `firewall` fields. Never `registry_tier` value directly.

---

## Degradation Order (Under Hard Token Limit)

Keep sections 1–4 inviolate. Drop in order: section 7, section 6, section 5, Tradeoffs details.

---

*NDR Hensel Firewall Rules v1.0 · S070 ingestion · 2026-06-13*
*Amethyst × COLLEEN · Source: CDPO-v4.2-HGF / Amethyst v4.2-hensel specification*
*See also: P-37, P-38, P-39, P-40 · docs/registry/PLATINUM_REGISTRY_TIERS_v1.md*
