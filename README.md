# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for building multi-agent AI systems with governance, provenance, evaluation, and fail-closed controls built into the orchestration layer.

Instead of treating governance as documentation added after deployment, DGAF explores what happens when agents, evidence, permissions, evaluation, and operational boundaries are governed as part of the system itself.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Separate bounded Solo track:** Experiment 001 executed but exposed a treatment-binding defect and is retained as apparatus-falsification evidence, not efficacy evidence. A subsequent non-empirical P-30 remediation diagnostic passed; no fresh empirical rerun is authorized.

## What DGAF explores

DGAF focuses on several problems that become increasingly important as AI systems become more autonomous:

- **Multi-agent orchestration** — coordinating specialized agents under explicit roles and constraints.
- **Provenance** — tracking where outputs, evidence, decisions, and system state came from.
- **Governance** — making authority, permissions, transitions, and failure conditions explicit.
- **Evaluation integrity** — separating tested behavior from unsupported claims.
- **Fail-closed design** — preventing missing evidence or uncertain state from silently becoming authorization.
- **Experimental reproducibility** — binding results to specific system, protocol, and evidence identities.

## Core idea

A capable AI system should not only produce answers.

It should also be able to answer:

- What evidence supports this?
- Which system state produced it?
- Who or what had authority?
- What assumptions remain unverified?
- Can the result be independently reproduced?
- Should execution continue when required evidence is missing?

DGAF is an attempt to make those questions part of the architecture.

## Current development

The repository currently includes working and tested components for:

- governed multi-agent orchestration;
- provenance and evidence contracts;
- deterministic validation and negative controls;
- candidate and experimental-state management;
- evaluation tooling;
- security and custody mechanisms;
- CI-based governance checks;
- blinded-experiment preparation.

The canonical High-Assurance track is currently progressing through pre-freeze engineering and independent-review preparation.

A separate bounded Solo track has also been used to test the apparatus. Its first final experiment exposed a deterministic P-30 treatment-binding defect before the intended DGAF treatment behavior could be evaluated. That run remains retained as falsification evidence; it is not pooled, repaired in place, or reported as an efficacy result.

Historical engineering and experimental records remain scoped to the exact system identities and predicates that produced them and are not treated as evidence for later versions automatically.

## Research boundary

DGAF distinguishes among three evidence classes.

### Engineering evidence

Tests, CI runs, deterministic checks, provenance validation, security controls, and explicitly non-empirical diagnostics.

### Apparatus-falsification evidence

Executions that reveal a protocol or treatment-binding defect and therefore test the experimental apparatus without supporting an efficacy inference.

### Efficacy evidence

Results from an authorized experimental protocol whose apparatus, treatment binding, blinding, and evidence chain remain valid for the intended scientific comparison.

The repository contains substantial engineering evidence and retained apparatus-falsification evidence. It does not yet contain valid DGAF efficacy evidence. The canonical High-Assurance PDMAL track remains empirical N = 0.

## Why this repository exists

The broader goal is to investigate whether multi-agent AI systems can become more:

- auditable,
- falsifiable,
- reproducible,
- resistant to silent authority drift,
- and explicit about what they actually know versus what remains unverified.

DGAF is both an implementation project and an experimental research platform for testing that idea.

## Project status

Active research and development.

The framework is not presented as empirically validated, production-certified, or currently authorized for a fresh empirical run.

Detailed governance state, evidence records, protocol controls, and historical verification artifacts are maintained inside the repository for technical review.

---

Dynamic Governance Agentic Formation  
Multi-agent orchestration · AI governance · provenance · evaluation · experimental integrity
