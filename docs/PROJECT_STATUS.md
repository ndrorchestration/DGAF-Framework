# DGAF/PDMAL Project Status

**Status date:** 2026-09-03  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** active documentation/control-plane lineage; resolve `main` directly for latest source  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Current successor candidate:** `48c12c6660df7decb61f9aac4d8560526a8754eb` (PR #200)  
**Current candidate branch:** `candidate/p35-validated-control-state-2026-09-02`  
**Exact candidate deployment:** `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`  
**Exact deployment URL:** `https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in structured post-provenance-correction, pre-freeze closure. Commit `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` is the corrected apparatus source that binds the seven restored behavior-affecting DGAF/TGL gate-state substrates into canonical provenance identity.

The current successor candidate is PR #200 at exact head `48c12c6660df7decb61f9aac4d8560526a8754eb`, derived from immutable P-35 validation boundary `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. The exact candidate/deployment pair is the only current deployment identity eligible for current-cycle deployment-bound verification.

The current candidate has a green validation wave, including Governance CI, PDMAL pre-freeze runner validation, PDMAL pre-authorization security, control-state binding, instrumentation dry-run, truth/evidence validation, regression, and repository coverage checks. Governance CI on the exact candidate also verified the pinned TLA+ Tools v1.8.0 checksum and completed the bounded DGAF containment model check with no model-checking error.

Historical P2/P6a runs for candidate `92ff830b…` and deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` remain historical and non-transferable. Current exact-candidate P2/P6a workflow artifacts are still required because runtime observations alone do not replace the candidate-bound retained workflow evidence.

Recent Vercel runtime diagnostics for the exact candidate deployment show two POST requests and two OPTIONS requests to `/api/orchestrate`. The observed POST status `503` is not itself a P6a failure: the P6a workflow contract explicitly accepts 200, 400, or 503 for the allowed-origin POST when the expected `Access-Control-Allow-Origin` header is present, and requires the disallowed-origin POST to omit that header. The preflight contract requires 204/allowed and 403/disallowed with the corresponding header rules. These runtime logs are diagnostic observations and do not substitute for the retained P6a workflow artifact.

No empirical data have been collected. No freeze has been created or crossed, authorization has not been granted, and the unblinding/empirical boundary remains untouched. Empirical N remains 0.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` |
| Corrected apparatus source | CANONICAL APPARATUS PROVENANCE | `2a54a67d…` |
| Immutable P-35 boundary | VALIDATED / IMMUTABLE | PR #199; `643dc77a…` |
| Current successor candidate | CURRENT / PRE-FREEZE / FAIL-CLOSED | PR #200; `48c12c…` |
| Exact candidate deployment | ESTABLISHED / READY | `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`; exact URL recorded above |
| P1 | OPEN | Final provenance/closure predicates remain to be completed |
| P2 | RERUN REQUIRED | Historical evidence does not transfer to `48c12c…` |
| P3 | IMPLEMENTATION PRESENT / OPEN | Current-candidate execution evidence still required |
| P4 | OPEN | Current-cycle blinding/custody evidence required |
| P5 | OPEN | Current-cycle environment/topology/RNG reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody/retrieval proof required |
| P6a | RERUN REQUIRED | Historical evidence does not transfer to `48c12c…`; exact workflow artifact required |
| P7 | SPECIFICATION ADOPTED / FINAL BINDING OPEN | Bind exact final candidate/deployment/protocol/analysis identity |
| P8 | OPEN / FAIL-CLOSED | Current-candidate TGL/P-35 verification required |
| P9 | NOT EXECUTED | Independent current-candidate verification required |
| Freeze | NOT ESTABLISHED | No immutable frozen identity is authoritative |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | ZERO | No authorized pilot execution |

## Evidence boundary

`DEFINED` does not mean `IMPLEMENTED`; `IMPLEMENTED` does not mean `VERIFIED`; `VERIFIED` does not mean experimental efficacy.

Historical successful runs remain provenance only unless the evidence artifact is explicitly bound to the exact current candidate and deployment. Runtime observations, deployment readiness, deterministic harness success, bounded model checks, synthetic evaluations, and documentation reconciliations do not establish real-world efficacy or authorize a pilot.

## Required closure sequence

1. Execute candidate-bound P2 and P6a against `48c12c…` / `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` and retain artifacts.
2. Complete current-candidate P3 artifact-contract evidence.
3. Complete current-candidate P4 blinding/custody evidence.
4. Complete current-candidate P5 reproducibility evidence.
5. Complete current-candidate P6 durable custody/retrieval/hash evidence.
6. Perform final P7 exact scientific binding.
7. Perform current-candidate P8/TGL/P-35 verification.
8. Execute independent current-candidate P9 verification.
9. Create and independently verify the immutable freeze.
10. Obtain explicit pilot authorization.
11. Only then execute the authorized blinded pilot.

## Current experimental state

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
