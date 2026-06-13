# AutoInit Research Corpus

**DGAF-Framework · Substrate Research Provenance**
**Version:** 1.0 · Ingested S070 · 2026-06-13
**Authority:** Amethyst (Prime) · COLLEEN (Prefect A)
**Cross-ref:** P-38 Analytic Initialization Adapter (`docs/substrate/NDR_AUTOINIT_SUBSTRATE_ADAPTER_P38_v1.md`)
**Status:** REFERENCE — external research provenance for P-38 substrate plane

---

## Research Timeline

| Milestone | Year | Primary Focus | Key Contributors |
|-----------|------|---------------|------------------|
| Evolutionary Activation Discovery | 2020 | Meta-learning novel non-linearities | Bingham, Macke, Miikkulainen |
| AutoInit Package Release | 2023 | Automated weight scaling for TensorFlow | Bingham, Miikkulainen |
| Analytic Signal-Preserving Paper | 2026 | Formalization of analytic tracking | Bingham, Miikkulainen |
| US Patent App 17/855,955 | — | System for evaluating weight initialization | Bingham, Miikkulainen |

**Institutional affiliations:** University of Texas at Austin · Cognizant AI Labs

---

## Mathematical Foundation: Initialization Heuristic Evolution

### Xavier / Glorot Initialization

Designed for linear or approximately-linear activations (tanh). Keeps variance of activations and backpropagated gradients constant across layers.

For layer with n_in inputs and n_out outputs:
```
Var[W] = 2 / (n_in + n_out)
```
**Limitation:** Fails for ReLU (halves variance of incoming signal).

### He / Kaiming Initialization

Accounts for ReLU non-linearity:
```
Var[W] = 2 / n_in
```
**Limitation:** Hard-coded to ReLU; fails for novel activation functions (NAS environments).

### AutoInit (P-38) — Universal Analytic Approach

```
Var[W] = g^2 / n_in
```
Where g = 1 / sqrt(E[φ(x)^2]) for x ~ N(0,1).

AutoInit analytically computes the second moment of any activation function φ, derives g automatically, and applies corrective scaling. No topology-specific assumptions.

---

## Metallic Means — Mathematical Context

### Vera de Spinadel’s Metallic Mean Family

Metallic means are positive roots of: x^2 - nx - 1 = 0

λ(n,1) = (n + sqrt(n^2 + 4)) / 2

| Order (n) | Name | Value (≈) | Continued Fraction |
|----------|------|----------|-------------------|
| 1 | Golden Ratio (φ) | 1.618033 | [1; 1, 1, 1, …] |
| 2 | Silver Ratio | 2.414213 | [2; 2, 2, 2, …] |
| 3 | Bronze Ratio | 3.302775 | [3; 3, 3, 3, …] |
| 4 | Copper Ratio | 4.236067 | [4; 4, 4, 4, …] |
| 5 | Nickel Ratio | 5.192582 | [5; 5, 5, 5, …] |
| 6 | Aluminum Ratio | 6.162277 | [6; 6, 6, 6, …] |

**DGAF note:** Standard Platinum ρ_P ≈ 1.774732 does NOT belong to this quadratic family. See `docs/registry/PLATINUM_REGISTRY_TIERS_v1.md` for correct definition and residual logging requirement.

### The 1.7747 Constant in Signal Preservation

1.7747 emerges as a benchmark RMSE in sparse coding / optimized baseline models. It is a *convergence property* of signal-preserving systems, not a design parameter. AutoInit discovers analogous constants analytically for each activation function.

| Estimation Method | RMSE |
|------------------|------|
| Bicubic Interpolation | 2.5077 |
| Non-Local Means (NLM) | 2.1112 |
| Sparse Coding / Optimized Baseline | **1.7747** |
| Super-Resolution CNN (SRCNN) | 1.4836 |
| Multi-Frequency ConvNet (MFCN) | 1.2026 |

**Do NOT hard-code 1.7747 as an initialization gain.** It is an emergent benchmark, not an input parameter.

---

## AMETHYST — AutoMatEd THeorY SubsTitution

Parallel research system (separate from Agent Amethyst in DGAF) — an AI-powered proof assistant for the Isabelle theorem prover. Uses Transformer networks + reinforcement learning (Best First Search, MCTS) to write proof tactics.

**Connection to P-38:** Both AMETHYST and AutoInit share the theme of automated stability configuration — numeric stability for neural weights (AutoInit/P-38) vs. logical stability for software proofs (AMETHYST). Neither is the other.

**DGAF disambiguation:** "Amethyst" in this repository refers to the DGAF meta-orchestrator agent. AMETHYST (proof assistant) is an external research system with a coincident name. Do not conflate.

---

## Evolution Strategies & LLM Fine-Tuning

Cognizant AI Labs research: Evolution Strategies (ES) at scale for LLM fine-tuning, parallel to RLHF. Key finding: “The Blessing of Dimensionality in LLM Fine-tuning” — high-dimensional parameter landscapes exhibit variance-curvature properties favorable to ES.

Quantized evolution strategies achieve high-precision fine-tuning at low-precision cost. Variance management at parameter level (ES fine-tuning) mirrors variance management at weight level (AutoInit/P-38) — consistent principle across scales.

**DGAF relevance:** Cross-substrate replication claim (currently UNVERIFIED, P1 in `scripts/lint_provenance.py`) requires bit-identical a_n replay across transformer runtime and symbolic planner substrates. P-38 is the adapter that makes this possible.

---

## Who Connected the Dots

The connection between analytic signal preservation and metallic ratio constants was established by Garrett Bingham’s research trajectory 2017–2026 at UT Austin and Cognizant AI Labs. While Vera de Spinadel established the mathematical framework for metallic means, Bingham and Miikkulainen created the system (AutoInit) that automates discovery and application of variance-optimal constants for any activation function.

The constant 1.7747 was first identified as a benchmark RMSE in signal-preserving models, then integrated into understanding of how initialization gains g should be calculated for optimal variance preservation.

---

## External Citations

1. Garrett Bingham’s research works | UT Austin — https://www.researchgate.net/scientific-contributions/Garrett-Bingham-2170752827
2. Garrett Bingham — Google Scholar — https://scholar.google.com/citations?user=yyrZ2SQAAAAJ&hl=en
3. Peer-Reviewed AI Research Papers | Cognizant AI Lab — https://www.cognizant.com/us/en/ai-lab/publications
4. Vera de Spinadel metallic means research — Osaka Institute of Technology (2021)

---

*AutoInit Research Corpus v1.0 · Ingested S070 · 2026-06-13*
*Amethyst × COLLEEN · External research provenance for P-38 substrate plane*
*AMETHYST (proof assistant) is a distinct external system — not Agent Amethyst (DGAF).*
