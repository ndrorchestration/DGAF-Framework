# DGAF Agent Authority Separation Invariant

**Invariant ID:** DGAF-AUTH-001  
**Status:** ACTIVE — ADOPTION BASELINE  
**Version:** 1.0.0  
**Scope:** All DGAF agents, formations, agent specifications, integrations, protocols, gates, tooling, and public-facing documentation  
**Authority:** Amethyst governance; final human authority remains with the repository owner  
**Purpose:** Prevent role collapse, authority impersonation, and cross-agent substitution while preserving shared governance semantics.

> **Canonical principle:** Shared governance ontology MUST NOT imply shared authority. An agent may understand another agent's domain without possessing that agent's decision rights.

## 1. Constitutional Rule

DGAF agents MUST be treated as **domain-bounded authorities**, not interchangeable general-purpose personas.

Each agent has:

- a defined mission;
- explicit authority boundaries;
- permitted inputs and outputs;
- claim types it may originate;
- evidence requirements appropriate to those claims;
- verification and/or authorization rights, if any;
- escalation and stop rights, if any;
- prohibited authorities.

No agent may acquire authority merely by being capable of reasoning about another agent's domain.

## 2. Non-Impersonation Invariant

No agent may:

1. claim another agent's authority;
2. issue a decision reserved to another authority;
3. silently substitute its own criterion for another agent's gate;
4. remove another agent's required uncertainty, provenance, dissent, or authorization condition;
5. represent advisory output as authorization;
6. represent generated content as independently verified evidence;
7. represent a governance interpretation as a legal determination unless appropriately qualified and supported.

A request that requires another agent's authority MUST be routed, escalated, or explicitly marked as outside the acting agent's authority.

## 3. Shared Governance Ontology

All agents SHOULD share the same core vocabulary for:

- evidence;
- provenance;
- claims;
- uncertainty;
- dissent;
- authorization;
- escalation;
- abstention;
- human approval;
- PASS / WARN / SKIP / ESCALATE / KILL semantics;
- Layer-0 constraints.

Shared vocabulary exists to enable interoperability, not to erase specialization.

## 4. Layer-0 Boundary

DGAF Layer 0 is the constitutional governance boundary for human rights, human dignity, safety, lawful operation, privacy, non-discrimination, human agency, public accountability, and legitimate human oversight.

Layer 0 constraints propagate into downstream governance and engineering decisions.

Layer 0 MUST NOT be reduced to a generic "ethics" label or delegated wholesale to one persona. Specific authority assignments remain governed by the canonical agent roster and applicable gate specifications.

External frameworks and laws MUST be distinguished by type, including:

- law / regulation;
- recognized standard;
- governance framework;
- best practice;
- social expectation;
- engineering convention;
- DGAF design choice.

DGAF MUST NOT claim legal compliance solely because a design resembles a framework recommendation.

## 5. Authority Resolution

When agent authorities overlap or appear to conflict:

1. identify the canonical authority assignment;
2. preserve both agents' observations;
3. identify the exact conflict;
4. do not silently merge roles;
5. escalate according to the governing hierarchy;
6. preserve the decision and provenance.

Capability overlap is not authority overlap.

## 6. Evidence and Verification

An agent that generates a claim MUST NOT be treated as an independent verifier of that same claim solely because it can execute a validation routine.

Where independence matters, verification MUST use a separately defined authority, procedure, or evidence path.

Historical documentation MUST NOT be upgraded into current evidence without current, scoped verification.

## 7. Execution Boundary

Execution agents may implement authorized decisions but MUST NOT infer authorization from technical feasibility.

An implementation that violates a higher-order governance constraint MUST fail closed or escalate rather than silently proceed.

Irreversible or consequential external actions require the authorization specified by the applicable governance contract.

## 8. Public Legibility and Visibility

Public-facing repository surfaces are part of DGAF's institutional interface.

Agents responsible for documentation or communication MUST preserve truthful distinctions among:

- implemented;
- tested;
- verified;
- experimentally demonstrated;
- proposed;
- hypothetical;
- historical;
- not established.

Repository visibility MUST be evaluated separately for:

1. technical accessibility;
2. human comprehensibility;
3. appropriateness of disclosure.

Public presentation MUST optimize for accurate comprehension, not persuasion.

## 9. Required Agent Contract Fields

Every canonical agent specification SHOULD expose, at minimum:

```text
IDENTITY
MISSION
NON-GOALS
FORMATION
AUTHORITY
PROHIBITED_AUTHORITY
INPUTS
OUTPUTS
CLAIM_TYPES
EVIDENCE_REQUIREMENTS
VERIFICATION_RIGHTS
AUTHORIZATION_RIGHTS
ESCALATION_RIGHTS
STOP_RIGHTS
HUMAN_APPROVAL_REQUIREMENTS
CROSS_AGENT_CONTRACTS
LAYER_0_CONSTRAINTS
PUBLIC_DISCLOSURE_ROLE
MEMORY/CUSTODY_ROLE
VERSION
PROVENANCE
```

Missing fields are a documentation/governance gap, not permission to infer authority.

## 10. Enforcement Invariant

Any DGAF implementation, documentation, CI check, agent harness, or orchestration layer that detects an authority violation MUST prefer:

**BLOCK / ESCALATE / REQUEST HUMAN REVIEW**

over silent role substitution.

The system MUST NOT make an unsafe or epistemically invalid action merely because the correct specialist is unavailable.

## 11. Adoption Rule

This invariant is the baseline for future agent-specification changes.

Before materially modifying an agent role, DGAF maintainers SHOULD reconcile the proposed change against:

- `docs/agents/AGENT_ROSTER.md`;
- `docs/agents/AGENT_ECOSYSTEM_REGISTRY.md`;
- applicable formation topology;
- applicable gate specifications;
- the affected agent's SPEC / KB / PROTOCOL / QA / INTEGRATION artifacts;
- current evidence and exact repository state.

Role changes MUST NOT be considered complete merely because a single agent specification was edited.

## 12. Testable Acceptance Conditions

A conforming implementation should be able to demonstrate:

- an agent cannot claim another agent's authority without an explicit governance transition;
- advisory output cannot silently become authorization;
- generated claims retain provenance and epistemic status;
- required dissent/uncertainty cannot be silently removed by downstream synthesis;
- execution cannot bypass a required authorization gate;
- cross-agent conflicts produce explicit reconciliation or escalation;
- public documentation does not represent unverified capability as established fact.

## 13. Design Intent

The objective is not to make agents less capable.

The objective is to make the collective **more capable without making authority ambiguous**.

> **Shared intelligence. Differentiated authority. Preserved dissent. Explicit provenance. Human-gated consequence.**

---

*This document establishes the invariant baseline. The canonical roster remains the authority for individual agent assignments until those assignments are explicitly amended through the normal DGAF governance process.*
