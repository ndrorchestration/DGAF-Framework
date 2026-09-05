---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-05
mainline_tip_at_last_reconciliation: 821878759797d0bfda2ae7a8bced980bd02c58a9
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

This is the current pre-authorization control record. The consolidated control-state anchor remains `89be386b…`; `82187875…` is the repository `main` reconciliation point after the exact-candidate P3 matrix-contract evaluator merged. Later documentation/control-plane descendants do not change the designated runtime candidate unless the canonical candidate manifest is explicitly changed.

## Current gate state

| Control | State | Evidence / scope |
|---|---|---|
| P-35 | VALIDATED | Immutable boundary `643dc77a…` |
| Consolidated control-state anchor | CURRENT | `89be386b…` |
| Mainline reconciliation anchor | DOCUMENTATION/CONTROL-PLANE | `82187875…` |
| Runtime candidate lineage | VERIFIED | candidate `7c1cc4bb…`; tree `586c00d6…` |
| Deployment reference | VERIFIED / LIVE RETRIEVED | Vercel deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`, READY production, Git source `7c1cc4bb…`; retained in `docs/evidence/PDMAL_DEPLOYMENT_IDENTITY_VERIFICATION_2026-09-05.md` |
| P1 Candidate Integrity | CLOSED / VERIFIED | exact apparatus/source, candidate/tree, self-bound provenance, and live deployment-to-candidate identity reconciled |
| P2 runtime | HISTORICAL RECORD / CURRENT ARTIFACT RETRIEVAL UNCONFIRMED | Run `33730195621`; artifact `9883521704`; live deployment identity is verified separately but five-case matrix has not been freshly re-executed |
| P6a CORS | HISTORICAL RECORD / CURRENT ARTIFACT RETRIEVAL UNCONFIRMED | Run `33728695806`; artifact `9882965299`; live deployment identity is verified separately but four-case CORS matrix has not been freshly re-executed |
| P3 Artifact Contract | CLOSED / VERIFIED | exact-candidate main run `33939955138`; source artifact `9961526468`; registry `9961526662`; canonical + 180-cell/adversarial schema contract retained |
| P4 Security / Blinding | OPEN / EVIDENCE PRESENT | main run `33939574283`; synthetic blinding/bijection/leakage/freeze-order checks pass, but real human/key custody and access separation remain unestablished |
| P5 Provenance / Reproducibility | OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT | run `33939955138` verifies candidate/tree, protocol/dependency identity, deterministic reproduction, environment and RNG/topology fingerprints; final analysis implementation/configuration binding remains pre-freeze work |
| P6 Durable Evidence Custody | CLOSED / VERIFIED | candidate-scoped Google Drive archive plus independent raw retrieval and SHA-256 equality; see `P6_DURABLE_CUSTODY_ATTESTATION_2026-09-05.md` |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding still required; P4/P5 prerequisites remain open |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | analysis implementation/configuration must be rebound at final P8 closure after prerequisites |
| P9 Independent Verification | OPEN | fresh independent verification of final bound chain not yet executed |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Pilot authorization | NOT GRANTED | separate governance decision |
| Empirical data | N = 0 | no authorized pilot execution |

## Current-candidate evidence established on 2026-09-05

### P1 deployment identity

The Vercel API independently resolved `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` as a READY production deployment for `ndrorchestration/DGAF-Framework`, sourced from Git commit `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`. This closes the deployment-identity uncertainty for P1. It does not recreate the P2/P6a runtime matrices.

### P3 artifact contract

Authoritative main run `33939955138` checked out the exact designated candidate/tree, ran the canonical pre-freeze artifact validator and the richer pilot artifact schema/adversarial fixtures, and emitted source-bound artifacts `9961526468` and `9961526662`. The test surface covers required fields, PRE-FREEZE/non-empirical constraints, exclusion consistency, record identity/hash integrity, canonical topology/failure coordinates, four-condition balance, duplicate rejection, and the 180-record/seed matrix contract. P3 is therefore CLOSED / VERIFIED as structural contract evidence, not empirical evidence.

### P4 synthetic operational evidence

Main run `33939574283` demonstrates synthetic mock-key blinding, deterministic bijection behavior, no cleartext/key leakage in the mock analyst-facing surface, and mock unblinding only after mock freeze. The evidence explicitly does not establish real human/key custody separation; P4 remains OPEN.

### P5 reproducibility evidence

Main run `33939955138` binds candidate/tree, protocol, hash-locked dependencies, Python/toolchain environment, deterministic contract reproduction, independently recomputed environment fingerprint, RNG child-stream separation, and topology fingerprint determinism. This materially advances P5, but the analysis control plan still requires final analysis implementation SHA and configuration SHA binding before the analysis chain is locked. P5 remains OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT.

### P6 durable custody

The finalized P3/P5 and P4 source/registry ZIPs were placed in independent Google Drive folder `1cbmvw8abh6m09M9YZRbRZ4kvsBlH2BLL`, retrieved back as raw bytes, and independently re-hashed. All SHA-256 values exactly matched their original GitHub artifact digests. P6 is CLOSED / VERIFIED for this candidate. The older historical P6 attestation remains non-transferable and unchanged.

## Runtime evidence boundary

The exact Vercel deployment is now independently live-retrievable and candidate-bound. However, the historical P2 and P6a GitHub Actions artifacts have not been freshly retrieved through the current verification path, and their authenticated runtime matrices have not been freshly re-executed. Their historical provenance records remain preserved without promotion.

## Evidence registry hardening

`docs/governance/CURRENT_CANDIDATE_EVIDENCE_REGISTRY_CONTRACT_v1.md` defines the unified immutable evidence-source tuple. PRs #236–#240 established designated-candidate self-binding and controller-side rejection of candidate/run/artifact/predicate tuple mismatches. The current evidence producers preserve explicit false freeze, pilot-authorization, unblinding, and empirical-execution controls.

## Remaining closure sequence

Current completed portions do not bypass the remaining operational and analysis prerequisites:

`P4 + final P5 binding → exact P7 binding → P8 → current-candidate P9 → immutable freeze → explicit authorization → blinded pilot`

P2/P6a remain separately historical/current-retrieval-limited runtime evidence and must not be silently promoted.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
