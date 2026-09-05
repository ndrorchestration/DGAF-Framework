# Pattern Commons Architecture

**Status:** Accepted architectural boundary / active reconciliation layer  
**Date:** 2026-09-04

## Purpose

Pattern definitions and pattern registries are ecosystem-level knowledge artifacts. They are not inherently owned by DGAF merely because DGAF implements or references them.

The architecture is a **federated source model with a normalized governance/index layer**: original repositories retain provenance and implementation context; Pattern Commons records canonical identity, relationships, and epistemic status without falsely implying that every artifact is one thing.

## Separation of concerns

- **Pattern Commons:** cross-family identity, provenance, aliases, semantic-equivalence relationships, epistemic status, evidence relationships, and cross-repository mappings.
- **NDR:** one pattern namespace/family within Pattern Commons. Its canonical family authority is `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`.
- **DGAF:** framework implementation, governance mechanisms, enforcement, evaluation, and references to applicable patterns. Its orchestration-pattern namespace remains `registry/PATTERN_REGISTRY_v2.md`.
- **Notion:** governance/index layer linking patterns to repositories, claims, decisions, implementations, evidence, and asset-boundary decisions.
- **Commercialization boundary:** determines whether an artifact is open, research, proprietary, private, security-sensitive, or trademark/certification governed; this is independent of epistemic validity.

## Authority rule

There is **no universal pattern registry**. Authority is scoped by family and artifact type:

| Artifact family | Authority |
|---|---|
| NDR patterns | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` + `docs/ndr_patterns_unified.json` as one release pair |
| DGAF orchestration patterns | `registry/PATTERN_REGISTRY_v2.md` |
| External patterns | Their originating repository/source |
| Cross-family identity/relationship | Pattern Commons architecture/index layer |
| Templates | Owning template registry |
| Agents | Owning agent registry |
| Evidence/claims | Owning evidence/claim registry |

A registry name, filename, identifier, or cross-reference does not override this authority model.

## Semantic authority boundary

Pattern Commons must distinguish **semantic representation from semantic authority**. An agent or repository may consume and reason over an approved ontology or vocabulary, but generated terminology must not silently become canonical.

The governing semantic progression is:

**defined → observed → supported → verified → authorized → canonical**

New terminology or semantic categories are candidate vocabulary until provenance and authorization establish canonical status. Shared terminology, repeated model output, registry membership, or confidence does not establish ontological truth.

## Registry family map

The census distinguishes:

1. **NDR P-series / named-session patterns** — unified NDR family.
2. **DGAF orchestration patterns** — distinct namespace using IDs such as `P-SAGA-001`, `P-TX-001`, and `P-CB-001`.
3. **External/cross-listed patterns** — canonical source remains external unless explicitly transferred.
4. **Taxonomy/vocabulary registries.**
5. **Template registries.**
6. **Agent registries.**
7. **Evidence/claim registries.**
8. **Ecosystem/portfolio registries.**
9. **Service/runtime registries.**
10. **Historical/deprecated registries.**

These must not be merged merely because they share the term `registry` or use similar identifiers.

## NDR release synchronization

The NDR human-readable and machine-readable registries now target the same release identity:

`NDR-REGISTRY-2026-07-03-P42`

The machine-readable counterpart records P-42 and version 2.4. The human-readable registry has been reconciled to that P-42 watermark. Deterministic validation remains required for the release to be considered fully synchronized at the provenance/digest level.

The synchronization check therefore has two distinct outcomes:

- **content identity:** watermark/count/version/date agree;
- **provenance identity:** source commit and content digests are bound and validated.

A content match does not by itself prove provenance identity.

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

## Historical artifacts

The former NDR differentiation and merge-plan documents are historical migration records. They remain useful for provenance but are not current authorities or task queues. Legacy registries and cards are similarly historical/superseded where the unified NDR registry explicitly records their disposition.

Historical artifacts must not be deleted solely to make the repository appear less redundant when deletion would destroy useful provenance.

## Epistemic rule

Registry membership does not establish truth, novelty, empirical support, completeness, safety, production readiness, or independent verification.

A canonical pattern record should distinguish at minimum:

`provenance → definition → claim → mechanism → implementation → evidence → replication/independence → scope → limitations → epistemic status`

## Anti-sprawl rule

Do not create another registry merely because an existing registry is difficult to navigate. Extend the owning authority, add a reconciliation/index record when scope crosses boundaries, or create a genuinely distinct artifact family only when its authority, lifecycle, and evidence boundary differ materially.

This is a documentation architecture rule and does not change DGAF/PDMAL experimental status.

**Current DGAF scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
