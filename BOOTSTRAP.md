# DGAF Workspace Bootstrap

> **Audience:** maintainers and contributors starting a project work session.
> **Scope:** project-local operating guidance. For public project orientation, start with [`README.md`](README.md).

This document provides a lightweight starting sequence for working inside the DGAF repository. It is an operating aid, not a statement of external certification, compliance, or system capability.

## Start here

Before making a substantive change:

1. Check [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) for the current authoritative project state.
2. Review the files and specifications relevant to the task rather than loading unrelated historical material.
3. Check [`CHANGELOG.md`](CHANGELOG.md) and applicable open issues or pull requests when recent changes matter.
4. Classify new claims and results according to the repository's evidence policy before presenting them as established.

For a research or experimental task, follow the applicable protocol and governance record; this bootstrap does not override candidate, freeze, authorization, or evidence boundaries.

## Repository orientation

| Need | Starting point |
|---|---|
| Public project overview | [`README.md`](README.md) |
| Current project state | [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) |
| Project status and evidence boundary | [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) |
| Technical architecture | [`README.technical.md`](README.technical.md) |
| Governance model | [`README.governance.md`](README.governance.md) |
| Agent authority | [`docs/agents/AGENT_AUTHORITY_MATRIX.md`](docs/agents/AGENT_AUTHORITY_MATRIX.md) |
| Experimental work | [`docs/experiment/`](docs/experiment/) |
| Evidence policy | [`docs/evidence/EVIDENCE_LADDER_POLICY.md`](docs/evidence/EVIDENCE_LADDER_POLICY.md) |
| Historical material | [`docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md`](docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md) |

## Working principles

- **Use the current authority for the question at hand.** Do not infer current state from an older summary when a living record exists.
- **Separate instruction from evidence.** A project workflow may direct an action without establishing that a resulting claim has been verified.
- **Keep authority explicit.** Project agent roles and automation components operate under repository-defined contracts; they are not independent authorities.
- **Preserve provenance.** Do not silently rewrite historical claims or results to make them appear current.
- **Scope results correctly.** Tests and evaluations establish only the behavior and evidence boundary they actually cover.
- **Use human approval where the applicable control requires it.**

## Evidence vocabulary

The repository uses explicit epistemic classifications. Consult the evidence policy for authoritative definitions and promotion rules. In particular, implementation, a passing test, an attestation, and a demonstrated real-world result are different kinds of evidence.

## Session hygiene

For changes that materially affect repository behavior, governance, experiment design, or public claims:

- update the appropriate authoritative documentation;
- add or update tests when behavior changes;
- preserve links between evidence and the artifact or execution that produced it;
- avoid promoting historical evidence to current verification without an explicit basis;
- review the public surface when a change affects reader-facing material.

## Historical workspace records

Older session anchors, orchestration queues, sweep logs, and agent-role records remain part of the repository's history. They may be useful for provenance or recovery, but should not automatically be treated as current operating authority. See the [Legacy Documentation Status Policy](docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md).
