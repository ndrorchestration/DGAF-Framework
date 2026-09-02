---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_sha: 92ff830b1c67413df745e37087d6447c9c251b9a
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
candidate_status: CURRENT RUNTIME CANDIDATE / NOT FROZEN / P3-P8 EVIDENCE REMAINING
active_p35_remediation_head: d83ea74c0f7ef7dd3e39a25345d6b201770a370c
active_p35_pre_freeze_run: 33590352168
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It is the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.

The current production/runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a`, with exact tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. Git history establishes the corrected apparatus source as its lineage basis. These identities remain distinct: apparatus provenance is not the same thing as executable candidate identity.

The active P-35 remediation is a separate engineering lineage: PR #188 / branch `remediation/p35-premise-hook-2026-09-01`, current head `d83ea74c0f7ef7dd3e39a25345d6b201770a370c`. Its exact-head pre-freeze runner validation passed in run `33590352168`, but that remediation head is not the current runtime candidate and does not inherit or transfer runtime evidence.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` is provenance only |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…`; seven restored gate-state substrates bound |
| Apparatus tree | IDENTIFIED | `973c92335caf84f37fc2b3c4df6dd83b3b855087` |
| Runtime candidate | CURRENT / NOT FROZEN | `92ff830b…`; tree `73cf3ad…` |
| Candidate lineage | ESTABLISHED | `2a54a67d…` → `92ff830b…` |
| Current production deployment | CAPTURED | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` in P2/P6a artifacts |
| Provenance identity | COMPLETE / VALIDATED | All seven restored gate-state blocks included in canonical identity |
| Seven-gate constitutive restoration | IMPLEMENTED / PRE-FREEZE VALIDATED | Semantic restoration and provenance integrity validated |
| Active P-35 remediation | VERIFIED / ENGINEERING ONLY | `d83ea74c…`; pre-freeze run `33590352168`; no candidate/freeze/authorization effect |
| P2 runtime | VERIFIED | Run `33509348174`; artifact `9800942933`; five required cases passed |
| P6a CORS | VERIFIED | Run `33509416955`; artifact `9800972819`; four required checks passed |
| P3 | IMPLEMENTED / OPEN | Current-candidate evidence required |
| P4 | OPEN | Current-cycle blinding/custody evidence required |
| P5 | OPEN | Current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required |
| P7 scientific specification | TECHNICALLY ADJUDICATED / FORMALLY OPEN | Must bind exact candidate/protocol/analysis/freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Runtime candidate still requires current-candidate TGL/P-35 and analysis binding; remediation is a prerequisite repair, not P8 closure |
| P9 independent verification | HISTORICAL SCOPED PASS / NEW CANDIDATE REVERIFY REQUIRED | `a43219b…` only; independent verification required for the selected pilot candidate |
| New freeze | NOT ESTABLISHED | Candidate is not frozen |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Current runtime boundary

P2 and P6a both record the same production deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` and candidate SHA `92ff830b1c67413df745e37087e6447c9c251b9a`.

P2 artifact digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`.  
P6a artifact digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`.

The P2 five-case suite passed, including the required fail-closed result for a missing live audit state. The P6a CORS suite passed its four checks, including allowed-origin preflight 204 and disallowed-origin preflight 403. These results are limited to their recorded endpoint/deployment/environment scope and are not efficacy evidence.

## Historical evidence boundary

Pre-correction candidates and deployments remain historical/non-closing. The prior `d56b5b3c…` / `dpl_76UU8mCm…` boundary must not be reused as current evidence or dispatch input.

Older audit records that say inline artifact validation is missing are historical/stale observations, not current implementation defects. The current implementation performs inline artifact validation. Historical records remain preserved; current evidence status is tracked separately here.

## Required closure sequence

1. Complete current-candidate P3 artifact-contract evidence.
2. Complete P4 operational blinding/custody evidence.
3. Complete P5 environment/topology/RNG reproducibility evidence.
4. Complete P6 durable archive/retrieval/hash evidence.
5. Bind P7 to the exact candidate/protocol/analysis/final-freeze identity.
6. Close P8 from current-candidate TGL/P-35 evidence only; the remediation run is prerequisite engineering evidence, not closure.
7. Execute independent P9 verification for the selected pilot candidate.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, runtime verification result, historical evidence artifact, or repeated semantic audit does not create a new apparatus candidate or authorize scientific execution. Evidence must remain bound to its exact candidate/deployment/predicate scope.
