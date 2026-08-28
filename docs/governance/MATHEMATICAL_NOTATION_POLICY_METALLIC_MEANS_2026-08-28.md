# Mathematical Notation Policy — Metallic Means and Related Constants

**Date:** 2026-08-28  
**Status:** CANONICAL TERMINOLOGY POLICY  
**Scope:** DGAF mathematical references, PDMAL research documentation, public-facing notation

## Purpose

This policy separates established mathematical notation from DGAF-specific notation. A symbol must not be presented as standard mathematical notation merely because it is convenient inside DGAF.

## Canonical notation

### Golden ratio

\[
\varphi = \frac{1+\sqrt{5}}{2} \approx 1.6180339887\ldots
\]

`φ` / `\varphi` is the established conventional symbol for the golden ratio.

### Spinadel metallic-means family

The metallic means family is parameterized as

\[
\sigma_{p,q}=\frac{p+\sqrt{p^2+4q}}{2},\qquad p,q\in\mathbb Z_{>0},
\]

for the positive solution of

\[
x^2-px-q=0.
\]

For the ordinary one-parameter metallic sequence (`q=1`), use

\[
\sigma_n=\sigma_{n,1}=\frac{n+\sqrt{n^2+4}}2.
\]

Examples:

| Quantity | Canonical notation | Exact value |
|---|---|---|
| Golden mean | `σ₁,₁ = φ` | `(1+√5)/2` |
| Silver mean | `σ₂,₁` | `1+√2` |
| Bronze mean | `σ₃,₁` | `(3+√13)/2` |
| Subtle mean | `σ₄,₁` | `2+√5` |
| Copper mean | `σ₁,₂` | `2` |
| Nickel mean | `σ₁,₃` | `(1+√13)/2` |

`σ` is the family symbol. It must not be described as an exclusive symbol for silver.

### Plastic number

Use

\[
\rho \approx 1.324717957244746\ldots
\]

for the plastic number / plastic constant, the unique real root of

\[
x^3-x-1=0.
\]

`ρ` is the preferred canonical mathematical notation. `P` also occurs as an alternative notation in reference literature. `ρP` is not the canonical mathematical notation and must not be presented as such.

The plastic number is not a member of Spinadel's ordinary quadratic metallic-means family merely because it is sometimes discussed alongside metallic means. Its defining polynomial is cubic.

## DGAF-specific Platinum Mean

DGAF intentionally defines

\[
pP=\frac{1}{2\sin(\pi/11)}\approx1.774732842\ldots
\]

as **Platinum Mean**, the circumradius-to-side ratio of a regular hendecagon with unit side length.

This is a DGAF-specific notation. It is not to be represented as a standard member of the quadratic metallic-means family, and no claim should be made that `pP` is a universally established mathematical symbol.

The phrase **platinum number** is independently ambiguous in mathematical literature: it has been used for the plastic number in some references and for other constants in dodecagonal/lattice contexts. Therefore public DGAF material should use the explicit expression and the phrase **DGAF-specific Platinum Mean** when referring to `pP`.

## Prohibited semantic substitutions

The following substitutions are prohibited in current mathematical authority:

- `ρP` → plastic number as though `ρP` were the standard symbol.
- `pP` → plastic number.
- `pP` → a member of the Spinadel metallic-means family.
- `1.774732842` → `ρ`.
- `ρ` → `1/(2 sin(π/11))`.
- `σ` → silver mean without family context.
- "platinum ratio" → `1/(2 sin(π/11))` as an unqualified standard mathematical identity.

Historical documents may retain obsolete notation for provenance, but such notation must be visibly classified as historical/superseded where it could otherwise be mistaken for current authority.

## Evidence basis

The policy follows the established Spinadel family notation `σ_{p,q}` and the conventional use of `φ` for the golden ratio. Mathematical literature also uses `ρ` for the plastic number; some references additionally list `P` as an alternative. The terminology "platinum number" is not sufficiently unique to serve as an unqualified mathematical identifier.

## Epistemic boundary

This policy establishes terminology and notation only. It does not establish PDMAL convergence, contraction, robustness, security, superiority, production efficacy, or empirical validity.

**DGAF/PDMAL control state remains: PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
