---
status: ACTIVE
state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
authority: Both
owner: DGAF/PDMAL experimental-control
last_verified: 2026-09-05
control_plane_lineage_tip_at_reconciliation: d859b8356a3488fbead2185f6006a048c0610d92
corrected_apparatus_source_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
corrected_apparatus_tree_sha: 973c92335caf84f37fc2b3c4df6dd83b3b855087
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
runtime_candidate_lineage: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 -> 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
candidate_deployment_id: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
protocol_version: 0.7.5
analysis_blob_sha: a269ed226b1d261663994fc3ef0e8a1a96da6cd3
analysis_config_sha256: 6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8
pilot_runner_blob_sha: b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243
pilot_artifact_schema_blob_sha: c620d3755a645c5f2ad14124f42ce07a1c670c5f
freeze_manifest_identity: null
freeze_manifest_sha256: null
freeze_commit_sha: null
freeze_timestamp_utc: null
freeze_author: null
independent_freeze_verification: null
p9_final_evidence: null
pilot_authorization_id: null
empirical_n: 0
---

# PDMAL Experiment — Pre-Freeze Manifest

## State boundary

This file is the **current negative/pre-freeze manifest**. It is not an immutable freeze and must not be cited as one. The living `main` branch is a documentation/control-plane lineage; it does not replace the designated runtime/scientific candidate unless the canonical candidate identity is explicitly changed.

The designated runtime candidate remains `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, tree `586c00d6dedb589e52108279f9759be3c4f927e1`, with candidate deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.

All freeze-specific identity fields above remain `null` because no execution-valid immutable freeze exists.

The final freeze must be created as a **new immutable object**, not by attempting to make this mutable negative record self-identifying. Its SHA-256 must be computed over the finalized freeze bytes and retained externally in a sidecar/attestation or equivalent independent record. A manifest must never embed the digest of its own complete bytes and then claim that embedded value hashes the resulting file; that would be circular. The `freeze_manifest_identity` / `freeze_manifest_sha256` nulls above are therefore pre-freeze placeholders indicating that the future external freeze identity/digest record does not yet exist, not fields to be self-populated inside the bytes being hashed.

## Experimental design selected pre-freeze

- Conditions: `null`, `simple`, `static`, `dgaf`
- Topologies: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- Failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`
- Trials per seed: 180
- Planned seeds: 50
- Planned raw trial records: 9,000
- Primary endpoint: FFCR per condition per seed
- Primary contrast: `dgaf` vs `null`
- Statistical unit: paired root seed
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`
- Primary estimand: equal-weight mean paired seed effect
- Bootstrap: 10,000 paired-seed percentile resamples
- Deterministic bootstrap seed: `20260823`
- Confidence interval: two-sided 95%, `alpha=0.05`
- Iterations: 100 fixed; no convergence-based early stopping
- No outcome-dependent weighting, silent imputation, or silent exclusion

These are design selections, not empirical results.

## Current evidence state

| Predicate | State | Current evidence boundary |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| Runtime candidate lineage | VERIFIED | candidate `7c1cc4bb…`; tree `586c00d6…` |
| Candidate deployment | VERIFIED | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`, exact candidate source |
| P1 Candidate Integrity | CLOSED / VERIFIED | apparatus/source, candidate/tree, provenance, deployment identity |
| P2 Runtime | CLOSED / VERIFIED | run `33730195621`; artifact `9883521704`; five-case authenticated matrix |
| P3 Artifact Contract | CLOSED / VERIFIED | run `33939955138`; artifacts `9961526468` / `9961526662`; structural/contract scope |
| P4 Security / Blinding | OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED | synthetic controls pass; real distinct-human custody/access separation absent |
| P5 Provenance / Reproducibility | CLOSED / VERIFIED | exact analysis/configuration/runner/schema/environment/RNG/topology chain |
| P6 Durable Evidence Custody | CLOSED / VERIFIED | independent archive/retrieval/SHA-256 equality for retained evidence set |
| P6a CORS | CLOSED / VERIFIED | run `33728695806`; artifact `9882965299`; four-case authenticated matrix |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | final binding awaits actual P4 custody and freeze-specific identities |
| P8 Analysis Lock / Freeze | OPEN / FAIL-CLOSED | analysis identities bound; immutable freeze not created or independently verified |
| P9 Independent Verification | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | all freeze-specific identity fields remain null |
| Pilot authorization | NOT GRANTED | separate governance decision absent |
| Empirical data | N = 0 | no authorized pilot observation |

## P4 boundary

The repository contains both the authoritative human/key-custody procedure and a pre-filled execution handoff. Their existence is not operational custody evidence.

The following remain absent and must not be inferred or fabricated:

- a genuinely distinct human Key Custodian;
- a distinct execution/analysis principal;
- real nonce-hardened key and mapping commitments;
- attributable custody and no-access attestations;
- independent custody review.

P4 therefore remains OPEN / NOT EXECUTED operationally.

## P7/P8/P9 boundary

`docs/governance/P7_FINAL_BINDING_DRAFT_2026-09-05.md` already assembles the established candidate/deployment/protocol/analysis/runner/schema and P2/P3/P5/P6/P6a identities. Its closure-blocking P4/freeze/P9/authorization fields remain explicit and unresolved.

P8 may construct the immutable freeze only after real P4 custody is independently verified and P7 is final with no unresolved closure-blocking placeholders. The immutable freeze must bind, at minimum:

1. final protocol blob/commit identity;
2. final accepted control-plane commit;
3. exact candidate SHA/tree and deployment identity;
4. exact analysis/configuration/runner/schema identities;
5. required P1/P2/P3/P4/P5/P6/P6a evidence identities/digests;
6. non-secret blinding-custody commitments and attestations;
7. an externally retained digest of the finalized immutable freeze bytes;
8. independent freeze-verification evidence.

P9 must then independently verify that complete frozen chain. Historical/scoped P9 runs are provenance only and do not transfer.

## Promotion rule

This pre-freeze manifest becomes superseded by a new execution-valid immutable freeze object only when:

- P4 real custody is independently verified;
- P7 final exact binding is closed;
- every freeze tuple field is exact and immutable;
- the finalized freeze object is created;
- its byte-level SHA-256 is retained externally in a non-circular sidecar/attestation;
- an independent verifier retrieves/re-resolves/re-hashes the finalized freeze bytes and records a PASS.

Even then, pilot authorization is a separate later governance transition.

**Freeze: NOT ESTABLISHED · Pilot authorization: NOT GRANTED · Empirical N: 0.**
