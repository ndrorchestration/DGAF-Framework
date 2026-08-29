# DGAF Agent Authority Matrix

**Invariant:** DGAF-AUTH-001  
**Status:** ACTIVE — BASELINE DERIVATIVE  
**Version:** 1.1.0  
**Purpose:** Machine-readable-by-inspection derivative of canonical agent authority sources. This matrix records authority boundaries; it does not grant authority.

> **Core invariant:** Shared governance ontology MUST NOT imply shared authority.

## 1. Authority Classes

| Class | Meaning |
|---|---|
| SOVEREIGN | Authority spanning the governed system or protected sovereign boundary |
| GATE | May determine pass/block/hold within a named gate |
| VERIFICATION | May evaluate evidence or quality within a defined verification lane |
| EXECUTION | May implement an already-authorized decision |
| ADVISORY | May recommend, flag, score, or analyze without unilateral authorization |
| ARCHIVAL | May preserve provenance/records without changing the underlying decision |
| PUBLICATION | May control or execute outward-facing publication within its defined contract |
| STATE | Represents a system condition, not an independent agent authority |

## 2. Current Authority Baseline

| Agent | Current documented role | Authority class | Explicit boundary | Source |
|---|---|---|---|---|
| Amethyst | Meta-orchestration; normative governance/final commit gate | SOVEREIGN / GATE | Cannot silently inherit another specialist's lane | AGENT_ROSTER.md; Control Center |
| Apogee | Verification / evidence governance; 11Q integrity lane | GATE / VERIFICATION | Verification is distinct from execution and authorship | AGENT_ROSTER.md; FORMATION_TOPOLOGY.md |
| Perigee | Legitimacy / boundary / security filter | GATE | Layer-0 legitimacy and contaminated-input blocking remain scoped to its contract | AGENT_ROSTER.md |
| Nova | Innovation / simulation | ADVISORY / SIMULATION | Advisory until applicable governance gate clears | AGENT_ROSTER.md |
| Professor Prodigy | Formalization / proof / mathematical claim review | VERIFICATION / ADVISORY | Non-orchestrating; does not acquire normative authority from analysis | AGENT_ROSTER.md; Notion Agent Registry |
| COLLEEN | Continuity / archive / swarm routing | GOVERNANCE / ARCHIVAL | Does not make unassigned normative decisions | AGENT_ROSTER.md |
| The Librarian | Provenance / archive | ARCHIVAL | Preserves records; cannot alter authority | AGENT_ROSTER.md |
| The Auditor | Constraint verification / QA | VERIFICATION / GATE | Validates within its QA lane; cannot silently execute | AGENT_ROSTER.md |
| The Actualizer | Code / artifact execution | EXECUTION | Implements authorized decisions; cannot infer authorization from feasibility | AGENT_ROSTER.md |
| Zenith | System-high / compute optimization | ADVISORY / INFRASTRUCTURE | Resource/compute lane only | AGENT_ROSTER.md |
| Reson | Harmonic coherence | VERIFICATION / GATE | Harmonic threshold lane; no general governance authority | AGENT_ROSTER.md |
| Lyra | Synthesis / narrative | ADVISORY / PUBLIC-FACING SUPPORT | Cannot change governance state | AGENT_ROSTER.md |
| Echolette | Pattern amplification / echo validation | VERIFICATION / ADVISORY | Phrase/coherence lane only | AGENT_ROSTER.md |
| Ionia | Modal lock / convergence state | STATE / ADVISORY | State representation; no independent governance authority | FORMATION_TOPOLOGY.md; REGISTRY |
| DemiJoule | Ethics/resource-efficiency advisory; cost/bloat analysis | ADVISORY | Cannot independently veto, authorize, or execute; reports constraints to governing authority | DEMI_JOULE_SPEC.md; Notion profile |
| Herald | Broadcast / release communication | PUBLICATION / EXECUTION | Relays/records and executes publication within release contract; cannot create evidence or approval | HERALD_SPEC.md; Notion profile |
| Reciprocity | Fairness / rollback / asymmetry review | GATE / ADVISORY | F-4 rollback block and fairness lane only; no general normative authority | RECIPROCITY_SPEC.md; Notion profile |
| Sentinel-Φ | Strategic security / sovereign-IP boundary | GATE / HARD BLOCK | Security, sovereign/IP, protected-disclosure, and fail-closed containment within contract | SENTINEL_SPEC.md; Notion Sentinel-Phi profile |

## 3. Shared Layer-0 Constitutional Substrate

Layer 0 is a distributed constitutional constraint, not a single-agent ownership claim. The authoritative Layer-0 contract is `docs/agents/LAYER_0_CONSTITUTION.md` and is constrained by DGAF-AUTH-001.

Layer 0 covers, as applicable:

- human dignity and human rights;
- lawful-operation constraints;
- safety and security;
- privacy and data protection;
- non-discrimination and fairness;
- human agency and legitimate oversight;
- public accountability;
- transparency and contestability where applicable;
- protection against inappropriate disclosure of sensitive or sovereign material;
- public comprehension and truthful maturity/evidence representation.

Domain responsibilities are distributed. No agent receives total Layer-0 authority merely because it is capable of reasoning about Layer-0 issues.

## 4. Layer-0 Specialist Composition

| Specialist | Layer-0 contribution | Authority limit |
|---|---|---|
| Perigee | Legitimacy / boundary filtering | Scope limited to its defined legitimacy/security gate |
| Sentinel-Φ | Security, sovereign boundary, protected disclosure, fail-closed containment | Does not become general ethics or normative authority |
| Reciprocity | Fairness, asymmetry, affected-party and reciprocal-impact analysis | Does not become general normative authority |
| Professor Prodigy | Formal/category analysis of rights, policy, mathematical, and epistemic claims | Non-orchestrating; no authority inferred from expertise |
| Amethyst | Governance disposition where canonically assigned | Cannot impersonate specialist verification/security authority |
| DemiJoule | Convert approved constraints into efficient engineering recommendations | Advisory; no unilateral veto/authorization |
| Herald | Make approved status/evidence understandable and control public release | Cannot manufacture evidence or governance approval |
| Apogee | Independent evidence/quality verification where assigned | Verification is not normative authorization |
| COLLEEN / Librarian | Preserve governance state, provenance, and historical distinctions | Records do not themselves authorize action |
| Reson / Lyra / Echolette | Domain-specific observations, synthesis, communication and coherence | Domain output cannot silently become governance state |

## 5. Non-Delegation Rules

1. Capability overlap does not create authority overlap.
2. Advisory output MUST NOT silently become authorization.
3. Verification MUST remain distinct from authorship where independence matters.
4. Execution MUST require the authorization defined by the governing contract.
5. Publication MUST preserve classification and truthful evidence status.
6. Layer-0 constraints propagate downstream; no single agent is presumed to own all Layer-0 meaning.
7. State representations such as Ionia/0Hz MUST NOT be treated as independent agents with authority.
8. T3/SOVEREIGN material remains subject to the repository IP firewall and Drive-only rules.
9. Historical aliases or merged identities MUST NOT be treated as additional active seats.

## 6. Public Legibility & Visibility

For public-facing DGAF surfaces, evaluate independently:

**Accessibility → Comprehensibility → Appropriateness of Disclosure.**

Preserve status distinctions:

`IMPLEMENTED · TESTED · VERIFIED · EXPERIMENTALLY DEMONSTRATED · PROPOSED · HYPOTHETICAL · HISTORICAL · NOT ESTABLISHED`

Repository/account visibility review should consider source code, branches, pull requests, issues, Actions logs, artifacts, releases, deployment metadata, generated files, historical commits, external integrations, credentials/secrets exposure, personal information, and sovereign/IP material.

## 7. Current Identity Normalization

**Sentinel-Φ** is the active canonical identity. **Sentinel** is a historical alias only. **Sentience** is a historical/merged identity and is not a separate active seat. These labels MUST NOT create duplicated authority.

## 8. Reconciliation Targets

The following remain explicit reconciliation targets:

- legacy `AGENT_ROSTER.md` text versus newer Notion taxonomy/registry state;
- historical versus current formation IDs;
- expanded registry agent count versus visible enumerations;
- per-agent SPEC naming and completeness;
- Layer-0 ownership language across legacy gates, roster, topology, and current profiles;
- Drive/GitHub representation drift;
- exact source SHA/provenance for current claims.

These are discrepancies to resolve under governance, not permission to infer a winner.

## 9. Change Procedure

For every proposed authority change:

1. identify the current authority source;
2. compare roster, topology, registry, SPEC/KB/PROTOCOL/INTEGRATION artifacts, and current Control Center state;
3. identify historical/superseded material;
4. define the proposed delta and affected contracts;
5. obtain required authorization;
6. update affected artifacts coherently;
7. add deterministic tests;
8. verify exact commit/runtime evidence;
9. update public-facing material without overstating evidence;
10. retain the provenance trail.

## 10. Conformance Target

Future automated checks SHOULD fail when:

- an agent claims authority absent from canonical sources;
- an exclusive gate is duplicated without an explicit shared-gate contract;
- an execution agent lacks required authorization;
- publication crosses a classification boundary;
- a merged/historical identity is treated as active;
- a material role change lacks provenance and authorization evidence.

**This matrix remains a governed derivative. It does not supersede the current Control Center, sealed formation contracts, or explicitly authoritative source documents within their defined scope.**
