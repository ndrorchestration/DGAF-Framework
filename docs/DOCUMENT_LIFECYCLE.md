---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL documentation control
last_verified: 2026-09-22
reconciliation_input_main: 92bc930bdd84f6c4258852e764d3e42019e41342
---

# Documentation Lifecycle Registry

This registry prevents documentation drift by making lifecycle state, authority, temporal meaning, and lineage explicit. It is the preferred place to determine whether a document is current, historical, superseded, a template, a reconciliation artifact, or a derivative.

Because this registry is itself versioned on protected `main`, `reconciliation_input_main` records the Git source baseline used for this revision. Exact current protected-main identity must be read from Git at use time; this file does not maintain a self-referential standing SHA.

## Lifecycle states

- **ACTIVE** — current authoritative document for its stated scope.
- **SUPERSEDED** — retained for history but must not guide implementation or freeze decisions.
- **HISTORICAL** — factual record of a prior state; do not treat as current state.
- **TEMPLATE** — schema or preparation document intended to be populated later.
- **RECONCILIATION** — non-sovereign artifact that compares or integrates multiple source families without silently replacing their authority.
- **DERIVATIVE** — artifact derived from one or more authoritative sources; must identify its sources and cannot outrank them without explicit ratification.

Lifecycle state is independent of file existence. A document can exist, be internally consistent, and still be HISTORICAL, SUPERSEDED, RECONCILIATION, or DERIVATIVE rather than authoritative.

## Temporal fields

Where timing changes interpretation, use these fields explicitly:

- **EVENT_TIME** — when the underlying event or action occurred.
- **RECORD_TIME** — when the event was recorded in the documentation/evidence system.
- **EFFECTIVE_TIME** — when a decision, rule, status, or authority became operative.
- **DISCOVERY_TIME** — when a discrepancy, defect, or previously unknown fact was discovered.
- **RESOLUTION_TIME** — when that discrepancy or defect was resolved or formally disposed.

A later record must not retroactively change the epistemic meaning of an earlier artifact. Historical claims should remain historically attributable even when later reconciliations correct the current state.

## Primary documents

| Document | Lifecycle | Authority | Scope / note |
|---|---|---|---|
| `docs/CURRENT_STATE.md` | ACTIVE | Both | Concise current repository/gate snapshot |
| `docs/PROJECT_STATUS.md` | DERIVATIVE | Both | Compatibility summary; must defer to CURRENT_STATE for live gate truth |
| `docs/ui/UI_CURRENT_STATE.md` | DERIVATIVE | Presentation/documentation | Current UI/interface projection index; must defer to CURRENT_STATE and active controllers for live gate truth |
| `docs/experiment/DOCUMENTATION_GAP_AUDIT.md` | HISTORICAL | Historical audit | Preserves the 2026-08-20 pre-authorization gap audit; not a current gate list |
| `docs/research/AOSS_V0_6_STAGE_A_INDEPENDENT_VALIDATION_HANDOFF.md` | ACTIVE / DERIVATIVE | Audit/control | Accepted external-review handoff; operationally requestable, but does not establish an external review result or independent validation |
| `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | HISTORICAL / SUPERSEDED | Historical control snapshot | Preserves the 2026-09-06 pre-authorization/final-candidate reconstruction state; live state belongs to CURRENT_STATE and active controllers |
| `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | ACTIVE / SPECIFICATION / PRE-FREEZE | Experimental specification | Active exact-scope protocol/workflow contract for legacy PDMAL v0.7.6; not live project-state authority |
| `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` | ACTIVE | Both | Authoritative implementation workload specification |
| `docs/evidence/PDMAL_EVIDENCE_INDEX.md` | ACTIVE / EXACT-SCOPE HISTORICAL INDEX | Evidence lineage | September 6 PDMAL v0.7.6 / #309 evidence map; not live project-state authority |
| `docs/evidence/EVIDENCE_LADDER_POLICY.md` | ACTIVE | Both | Permanent evidence-promotion policy |
| `docs/experiment/FREEZE_MANIFEST_TEMPLATE.md` | TEMPLATE | Both | Becomes `FREEZE_MANIFEST.md` only at freeze |
| `docs/DOCUMENT_LIFECYCLE.md` | ACTIVE | Both | Lifecycle registry itself |
| `docs/governance/DGAF_DOCUMENTATION_ARCHITECTURE_v1.md` | RECONCILIATION | Audit/control | Cross-family integration map; non-authoritative unless separately ratified |
| `docs/governance/AGENT_IDENTITY_RECONCILIATION_2026-09-04.md` | RECONCILIATION | Audit/control | Preserves agent-ID conflicts without replacing sovereign identity authority |
| `docs/governance/instrument_identity_manifest_2026-09-04.json` | RECONCILIATION | Audit/control | Numerical/control instrument identity conflict register; fail-closed pending authority decisions |

## Source-family seed map

Before proposing a new documentation artifact, inspect the existing owner for that concern. Current source families include:

| Concern | Existing seed/source family |
|---|---|
| Documentation lifecycle | `docs/DOCUMENT_LIFECYCLE.md` |
| Documentation gaps/hygiene | `docs/experiment/DOCUMENTATION_GAP_AUDIT.md` plus dated documentation reconciliation/hygiene records |
| Temporal/history | session logs, version histories, dated governance/evidence records |
| Taxonomy | agent/ecosystem registries and identity reconciliation records |
| Pattern library | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` and `docs/ndr_patterns_unified.json` lineage |
| Agent architecture | `docs/AGENT_ARCHITECTURE_ASSESSMENT.md` |
| Agent identity | `docs/agents/AGENT_ROSTER.md` plus conflict-preserving identity controls |
| Formation/topology | `docs/agents/FORMATION_TOPOLOGY.md` |
| Ecosystem registry | `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md` lineage |
| Numerical instruments | QA/AXIS/AHG/agent rubric sources plus the instrument reconciliation manifest |
| Evidence/provenance | evidence indexes, metrics provenance, workflow artifacts, and governance evidence records |
| Transversal assurance | expert-panel reviews, assurance matrices, and transversal audit records |

The detailed cross-family integration model is `docs/governance/DGAF_DOCUMENTATION_ARCHITECTURE_v1.md`; this lifecycle registry classifies authority and temporal use, while that document maps relationships across families.

## Task-specification history

The expert-panel review progressed through v0.7.0/v0.7.1/v0.7.2/v0.7.3 drafts before approving v0.7.4. Separate historical files for those drafts are not present in the current repository; therefore no nonexistent files are marked or invented. The review history is preserved in the governance record and repository commit history.

**Rule:** v0.7.4 is the only task specification authorized for implementation in the current branch unless a later authoritative decision explicitly supersedes it.

## Authority rules

- GitHub source files and CI runs are authoritative for implementation and execution evidence within their exact executed scope.
- Notion records are authoritative for governance decisions, panel adjudication, and control-plane state within their explicit scope and temporal identity.
- Reconciliation artifacts do not acquire sovereignty merely by aggregating multiple sources.
- Historical documents remain useful for provenance but cannot override current active documents.
- A document marked `SUPERSEDED` or `HISTORICAL` must never be cited as the current implementation specification.
- A `RECONCILIATION` artifact must preserve source disagreement instead of silently choosing a winner.
- A `DERIVATIVE` artifact must preserve its upstream identity and may not promote derived claims beyond the evidence/authority of those sources.

## Material-change impact rule

A change touching any of the following requires an explicit impact path:

- identity or identifier;
- taxonomy or status class;
- formula, weight, threshold, or parameterization;
- authority or supersession;
- dependency or implementation binding;
- deployment/runtime identity;
- evidence, artifact provenance, or evidentiary claim;
- experimental protocol, freeze, blinding, authorization, or analysis semantics.

For a material change, identify at minimum:

`affected concepts -> affected documents -> affected layers -> affected tests -> affected evidence -> required re-verification`

If the impact path is unknown, the affected claim remains fail-closed rather than being assumed transferable.

## Anti-duplication rule

Before creating a new artifact:

1. search existing repository and connected governance sources for an existing owner;
2. classify the proposed artifact as ACTIVE/canonical, RECONCILIATION, DERIVATIVE, HISTORICAL, TEMPLATE, or other explicitly bounded role;
3. extend the existing owner when the scope is the same;
4. create a separate artifact only for genuinely distinct scope;
5. preserve source and supersession lineage;
6. reject or reclassify duplicate artifacts that would otherwise claim overlapping authority.

A new document does not become authoritative merely because it is newer.

## Update rule

Every material state change must update the applicable active current-state/evidence records or explicitly document why no propagation is required. Historical records are appended or superseded; they are not rewritten to erase prior evidence.

Documentation reconciliation alone does not create a freeze, authorize a pilot, permit unblinding, or increase empirical N.

**Scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.

## 2026-09-22 — AOSS Stage-A independent-review documentation state

The following current-facing records are **ACTIVE** for the AOSS Stage-A external-review phase:

| Document / controller | Lifecycle | Authority / role |
|---|---|---|
| `docs/CURRENT_STATE.md` | ACTIVE | Primary current-facing repository state summary; must preserve exact evidence/authorization boundaries |
| `docs/research/AOSS_V0_6_STAGE_A_INDEPENDENT_VALIDATION_HANDOFF.md` | ACTIVE | Reviewer-facing handoff contract accepted via PR #928; makes external review operationally requestable but does not itself establish independence or validation |
| GitHub Issue #901 | ACTIVE | Stage-A collection-execution-readiness controller |
| GitHub Issue #929 | ACTIVE | External reviewer engagement and returned-evidence controller |
| GitHub Issue #927 | HISTORICAL / COMPLETED | Handoff-preparation controller; closed after PR #928 acceptance |

The #900–#925 AOSS apparatus records remain authoritative for the exact mechanisms they bind, but they are not substitutes for the accepted #928 external-review handoff or for real reviewer evidence under #929.

Current external-review boundary:

```text
INDEPENDENT_VALIDATION_HANDOFF=ACCEPTED
EXTERNAL_REVIEW=NOT_EXECUTED
reviewer_attribution_verified=false
independence_verified=false
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

This lifecycle update is documentation-only. It does not grant reviewer independence, execution admission, collection readiness, scientific-N promotion, canonical DGAF efficacy, or High-Assurance authorization.
