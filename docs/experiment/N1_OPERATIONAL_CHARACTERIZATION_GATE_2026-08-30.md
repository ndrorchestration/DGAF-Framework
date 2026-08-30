# N=1 Operational Characterization Gate — 2026-08-30

**Status:** EXECUTION GATE DEFINED / AUTHORIZATION STILL EXTERNAL

## Epistemic boundary

N=1 does **not** test or establish DGAF efficacy. It establishes only whether the **designated post-#151 candidate apparatus** can execute the specified PDMAL procedure end-to-end and produce a coherent, preserved, analyzable observation.

The candidate is **not frozen**. N=1 characterization does not imply that a later freeze will use the same identity if a substantive apparatus change occurs.

Implementation != Verification != Empirical Validation.

A successful N=1 observation must be classified as **Operationally Characterized**, not Proven, and not as evidence sufficient by itself for a causal efficacy claim.

## Candidate boundary

- Candidate apparatus SHA: `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`
- Candidate designation/control commit: `02c146d1e0cdc423948ac0dfa11e98f812edfb44`
- Candidate designation ref: `experimental-candidate/2026-08-30-post151`
- Prior candidate: `c6157158…` (superseded/pre-remediation provenance only)
- Prior P2/P6a evidence boundary: `303f4424…` (not transferable)
- Deployment: exact post-#151 deployment identity must be verified before P2/P6a closure
- Protocol: v0.7.5
- Primary contrast: `dgaf` versus `null`
- Primary endpoint: FFCR
- Analysis implementation: `experiments/pdmal_pilot/analysis.py`
- Artifact schema: `experiments/pdmal_pilot/pilot_artifact_schema.py`
- Runner: `experiments/pdmal_pilot/run_pilot.py`

## Required N=1 observation

Execute one bounded PDMAL synchronization run using the exact designated candidate apparatus and governing protocol. Preserve the complete raw output and integrity metadata. Do not modify the apparatus between execution and archival.

The N=1 run is a characterization run, not the 50-seed efficacy pilot and not a substitute for the preregistered statistical study.

## Minimum acceptance predicates

1. Exact candidate apparatus identity is recorded.
2. Execution uses the designated candidate apparatus without source modification.
3. The specified PDMAL execution completes or terminates under defined failure semantics.
4. Required artifact fields are emitted according to the bound schema.
5. Artifact integrity/hash is recorded.
6. Runtime/environment identity is recorded to the extent available.
7. Any failure, warning, omission, or anomaly is preserved rather than silently repaired.
8. The result is classified using the project's epistemic claim vocabulary.
9. No efficacy conclusion is derived from N=1.

## Authorization boundary

This document defines the characterization gate. It does not grant authorization. Authorization must be explicitly recorded by the responsible experiment authority before execution.

**Authorization:** NOT GRANTED BY THIS DOCUMENT
**Empirical N at creation:** 0

## Completion condition

This gate is complete only when one candidate-scoped N=1 execution artifact exists and has been durably preserved with the candidate identity and integrity metadata above.

Any candidate identity change caused by substantive apparatus modification resets the gate to the new candidate cycle.

**Current state:** Post-#151 candidate designated; deployment/source identity requires exact current verification; N=1 execution NOT RECORDED.
