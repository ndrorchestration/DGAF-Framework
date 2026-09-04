---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL documentation control
last_verified: 2026-09-04
applies_to_sha: current branch head at update time
---

# Documentation Lifecycle Registry

This registry prevents documentation drift by making lifecycle state, authority, temporal scope, and cross-document lineage explicit. It is the preferred place to determine whether a document is current, historical, superseded, a template, or a reconciliation/control artifact.

## Lifecycle states

- **ACTIVE** — current authoritative document for its stated scope.
- **SUPERSEDED** — retained for history but must not guide implementation or freeze decisions.
- **HISTORICAL** — factual record of a prior state; do not treat as current state.
- **TEMPLATE** — schema or preparation document intended to be populated later.
- **RECONCILIATION** — explicit conflict/index/control document; it does not silently replace the sources it reconciles.
- **DERIVATIVE** — derived from another source and must retain an explicit lineage reference.

## Primary documents

| Document | Lifecycle | Authority | Scope / note |
|---|---|---|---|
| `docs/CURRENT_STATE.md` | ACTIVE | Both | Concise current repository/gate snapshot |
| `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | ACTIVE | Both | Detailed PDMAL operational control record |
| `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | ACTIVE / PRE-FREEZE | Both | Authoritative experimental protocol; remains unfrozen |
| `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` | ACTIVE | Both | Authoritative implementation workload specification |
| `docs/evidence/PDMAL_EVIDENCE_INDEX.md` | ACTIVE | Both | Current evidence-to-control mapping |
| `docs/evidence/EVIDENCE_LADDER_POLICY.md` | ACTIVE | Both | Permanent evidence-promotion policy |
| `docs/experiment/FREEZE_MANIFEST_TEMPLATE.md` | TEMPLATE | Both | Preparation artifact; never infer that a template implies a freeze |
| `docs/experiment/DOCUMENTATION_GAP_AUDIT.md` | HISTORICAL | Both | Dated 2026-08-20 apparatus-era audit; preserve as historical evidence and do not import its old freeze/current-state claims into the 2026-09-04 state |
| `docs/governance/DOCUMENTATION_RECONCILIATION_2026-08-28.md` | HISTORICAL / RECONCILIATION | Both | Dated reconciliation record; useful for lineage, not a current-state substitute |
| `docs/governance/DOCUMENTATION_HYGIENE_RECONCILIATION_2026-09-02.md` | HISTORICAL / RECONCILIATION | Both | Closed hygiene sweep; does not by itself certify current semantic completeness |
| `docs/governance/DGAF_DOCUMENTATION_ARCHITECTURE_v1.md` | RECONCILIATION | Control-plane | Integration map for temporal, taxonomic, pattern, agentic, layered, evidence, and transversal documentation; not a replacement source |
| `docs/DOCUMENT_LIFECYCLE.md` | ACTIVE | Both | Lifecycle registry itself |

## Temporal lineage model

A material record may carry five distinct temporal fields:

`EVENT_TIME` — when the underlying event/fact occurred

`RECORD_TIME` — when the event/fact was documented

`EFFECTIVE_TIME` — when the resulting rule/configuration became operative

`DISCOVERY_TIME` — when a defect/fact was discovered

`RESOLUTION_TIME` — when remediation was completed

A later summary cannot retroactively alter the epistemic meaning of an earlier artifact. Dated historical audits are therefore retained rather than rewritten to match the current state.

## Documentation dimensions

For cross-cutting changes, documentation should be checked across the following existing source families before a new artifact is created:

1. **Temporal / history** — session records, version histories, dated governance records, historical progress analyses.
2. **Taxonomy** — agent, formation, instrument, pattern, state, and registry sources.
3. **Pattern library** — `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` and `docs/ndr_patterns_unified.json` plus their declared release identity.
4. **Agentic architecture** — `docs/AGENT_ARCHITECTURE_ASSESSMENT.md`, `docs/agents/AGENT_ROSTER.md`, `docs/agents/FORMATION_TOPOLOGY.md`, and ecosystem registry lineage.
5. **Layered assurance** — L0 identity/legitimacy through L4 governance integrity, as applicable to the source under review.
6. **Evidence / provenance** — evidence indexes, metric provenance, CI artifacts, execution records, and claim-status records.
7. **Transversal assurance** — audits and reconciliation records that follow a concept across identity → taxonomy → specification → implementation → test → execution → evidence → claim → governance → historical lineage.

## Source-seed rule

DGAF already contains dedicated seeds for timeline/history, taxonomy, pattern libraries, agentic architecture, lifecycle control, evidence/provenance, and transversal review. A proposed new document must first identify the existing source that owns the concept.

Preferred action order:

1. **Extend** the owning source when the concept belongs there.
2. **Reconcile/index** when the change crosses multiple existing sources.
3. **Create a new artifact** only when it has a genuinely distinct scope or lifecycle.
4. **Preserve lineage** whenever a derivative, historical, or superseding artifact is created.

A duplicate document with overlapping authority is a documentation defect, not evidence of completeness.

## Task-specification history

The expert-panel review progressed through v0.7.0/v0.7.1/v0.7.2/v0.7.3 drafts before approving v0.7.4. Separate historical files for those drafts are not present in the current repository; therefore no nonexistent files are marked or invented. The review history is preserved in the governance record and repository commit history.

**Rule:** v0.7.4 is the only task specification authorized for implementation in the current branch.

## Authority rules

- GitHub source files and CI runs are authoritative for implementation and execution evidence.
- Notion records are authoritative for governance decisions, panel adjudication, and control-plane state.
- Historical documents remain useful for provenance but cannot override current active documents.
- A document marked `SUPERSEDED` or `HISTORICAL` must never be cited as the current implementation specification.
- A `RECONCILIATION` document records disagreement or integration state; it does not grant itself authority over the sources it names.
- A `DERIVATIVE` record inherits the epistemic limitations of its upstream source unless independently re-established.

## Material-change impact rule

Any change touching an identifier, formula, threshold, authority, formation, pattern, state machine, dependency, deployment identity, or evidentiary claim should identify:

`affected concepts → affected documents → affected layers → affected tests → affected evidence → required re-verification`

This impact check is especially important when a human-readable label can refer to more than one technical object.

## Update rule

Every material state change must update the active current-state/evidence records. Historical records are appended or superseded; they are not rewritten to erase prior evidence.

## Scientific boundary

Documentation lifecycle controls do not authorize freeze, pilot execution, unblinding, production certification, or empirical claims. At the current control state, the scientific boundary remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0**.
