# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Status date:** 2026-09-01  
**Controlled candidate:** `566273c6c2906bdf71827381493a26ee7697034c`  
**PR:** #187 (draft; unmerged)  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is the current planning/control surface. It does not itself constitute executed experimental evidence. Historical evidence remains exact-SHA/run/artifact/deployment scoped. No evidence from a superseded candidate is inherited automatically.

## Predicate matrix

| Predicate | Current state | Current closure requirement |
|---|---|---|
| P1 Candidate Integrity | **OPEN** | Final apparatus/candidate identity and provenance must be reconciled and retained |
| P2 Execution Contract / Runtime | **OPEN** | Fresh authenticated five-case runtime matrix bound to the exact candidate and deployment |
| P3 Artifact Contract | **OPEN** | Fresh exact-candidate schema, identity, uniqueness, balance, canonical-matrix, and deviation evidence |
| P4 Security / Blinding | **OPEN** | Fresh custody, bijection, access separation, and operational procedure evidence |
| P5 Provenance / Reproducibility | **OPEN** | Fresh exact-candidate execution proving RNG separation, determinism, environment/toolchain, and artifact binding |
| P6 Durable Evidence Custody | **OPEN** | Current evidence archived, independently retrieved, and hash-verified |
| P6a Runtime/CORS | **OPEN** | Fresh authenticated four-case CORS matrix bound to the exact candidate/deployment |
| P7 Scientific Target | **OPEN / EXTERNAL DECISION** | Scientific decision must be explicitly bound to final candidate/protocol/analysis/freeze identity |
| P8 Analysis Lock | **OPEN / FAIL-CLOSED** | All applicable prerequisites and analysis/schema/runner/protocol bindings must be evidenced on the current candidate |
| P9 Independent Verification | **OPEN** | Independent verifier must execute successfully on the current candidate and bind run/artifact evidence |

## Current implementation evidence

The controlled candidate implements or exercises the following verification machinery:

- exact `HEAD == GITHUB_SHA` identity checking;
- deterministic PDMAL structural/instrumentation dry-run checks;
- P5 RNG-stream separation and repeated-case digest checks;
- independent P9 `jq -S -c` canonicalization and `sha256sum` comparison;
- exact-candidate authority-identity regression;
- artifact upload/download/checksum custody;
- completion-controller reconciliation of candidate, workflow run, artifact ID, and artifact digest;
- fail-closed baseline registry synthesis when exact evidence is absent;
- structured predicate-evidence handling in the completion controller.

These implementation capabilities do not by themselves close P3–P9.

## Latest verification event

The latest candidate-bound PDMAL run passed the substantive deterministic structural tests, artifact generation/custody checks, and registry generation. Its final one-seed structural dry-run step then failed because the embedded Python command has malformed shell quoting (the command is missing its terminating quote). This is classified as a **CI implementation defect**, not experimental failure.

The required response is a narrowly scoped repair that creates a new candidate and reruns the complete candidate-bound chain. The prior candidate's evidence remains historical.

## Superseded candidate boundary

The immediately preceding exact-candidate cycle was `cea9e49deb6738f29deefa95b1357b8c1663b6b3`. It produced candidate-bound P9/PDMAL evidence, but the subsequent controller correction created `566273c6…`. No P9/PDMAL/P3–P6 closure may be inferred for `566273c6…` from those artifacts.

## Historical controls

- **E2b:** CLOSED / VERIFIED within its historical exact execution boundary; not automatically current-candidate evidence.
- **M6:** CLOSED / VERIFIED within its historical exact candidate boundary; not automatically current-candidate evidence.

## Evidence inheritance rule

Evidence may be used for historical lineage or diagnostic comparison, but current closure requires exact-scope identity. At minimum, the relevant claim must bind the source/candidate SHA and, where applicable, workflow run, deployment identity, artifact ID, and artifact digest. Cross-candidate copying or manual status promotion is prohibited.

## Critical path

1. Repair the PDMAL CI quoting defect and create a new candidate.
2. Re-run PDMAL instrumentation and P9 on that exact SHA.
3. Reconcile P3–P6/P9 evidence without transfer.
4. Execute authenticated P2/P6a against the exact deployment identity.
5. Complete P4/P5/P6 current-cycle evidence.
6. Resolve P7 as the external scientific decision and bind it exactly.
7. Close P8 only from current-candidate evidence.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the authorized blinded pilot.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
