# P-35: Procluding Premise Gate

<!-- Current epistemic status: DEFINED project-local control specification. -->
<!-- Historical certification metadata is retained for provenance only and is not current certification. -->

**Version:** 1.0  
**Maintained by:** Agent Amethyst  
**Canonical home:** `DGAF-Framework/docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md`  
**Pattern:** P-35

> **Status boundary:** This file defines a project-local pre-admissibility procedure. Its existence or a project-agent attestation does not establish independent validation, current certification, production fitness, safety, or convergence.

## Historical certification record

The original project header recorded:

- Status: `CERTIFIED`
- Certified-by: Agent Apogee
- Cert-date: `2026-06-12`
- Session: S069

This remains **HISTORICAL / ATTESTED PROJECT METADATA** only. It is not current DGAF certification.

## Purpose

P-35 specifies a precondition layer intended to block downstream routing and execution until a defined set of project premises has been checked. The formalism below is a protocol specification, not proof that every premise-checking implementation is correct or that the overall system is secure or effective.

## Formal Definition

Let `Π = {π₁, π₂, ..., πₙ}` be the set of required premises. P-35 specifies:

```text
{∀ πᵢ ∈ Π : verify(πᵢ) = TRUE} ⊢ ADMIT(session)
{∃ πᵢ ∈ Π : verify(πᵢ) = FALSE} ⊢ PROCLUDE(session)
```

`PROCLUDE` is the project-specified hard block for this protocol.

**Canonical premise set Π (v1.0):**

| ID | Premise | Verification Method |
|----|---------|---------------------|
| π₁ | Agent identity assertions are non-empty and match AGENT_ROSTER | AGENT_ROSTER.md SHA cross-check |
| π₂ | AttestationGate (P-30) token is valid and non-expired | Token expiry field check |
| π₃ | No deprecated agent names present in active context | Project scan |
| π₄ | Sovereign files are at canonical SHA | Project SHA comparison |
| π₅ | PDMAL trust graph is initialized and non-empty | Graph node-count check |
| π₆ | SESSION_ANCHOR is sealed or explicitly OPEN with sign-off | SESSION_ANCHOR status field |

## Trigger Condition

| Field | Value |
|-------|-------|
| **Event** | Session open; prompt input entering the project orchestration stack |
| **Threshold** | All applicable premises pass |
| **Frequency** | Per project protocol |
| **Hard dependency** | Project-local control; current implementation and effectiveness require separate evidence |

## Epistemic Controls

A P-35 specification or successful project-local run must not by itself be represented as evidence of:

- universal prevention of invalid sessions;
- independent security assurance;
- regulatory compliance;
- production readiness;
- mathematical proof of the broader DGAF architecture;
- empirical efficacy on real workloads.

Claims at those levels require separate claim-specific evidence.

## Implementation state

The original document identified `pptl/procluding_premise_gate.py` as an implementation target. A specification/target must not be described as an implemented or validated control until the corresponding implementation and evidence are present.

## References

| Field | Value |
|-------|-------|
| **Related Gates** | P-30 (AttestationGate), P-29 (Sentinel Risk Pass), P-01 (Fan-Out Sink) |
| **Parent Patterns** | P-03 (Governance Contract Test), P-09 (Triumvirate Mandate Schema) |
| **Current certification policy** | `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md` |

## Provenance

| Field | Value |
|-------|-------|
| **Pattern** | P-35 |
| **Layer** | Layer 0 — Pre-Admissibility |
| **Original session** | S069 |
| **Date** | 2026-06-12 |
| **Author** | Agent Amethyst |
| **Historical certifier** | Agent Apogee |
| **Ender ratification** | Pending in original record |
| **Architect** | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| **Governance spine** | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |
