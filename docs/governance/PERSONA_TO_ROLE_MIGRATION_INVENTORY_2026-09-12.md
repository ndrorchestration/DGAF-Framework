# Persona-to-Role Migration Inventory — 2026-09-12

**Status:** Initial ecosystem inventory / documentation control  
**Canonical design:** `docs/superpowers/specs/2026-09-12-persona-to-role-architecture-migration-design.md`  
**Rule:** inventory first; classify before modification; no destructive global rename.

## Purpose

Track named-agent/persona dependencies that must be decomposed into functional roles, capabilities, policies, contracts, execution profiles, presentation aliases, or historical lineage.

This inventory is intentionally conservative. A reference is not automatically a migration target merely because it contains a persona name.

## Classification codes

- `FD` — functional dependency
- `PP` — persona/presentation
- `FX` — fixture/demo identity
- `HP` — historical/provenance identity
- `UN` — undefined/conflicting; specification required before migration

## Confirmed foundation surfaces

### `ndrorchestration/DGAF-Framework`

**Priority:** P0 foundation

Observed current structures include:

- `registry/agent_identity_manifest.v1.json`
- `docs/agents/AGENT_AUTHORITY_MATRIX.md`
- `docs/agents/FORMATION_TOPOLOGY.md`
- `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md`
- `docs/VOCABULARY_TRANSLATION_MATRIX.json`
- `app/lib/public-translation.ts`
- `scripts/validate_vocabulary_translation_matrix.py`
- historical/current agent specification directories under `docs/agents/**`

Representative named identities include Amethyst, COLLEEN, Sentinel/Sentinel-Phi, DemiJoule, Reciprocity, Prodigy, Perigee, Nova, Herald, Reson, Librarian, Auditor, Actualizer, Ionia, and others in the historical taxonomy.

**Initial classification:** mixed `FD + PP + HP + UN`.

**Required outcome:**

1. derive role/capability contracts from actual specifications and executable dependencies;
2. create role registry + lineage mapping;
3. prove named-actor authority matrix equivalence against role-based authority matrix;
4. preserve historical files/evidence unchanged where identity is event-time provenance;
5. leave undefined/conflicting roles unmigrated until adjudicated.

### `ndrorchestration/junior-apogee-app` — current product working identity: AI Evaluation Workbench

**Priority:** P1 consumer / evaluation product

Current `main` after naming-boundary migration still contains an active `AgentName` enum and named role members including Prodigy, Reciprocity, COLLEEN, and DemiJoule, plus a compatibility-only former primary member now serialized/displayed as `Evaluation Orchestrator`.

Affected surfaces include:

- `src/junior_apogee/models.py`
- `src/junior_apogee/agents/profiles.py`
- `src/junior_apogee/evaluation/engine.py`
- `src/junior_apogee/governance/checker.py`
- `src/junior_apogee/metrics/aggregator.py`
- `app.py`
- `scripts/generate_report.py`
- demo data and test fixtures
- unit/integration tests that assert `AgentName` semantics

**Initial classification:** predominantly `FD + FX`, with compatibility/history `HP` for retired identifiers.

**Required outcome:** replace identity-keyed evaluation behavior with explicit role/capability/execution-profile contracts while preserving test semantics and backwards compatibility.

### `ndrorchestration/ndrorchestration`

**Priority:** P1 documentation / public ecosystem surface

Observed current/historical surfaces include:

- `docs/agent-amethyst-instantiation.md`
- `docs/agent-colleen-instantiation.md`
- `docs/agent-reciprocity-instantiation.md`
- `docs/agent-roster.md`
- `docs/agent-activation-order.md`
- `docs/vocabulary-taxonomy.md`
- classification and bridge documents referencing named agents

**Initial classification:** mixed `PP + HP`, with some potentially current functional workflow descriptions requiring `FD` review.

**Required outcome:** preserve historical instantiation documents as lineage; update current-facing ecosystem architecture and workflow descriptions to role/capability terminology once canonical registry IDs exist.

## Additional ecosystem surfaces requiring inventory

The following repositories/surfaces are known or strongly indicated by prior cross-repository documentation and must be checked before compatibility aliases are retired:

- `agent-control-plane`
- `sentinel-governance`
- `ai-governance-frameworks`
- `ai-prompt-systems-portfolio`
- `Amethyst-Governance-Eval-Stack`
- `resumeapex-eval`
- `Driftwatch` / `Orbit-Driftwatch`
- `Morse-Orchestration`
- research/prototype repositories that import or copy DGAF agent vocabularies

Presence in this list means **inventory required**, not that a migration is already justified.

## Migration order

1. DGAF registry schema + lineage + authority equivalence.
2. DGAF current-facing translation/validation consumers.
3. AI Evaluation Workbench identity-keyed runtime/test structures.
4. Public/profile documentation surfaces.
5. Dependent governance/evaluation/control-plane repositories.
6. Remaining research/prototype consumers.
7. Cross-repo verification and compatibility-alias retirement.

## Acceptance checklist per repository

- [ ] named references inventoried
- [ ] every reference classified `FD`, `PP`, `FX`, `HP`, or `UN`
- [ ] undefined/conflicting roles adjudicated before migration
- [ ] role/capability replacement specified from actual behavior/spec
- [ ] historical evidence left immutable
- [ ] persona-only aliases proven semantically replaceable
- [ ] behavior-changing persona content extracted to explicit execution/policy objects
- [ ] authority equivalence proven where authority exists
- [ ] tests equal or stronger
- [ ] compatibility layer present for active consumers
- [ ] rollback path documented
- [ ] cross-repo consumer verification complete

## Non-effect boundary

Inventory or migration completion does not promote governance state, scientific evidence, authorization, production readiness, efficacy, compliance, safety, or empirical N.
