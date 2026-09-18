# GATE UNIT TEMPLATE — Canonical Practice Unit

<!-- DGAF-Framework canonical gate spec unit template (P-24) -->
<!-- Copy this file to docs/gates/[GATE_ID].md or docs/protocols/[PROTOCOL_ID].md -->
<!-- Remove all HTML comments before committing -->

**Version:** 1.0  
**Maintained by:** `role.governance-orchestrator` (functional contract)  
**Template authority:** `DGAF-Framework/docs/gates/GATE_UNIT_TEMPLATE.md`  
**Pattern:** P-24 (Canonical Practice Unit)  

---

```text
<!-- STATUS HEADER — required on every gate/protocol doc -->
Status:       DRAFT | REVIEW | ACCEPTED_FOR_SCOPE
Reviewed-by-role: role.evidence-verification-reviewer
Review-date:  YYYY-MM-DD
Last-updated: YYYY-MM-DD (Session SXX)
```

---

## [GATE-ID]: Gate / Protocol Name

> One-sentence summary of what this gate enforces and why it exists in the applicable governance loop.
>
> **Authority boundary:** `ACCEPTED_FOR_SCOPE` is an internal governed review state. It does not establish external certification, regulatory compliance, independent validation, production readiness, or scientific efficacy.

---

## Rationale

One paragraph. Answer: **why does this gate exist?** What failure mode does it prevent? What PHDGE property does it protect (harmonic coherence, temporal integrity, sovereignty, IP, evidence quality)? Name the worst-case scenario if this gate were absent.

---

## Trigger Condition

| Field | Value |
|-------|-------|
| **Responsible role** | [functional `role.*` ID from `governance/role_capability_registry.v1.json`] |
| **Event** | [Input received \| Output produced \| State transition \| Cycle boundary \| Session open/close \| Commit issued] |
| **Threshold** | [Numeric: e.g., `phi_ratio < 1.0` \| Symbolic: e.g., `drift_score > 0.80` \| Boolean: e.g., `quorum = false`] |
| **Frequency** | [Every cycle \| Every session \| On-demand \| On BLG detection] |
| **Hard dependency** | [Yes — blocks next gate \| No — advisory] |

---

## Passing State

Describe the condition that constitutes a clean pass. Include a schema example.

```json
{
  "gate": "[GATE-ID]",
  "status": "PASS",
  "role_id": "[responsible role.* id]",
  "phi_ratio": 1.618,
  "score": "≥ threshold",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**Human-readable pass condition:** [Describe in one sentence what a passing artifact looks like.]

---

## Failing State

Describe what a failure looks like. Include a schema example and the immediate consequence.

```json
{
  "gate": "[GATE-ID]",
  "status": "FAIL",
  "role_id": "[responsible role.* id]",
  "reason": "[specific failure condition]",
  "escalation_role": "[role.security-containment-gate | role.governance-orchestrator | human authority]",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**Immediate consequence:** [Block commit \| Escalate to `role.security-containment-gate` \| Route to `role.governance-orchestrator` \| Surface as bounded governance finding]

---

## Recovery Protocol

Step-by-step remediation path from FAIL to PASS.

1. **Identify root cause** — [what diagnostic to run first]
2. **Remediation action** — [what agent takes what action]
3. **Re-test** — [what triggers re-evaluation of the gate]
4. **Escalation if unresolved** — [after N cycles / N minutes, escalate to: _____]
5. **Ionian Lock** — [if applicable: conditions under which the artifact is locked and iteration terminates]

---

## References

| Field | Value |
|-------|-------|
| **MDAR Protocol** | `docs/protocols/MDAR_PROTOCOL_v1.md` |
| **Related Gates** | [GATE-ID, GATE-ID] |
| **Parent Pattern** | [P-XX] |
| **NIST Control** | [e.g., GV-1.1 \| MS-2.5 \| AC-3] |
| **EU AI Act Article** | [e.g., Art. 9 \| Art. 13 \| Art. 17] \| N/A |
| **Supersedes** | [prior version file path or N/A] |

---

## Provenance

| Field | Value |
|-------|-------|
| **Gate ID** | [GATE-ID] |
| **Session** | [SXX] |
| **Date** | YYYY-MM-DD |
| **Author / executor role** | [functional `role.*` ID] |
| **Review role** | `role.evidence-verification-reviewer` |
| **Architect** | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| **Governance spine** | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |

## Functional authority contract

Current authority is resolved from `governance/role_capability_registry.v1.json` and identity/provenance mappings from `governance/persona_role_lineage.v1.json`. Historical persona labels may be recorded as provenance, but no persona label grants authority. The template must use functional role IDs for current ownership, review, escalation, and execution semantics.
