# CROSS_REF.md

> **Last reviewed:** 2026-08-26  
> **Purpose:** Canonical cross-reference index for project-local patterns, files, agents, terminology, evidence boundaries, and ecosystem relationships.

## Epistemic policy

This index distinguishes project records from externally validated facts. A registry entry, agent attestation, Gold Star/S-Tier label, owner approval, benchmark label, commercial status, sponsorship, or historical sweep result is **not by itself** independent scientific validation, certification, legal compliance, or production readiness.

Use the evidence states consistently:

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

Commercialization, legal/trademark status, and epistemic status are independent dimensions.

## Semantic / ontological boundary

DGAF permits agents to consume and reason over an approved ontology, but agents must not silently introduce, redefine, or assert ontology outside the authorized semantic layer.

Operational records must distinguish **representation, classification, policy status, epistemic status, and ontological assertion**. New semantic categories or terminology are candidate vocabulary until provenance and authorization establish canonical status. Repetition, confidence, or model wording does not create semantic authority.

The canonical semantic progression is:

**defined → observed → supported → verified → authorized → canonical**

**Ontology drift** is a distinct semantic-drift class: an unauthorized change in effective vocabulary, entity boundaries, relations, or semantic commitments. The broader semantic-risk taxonomy is **definition drift, ontology drift, epistemic drift, policy drift, and provenance drift**.

A semantic/ontological detector is not automatically a gate. Threshold-bearing or blocking use requires empirical characterization, including representative traces, adversarial evaluation, error characterization, independence analysis, reproducibility, and demonstrated control value.

## Pattern Commons boundary

**Architecture:** [`docs/PATTERN_COMMONS_ARCHITECTURE.md`](docs/PATTERN_COMMONS_ARCHITECTURE.md)

Pattern Commons is the proposed ecosystem-level layer for pattern identity, provenance, semantic relationships, epistemic status, and cross-repository mapping. DGAF is the implementation/governance substrate and does not automatically own every pattern-bearing artifact in the portfolio.

### Pattern namespaces

- **NDR P-series / named-session patterns:** canonical family currently represented by `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`.
- **DGAF orchestration patterns:** `registry/PATTERN_REGISTRY_v2.md`, using identifiers such as `P-SAGA-001`, `P-TX-001`, `P-CB-001`; this is distinct from the NDR P-series.
- **External/cross-listed patterns:** repositories such as `ai-governance-frameworks`, `ai-prompt-systems-portfolio`, `Amethyst-Governance-Eval-Stack`, `aoga-dashboard`, and `sentinel-governance` may contain independent, adapted, or cross-reference artifacts. Canonical-source evidence is required before consolidation.

Shared identifiers or terminology do not establish semantic equivalence.

## NDR registry boundary

**Canonical Markdown source:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
**Machine-readable counterpart:** `docs/ndr_patterns_unified.json`

Known reconciliation issue: the Markdown registry declares a P-41 watermark while the machine-readable registry has advanced to P-42. This is a synchronization issue until explicitly reconciled; do not silently promote either artifact as the sole current sequence without documenting the discrepancy.

Current canonical P-series represented in the source registry include P-01–P-42, with P-42 AHG specified and implementation status explicitly bounded by evidence.

## P-35–P-38 research candidates

The following concepts are research candidates, not currently assigned canonical P-numbers:

- Epistemic Overreach
- Mutual Reference Instability
- Semantic Convergence Failure
- Observational Perturbation

They must not override the existing P-35–P-42 namespace without an explicit registry decision.

## AHG / P-42 vocabulary boundary

**Canonical expansion:** AHG = Adaptive Harmonic Governance.

Earlier expansions remain historical/deprecated unless a source explicitly identifies them as historical. Project-defined quantities must not be presented as established control-theory laws without derivation and validation.

The P-42 architecture includes project-defined concepts such as Cognitive Phase Energy, Phase Velocity, Phase Acceleration, Productive Divergence, Destabilizing Entropy, Compliance Coefficient, Mission Utility, Recovery Score, Governance Momentum, Hysteresis Band, Sidecar Monitor, Heartbeat, and Cognitive Control Plane. Their names do not by themselves establish external scientific status.

## PDMAL boundary

PDMAL is a separate technical/research track. Do not infer that AHG, Zeta-Pell, PDMAL, or similarly named artifacts form one mathematical system merely because they share terms such as φ, convergence, governance, or lattice. A bridge must be explicitly specified and independently evidenced.

The current audited PDMAL work is bounded to its corrected lattice formalization and associated experimental apparatus/evidence.

## Evidence / evaluation boundary

Benchmark names and percentages must never be used as proof that the named benchmark was actually run. The authoritative evidence is the corresponding test code plus a reproducible run artifact.

A mathematically valid definition does not establish empirical efficacy. A successful implementation test does not establish universal effectiveness. A project attestation is not independent certification.

## Commercialization / openness boundary

See [`docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`](docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md).

**Asset-level inventory:** `docs/GOVERNANCE/DGAF_ASSET_LEVEL_BOUNDARY_INVENTORY_2026-08-25.md`.

Default public candidates include the reference implementation, core specifications/schemas, reproducible examples, public tests, research protocols, and non-sensitive Pattern Commons material.

Legitimate non-public categories include customer/confidential data, secrets, security-sensitive material, and independently developed commercial operational differentiation. Withheld implementation must not be described as “open source,” and commercial status must never be used to obscure unsupported claims.

## Trademark / certification boundary

See [`docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md).

The Apache-2.0 license grants software rights but does not grant trademark rights. No active DGAF certification program is established by the current repository. “Official,” “Certified,” “Endorsed,” or equivalent claims require separate governance and defined evidence.

## Cross-disciplinary boundary

The ecosystem intentionally connects:

- software architecture;
- agent orchestration;
- governance and policy;
- empirical evaluation;
- mathematical research;
- observability/reliability;
- security/privacy;
- intellectual-property/commercial governance;
- certification/assurance.

A relationship across disciplines does not establish equivalence across them. Each relationship should be classified as implementation, dependency, adaptation, evidence linkage, analogy, hypothesis, or unresolved.

## Key governance references

| Concern | Canonical reference |
|---|---|
| Semantic/ontological boundary | `docs/CURRENT_STATE.md`, this index, vocabulary/taxonomy governance |
| Pattern Commons | `docs/PATTERN_COMMONS_ARCHITECTURE.md` |
| Commercialization/open source | `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md` |
| Asset-level boundary inventory | `docs/GOVERNANCE/DGAF_ASSET_LEVEL_BOUNDARY_INVENTORY_2026-08-25.md` |
| Trademark/certification | `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md` |
| Cross-disciplinary boundary | `docs/GOVERNANCE/DGAF_ECOSYSTEM_BOUNDARY_CROSSWALK_2026-08-25.md` |
| Current project status | `docs/PROJECT_STATUS.md`, `docs/CURRENT_STATE.md` |
| Evidence policy | `docs/evidence/` |
| NDR registry | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` |
| Machine-readable NDR registry | `docs/ndr_patterns_unified.json` |
| License | `LICENSE` |
| Funding | `.github/FUNDING.yml` |

## Historical terminology rule

Historical sweep logs, old deadlines, attestation percentages, tier labels, and previous nomenclature remain preserved for provenance. They must not be silently promoted to current state.

- Old deadlines are historical unless a current document re-establishes them.
- “Ratified,” “A-TIER,” “Gold Star,” and “S-Tier” are project-local status labels unless an external standard explicitly says otherwise.
- Exact percentages require a source run, not a copied literal.
- Mathematical vocabulary must describe the implemented operation; metaphorical names must be marked as metaphor.
- A planned component must not be described elsewhere as active merely because a specification exists.
- Ontological language must describe authorized semantic state rather than silently converting representation or classification into an assertion about what an entity fundamentally is.

## Current cleanup priorities

1. Reconcile the NDR Markdown P-41 watermark against the machine-readable P-42 registry.
2. Continue ecosystem-wide pattern provenance/alias analysis before any physical consolidation.
3. Continue file/path-level classification against the commercialization/openness boundary inventory.
4. Keep Notion architecture/evidence records synchronized with GitHub source changes.
5. Preserve historical evidence while correcting current-state labels.
6. Empirically characterize any semantic/ontological detector before promoting it to a threshold-bearing or blocking control.

*Reviewed 2026-08-26 as part of the repository-wide epistemic, temporal, terminology, semantic, traceability, and commercialization-boundary audit.*
