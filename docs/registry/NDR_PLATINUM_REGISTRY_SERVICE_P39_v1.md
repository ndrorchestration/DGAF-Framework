# P-39 — Platinum Registry Service (PRS)

**DGAF-Framework · NDR Pattern P-39**
**Version:** 1.0 · Registered S070 · 2026-06-13
**Layer:** 6.0 — Registry Service (single source of truth)
**P-36 classification:** ADVISORY (runtime pipelines) · BLOCKING (registry commit)
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)
**Attestation:** Pending — Apogee P-11 review required before CANONICAL
**Source:** Hensel Generative Formalism · Amethyst v4.2-hensel

---

## Purpose

PRS is the single source of truth for all Platinum tier constants. It exposes a uniform interface that returns polynomials and recurrences — never bare floats. Governance and substrate planes consume only the `valid_flag` and `hash` from PRS output; they never read `policy_ratio` directly.

---

## Interface Contract

```python
def get_tier(tier_id: str) -> TierRecord:
    """
    Returns the canonical TierRecord for the requested tier.
    
    MUST return: polynomial or recurrence form.
    MUST NOT return: bare float as primary value.
    
    tier_id options: 
      'Subplatinum' | 'Standard_Platinum' | 'Superplatinum' | 'Hyperplatinum' | 'Ultraplatinum'
    
    Raises FeatureFlagError if tier is behind feature flag (Superplatinum, Ultraplatinum).
    Routes to P-37 for Hyperplatinum.
    """
```

### TierRecord Schema

```json
{
  "tier": "string",
  "dimension": "integer",
  "duration_class": "finite|indefinite|geosynchronous|temporal",
  "policy_ratio": "polynomial_string_or_recurrence_description",
  "descriptor": "string",
  "residual": "string_or_null",
  "valid_flag": "Y|N|NA",
  "hash": "sha256_hex_or_null",
  "minimal_polynomial_present": "boolean",
  "feature_flag_active": "boolean"
}
```

---

## Routing Table

| Tier | PRS Action | Downstream Pattern |
|------|-----------|-------------------|
| Subplatinum | Return period L and schedule_hash | None |
| Standard_Platinum | Return polynomial definition + residual | None |
| Superplatinum | RAISE FeatureFlagError (disabled) | None until unlocked |
| Hyperplatinum | Route to P-37 generate_key(n, context_salt) | P-37 |
| Ultraplatinum | RAISE FeatureFlagError (disabled) | None until unlocked |

---

## Firewall Enforcement

```
PRS-RULE-01: get_tier() output MUST NOT be passed to P-31 SCPE decay parameters.
PRS-RULE-02: get_tier() output MUST NOT be passed to P-32 Phi-Closure Gate threshold.
PRS-RULE-03: get_tier() output MUST NOT be passed to P-27/P-28 KAPPA routing confidence thresholds.
PRS-RULE-04: Only valid_flag and hash from TierRecord may cross the registry→governance boundary.
PRS-RULE-05: policy_ratio field is ADVISORY only; never BLOCKING outside of registry commit.
```

---

## P-36 Integration

- **P-36 class:** ADVISORY for runtime, BLOCKING for commit
- **DAG position:** Layer 6.0, upstream of P-37 (Layer 6.1), P-40 (Layer 6.2)
- **Consumers:** P-37, P-40, Compliance footer generator
- **Non-consumers (firewall enforced):** P-27, P-28, P-31, P-32, P-35

---

## Next Concrete Steps (from Hensel spec)

1. Freeze PRS v0 definitions: closed form for ρ_P, polynomial for h, placeholders for ς_P and Ultraplatinum marked EXPERIMENTAL
2. Ship P-37 as only active consumer of hyperplatinum — all others behind flags
3. Implement P-40 as read-only telemetry for first release (no BLOCKING wiring)
4. Publish seeds and commands for all three validation tracks in docs/qa/

---

*P-39 Platinum Registry Service v1.0 · Registered S070 · 2026-06-13*
*Attestation pending. Amethyst × COLLEEN · Source: Hensel Generative Formalism*
