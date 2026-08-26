---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-25
applies_to_sha: 39c138bb29697a561b49ef206c9f9a185e8a9c7b
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment that produced it. This document describes current state without retroactively transferring historical evidence.

## Authoritative current state

|| Gate / boundary | Status | Current meaning |
|---|---|---|
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` remains provenance only for the corrected apparatus |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Panel-ready record (`P7_ADJUDICATION_RECORD_PANEL_READY_2026-08-23.md`) presents 11 proposed decisions all OPEN / PENDING AUTHORITY ADOPTION; primary contrast (DGAF vs null) selected but formal adoption not evidenced; see `P7_SCIENTIFIC_SPECIFICATION_TRACEABILITY_MATRIX.md` |
| P8 analysis lock | OPEN / FAIL-CLOSED | Implementation and controls exist, but executed candidate-scoped verification is incomplete |
| Exact verification candidate | IDENTIFIED | `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is the candidate tree named by the current P8 checklist |
| New immutable freeze | NOT CREATED | Candidate has not yet crossed the freeze boundary |
| Operational evidence closure | INCOMPLETE | Durable retention, candidate-scoped runtime evidence, and remaining custody/provenance checks require closure |
| P9 independent verification | NOT EXECUTED | Downstream of candidate evidence closure |
| Pilot authorization | NOT GRANTED | Separate governance transition after required predicates and freeze verification |
| Empirical data | N = 0 | No authorized empirical pilot has been executed |

## Candidate identity boundary

The P8 verification checklist identifies `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` as the exact candidate tree for verification. Later documentation-only commits do not silently redefine that apparatus. Any substantive apparatus change requires a new candidate identity and re-verification.

Historical SHA references, including earlier PR #77 and pre-correction P8 bindings, remain provenance where they describe what was actually examined; they are not current-state assertions.

## Canonical predicate state

- **P1 Candidate integrity:** PARTIAL — candidate exists; executed candidate evidence still required.
- **P2 Execution contract:** PARTIAL — implementation controls exist; current runtime evidence remains incomplete.
- **P3 Artifact contract:** PARTIAL — executable contract is strengthened; candidate-scoped verification remains required.
- **P4 Security / blinding integrity:** PARTIAL — controls and synthetic evidence exist; operational custody boundary remains to be fully evidenced.
- **P5 Provenance / reproducibility:** PARTIAL — bindings exist; candidate-scoped reproduction and environment evidence remain incomplete.
- **P6 Durable evidence custody:** OPEN — durable archive plus independent retrieval/hash evidence remains required.
- **P7 Scientific target specification:** TECHNICALLY ADJUDICATED / FORMALLY OPEN — the panel-ready record presents all 11 scientific decisions as OPEN / PENDING AUTHORITY ADOPTION; the primary contrast (DGAF vs null) has been selected but formal authority adoption is not evidenced; must remain traceable to the authoritative adjudication record and protocol before P8 closure claims scientific closure.
- **P8 Analysis lock:** OPEN / FAIL-CLOSED — no closure by implementation presence alone.
- **P9 Independent verification:** NOT EXECUTED.

Authorization is separate from predicate status. Freeze is separate from authorization. Merge is not freeze, and execution is not empirical validation.

## Current documentation and hygiene rules

1. Current-state assertions must identify the current candidate or explicitly say that a SHA is historical.
2. Historical evidence must retain the SHA/run/deployment actually examined.
3. Status documents cannot create closure by assertion; closure requires the evidence specified by the relevant predicate.
4. A frozen candidate tree is immutable. Later documentation corrections may clarify the record but do not rewrite the frozen apparatus.
5. P7 adoption, P8 implementation, freeze, authorization, execution, and empirical efficacy are distinct state transitions.
6. The current empirical boundary remains **N = 0** and no efficacy claim is authorized.

## Required next evidence events

1. Execute the applicable CI/test hierarchy against exact candidate `2a80f819...` and retain run IDs, logs, artifacts, and executed-tree identity.
2. Complete candidate-scoped P8 verification, including analysis, artifact, schema/security, compilation, provenance, determinism, and environment checks as applicable.
3. Establish durable evidence retention and independently verify retrieval and integrity.
4. Complete remaining operational blinding custody and runtime-dependent verification according to explicit applicability/fallback rules.
5. Derive and evidence P1–P8 from the exact candidate; do not infer closure from configuration alone.
6. Create an immutable freeze only after required pre-freeze predicates are satisfied.
7. Execute independent/adversarial verification against the frozen candidate.
8. Make a separate authorization decision.
9. Only then execute the blinded empirical pilot and proceed to formal unblinding and locked analysis.

**No empirical pilot execution is authorized. Empirical N remains 0. Authorization remains NOT GRANTED.**
