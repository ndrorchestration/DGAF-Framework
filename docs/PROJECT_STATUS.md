# DGAF/PDMAL Project Status

**Status date:** 2026-09-01  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** active documentation/control-plane lineage; resolve `main` directly for latest source  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Current production/runtime candidate:** `92ff830b1c67413df745e37087e6447c9c251b9a`  
**Current candidate tree:** `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`  
**Current production deployment observed in P2/P6a evidence:** `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in structured post-provenance-correction, pre-freeze closure. Commit `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` is the corrected apparatus source that binds the seven restored behavior-affecting DGAF/TGL gate-state substrates into canonical provenance identity. It is distinct from the current production/runtime candidate.

The current production/runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a`, a deployment-workflow repair commit whose exact tree is `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. Git history comparison establishes the corrected apparatus source as the candidate's ancestor/lineage basis; the two identities must remain distinct in all scientific binding.

Fresh P2 and P6a verification have now executed against candidate `92ff830b…` and recorded the same production deployment identity `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` in their artifacts. P2 run `33509348174` produced artifact `9800942933` with digest `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`. P6a run `33509416955` produced artifact `9800972819` with digest `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`. These close the P2 and P6a runtime-verification gates for their stated evidence scope; they do not by themselves close P3–P6, P7, P8, P9, freeze, authorization, or the empirical boundary.

The canonical scientific lineage is:

`corrected apparatus source → candidate provenance/lineage → exact candidate commit → exact candidate tree → exact production deployment → P2/P6a → P3–P6 evidence → P7 final candidate binding → P8 TGL/P-35 verification → P9 → freeze → authorization → blinded pilot`.

No empirical data have been collected. No freeze has been created or crossed, authorization has not been granted, and the unblinding/empirical boundary remains untouched. Empirical N remains 0.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` |
| Current repository main | CURRENT CONTROL-PLANE LINEAGE | Resolve `main` directly |
| Corrected apparatus source | CANONICAL APPARATUS PROVENANCE | `2a54a67d…`; seven restored gate-state substrates bound |
| Current runtime candidate | CURRENT / NOT FROZEN | `92ff830b…`; tree `73cf3ad…` |
| Candidate → apparatus lineage | ESTABLISHED | `2a54a67d…` is ancestor/lineage basis of `92ff830b…` |
| Current production deployment identity | CAPTURED IN RUNTIME EVIDENCE | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| P2 | VERIFIED | Run `33509348174`; artifact `9800942933`; candidate-bound |
| P6a | VERIFIED | Run `33509416955`; artifact `9800972819`; candidate-bound |
| P3 | IMPLEMENTATION PRESENT / OPEN | Current-candidate evidence still required |
| P4 | OPEN | Current-cycle blinding/custody evidence required |
| P5 | OPEN | Current-cycle environment/topology/RNG reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required |
| P7 | SPECIFICATION ADOPTED / FINAL BINDING OPEN | Bind exact apparatus/candidate/deployment/protocol/analysis identity |
| P8 | OPEN / FAIL-CLOSED | TGL/P-35 current-candidate verification required |
| P9 | NOT EXECUTED | Independent current-candidate verification required |
| Freeze | NOT ESTABLISHED | No immutable frozen identity is authoritative |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | ZERO | No authorized pilot execution |
| Documentation quality | ACTIVE RECONCILIATION | Historical claims retained; current-state claims corrected |

## Deployment provenance controls

The current runtime candidate is `92ff830b1c67413df745e37087e6447c9c251b9a` with tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`. The production deployment identity recorded by both P2 and P6a is `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`, with deployment URL `https://dynamicgovernanceagenticformation-3y3d8o5dp-ndrorchestration.vercel.app`.

The deployment workflow in the current candidate requires authenticated Vercel deployment, establishes behavior-affecting runtime configuration before deployment attestation, checks READY/production state, and verifies source SHA equality before emitting deployment provenance evidence. Runtime verification artifacts separately record their candidate SHA and deployment ID. These are complementary controls and must not be collapsed into a single assertion.

Operational dispatch documents must contain only the current candidate's exact dispatch values. Superseded SHA/deployment pairs remain historical/non-closing evidence and must not be reused as current dispatch inputs.

## Evidence boundary by gate

P2 verifies the current runtime execution contract for the candidate/deployment scope recorded in its artifact. Its five required cases passed, including expected fail-closed behavior for the live-audit-missing case.

P6a verifies the current CORS behavior for the candidate/deployment/endpoint scope recorded in its artifact. Allowed-origin preflight returned 204, disallowed-origin preflight returned 403, and both POST cases passed their expected checks.

P3 is implemented but remains open pending current-candidate evidence. P4, P5, and P6 remain open at their respective evidence boundaries. P7 is adopted as the scientific specification but remains open for final immutable candidate binding. P8 remains fail-closed until its TGL/P-35 predicates are verified against the final candidate. P9 is independent and has not been executed.

No CI success, deterministic dry run, runtime PASS, deployment readiness, historical artifact, semantic audit, or documentation update constitutes efficacy evidence or pilot authorization.

## Documentation hygiene and stale-claim policy

Historical audit records must retain their original findings and exact scope. Older documents that state that inline artifact validation is missing are therefore classified as **historical/stale claims**, not current implementation defects, because the current implementation now performs the inline validation.

Those historical records should not be silently rewritten to erase the former finding. Current-state documents must instead state the present implementation and independently identify any remaining current-candidate evidence gap. Contradictory operational claims such as “current candidate,” “ready to dispatch,” or “verified” are corrected only where they function as current control-plane assertions.

## Required closure sequence

1. Preserve the corrected apparatus source `2a54a67d…` as the canonical apparatus provenance anchor.
2. Preserve the distinct runtime candidate `92ff830b…` and exact tree `73cf3ad…` as the current candidate identity.
3. Bind the exact production deployment identity and P2/P6a evidence to that candidate.
4. Complete P3–P6 current-cycle artifact, blinding, reproducibility, and durable-custody evidence.
5. Close P7 only when the final candidate/protocol/analysis/freeze identity is immutably bound.
6. Close P8 only from current-candidate TGL/P-35 evidence.
7. Execute independent P9 verification.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the authorized blinded pilot.

## Current experimental state

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
