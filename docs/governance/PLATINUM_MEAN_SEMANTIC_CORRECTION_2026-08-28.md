# Platinum Mean / Plastic Constant Semantic Correction

**Date:** 2026-08-28  
**Status:** Active semantic-control record  
**Scope:** DGAF terminology and PDMAL mathematical references

## Canonical notation correction

DGAF intentionally uses **pP / Platinum Mean** for the regular-hendecagon unit-side circumradius:

`pP = 1 / (2 sin(π/11)) ≈ 1.774732842`

The mathematical **plastic number / plastic constant** is instead conventionally denoted:

`ρ ≈ 1.3247179572447454`, the unique real root of `x³ - x - 1 = 0`.

Some references also use `P` for the plastic number. `ρP` is not the canonical mathematical notation and must not be presented as such.

These quantities are distinct and must not be conflated.

## Metallic-means family boundary

The Spinadel metallic-means family is conventionally parameterized as

`σ_{p,q} = (p + √(p² + 4q)) / 2`,

for the positive root of `x² - px - q = 0`. For the ordinary sequence, `σ_n = σ_{n,1}`. Thus `φ = σ_{1,1}` is the golden ratio, `σ_{2,1}` is silver, and `σ_{3,1}` is bronze. The plastic number `ρ` is cubic and is not thereby a member of this quadratic family.

## PDMAL boundary

The PDMAL plastic-constant convergence mathematics uses `ρ`, not `pP`. Historical documents that call `1.7747` or `1.77473` `ρP`, `ρ`, or "Platinum Ratio" are semantic predecessors and must be treated as historical/superseded terminology unless independently re-derived under current governance.

The correction does **not** invalidate the geometric quantity `1.774732842`; it changes its semantic classification to the DGAF-defined `pP / Platinum Mean` where that notation is intended.

## Platinum terminology boundary

The phrase **platinum number** is overloaded in mathematical literature: some sources use it as an alternative name for the plastic number, while other mathematical/physical literature uses platinum-number/ratio terminology for different geometric constants. DGAF therefore must not present "Platinum Mean" or "platinum ratio" as a universally standardized mathematical name for `1/(2 sin(π/11))`.

## Affected historical material

Repository-wide searches identified historical/current-surface references including:

- `docs/formalism/constants/11Q-derivation.md`
- `docs/formalism/hensel-general-formalism.md`
- `docs/registry/PLATINUM_REGISTRY_TIERS_v1.md`
- `docs/architecture/platinum-convergence-audit-v1.md`
- `docs/gates/NDR_HENSEL_FIREWALL_RULES_v1.md`

Those documents must not be treated as current mathematical authority solely because they remain in the repository. Where practical, their current status should be revised or an explicit supersession note should be added. Historical evidence should be preserved rather than silently deleted.

## Canonical policy

The complete notation hierarchy is maintained in:

`docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`

That policy is authoritative for current DGAF mathematical notation.

## Epistemic boundary

This correction establishes terminology only. It does not establish PDMAL convergence, contraction, robustness, security, superiority, production efficacy, or empirical validity.

**Current DGAF/PDMAL control state remains: PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
