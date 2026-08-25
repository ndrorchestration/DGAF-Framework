# DGAF Prior-Art and Related-Work Scope

**Status:** Research map and comparison protocol; not a novelty conclusion  
**Date:** 2026-08-25

## Purpose

This document defines how DGAF's related-work and prior-art review should be conducted before public claims about novelty, distinctiveness, or priority are strengthened.

The purpose is not to search for evidence that confirms originality. The purpose is to identify relevant overlap, distinguish terminology from mechanism, and describe DGAF accurately in relation to existing work.

## 1. Review question

The central question is:

> Which elements of DGAF are established techniques, adaptations, combinations, or potentially distinct formulations when compared with relevant work in multi-agent systems, orchestration, governance, runtime assurance, evaluation, provenance, and distributed systems?

A secondary question concerns synthesis:

> Even where individual components are established, does DGAF define a materially distinct integration, evidence discipline, or implementation boundary that warrants separate technical characterization?

Neither question should be answered by terminology alone.

## 2. Comparison dimensions

Each candidate prior work should be compared across:

| Dimension | Question |
|---|---|
| Problem | What problem is addressed? |
| Unit of control | Model output, agent, action, workflow, system, or organization? |
| Orchestration mechanism | How are roles, tasks, communication, or topology organized? |
| Governance mechanism | Is governance declarative, runtime-enforced, test-based, policy-based, or otherwise operationalized? |
| Evidence/provenance | What execution or claim evidence is retained and how is it bound to artifacts? |
| Evaluation | What outcomes or behaviors are measured and against what baselines? |
| Scope | What environments and assumptions bound the claims? |
| Evidence state | Conceptual, implemented, tested, empirical, independently reproduced, or other? |

Superficial similarity should not be treated as equivalence, and differences in terminology should not be treated as novelty.

## 3. Required research domains

The review should cover at minimum:

1. Multi-agent systems and coordination architectures.
2. Agent orchestration and control planes.
3. AI governance and runtime assurance.
4. Agent evaluation, testing, and benchmarking.
5. Provenance, traceability, reproducibility, and evidence management.
6. Distributed systems, fault containment, recovery, and control mechanisms.
7. Formal methods and specification where DGAF makes bounded formal claims.

Additional domains should be added when a DGAF component depends materially on their concepts.

## 4. Initial literature signals — not conclusions

A preliminary scan identifies substantial and growing work connecting agent orchestration with governance, assurance, evaluation, and traceability. Recent surveys and frameworks discuss fragmented governance and evaluation practices, trajectory-level accountability, runtime controls, action provenance, trace-based assurance, and multi-agent coordination.

These signals mean DGAF must **not** claim that the general combination of orchestration and governance is unprecedented. They instead define comparison targets for determining the narrower contribution of DGAF's formulation and implementation.

In particular, the review should examine whether DGAF differs in:

- its explicit three-concern relationship among formation/orchestration, governance/control, and evidence/provenance;
- its claim-level epistemic governance integrated with implementation and experimental gates;
- its version-bound evidence and provenance discipline;
- the relationship between governance controls and experimental authorization; and
- any specific implementation mechanisms that survive mechanism-level comparison.

These are hypotheses for comparison, not novelty claims.

## 5. Review protocol

For each source or system:

1. Record the stable bibliographic or repository identifier.
2. Extract only claims supported by the source itself.
3. Populate the comparison dimensions.
4. Identify direct overlap, partial overlap, and unresolved relationships.
5. Record differences without assuming that differences are improvements.
6. Assign a provisional relationship:
   - `foundational prior work`
   - `related approach`
   - `partial overlap`
   - `implementation analogue`
   - `candidate distinction`
   - `unresolved`
7. Revisit candidate distinctions after broader search and expert review.

The final related-work section should preserve meaningful overlap rather than minimizing it.

## 6. Novelty language rules

Until the review is complete, public language should prefer:

- “DGAF presents a documented synthesis…”
- “DGAF combines…”
- “DGAF proposes…”
- “This implementation explores…”
- “The framework differs in the following documented respects…”

Avoid:

- “first ever”;
- “unique” without a defined comparison universe;
- “unprecedented”;
- “solves” where evidence only supports implementation or bounded testing; and
- any implication that publication timestamp alone proves conceptual priority.

## 7. Deliverables

The review should produce:

- a machine-readable or tabular related-work matrix;
- a narrative related-work section for the technical overview or white paper;
- a list of established dependencies and influences;
- a list of unresolved comparison questions; and
- a narrowly scoped contribution statement revised to match the evidence.

## 8. Current conclusion

**No absolute novelty conclusion has been reached.** The current public record supports describing DGAF as a documented research and implementation framework with a specific evidence-aware formulation. The distinctiveness and scientific significance of that formulation remain questions for systematic comparison, experimentation, and external scrutiny.

## Cross-references

- [`CANONICAL_TECHNICAL_OVERVIEW.md`](CANONICAL_TECHNICAL_OVERVIEW.md)
- [`PUBLICATION_AND_PROVENANCE_SPINE.md`](PUBLICATION_AND_PROVENANCE_SPINE.md)
- [`PATTERN_COMMONS_ARCHITECTURE.md`](PATTERN_COMMONS_ARCHITECTURE.md)
- [`CLAIM_EVIDENCE_INDEX.md`](CLAIM_EVIDENCE_INDEX.md)
