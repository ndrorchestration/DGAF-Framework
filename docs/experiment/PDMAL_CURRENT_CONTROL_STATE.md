---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-05
mainline_tip_at_last_reconciliation: 9cf9fcdd3454ce7309efdcbbe4ef29f802a7c97e
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# PDMAL Current Control State

This is the current pre-authorization control record. The consolidated control-state anchor remains `89be386b…`; `9cf9fcdd…` is the current repository documentation/control-plane tip at this reconciliation. Documentation descendants do not replace the designated runtime candidate unless the canonical candidate manifest is explicitly changed.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Consolidated control-state anchor | CURRENT | `89be386b…` |
| Mainline reconciliation anchor | DOCUMENTATION/CONTROL-PLANE | `9cf9fcdd…` |
| Runtime candidate lineage | VERIFIED | candidate `7c1cc4bb…`; tree `586c00d6…` |
| Deployment reference | VERIFIED / LIVE RETRIEVED | Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`, READY production, Git source `7c1cc4bb…` |
| P1 Candidate Integrity | CLOSED / VERIFIED | exact apparatus/source, candidate/tree, self-bound provenance, and live deployment-to-candidate identity reconciled |
| P2 runtime | CLOSED / VERIFIED | run `33730195621`; artifact `9883521704`; digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`; five-case authenticated matrix passed on exact candidate/deployment |
| P3 Artifact Contract | CLOSED / VERIFIED | exact-candidate run `33939955138`; source artifact `9961526468`; registry `9961526662`; canonical + adversarial schema contract retained |
| P4 Security / Blinding | OPEN / EVIDENCE PRESENT | synthetic blinding/bijection/leakage/freeze-order checks pass, but real human/key custody and access separation remain unestablished |
| P5 Provenance / Reproducibility | OPEN / FINAL IDENTITY BINDING RECORDED FOR REVIEW | reproducibility evidence present; exact analysis/configuration/runner/schema identities recorded in `docs/governance/P8_ANALYSIS_LOCK.md`; authoritative merge/review still required |
| P6 Durable Evidence Custody | CLOSED / VERIFIED | candidate-scoped Google Drive archive plus independent raw retrieval and SHA-256 equality |
| P6a CORS | CLOSED / VERIFIED | run `33728695806`; artifact `9882965299`; digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`; four-case authenticated CORS matrix passed on exact candidate/deployment |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding still required; P4/P5 prerequisites remain open |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | current analysis identities are recorded, but final prerequisite acceptance and immutable freeze remain open |
| P9 Independent Verification | NOT EXECUTED / OPEN | fresh independent verification of final bound chain not yet executed |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical data | N = 0 | no authorized pilot execution |

## Current-candidate evidence established

### P1 deployment identity

The exact Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` is bound to runtime candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`. This is deployment-identity evidence, not efficacy evidence.

### P2 authenticated runtime matrix

Run `33730195621` executed the five predeclared runtime cases with the protected Vercel bypass credential present and withheld. All cases matched their expected HTTP/decision outcomes. Artifact `9883521704` remains candidate/deployment-bound. The expected HTTP 503 / `BLOCKED` result for the valid request is fail-closed contract behavior because live audit state is not wired into `/api/orchestrate`; it is not general application-health evidence.

### P3 artifact contract

Run `33939955138` checked out the exact designated candidate/tree and verified the pre-freeze/pilot artifact schema, identity, canonical matrix, determinism, duplicate-rejection, and fail-closed unauthorized-pilot contract. P3 is structural/contract evidence only.

### P4 synthetic operational evidence

Run `33939574283` demonstrates synthetic mock-key blinding, deterministic bijection, leakage controls, and freeze-order behavior. It explicitly does not establish real human/key custody or access separation. P4 remains OPEN.

### P5 reproducibility and final identity record

Run `33939955138` binds candidate/tree, protocol, hash-locked dependencies, toolchain/environment, deterministic reproduction, environment fingerprint, RNG child-stream separation, and topology fingerprint determinism.

The designated candidate analysis-control identities are now recorded in `docs/governance/P8_ANALYSIS_LOCK.md`:

- analysis implementation blob: `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- analysis configuration SHA-256: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner blob: `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema blob: `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol version: `0.7.5`.

P5 remains OPEN until this binding lands on the authoritative control plane and passes the normal consistency/review checks.

### P6 durable custody

The finalized P3/P5 and P4 source/registry ZIPs were copied to the independent archive, retrieved as raw bytes, and independently re-hashed. The retrieved SHA-256 values matched their original GitHub artifact digests.

### P6a authenticated CORS matrix

Run `33728695806` executed the four required live CORS checks against the exact candidate deployment. Allowed and disallowed POST behavior and allowed/disallowed preflight behavior all matched the predeclared policy. Artifact `9882965299` remains candidate/deployment-bound. This evidence is endpoint/deployment/environment/origin scoped.

## Evidence registry hardening

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_REGISTRY_CONTRACT_v1.md` defines the immutable evidence-source tuple. Completion-controller hardening binds evidence to the exact triggering workflow run rather than a latest-matching run. Historical failures and superseded candidate records remain preserved.

## Remaining closure sequence

`P4 real custody + authoritative P5 binding → exact P7 binding → P8 / immutable freeze → independent P9 → explicit authorization → blinded pilot`

No completed gate above authorizes empirical execution or changes empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
