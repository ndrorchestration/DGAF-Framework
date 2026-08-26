---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: e6beeb66335e1b50a239697badab22dab50eb5ba
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

> **Current boundary:** `e6beeb66335e1b50a239697badab22dab50eb5ba` remains the executable verification candidate. Commit `93b10d084ddb563d88b11818baad8b40565cb0ce` adds the preauthorization negative-control matrix as documentation only and does **not** advance the apparatus candidate. The candidate remains pre-freeze; P7 is technically adjudicated but formally open; P8 remains open/fail-closed; empirical **N = 0**; authorization is not granted.

## Authoritative current state

| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Scientific decisions are resolved; authority adoption and exact binding remain open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Corrective implementation work is present; candidate-scoped runtime and binding evidence remain incomplete |
| Exact verification candidate | IDENTIFIED (corrected) | `e6beeb66335e1b50a239697badab22dab50eb5ba` is the executable candidate |
| Documentation successor | NON-APPARATUS | `93b10d084ddb563d88b11818baad8b40565cb0ce` adds negative-control documentation only |
| New immutable freeze | NOT CREATED | Candidate has not crossed the freeze boundary |
| Operational evidence closure | INCOMPLETE | P2/P6a execution, durable custody, and independent provenance evidence remain open |
| P9 independent verification | NOT EXECUTED | Downstream of candidate evidence closure |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## Candidate transition record

`83e1678f...` was the earlier corrected candidate. Subsequent executable fixes changed the verification surface, producing `e6beeb66335e1b50a239697badab22dab50eb5ba` as the current executable candidate. Later documentation-only commits must not be treated as apparatus changes.

### Documentation-only successor

- `93b10d084ddb563d88b11818baad8b40565cb0ce` — adds `docs/evidence/NEGATIVE_CONTROL_MATRIX.md`; documentation-only; does not change executable apparatus.

## Canonical predicate state

- **P1 Candidate integrity:** PARTIAL — current candidate identified; final candidate-scoped reconciliation required.
- **P2 Execution contract:** PARTIAL — formal P2 runtime verification remains outstanding.
- **P3 Artifact contract:** PARTIAL — integrity controls implemented; candidate-scoped artifact execution remains required.
- **P4 Security / blinding integrity:** PARTIAL — controls exist; operational custody evidence remains incomplete.
- **P5 Provenance / reproducibility:** PARTIAL — candidate identity is preserved across documentation successor; final environment fingerprint remains required.
- **P6 Durable evidence custody:** OPEN — durable archive plus independent retrieval/hash evidence remains required.
- **P7 Scientific target specification:** TECHNICALLY ADJUDICATED / FORMALLY OPEN — authority adoption and exact binding remain required.
- **P8 Analysis lock:** OPEN / FAIL-CLOSED — implementation presence is not closure.
- **P9 Independent verification:** NOT EXECUTED.

## Semantic / ontological boundary control

DGAF permits agents and components to consume and reason over an approved ontology. They must not silently introduce, redefine, or assert ontology outside the authorized semantic layer.

The canonical semantic progression is **defined → observed → supported → verified → authorized → canonical**. Operational documentation must distinguish representation, classification, policy status, epistemic status, and ontological assertion. New semantic categories are candidate vocabulary until provenance and authorization establish canonical status. Agent repetition, confidence, or wording does not create semantic authority.

**Ontology drift** is a distinct semantic-drift class: an unauthorized change in effective vocabulary, entity boundaries, relations, or semantic commitments. The broader semantic-risk taxonomy is **definition drift, ontology drift, epistemic drift, policy drift, and provenance drift**.

Semantic/ontological detection is not automatically a blocking gate. A detector must be empirically characterized before threshold-bearing or gate-bearing use.

## Required next evidence events

1. Execute authenticated P2 against the exact READY deployment for `e6beeb...`.
2. Execute P6a CORS against the same deployment identity.
3. Complete P4 operational blinding/custody verification.
4. Complete P6 durable archive/retrieval/hash evidence.
5. Complete P5 environment fingerprint/reproducibility evidence.
6. Complete P7 authority adoption and exact cryptographic binding.
7. Freeze canonical protocol, artifact schema, endpoints, baselines, negative controls, and statistical analysis plan.
8. Reconcile P1–P8 from candidate-scoped evidence.
9. Perform P9 independent verification.
10. Create and verify a new immutable freeze.
11. Obtain explicit pilot authorization.
12. Only then execute the authorized blinded pilot.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
