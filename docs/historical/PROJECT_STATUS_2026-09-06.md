# DGAF/PDMAL Project Status

**Status date:** 2026-09-06  
**v0.7.6 apparatus-introduction boundary:** `972edd41f16c69c6912af08c7d6c3aa627fdd8a9` (not current `main`)
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Historical runtime-evidence candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Historical candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Historical candidate deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Final v0.7.6 candidate:** NOT DESIGNATED — tracked by Issue #309  
**Pilot status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED  
**Empirical N:** 0

> **Historical snapshot notice:** This file preserves the 2026-09-06 project-status snapshot. It is not current authority after later Track A preflight, freeze, closure, verification, collection, dataset-lock, and unblinding-authorization work. Use `../CURRENT_STATE.md` for current status.

## Candidate-authority reconciliation

PR #308 changed the experimental apparatus to protocol v0.7.6 / artifact schema 1.1 at `972edd41…`. The prior `7c1cc4bb…` runtime candidate retains valid exact-scope evidence but is historical provenance for final-candidate purposes and is not eligible to become the final freeze/N=1 candidate. Issue #309 is the convergence authority for explicitly selecting an exact immutable v0.7.6 descendant and classifying or regenerating only the evidence that is identity-dependent.

The consolidated control-state anchor `89be386b…` remains valid for its control/provenance role; it does not designate the final candidate.

## Executive state

DGAF is in pre-freeze closure. Historical P1, P2, P3, P5, P6, and P6a results remain closed/verified within their explicitly bounded engineering/governance evidence contracts for `7c1cc4bb…`; they do not automatically close those predicates for the future final candidate. PR #326 integrated the validated Mode-T engineering mechanism stack, but P4 remains operationally open because no admissible H/I/T custody mode has been independently accepted and executed for the final run. P7 final binding, P8 immutable freeze/readiness, final P9, freeze establishment, and authorization remain open or absent.

None of these engineering states establishes empirical efficacy.

## Gate board

| Gate / control | Status | Evidence / limitation |
|---|---|---|
| Corrected apparatus provenance | CANONICAL ANCHOR | `2a54a67d…` |
| Consolidated control-state anchor | CANONICAL CONTROL/PROVENANCE ANCHOR | `89be386b…`; not a final-candidate designation |
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Historical P1 | CLOSED / VERIFIED | exact `7c1cc4bb…` apparatus/candidate/tree and scoped deployment identity; final-candidate transfer/reverification pending #309 |
| Historical P2 | CLOSED / VERIFIED | run `33730195621`; retrievable artifact `9883521704`; exact runtime predicates only; final-candidate transfer/reverification pending #309 |
| Historical P3 | CLOSED / VERIFIED | run `33939955138`; artifact-contract evidence; final-candidate transfer/reverification pending #309 |
| P4 | OPEN / FAIL-CLOSED | Mode-T mechanisms integrated by #326; no real admissible custody instance independently accepted/executed |
| Historical P5 | CLOSED / VERIFIED | provenance/reproducibility and exact analysis-control identity binding for pre-v0.7.6 candidate; final-candidate transfer/reverification pending #309 |
| Historical P6 | CLOSED / VERIFIED | defined external archive/retrieval/SHA-256 equality contract; final-candidate rebind decision pending #309 |
| Historical P6a | CLOSED / VERIFIED | run `33728695806`; retrievable artifact `9882965299`; exact CORS predicates only; final-candidate transfer/reverification pending #309 |
| Final v0.7.6 candidate | NOT DESIGNATED | Issue #309 |
| P7 | ADOPTED / FINAL BINDING OPEN | final scientific/pre-freeze identity chain incomplete |
| P8 | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance transition |
| Empirical data | N = 0 | no authorized pilot execution |

## Current execution evidence

On 2026-09-05, both `7c1cc4bb…`-scoped runtime evidence records were successfully re-retrieved:

- P2 artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

This is not a new runtime execution.

Historical-candidate P3/P5 evidence is retained from run `33939955138`. Synthetic P4 evidence is retained from run `33939574283`. The P6 round-trip record covers the finalized evidence sets within its defined byte-equality scope.

## P4 custody state

The canonical P4 control is now effective control separation rather than a mandatory two-human topology:

- `H`: genuinely distinct human custody;
- `I`: institutional/third-party custody outside the analyst's unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

No real H/I/T custody instance had been independently accepted and executed for the final High-Assurance run at the time of this snapshot, so P4-A remained OPEN / FAIL-CLOSED.

## Evaluation-integrity update

PR #269 merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` after all returned exact-head workflows succeeded. Task 4 (`audit_hallucination_rate`) now fails closed without provenance-controlled ground truth plus independently generated corresponding outputs and uses deterministic six-field comparison rather than baseline-derived/random scoring.

This establishes evaluator mechanics only. No Task-4 model-performance result exists.

## Engineering-quality state

Issue #270 was CLOSED / COMPLETED. Its remediation restored a clean current-lineage flake8/Black/isort/mypy baseline and converted those checks to fail-closed workflow gates.

## Mathematical hygiene state

Current PDMAL mathematical authority at the time distinguished:

- `ρ ≈ 1.3247179572447454` as the plastic constant, the real root of `x³=x+1`;
- `pP = 1/(2 sin(π/11)) ≈ 1.774732842` as DGAF-specific Platinum Mean notation.

The exact Cheeger constant for the dodecahedral base graph is `0.6`. Unweighted Forman–Ricci curvature is `-2` on every edge. These are formalization/engineering facts, not empirical efficacy results.

## Evidence boundary

Evidence remains exact-candidate, workflow, artifact, deployment, protocol/schema, and predicate scoped. Documentation-only control-plane changes neither reopen valid exact-scope evidence nor inherit it automatically.

## Required closure sequence at the time of this snapshot

`complete candidate-relevant P4 apparatus work → explicitly designate exact v0.7.6 final candidate under #309 → classify/regenerate identity-dependent evidence → verified real P4-A custody mode → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

**Current experimental state at the time of this snapshot: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
