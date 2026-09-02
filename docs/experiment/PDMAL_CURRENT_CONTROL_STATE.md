---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: 92ff830b1c67413df745e37087e6447c9c251b9a
candidate_status: CURRENT RUNTIME CANDIDATE / NOT FROZEN / P3-P8 EVIDENCE REMAINING
active_p35_remediation_head: 9ba7677c98c2eb8502ca141b70ff59104ad89fea
active_p35_pre_freeze_run: 33604135832
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It is the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.

The current production/runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a`, with exact tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. Git history establishes the corrected apparatus source as its lineage basis. These identities remain distinct: apparatus provenance is not the same thing as executable candidate identity.

The active P-35 remediation is a separate engineering lineage: PR #188 / branch `remediation/p35-premise-hook-2026-09-01`, current head `9ba7677c98c2eb8502ca141b70ff59104ad89fea`. Its exact-head runtime characterization completed in run `33604135832` as PRE-FREEZE/non-empirical verification, with 54/54 characterization trials complete and zero failed. That remediation head is not the current runtime candidate and does not inherit or transfer runtime evidence.

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
| Active P-35 remediation | VERIFIED / ENGINEERING ONLY | `9ba7677c…`; exact-head runtime characterization `33604135832`; no candidate/freeze/authorization effect |
| P2 runtime | VERIFIED | Run `33509348174`; artifact `9800942933`; five required cases passed |
| P6a CORS | VERIFIED | Run `33509416955`; artifact `9800972819`; four required checks passed |
| P3 | IMPLEMENTED / OPEN | Current-candidate evidence required |
| P4 | OPEN | Current-cycle blinding/custody evidence required |
| P5 | OPEN | Current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required |
| P7 scientific specification | ADOPTED / FINAL BINDING OPEN | Must bind exact candidate/protocol/analysis/freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Runtime candidate still requires current-candidate TGL/P-35 and analysis binding; remediation is a prerequisite repair, not P8 closure |
| P9 independent verification | NOT EXECUTED FOR CURRENT CANDIDATE | Independent audit/reproduction required |
| New freeze | NOT CREATED | Candidate is not frozen |
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

## Current remediation evidence boundary

PR #188 / branch `remediation/p35-premise-hook-2026-09-01` is engineering/pre-freeze evidence only. Current head `9ba7677c98c2eb8502ca141b70ff59104ad89fea` includes the P-35 premise-hook remediation and a follow-up correction to `p9-independent-evidence.sha256` for Windows CRLF/on-disk hashing.

Run `33604135832` completed exact-head runtime characterization for that SHA. Artifact `9836428941` contains `runtime_characterization.json` and its SHA-256 sidecar. The characterization is PRE-FREEZE and non-empirical: 54 expected trials across 3 seeds × conditions (`null`, `simple`, `static`) × topologies (`ring`, `pdmal`) × failure counts (0, 2, 5), with 54 completed and 0 failed. The inner artifact digest is `4f2d3193a3a008c22d26f4c4d52bc84d04eb0292117acf969c01ee4f7003e3aa`, and the sidecar records the same digest.

Formal P-35 acceptance remains pending a runner-boundary predicate showing that `run_pilot()` rejects a missing premise checker before task construction and that an explicit checker reaches DGAF `ConsensusTask`. The remediation run is not experimental efficacy evidence and does not close P8, create a freeze, or authorize execution.

## Required closure sequence

1. Complete current-candidate P3 artifact-contract evidence.
2. Complete P4 operational blinding/custody evidence.
3. Complete P5 environment/topology/RNG reproducibility evidence.
4. Complete P6 durable archive/retrieval/hash evidence.
5. Bind P7 to the exact candidate/protocol/analysis/final-freeze identity.
6. Close P8 from current-candidate TGL/P-35 evidence only; the remediation characterization is prerequisite engineering evidence, not closure.
7. Execute independent P9 verification.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, runtime characterization result, historical evidence artifact, or repeated semantic audit does not create a new apparatus candidate or authorize scientific execution. Evidence must remain bound to its exact candidate/deployment/predicate scope.
