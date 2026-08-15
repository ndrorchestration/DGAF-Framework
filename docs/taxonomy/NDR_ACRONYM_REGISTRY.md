# NDR Acronym Registry

**Status:** CANONICAL REGISTRY / epistemic vocabulary control
**Date:** 2026-08-15

## Purpose

This registry establishes the canonical expansion and scope of acronyms used across the NDR project ecosystem. An acronym's expansion is a **DEFINED vocabulary fact**; it does not establish that the named system is implemented, validated, or equivalent to an external technology.

When an acronym has conflicting historical expansions, the conflict is recorded rather than silently erased.

## Canonical acronyms

| Acronym | Canonical expansion | Scope / meaning | Evidence status | Notes |
|---|---|---|---|---|
| **AHG** | Adaptive Harmonic Governance | DGAF governance/control framework and related components | DEFINED; implementation varies by artifact | Do not use "Adaptive Hierarchical Governance" as the current expansion. That wording is historical/inconsistent. |
| **AH3** | Adaptive Harmonic-Hierarchical Hybrid | Historical AHG/Zeta-Pell naming variant | HISTORICAL | Not the canonical expansion of AHG. |
| **ASIS** | Acoustic Spatial Insight System | Acoustic/spatial perception system | DEFINED | Canonical expansion established 2026-08-14. |
| **SIL** | Spatial Intelligence Layer | Perception/spatial abstraction layer within the ASIS concept | DEFINED | Do not imply a standardized external technology. |
| **PDMAL / PDMA-L** | Phi-Driven Multi-Agent Lattice | Dodecahedral-graph lattice/control structure and associated formalism | VERIFIED for explicitly tested graph/math quantities; DEFINED for architecture | Not established as a complete BFT consensus protocol. |
| **DGAF** | Dynamic Governance Agentic Formation | Agentic governance/orchestration framework | DEFINED; implementation evidence is artifact-specific | Do not infer capability from framework name alone. |
| **SACP** | Semantic/Systems? — **UNRESOLVED IN CURRENT GITHUB SURFACE** | Historical term requiring source-of-truth confirmation | AMBIGUOUS | Do not invent an expansion. Preserve the acronym until a canonical source is located. |
| **BFT** | Byzantine Fault Tolerance | Established distributed-systems fault model/property | EXTERNAL STANDARD TERM | PDMAL is not automatically BFT merely because BFT terminology appears nearby. |
| **AXIS** | **SOURCE-DEPENDENT / REQUIRES CANONICAL EXPANSION CHECK** | DGAF metric/constraint vocabulary | AMBIGUOUS | Search results establish AXIS as a project term, but this registry does not promote an unverified backronym to canonical status. |
| **MDAR** | **SOURCE-DEPENDENT / REQUIRES CANONICAL EXPANSION CHECK** | DGAF protocol reference | AMBIGUOUS | Existing documents use the acronym; expansion must be recovered from its canonical protocol document before normalization. |
| **KB** | Knowledge Base | Agent knowledge/documentation artifact | STANDARD / DEFINED | Descriptive, not a capability claim. |
| **QA** | Quality Assurance | Testing/review terminology | STANDARD / DEFINED | Does not imply that quality has been demonstrated unless tests are actually run. |
| **API** | Application Programming Interface | Software interface | STANDARD / DEFINED | Standard external term. |
| **CSV** | Comma-Separated Values | Tabular data format | STANDARD / DEFINED | Standard external term. |
| **JSON** | JavaScript Object Notation | Structured data format | STANDARD / DEFINED | Standard external term. |
| **TF-IDF** | Term Frequency–Inverse Document Frequency | Text-weighting method | STANDARD / DEFINED | Used in the Semantic Entropy detector's similarity graph. |
| **MSE** | Mean Squared Error | Error metric | STANDARD / DEFINED | Must retain its actual calculation context. |
| **PAR** | Packet Acceptance Rate | AHG/Zeta-Pell benchmark metric | DEFINED in project artifact | Historical numerical values require provenance/recomputation. |
| **AR** | Augmented Reality | Spatial/phone perception context | STANDARD / DEFINED | Do not imply AR capability beyond the implemented platform. |
| **SLAM** | Simultaneous Localization and Mapping | Spatial-computing method | STANDARD / DEFINED | Do not claim a SLAM implementation unless source code/evaluation supports it. |
| **PID** | Proportional–Integral–Derivative | Control method | STANDARD / DEFINED | AHG/Zeta-Pell usage must correspond to actual PID implementation. |
| **FML** | **CONTEXT-DEPENDENT / REQUIRES SOURCE CHECK** | Historical AHG/Zeta-Pell mitigation terminology | AMBIGUOUS | Do not expand from inference. |
| **PDM** | **DO NOT ASSUME PDMAL** | Possible project-local abbreviation | AMBIGUOUS | Similar-looking acronyms are not interchangeable. |

## Critical acronym controls

### 1. One acronym, one current canonical expansion

An acronym may have historical expansions, but only one should be marked `CANONICAL` for the current ecosystem. Historical variants remain traceable.

### 2. Similar acronyms are not aliases

`PDM`, `PDMA`, `PDMAL`, and `PDMA-L` must not be silently normalized to one another. Use the exact project-defined form.

### 3. Acronym expansion is not evidence

For example:

`PDMAL = Phi-Driven Multi-Agent Lattice`

does not prove any particular convergence, consensus, governance, or fault-tolerance property.

### 4. Do not backronym ambiguous terms

If source evidence does not establish what an acronym expands to, mark it `AMBIGUOUS` rather than constructing an expansion that merely fits the surrounding concept.

### 5. Mathematical acronyms receive the same epistemic treatment

A mathematical or scientific acronym can be correctly expanded while its use in a project remains only analogous. The external definition and the project's implementation must be documented separately.

## Known conflicts requiring source-level resolution

### AHG

Current canonical expansion: **Adaptive Harmonic Governance**.

Historical/inconsistent expansion: **Adaptive Hierarchical Governance**.

Historical hybrid: **Adaptive Harmonic-Hierarchical Hybrid (AH3)**.

The Zeta-Pell audit documented this conflict directly. It must not be silently reintroduced into current taxonomy.

### SACP

The acronym is present in historical project context, but the current repository search did not provide sufficient evidence to safely expand it. Until its canonical source is located, it remains `UNRESOLVED`.

### AXIS / MDAR / FML

These are established project-local tokens, but their expansions require direct inspection of their canonical specifications. Do not infer expansions from file names or surrounding prose.

## Audit rule

Future acronym sweeps must report:

1. acronym token;
2. every materially different expansion found;
3. canonical expansion, if established;
4. source file(s);
5. evidence class;
6. whether the expansion is current, historical, ambiguous, or deprecated;
7. whether the acronym is being used as an external-standard term or an NDR-local term.

**No acronym is considered reconciled merely because one plausible expansion exists.**
