# Continuum — Integration v1.0

**Agent:** Continuum
**Agent ID:** A-29
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-09-04

---

## Integration Contracts

### Clarion → Continuum (primary input)

| Signal | Condition | Trigger |
|---|---|---|
| Diagnosed CI failure with run ID, job ID, and artifact identifiers | Clarion completes Procedure 1 on a CI failure | Clarion reports a CI failure finding |
| SHA pin drift finding | Clarion confirms a checksum mismatch via Procedure 3 | Clarion reports a pin drift finding |

Clarion provides the raw CI-execution evidence (run IDs, job IDs, artifact IDs, failing steps, root-cause classifications). Continuum takes that evidence and assesses its provenance, transfer risk, and evidence-state label. Clarion does not assess provenance; Continuum does not diagnose CI execution failures.

### Continuum → Cadence (downstream consumer)

| Signal | Condition | Trigger |
|---|---|---|
| Provenance assessment for a PR's evidence | Continuum completes Procedure 1 (lineage tracing) or Procedure 2 (anti-transfer scan) on a PR's evidence | Continuum reports a provenance finding |
| Staleness finding for a document or manifest | Continuum completes Procedure 3 on a document or manifest | Continuum reports a staleness finding |
| Evidence-state label for an artifact or assessment | Continuum completes Procedure 4 | Continuum reports an evidence-state label |

Cadence uses Continuum's provenance, staleness, and evidence-state findings to determine whether a reconciliation sequence or merge order preserves evidence integrity. Continuum does not sequence or recommend merge order.

### Continuum → Keystone (peer exchange)

| Direction | Signal | Trigger |
|---|---|---|
| Continuum → Keystone | Evidence-chain break or transfer risk that may have a structural cause | Continuum finds a provenance gap that may stem from a workflow, trigger, or pin-management defect |
| Keystone → Continuum | Structural-integrity flag (defective trigger binding, missing isolation, pin-management gap) | Keystone identifies a control-plane structural issue that may create or exacerbate a provenance risk |

Continuum and Keystone are peer VERIFICATION agents with different scopes. Continuum checks the evidence chain; Keystone checks the control-plane structure. Either may flag an issue that the other should investigate. Neither substitutes for the other.

### Continuum → The Librarian (downstream, archival)

| Signal | Condition | Trigger |
|---|---|---|
| Provenance record for archival | Continuum completes a lineage trace or anti-transfer scan that produces a structured provenance finding | Continuum reports a provenance finding that should be archived |
| Staleness finding for archival | Continuum completes a staleness scan that identifies a stale reference or stale sidecar | Continuum reports a staleness finding that should be archived |

The Librarian archives provenance and staleness records. Continuum produces the findings that The Librarian archives. Continuum does not archive; The Librarian does not assess provenance.

### Continuum → The Actualizer (downstream, with boundary)

| Signal | Condition | Trigger |
|---|---|---|
| Stale sidecar flagged | Continuum completes Procedure 5 and finds a sidecar mismatch | Continuum reports a stale sidecar with expected and actual checksums |
| Stale reference flagged | Continuum completes Procedure 3 and identifies a stale SHA, deployment ID, or other reference | Continuum reports the stale reference with the correct current value (if known) |

The Actualizer may implement authorized fixes for stale sidecars or stale references. Continuum flags the issue; The Actualizer fixes it. Continuum does not instruct The Actualizer to act, and does not assess whether a fix is authorized.

### Continuum → Orchestrator (primary consumer)

Continuum's primary consumer is the orchestrator. Continuum delivers:

- Evidence lineage traces (candidate_sha → workflow_run_id → artifact_id → artifact_digest, with verification at each link)
- Anti-transfer risk findings (identifier, nature of risk, severity)
- Staleness findings (file path, field, stale value, current value if known)
- Evidence-state labels (label applied, supporting evidence, ambiguity flags)
- Sidecar integrity verification (path, expected checksum, actual checksum, match/mismatch)
- Historical-vs-current overlay assessments (whether an overlay is needed, what it should convey)

Continuum does not make status judgments that require gate authority, does not close gates, does not authorize evidence, and does not rewrite historical records.

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Orchestrator asks Continuum to produce or modify evidence | Continuum states it only assesses provenance; refers to the appropriate agent |
| Orchestrator asks Continuum to close a gate or authorize evidence | Continuum states it does not close gates or authorize; refers to Apogee or the appropriate authority |
| Orchestrator asks Continuum to rewrite a historical record | Continuum states it does not rewrite historical records; reports the overlay need as a separate finding |
| Artifact metadata unavailable (run deleted, artifact expired, sidecar missing) | Report "lineage incomplete" with the specific missing element; do not fabricate identifiers or checksums |
| Orchestrator asks Continuum to diagnose a CI failure | Continuum states that is Clarion's lane; refers to Clarion for CI-execution diagnosis |
| Ambiguous identifier (SHA could be candidate, commit, or artifact) | Report the identifier and the ambiguity; do not assume which it is without evidence |

---

## Shared Lane Conventions

Within the VERIFICATION / ARCHIVAL authority class:

- The Auditor validates constraints.
- The Librarian archives provenance and records.
- Continuum assesses evidence lineage, provenance, transfer risk, and staleness.

These lanes are distinct. Continuum does not archive (The Librarian's lane), does not validate constraints (The Auditor's lane), and does not diagnose CI execution failures (Clarion's lane). Continuum may produce findings that inform each of those lanes, but does not substitute for them.

---

Classification: T1 PUBLIC
