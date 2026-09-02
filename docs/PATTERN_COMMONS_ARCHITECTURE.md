# Pattern Commons Architecture

**Status:** Proposed / audit phase  
**Date:** 2026-09-02

## Purpose

Pattern definitions and pattern registries are ecosystem-level knowledge artifacts. They are not inherently owned by DGAF merely because DGAF implements or references them.

The intended architecture is a **federated source model with a normalized governance/index layer**: original repositories retain provenance and implementation context; the Pattern Commons records canonical identity, relationships, and epistemic status without falsely implying that every artifact is one thing.

## Separation of concerns

- **Pattern Commons:** canonical identity, provenance, aliases, semantic equivalence, epistemic status, evidence relationships, and cross-repository mappings.
- **NDR:** a pattern namespace/family within the Pattern Commons; it is not synonymous with the entire ecosystem registry.
- **DGAF:** framework implementation, governance mechanisms, enforcement, evaluation, and references to applicable patterns.
- **Notion:** governance/index layer linking patterns to repositories, claims, decisions, implementations, evidence, and asset-boundary decisions.
- **Commercialization boundary:** determines whether an artifact is open, research, proprietary, private, security-sensitive, or trademark/certification governed; this is independent of epistemic validity.

## Semantic authority boundary

Pattern Commons must distinguish **semantic representation from semantic authority**. An agent or repository may consume and reason over an approved ontology or vocabulary, but generated terminology must not silently become canonical.

The governing semantic progression is:

**defined → observed → supported → verified → authorized → canonical**

A pattern record should distinguish, where applicable:

- representation;
- classification;
- policy status;
- epistemic status;
- ontological assertion;
- candidate vocabulary;
- canonical vocabulary.

New terminology or semantic categories are candidate vocabulary until provenance and authorization establish canonical status. Shared terminology, repeated model output, registry membership, or confidence does not establish ontological truth.

**Ontology drift** is a distinct semantic-drift class meaning an unauthorized change in effective vocabulary, entity boundaries, relations, or semantic commitments. It is tracked alongside definition drift, epistemic drift, policy drift, and provenance drift.

Semantic/ontological detection is not inherently a gate. Any detector promoted to threshold-bearing or blocking use requires empirical characterization and evidence of control value.

## Transversal candidate agreement boundary — 2026-09-02

Pattern Commons now treats candidate agreement as a cross-registry consistency property.

The minimum identity tuple for a live experimental candidate is:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

Independent projections are expected to agree across GitHub, Vercel, Notion, evidence registries, taxonomy/vocabulary registries, pattern registries, and public/current documentation.

Agreement classes:

- `ROLE DIFFERENCE` — distinct identifiers with intentionally distinct semantic roles.
- `HISTORICAL DIFFERENCE` — prior identity retained for provenance and explicitly non-closing.
- `TRANSVERSAL DRIFT` — live projections can reasonably be interpreted as different current states.
- `BLOCKING CONTRADICTION` — a discrepancy could permit invalid evidence transfer or a governance transition.

The Pattern Commons must not resolve a disagreement by selecting whichever registry is newer or more convenient. The source-specific role and provenance must be preserved.

## P-35 / P-42 namespace boundary

`P-35` is **Procluding Premise Gate** and `P-42` is **Adaptive Harmonic Governance (AHG)**. The renumbering is canonical and must remain synchronized across pattern documents, cross-reference indexes, and machine-readable registries.

The current P-35 remediation adds an explicit premise-check dependency at the DGAF/TGL/ConsensusTask boundary. Pattern Commons records this as an engineering/wiring dependency. It must not be represented as a PDMAL-specific constitutional premise policy unless that policy is separately approved by experimental-control governance.

## Current synchronization overlay

The existing NDR registry markdown and machine-readable registry have historically moved at different watermarks. The repository therefore uses an explicit reconciliation overlay rather than silently rewriting historical registry state.

Canonical current overlay:

- `docs/NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md`
- `docs/ndr_patterns_unified_transversal_overlay.json`
- `patterns/NDR_TRANSVERSAL_CANDIDATE_AGREEMENT_v1.md`

These artifacts do not replace the historical registry. They establish the current transversal/dependency semantics to be consumed alongside the source-specific registries until a governed registry-version merge is performed.

## Registry family map

The census currently distinguishes at least:

1. **NDR P-series / named-session patterns** — the unified NDR family.
2. **DGAF orchestration patterns** — e.g. `registry/PATTERN_REGISTRY_v2.md`, using IDs such as `P-SAGA-001`, `P-TX-001`, and `P-CB-001`; this is a distinct namespace from NDR P-01–P-42.
3. **External/cross-listed patterns** — patterns housed in other portfolio repositories, where canonical-source evidence determines whether an artifact is an alias, cross-reference, adapter, or independent pattern.
4. **Taxonomy/vocabulary registries.**
5. **Template registries.**
6. **Agent registries.**
7. **Evidence/claim registries.**
8. **Ecosystem/portfolio registries.**
9. **Service/runtime registries.**
10. **Historical/deprecated registries.**

These must not be merged merely because they share the term `registry` or use similar identifiers.

## Equivalence rule

Same identifier, filename, terminology, or repository location is insufficient evidence of pattern equivalence. Equivalence requires comparison of:

- definition;
- mechanism;
- scope;
- provenance;
- claimed function;
- implementation relationship;
- evidence state; and
- known limitations.

Where equivalence is unresolved, retain separate source records and record the relationship as `candidate-alias`, `possible-equivalence`, `cross-reference`, or `independent-pattern` rather than forcing a merge.

## Epistemic rule

Registry membership does not establish truth, novelty, empirical support, completeness, safety, production readiness, or independent verification.

Every canonical pattern record should distinguish at minimum:

`provenance → definition → claim → mechanism → implementation → evidence → replication/independence → scope → limitations → epistemic status`

Recommended epistemic statuses remain:

`observed · candidate · proposed · implemented · empirically supported · independently verified · formalized · deprecated · rejected · unresolved`

## Cross-disciplinary rule

A pattern may participate in multiple disciplines—software architecture, AI evaluation, governance, security, reliability, observability, mathematics, legal/commercial policy, or organizational process—without becoming equivalent across those domains.

Disciplinary applicability must therefore be recorded separately from epistemic validity. A pattern can be:

- technically implemented but empirically unsupported;
- empirically observed but not formally proved;
- legally governed but technically experimental;
- commercially valuable but scientifically unvalidated;
- mathematically well-defined but operationally inert.

This separation prevents business value, nomenclature, or formal appearance from being mistaken for evidence.

## Relationship to commercialization

See [`GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`](GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md).

A pattern's commercial/private/security status is an asset-governance attribute, not a truth claim. Public claims about a commercial or private implementation still require enough evidence to substantiate what is publicly asserted.

See [`GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md) for future official/certification terminology.

## Current NDR candidates

The current audit has identified candidate concepts for the next NDR wave:

- **Epistemic Overreach** — candidate pattern.
- **Mutual Reference Instability** — candidate pattern.
- **Semantic Convergence Failure** — candidate pattern; any Semantic Delta CRDT language remains a proposed design, not an established technology claim.
- **Observational Perturbation** — candidate pattern; replaces the more narrowly phrased “observational inertia” concept pending causal instrumentation experiments.

These remain candidate definitions until formalization and evidence are completed. They must not be silently assigned canonical P-numbers while the existing registry already contains P-35–P-42.

## Migration policy

No existing pattern artifacts should be moved, deleted, or consolidated until provenance, ownership, aliases, semantic equivalence, licensing, and epistemic status have been reconciled.

The dedicated Pattern Commons repository decision remains deferred until the ecosystem census and audit provide sufficient evidence.

## Governance references

- [`GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`](GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md)
- [`GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md)
- [`GOVERNANCE/DGAF_ECOSYSTEM_BOUNDARY_CROSSWALK_2026-08-25.md`](GOVERNANCE/DGAF_ECOSYSTEM_BOUNDARY_CROSSWALK_2026-08-25.md)
- [`CROSS_REF.md`](../CROSS_REF.md)
- [`CURRENT_STATE.md`](CURRENT_STATE.md)
- `../taxonomy/TRANSVERSAL_AGREEMENT_AND_DEPENDENCY_TAXONOMY_2026-09-02.md`
- `NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md`
- Apache-2.0 [`LICENSE`](../LICENSE)
