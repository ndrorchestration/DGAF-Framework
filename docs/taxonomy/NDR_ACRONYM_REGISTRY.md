# NDR Acronym Registry

**Status:** CANONICAL REGISTRY / epistemic vocabulary control  
**Date:** 2026-09-06

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
| **PDMAL / PDMA-L** | Phi-Driven Multi-Agent Lattice | Lattice/control research architecture; topology is an experimental/design variable rather than implied by the acronym | DEFINED for architecture; graph/math quantities are VERIFIED only where explicitly tested | Current active identity. Dodecahedral math may be verified without establishing dodecahedral efficacy or making that topology constitutive. |
| **PDMAL-D** | Phi-Dodecahedral Multi-Agent Lattice | Prospective successor identity in which dodecahedral topology would be constitutive | PROSPECTIVE / NOT_TRIGGERED | Evidence-gated naming transition. Do not describe PDMAL-D as active, canonical architecture, or established successor until the transition gate is satisfied. |
| **DGAF** | Dynamic Governance Agentic Formation | Agentic governance/orchestration framework | DEFINED; implementation evidence is artifact-specific | Do not infer capability from framework name alone. |
| **PHDGE** | Phi-Harmonic Dynamic Governance Ecosystem | Historical umbrella/ensemble brand in older ops/generator material | HISTORICAL / NON-CANONICAL | Preserve as lineage only. It is not current authority, not the active ensemble identity, and must not replace current NDR AI Systems ecosystem framing without a new explicit naming decision. |
| **PPTL** | Phi-Pentagon Topology Lab | Repository-local topology/governance harness name | DEFINED; implementation/evidence remains artifact-specific | Supported by `pptl/README.md` and `pptl/__init__.py`; older competing expansions are historical/current-facing residue, not equal canonical candidates. |
| **AXIS** | Agent X-axis Invariant Spectrum | DGAF invariant measurement/metric spine | DEFINED; operationalization status is artifact-specific | Canonical expansion is explicitly recorded in `docs/qa/AXIS_METRIC_SPEC.md`; the specification itself states that full operationalization remains a roadmap item. |
| **SACP** | Historical opaque identifier; deprecated from current naming | Historical/project-local term | HISTORICAL / DEPRECATED | No stronger owning expansion has been recovered. Do not backronym; use the concrete capability/mechanism name in current prose. |
| **BFT** | Byzantine Fault Tolerance | Established distributed-systems fault model/property | EXTERNAL STANDARD TERM | PDMAL is not automatically BFT merely because BFT terminology appears nearby. |
| **MDAR** | Monitor–Detect–Assess–Respond | DGAF protocol / response loop | DEFINED | Canonicalized 2026-09-26 after repeated historical candidate usage and no stronger conflicting owner was recovered. |
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
| **FML** | Historical opaque identifier; deprecated from current naming | Historical AHG/Zeta-Pell mitigation terminology | HISTORICAL / DEPRECATED | No recoverable canonical expansion. Current prose must spell out the concrete mechanism instead of using bare FML. |
| **PDM** | **DO NOT ASSUME PDMAL** | Possible project-local abbreviation | AMBIGUOUS | Similar-looking acronyms are not interchangeable. |

## Controlled non-acronym terms and notation

These terms are governed here because they have repeatedly appeared near acronym/brand discussions, but they must **not** be converted into acronyms or silently normalized into one another.

| Token | Classification | Controlled meaning / disposition |
|---|---|---|
| **Orbit** / **Orbit-Driftwatch** | Product / presentation name | Treat as a product/name, not a confirmed acronym. **Observable Multi-Agent Reasoning** is a project tagline, not an O-R-B-I-T expansion. `ORBIT-N1` is a named bounded orchestration pattern. Do not invent a backronym without explicit source authority. |
| **noetic** | External established term | Philosophical/cognitive term relating to mind, intellect, or knowing. Optional analytical lens only; not canonical DGAF state vocabulary. |
| **neotic** | Rare external term | Rare attested term roughly concerning what is addressed to understanding. Do not silently normalize it to `noetic` or reuse it as an emergence-state label. |
| **ontic** | External established term | Concerns what exists or is actually the case. Optional analytical lens; not a substitute for explicit operational predicates. |
| **epistemic** | Canonical DGAF evidence term | Use for justification, support, uncertainty, provenance, and claim status. |
| **neontic** | External specialist term / rejected DGAF coinage | Existing specialist usage includes modern/extant meanings. Do not coin it as a DGAF emergence label; use explicit terms such as `emergent behavior`, `adaptive behavior`, or a defined transition predicate. |
| **pP / Platinum Mean** | Project-defined mathematical notation/name | `pP = 1/(2 sin(pi/11)) ≈ 1.774732842`, the unit-side regular-hendecagon circumradius ratio. This project label does not establish any governance or efficacy property. |
| **ρ / plastic constant** | External standard mathematical constant | Distinct from pP: the real root of `x^3 = x + 1`, approximately `1.3247179572447454`. Never conflate it with Platinum Mean. |

A memorable label, numeric coincidence, project-defined notation, or product tagline does not establish implementation, optimality, causal stability, governance efficacy, or scientific authority.

## Critical acronym controls

### 1. One acronym, one current canonical expansion

An acronym may have historical expansions, but only one should be marked `CANONICAL` for the current ecosystem. Historical variants remain traceable.

### 2. Similar acronyms are not aliases

`PDM`, `PDMA`, `PDMAL`, and `PDMA-L` must not be silently normalized to one another. Use the exact project-defined form.

### 3. Acronym expansion is not evidence

For example:

`PDMAL = Phi-Driven Multi-Agent Lattice`

does not prove any particular convergence, consensus, governance, fault-tolerance, or topology-benefit property.

Likewise, the definition of `PDMAL-D` does not make the successor active or establish that a dodecahedral topology is constitutive or beneficial.

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

### PDMAL / PDMAL-D

Current active identity: **PDMAL = Phi-Driven Multi-Agent Lattice**.

Prospective successor identity: **PDMAL-D = Phi-Dodecahedral Multi-Agent Lattice**.

The 2026-08-31 naming-transition record classifies the PDMAL → PDMAL-D transition as **NOT_TRIGGERED**. Dodecahedral graph quantities may be mathematically verified while the topology remains a candidate experimental factor. No naming preference, visualization, design intuition, single experiment, or historical structural use is sufficient to promote PDMAL-D to active status.

Current documentation must therefore distinguish three things:

1. the active PDMAL identity;
2. verified dodecahedral graph/math quantities within their exact scope; and
3. the untriggered prospective PDMAL-D architectural identity.

### AXIS

Current canonical expansion: **Agent X-axis Invariant Spectrum**. The authoritative source is `docs/qa/AXIS_METRIC_SPEC.md`.

The acronym is reconciled at the vocabulary level. Separate verification is still required for claims about AXIS's operational deployment, scoring validity, or performance.

### PHDGE / Orbit

PHDGE is retained only as **historical / non-canonical ecosystem branding**. Historical generator and Drive-update material may preserve it as event-time provenance, but current-facing authority must not be regenerated from those templates.

Orbit is a **product/name**, not a confirmed acronym. The phrase “Observable Multi-Agent Reasoning” may be retained as a tagline where historically/source-accurate, but it must not be used as an O-R-B-I-T expansion unless a future explicit naming authority establishes one.

### SACP / FML

Both are retained as **historical opaque identifiers**. No stronger owning expansion has been recovered, so neither may be used as an undefined current acronym. Current prose must name the concrete capability/mechanism instead. Historical literal occurrences remain provenance.

### MDAR

Current canonical expansion: **Monitor–Detect–Assess–Respond**. The missing historical `MDAR_PROTOCOL_v1.md` path remains a provenance gap; it does not leave the current acronym undefined.

## Audit rule

Future acronym sweeps must report:

1. acronym token;
2. every materially different expansion found;
3. canonical expansion, if established;
4. source file(s);
5. evidence class;
6. whether the expansion is current, historical, ambiguous, deprecated, or prospective;
7. whether the acronym is being used as an external-standard term or an NDR-local term.

**No acronym is considered reconciled merely because one plausible expansion exists.**


## 2026-09-26 ecosystem acronym-completeness overlay

Current reader-facing ecosystem terminology follows a stronger rule: every acronym must either have a canonical expansion or be explicitly classified as a non-acronym token / historical opaque identifier. Undefined current acronyms are prohibited.

Additional current definitions used across connected ecosystem documentation include:

| Identifier | Expansion / classification |
|---|---|
| **AOSS** | Agent Observation and Safety System |
| **ACP** | Agent Control Plane |
| **AOGA** | Agentic Orchestration and Governance Architecture |
| **GSAE** | Governed Self-Improving Agent Ecosystem |
| **CCB** | Coherence Control Benchmark |
| **MORSE** | Multi-Orbital Resonance Scheduling Experiment |
| **MOLI** | Multi-Orbital Loop Interchange |
| **AIMY** | Agentic Iteration Metaconcert YAML |
| **CSDF** | Cyber Shield Defense Framework (historical DGAF lineage name) |
| **PHDGE** | Phi-Harmonic Dynamic Governance Ecosystem (historical / non-canonical) |
| **AAR** | Action Admission Record |
| **PDP** | Policy Decision Point |
| **PEP** | Policy Enforcement Point |
| **SSoT / SSOT** | Single Source of Truth |
| **RDC** | Remote Desktop Commander |

Identifier-only labels such as **TLE**, **TL3**, **M0**, **E0**, and **R0–R7** must be defined by scope without inventing letter-perfect backronyms.

Machine-readable completeness authority: `docs/taxonomy/ACRONYM_REGISTRY.v1.json`.
Validation entry point: `python scripts/validate_acronym_registry.py`.
