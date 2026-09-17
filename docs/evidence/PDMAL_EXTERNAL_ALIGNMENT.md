# PDMAL External Methodology Alignment

The PDMAL topology experiment should align its design with established network-science and distributed-systems evaluation practice without treating those sources as evidence for PDMAL itself.

## Alignment targets

- Graph-theoretic definitions: connectivity, diameter, degree, efficiency.
- Network robustness: random and targeted failure analysis.
- Small-world comparison: Watts-Strogatz family.
- Multi-agent consensus: convergence and failure behavior under communication constraints.
- Experimental design: paired stochastic trials, preregistration, effect sizes, confidence intervals, and multiplicity control.
- Reproducibility: frozen manifests, seeds, environment records, raw data, and analysis scripts.

## 2026-09-17 research extensions

The following research directions are now formalized as **exploratory / future work** and have **no current scientific-state effect**:

- structural graph predictors such as connectivity, algebraic connectivity, expansion/conductance, path redundancy, centralization, and explicitly defined curvature measures;
- communication-edge ablation as a prospective way to estimate which edges have measurable causal importance;
- provenance/evidence dependence as a separate variable from communication topology;
- correlated-verification and false-consensus measurements;
- comparison of structural predictions against observed robustness rather than assuming a graph invariant implies an agentic advantage.

See:

- `../research/STRUCTURAL_EPISTEMICS_RESEARCH_PROGRAM.md`;
- `../governance/CORRELATED_VERIFICATION_THREAT_MODEL.md`;
- `../experiment/PDMAL_STRUCTURAL_PREDICTOR_REGISTRY.md`;
- `../experiment/PDMAL_CRITICAL_EDGE_ABLATION_PROTOCOL.md`;
- `../research/MATHEMATICAL_CLAIM_CLASSIFICATION_STANDARD.md`.

These additions do **not** amend the locked Track A Epoch 002 primary analysis, authorize materialization or analysis, or permit post-hoc promotion of newly introduced predictors to confirmatory status.

## External methodological context

Recent multi-agent research provides methodological precedent for treating communication structure and dependence as measurable variables:

- Li et al. (2026), *Discovering Efficient and Explainable Communication Topologies for LLM-based Multi-Agent Systems via Causal Inference*, arXiv:2608.12921, uses communication-edge interventions/masking as part of causal topology analysis. [arXiv:2608.12921](https://arxiv.org/abs/2608.12921)
- Garg et al. (2025), *Correlated Errors in Large Language Models*, arXiv:2506.07962 / ICML 2025, documents substantial correlation among LLM errors. [arXiv:2506.07962](https://arxiv.org/abs/2506.07962)
- Wu, Li & Li (2025), *Can LLM Agents Really Debate?*, arXiv:2511.07784, studies majority pressure, correction, and group diversity in controlled multi-agent debate. [arXiv:2511.07784](https://arxiv.org/abs/2511.07784)

These sources motivate questions and methods. They are not evidence of a PDMAL-specific advantage.

## Evidence boundary

Literature establishes definitions and methodological precedent. The PDMAL advantage remains a hypothesis until the preregistered experiment produces and analyzes observations under the applicable governed authorization path.
