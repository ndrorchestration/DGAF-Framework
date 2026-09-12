# Persona-to-Role Architecture Migration Design

**Date:** 2026-09-12  
**Status:** Proposed canonical ecosystem architecture  
**Scope:** DGAF and dependent NDR repositories that encode named personas/agents in active code, configuration, authority mappings, tests, or current-facing documentation.

## 1. Decision

Named agents/personas are no longer primitive architectural units.

Current systems SHALL bind executable behavior and authority to functional **capabilities, roles, policies, contracts, and stable IDs**. A persona may remain as presentation or historical lineage, but it MUST be replaceable without changing the semantics of the underlying role unless its behavior is explicitly modeled as a separate execution profile or policy.

Canonical hierarchy:

```text
Capability
  -> Role Contract
    -> Role Instance / Executor
      -> Optional Persona / Presentation
```

A role may be executed by an LLM, deterministic code, a human, an ensemble, or another implementation.

## 2. Migration classification

Every named-agent reference MUST be classified before modification.

| Class | Treatment |
|---|---|
| Functional dependency | Replace with canonical role/capability ID. |
| Persona/presentation | Move behind an optional presentation mapping. |
| Fixture/demo identity | Replace with a neutral fixture unless identity itself is under test. |
| Historical/provenance identity | Preserve exactly; connect to current role through lineage metadata. |
| Undefined | Do not migrate. Mark for specification/adjudication first. |

No destructive global search-and-replace is permitted.

## 3. Migration invariants

The following MUST remain true throughout migration:

```yaml
migration_invariants:
  historical_actor_identity_is_immutable: true
  historical_alias_resolves_to_current_role: true
  tests_after_migration: ">= tests_before"
  semantic_equivalence: "required_where_expected"
  no_authority_lost: true
  no_authority_gained: true
  role_authority_matrix_equivalence: "proven"
  cross_repo_transition_layer: "required"
  consumer_migration_before_alias_removal: true
  speculative_mapping_for_undefined_roles: "forbidden"
  rollback_plan_required: true
```

Historical evidence MUST retain the actor identity recorded at event time. Current role interpretation is added by immutable lineage mapping; historical records are not rewritten to pretend that later role names existed earlier.

## 4. Role & Capability Registry

The ecosystem SHALL define a versioned Role & Capability Registry.

Minimum role schema:

```yaml
role_id: evidence_integrity_reviewer
schema_version: 1
status: ACTIVE # ACTIVE | PROPOSED | DEPRECATED | HISTORICAL
responsibilities: []
may: []
may_not: []
capabilities: []
execution_constraints:
  independence_required: true
  self_review_allowed: false
historical_aliases: []
presentation:
  persona_required: false
governance:
  owner: null
  approved_by: null
  approved_at: null
  spec_sha: null
provenance:
  created_from: []
  supersedes: []
```

The registry itself MUST carry schema versioning, provenance, review status, and explicit deprecation paths.

## 5. Authority migration

Authority MUST move from named-agent bindings to role bindings only after equivalence is demonstrated.

For each legacy edge:

```text
LegacyActor -> action -> resource -> conditions
```

there MUST be exactly one corresponding role-based edge:

```text
Role -> action -> resource -> conditions
```

unless an intentional authority change is separately reviewed and recorded.

Default acceptance rule:

```text
LegacyPermissions == MigratedPermissions
```

No authority may silently broaden or disappear because of a naming migration.

## 6. Role overlap policy

- **Merge** only when responsibilities, scope, authority, invocation timing, independence constraints, and failure semantics are functionally equivalent.
- **Split** when capabilities overlap but authority, timing, scope, or independence requirements differ.
- **Preserve pending adjudication** when equivalence cannot be demonstrated.

Default: **preserve**, not merge.

## 7. Persona replacement invariant

For presentation-only personas, changing the persona MUST NOT alter role semantics.

If a named persona contains prompts, heuristics, routing rules, memory behavior, or other logic that materially changes output, that behavior MUST be extracted into an explicit architectural object such as:

- `execution_profile`
- `behavior_policy`
- `prompt_strategy`
- `interaction_policy`

It may not remain hidden inside a presentation layer.

## 8. Initial functional decomposition

Historical persona material should be mapped by actual specification/code, not by name. Candidate role families include:

- governance orchestration
- continuity & provenance coordination
- evidence integrity & verification
- security & policy boundary enforcement
- uncertainty/risk escalation
- research & synthesis
- coordination & fairness
- knowledge retrieval & archival
- independent audit/challenge
- artifact execution/materialization
- coherence/signal evaluation
- exploratory/simulation execution
- notification/communication

These are candidate role families, not automatic one-to-one replacements. Undefined or conflicting personas remain unmigrated until specified.

## 9. Historical lineage

Existing agent/persona specifications, registries, experiment records, rubrics, historical formations, and evidence artifacts remain part of the historical design lineage.

Historical directories may be frozen or clearly marked historical, but they MUST NOT be rewritten if doing so would alter evidence identity, hashes, protocol references, signed records, or reproducibility.

## 10. Cross-repository migration order

1. Adopt migration invariants and this canonical architecture.
2. Define registry schema and registry governance.
3. Implement identity-lineage / compatibility mapping.
4. Inventory DGAF named-agent dependencies.
5. Inventory the AI Evaluation Workbench named-agent dependencies.
6. Inventory dependent repositories and integrations.
7. Migrate repositories in dependency order, foundations before consumers.
8. Prove behavior, authority, and historical-resolution equivalence.
9. Freeze historical agent architecture as documented lineage.
10. Retire compatibility aliases only after all active consumers have migrated.

The compatibility window is evidence-based, not calendar-based: aliases remain until all active consumers have migrated and cross-repository equivalence verification passes.

## 11. Validation requirements

Each migration wave MUST demonstrate:

- equal or stronger test coverage;
- no unresolved functional dependency on a persona name;
- deterministic historical alias resolution;
- role-authority equivalence;
- no evidence mutation;
- no governance-state or scientific-state promotion caused by the migration;
- explicit rollback path;
- cross-repository consumer compatibility where applicable.

## 12. Research opportunity

After decomposition, topology, specialization, role separation, executor/model identity, persona presentation, and behavioral prompt profiles can be tested independently.

This creates cleaner experiments because a named-agent bundle no longer changes several independent variables at once.

## 13. Current governance boundary

This architecture migration is documentation and software-architecture work. It does not itself establish scientific evidence, independent verification, freeze, authorization, efficacy, production readiness, or empirical N.

DGAF's live governance/scientific state remains governed by the existing current-state and control records. This design MUST NOT be interpreted as an authorization transition.

## 14. Canonical principle

> Named agents are presentation and historical lineage, not primitive architectural units. Current systems bind behavior and authority to functional roles, capabilities, policies, and contracts. Any retained persona must be replaceable without changing the semantics of the underlying system.
