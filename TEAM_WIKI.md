# DGAF Framework — Collaboration and Architecture Guide

> **Status:** Reference guide for collaboration and architectural orientation. For current project status, use [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) and [`docs/PROJECT_STATUS.md`](./docs/PROJECT_STATUS.md). Historical session details are retained in repository history and evidence records.

## Overview

DGAF is a research and implementation framework for governed agent orchestration, evaluation, provenance, and control design. Collaboration is organized around explicit responsibilities, evidence boundaries, and review procedures rather than informal assumptions about authority.

Named agents and components are project architecture abstractions. Their names do not independently grant authority or establish autonomous capability. Current authority boundaries are defined by the [`Agent Authority Matrix`](./docs/agents/AGENT_AUTHORITY_MATRIX.md) and [`Agent Authority Invariant`](./docs/agents/AGENT_AUTHORITY_INVARIANT.md).

## Collaboration model

DGAF work generally separates five concerns:

- **Orchestration:** coordinating tasks and workflow state.
- **Implementation:** developing and maintaining repository artifacts.
- **Evaluation:** testing contracts and examining outputs against defined criteria.
- **Governance:** applying project controls, authority boundaries, and escalation rules.
- **Evidence:** recording what was done and what a result supports.

The same role may contribute to multiple concerns, but a contribution does not automatically constitute approval, verification, or authorization.

## Agent and component references

The repository uses named roles such as Amethyst, COLLEEN, Apogee, DemiJoule, Herald, Professor Prodigy, Sentinel-Phi, and the Resonance agents. These names help organize responsibilities and interfaces.

For the current roster and role contracts, see [`ENSEMBLE_ROSTER.md`](./ENSEMBLE_ROSTER.md). For authority questions, the authority matrix is controlling. Human decision authority remains outside agent-role naming conventions.

## Pattern architecture

DGAF maintains project patterns and control definitions for recurring engineering and governance problems. Pattern identifiers provide a stable way to reference a design; they do not by themselves establish that a pattern is effective in every environment.

Current pattern information is maintained in the relevant pattern registry and specifications. When older terminology appears in historical documents, consult the current terminology and supersession records before treating it as canonical.

## Governance and review

Work affecting controls, evidence, or promotion should identify:

1. the applicable contract or specification;
2. the evidence required for the claim being made;
3. the authority responsible for review or authorization;
4. the provenance needed to reproduce or audit the result.

A passing test, design review, or project-local attestation has the scope defined by its evidence. Broader claims require broader evidence.

## Current work

Do not use this guide as a backlog or live session tracker. Current priorities and experimental boundaries change over time and are maintained in the project's current-state records and active issues/pull requests.

## Historical material

DGAF preserves earlier session records, architecture proposals, terminology, and operational decisions where they are useful for provenance. Historical availability does not make a record a current authority.

See [`docs/HISTORICAL_RECORDS_INDEX.md`](./docs/HISTORICAL_RECORDS_INDEX.md) and [`docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md`](./docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md) for repository-wide handling of historical material.

## Useful entry points

- [`README.md`](./README.md) — public project overview
- [`README.technical.md`](./README.technical.md) — technical reference
- [`README.governance.md`](./README.governance.md) — governance reference
- [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) — current state
- [`docs/PROJECT_STATUS.md`](./docs/PROJECT_STATUS.md) — project status
- [`docs/agents/AGENT_AUTHORITY_MATRIX.md`](./docs/agents/AGENT_AUTHORITY_MATRIX.md) — authority boundaries
- [`docs/HISTORICAL_RECORDS_INDEX.md`](./docs/HISTORICAL_RECORDS_INDEX.md) — historical navigation

---

*This guide explains collaboration and architecture. It does not supersede current technical contracts, evidence records, or project authority controls.*
