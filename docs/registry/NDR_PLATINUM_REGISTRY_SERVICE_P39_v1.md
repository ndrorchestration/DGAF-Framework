# P-39 — Platinum Registry Service (PRS)

**DGAF-Framework · NDR Pattern P-39**  
**Version:** 1.0 · Registered S070 · 2026-06-13  
**Layer:** 6.0 — Registry Service (single source of truth)  
**P-36 classification:** ADVISORY (runtime pipelines) · BLOCKING (registry commit)  
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)  
**Attestation:** Pending — Apogee P-11 review required before CANONICAL  
**Source:** Hensel Generative Formalism · Amethyst v4.2-hensel

> **Notation control:** Current mathematical notation is governed by `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`. `pP` is DGAF-specific Platinum Mean notation for `1/(2sin(π/11)) ≈ 1.774732842`; `ρ` is the plastic number `≈1.3247179572447454`; `ρP` is not canonical mathematical notation.

> **Epistemic boundary:** PRS is an interface/registry specification. It does not by itself establish that any tier is scientifically valid, production-ready, secure, or empirically effective.

---

## Purpose

PRS is the single source of truth for the project-defined Platinum tier registry. It exposes a uniform interface that returns polynomials, recurrences, or explicitly defined forms rather than bare floats as the primary representation. Governance and substrate planes consume only the declared interface fields that are permitted by the namespace firewall; they do not read `policy_ratio` directly where the firewall prohibits it.

---

## Interface Contract

```python
def get_tier(tier_id: str) -> TierRecord:
    """
    Returns the canonical TierRecord for the requested tier.

    MUST return: polynomial, recurrence, or explicit symbolic definition.
    MUST NOT return: bare float as the primary mathematical representation.

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
| Standard_Platinum | Return project-defined `pP = 1/(2sin(π/11))` plus explicit residual metadata where comparisons are made | None |
| Superplatinum | RAISE FeatureFlagError (disabled) | None until unlocked |
| Hyperplatinum | Route to P-37 generate_key(n, context_salt) | P-37 |
| Ultraplatinum | RAISE FeatureFlagError (disabled) | None until unlocked |

### Standard Platinum notation

`Standard_Platinum` uses **`pP` / Platinum Mean** only as project-defined notation:

`pP = 1/(2sin(π/11)) ≈ 1.774732842`

It is the unit-side regular-hendecagon circumradius. It is not the plastic number and is not a member of the quadratic Spinadel metallic-means family. Any historical `ρ_P` label for this value is superseded.

The mathematical plastic number is `ρ ≈ 1.3247179572447454`, the real root of `x^3 - x - 1 = 0`.

---

## Firewall Enforcement

```text
PRS-RULE-01: get_tier() output MUST NOT be passed to P-31 SCPE decay parameters.
PRS-RULE-02: get_tier() output MUST NOT be passed to P-32 Phi-Closure Gate threshold.
PRS-RULE-03: get_tier() output MUST NOT be passed to P-27/P-28 KAPPA routing confidence thresholds.
PRS-RULE-04: Only valid_flag and hash from TierRecord may cross the registry→governance boundary.
PRS-RULE-05: policy_ratio field is ADVISORY only; never BLOCKING outside of registry commit.
PRS-RULE-06: Legacy ρ_P notation MUST NOT be emitted as current mathematical authority.
```

---

## P-36 Integration

- **P-36 class:** ADVISORY for runtime, BLOCKING for commit
- **DAG position:** Layer 6.0, upstream of P-37 (Layer 6.1), P-40 (Layer 6.2)
- **Consumers:** P-37, P-40, Compliance footer generator
- **Non-consumers (firewall enforced):** P-27, P-28, P-31, P-32, P-35

---

## Next Concrete Steps (from Hensel spec)

1. Freeze PRS v0 definitions: project-defined `pP = 1/(2sin(π/11))`, polynomial/recurrence representation for h, and placeholders for Superplatinum and Ultraplatinum marked EXPERIMENTAL.
2. Ship P-37 as the only active consumer of Hyperplatinum — all others behind flags.
3. Implement P-40 as read-only telemetry for first release (no BLOCKING wiring).
4. Publish seeds and commands for all validation tracks in `docs/qa/`.
5. Preserve historical `ρ_P` terminology only in explicit supersession/provenance records.

---

*P-39 Platinum Registry Service v1.0 · Registered S070 · notation corrected 2026-08-28*  
*Attestation pending. Amethyst × COLLEEN · Source: Hensel Generative Formalism*

**Current DGAF/PDMAL control state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
