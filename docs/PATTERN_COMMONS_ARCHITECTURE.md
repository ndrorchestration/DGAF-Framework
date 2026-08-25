# Pattern Commons Architecture

**Status:** Proposed / audit phase  
**Date:** 2026-08-25

## Purpose

Pattern definitions and pattern registries are ecosystem-level knowledge artifacts. They are not inherently owned by DGAF merely because DGAF implements or references them.

The intended architecture is a **federated source model with a normalized governance/index layer**: original repositories retain provenance and implementation context; the Pattern Commons records canonical identity, relationships, and epistemic status without falsely implying that every artifact is one thing.

## Separation of concerns

- **Pattern Commons:** canonical identity, provenance, aliases, semantic equivalence, epistemic status, evidence relationships, and cross-repository mappings.
- **NDR:** a pattern namespace/family within the Pattern Commons; it is not synonymous with the entire ecosystem registry.
- **DGAF:** framework implementation, governance mechanisms, enforcement, evaluation, and references to applicable patterns.
- **Notion:** governance/index layer linking patterns to repositories, claims, decisions, implementations, evidence, and asset-boundary decisions.
- **Commercialization boundary:** determines whether an artifact is open, research, proprietary, private, security-sensitive, or trademark/certification governed; this is independent of epistemic validity.

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

## Current NDR synchronization boundary

The NDR Markdown registry currently declares P-01–P-41 as its canonical P-series watermark, while the machine-readable registry has advanced to P-42. This is a known synchronization discrepancy and must be treated as a **consistency issue**, not resolved by silently choosing whichever artifact is newer.

Until reconciled, no new pattern should rely on an implicit assumption that the two representations are synchronized.

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
- Apache-2.0 [`LICENSE`](../LICENSE)
