# DGAF/PDMAL Project Status

**Status date:** 2026-09-04  
**Last reconciled main tip:** `49a89d0da09a767bfea9ecc602905862ab17991f`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Verified executable runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Verified runtime deployment:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`  
**Corrected apparatus provenance anchor:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Pilot status:** PRE-FREEZE; authorization not granted  
**Empirical N:** 0

## Executive state

The repository is in post-control-plane-remediation, pre-freeze closure. The consolidated control-state anchor is `89be386b…`; subsequent `main` commits are documentation/control-plane reconciliation unless executable semantics change. The verified executable runtime identity remains `7c1cc4…` with deployment `dpl_8Ms…`. Documentation-only lineage does not alter the runtime surfaces covered by P2/P6a, so those predicates remain closed.

## Gate board

| Gate / control | Status | Evidence / state |
|---|---|---|
| Corrected apparatus provenance | CANONICAL ANCHOR | `2a54a67d…` |
| Control-plane consolidated anchor | CURRENT | `89be386b…` |
| Last reconciled main tip | CURRENT AT RECONCILIATION | `49a89d0d…` |
| Verified executable candidate | CURRENT VERIFIED RUNTIME IDENTITY | `7c1cc4…` |
| Runtime deployment | VERIFIED READY | `dpl_8Ms…` |
| P2 | CLOSED / VERIFIED | Run `33730195621`; artifact `9883521704` |
| P6a | CLOSED / VERIFIED | Run `33728695806`; artifact `9882965299` |
| P3 | OPEN | Current-candidate evidence packet required |
| P4 | OPEN | Operational blinding/custody |
| P5 | OPEN | Reproducibility/provenance closure |
| P6 | OPEN / FAIL-CLOSED | Durable external archive/retrieval/hash proof |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact protocol/candidate/analysis binding |
| P8 | OPEN / FAIL-CLOSED | Prerequisites and analysis lock |
| P9 | OPEN | Independent verification |
| Freeze | NOT ESTABLISHED | No immutable pilot identity |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | ZERO | No authorized pilot execution |

## Current-candidate evidence packet

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_PACKET_2026-09-04.md` defines the exact current-candidate P3–P9 evidence tuple and explicitly separates already-retained P2/P6a runtime evidence from outstanding operational, provenance, custody, analysis-lock, and independent-verification requirements.

The packet is a control/readiness artifact only. It does not promote historical evidence, create empirical observations, establish a freeze, or grant authorization.

## Evidence execution status

The retained current runtime evidence consists of exact-candidate P2 and P6a artifacts. Their workflow runs and artifact digests remain bound to `7c1cc4…` / `dpl_8Ms…`.

The strongest historical P3–P6 completion artifacts and P9 pass remain scoped to the superseded candidate `a43219b4…` and are therefore non-transferable.

## Evidence boundary

Evidence remains candidate- and workflow-scoped. Closed P2/P6a evidence is not reopened by documentation-only control-plane changes. Current P3–P6 closure still requires the operational and durable-custody predicates defined by the governance protocol.

## Current documentation hygiene state

The 2026-09-04 reconciliation pass distinguishes the consolidated control-state anchor from the mainline reconciliation tip. Later documentation-only descendants are not executable candidates unless executable semantics materially change and a new candidate is independently established.

## Required closure sequence

`P3 → operational P4/P5/P6 → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**