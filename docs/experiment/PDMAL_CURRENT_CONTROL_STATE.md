---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_sha: 58ba9a072f40e94638b0332eeec19dd882a7ff95
applies_to_tree: abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb
selected_candidate_pr: 192
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
historical_runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
historical_runtime_deployment: dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc
candidate_status: SELECTED EXPERIMENTAL CANDIDATE / NOT FROZEN / PRE-FREEZE
pilot_authorization: NOT_GRANTED
empirical_n: 0
freeze_status: NOT_CREATED
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.

The selected experimental candidate is PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`, with exact tree `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`. It is the September 2 pre-freeze verification boundary and is not frozen.

The historical runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a` / tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`, with prior deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. Its P2/P6a evidence remains exact-scoped historical evidence and is not transferable to the selected candidate.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Selected experimental candidate | CURRENT / NOT FROZEN | PR #192 / `58ba9a…`; tree `abdbc9b…` |
| Exact candidate deployment | NOT ESTABLISHED | No READY Vercel deployment with recorded Git SHA `58ba9a…` |
| Candidate CI wave | 18/18 SUCCESS | Exact candidate workflows completed successfully |
| P-35 boundary | VERIFIED — ENGINEERING/PRE-FREEZE | Explicit checker dependency enforced in remediation and integrated into selected candidate |
| P2 runtime | OPEN / DEPLOYMENT-BOUND | Fresh authenticated 5-case matrix required on exact candidate deployment |
| P6a CORS | OPEN / DEPLOYMENT-BOUND | Fresh authenticated 4-case matrix required on same deployment |
| P3 | VERIFIED — ENGINEERING/CONTROL SCOPE | Current candidate CI, artifact, and instrumentation controls pass |
| P4 | OPEN | Current-cycle operational blinding/custody evidence required |
| P5 | VERIFIED — VERIFIER/TOOLCHAIN SCOPE | Candidate hashes, lock, package/toolchain and deterministic instrumentation retained; final closure remains open |
| P6 | OPEN / FAIL-CLOSED | Durable independent archive/retrieval/hash proof required |
| P7 | EXACT-CANDIDATE BINDING RECORDED PRE-FREEZE | Scientific target preserved; freeze identity not established |
| P8 | OPEN / FAIL-CLOSED | Current-candidate TGL/P-35, analysis, runtime, and operational predicates remain incomplete |
| P9 | OPEN | Fresh independent final-candidate verification required |
| New freeze | NOT CREATED | Candidate remains pre-freeze |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Current candidate evidence boundary

Candidate-bound evidence includes pre-freeze runner validation, governance evaluation evidence, freeze-control negative-state evidence, deterministic instrumentation dry-run output, exact candidate source hashes, dependency-lock/package fingerprints, and successful control-plane workflow completion.

The candidate evidence payloads may record GitHub's PR merge-ref execution identity (`fb1f4669…`) internally. That workflow identity is retained as execution provenance and is not substituted for candidate head `58ba9a…`.

## Current deployment boundary

The GitHub combined status for candidate `58ba9a…` reports Vercel `failure` at the provider build/deployment-rate-limit target. The latest Vercel deployment inventory contains READY deployments for other commits, but none whose recorded Git SHA equals `58ba9a072f40e94638b0332eeec19dd882a7ff95`.

Accordingly, no runtime result can currently be treated as candidate-closing P2/P6a evidence. In particular, prior P2/P6a evidence for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` does not transfer.

## Historical evidence boundary

Earlier completion-candidate, runtime, deployment, remediation, artifact, and P9 records remain preserved at their original scope. A historical document may call an older SHA current within its original temporal window; that wording must not be treated as a September 2 current control assertion.

The prior `92ff830b…` runtime evidence is retained as historical P2/P6a evidence. Prior `a43219b…` completion-candidate PDMAL/P9 evidence is likewise historical/non-transferable.

## P-35 control boundary

The selected candidate integrates the verified P-35 production boundary from PR #188. The control requires an explicit callable premise checker, propagates it through the DGAF/TGL/ConsensusTask path, and seals unexpected checker exceptions as `KILL`. This establishes an engineering control boundary; it does not itself define or approve a PDMAL-specific constitutional premise policy.

## Required closure sequence

1. Establish exact READY Vercel deployment with recorded Git SHA `58ba9a…`.
2. Execute authenticated P2 and P6a against that same deployment.
3. Complete current-cycle P4 and durable P6 evidence.
4. Preserve/complete exact P7 binding to the final protocol and analysis identity.
5. Close P8 from current-candidate evidence only.
6. Execute fresh independent P9 verification.
7. Create and independently verify a new immutable freeze.
8. Obtain explicit pilot authorization.
9. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, READY deployment for another SHA, historical verification result, repeated semantic audit, or engineering remediation does not create a new apparatus candidate or authorize scientific execution. Evidence must remain bound to its exact candidate/deployment/predicate scope.
