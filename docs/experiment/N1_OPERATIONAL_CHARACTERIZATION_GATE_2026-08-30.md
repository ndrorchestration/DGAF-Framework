# N=1 Operational Characterization Gate — 2026-08-30

**Status:** EXECUTION GATE DEFINED / AUTHORIZATION STILL EXTERNAL

## Purpose

This gate deliberately separates a minimum viable N=1 operational characterization from the later full scientific pilot. Its purpose is to establish whether the **designated post-#151 candidate apparatus** can execute the specified PDMAL procedure end-to-end without conflating characterization with efficacy.

## Epistemic boundary

N=1 does **not** test or establish DGAF efficacy. It establishes only whether the designated candidate apparatus can execute the specified PDMAL procedure end-to-end and produce a coherent, preserved, analyzable observation.

Implementation != Verification != Empirical Validation.

A successful N=1 observation is **Operationally Characterized**, not Proven, and not evidence sufficient by itself for a causal efficacy claim.

## Candidate boundary

- Apparatus / candidate source SHA: `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
- Candidate designation/control commit: `02c146d1e0cdc423948ac0dfa11e98f812edfb44` (control record only; not apparatus identity)
- Current documentation lineage: `main` (resolve directly)
- Prior candidate: `c6157158…` — superseded pre-remediation
- Prior runtime evidence boundary: `303f4424…` — historical P2/P6a scope only
- Deployment: **TO BE VERIFIED FOR EXACT POST-#151 CANDIDATE** before current-candidate runtime closure
- Protocol: v0.7.5
- Primary contrast: `dgaf` versus `null`
- Primary endpoint: FFCR
- Analysis implementation: `experiments/pdmal_pilot/analysis.py`
- Artifact schema: `experiments/pdmal_pilot/pilot_artifact_schema.py`
- Runner: `experiments/pdmal_pilot/run_pilot.py`

## Required N=1 observation

Execute one bounded PDMAL synchronization run using the exact designated candidate apparatus and governing protocol. Preserve the complete raw output and its integrity metadata. Do not modify the apparatus between execution and archival.

The N=1 run is a characterization run, not the 50-seed efficacy pilot and not a substitute for the preregistered statistical study.

## Minimum acceptance predicates

1. Exact candidate identity is recorded.
2. Execution uses the designated candidate apparatus without source modification.
3. The specified PDMAL execution completes or terminates under its defined failure semantics.
4. Required artifact fields are emitted according to the bound schema.
5. Artifact integrity/hash is recorded.
6. Runtime/environment identity is recorded to the extent available.
7. Any failure, warning, omission, or anomaly is preserved rather than silently repaired.
8. The result is classified using the project's epistemic claim vocabulary.
9. No efficacy conclusion is derived from N=1.

## Non-blocking work

The following are explicitly not prerequisites for this bounded N=1 characterization unless they directly make the observation uninterpretable:

- Phi-calculus refinement;
- README/public presentation refinement;
- grant prospecting or narrative development;
- exhaustive comparative-baseline research;
- additional governance layers invented after this gate;
- expansion of the empirical sample beyond N=1;
- perfection of the full independent-verification architecture.

## Blocking defects

A defect may block N=1 only when it prevents the specified observation from being interpreted, for example:

- candidate identity cannot be established;
- the runner cannot execute the defined procedure;
- required outputs cannot be distinguished from missing outputs;
- artifact integrity cannot be preserved;
- the execution path differs materially from the specified candidate;
- a known control-plane failure invalidates the intended observation.

Discovery of a blocking defect does not authorize unrelated architectural expansion. Repair must be narrowly scoped to the blocking predicate, followed by candidate re-identification and re-verification as required.

## Claim vocabulary

Use only these classifications in the resulting record:

- **Observed** — directly present in the run artifact/log.
- **Verified** — independently or procedurally checked against a defined predicate.
- **Operationally Characterized** — demonstrated by bounded execution without implying efficacy.
- **Inferred** — supported interpretation that exceeds direct observation.
- **Hypothesized** — proposed explanation or expected effect.
- **Planned** — future intended activity.
- **Not Established** — claim for which the available evidence is insufficient.

## Authorization boundary

This document defines the execution gate. It does not itself grant authorization. Authorization must be explicitly recorded by the responsible experiment authority before execution.

**Authorization:** NOT GRANTED BY THIS DOCUMENT
**Empirical N at creation:** 0

## Completion condition

This gate is complete only when one candidate-scoped N=1 execution artifact exists and has been durably preserved with the candidate identity and integrity metadata above.

**Current state:** Post-#151 candidate designated; deployment identity requires exact verification; N=1 execution NOT RECORDED.
