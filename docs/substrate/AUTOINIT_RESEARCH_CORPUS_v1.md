# AutoInit Research Corpus

**DGAF-Framework · Substrate Research Provenance**  
**Version:** 1.0 · Ingested S070 · 2026-06-13  
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)  
**Cross-ref:** P-38 Analytic Initialization Adapter (`docs/substrate/NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md`)  
**Status:** REFERENCE — external research provenance for P-38 substrate plane

> **Epistemic boundary:** This corpus records cited research context and historical project interpretations. Citation or mathematical plausibility does not by itself establish P-38 efficacy, DGAF cross-substrate equivalence, or PDMAL experimental validity.
>
> **Notation control:** `ρ` denotes the plastic number. `pP` / Platinum Mean is DGAF-specific notation for `1/(2sin(π/11)) ≈ 1.774732842`. `ρP` is not canonical mathematical notation.

---

## Research Timeline

| Milestone | Year | Primary Focus | Key Contributors |
|-----------|------|---------------|------------------|
| Evolutionary Activation Discovery | 2020 | Meta-learning novel non-linearities | Bingham, Macke, Miikkulainen |
| AutoInit Package Release | 2023 | Automated weight scaling for TensorFlow | Bingham, Miikkulainen |
| Analytic Signal-Preserving Paper | 2026 | Formalization of analytic tracking | Bingham, Miikkulainen |
| US Patent App 17/855,955 | — | System for evaluating weight initialization | Bingham, Miikkulainen |

**Institutional affiliations:** University of Texas at Austin · Cognizant AI Labs

The bibliographic claims above are retained as project provenance and require source-level verification before being used as authoritative external citations.

---

## Mathematical Foundation: Initialization Heuristic Evolution

### Xavier / Glorot Initialization

Designed for common linear/symmetric activation assumptions and widely used as a variance-scaling initialization family.

```text
Var[W] = 2 / (n_in + n_out)
```

The exact validity of any simplification depends on the activation and parameterization used.

### He / Kaiming Initialization

For ReLU-family assumptions:

```text
Var[W] = 2 / n_in
```

The method is specialized to its stated assumptions and should not be generalized to arbitrary activation functions without analysis.

### AutoInit (P-38) — Analytic Approach

```text
Var[W] = g^2 / n_in
```

where the project specification defines `g = 1 / sqrt(E[φ(x)^2])` for `x ~ N(0,1)` under the declared activation model.

This is the P-38 architectural formulation. Whether an implementation achieves the intended variance preservation across arbitrary activations is an empirical question requiring reproducible evaluation.

---

## Metallic Means — Mathematical Context

### Vera de Spinadel’s Metallic Mean Family

The ordinary metallic-mean sequence can be represented as the positive roots of:

```text
x² - n x - 1 = 0
```

with

```text
σ_n = (n + sqrt(n² + 4)) / 2
```

For the broader parameterization used in current DGAF documentation, use `σ_{p,q}` for the positive root of `x² - px - q = 0`.

| Order (n) | Name | Value (≈) | Continued Fraction |
|----------|------|----------|-------------------|
| 1 | Golden Ratio (φ) | 1.618034 | [1; 1, 1, 1, …] |
| 2 | Silver Ratio | 2.414213 | [2; 2, 2, 2, …] |
| 3 | Bronze Ratio | 3.302776 | [3; 3, 3, 3, …] |
| 4 | Copper Ratio | 4.236068 | [4; 4, 4, 4, …] |
| 5 | Nickel Ratio | 5.192582 | [5; 5, 5, 5, …] |
| 6 | Aluminum Ratio | 6.162278 | [6; 6, 6, 6, …] |

### DGAF Platinum Mean boundary

The DGAF-specific Platinum Mean is:

```text
pP = 1 / (2 sin(π/11)) ≈ 1.774732842
```

This is the unit-side circumradius of a regular hendecagon. It is not the plastic number and is not a member of the quadratic metallic-means family.

The mathematical plastic number is:

```text
ρ ≈ 1.324717957244746
```

as the real root of `x³ - x - 1 = 0`.

Historical `ρ_P` references for the `1.7747…` value are superseded notation and must not be used as current mathematical authority.

---

## The 1.7747 Value in Signal-Preservation History

Historical project material associates a value near `1.7747` with a sparse-coding/optimized-baseline RMSE. That is an empirical benchmark value in the cited context, not a mathematical constant and not evidence that AutoInit derives `pP`.

| Estimation Method | Historical RMSE |
|------------------|-----------------|
| Bicubic Interpolation | 2.5077 |
| Non-Local Means (NLM) | 2.1112 |
| Sparse Coding / Optimized Baseline | **1.7747** |
| Super-Resolution CNN (SRCNN) | 1.4836 |
| Multi-Frequency ConvNet (MFCN) | 1.2026 |

**Evidence classification:** HISTORICAL / SOURCE-DEPENDENT. These values must not be converted into a claim that `1.7747` is an initialization constant, a convergence constant, or the definition of `pP`.

**Do NOT:** hard-code `1.7747` as an initialization gain merely because it is numerically close to `pP`. P-38 gain computation is defined from the activation-function moment model, not from this benchmark value.

---

## AMETHYST — Disambiguation

Parallel research system (separate from Agent Amethyst in DGAF) — an AI-powered proof-assistant research effort. Uses the name AMETHYST independently.

**DGAF disambiguation:** "Amethyst" in this repository refers to the DGAF meta-orchestrator agent. AMETHYST is a distinct external research reference. Do not conflate the identities.

---

## Evolution Strategies & LLM Fine-Tuning

Cognizant AI Labs research on Evolution Strategies (ES) for LLM fine-tuning is retained as contextual research provenance.

Claims that variance management at parameter level is analogous to variance management at weight level are architectural analogies, not proof of equivalence.

**DGAF relevance:** The cross-substrate replication claim remains **UNVERIFIED**. P-38 may be an adapter in that research design, but the repository does not presently establish bit-identical `a_n` replay across transformer and symbolic-planner substrates as an achieved result.

---

## Who Connected the Dots

Historical project material described a connection between analytic signal preservation and metallic-ratio terminology. That connection is retained as project history, not as an established external mathematical result.

In particular, the `1.7747` benchmark value must not be retroactively interpreted as proof of the DGAF-defined `pP` quantity or as evidence that AutoInit analytically “discovers” that same value in all activation regimes.

---

## External Citations

1. Garrett Bingham’s research works | UT Austin — <https://www.researchgate.net/scientific-contributions/Garrett-Bingham-2170752827>
2. Garrett Bingham — Google Scholar — <https://scholar.google.com/citations?user=yyrZ2SQAAAAJ&hl=en>
3. Peer-Reviewed AI Research Papers | Cognizant AI Lab — <https://www.cognizant.com/us/en/ai-lab/publications>
4. Vera de Spinadel metallic means research — Osaka Institute of Technology (2021)

These references are pointers, not independently verified evidence in this repository. Source-level verification is required before citing any individual claim as authoritative.

---

*AutoInit Research Corpus v1.0 · Ingested S070 · notation/evidence correction 2026-08-28*  
*Amethyst × COLLEEN · External research provenance for P-38 substrate plane*  
*AMETHYST (proof-assistant research reference) is distinct from Agent Amethyst (DGAF).*

**Current DGAF/PDMAL control state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
