# DGAF/PDMAL Project Status

**Status date:** 2026-09-02  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** `275756fd81c975f17ae3d16d24e599db0617cf85` — documentation/control-plane lineage  
**Selected experimental candidate:** PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`  
**Selected candidate tree:** `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in structured post-provenance-correction, pre-freeze closure. Commit `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` remains the corrected apparatus provenance anchor and is distinct from the executable candidate.

The September 2 selected experimental candidate is PR #192 / `58ba9a072f40e94638b0332eeec19dd882a7ff95`, exact tree `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`. This candidate integrates the verified P-35 production boundary and remains pre-freeze. Its GitHub Actions verification wave is green, but deployment identity is not established for this exact SHA.

The previously verified runtime candidate `92ff830b1c67413df745e37087e6447c9c251b9a` and production deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` remain historical evidence for their exact scope. Their P2/P6a results do not transfer to `58ba9a…`.

The selected candidate has 18/18 successful GitHub Actions workflows, including Governance CI `33616403706`, Pre-Freeze Runner Validation `33616403754`, Pre-Authorization Security `33616403843`, Instrumentation Dry Run `33616403724`, and Harness Validation `33616403784`. The GitHub combined status still reports Vercel `failure` at the provider build/deployment-rate-limit target, and the latest Vercel inventory contains no READY deployment whose recorded Git SHA is `58ba9a…`.

The canonical scientific/control lineage is:

`corrected apparatus source → selected candidate → exact candidate tree → exact deployment binding → fresh P2/P6a → P3–P6 evidence → P7 final binding → P8 → P9 → freeze → authorization → blinded pilot`.

No empirical data have been collected. No freeze has been created or crossed, authorization has not been granted, and the unblinding/empirical boundary remains untouched. Empirical N remains 0.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | Preserved historical record |
| Current repository main | CURRENT CONTROL-PLANE LINEAGE | `275756fd…`; resolve `main` directly |
| Corrected apparatus source | CANONICAL APPARATUS PROVENANCE | `2a54a67d…` |
| Selected experimental candidate | CURRENT / NOT FROZEN | PR #192 / `58ba9a…`; tree `abdbc9b…` |
| Candidate → apparatus lineage | ESTABLISHED | Selected candidate descends from corrected apparatus lineage |
| Exact current deployment identity | NOT ESTABLISHED | No READY Vercel deployment recorded with Git SHA `58ba9a…` |
| P2 | OPEN / DEPLOYMENT-BOUND | Fresh exact-candidate runtime matrix required |
| P6a | OPEN / DEPLOYMENT-BOUND | Fresh exact-candidate CORS matrix required |
| P3 | VERIFIED — ENGINEERING/CONTROL SCOPE | Current candidate CI, artifact, and instrumentation controls pass; full experimental execution remains separate |
| P4 | OPEN | Current-cycle operational blinding/custody closure required |
| P5 | VERIFIED — TOOLCHAIN/REPRODUCIBILITY SCOPE | Current candidate hashes, lock, package/toolchain and deterministic instrumentation retained; final closure remains open |
| P6 | OPEN / FAIL-CLOSED | Durable independent archive/retrieval proof required |
| P7 | EXACT-CANDIDATE BINDING RECORDED PRE-FREEZE | Scientific target preserved; freeze/authorization identity not established |
| P8 | OPEN / FAIL-CLOSED | Depends on current-candidate runtime/TGL/P-35, operational, binding, and P9 predicates |
| P9 | OPEN | Fresh independent verification of `58ba9a…` required |
| Freeze | NOT ESTABLISHED | No immutable frozen identity is authoritative |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | ZERO | No authorized pilot execution |
| Documentation quality | ACTIVE RECONCILIATION | Historical claims preserved; current assertions corrected |

## Deployment provenance controls

The selected experimental candidate is `58ba9a072f40e94638b0332eeec19dd882a7ff95` with tree `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`. No current deployment binding has been established for that exact SHA.

The historical runtime candidate `92ff830b…` had P2/P6a evidence against deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`. That deployment/evidence pair remains exact-scoped historical evidence and is explicitly non-transferable to `58ba9a…`.

A current candidate-bound runtime result must identify the exact candidate commit/tree and exact deployment identity. Successful CI, a READY deployment for another SHA, or repository ancestry cannot substitute for that binding.

## Evidence boundary by gate

P2 and P6a remain open because their last verified runtime evidence belongs to `92ff830b…`, not `58ba9a…`.

P3 is verified at current engineering/control scope. P4 remains open pending full operational blinding and custody evidence. P5 has current verifier/toolchain evidence but final closure remains open. P6 remains fail-closed pending durable external archive/retrieval/hash evidence. P7 has an exact-candidate pre-freeze binding record, but freeze identity is not established. P8 remains fail-closed and P9 requires fresh independent verification.

No CI success, deterministic dry run, historical runtime PASS, documentation update, READY deployment for a different SHA, or synthetic evaluator result constitutes efficacy evidence or pilot authorization.

## Documentation hygiene and stale-claim policy

Historical audit records must retain their original findings and exact scope. Documents that describe `92ff830b…` and `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` as the current runtime must therefore be corrected when they function as active control-plane assertions; their underlying evidence remains preserved as historical/non-transferable evidence.

Current-state documents must identify `58ba9a…` as the selected experimental candidate and explicitly separate candidate identity from workflow merge-ref identity and deployment identity.

## Required closure sequence

1. Preserve the corrected apparatus source `2a54a67d…` as the canonical provenance anchor.
2. Preserve the selected candidate `58ba9a…` / tree `abdbc9b…` as the current experimental boundary.
3. Establish a READY deployment whose recorded Git SHA exactly matches `58ba9a…`.
4. Run fresh authenticated P2/P6a against that same deployment.
5. Complete current-cycle P4/P5/P6 closure evidence.
6. Maintain the exact P7 binding and close only with final protocol/analysis/freeze identity.
7. Close P8 only from current-candidate evidence.
8. Execute independent fresh P9 verification.
9. Create and independently verify a new immutable freeze.
10. Obtain explicit pilot authorization.
11. Only then execute the authorized blinded pilot.

## Current experimental state

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
