---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-10
canonical_high_assurance_empirical_n: 0
final_candidate_status: NOT_DESIGNATED
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
canonical_dgaf_efficacy: NOT_ESTABLISHED
track_a_epoch_001_collection: COMPLETE_BLINDED_RETAINED
track_a_epoch_001_inferential_seed_units: 50
track_a_epoch_001_blinded_observations: 2250
track_a_epoch_001_dataset_lock: ESTABLISHED
track_a_epoch_001_unblinding_authorization: ESTABLISHED_HISTORICAL
track_a_epoch_001_unblinding_recoverability: CRYPTOGRAPHICALLY_UNRECOVERABLE
track_a_epoch_001_primary_analysis: UNANALYZABLE_NOT_RUN
track_a_successor_issue: 523
track_a_successor_collection_authorization: NOT_ESTABLISHED
---

# DGAF-Framework / PDMAL — Current State

This file is the primary current-facing repository summary. GitHub remains authoritative for implementation, immutable evidence identities, issues, and CI. Notion is the governance/control-plane mirror. Historical records remain valid only for the exact scope they bind.

**Important:** the canonical High-Assurance program, Track A Epoch 001, and any future Track A successor epoch are separate governance/evidence boundaries. Progress in one must not be silently promoted into another.

## Canonical High-Assurance provenance boundary

Repository **main** recency does not redefine the High-Assurance apparatus source, candidate identity, or deployment identity. Those remain exact-scope provenance records until an explicit governing transition replaces them.

- apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- apparatus source tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`
- historical runtime-evidence candidate identity: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- historical runtime deployment identity: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- final v0.7.6 High-Assurance candidate identity: **NOT DESIGNATED**

The separate High-Assurance program therefore remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / canonical empirical N=0**.

## Executive boundary

| Area | Current state |
|---|---|
| Canonical High-Assurance program | **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0** |
| Canonical DGAF efficacy | **NOT ESTABLISHED** |
| Track A Epoch 001 prospective collection | **COMPLETE / BLINDED / RETAINED** |
| Epoch 001 inferential seed units | **50** |
| Epoch 001 blinded raw observations | **2,250** |
| Epoch 001 dataset lock | **ESTABLISHED** |
| Epoch 001 protected mapping recoverability | **CRYPTOGRAPHICALLY UNRECOVERABLE** |
| Epoch 001 unblinded analysis input | **CANNOT BE MATERIALIZED FROM RETAINED EVIDENCE** |
| Epoch 001 primary analysis | **UNANALYZABLE / NOT RUN** |
| Epoch 001 outcome aggregation | **NOT PERFORMED** |
| Successor Track A lane | **ISSUE #523 OPEN — EPOCH 002 RUNNER + CUSTODY-V2 TOOLING MERGED; REAL RECOVERY EVIDENCE ABSENT** |
| Successor empirical collection | **NOT AUTHORIZED** |
| B1 standalone non-empirical lane | **COMPLETE** |
| B2 standalone non-empirical lane | **COMPLETE** |
| B3 standalone non-empirical lane | **COMPLETE** |
| Track C composition | **MERGED NON-EMPIRICAL PROPOSAL** |
| Track C empirical execution | **NOT AUTHORIZED** |

No row above establishes independent validation, production certification, integrated DGAF efficacy, High-Assurance authorization, or a completed Track A primary result.

## Track A Epoch 001 — immutable historical prospective collection

Epoch 001 was prospectively preregistered and collected under the locked topology-robustness protocol.

Locked design:

- 50 prospective seeds: `20270101..20270150`
- 5 topologies: ring, PDMAL, random-regular, small-world, complete
- 9 failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`
- 45 cells per seed
- 2,250 blinded raw observations
- algorithm: `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`
- primary endpoint: strict-boolean `ffcr_success`
- primary comparison: PDMAL vs matched random-regular
- locked analysis: 10,000 paired percentile-bootstrap resamples, seed `20270151`, alpha `0.05`

The collection remains valid evidence that the prospective blinded panel was executed and retained. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**.

### Established Epoch 001 chain

Epoch 001 legitimately established:

1. prospective preregistration;
2. locked primary-analysis implementation;
3. hardened fail-closed runner;
4. stabilized candidate;
5. precollection preflight — **PASS**;
6. immutable freeze — **ESTABLISHED**;
7. final closure — **ESTABLISHED**;
8. verification — **PASS / DEVELOPER SELF-ATTESTED / NONINDEPENDENT**;
9. collection authorization — **ESTABLISHED**;
10. prospective blinded collection — **COMPLETE**;
11. dataset lock / collection receipt — **ESTABLISHED**;
12. unblinding authorization — **ESTABLISHED historically** for mapping release/decryption;
13. materializer, receipt, custody-key-preflight, and primary-analysis-authorization tooling — **MERGED / VALIDATED**.

Those historical gates are not revoked. The later custody adjudication changes what can still be recovered and analyzed from the retained evidence.

### Custody/recovery failure

Issue #496 is now **CLOSED / NOT PLANNED** as `[UNRECOVERABLE] Track A Epoch 001 unblinded-input materialization`.

The accepted collection path generated a fresh 256-bit topology-blinding secret at runtime, retained the protected topology mapping only inside a CMS-encrypted protected bundle, and destroyed the plaintext protected directory/tar after encryption. The retained artifact contains ciphertext, certificate, and digest commitments, but no recoverable private-key escrow.

The actual operating model is solo. No separate authorized key holder or recoverable copy of the matching CMS private key has been established. A newly generated key cannot match the retained certificate/ciphertext, and the HMAC-keyed topology/order mapping cannot be honestly reconstructed from the public blinded dataset without guessing.

Therefore:

- `TRACK_A_EPOCH_001 = BLINDED_COLLECTION_COMPLETE / CRYPTOGRAPHICALLY_UNRECOVERABLE_FOR_UNBLINDING`
- `TRACK_A_EPOCH_001_PRIMARY_ANALYSIS = UNANALYZABLE / NOT_RUN`
- protected mapping/key recovery must **not** use brute force, guessing, inference, regenerated keys, or reconstruction;
- Epoch 001 must **not** be pooled into a successor confirmatory analysis;
- canonical DGAF efficacy remains **NOT ESTABLISHED**.

The custody failure is itself an engineering/governance finding. It does not erase the successful blinded collection or dataset lock, and it does not create an efficacy result.

## Successor Track A — issue #523

Issue #523, `Track A: replace unrecoverable Epoch 001 with recoverable solo-custody successor`, is the controlling scientific-design lane.

The successor uses a new epoch/protocol identity and fresh seeds/blinding while preserving the locked endpoint, estimand, matrix semantics, and prospective analysis boundaries unless separately justified before outcome access.

Merged non-empirical successor work now includes:

- Epoch 002 primary-analysis implementation lock under PR #585;
- fail-closed Epoch 002 runner and machine contract under PR #591;
- custody schema v2 hardening and exact runner/custody-source rebinding under PR #597, merge `bdd213b9437dbe6bb65e0035a9de3dfd456e145c`.

The custody-v2 implementation requires recovery evidence for both encrypted user-controlled backup copies, explicit distinct storage classes, per-backup container/public-key identity checks, and a timezone-qualified recovery record. Legacy schema-v1 evidence cannot satisfy the Epoch 002 precollection custody prerequisite.

These are implementation and validation gates only. They do **not** establish a real custody key, valid operator recovery receipt/certificate, precollection preflight, candidate freeze, collection authorization, empirical collection, unblinding, primary analysis, or efficacy evidence.

Required boundaries:

- secret/passphrase/private-key material stays outside GitHub, Notion, chat, workflow inputs, logs, and committed files;
- the real recovery drill must derive the public key from each recovered encrypted private-key copy and exactly match the collection certificate before authorization;
- solo custody is explicitly **SAME_SYSTEM_NONINDEPENDENT**;
- recoverability is not independent custody;
- replacement empirical collection remains **NOT AUTHORIZED** until the new prospective gate chain is established;
- dataset lock must still precede unblinding;
- controlled materialization, immutable input receipt, and separate primary-analysis authorization remain separate later gates;
- no Epoch 001 historical pooling or outcome-driven tuning is allowed.

## Accepted Epoch 001 provenance identities

Important historical identities remain valid for their exact scope:

- frozen candidate SHA: `961b9918002c4c68afac9c0fd5dd3e352e49b926`
- frozen candidate tree: `f20fa0ffee4b47872d84ce10cc9fd05e75c7306d`
- preregistration merge: `26077b27ca336454148006e6daf4cd087005b421`
- analysis-lock merge: `e9ea59ad839aef33fbce10ed04c2157358c4326d`
- locked analysis blob: `76bc8e9604c5d7e039e324e73036f353dc8ea31f`
- freeze merge: `bea146656ff4fdd81572215fb9d2d38296ca4455`
- final closure merge: `df74ead1481dbf8a475d9e6c9a452749d7c06196`
- verification merge: `4e4d872cf17f1b2c9d39f7f5969bf395abbd7617`
- collection authorization merge: `659aaa4dea2dd42624747952f1a47f307e69a014`
- collection run: `34262408225`
- dataset-lock commit: `fbf3e2da3be0a36c1102a69c996026e95c33cceb`
- unblinding authorization merge: `2e1981870a8455abed36fd72dcb3aaa35e2f9bff`
- controlled materializer tooling merge: `f92c251bb8fcf068c644db04ae9d2f855c382caa`
- unblinded-input receipt tooling merge: `f36d746f603f95d14098322792bec074b21b54cb`
- custody-key preflight tooling merge: `498bb51ffb559145217b84be969fe74cf9f27579`
- primary-analysis authorization tooling merge: `f95fd3303535cad4e53a24854c9adf7a25b79ab5`

These SHAs identify historical apparatus/governance events; none is the moving repository main merely because it is listed here.

## Recent engineering / governance state

Recent merged work after the original Epoch 001 tooling chain includes:

- security/dependency refresh;
- Track A custody-handoff operator runbook;
- agent identity / moving scientific-state decoupling;
- non-destructive branch-disposition inventory;
- prospective weighted Forman–Ricci replication research;
- fail-closed Task-4 corpus-intake locking;
- exact-source live staging-breaker evidence capped at `PASS_STRUCTURAL_LIVE_STAGING_ONLY`;
- Vocabulary Translation Matrix v2 with active-identity coverage and vocabulary governance;
- sovereign agent-ontology adjudication and current-facing namespace migration under completed issue #522;
- Epoch 002 primary-analysis implementation lock under PR #585, without analysis authorization;
- update-safe npm lockfile integrity validation under PR #587;
- direct npm dependency-scope provenance hardening under PR #589;
- Epoch 002 fail-closed runner binding under PR #591;
- TLA+ byte-verification reliability hardening under PR #596;
- dual-backup custody-v2 implementation and runner rebinding under PR #597.

These are meaningful implementation/governance advances but have **no automatic scientific-state effect**.

## Agent identity / vocabulary boundary

Vocabulary translation is downstream of identity and authority governance. Current translation controls distinguish canonical identity, accepted alias, abstract role/archetype, state, formation seat, and historical lineage.

Issue #522 is **CLOSED / COMPLETED**. The accepted ontology contract establishes sovereign seat precedence through `docs/agents/AGENT_ROSTER.md` plus `registry/agent_ontology_adjudication.v1.json`; formation/topology identifiers remain local unless separately promoted. Sentinel and Sentinel-Phi remain distinct, `IONIA_STATE` remains a separate runtime/formation state from Agent Ionia A-13, and current-facing namespace migration is complete. Historical conflict records remain provenance rather than current unresolved state.

## B1 / B2 / B3 and Track C

B1, B2, and B3 have completed standalone non-empirical lanes. Track C has a merged non-empirical composition proposal.

These states establish integration-readiness predicates only. They do not establish empirical benefit or integrated DGAF efficacy.

`TRACK_C_EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

## Solo Epoch 004 — bounded historical evidence

`PDMAL-SOLO-CANONICAL-EPOCH-004` remains separate from Epoch 001, any successor Track A epoch, and High-Assurance.

It executed 50 paired seeds across 4 conditions × 5 topologies × 9 failure levels = 9,000 observations and produced negative evidence for its exact executed treatment:

- DGAF FFCR: `0.7337777777777778`
- null FFCR: `0.8275555555555555`
- paired effect: `-0.0937777777777778`
- two-sided 95% CI: `[-0.11822222222222223, -0.07066666666666668]`
- classification: **`EVIDENCE_AGAINST_DIRECTIONAL_DGAF`**

A later source-bound audit found canonical seven-gate treatment fidelity **NOT ESTABLISHED**. Preserve the result as exact-treatment historical evidence only.

## Evidence rules

Current-facing documentation must preserve these distinctions:

1. Architecture is not implementation.
2. Implementation is not empirical evidence.
3. A passing test proves only its defined predicate and environment.
4. Developer self-verification is not independent verification.
5. Freeze is not authorization.
6. Closure is not authorization.
7. Authorization is not execution.
8. Collection execution is not unblinding.
9. Unblinding authorization is not proof that unblinding remains recoverable.
10. A completed blinded collection may become unanalyzable if its protected mapping cannot be recovered.
11. Execution is not efficacy until the locked analysis supports that claim.
12. Historical evidence does not silently transfer to a new SHA, protocol, treatment, epoch, or evidence identity.
13. A successor experiment must not pool, infer, reconstruct, or tune from inaccessible Epoch 001 outcomes.
14. Canonical DGAF efficacy remains **NOT ESTABLISHED** until evidence satisfying that exact claim exists.

## Current next scientific gate

The next legitimate Track A transition is **real operator-controlled custody recovery evidence under schema v2**, not additional custody-tool design and not Epoch 001 decryption or analysis.

Issue #523 must next establish the real non-secret custody recovery receipt/certificate evidence from the operator-controlled recovery drill. Only after that evidence validates against the merged custody-v2 and Epoch 002 runner contracts may the successor proceed to the remaining precollection preflight, candidate-freeze, closure/verification, and separate collection-authorization gates.

At this moment:

- Epoch 001 collection remains **COMPLETE / BLINDED / RETAINED**;
- Epoch 001 unblinding is **CRYPTOGRAPHICALLY UNRECOVERABLE**;
- Epoch 001 primary analysis is **UNANALYZABLE / NOT RUN**;
- Epoch 002 analysis implementation, runner, and custody-v2 contract are **MERGED / VALIDATED AS NON-EMPIRICAL IMPLEMENTATION**;
- real Epoch 002 custody recovery evidence is **NOT ESTABLISHED**;
- successor Track A empirical collection is **NOT AUTHORIZED**;
- canonical DGAF efficacy remains **NOT ESTABLISHED**;
- High-Assurance remains **NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0**.

## Public terminology

For the industry-neutral map from project-local vocabulary to functional descriptions, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md) and `VOCABULARY_TRANSLATION_MATRIX.json`.

Older dated status documents are historical snapshots unless they explicitly identify themselves as current authority.
