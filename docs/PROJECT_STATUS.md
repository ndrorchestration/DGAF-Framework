# DGAF/PDMAL Project Status

**Status date:** 2026-09-05  
**Documentation-hygiene reconciliation source boundary:** `a3bafa6fca8599df479a685828f5fdddb6bae589`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Designated executable runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Candidate deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Pilot status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED  
**Empirical N:** 0

## Executive state

DGAF is in pre-freeze closure. The designated runtime candidate and its deployment remain distinct from later documentation, evaluator, and control-plane commits.

P1, P2, P3, P5, P6, and P6a are closed/verified within their explicitly bounded engineering/governance evidence contracts. P4 remains operationally open because no admissible H/I/T custody mode has been instantiated and verified. P7 final binding, P8 immutable freeze/readiness, final P9, freeze establishment, and authorization remain open or absent.

PR #286 removed an unnecessary mandatory-second-human dependency by redefining P4 around effective control separation; it did not close P4. Issue #287 now carries the threat-model/design work for a possible zero-human Mode T lifecycle and must not be treated as evidence that such a mechanism is already accepted.

None of these engineering states establishes empirical efficacy.

## Gate board

| Gate / control | Status | Evidence / limitation |
|---|---|---|
| Corrected apparatus provenance | CANONICAL ANCHOR | `2a54a67d…` |
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| P1 | CLOSED / VERIFIED | exact apparatus/candidate/tree and scoped deployment identity |
| P2 | CLOSED / VERIFIED | run `33730195621`; retrievable artifact `9883521704`; exact runtime predicates only |
| P3 | CLOSED / VERIFIED | run `33939955138`; artifact-contract evidence |
| P4 | OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED | H/I/T custody architecture defined; no real custody instance verified |
| P5 | CLOSED / VERIFIED | provenance/reproducibility and exact analysis-control identity binding; not efficacy evidence |
| P6 | CLOSED / VERIFIED | defined external archive/retrieval/SHA-256 equality contract |
| P6a | CLOSED / VERIFIED | run `33728695806`; retrievable artifact `9882965299`; exact CORS predicates only |
| P7 | ADOPTED / FINAL BINDING OPEN | final scientific/pre-freeze identity chain incomplete |
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

## P4 custody state

The canonical P4 control is now effective control separation rather than a mandatory two-human topology:

- `H`: genuinely distinct human custody;
- `I`: institutional/third-party custody outside the analyst's unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

Issue #285 is completed as the governance-architecture correction. Issue #255 is superseded historical context. No H/I/T execution instance exists yet, so P4-A remains OPEN / NOT EXECUTED.

Issue #287 is a design/threat-model lane for a possible solo Mode T lifecycle. It explicitly does not establish that GitHub-hosted runners, timelock encryption, drand, or any other candidate mechanism already satisfies P4.

## Evaluation-integrity update

PR #269 merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` after all returned exact-head workflows succeeded. Task 4 (`audit_hallucination_rate`) now fails closed without provenance-controlled ground truth plus independently generated corresponding outputs and uses deterministic six-field comparison rather than baseline-derived/random scoring.

This establishes evaluator mechanics only. No Task-4 model-performance result exists.

## Engineering-quality state

Issue #270 is **CLOSED / COMPLETED**. Its remediation restored a clean current-lineage flake8/Black/isort/mypy baseline and converted those checks to fail-closed workflow gates. The exact remediation evidence includes successful Python 3.10/3.11/3.12 matrix execution and deterministic negative controls that intentionally trigger each primary quality tool.

Issue #277 remains **OPEN** for branch-protection/ruleset enforcement. The quality workflow itself is fail-closed when run, but repository configuration readback did not establish that the Python matrix is required before every merge. That repository-administration gap is separate from the repaired code/workflow quality baseline.

## Mathematical hygiene state

Current PDMAL mathematical authority distinguishes:

- `ρ ≈ 1.3247179572447454` as the plastic constant, the real root of `x³=x+1`;
- `pP = 1/(2 sin(π/11)) ≈ 1.774732842` as DGAF-specific Platinum Mean notation.

The exact Cheeger constant for the dodecahedral base graph is `0.6`. Unweighted Forman–Ricci curvature is `-2` on every edge, so it currently carries no discriminating audit signal until meaningful weights are defined. These are formalization/engineering facts, not empirical efficacy results.

## Reconciliation interpretation

The immutable boundary `a3bafa6f…` is the source state used for this hygiene reconciliation. It is not labeled “current main” inside the file because the file's own commit must be a later descendant. This status record also does not claim that candidate-scoped runtime/deployment evidence automatically transfers to later repository descendants.

Historical Vercel quota incidents, stale quality findings, and previous custody assumptions remain historical to their affected SHAs and records unless freshly re-observed or explicitly promoted.

## Evidence boundary

Evidence remains exact-candidate, workflow, artifact, deployment, and predicate scoped. Documentation-only control-plane changes neither reopen valid exact-scope evidence nor inherit it automatically. Archive/retrieval digest equality does not establish empirical efficacy or independent custody.

## Required closure sequence

`verified real P4-A custody mode → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
