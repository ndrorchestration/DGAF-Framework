# DGAF Historical-Priority Timeline Methodology

**Established 2026-09-01.** This document records the methodological standard for any DGAF historical-priority timeline work going forward. It is stored as a file rather than in memory context to avoid exceeding the memory character budget.

## Core Principle

Use the **existing DGAF taxonomy, vocabulary, and provenance conventions** — do **not** invent a new classification system. The existing External-equivalent mapping convention already provides the appropriate structure.

## Epistemic Status Preservation

Every substantive claim retains its canonical epistemic class:

- `DEFINED`, `IMPLEMENTED`, `COMPUTED`, `VERIFIED`, `ATTESTED`
- `HISTORICAL`, `HYPOTHESIS`, `METAPHOR`, `UNSUPPORTED`, `DEPRECATED`

Timeline conclusions are **separate** from epistemic status. The five allowable timeline conclusions are:

1. **DGAF PRIOR** — dated evidence establishes the mechanism/concept before the external analogue
2. **PARALLEL / INDEPENDENT CONVERGENCE** — both appear independently within a close period; neither can responsibly be declared first
3. **EXTERNAL PRIOR** — the external concept predates the relevant DGAF evidence
4. **TERMINOLOGICAL CONVERGENCE** — underlying mechanism may have existed independently; terminology subsequently converged
5. **UNRESOLVED** — available provenance cannot establish chronological priority

## Per-Object Structure

For each significant DGAF primitive, record:

| Field | Meaning |
|-------|---------|
| **DGAF object** | Exact concept, mechanism, vocabulary item, architecture, experiment |
| **DGAF earliest evidence** | Earliest dated artifact actually supporting the claim |
| **DGAF epistemic class** | `DEFINED`, `IMPLEMENTED`, `COMPUTED`, `VERIFIED`, etc. |
| **External analogue** | Closest recognized external concept |
| **External earliest evidence** | Earliest authoritative dated source located |
| **Temporal relationship** | Prior / parallel / subsequent / unresolved |
| **Functional overlap** | What actually overlaps |
| **Functional divergence** | What differs |
| **Terminological relationship** | Same term / different term / later convergence |
| **Provenance strength** | How firmly each date is established |
| **Priority conclusion** | What can actually be claimed |
| **Open evidence** | What would change the conclusion |

## Strongest Form of the Research

The research should be a **provenance-backed functional convergence audit**:

> For every significant DGAF primitive, determine the earliest dated DGAF evidence, identify the closest externally recognized analogue, locate its earliest authoritative evidence, compare the actual functions, and determine whether the evidence supports prior development, parallel convergence, external precedence, terminology convergence, or an unresolved relationship.

## Negative Findings

Preserve negative findings. If extensive searching locates no earlier equivalent, the defensible statement is:

> "No earlier authoritative equivalent was located within the searched corpus as of [date]."

This is stronger and more scientifically appropriate than an unsupported "first." It does not claim absolute novelty.

## Priority Dimensions Are Provenance Dimensions

Conceptual priority, formalization priority, implementation priority, and publication priority are **dimensions of the existing provenance comparison**, not additional DGAF taxonomy. This keeps the system consistent with the repository's explicit rule that the vocabulary registry is a translation registry rather than a certification registry.

## PDMAL/BFT Example — How This Works in Practice

PDMAL's canonical mapping is deliberately constrained: graph properties and selected mathematical quantities can be `VERIFIED`, while the broader architectural role is `DEFINED`. Claiming that PDMAL is a complete BFT protocol remains `UNSUPPORTED` without separate implementation and fault-model evidence.

If an earlier BFT paper with something that superficially resembles PDMAL is found, the timeline **cannot** conclude:

- "PDMAL was already BFT." (unsupported identity claim)
- "PDMAL independently invented BFT." (unsupported independence claim)

Instead, compare the actual functional objects:

- **PDMAL lattice/control structure** vs. **external BFT mechanism**

Record exactly where they overlap and diverge. Apply the same discipline to terms such as **Ricci, Lyapunov, spectral, Hecke, attractor, Phi-Calculus**: the existing vocabulary explicitly requires the name to correspond to the mathematical object actually implemented; otherwise it remains metaphorical or otherwise qualified.

## Formation Governance vs. Action Governance — The Consolidation Test

The historical investigation has converged on an important architectural distinction that the methodology must capture: **governing individual agent actions is not the same as governing the formation itself.**

This distinction emerged directly from the historical priority audit. External systems (notably Microsoft AGT, ADR 0006 dated 2026-04-18) demonstrate veto-based governance, escalation by fanout, constitutional constraint layers, and actor-role maps — but these operate at the **action-governance** layer: an agent proposes an action, a gate evaluates it, a critic may veto or escalate, and execution proceeds or is blocked. The formation producing the agent is not itself the governed object.

DGAF's candidate lineage, by contrast, includes evidence of **formation-as-governed-object**: the formation proposal, membership resolution, authority assignment, topology construction, veto/conflict resolution, and committed formation state are treated as joint architectural objects, with formation transitions (FORM → RECONFIGURE → HANDOFF → ESCALATE → SUSPEND → DISBAND) as first-class governed state transitions. This is the **formation-governance** layer.

The methodology therefore includes a consolidation predicate test for any claim that DGAF possesses an integrated formation-centric governance architecture. The test is:

| Predicate | Required evidence |
|-----------|-------------------|
| F1 | Dynamic membership / formation |
| F2 | Formation represented explicitly as state |
| F3 | Authority attached to formation or membership |
| F4 | Topology participates in authority/governance |
| F5 | Formation transitions are explicit |
| F6 | Conflict-resolution semantics exist |
| F7 | Veto/escalation can alter formation state |
| F8 | Transition semantics are idempotent |
| F9 | Evidence/audit is attached to the transition |
| F10 | All of F1–F9 are one coherent architecture, not unrelated modules |

The priority question becomes: **Did anyone publish or implement F1–F10 before DGAF's earliest corresponding evidence?**

This test operationalizes the "integrated architecture" question that the per-object structure alone cannot answer. Individual predicates (F1–F9) can each have external precedents; the historically interesting question is whether the **full consolidated architecture (F10)** existed before DGAF's corresponding evidence.

**Current assessment (as of the most recent sweep):**

- **F1–F8:** individual precedents exist in the broader literature/software ecosystem.
- **F9:** strong external precedent exists.
- **F10:** no exact pre-DGAF match has yet been established.

This makes the consolidation test the highest-value historical-priority investigation remaining.

## Cross-Domain Integration as the Correct Claim Unit

The most recent historical sweep indicates that the historically interesting object is **not** the full tuple of individual controlled mechanisms, but a narrower **cross-domain composition in which a changeable multi-agent formation is treated as a persistent governed state and the same lifecycle subsequently carries governance and evidence constraints across experimental execution, exact candidate identity, verification, and authorization**.

For that claim, the relevant unit of comparison is therefore **not** "did a prior system contain one of these mechanisms?" but "did a prior public system make the formation itself the governed object **and** connect that formation governance to exact experimental candidate identity and candidate-scoped verification/authorization?"

The current evidence chain supports a defensible distinction between three layers:

1. **Action-governance primitives** — external prior.
2. **Formation-as-governed-object primitives** — substantially external prior, with TB-CSPN as a notably close modern comparator that includes dynamic group formation, supervisor authorization, membership thresholds, a group registry, transition metadata with provenance, and multi-stage validation before integration; it does **not** clearly establish formation-level veto, authority conflict resolution, formation-transition idempotency, or exact software-candidate identity.
3. **The integrated lifecycle joining formation governance to candidate-bound experimental evidence and verification** — unresolved; strongest remaining historical question.

Any future claim must be stated at layer 3 only if the predecessor search covers that exact cross-domain integration, with primary dated sources, and must avoid presenting the individual layers as if they were the integrated claim.

## Self-Audit Before External Comparison — DGAF Must Evidence Its Own Integration

Before comparing DGAF against predecessors, the methodology requires a DGAF self-audit of the claimed integrated architecture. The historical claim can only be as strong as the positive evidence that DGAF implements the full composition as a jointly governed architecture, not merely as co-occurring artifacts in the same repository.

For each claimed component, the audit must establish:

- Earliest DGAF evidence.
- Epistemic level: defined, documented, implemented, verified, or external.
- Whether the evidence shows **integration** (the components are mutually constraining) or only **co-occurrence** (the components exist in the same project).

This audit is especially important because the DGAF commit history shows the strongest formation-specific elements appearing in a staged sequence: April 29 naming/identification, May 1 formation specification plus authority conflict resolution, veto hierarchy, and idempotency guarantee. That sequence supports an **independent architectural evolution** story even where it does not support an April 29 assertion of the full integrated composition.

## Formation Governance vs. Action Governance — The Consolidation Test

The historical investigation has converged on an important architectural distinction that the methodology must capture: **governing individual agent actions is not the same as governing the formation itself.**

This distinction emerged directly from the historical priority audit. External systems (notably Microsoft AGT, ADR 0006 dated 2026-04-18) demonstrate veto-based governance, escalation by fanout, constitutional constraint layers, and actor-role maps — but these operate at the **action-governance** layer: an agent proposes an action, a gate evaluates it, a critic may veto or escalate, and execution proceeds or is blocked. The formation producing the agent is not itself the governed object.

DGAF's candidate lineage, by contrast, includes evidence of **formation-as-governed-object**: the formation proposal, membership resolution, authority assignment, topology construction, veto/conflict resolution, and committed formation state are treated as joint architectural objects, with formation transitions (FORM → RECONFIGURE → HANDOFF → ESCALATE → SUSPEND → DISBAND) as first-class governed state transitions. This is the **formation-governance** layer.

The methodology therefore includes a consolidation predicate test for any claim that DGAF possesses an integrated formation-centric governance architecture. The test is:

| Predicate | Required evidence |
|-----------|-------------------|
| F1 | Dynamic membership / formation |
| F2 | Formation represented explicitly as state |
| F3 | Authority attached to formation or membership |
| F4 | Topology participates in authority/governance |
| F5 | Formation transitions are explicit |
| F6 | Conflict-resolution semantics exist |
| F7 | Veto/escalation can alter formation state |
| F8 | Transition semantics are idempotent |
| F9 | Evidence/audit is attached to the transition |
| F10 | All of F1–F9 are one coherent architecture, not unrelated modules |

The priority question becomes: **Did anyone publish or implement F1–F10 before DGAF's earliest corresponding evidence?**

This test operationalizes the "integrated architecture" question that the per-object structure alone cannot answer. Individual predicates (F1–F9) can each have external precedents; the historically interesting question is whether the **full consolidated architecture (F10)** existed before DGAF's corresponding evidence.

**Current assessment (as of the most recent sweep):**

- **F1–F8:** individual precedents exist in the broader literature/software ecosystem.
- **F9:** strong external precedent exists.
- **F10:** no exact pre-DGAF match has yet been established.

This makes the consolidation test the highest-value historical-priority investigation remaining.

## Negative Findings Preserved

Preserve negative findings. If extensive searching locates no earlier equivalent, the defensible statement is:

> "No earlier authoritative equivalent was located within the searched corpus as of [date]."

This is stronger and more scientifically appropriate than an unsupported "first." It does not claim absolute novelty.

## Priority Dimensions Are Provenance Dimensions

- No claim of the form "DGAF invented X before company Y."
- No promotion from analogy to identity without implementation evidence.
- No quantitative claims without provenance/reproducibility.
- No historical claims without retaining their historical qualifier.
- No treating timeline conclusions as new epistemic statuses.
