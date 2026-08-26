# DGAF Canonical Technical Overview

**Status:** Public technical overview; conceptual and implementation claims only unless separately evidenced  
**Version:** 0.1.0-draft  
**Date:** 2026-08-25

## Executive summary

**Dynamic Governance Agentic Formation (DGAF)** is an open research and implementation framework for designing and evaluating agentic systems in which orchestration is accompanied by explicit governance, provenance, and evidence controls.

DGAF starts from a practical systems problem: as AI systems become multi-step, tool-using, and multi-agent, evaluating a final answer alone is insufficient to characterize system behavior. Decisions, state transitions, delegated work, and external actions can introduce failure modes that are invisible in an output-only evaluation. DGAF therefore treats **behavioral control, traceability, and claim discipline as system concerns rather than documentation added after the fact**.

DGAF is a framework and implementation substrate, not a claim that any particular governance architecture has been empirically proven superior. Its components have different evidence states, and the repository's claim/evidence controls remain authoritative for those distinctions.

## 1. The problem

Agentic systems create a gap between what a system produces and how it behaves while producing it. A system may reach a superficially acceptable outcome while still exhibiting role drift, unsupported propagation, unsafe delegation, unrecoverable state transitions, or insufficient provenance for later inspection.

DGAF addresses the design question:

> How can an agentic system make governance constraints, execution controls, and evidence about its behavior inspectable without confusing implementation with empirical proof?

The framework does not assume that one control mechanism eliminates these failures. Instead, it provides a structure for specifying controls, testing bounded behavior, recording evidence, and keeping unresolved questions visible.

## 2. Core formulation

DGAF can be understood as a coordinated relationship among three system concerns:

1. **Formation and orchestration** — how agents, roles, tasks, and interactions are composed.
2. **Governance and control** — how constraints, gates, permissions, recovery behavior, and escalation boundaries influence execution.
3. **Evidence and provenance** — how claims, configurations, executions, artifacts, and limitations are recorded and related.

These concerns are analytically distinct but operationally connected. Orchestration without governance can optimize coordination without sufficient constraint. Governance without execution attachment can remain policy rather than control. Evidence without a relationship to the executed system can become narrative rather than verification.

This three-concern formulation is a **design model**, not a claim of exclusive novelty. The publication and prior-art process must determine which mechanisms are established, adapted, or distinct in DGAF's specific synthesis.

## 3. Architectural stance

DGAF treats governance as capable of participating in the control plane of an agentic system rather than existing solely as a policy document or retrospective review process. Depending on the component, controls may define invariants, gate transitions, constrain capabilities, record provenance, or require explicit evidence before a stronger claim is promoted.

The framework's epistemic stance is equally important: a passing test establishes only what that test and its scope support. Repository text, a deployment, a formal notation, or the existence of an implementation does not automatically establish efficacy, safety, novelty, or production readiness.

## 4. Evidence-aware development

DGAF uses claim-specific evidence rather than repository-wide certification. Public statements should distinguish at least:

- **Defined:** a concept or specification has been articulated.
- **Implemented:** an artifact or mechanism exists.
- **Verified:** a stated bounded check or test has succeeded within its defined scope.
- **Empirically supported:** a relevant experimental protocol and data support a scoped result.
- **Unknown or open:** evidence is absent, incomplete, or not yet applicable.

The exact canonical vocabulary and evidence status for individual claims remain governed by the repository's evidence standards and indexes.

## 5. Relationship to PDMAL

**Phi-Driven Multi-Agent Lattice (PDMAL / PDMA-L)** is a related lattice/control research track within the broader DGAF ecosystem. Shared terminology or repository location does not make DGAF and PDMAL equivalent.

The current PDMAL experimental track is **pre-freeze**. The corrected candidate apparatus has not been freeze-verified, pilot authorization has not been granted, and empirical **N = 0**. Consequently, this overview makes no claim that PDMAL improves coordination, reliability, fault tolerance, or other outcomes.

PDMAL may become a source of empirical research questions about orchestration topology and control. Those questions must be answered through the frozen protocol and evidence process rather than inferred from architecture alone.

## 6. What is currently inspectable

The public DGAF repository provides implementation and governance artifacts spanning agent orchestration, evaluation tooling, provenance practices, control and gate definitions, epistemic auditing, and experimental protocols. It is intended to be sufficiently inspectable for others to examine the framework's mechanisms and reproduce appropriately scoped repository-local behavior.

Inspection and reproducibility do not require agreement with the framework. Independent criticism, alternative implementations, null results, and failed replications are valuable evidence within the same epistemic model.

## 7. What DGAF does not currently claim

This overview does **not** claim that DGAF or PDMAL:

- has been empirically demonstrated to outperform alternative architectures;
- eliminates hallucination, drift, coordination failure, or other failure classes;
- constitutes a complete Byzantine Fault Tolerance protocol merely because of its topology;
- is independently validated as a complete framework;
- is production-ready as a whole; or
- is absolutely novel.

Such claims require claim-specific evidence and, where relevant, comparison and independent scrutiny.

## 8. Research questions

The framework motivates several research questions rather than presupposing their answers:

- Which governance controls improve measurable properties of agentic execution under defined conditions?
- Which controls merely move failure modes elsewhere or impose unacceptable coordination costs?
- How should evidence about multi-agent behavior be retained so that claims remain reproducible and auditable?
- Which architectural differences are meaningful under blinded or controlled comparison?
- What level of independent reproduction is necessary before a governance mechanism should be treated as reliable beyond its originating implementation?

These questions define a research agenda, not established findings.

## 9. Contribution hypothesis

DGAF's potential contribution is not the assertion that governance, orchestration, or provenance are individually new concepts. The candidate contribution is a **specific evidence-aware synthesis that connects formation, runtime-oriented governance, and claim/evidence provenance within one inspectable framework**, together with mechanisms and protocols intended to keep implementation status and empirical status separate.

Whether that synthesis is sufficiently distinct to constitute a novel research contribution remains subject to a scoped prior-art review. The appropriate public claim at present is therefore a documented formulation and implementation, not a verdict of priority.

## 10. How to evaluate the framework

DGAF should be evaluated on multiple axes:

1. **Specification quality:** Are concepts, invariants, assumptions, and failure conditions sufficiently precise?
2. **Implementation integrity:** Do mechanisms behave as their scoped tests specify?
3. **Reproducibility:** Can another party reproduce the relevant behavior from retained artifacts and instructions?
4. **Empirical efficacy:** Do controlled experiments demonstrate a benefit against defined baselines?
5. **Independence:** Do results survive scrutiny or reproduction outside the originating implementation?

Success on one axis must not be used as evidence for success on another.

## 11. Publication boundary

This document is designed as the canonical entry point for readers encountering DGAF externally. It should be read with the repository's current-state and claim/evidence documents, which take precedence for time-sensitive verification and gate status.

The public objective is **discoverability with epistemic integrity**: make the formulation sufficiently clear that others can identify what is proposed, what exists, what has been checked, and what remains unknown.

## Cross-references

- [`PUBLICATION_AND_PROVENANCE_SPINE.md`](PUBLICATION_AND_PROVENANCE_SPINE.md)
- [`CLAIM_EVIDENCE_INDEX.md`](CLAIM_EVIDENCE_INDEX.md)
- [`CURRENT_STATE.md`](CURRENT_STATE.md)
- [`README.md`](../README.md)
- [`PATTERN_COMMONS_ARCHITECTURE.md`](PATTERN_COMMONS_ARCHITECTURE.md)
- [`experiment/PDMAL_CURRENT_CONTROL_STATE.md`](experiment/PDMAL_CURRENT_CONTROL_STATE.md)
- [`experiment/PDMAL_EXPERIMENT_PROTOCOL.md`](experiment/PDMAL_EXPERIMENT_PROTOCOL.md)
