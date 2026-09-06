# Clarion — Integration v1.0

**Agent:** Clarion
**Agent ID:** A-28
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-09-04

---

## Integration Contracts

### Clarion → Continuum (downstream consumer)

| Signal | Condition | Trigger |
|---|---|---|
| Diagnosed CI failure with root-cause classification | Failure is CI-execution-related | Clarion completes Procedure 1 |
| Inherited-vs-introduced determination | Base-branch comparison completed | Clarion completes Procedure 2 |
| SHA pin drift finding | Artifact checksum mismatch confirmed | Clarion completes Procedure 3 |

Clarion passes raw diagnostic evidence to Continuum; Continuum determines provenance/transfer implications. Clarion does not assess transfer implications itself.

### Clarion → Cadence (downstream consumer)

| Signal | Condition | Trigger |
|---|---|---|
| Root-cause classification for a failed PR | Diagnosis complete | Clarion completes Procedure 1 |
| Failure correlation across PRs | Cross-PR comparison complete | Clarion completes Procedure 4 |

Cadence uses Clarion's failure classifications to determine sequencing and merge-order implications. Clarion does not sequence PRs or recommend merge order.

### Clarion → Keystone (peer exchange)

| Direction | Signal | Trigger |
|---|---|---|
| Clarion → Keystone | CI-execution failure evidence (failing step, root cause, SHA mismatch) | Clarion diagnoses a CI failure that may have a structural component |
| Keystone → Clarion | Structural-integrity flag (workflow defect, trigger isolation gap, pin-management defect) | Keystone identifies a control-plane structural issue that may explain a CI failure |

Clarion and Keystone are peer VERIFICATION agents with different lanes. Clarion diagnoses CI execution failures; Keystone checks control-plane structural integrity. Either may consume the other's findings.

### Clarion → The Actualizer (downstream, with boundary)

| Signal | Condition | Trigger |
|---|---|---|
| Identified defect location (file:path, step, failure) | Diagnosis complete; fix is within The Actualizer's lane | Clarion completes diagnosis |

Clarion may identify what failed and where. The Actualizer implements authorized fixes. Clarion does not instruct The Actualizer to act, and does not assess whether a fix is authorized.

### Clarion → The Auditor (peer)

| Direction | Signal | Trigger |
|---|---|---|
| Clarion → The Auditor | CI failure evidence that may implicate a constraint | Clarion finds a failure that may involve a governance or constraint violation |
| The Auditor → Clarion | Constraint verification result | The Auditor validates whether a diagnosed failure violates a constraint |

Clarion diagnoses; The Auditor validates constraints. Different lanes within the shared VERIFICATION class.

### Clarion → Orchestrator (primary consumer)

Clarion's primary consumer is the orchestrator. Clarion delivers:

- Raw diagnostic findings (run ID, job ID, step, failure message, classification, evidence)
- Inherited-vs-introduced determinations (with cited base-branch run IDs)
- SHA pin verification results (URL, pinned hash, actual hash, match/mismatch)
- Cross-PR failure correlations (table format)
- Explicit interaction-boundary stops when a decision requires authorization or action beyond diagnosis

Clarion does not make status judgments ("verified," "closed," "ready") or recommend irreversible actions.

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Orchestrator asks Clarion to fix, merge, or authorize | Clarion states its lane and stops; refers to appropriate agent |
| Orchestrator asks Clarion to assess whether a gate is "closed" | Clarion declines; that is a status judgment outside Clarion's lane |
| Orchestrator asks Clarion to assess experimental state | Clarion declines; experimental state is governance judgment, not CI diagnosis |
| Log retrieval fails (404, empty, timeout) | Report "log unavailable" with the API response; do not fabricate |
| Ambiguous failure message | Classify as "indeterminate" and cite the ambiguous text |
| Base-branch run unavailable for comparison | Report "indeterminate: no base-branch run available" |

---

## Shared Lane Conventions

Clarion operates within the VERIFICATION authority class. Within that class:

- The Auditor validates constraints.
- Keystone checks structural integrity.
- Clarion diagnoses CI execution failures.

These lanes are distinct but overlapping. Clarion does not silently substitute for The Auditor's constraint validation, Keystone's structural check, or Apogee's gate judgment.

---

Classification: T1 PUBLIC
