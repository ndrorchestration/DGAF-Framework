# DGAF Related-Work Matrix

**Status:** Living prior-art map; comparative analysis, not a novelty verdict  
**Created:** 2026-08-25  
**Scope:** Multi-agent orchestration, governance, runtime assurance, evaluation, provenance, and reproducibility.

## Purpose

DGAF should not claim novelty merely because its terminology differs from existing systems. This matrix compares mechanisms and boundaries so that overlap, synthesis, and candidate distinctions can be stated precisely.

A source's absence from this matrix is not evidence that it is irrelevant. This is a bounded working map that must expand before any strong novelty claim.

## Comparison dimensions

| Dimension | Question |
|---|---|
| Orchestration | How are agents, roles, workflows, or topology coordinated? |
| Governance | Where are constraints and authorization decisions represented? |
| Runtime enforcement | Can controls mediate actions during execution? |
| Evaluation | How is system behavior measured or tested? |
| Provenance | What records support reconstruction or accountability? |
| Reproducibility | Are protocols, artifacts, versions, and analyses bound together? |
| Epistemic claims | How are implementation, verification, and empirical claims separated? |

## Comparative map

| Work / family | Primary contribution | Material overlap with DGAF | Candidate distinction requiring verification |
|---|---|---|---|
| Multi-agent orchestration research | Coordination architectures, roles, communication, and task decomposition | DGAF is also an orchestration substrate | DGAF may place governance and evidence controls alongside orchestration rather than treating coordination as sufficient |
| Trace-based assurance for agentic orchestration (2026) | Contracts, traces, deterministic replay, fault injection, runtime action mediation | Strong overlap in assurance, contracts, containment, and reproducibility | DGAF must demonstrate any architectural distinction at the implementation/specification level; terminology alone is not sufficient |
| Agentic AI governance frameworks | Lifecycle controls, risk mapping, audit, and accountability | Strong overlap in governance and provenance | DGAF's candidate contribution is the integration of claim/evidence governance with executable repository controls; this requires direct comparison |
| Runtime action-boundary governance | Trusted mediation between model proposals and side effects | Overlap in control-plane and fail-safe concepts | DGAF must not imply unique runtime governance unless its mechanism and scope materially differ |
| Agentic evaluation surveys and benchmarks | Metrics and evaluation across reasoning, planning, tools, and collaboration | Overlap in evaluation and measurement | DGAF's evidence ladder and claim-specific status model are governance artifacts, not demonstrated superior evaluation methodology |
| Transparency/provenance research | Trajectory accountability and audit-ready records | Strong overlap in lifecycle evidence and traceability | DGAF may contribute a repository-centered linkage between claims, evidence, implementation identity, and revision triggers |
| Formal methods and model checking | Bounded or formal verification of system properties | DGAF uses bounded verification for selected controls | Bounded verification must remain scoped and cannot be presented as proof of framework-wide correctness |

## Candidate contribution statement — provisional

> **DGAF is an open research and implementation framework that treats agent orchestration, governance controls, and evidence/claim provenance as coupled but separable concerns. Its candidate contribution is a repository-operational architecture in which claims are explicitly scoped to evidence, revision conditions, and versioned implementation artifacts rather than inferred from framework-level labels.**

This statement is a **definition of the proposed contribution**, not a claim of empirical superiority, universal novelty, or independent validation.

## What is currently defensible

- DGAF publicly documents an integrated implementation and governance approach for orchestration, evaluation, provenance, and epistemic controls.
- The repository contains claim/evidence indexing, bounded verification and deterministic testing for selected components, and explicit experimental gate controls.
- Current PDMAL efficacy remains unestablished: the corrected apparatus is pre-freeze, pilot authorization has not been granted, and empirical N remains 0.

## What is not currently defensible

- That DGAF is the first framework to combine these concerns.
- That the architecture is empirically better than alternatives.
- That repository-local verification establishes production readiness or general correctness.
- That conceptual similarity or difference can be determined from names alone.

## Required next comparisons

1. Build a source-level bibliography with stable identifiers and version dates.
2. Compare concrete mechanisms, not abstracts alone.
3. Identify whether each candidate DGAF distinction is unique, adapted, synthesized, or independently rediscovered.
4. Record contradictory evidence and prior art that narrows contribution claims.
5. Revise the candidate contribution statement before external publication if the comparison warrants it.

## Publication rule

External-facing materials may describe DGAF as a **distinct formulation or implementation** only when the statement is scoped to the documented formulation. Claims of novelty or priority require a substantially broader prior-art review and calibrated language.

## Cross-references

- `PUBLICATION_AND_PROVENANCE_SPINE.md`
- `CLAIM_EVIDENCE_INDEX.md`
- `PATTERN_COMMONS_ARCHITECTURE.md`
- `experiment/PDMAL_CURRENT_CONTROL_STATE.md`
- `experiment/PDMAL_EXPERIMENT_PROTOCOL.md`
