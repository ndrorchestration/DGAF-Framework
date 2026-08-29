# DGAF Agent Authority Matrix

**Invariant:** DGAF-AUTH-001  
**Status:** ACTIVE — BASELINE DERIVATIVE  
**Version:** 1.0.0  
**Purpose:** Machine-readable-by-inspection derivative of the canonical roster, formation topology, and agent specifications. This matrix does not grant authority; it records existing authority boundaries and identifies where reconciliation is required.

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

## 2. Canonical Baseline

| Agent | Current documented role | Authority class | Explicit boundary | Source |
|---|---|---|---|---|
| Amethyst | Meta-orchestration; final commit/normative governance | SOVEREIGN / GATE | Cannot silently inherit another specialist's lane | AGENT_ROSTER.md |
| Apogee | Evidence governance; verification; Layer-0 legitimacy gate | GATE / VERIFICATION | Owns scoring/verification lane; does not become execution authority | AGENT_ROSTER.md; FORMATION_TOPOLOGY.md |
| Perigee | Proximal boundary/security filter | GATE | Automatic boundary blocks within its documented scope | AGENT_ROSTER.md; FORMATION_TOPOLOGY.md |
| Nova | Innovation/simulation | ADVISORY / SIMULATION | Advisory until applicable governance gate clears | AGENT_ROSTER.md |
| Professor Prodigy | Mathematical/formalization authority | VERIFICATION / ADVISORY | Does not orchestrate | AGENT_ROSTER.md; PROFESSOR_PRODIGY_KB.md |
| COLLEEN | Institutional anchor; swarm/continuity/archive governance | GOVERNANCE / ARCHIVAL | Surfaces and manages governance state; normative authority remains governed by canonical assignments | AGENT_ROSTER.md |
| The Librarian | Provenance/archive | ARCHIVAL | Preserves records; does not alter decision authority | AGENT_ROSTER.md |
| The Auditor | Constraint verification / QA | VERIFICATION / GATE | Validates; does not silently execute | AGENT_ROSTER.md |
| The Actualizer | Code/artifact execution | EXECUTION | Implements authorized changes; cannot infer authorization from feasibility | AGENT_ROSTER.md |
| Zenith | Compute/system-high optimization | ADVISORY / INFRASTRUCTURE | Resource/compute lane only | AGENT_ROSTER.md |
| Reson | Harmonic coherence | VERIFICATION / GATE | Harmonic score lane; threshold semantics remain scoped | AGENT_ROSTER.md |
| Lyra | Narrative/synthesis | ADVISORY / PUBLIC-FACING SUPPORT | No authority to change governance state | AGENT_ROSTER.md |
| Echolette | Pattern amplification/echo validation | VERIFICATION / ADVISORY | Phrase/coherence lane only | AGENT_ROSTER.md |
| Ionia | 0Hz convergence state | STATE | Not a functional seat; no independent decision authority | FORMATION_TOPOLOGY.md; AGENT_ECOSYSTEM_REGISTRY.md |
| DemiJoule | Token/compute efficiency; quality-cost analysis | ADVISORY | Normal operation non-blocking; joint block only with specified Apogee failure | DEMIJOULÉ SPEC / roster |
| Herald | External publication/release communication | PUBLICATION / EXECUTION | Executes publication authority within release contract; cannot publish sovereign data | HERALD SPEC |
| Reciprocity | Fairness/rollback/TNR/feedback integrity | GATE / ADVISORY | Owns Q9/F-4 rollback lane; fairness flags remain distinct from governance authority | RECIPROCITY SPEC / INTEGRATION |
| Sentinel-Φ / Sentinel | Security/IP/T3 boundary | GATE / HARD BLOCK | Sovereign/security boundary only; conflict resolution follows canonical contract | SENTINEL SPEC / FORMATION_TOPOLOGY |
| Sentience | Ethics Bridge / ETHICAL_HOLD | GATE | Holds ethical review authority within its sealed Ethics Bridge contract | FORMATION_TOPOLOGY / REGISTRY |

## 3. Non-Delegation Rules

1. Capability overlap does not create authority overlap.
2. Advisory output MUST NOT silently become authorization.
3. Verification MUST remain distinct from authorship where independence matters.
4. Execution MUST require the authorization defined by the governing contract.
5. Publication MUST preserve classification and truthful evidence status.
6. Layer-0 constraints propagate downstream; no single agent is presumed to own all Layer-0 meaning.
7. A system STATE such as Ionia/0Hz MUST NOT be treated as an agent with independent authority.
8. T3/SOVEREIGN material remains subject to the repository's IP firewall and Drive-only rules.

## 4. Layer-0 Shared Substrate

Layer 0 is a **shared constitutional substrate**, not a single-persona role. It includes:

- human dignity and human rights;
- lawful-operation constraints;
- safety and security;
- privacy;
- non-discrimination and fairness;
- human agency and oversight;
- public accountability;
- legitimate disclosure/transparency;
- contestability/recourse where applicable;
- protection against inappropriate exposure of sensitive or sovereign material.

Specialist interpretation is divided by domain. Canonical gate ownership remains defined by the roster and topology.

## 5. Public Legibility & Visibility

For public-facing DGAF surfaces, evaluate independently:

**Accessibility → Comprehensibility → Appropriateness of disclosure.**

Agents must preserve explicit status distinctions:

`IMPLEMENTED · TESTED · VERIFIED · EXPERIMENTALLY DEMONSTRATED · PROPOSED · HYPOTHETICAL · HISTORICAL · NOT ESTABLISHED`

Public presentation must optimize for accurate comprehension, not persuasion.

## 6. Reconciliation Requirements

The following are known sources requiring explicit reconciliation before authority changes are canonicalized:

- legacy role text in `AGENT_ROSTER.md` versus newer role-specific specs;
- Layer-0 attribution/ownership language across roster, topology, and agent documents;
- Sentinel versus Sentinel-Φ naming and authority continuity;
- historical IDs versus current formation IDs;
- agent specification naming conventions;
- any Drive/GitHub representation drift.

These are **reconciliation targets**, not permission to silently rewrite canonical authority.

## 7. Required Change Procedure

For a proposed authority change:

1. identify the affected agent and current authority source;
2. compare roster, topology, registry, and SPEC/KB/PROTOCOL/INTEGRATION artifacts;
3. identify conflicts and historical provenance;
4. define the proposed delta and its scope;
5. obtain the authorization required by the canonical governance contract;
6. update all affected artifacts atomically where practical;
7. add or update deterministic tests;
8. verify exact commit identity and CI evidence;
9. update public-facing documentation without overstating evidence.

## 8. Conformance Target

A future automated check should fail when:

- an agent claims an authority absent from the canonical matrix;
- two agents are assigned the same exclusive authority without an explicit shared-gate contract;
- an execution agent is permitted to proceed without required authorization;
- a publication artifact crosses its classification boundary;
- a documented role change is missing its required provenance/authorization record.

**The matrix is descriptive at this stage. It does not supersede the sovereign roster or sealed formation contracts.**
