# DGAF Cross-Reference & Epistemic Boundary Index

> **Last reviewed:** 2026-08-29  
> **Purpose:** Canonical cross-reference index for project-local patterns, files, agents, terminology, evidence boundaries, and ecosystem relationships.

## How to use this index

Use this file to answer **where a concept belongs, which record is authoritative, and what relationship is actually established**. It is a cross-reference, not a replacement for technical specifications or evidence records.

## Epistemic policy

This index distinguishes project records from externally validated facts. A registry entry, agent attestation, tier label, owner approval, benchmark label, commercial status, sponsorship, or historical sweep result is not by itself independent scientific validation, certification, legal compliance, or production readiness.

Use the evidence states consistently:

### Evidence state progression

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

Commercialization, legal/trademark status, and epistemic status are independent dimensions.

## Semantic / ontological boundary

DGAF permits agents to consume and reason over an approved ontology. New semantic categories or terminology are candidate vocabulary until provenance and authorization establish canonical status.

Operational records distinguish **representation, classification, policy status, epistemic status, and ontological assertion**. Repetition, confidence, or model wording does not create semantic authority.

The canonical semantic progression is:

### Semantic progression

`defined → observed → supported → verified → authorized → canonical`

Ontology drift is an unauthorized change in effective vocabulary, entity boundaries, relations, or semantic commitments. The broader semantic-risk taxonomy is **definition drift, ontology drift, epistemic drift, policy drift, and provenance drift**.

A semantic/ontological detector is not automatically a gate. Threshold-bearing or blocking use requires empirical characterization, representative traces, adversarial evaluation, error characterization, independence analysis, reproducibility, and demonstrated control value.

## Pattern Commons boundary

**Architecture:** [`docs/PATTERN_COMMONS_ARCHITECTURE.md`](docs/PATTERN_COMMONS_ARCHITECTURE.md)

Pattern Commons is the proposed ecosystem-level layer for pattern identity, provenance, semantic relationships, epistemic status, and cross-repository mapping. DGAF is the implementation/governance substrate and does not automatically own every pattern-bearing artifact in the portfolio.

### Pattern namespaces

- **NDR P-series:** `docs/ndr_patterns_unified.json` is the current machine-readable registry; `docs/NDR_PATTERN_REGISTRY_UNIFIED_P42.md` is the current human-readable P-42 reconciliation companion. `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` remains historical until separately reconciled.
- **DGAF orchestration patterns:** `registry/PATTERN_REGISTRY_v2.md`, including identifiers such as `P-SAGA-001`, `P-TX-001`, and `P-CB-001`.
- **External/cross-listed patterns:** adjacent repositories may contain independent or adapted artifacts. Canonical-source evidence is required before consolidation.

Shared identifiers or terminology do not establish semantic equivalence.

## NDR registry boundary

**Current machine-readable registry:** `docs/ndr_patterns_unified.json`  
**Current human-readable reconciliation:** `docs/NDR_PATTERN_REGISTRY_UNIFIED_P42.md`  
**Historical Markdown snapshot:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
**P-42 pattern card:** `patterns/P-42_AHG.md`  
**Reconciliation:** `docs/governance/NDR_REGISTRY_RECONCILIATION_2026-08-28.md`

The registry reconciliation is a documentation synchronization concern, not evidence of empirical efficacy.

## Research candidates

Epistemic Overreach, Mutual Reference Instability, Semantic Convergence Failure, and Observational Perturbation remain research candidates rather than canonical P-series assignments. A registry decision is required before changing the established P-35–P-42 namespace.

## AHG / P-42 vocabulary boundary

**Canonical expansion:** AHG = Adaptive Harmonic Governance.

Project-defined quantities and architecture terms are not presented as established external control-theory laws without derivation and validation. Names establish project vocabulary; they do not establish external scientific status.

## PDMAL boundary

PDMAL is a separate technical/research track. Shared terms such as φ, convergence, governance, or lattice do not establish that AHG, Zeta-Pell, PDMAL, or related artifacts form one mathematical system. Any bridge must be explicitly specified and independently evidenced.

## Evidence / evaluation boundary

Benchmark names and percentages are not evidence that the named benchmark was run. The authoritative evidence is the corresponding test code plus a reproducible run artifact.

Repository-native deterministic evaluator fixtures may establish mechanism correctness for their exact executed tree. They do not by themselves establish model capability, adversarial robustness, deployment validity, PDMAL efficacy, or generalization.

## Commercialization / openness boundary

See [`docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`](docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md) and the asset-level inventory at `docs/GOVERNANCE/DGAF_ASSET_LEVEL_BOUNDARY_INVENTORY_2026-08-25.md`.

Public reference implementation, specifications, reproducible examples, public tests, research protocols, and non-sensitive Pattern Commons material are default public candidates when needed for reproducibility. Secrets, customer/confidential data, security-sensitive material, and independent commercial operational differentiation may remain non-public. Withheld implementation must not be described as open source.

## Trademark / certification boundary

See [`docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md).

The Apache-2.0 license grants software rights but not trademark rights. No active DGAF certification program is established by the current repository. Official, certified, endorsed, or equivalent claims require separate governance and defined evidence.

## Cross-disciplinary boundary

The ecosystem connects software architecture, agent orchestration, governance, empirical evaluation, mathematical research, observability/reliability, security/privacy, intellectual-property governance, and assurance. A relationship across disciplines does not establish equivalence across them.

Classify relationships as implementation, dependency, adaptation, evidence linkage, analogy, hypothesis, or unresolved.

## Key governance references

| Concern | Canonical reference |
|---|---|
| Current project status | `docs/PROJECT_STATUS.md`, `docs/CURRENT_STATE.md` |
| Public documentation style | `docs/governance/DOCUMENTATION_STYLE_GUIDE.md` |
| Public-surface publication control | `docs/governance/PUBLIC_SURFACE_QA_STANDARD.md` |
| Pattern Commons | `docs/PATTERN_COMMONS_ARCHITECTURE.md` |
| Commercialization/open source | `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md` |
| Trademark/certification | `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md` |
| Evidence policy | `docs/evidence/` |
| NDR registry | `docs/ndr_patterns_unified.json`, `docs/NDR_PATTERN_REGISTRY_UNIFIED_P42.md` |
| Historical NDR registry | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` |
| License | `LICENSE` |
| Funding | `.github/FUNDING.yml` |

## Historical terminology rule

Historical sweep logs, old deadlines, attestation percentages, tier labels, and previous nomenclature remain preserved for provenance. They are not current authority unless a current document explicitly re-establishes them.

- Old deadlines remain historical unless re-established.
- `Ratified`, `A-TIER`, `Gold Star`, and `S-Tier` are project-local labels unless an external standard explicitly says otherwise.
- Exact percentages require a source run, not a copied literal.
- Mathematical vocabulary must describe the implemented operation; metaphorical names must be marked as metaphor.
- A planned component is not active merely because a specification exists.
- Ontological language should describe authorized semantic state rather than converting representation or classification into an assertion about what an entity fundamentally is.

## Current cleanup priorities

1. Reconcile the historical human-readable NDR registry with the P-42 machine-readable registry and current companion.
2. Verify deterministic evaluation-integrity fixture execution on the exact Governance CI tree before promoting #64 beyond IMPLEMENTED.
3. Continue weighted Forman–Ricci falsification under Issue #72; do not promote a single-trial result to validation.
4. Continue file/path classification against the commercialization/openness inventory.
5. Keep architecture/evidence records synchronized with GitHub source changes.
6. Preserve historical evidence while correcting current-state labels.
7. Empirically characterize semantic/ontological detectors before threshold-bearing or blocking use.
8. Keep #117 and #122 open until their implementation/provenance prerequisites are satisfied.
9. Keep public-facing documentation aligned with the repository-wide documentation style and public-surface controls.

*Reviewed 2026-08-29 as part of the repository-wide epistemic, temporal, terminology, semantic, traceability, evaluation-integrity, registry, commercialization-boundary, and public-surface audit.*
