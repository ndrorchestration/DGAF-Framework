---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: 83e1678f55d16f32b5ce363e091ac74479cbfe1f
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **What this document does NOT claim (2026-08-26 update):** The current apparatus candidate is `83e1678f55d16f32b5ce363e091ac74479cbfe1f`. Later commits inspected in the candidate-to-current comparison are documentation/README/cross-reference changes only and do not redefine the apparatus candidate. This document does **not** constitute a freeze, a P8 closure, pilot authorization, or empirical validation. P7 is technically adjudicated but formally OPEN pending authority adoption and exact binding. P8 remains OPEN / FAIL-CLOSED. Empirical **N = 0**. No efficacy claim is authorized. Merge ≠ freeze; execution ≠ empirical validation.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Scientific decisions are resolved in the current P7 record; explicit authority adoption and exact protocol/apparatus/freeze binding remain outstanding |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation and controls exist, but executed candidate-scoped verification and analysis binding are incomplete |
| Exact apparatus candidate | IDENTIFIED | `83e1678f55d16f32b5ce363e091ac74479cbfe1f` remains the candidate; later inspected descendants are documentation-only |
| New immutable freeze | NOT CREATED | Candidate has not crossed the freeze boundary |
| Operational evidence closure | INCOMPLETE | Durable retention, candidate-scoped runtime evidence, and remaining custody/provenance checks require closure |
| P9 independent verification | NOT EXECUTED | Downstream of candidate evidence closure |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## Candidate identity boundary

The apparatus candidate is `83e1678f55d16f32b5ce363e091ac74479cbfe1f`. The prior immutable apparatus reference `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` remains historical provenance and must not be reused as the current corrected candidate. The candidate-to-current audit inspected the subsequent documentation revisions and found only documentation/README/cross-reference changes; no executable apparatus, schema, workflow, dependency, or runtime source file changed in that interval. Those commits therefore do not advance the apparatus candidate. This is an audit result, not a freeze or execution verification. Any future substantive apparatus change requires a new candidate identity and re-verification.

Historical SHA references, including earlier PR #77 and pre-correction P8 bindings, remain provenance where they describe what was actually examined; they are not current-state assertions.

## Canonical predicate state

- **P1 Candidate integrity:** PARTIAL — candidate exists; executed candidate evidence still required.
- **P2 Execution contract:** PARTIAL — implementation controls exist; current runtime evidence remains incomplete.
- **P3 Artifact contract:** PARTIAL — executable contract is strengthened; candidate-scoped verification remains required.
- **P4 Security / blinding integrity:** PARTIAL — controls and synthetic evidence exist; operational custody boundary remains to be fully evidenced.
- **P5 Provenance / reproducibility:** PARTIAL — bindings exist; candidate-scoped reproduction and environment evidence remain incomplete.
- **P6 Durable evidence custody:** OPEN — durable archive plus independent retrieval/hash evidence remains required.
- **P7 Scientific target specification:** TECHNICALLY ADJUDICATED / FORMALLY OPEN — primary contrast selected; formal authority adoption and exact binding remain outstanding.
- **P8 Analysis lock:** OPEN / FAIL-CLOSED — no closure by implementation presence alone.
- **P9 Independent verification:** NOT EXECUTED.

Authorization is separate from predicate status. Freeze is separate from authorization. Merge is not freeze, and execution is not empirical validation.

## Semantic / ontological boundary control

DGAF permits agents and components to consume and reason over an approved ontology. They must not silently introduce, redefine, or assert ontology outside the authorized semantic layer.

The canonical semantic progression is **defined → observed → supported → verified → authorized → canonical**. Operational documentation must distinguish representation, classification, policy status, epistemic status, and ontological assertion. New semantic categories are candidate vocabulary until provenance and authorization establish canonical status. Agent repetition, confidence, or wording does not create semantic authority.

**Ontology drift** is a distinct semantic-drift class: an unauthorized change in effective vocabulary, entity boundaries, relations, or semantic commitments. The broader semantic-risk taxonomy is **definition drift, ontology drift, epistemic drift, policy drift, and provenance drift**.

Semantic/ontological detection is not automatically a blocking gate. A detector must be empirically characterized before threshold-bearing or gate-bearing use. This governance control does not advance P1–P9 or alter experimental state.

## Current documentation and hygiene rules

1. Current-state assertions must identify the current candidate or explicitly say that a SHA is historical.
2. Historical evidence must retain the SHA/run/deployment actually examined.
3. Status documents cannot create closure by assertion; closure requires the evidence specified by the relevant predicate.
4. A frozen candidate tree is immutable. Later documentation corrections may clarify the record but do not rewrite the frozen apparatus.
5. P7 adoption, P8 implementation, freeze, authorization, execution, and empirical efficacy are distinct state transitions.
6. Semantic representation, classification, policy status, epistemic status, and ontology must not be silently conflated.
7. Candidate vocabulary must not be promoted to canonical vocabulary without provenance and authorization.
8. The current empirical boundary remains **N = 0** and no efficacy claim is authorized.

## Required next evidence events

1. Retain `83e1678f55d16f32b5ce363e091ac74479cbfe1f` as the apparatus candidate unless a substantive apparatus change is discovered.
2. Execute the full repository audit on that immutable candidate and retain its coverage manifest.
3. Run fresh engineering/unit/contract tests on that exact candidate.
4. Run candidate-scoped artifact, negative-path, determinism, and topology-invariant tests.
5. Execute current-candidate P2 runtime verification.
6. Execute current-candidate P6a CORS verification.
7. Complete synthetic and operational blinding verification as applicable.
8. Establish durable evidence custody and direct retrieval/hash verification.
9. Reconcile topology fingerprints and environment identity on the exact candidate.
10. Complete formal P7 authority adoption and bind the decisions to the exact protocol/candidate identity.
11. **P8 analysis lock — NEXT GATE.** Bind the executable analysis implementation/configuration to the exact candidate and protocol identity.
12. Derive P1–P8 from candidate-scoped evidence.
13. Perform P9 independent verification.
14. Create a new immutable freeze and independently verify that exact freeze.
15. Obtain explicit pilot authorization.
16. Only then execute the authorized 50-seed blinded pilot.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
