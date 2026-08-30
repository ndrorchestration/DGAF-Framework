# R5–R7 Required-Gate Semantic Recovery Map — 2026-08-30

**Status:** READ-ONLY SEMANTIC RECOVERY COMPLETE / IMPLEMENTATION NOT YET AUTHORIZED
**Scope:** Seven constitutive gates of the canonical `dgaf` treatment
**Empirical N:** 0
**Pilot authorization:** NOT GRANTED

## Purpose

This record performs the minimum R1–R4 semantic determination required before any R5–R7 implementation work. It does not wire or modify the apparatus. It establishes what must be true before the seven required TGL gates may become candidate-bound experimental components.

## Governing evidence

The current PDMAL protocol defines the experimental `dgaf` condition as the full DGAF configuration and explicitly includes the DGAF adapter in the experimental scope. The canonical `TriadicGovernanceLoop.REQUIRED_STEPS` identifies steps 1, 2, 3, 4, 5, 6, and 8 as required. The PDMAL adapter turns a required skipped gate into `FAIL_CLOSED`. Therefore these seven gates are constitutive of the treatment definition, while fail-closed behavior is the correct behavior when a required semantic contract is unavailable.

## Gate-by-gate decision map

| Gate | Historical contract state | Current substrate evidence | Faithful translation status | R5 decision | R6/R7 prerequisite |
|---|---|---|---|---|---|
| P-31 SCPE | RECOVERED; historical semantics require reconciliation | `ConsensusState` provides agent values, alive state, topology/neighborhood state, failure history, iteration, and metrics | **NOT YET ESTABLISHED** | Do not wire until R2–R4 contract is explicit | Candidate-bound adapter + execution evidence |
| P-33 Convergence | RECOVERED; current task has an explicit convergence criterion, but historical gate contract must be distinguished from task endpoint | `current_final_std`, values, iteration and topology state are available | **PARTIALLY ESTABLISHED; CONTRACT RECONCILIATION REQUIRED** | Preserve existing task convergence semantics; do not equate endpoint threshold with historical gate semantics without proof | Candidate-bound gate + deterministic boundary tests |
| DemiJoule | RECOVERED in canonical TGL slot; historical payload semantics require reconciliation | Numeric consensus state alone is not sufficient evidence for historical DemiJoule payload semantics | **NOT ESTABLISHED** | FAIL_CLOSED pending explicit loss analysis; no numeric proxy substitution | Explicit adapter contract + candidate-bound tests |
| P-27 KAPPA | RECOVERED; historical routing contract requires reconciliation | `active_neighbors`, `original_neighbors`, failure state, values available; no proof yet that these preserve historical KAPPA semantics | **NOT YET ESTABLISHED** | No wiring until semantic mapping is explicit | Adapter + invariants + adversarial routing tests |
| P-29 Sentinel | RECOVERED; historical risk-pass contract requires reconciliation | Current state provides alive/failure/topology/metrics context | **NOT YET ESTABLISHED** | No wiring until historical risk semantics are recovered | Adapter + failure-path tests + candidate binding |
| P-32 Phi Closure | RECOVERED; historical closure/statefulness requires reconciliation | `failure_history`, iteration, values and metrics exist, but lossless historical mapping is not established | **NOT YET ESTABLISHED** | FAIL_CLOSED pending explicit contract | Adapter + stateful sequence tests + provenance |
| P-30 Apogee | PARTIAL recovery; historical attestation semantics require reconciliation | Current turn audit and state context exist; no proof of lossless Apogee semantics | **NOT YET ESTABLISHED** | No wiring until semantics are explicit | Adapter + attestation-boundary tests |

## Important negative findings

1. The existence of `ConsensusState` fields does not establish semantic equivalence with historical gate inputs.
2. A numerically convenient mapping (for example `current_final_std` into multiple historical gates) is not accepted without an explicit contract.
3. Historical validation claims do not transfer to the current candidate.
4. Unit tests of the adapter do not establish candidate-bound verification.
5. Fail-closed is the default whenever a faithful mapping cannot be established.

## R5 implementation boundary

R5 is authorized only after the gate contract for a specific component is sufficiently explicit to answer all of the following:

- What historical input does the gate require?
- What current `ConsensusState` fields supply that input?
- What information is lost?
- Does the transformation change semantics?
- What invariants must remain true?
- What output/failure behavior is required?
- What deterministic test vectors establish the adapter contract?

Where the answer to the semantic-change question is "yes" or "unknown", the gate remains FAIL_CLOSED and is not wired as though historical behavior had been restored.

## Candidate-cycle consequence

Any R5 implementation that changes executable apparatus semantics creates a **new experimental candidate cycle**. The implementing commit cannot inherit P3–P9 evidence from `c6157158…` or any earlier apparatus identity.

Required sequence after implementation:

`implementation` → `candidate designation` → `fresh P2/P6a and relevant P3–P8 evidence` → `independent P9` → `freeze` → `authorization`.

## Anti-trap constraint

This map is intentionally limited to the seven gates established as constitutive by the canonical `dgaf` execution contract. It does not authorize reconstruction of HPG, Herald, or unrelated historical governance mechanisms.

No additional pre-N=1 prerequisite may be added unless it is demonstrated to affect treatment identity or observation interpretability.

## Current disposition

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**

The R1–R4 semantic determination does not yet justify wiring any of the seven gates based solely on the current substrate fields. The next work is gate-specific historical contract extraction and contradiction reconciliation, followed by an explicit adapter contract only where semantic fidelity can be demonstrated.
