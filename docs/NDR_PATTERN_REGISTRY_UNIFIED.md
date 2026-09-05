# NDR Pattern Registry (Unified)

**DGAF-Framework · Unified Edition**
**Version:** 2.5 release candidate — reconciliation of human/machine registry identity
**Status:** **CANONICAL NDR FAMILY AUTHORITY**
**Registry release identity:** `NDR-REGISTRY-2026-07-03-P42`
**Effective watermark:** **P-42**
**Release date:** 2026-07-03
**Machine-readable counterpart:** `docs/ndr_patterns_unified.json`
**Cross-family architecture:** `docs/PATTERN_COMMONS_ARCHITECTURE.md`

> This is the canonical human-readable NDR family registry. The machine-readable counterpart and this document are required to share the same release identity. Until the release-validation workflow records a verified source commit/content digest pair for both representations, the release remains a **reconciliation candidate**, not a newly promoted scientific or experimental authority.

## Authority and scope

This registry is authoritative for the **NDR pattern family**. It is not the universal pattern registry for the ecosystem and must not be conflated with:

- `registry/PATTERN_REGISTRY_v2.md` — DGAF orchestration-pattern namespace
- external project pattern registries — retain their own source authority
- `docs/PATTERN_COMMONS_ARCHITECTURE.md` — cross-family identity, relationship, and equivalence model
- evidence, rubric, gate, metric, agent, template, or ecosystem registries — distinct artifact families

## Release metadata

| Field | Value |
|---|---|
| Registry release identity | `NDR-REGISTRY-2026-07-03-P42` |
| Registry watermark | **P-42** |
| Total named P-series patterns | **42** |
| Total NDR named session patterns | 8 |
| Total formation patterns | 2 |
| Stasis block | 133 entries; canonical status recorded by JSON counterpart |
| Machine-readable version | **2.4** |
| Machine-readable watermark | **P-42** |
| Machine-readable last updated | **2026-07-03** |
| Machine-readable session | **S072-colleen-spec-v53.2** |
| Reconciliation state | **CANDIDATE — release identity established; source/digest validation required** |

## Human/machine synchronization rule

The Markdown and JSON representations are two representations of one NDR release, not independent authorities. A valid synchronized release must bind, at minimum:

1. registry release identity;
2. watermark and total pattern count;
3. effective date/session;
4. source commit;
5. schema version for machine-readable data;
6. content digest for each representation;
7. validation result.

The repository consistency check may continue to report a warning while this migration is reconciled, but a warning must not be interpreted as full synchronization or evidence promotion.

## P-series registry

The current machine-readable counterpart records P-01 through P-42. P-42 is:

| Pattern | Name | Layer | Class | Status |
|---|---|---|---|---|
| P-42 | Adaptive Harmonic Governance (AHG) | Layer 12 — Cognitive Control Plane | ADVISORY | SPECIFIED |

P-42 was explicitly renumbered from an earlier P-35 designation because P-35 is already occupied by **Procluding Premise Gate**. Its implementation remains pending; registration does not establish empirical validation.

The remaining P-series definitions are represented in the machine-readable counterpart and historical registry lineage. Where an older Markdown snapshot differs from the machine-readable release, the difference is a release-reconciliation issue rather than permission to silently rewrite history.

## Historical absorption / disposition

The unified registry supersedes or absorbs the historical NDR registry surfaces previously used during the S066/S069 migration:

- `docs/NDR_PATTERN_REGISTRY.md` → redirect/superseded
- `docs/patterns/NDR_PATTERN_REGISTRY.md` → superseded
- `docs/governance/ndr-pattern-registry-v3.md` → deleted/absorbed in the historical migration
- legacy individual NDR pattern cards → archived/absorbed where applicable
- `patterns/ndr_patterns.json` → superseded by `docs/ndr_patterns_unified.json`
- `docs/NDR_REGISTRY_DIFFERENTIATION.md` → historical migration record
- `docs/NDR_REGISTRY_MERGE_PLAN.md` → historical migration record

These records remain useful for provenance. They are not active pattern-number authorities or current work queues.

## Equivalence and cross-family rule

Shared names, terminology, identifiers, or filenames do not establish semantic equivalence. Equivalence requires comparison of definition, mechanism, scope, provenance, claimed function, implementation relationship, evidence, and limitations.

Unresolved relationships should remain explicitly classified, for example as `candidate-alias`, `possible-equivalence`, `cross-reference`, `companion`, or `independent-pattern`.

## Epistemic boundary

Registration in this registry establishes registry identity and provenance only. It does **not** by itself establish:

- scientific validity;
- novelty or priority;
- empirical support;
- runtime efficacy;
- experimental authorization;
- freeze status;
- production readiness.

Those claims require their own evidence and authority chains.

## Current control note

This registry reconciliation is documentation/configuration hygiene. It does not alter DGAF/PDMAL experimental gates, freeze state, authorization, or empirical N.

**Current DGAF scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.

---

*Canonical NDR family registry. Release synchronization remains subject to deterministic validation and provenance binding.*
