# DGAF v1 Agent-Role Mapping

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Vocabulary authority:** `docs/VOCABULARY_TRANSLATION_MATRIX.json`  
**Scientific-state effect:** NONE

This document maps generic v1 control-plane execution roles to existing DGAF agent identities without changing the agents' normative authority.

## Identity / role / translation boundary

Three concepts must remain separate:

- **canonical identity** — project-local agent identity such as `Amethyst`, `Apogee`, `DemiJoule`, or `Sentinel-Phi`;
- **generic or archetypal role** — execution contract such as `VERIFY`, `GOVERN`, `TRIBUNAL`, or `SENTINEL_ARCHETYPE`;
- **external functional label** — public-facing translation such as `Governance Orchestrator` or `Runtime Safety & Constraint Adviser`.

A role assignment does not create an identity, a public label does not create authority, and an alias does not create a second active seat.

## Generic execution roles

| Generic role | DGAF contribution | External reading | Constraint |
|---|---|---|---|
| `EXPLOIT` | Amethyst-led improvement; may use DemiJoule for resource-efficiency advice | Governance Orchestrator may pursue bounded improvement with Runtime Safety & Constraint advice | Must remain within inherited envelope |
| `DIVERGE` | Amethyst/COLLEEN may instantiate materially distinct alternatives; Nova may provide exploratory alternatives | Governed alternative generation / simulation | Diversity is not independence proof |
| `VERIFY` | Reciprocity, Professor Prodigy, Apogee, and relevant verification components | Bounded evidence, formal-methods, reciprocal-impact, and QA review | Verification role does not imply verifier independence; Professor Prodigy remains non-orchestrating |
| `GOVERN` | Sentinel-Phi as canonical governance/security identity, with Layer-0 constitutional substrate | Security & Policy Boundary Enforcement | Sentinel-Phi may veto/escalate within inherited authority; the role does not create that authority |

## Supporting identities and public translations

| Canonical identity | External-facing label | Role boundary |
|---|---|---|
| **Amethyst** | Governance Orchestrator | Meta-orchestration and lifecycle coordination within inherited governance |
| **COLLEEN** | Continuity & Provenance Coordinator | Continuity, archive, provenance, durable-state, and routing integrity |
| **Sentinel-Phi** | Security & Policy Boundary Enforcer | Canonical governance/security identity; historical `Sentinel` is an alias, not a separate active seat |
| **DemiJoule** | Runtime Safety & Constraint Adviser | Advisory resource/constraint, runtime-safety, ethics, and error-containment analysis; no independent normative authorization |
| **Reciprocity** | Reciprocal-Impact & Fairness Reviewer | Affected-party, reciprocal-impact, perspective-equity, fairness, and asymmetry review within its contract |
| **Professor Prodigy** | Formal Methods & Mathematical Analyst | Formalization, proof, mathematical/category discipline; non-orchestrating |
| **Apogee** | Evidence & Verification Reviewer | Evidence/integrity review and loop validation; independence is separately evidenced and never inferred from the name |
| **Herald** | Publication & External Communication Gatekeeper | Evidence/public-surface publication and classification; cannot manufacture evidence or approval |
| **Nova** | Simulation & Hypothesis Explorer | Exploratory alternatives and simulation; no authorization or evidence promotion |

## Sentinel disambiguation

`Sentinel` has historically appeared in two different semantic positions and must now be disambiguated:

1. historical identity alias `Sentinel` → canonical identity **Sentinel-Phi**;
2. AHG/runtime archetype associated with DemiJoule → **`SENTINEL_ARCHETYPE`**.

The second is a role class, not an alias and not an identity. Therefore a statement that DemiJoule is operating in a Sentinel archetype must never be translated as “DemiJoule is Sentinel-Phi.”

## Apogee canonicalization

`Apogee Lens` is retained only as an accepted alias for **Apogee**. New canonical technical and public documentation should use `Apogee` for identity and **Evidence & Verification Reviewer** for the external functional label.

The term “verification” in the label is functional, not an independence claim. An `INDEPENDENTLY VERIFIED` scientific or governance state requires its own accepted evidence record.

## Boundary rule

The generic role is an execution contract, not a new agent. Existing agent identity and authority remain canonical in the agent registry. A task may invoke a role through one or more eligible agents, but role invocation does not silently change an agent's authority.

Public translation follows the same rule: translation is explanatory metadata and has `authority_effect = NONE` and `scientific_state_effect = NONE`.

## PDMAL boundary

These mappings are control-plane semantics only. They do not define PDMAL topology, alter the experimental protocol, change Track A custody or analysis state, or constitute efficacy evidence.
