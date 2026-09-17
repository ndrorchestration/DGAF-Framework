# PDMAL Structural Predictor Registry

> **Status:** EXPLORATORY / FUTURE-WORK QUARANTINE  
> **Scientific-state effect:** NONE  
> **Current Track A Epoch 002 primary-analysis effect:** NONE  
> **Established:** 2026-09-17

## Purpose

This registry predefines graph-structural quantities that may be useful in **future** PDMAL analyses or separately preregistered experiments.

It does **not** amend the current Track A Epoch 002 protocol, add a current primary endpoint, authorize analysis, or permit exploratory access to locked/unmaterialized outcome data.

At establishment:

- Epoch 002 dataset lock is established;
- bounded unblinding is authorized only for its accepted controlled scope;
- real materialization is not established;
- primary analysis is not authorized and has not run;
- scientific N increment remains 0.

## Epistemic rule

A structural graph quantity is a **predictor or mathematical property**, not evidence of agentic efficacy by itself.

The allowed inference form is:

```text
verified graph property -> verified property of that graph
```

The prohibited inference form without experiment is:

```text
verified graph property -> superior agentic robustness/performance
```

Any relationship between topology statistics and observed agent outcomes remains empirical.

## Graph representation contract

Before calculating a predictor, the analysis must declare:

- graph identity/version;
- directed vs undirected;
- simple vs multigraph;
- weighted vs unweighted;
- static vs temporal;
- whether self-loops are admitted;
- whether transformations/symmetrization were applied;
- node and edge inclusion criteria.

A predictor calculated on a transformed graph must be labeled as a property of that transformed representation.

## Predictor families

### P-STR-01 — Size and density

Candidate quantities:

- number of vertices `|V|`;
- number of edges `|E|`;
- density;
- mean degree;
- degree variance;
- maximum degree.

**Interpretation:** descriptive structure only.

### P-STR-02 — Vertex connectivity

Candidate quantity:

```text
kappa(G)
```

minimum number of vertices whose removal disconnects the graph, under the declared graph convention.

**Hypothesis family:** higher vertex connectivity may reduce sensitivity to some node-failure patterns.

**Caveat:** connectivity alone does not determine LLM-agent error propagation, message semantics, or correction quality.

### P-STR-03 — Edge connectivity

Candidate quantity:

```text
lambda_edge(G)
```

minimum number of edges whose removal disconnects the graph.

Keep notation distinct from Laplacian eigenvalues.

### P-STR-04 — Diameter and path length

Candidate quantities:

- graph diameter;
- mean shortest-path length;
- eccentricity distribution;
- path-length distribution.

Potential outcomes to compare prospectively include correction latency and communication cost.

### P-STR-05 — Global efficiency

Candidate quantity:

```text
E_global(G) = average_{i != j} 1 / d(i,j)
```

using an explicitly declared convention for disconnected pairs.

### P-STR-06 — Algebraic connectivity

For a compatible undirected graph representation, candidate quantity:

```text
lambda_2(L)
```

where `L` is the declared graph Laplacian and `lambda_2` is the second-smallest eigenvalue.

**Hypothesis family:** algebraic connectivity may predict mixing, consensus, or failure resilience under some dynamical models.

**Boundary:** this does not imply that LLM-agent message passing obeys a linear consensus process.

### P-STR-07 — Normalized spectral gap

Where justified, record eigenvalues of the normalized Laplacian or a declared stochastic/transition matrix.

Any spectral interpretation must identify the matrix and model. Different matrices are not interchangeable.

### P-STR-08 — Clustering

Candidate quantities:

- local clustering coefficient distribution;
- global/transitivity coefficient.

Potential research question: whether local redundancy improves correction or instead increases local correlated reinforcement.

### P-STR-09 — Centralization and concentration

Candidate quantities:

- degree centralization;
- betweenness centralization;
- eigenvector-centrality concentration where mathematically appropriate;
- maximum-node share of shortest paths.

Potential research question: whether highly concentrated communication creates single points of epistemic amplification or control.

### P-STR-10 — Betweenness distribution

Record node and edge betweenness with the exact weighting convention.

Potential future use: compare structurally critical edges/nodes against measured ablation effects.

### P-STR-11 — Expansion / conductance

Candidate quantities include exact or approximate:

```text
h(G)     # Cheeger/isoperimetric quantity under a declared definition
phi(G)   # conductance under a declared definition
```

Definitions vary; the exact formula and normalization must be preserved with the result.

### P-STR-12 — Path redundancy

Prospective measures may include:

- count of internally vertex-disjoint paths between designated node pairs;
- edge-disjoint path counts;
- average alternate-path availability under controlled failures.

### P-STR-13 — Cut-set exposure

Candidate quantities:

- minimum cut size;
- number/distribution of small cuts;
- fraction of communication demand traversing identified cuts.

### P-STR-14 — Curvature

Graph curvature may be explored only when the exact definition is declared, e.g.:

- unweighted Forman-Ricci curvature;
- augmented Forman curvature;
- Ollivier-Ricci curvature with declared transport/idleness parameters.

Different curvature definitions are not interchangeable. A curvature value is a graph property under its specified definition, not an agentic robustness result.

### P-STR-15 — Motif and community structure

Candidate quantities:

- motif counts relevant to communication loops;
- modularity under a declared method;
- community-size distribution;
- bridge-edge counts.

These remain exploratory unless separately preregistered.

## Outcome families for future testing

Possible outcomes for a future protocol include:

- fault/failure containment;
- task success;
- false-consensus rate;
- minority-correction rate;
- time/turns to correction;
- communication/token cost;
- tool-call cost;
- message count;
- latency;
- evidence-source diversity;
- epistemic amplification without evidence gain.

If a future PDMAL protocol reuses an existing endpoint name such as `ffcr_success`, that reuse must preserve the exact endpoint definition or explicitly declare a new version.

## Predictor-selection discipline

For any future confirmatory predictor study:

1. choose the predictor set before outcome inspection;
2. define every graph transformation before calculation;
3. freeze code/version/hash for predictor generation;
4. declare primary vs secondary predictors;
5. declare directionality only where genuinely justified;
6. specify multiplicity control or hierarchical testing;
7. define missing/undefined predictor handling;
8. use held-out or prospective data for predictive claims where practical;
9. retain null and contradictory findings;
10. separate explanatory fit from out-of-sample prediction.

## Current classification

All quantities newly introduced by this document are **EXPLORATORY / FUTURE WORK** relative to the currently locked Track A Epoch 002 primary analysis unless an older accepted protocol independently preregistered the exact same quantity and role.

This registry must not be used to reinterpret the current locked analysis plan after outcome access.

## Relationship to known PDMAL invariants

Previously verified graph facts, when exact-scope evidence exists, remain mathematical properties of their specified graph. This registry does not revise or supersede those facts. It only prevents their conversion into an efficacy claim without empirical evidence.

## Future test model

A future analysis may evaluate a model of the form:

```text
structural predictors X(G)
  -> prospective outcome Y(G, failure_condition, seed, task)
```

The empirical question is whether `X(G)` predicts `Y` beyond appropriate baselines and whether that relationship generalizes.

## External methodology anchors

- Li et al. (2026), *Discovering Efficient and Explainable Communication Topologies for LLM-based Multi-Agent Systems via Causal Inference*, arXiv:2608.12921. https://arxiv.org/abs/2608.12921
- Network-science and graph-theoretic alignment already recorded in `../evidence/PDMAL_EXTERNAL_ALIGNMENT.md`.

External results establish precedent, not PDMAL-specific evidence.
