# Repository Architecture Council — 2026-08-15

## Purpose

This is the cross-disciplinary review framework for improving the ndrorchestration repository ecosystem. It evaluates repositories according to their actual role rather than forcing every repository into the same maturity model.

## Council disciplines

1. Principal Systems Architecture — boundaries, topology, dependencies.
2. AI/Agent Architecture — orchestration, agent interfaces, control planes.
3. Research Science — hypotheses, methodology, falsifiability.
4. Experimental Science — reproducibility, baselines, instrumentation.
5. Evaluation/Statistics — metrics, calibration, uncertainty, benchmark validity.
6. Epistemic Audit — claim/evidence separation and provenance.
7. Software Architecture — APIs, modularity, maintainability.
8. Reliability/Operations — failure behavior, observability, deployment.
9. DevSecOps — secrets, dependencies, permissions, supply chain.
10. ML Engineering — model/data/inference boundaries.
11. Acoustic/Signal Engineering — ASIS and Acoustic-Mesh physical claims.
12. Control Systems — AHG/PDMAL control semantics.
13. Mathematical Review — formal definitions, derivations, source discipline.
14. Knowledge Architecture — GitHub/Notion/Vercel/document topology.
15. Technical Writing — README, quickstart, specifications, limitations.
16. Portfolio Review — demonstrability and professional signal.
17. UX/Product Architecture — runnable demonstrations and user paths.
18. Red Team — skeptical interpretation and failure modes.
19. Repository Maintenance — lifecycle, CI, releases, contribution hygiene.

## Review dimensions

Each repository is evaluated on:

- Identity and scope
- Architecture and boundaries
- Implementation quality
- Evidence quality
- Reproducibility
- Reliability and security
- Documentation
- Portfolio/demo value

## Maturity rule

A repository is not promoted merely because its documentation is polished. The preferred evidence chain is:

`CONCEPT → SPECIFICATION → IMPLEMENTATION → TEST → MEASUREMENT → ARTIFACT → DOCUMENTED CONCLUSION`

Claims must be classified separately from implementation and deployment status.

## Initial priority set

The first expert pass covers the highest-leverage/core systems:

| Repository | Primary class | Initial council priority |
|---|---|---|
| `DGAF-Framework` | Governance / evaluation research | Anchor / canonical vocabulary |
| `agent-control-plane` | Engineering / orchestration | High |
| `Driftwatch` | Evaluation / monitoring research | High |
| `Meshsense` | Application / runtime surface | Critical runtime gate |
| `Acoustic-mesh` | Acoustic / networking engineering | High experimental |
| `phi-calculus-app` | Mathematical visualization research | High evidence discipline |
| `AHG-Zeta-Pell-Autonomous-Lattice` | Mathematical/control research | High evidence discipline |
| `Amethyst-Governance-Eval-Stack` | Evaluation / governance | High |
| `sentinel-governance` | Governance | Medium-high |
| `3d-visualization-hub` | Visualization support | Medium |

Secondary, portfolio, archive, career, dashboard, and utility repositories remain distinct unless the evidence review shows that they belong in a core system boundary.

## Preliminary README-level findings

### DGAF-Framework
**Strengths:** explicit epistemic standard, canonical terminology, clear separation of related repositories, evidence-aware status language.

**Next audit:** verify that referenced standards, gates, registries, and cross-reference maps agree with the current 29-repository inventory; inspect actual implementation/tests rather than README claims.

### agent-control-plane
**Strengths:** appropriately conservative experimental-engineering boundary; explicit distinction between design specifications and implementation evidence.

**Next audit:** inspect source tree, interfaces, tests, CI, security, and whether the repository currently has enough implementation substance to justify its architectural role.

### Driftwatch
**Strengths:** explicit calibration/evidence boundary; operational quickstart; clear separation from governance projects.

**Next audit:** benchmark detector behavior, false positives/negatives, threshold provenance, reproducibility, and current Vercel runtime.

### Meshsense
**Strengths:** canonical GitHub identity is established and deployment identity is known.

**Blocking issue:** production deployment is READY but current runtime verification is authentication-constrained and prior observations showed a legacy runtime signature inconsistent with canonical source. Runtime closure remains PENDING until canonical-source deployment equivalence is demonstrated.

### Acoustic-mesh
**Strengths:** correctly framed as acoustic/WebRTC engineering rather than governance or architecture research; physical claims are explicitly evidence-gated.

**Next audit:** inspect actual signal-processing/network implementation, test fixtures, latency/quality measurements, sensor/acoustic methodology, and reproducible experiment protocol.

### phi-calculus-app
**Strengths:** unusually explicit mathematical boundary; defined recurrence and experimental geometry are distinguished from claims of established theory.

**Next audit:** formal derivations, numerical correctness, test coverage, provenance of mathematical claims, and whether the visualization communicates definitions versus empirical conclusions.

### AHG-Zeta-Pell-Autonomous-Lattice
**Next audit:** source recovery and Pass 2 evidence. Do not promote mathematical or control-theoretic claims beyond what derivations and reproducible computations support.

### Amethyst-Governance-Eval-Stack / sentinel-governance
**Next audit:** determine whether their boundaries remain complementary or whether functionality/documentation is duplicated with DGAF, Driftwatch, or the control-plane work.

## Anti-patterns this council is explicitly preventing

- Treating a README as validation.
- Treating deployment existence as runtime correctness.
- Treating runtime correctness as empirical system performance.
- Treating shared terminology as system equivalence.
- Treating historical benchmarks as current evidence.
- Treating mathematical vocabulary as mathematical proof.
- Promoting every repository into the core architecture.
- Rewriting documentation when the actual missing artifact is an experiment, benchmark, test, or deployment verification.

## Execution sequence

1. Core repository structural inspection.
2. Evidence and reproducibility inspection.
3. CI/security/reliability inspection.
4. Cross-repository interface and dependency audit.
5. Vercel/runtime reconciliation where applicable.
6. Notion registry reconciliation after substantive findings.
7. Targeted implementation/documentation changes.
8. Final ecosystem manifest update.

## Current evidence boundary

This document records the council framework and preliminary README-level assessment. It does **not** certify repository implementation quality. Repository-level conclusions require inspection of source, tests, workflows, deployment artifacts, benchmarks, and dated evidence.
