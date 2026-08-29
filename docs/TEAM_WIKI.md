# DGAF Collaboration and Architecture Guide

> **Status:** reference guide for project collaboration and historical architecture context.
> **Current authority:** use the repository's current-state, agent-authority, and governance documents for active decisions.

This guide explains how DGAF has organized collaboration, agent roles, and pattern-oriented development. Some terminology and workflow descriptions originated in earlier phases of the project and are retained for context; they do not supersede current repository authorities.

## DGAF today

**DGAF — Dynamic Governance Agentic Formation** is a research and implementation framework for agent orchestration, evaluation, provenance, and governance controls.

The project has evolved through multiple naming and architecture phases. When older records use different expansions or taxonomy, treat those records according to the [Legacy Documentation Status Policy](governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md) rather than silently reinterpreting them.

For the public overview, see [`README.md`](../README.md). For current status, see [`CURRENT_STATE.md`](CURRENT_STATE.md).

## Collaboration model

DGAF uses named agent roles as **architectural and workflow abstractions**. A role may contribute a particular analytical lens, implementation responsibility, or control function, but a role name does not itself create authority or establish autonomous capability.

Current authority boundaries are defined in:

- [`agents/AGENT_AUTHORITY_INVARIANT.md`](agents/AGENT_AUTHORITY_INVARIANT.md)
- [`agents/AGENT_AUTHORITY_MATRIX.md`](agents/AGENT_AUTHORITY_MATRIX.md)
- [`agents/LAYER_0_CONSTITUTION.md`](agents/LAYER_0_CONSTITUTION.md)

Human authority remains explicit where repository controls require approval.

## Role families

The project has used role families including:

| Role family | Typical function |
|---|---|
| Orchestration | task coordination and decomposition |
| Evaluation | quality, coherence, and evidence review |
| Governance and safety | control-boundary and failure review |
| Provenance and observability | trace, audit, and record handling |
| Research and formalism | mathematical, experimental, and specification review |
| Architecture | system and interface design |

Specific agent names and historical assignments should be interpreted through their current contracts. The authoritative agent matrix takes precedence over this overview.

## Pattern-oriented development

DGAF's pattern work is intended to make reusable design decisions easier to identify, compare, and trace. A pattern reference is a design artifact, not evidence that every implementation using the pattern is effective.

When adding or changing a pattern:

1. identify the problem and the scope of the proposed pattern;
2. distinguish an adopted external pattern from a project-specific composition or hypothesis;
3. record provenance and relationships where appropriate;
4. connect implementation and tests to the applicable contract;
5. avoid promoting a pattern to a broader claim without supporting evidence.

See the pattern registry and current Pattern Commons documentation for canonical terminology and cross-repository boundaries.

## Workflow guidance

Use the simplest workflow that fits the task. For substantive changes:

1. identify the current authoritative specification or issue;
2. make the implementation or documentation change;
3. run the applicable validation;
4. record evidence at the correct scope;
5. update current documentation when the change affects project state;
6. preserve historical records rather than rewriting their provenance.

Experimental workflows have additional freeze, authorization, and evidence requirements defined by their protocols.

## Terminology

Terminology evolves. Current canonical definitions are maintained in the repository's terminology, governance, and mathematical-notation policies. Historical glossary entries may remain useful search leads but should not be treated as current authority merely because they appear in an older wiki.

## Related documentation

- [Public project overview](../README.md)
- [Technical reference](../README.technical.md)
- [Governance reference](../README.governance.md)
- [Current project state](CURRENT_STATE.md)
- [Project status](PROJECT_STATUS.md)
- [Agent authority matrix](agents/AGENT_AUTHORITY_MATRIX.md)
- [Legacy documentation status policy](governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md)

---

*This guide is intentionally descriptive rather than a promotion or certification record. For active operational decisions, follow the current authoritative documents.*
