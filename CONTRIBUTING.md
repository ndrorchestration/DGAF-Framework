# Contributing

> **Governance:** DGAF / Agent Amethyst — changes are subject to repository integrity and governance checks before merge. See the public documentation spine and `CROSS_REF.md` for current boundaries.

## Scope

DGAF is the implementation and governance substrate for agent orchestration, evaluation, provenance, and epistemic controls. The broader ecosystem also contains Pattern Commons material, research artifacts, specialized registries, and adjacent repositories. Do not assume an artifact belongs in DGAF merely because DGAF references or implements it.

## Development

- Keep changes small and reviewable.
- Prefer explicit, versioned documentation over informal notes.
- Update `CHANGELOG.md` for every meaningful change following Keep a Changelog conventions.
- Preserve historical evidence; correct current-state labels rather than silently rewriting history.
- Do not introduce absolute validation, performance, safety, certification, or completeness claims without corresponding evidence.

## Pattern Commons and registry hygiene

- Before creating a new pattern, search the ecosystem for existing definitions, registries, aliases, and cross-listings.
- Use `docs/PATTERN_COMMONS_ARCHITECTURE.md` to distinguish NDR, DGAF orchestration patterns, external patterns, and adjacent registry classes.
- Do not create duplicate canonical definitions merely because a pattern is useful to DGAF. Prefer a cross-reference/adapter record when another repository is authoritative.
- Shared identifiers or terminology are not sufficient evidence of semantic equivalence.
- Pattern records should expose provenance, mechanism, scope, evidence status, and epistemic boundaries.

## Openness and commercialization boundary

Changes must be considered against `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md`.

Public by default when needed for reproducibility:
- core reference implementation;
- schemas/specifications;
- public tests and reproducible examples;
- public research protocols and evidence;
- non-sensitive Pattern Commons material.

Do not publish:
- secrets, credentials, customer data, private telemetry, confidential contracts, or sensitive personal information;
- security-sensitive exploit details before responsible disclosure;
- customer-specific confidential material.

Commercial differentiation may legitimately be delivered through services, operations, integrations, hosted infrastructure, specialized tooling, support, training, and future assurance/certification programs. Do not describe withheld functionality as “open source.”

## Trademark and certification boundary

The Apache-2.0 license does not grant trademark rights. See `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`. Repository access, contributor approval, project attestation, or test execution does not by itself authorize claims of official DGAF endorsement or certification.

## Security and privacy

- Never commit secrets or credentials.
- Do not commit customer/private telemetry.
- Route security-sensitive findings through the repository security process.
- Preserve evidence needed to substantiate public claims without exposing protected data.

## Spec changes

- Agent role changes must update the canonical role table in architecture documentation.
- Pattern changes must identify the relevant Pattern Commons namespace/relationship.
- Retired artifacts must be annotated as historical/deprecated rather than silently deleted when provenance matters.

## Pull requests

Explain:
1. which governance or research component is affected;
2. whether the change affects patterns, evidence, taxonomy, experimentation, commercialization, security, or certification boundaries;
3. what evidence supports any changed claim;
4. whether the change creates or resolves a cross-repository relationship.
