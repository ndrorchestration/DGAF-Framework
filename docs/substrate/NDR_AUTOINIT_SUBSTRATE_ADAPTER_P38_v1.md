# P-38 — Analytic Initialization Adapter (AutoInit)

**DGAF-Framework · NDR Pattern P-38**  
**Version:** 1.0 · Registered S070 · 2026-06-13  
**Layer:** 5.5 — Substrate Adapter  
**P-36 classification:** ADVISORY  
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)  
**Attestation:** Pending — Apogee P-11 review required before CANONICAL  
**Source:** AutoInit — Bingham & Miikkulainen (UT Austin / Cognizant AI Labs) · Hensel v4.2 substrate plane spec

> **Firewall rule:** Substrate plane uses AutoInit analytic gain per activation. Registry tier ratios (`pP`, `ρ`, `h`, etc.) MUST NOT enter gain computation.

> **Notation control:** Current mathematical notation is governed by `docs/governance/MATHEMATICAL_NOTATION_POLICY_METALLIC_MEANS_2026-08-28.md`. `pP` is DGAF-specific Platinum Mean notation for `1/(2sin(π/11)) ≈ 1.774732842`. `ρ` is the plastic number `≈1.3247179572447454`. `ρP` is not canonical mathematical notation.

---

## Purpose

P-38 specifies an analytic weight-initialization adapter intended to derive variance-preserving initialization from activation-function statistics. This is an architectural specification; implementation and empirical efficacy must be evidenced separately.

The adapter is intended to reduce dependence on topology-specific initialization heuristics where its mathematical assumptions are satisfied. Any cross-substrate or generalization claim requires reproducible evidence beyond the specification itself.

---

## Mathematical Foundation

### Variance-Preserving Objective

For a weight matrix W and activation function φ, the specification targets preservation of output/input variance under its stated assumptions:

```text
Var[W] = g^2 / (n_in * second_moment(φ))
```

Where:

- `g` = analytic gain derived from φ's second moment
- `n_in` = number of input connections
- `second_moment(φ)` = E[φ(x)^2] for x ~ N(0, 1)

### Prior Art Comparison

| Scheme | Activation Assumption | Variance Formula | Limitation |
|--------|----------------------|-----------------|------------|
| Xavier / Glorot | Linear / symmetric | 2 / (n_in + n_out) | Commonly tuned to activation assumptions |
| He / Kaiming | ReLU | 2 / n_in | Specialized to ReLU-family assumptions |
| **AutoInit (P-38)** | **Analytic, subject to stated assumptions** | **g^2 / n_in** | Requires validity of the analytic moment calculation |

### Gain Computation

The specification computes `g` by:

1. Evaluating `E[φ(x)^2]` for `x ~ N(0,1)` under the declared activation model.
2. Setting `g = 1 / sqrt(E[φ(x)^2])`.
3. Applying the resulting scaling to weight initialization.

For complex-valued layers, real and imaginary variance components are tracked independently where the implementation supports that model.

---

## The 1.7747 Value — Semantic Correction

Historical P-38 material associated **1.7747** with a "Standard Platinum" quantity and labeled it `ρ_P`. That terminology is superseded.

The current DGAF notation is:

- **`pP` / Platinum Mean:** `1/(2sin(π/11)) ≈ 1.774732842`, a DGAF-specific geometric quantity (unit-side regular-hendecagon circumradius).
- **`ρ` / plastic number:** `≈1.3247179572447454`, the real root of `x³ - x - 1 = 0`.

A benchmark RMSE value near `1.7747`, where present in historical source material, is an empirical benchmark figure and must not be represented as the mathematical definition of `pP`, as a plastic constant, or as an analytically discovered universal initialization constant without independent evidence.

If the historical sparse-coding benchmark table is retained, its values must be treated as **historical/contextual benchmark data**, not as DGAF/P-38 validation:

| Estimation Method | Historical RMSE |
|------------------|-----------------|
| Bicubic Interpolation | 2.5077 |
| Non-Local Means (NLM) | 2.1112 |
| Sparse Coding / Optimized Baseline | **1.7747** |
| SRCNN | 1.4836 |
| MFCN | 1.2026 |

The table does not establish that `pP` is a convergence constant, optimal scaling factor, or property of AutoInit. Any such claim requires source provenance and independent reproduction.

**Do NOT:** hard-code `1.7747` as a gain merely because it resembles `pP`. P-38 gain computation should use the declared activation-function moment calculation.

---

## AutoInit Performance Evidence

The historical performance figures below are retained as unverified/contextual material unless a reproducible source, dataset, command, environment, and retained output are supplied:

| Network Topology | Scheme | Historical Success Rate | Historical Final Accuracy |
|-----------------|--------|-------------------------|----------------------------|
| CNN | Xavier | 82% | 74.5% |
| CNN | AutoInit (P-38) | 99% | 78.2% |
| Transformer | He | 65% | 81.0% |
| Transformer | AutoInit (P-38) | 97% | 84.5% |
| Deep Residual | Data-Dependent | 88% | 80.1% |
| Deep Residual | AutoInit (P-38) | 98% | 82.3% |

**Evidence classification:** HISTORICAL / UNVERIFIED in this repository surface. These values do not establish DGAF/P-38 efficacy.

---

## DGAF Integration

### What P-38 specifies for DGAF agents

- Analytic initialization as a substrate adapter.
- Separation between governance-plane thresholds and substrate-plane initialization.
- A reproducible interface for recording activation assumptions, gain derivation, and initialization parameters.

### What P-38 does NOT touch

- P-27/P-28 KAPPA routing confidence thresholds (governance plane)
- P-31 SCPE decay parameters (governance plane)
- P-32 Phi-Closure Gate thresholds (governance plane)
- P-39 PRS `policy_ratio` values (registry plane)

---

## Research Provenance

| Milestone | Year | Contribution |
|-----------|------|--------------|
| Evolutionary Activation Discovery | 2020 | Meta-learning novel non-linearities (Bingham, Macke, Miikkulainen) |
| AutoInit Package Release | 2023 | Automated weight scaling for TensorFlow (Bingham, Miikkulainen) |
| Analytic Signal-Preserving Paper | 2026 | Formalization of analytic tracking (Bingham, Miikkulainen) |
| US Patent App 17/855,955 | — | System for evaluating weight initialization (Bingham, Miikkulainen) |
| Vera de Spinadel | 1990s | Metallic means family definition (mathematical foundation) |

Source-specific bibliographic verification remains a separate provenance task; the presence of a citation here is not independent validation of P-38.

---

## Substrate Study (Research Program Obligation)

**OPP-S070-001:** The repository source currently terminates mid-sentence at `Bit-identical a_n replay va...`. The previous file content is therefore incomplete at this boundary. The truncation has been preserved as an explicit integrity finding rather than silently inventing the missing research-program text.

Required follow-up is to recover the authoritative remainder from version history or another provenance-controlled source before this section is treated as complete.

## Epistemic Boundary

This document is an architectural specification and terminology correction. It does not establish P-38 efficacy, DGAF cross-substrate equivalence, production readiness, or PDMAL experimental validity.

**Current DGAF/PDMAL control state remains: PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
