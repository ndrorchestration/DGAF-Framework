> **Historical snapshot / superseded for present-state use — 2026-09-05:** This file preserves the 2026-09-01 control-plane state and its then-current candidate/evidence identities. It is not current gate authority. The current designated runtime candidate is `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`; present gate state is controlled by `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`, `docs/experiment/NEW_CANDIDATE_MANIFEST.md`, and `docs/CURRENT_STATE.md`. Do not promote the historical OPEN/VERIFIED states below into present-state claims.

# DGAF/PDMAL Current State — 2026-09-01

## Authority

This record is the current control-plane reconciliation for 2026-09-01. It is subordinate to exact execution evidence and does not itself create experimental evidence, freeze, authorization, or empirical data.

**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Current production/runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a`  
**Current candidate tree:** `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`  
**Current production deployment recorded by P2/P6a:** `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`  
**Epistemic boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.

## Provenance distinction

`2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` is the corrected apparatus source. It is the canonical provenance anchor for the seven restored behavior-affecting DGAF/TGL gate-state substrates.

`92ff830b1c67413df745e37087e6447c9c251b9a` is a distinct deployment-workflow repair commit and the current production/runtime candidate. Its exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`.

Git history comparison establishes the corrected apparatus source as the ancestor/lineage basis of the runtime candidate. This lineage relationship does not make the two identities interchangeable: the apparatus source remains the scientific provenance anchor, while the runtime candidate is the exact executable candidate bound to runtime evidence.

## Current gate state

| Boundary | State |
|---|---|
| Corrected apparatus | CANONICAL PROVENANCE ANCHOR |
| Candidate lineage | ESTABLISHED from `2a54a67d…` to `92ff830b…` |
| Candidate tree | IDENTIFIED as `73cf3ad…` |
| Production deployment | CAPTURED as `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` in P2/P6a evidence |
| P2 | VERIFIED — run `33509348174`, artifact `9800942933` |
| P6a | VERIFIED — run `33509416955`, artifact `9800972819` |
| P3 | IMPLEMENTATION PRESENT / CURRENT-CANDIDATE EVIDENCE OPEN |
| P4 | OPEN |
| P5 | OPEN |
| P6 | OPEN / FAIL-CLOSED |
| P7 | SPECIFICATION ADOPTED / FINAL CANDIDATE BINDING OPEN |
| P8 | OPEN / FAIL-CLOSED — TGL/P-35 candidate verification required |
| P9 | NOT EXECUTED |
| Freeze | NOT ESTABLISHED |
| Authorization | NOT GRANTED |
| Empirical data | N=0 |

## P2 evidence

P2 run `33509348174` executed against candidate `92ff830b1c67413df745e37087e6447c9c251b9a` and recorded deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. Artifact `9800942933` has digest `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`. All five required runtime cases passed. The `valid_missing_audit` case remained correctly fail-closed with HTTP 503 and decision `BLOCKED`.

## P6a evidence

P6a run `33509416955` executed against the same candidate and deployment identity. Artifact `9800972819` has digest `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`. The allowed-origin preflight returned 204, the disallowed-origin preflight returned 403, and both POST cases passed their expected checks. The artifact explicitly limits its epistemic scope to the tested endpoint, deployment, environment, and configured origins.

## Scientific lineage

The canonical binding chain is:

`corrected apparatus source → candidate provenance/lineage → exact candidate commit → exact candidate tree → exact production deployment → P2/P6a → P3–P6 evidence → P7 final candidate binding → P8 TGL/P-35 verification → P9 → freeze → authorization → blinded pilot`.

No downstream state may inherit evidence merely because it shares a repository, branch, deployment URL, or related documentation commit. Evidence must be bound to the exact applicable identity and predicate scope.

## Historical/stale documentation classification

Older audit records that state inline artifact validation is missing are historical/stale claims, not current implementation defects. The current implementation performs inline artifact validation. Historical records remain preserved as historical evidence and should not be silently rewritten to erase their former observations.

Current-state documentation must describe the implementation as it exists now and separately track any remaining candidate-scoped evidence gap. A stale historical claim must not be promoted into a current defect merely by search or text reuse.

## Governance boundary

P2/P6a verification is runtime evidence only. It does not establish efficacy, scientific success, freeze, authorization, or an empirical sample. P3–P6 require their own current-cycle predicates. P7 remains open until exact final candidate/protocol/analysis/freeze binding is established. P8 remains fail-closed until TGL/P-35 candidate verification is complete. P9 remains independent and unexecuted.

No unblinding or authorized empirical execution has occurred. Empirical N remains zero.
