# DGAF/PDMAL Project Status

**Status date:** 2026-09-05  
**Repository reconciliation base:** `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Designated executable runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Candidate deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Pilot status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED  
**Empirical N:** 0

## Executive state

DGAF is in pre-freeze closure. The designated runtime candidate and its deployment remain distinct from later documentation, evaluator, and control-plane commits.

P1, P2, P3, P5, P6, and P6a are closed/verified within their explicitly bounded engineering/governance evidence contracts. P4 remains operationally open because real distinct-human production-key custody/access separation has not been executed/evidenced. P7 final binding, P8 immutable freeze/readiness, final P9, freeze establishment, and authorization remain open or absent.

None of these engineering states establishes empirical efficacy.

## Gate board

| Gate / control | Status | Evidence / limitation |
|---|---|---|
| Corrected apparatus provenance | CANONICAL ANCHOR | `2a54a67d…` |
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| P1 | CLOSED / VERIFIED | exact apparatus/candidate/tree and live deployment identity |
| P2 | CLOSED / VERIFIED | run `33730195621`; retrievable artifact `9883521704`; exact runtime predicates only |
| P3 | CLOSED / VERIFIED | run `33939955138`; artifact-contract evidence |
| P4 | OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED | synthetic blinding behavior exists; real custody/access separation absent |
| P5 | CLOSED / VERIFIED | provenance/reproducibility and exact analysis-control identity binding; not efficacy evidence |
| P6 | CLOSED / VERIFIED | defined external archive/retrieval/SHA-256 equality contract |
| P6a | CLOSED / VERIFIED | run `33728695806`; retrievable artifact `9882965299`; exact CORS predicates only |
| P7 | ADOPTED / FINAL BINDING OPEN | final scientific/freeze identity chain incomplete |
| P8 | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance transition |
| Empirical data | N = 0 | no authorized pilot execution |

## Current execution evidence

On 2026-09-05, both candidate-scoped runtime evidence records were successfully re-retrieved:

- P2 artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

This is not a new runtime execution.

Current-candidate P3/P5 evidence is retained from run `33939955138`. Synthetic P4 evidence is retained from run `33939574283`. The P6 round-trip record covers the finalized evidence sets within its defined byte-equality scope.

P5 closure is further bounded by the current canonical control record: analysis implementation/configuration/runner/schema identities and deterministic provenance/reproducibility controls are fixed and verified. This does not establish efficacy.

## Evaluation-integrity update

PR #269 merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` after all returned exact-head workflows succeeded. Task 4 (`audit_hallucination_rate`) now fails closed without provenance-controlled ground truth plus independently generated corresponding outputs and uses deterministic six-field comparison rather than baseline-derived/random scoring.

This establishes evaluator mechanics only. No Task-4 model-performance result exists.

## Current engineering-quality finding

Issue #270 records later-lineage Black/isort/mypy debt observed in Python Tests & Quality Checks run `33957199893`. Those diagnostics are currently `continue-on-error`, so workflow SUCCESS must not be represented as a clean formatting/type baseline. Blocking pytest passed across Python 3.10/3.11/3.12 for the PR #269 execution.

## Current-main interpretation

The reconciliation base `17fbe054…` is a later evaluator/control-plane descendant. This status document does not claim that candidate-scoped runtime/deployment evidence automatically transfers to repository `main`, nor does it require every documentation descendant to be separately production-deployed to preserve valid candidate-scoped evidence.

Historical Vercel quota incidents remain historical to their affected SHAs and are not represented as the current repository state unless freshly re-observed.

## Evidence boundary

Evidence remains exact-candidate, workflow, artifact, deployment, and predicate scoped. Documentation-only control-plane changes neither reopen valid exact-scope evidence nor inherit it automatically. Archive/retrieval digest equality does not establish empirical efficacy or independent human control.

## Required closure sequence

`real P4 custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
