---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: 190a205002e9a9014005793a346324b5fb08ec76
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **What this document does NOT claim (2026-08-26 update):** The current verification candidate contains post-`83e1678f...` P8 integrity fixes. It does **not** constitute a freeze, P8 closure, pilot authorization, or empirical validation. P7 is technically adjudicated but formally OPEN pending authority adoption and exact binding. P8 remains OPEN / FAIL-CLOSED. Empirical **N = 0**. No efficacy claim is authorized. Merge ≠ freeze; execution ≠ empirical validation.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Scientific decisions are resolved; authority adoption and exact binding remain open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Integrity fixes are present, but fresh candidate-scoped execution and binding are incomplete |
| Exact verification candidate | IDENTIFIED (corrected P8 basis) | `190a205002e9a9014005793a346324b5fb08ec76` is the current executable candidate requiring verification |
| Prior candidate | SUPERSEDED | `83e1678f55d16f32b5ce363e091ac74479cbfe1f` remains historical candidate provenance |
| New immutable freeze | NOT CREATED | Candidate has not crossed the freeze boundary |
| Operational evidence closure | INCOMPLETE | Candidate-scoped runtime evidence, durable retention, and custody/provenance checks remain open |
| P9 independent verification | NOT EXECUTED | Downstream of candidate evidence closure |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## Candidate transition record

`83e1678f...` was previously the corrected verification candidate. Subsequent executable integrity fixes require a new candidate identity:

- `d65df466...` — P8 analysis rejects boolean numeric inputs;
- `141d02a4...` — pilot artifact records are bound to document identity and duplicate matrix cells are rejected;
- `c70d0691...` — each blinded condition must contain the complete 45-cell matrix;
- `60a33634...` — isolated retry timing honors the injected clock;
- `190a2050...` — pilot recovery/status semantics distinguish zero-failure success from recovered failures.

These are executable changes, so `190a205002e9a9014005793a346324b5fb08ec76` is the current verification candidate. Earlier SHAs remain historical provenance for what was actually examined.

## Canonical predicate state

- **P1 Candidate integrity:** PARTIAL — current candidate identified; fresh execution evidence required.
- **P2 Execution contract:** PARTIAL — implementation exists; candidate-scoped runtime evidence remains incomplete.
- **P3 Artifact contract:** PARTIAL — identity, uniqueness, and balanced-matrix checks strengthened; candidate-scoped validation remains required.
- **P4 Security / blinding integrity:** PARTIAL — controls exist; operational custody evidence remains incomplete.
- **P5 Provenance / reproducibility:** PARTIAL — record/document bindings strengthened; fresh candidate environment evidence remains required.
- **P6 Durable evidence custody:** OPEN — durable archive plus independent retrieval/hash evidence remains required.
- **P7 Scientific target specification:** TECHNICALLY ADJUDICATED / FORMALLY OPEN — authority adoption and exact binding remain required.
- **P8 Analysis lock:** OPEN / FAIL-CLOSED — implementation presence is not closure.
- **P9 Independent verification:** NOT EXECUTED.

Authorization is separate from predicate status. Freeze is separate from authorization. Merge is not freeze, and execution is not empirical validation.

## Semantic / ontological boundary control

DGAF permits agents and components to consume and reason over an approved ontology. They must not silently introduce, redefine, or assert ontology outside the authorized semantic layer.

The canonical semantic progression is **defined → observed → supported → verified → authorized → canonical**. Operational documentation must distinguish representation, classification, policy status, epistemic status, and ontological assertion. New semantic categories are candidate vocabulary until provenance and authorization establish canonical status. Agent repetition, confidence, or wording does not create semantic authority.

**Ontology drift** is a distinct semantic-drift class: an unauthorized change in effective vocabulary, entity boundaries, relations, or semantic commitments. The broader semantic-risk taxonomy is **definition drift, ontology drift, epistemic drift, policy drift, and provenance drift**.

Semantic/ontological detection is not automatically a blocking gate. A detector must be empirically characterized before threshold-bearing or gate-bearing use. This governance control does not advance P1–P9 or alter experimental state.

## Required next evidence events

1. Execute the full verification suite against `190a205002e9a9014005793a346324b5fb08ec76`.
2. Execute candidate-scoped P2 runtime verification and retain deployment identity, logs, and artifacts.
3. Verify P3 artifact schema, exact record/document identity binding, balanced matrix completeness, and sidecar integrity.
4. Verify deterministic retry/timing behavior after the clock correction.
5. Complete synthetic and operational blinding verification as applicable.
6. Establish durable evidence custody and direct retrieval/hash verification.
7. Reconcile topology fingerprints and environment identity on the exact candidate.
8. Complete formal P7 authority adoption and exact binding.
9. Lock P8 analysis implementation/configuration to the exact candidate and protocol identity.
10. Derive P1–P8 from candidate-scoped evidence.
11. Perform P9 independent verification.
12. Create a new immutable freeze and independently verify that exact freeze.
13. Obtain explicit pilot authorization.
14. Only then execute the authorized 50-seed blinded pilot.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
