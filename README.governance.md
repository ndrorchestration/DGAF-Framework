# DGAF-Framework — Governance & Standards Crosswalk Reference

> **Audience:** auditors, AI risk reviewers, governance practitioners, and technical reviewers  
> **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md)  
> **Technical entry point:** [`README.technical.md`](./README.technical.md)

## Scope and evidence boundary

DGAF is a structured multi-agent governance research and implementation framework. The repository contains governance specifications, selected executable controls, CI gates, authority contracts, evidence/provenance mechanisms, presentation-layer governance projections, and a bounded recurring-assurance catalog.

Mappings to NIST AI RMF, the EU AI Act, ISO/IEC 42001, or OWASP are project-local traceability aids. They are **not** legal-compliance determinations, certifications, conformity assessments, security certifications, or proof that every external requirement is implemented or independently validated.

**Current source boundary:** protected signed/verified `main` is `b1d91621bd73e70866d5ff8fd38fb98e440b30e9` after accepted PR #783.

**Current scientific boundary:** High-Assurance remains **PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0**. Track A Epoch 002 collection is complete at 50 paired seed units / 2,250 blinded observations; dataset lock is established; bounded mapping release/decryption is authorized; materialization tooling is accepted; real materialization and its immutable receipt are not established; primary analysis is not authorized/run; canonical efficacy and independent validation remain not established.

## Governance presentation surfaces

The Governance Command Center contains three accepted presentation-only Semantic Control Field views:

- **Decision Frontier — #776:** current state, evidence/provenance, blocker, nearest admissible transition, unreachable transitions, consequence preview, and receipt semantics.
- **Governance Map — #779:** canonical vertical escalation, explicitly named lateral relationships, and global field conditions.
- **State-Space Explorer V0 — #783:** discrete/categorical reachability derived from canonical stages, with native predicate state separated from derived `established`, `frontier`, and `blocked_by_predecessor` regions.

These views improve inspectability but do not grant authority or create evidence. State-Space V0 explicitly leaves continuous/manifold coordinates, readiness distance, authorization probability, scalar evidence quality, efficacy gradients, consequence values, and reversibility values unestablished.

## Repository assurance inventory

Accepted progression:

1. **PR #780** established `registry/audit_catalog.v1.json` and deterministic validation.
2. **PR #782** added deterministic discovery of workflow definitions not exactly represented by accepted catalog implementation paths.
3. **PR #785** added seven source-verified recurring assurance mappings.

Coverage remains **`PARTIAL_CORE_FAMILIES_ONLY`**.

Interpretation rules:

- cataloged recurring assurance means an accepted current mapping exists for that family/path;
- catalog membership does **not** imply protected-branch requiredness;
- current protected-main required contexts are separately **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**;
- `UNMAPPED` / `UNCLASSIFIED` means current assurance-role adjudication is incomplete, not that the workflow is non-assurance;
- **PR #784** is closed unmerged and its proposed census is not accepted implementation;
- catalog coverage does not establish exhaustive security, governance, scientific, compliance, or audit assurance.

Known gaps include remaining workflow/script/test/method classification, exact job/workflow/ruleset requiredness, shared-dependency/independence analysis, external-runtime ingress assurance, presentation-projection assurance, and historical family-versus-execution-instance reconciliation.

## NIST AI RMF project mapping

NIST AI RMF 1.0 defines four Core functions: **GOVERN, MAP, MEASURE, and MANAGE**.

| Function | DGAF project relation | Evidence boundary |
|---|---|---|
| **GOVERN** | Role/authority definitions, claim/evidence controls, promotion gates, governance projections, assurance inventory | Artifact-specific mapping only; no framework-wide NIST conformance claim. |
| **MAP** | Context/ecosystem mapping, dependency/coupling representation, architecture decomposition | Completeness against all MAP outcomes is not independently established. |
| **MEASURE** | Evaluation gates, structured evidence, recurring-assurance inventory, test and audit artifacts | Passing tests establish only their declared predicates/scopes. |
| **MANAGE** | Fail-closed gates, escalation/authority controls, recovery patterns, risk-response mechanisms | Mechanism existence does not establish risk-reduction efficacy or organizational adoption. |

## EU AI Act conceptual crosswalk

The EU AI Act applies according to regulated role, system classification, use context, and other legal conditions. DGAF has not been assessed here for legal applicability or conformity.

| Provision | Theme | DGAF project relation | Limitation |
|---|---|---|---|
| **Article 9** | Risk management | Project-local gate/risk specifications and iterative review | No legal compliance determination. |
| **Article 12** | Record-keeping/logging | Git history, evidence records, assurance catalog, selected structured logs | Does not establish every Article 12 requirement. |
| **Article 13** | Transparency | Documentation, authority descriptions, state/evidence disclosure | Partial conceptual relation only. |
| **Article 14** | Human oversight | Human authorization/override and fail-closed escalation in selected flows | No conformity assessment. |
| **Article 17** | Quality management | QA/evidence workflows, governance procedures, assurance inventory | Repository artifacts are not asserted to constitute a complete QMS. |
| **Article 72** | Post-market monitoring | Runtime telemetry/audit concepts may inform future processes | No verified Article 72 monitoring system is claimed. |

## OWASP Agentic Top 10 — project crosswalk

DGAF mechanisms may relate to agentic risks such as goal hijack, tool misuse, identity/privilege abuse, supply-chain vulnerabilities, unexpected code execution, memory/context poisoning, insecure inter-agent communication, cascading failures, human-agent trust exploitation, and rogue-agent behavior.

Those relationships are candidate/scoped mitigations. They do not prove that a risk is eliminated or that DGAF has passed an OWASP security certification.

## Audit and provenance surfaces

Complementary trace surfaces include:

1. the machine-readable assurance catalog;
2. the workflow coverage-gap scanner;
3. Git commit/pull-request/workflow history;
4. selected evidence/control-state artifacts;
5. SWEEP/session records where present;
6. `CHANGELOG.md` for selected semantic/project history;
7. Governance Command Center / ORBIT projections for read-only inspection.

For any claim, reconstruct only the chain supported by retained artifacts. Missing links remain **UNKNOWN / NOT VERIFIED / UNCLASSIFIED**, not filled by inference.

## Evidence interpretation rules

- **Mapped**: an artifact has a documented relationship to an external concept/requirement.
- **Implemented**: a relevant mechanism exists in source/configuration.
- **Verified**: a bounded test/check succeeded for its declared identity and scope.
- **Authorized**: a governing record permits the bounded action it names.
- **Executed**: the authorized action actually occurred.
- **Empirically supported**: admissible observations support the exact claim under its controlled protocol.
- **Cataloged recurring assurance**: an accepted assurance mapping exists; this is not branch-protection requiredness.
- **Unmapped / unclassified**: no current assurance-role determination has been accepted.

None of these automatically means legally compliant, certified, secure, safe, effective, deployed, production healthy, independently validated, or High-Assurance authorized.

## Current routing

- [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) — live repository/scientific state;
- [`registry/audit_catalog.v1.json`](./registry/audit_catalog.v1.json) — bounded machine-readable assurance inventory;
- [`README.technical.md`](./README.technical.md) — implementation architecture;
- [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md) — public terminology;
- [`docs/HISTORICAL_RECORDS_INDEX.md`](./docs/HISTORICAL_RECORDS_INDEX.md) — historical/provenance routing.

---

*README.governance · reconciled 2026-09-17 through protected-main `b1d91621…`.*
