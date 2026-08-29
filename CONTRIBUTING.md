# Contributing

DGAF welcomes technically rigorous contributions that improve the implementation, research apparatus, documentation, or reproducibility of the project. The goal is to make changes easy to understand, review, reproduce, and maintain.

> **Governance boundary:** Contribution and CI processes establish engineering evidence; they do not by themselves create an experimental freeze or grant pilot authorization.

## Before you change something

1. Identify the component and its current authoritative documentation.
2. Check `docs/CURRENT_STATE.md` and `CROSS_REF.md` when the change touches status, terminology, patterns, evidence, or cross-repository relationships.
3. Search for an existing implementation, specification, registry entry, or historical record before creating a duplicate.
4. Decide whether the change is implementation, documentation, research, evidence, governance, or maintenance work.

## Development principles

- Keep changes focused and reviewable.
- Prefer explicit contracts and versioned documentation over informal assumptions.
- Preserve historical evidence when it has provenance value; correct current-state references rather than rewriting history.
- Match claims to their evidence boundary. A test result describes what that test established; it does not automatically generalize to the whole repository.
- Avoid introducing new terminology when an existing canonical term already describes the concept.
- When a new term is necessary, define it, identify its scope, and record its relationship to existing vocabulary.

## Documentation quality

Documentation is part of the public engineering surface. Follow [`docs/governance/DOCUMENTATION_STYLE_GUIDE.md`](docs/governance/DOCUMENTATION_STYLE_GUIDE.md) and [`docs/governance/PUBLIC_SURFACE_QA_STANDARD.md`](docs/governance/PUBLIC_SURFACE_QA_STANDARD.md).

In particular:

- Give each document a clear job and audience.
- Lead with the information the reader needs most.
- Prefer concise positive descriptions of what is known over repeated defensive caveats.
- Keep detailed audit and predicate information in evidence/governance records rather than duplicating it across landing pages.
- Label historical and superseded material where readers encounter it.
- Keep dates, branch names, SHAs, issue numbers, and status labels current when a document represents living state.
- Use task-oriented link labels on high-level surfaces.

## Pattern Commons and registry hygiene

Before creating or renaming a pattern:

- search existing definitions, registries, aliases, and cross-listings;
- use `docs/PATTERN_COMMONS_ARCHITECTURE.md` to distinguish NDR, DGAF orchestration patterns, external patterns, and adjacent registry classes;
- avoid duplicate canonical definitions when an existing repository is authoritative;
- record provenance, mechanism, scope, evidence status, and epistemic boundaries;
- treat shared identifiers or terminology as search leads, not proof of semantic equivalence.

## Openness, security, and privacy

Public technical material should be sufficiently complete for independent inspection and reproducibility where practical. Do not publish:

- secrets or credentials;
- customer or confidential data;
- private telemetry or sensitive personal information;
- security-sensitive exploit details before responsible disclosure;
- customer-specific confidential material.

Review changes against `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`. Withheld functionality must not be described as open source.

## Trademark and certification

The Apache-2.0 license does not grant trademark rights. See `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`. Repository access, contributor approval, project attestation, or test execution does not by itself authorize claims of official DGAF endorsement or certification.

## Spec and architecture changes

- Agent-role changes should update the canonical role mapping.
- Pattern changes should identify the relevant Pattern Commons namespace or relationship.
- Contract changes should identify compatibility impact and regression coverage.
- Historical artifacts should remain identifiable as historical/deprecated when provenance requires retention.

## Pull requests

A useful pull request should tell a reviewer:

1. **What changed?** Name the affected component or document.
2. **Why?** State the problem or objective in concrete terms.
3. **What is the boundary?** Identify whether the change affects implementation, evidence, experimentation, terminology, security, commercialization, or another governed surface.
4. **How was it checked?** Provide relevant tests, runs, artifacts, or review evidence and their exact scope.
5. **What did not change?** State important boundaries when the change could reasonably be mistaken for a broader architectural or experimental transition.

Avoid broad claims such as "validated the system" when the evidence establishes only a component, exact tree, or particular execution.
