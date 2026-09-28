# DGAF System Architecture — Relationship Taxonomy

**Status:** ACTIVE_NON_AUTHORIZING / DOCUMENTATION-ONLY / NON-AUTHORIZING  
**Purpose:** classify DGAF-related entities by architectural relationship without collapsing governance, observation, research, execution, and presentation into one generic "subsystem" label.

## Canonical rule

Use **DGAF System Architecture** or **DGAF Architecture Family** as the umbrella description.

Reserve **DGAF subsystem** for internal DGAF software/control capabilities that directly participate in governance operation.

Do not call an external assurance system, research program, testbed, experimental campaign, execution substrate, runtime, transport, or operator tool a DGAF subsystem merely because DGAF governs it, consumes evidence from it, or integrates with it.

## Relationship classes

| Class | Meaning | Canonical relationship |
|---|---|---|
| DGAF Core Component | Internal governance capability required for DGAF operation | DGAF contains / implements it |
| DGAF Assurance System / Workstream | Produces or evaluates evidence without inheriting governance authority | DGAF consumes evidence from / governs use of it |
| DGAF Research Program | Investigates a hypothesis, method, topology, or governance question | DGAF governs / evaluates evidence from it |
| DGAF Experimental Testbed | Controlled apparatus/laboratory for repeatable experiments | DGAF governs experiments conducted through it |
| DGAF Experimental Campaign | Bounded governed empirical lifecycle | DGAF authorizes / constrains / closes it |
| DGAF-Integrated System | External execution/runtime/workflow/transport/tool system | DGAF governs / authorizes use of it |
| Operator Control Surface | Human-facing interface for inspection or governed action | Operators interact with DGAF through it |
| Assurance Criterion / Quality Dimension | Evaluation lens, invariant, or conformance criterion | DGAF/audits evaluate against it |
| Reference Architecture / Profile | Architectural pattern or bounded operating configuration | Implementations conform to / instantiate it |

## Canonical placement

| Entity | Primary class | Boundary |
|---|---|---|
| DGAF — Dynamic Governance Agentic Formation | Governance framework / governance authority | Governs evidence interpretation, authorization, admissible state transitions, and fail-closed decisions |
| Policy, authorization, state-transition controls | DGAF Core Components | True internal DGAF components/subsystems |
| AAR, PDP, PEP, capability governance | DGAF Core Components — authority/capability control | Provider/transport does not create authority |
| Replay, idempotency, revocation, trust-anchor safeguards | DGAF Core Components — execution-authority safeguards | Govern side-effect authority and fail-closed semantics |
| Provenance, receipts, custody, claim/evidence binding | Evidence & Assurance Components | Internal evidence-accounting/integrity mechanisms |
| DGAF-local truth/epistemic assurance mechanisms | Evidence & Assurance Components | Distinct from the broader Structural Epistemics research program |
| Audit registry, evidence-bound audit, audit-of-audits | Assurance Governance | Audit result does not inherit underlying system authority |
| AOSS — Agent Observation and Safety System | Observation & Assurance System / validation workstream | AOSS observes and assures; DGAF governs and authorizes |
| Structural Epistemics | Research Program / epistemic foundation | Research foundation informing AOSS and DGAF assurance mechanisms |
| PDMAL — Phi-Driven Multi-Agent Lattice | Research Program / governed experimental workload | Topology/coordination/failure research; practical utility remains evidence-bounded |
| PPTL — Phi-Pentagon Topology Lab | Experimental Testbed | Topology laboratory/test apparatus; not governance authority |
| Triads / Quintets | Coordination motifs / experimental interventions | Topology-choreography motifs; geometry/symmetry is not efficacy evidence |
| Track A / Epoch lifecycles | Experimental Campaigns | Bounded governed empirical programs, not software subsystems |
| Governance benchmark | Assurance Benchmark | Evaluation instrument; not authorization authority |
| Cold-start / self-application lanes | Self-validation Program | Same-system testing/evidence, not independent validation |
| AOGA — Agentic Orchestration and Governance Architecture | Reference Architecture / architecture lineage | Does not imply a separate governance authority absent explicit evidence |
| Q-CP / Q-BE / Q-MP | Quality Dimensions / assurance controls | Evaluation criteria, not systems |
| ACP — Agent Control Plane | DGAF-Integrated Execution Substrate | ACP executes; DGAF governs |
| Remote Desktop Commander | DGAF-Integrated Execution Endpoint | Adds execution reach/evidence capture, not governance authority or independence |
| n8n | DGAF-Integrated Workflow Runtime | Workflow/orchestration runtime governed through policy |
| Reticulum | Transport / Integration Research Lane | Candidate communications/runtime adapter; not DGAF core unless separately adopted |
| Governance/evidence/state-space UI | Operator Control Surface | Displays/mediates governed state; does not create control truth |

## Naming rules

1. Use **DGAF component** only for a capability implemented inside DGAF and directly participating in governance operation.
2. Use **DGAF assurance system/workstream** for non-authorizing evidence-producing/evaluating systems.
3. Use **DGAF research program** or **DGAF-governed research program** for hypothesis-driven research such as PDMAL.
4. Use **experimental testbed** for apparatus/labs such as PPTL.
5. Use **experimental campaign** for bounded Track/Epoch lifecycles.
6. Use **DGAF-integrated system** for external runtimes/execution systems such as ACP, RDC, n8n, and future adapters.
7. Use **operator control surface** for governance/evidence/state-space interfaces.
8. Do not use "subsystem" merely to mean "related to DGAF."

## Authority invariant

`OBSERVED != VERIFIED != ACCEPTED != AUTHORIZED != EXECUTED != SCIENTIFICALLY_VALIDATED`

- **AOSS observes / assures.**
- **DGAF interprets / governs / authorizes.**
- **ACP and governed runtimes execute.**
- **Research programs generate bounded evidence.**
- **Operator surfaces display and mediate; they do not create authority.**

## Historical-language rule

Do not mass-rewrite historical evidence, audits, or retained research merely because they contain the word "subsystem." Preserve event-time terminology unless it creates a current-facing authority ambiguity. Current-facing documentation should use the relationship classes above.

Repository scan at the source base found 11 uses of "subsystem"; most are generic/internal/historical and do not justify blanket replacement.

## Public shorthand

> **DGAF governs. AOSS observes. ACP executes. Structural Epistemics supplies the epistemic research foundation. PDMAL and PPTL supply governed research workloads and testbeds.**

This shorthand is explanatory only and does not collapse the precise classes above.

## Non-effect

This taxonomy changes naming and architecture routing only. It does not alter scientific N, efficacy, independent-validation status, external-validation status, execution authority, protected-materialization authority, production security, or High-Assurance status.
