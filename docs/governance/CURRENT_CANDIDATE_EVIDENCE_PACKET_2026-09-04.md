# Current-Candidate Evidence Packet — 2026-09-04

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED  
**Latest reconciliation:** 2026-09-05  
**Purpose:** Define and track the exact evidence packet for the designated executable runtime candidate without promoting historical evidence or generating empirical observations.

## Operating practice

The evidence process follows `docs/governance/EVIDENCE_OPERATING_PRINCIPLES.md`: identity before inference, evidence before status, unknown stays unknown, verification is distinct from efficacy, and independent challenge precedes irreversible transitions. These are operating practices for the existing P1–P9 process, not additional gates.

## Identity boundary

| Identity | Value | Role |
|---|---|---|
| Corrected apparatus source | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | Canonical provenance anchor |
| Consolidated control-state anchor | `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` | Consolidated control-state lineage anchor |
| Latest evidence-producing main tip | `821878759797d0bfda2ae7a8bced980bd02c58a9` | Control-plane/workflow definition identity; not the runtime candidate |
| Verified executable runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Designated executable identity |
| Candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | Exact runtime-candidate tree |
| Deployment reference | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Vercel production deployment, freshly live-retrieved 2026-09-05 |
| Deployment source SHA | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Vercel-reported Git source match |

## 2026-09-05 reconciliation

Current-candidate evidence has materially advanced:

- **P1 CLOSED / VERIFIED** — candidate/tree/apparatus provenance is self-bound and the recorded production deployment was independently live-retrieved from Vercel as READY and sourced from exact candidate `7c1cc4bb…`.
- **P3 CLOSED / VERIFIED** — authoritative main run `33939955138` executed the exact-candidate artifact-contract and 180-cell/adversarial schema fixtures; artifacts `9961526468` and `9961526662` are retained and source-bound.
- **P4 OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT** — main run `33939574283` verifies synthetic mock-key blinding/bijection/leakage/freeze-order controls, but actual human/key custody and access separation are not established.
- **P5 OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT** — run `33939955138` verifies exact candidate/tree, protocol/dependency identity, toolchain/environment, deterministic reproduction, RNG stream separation, and topology determinism; final analysis implementation/configuration binding remains pre-freeze work.
- **P6 CLOSED / VERIFIED** — finalized current-candidate evidence was archived to an independent Google Drive location, retrieved as raw bytes, independently SHA-256 hashed, and matched byte-for-byte.
- **P7 ADOPTED / FINAL BINDING OPEN; P8 OPEN / FAIL-CLOSED; P9 OPEN.**
- **Freeze NOT ESTABLISHED; pilot authorization NOT GRANTED; empirical N=0.**

## Historical runtime evidence — provenance retained, live deployment now confirmed

Repository records previously cited P2/P6a evidence for the exact candidate/deployment pair. The exact Vercel deployment itself is now independently live-retrievable and candidate-bound, but the historical GitHub Actions artifacts below have not been freshly re-retrieved through the current verification path and their authenticated matrices have not been freshly re-executed.

### P2 — Execution Contract / Runtime

- Historically recorded workflow run: `33730195621`
- Historically recorded artifact: `9883521704`
- Historically recorded artifact digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`
- Candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- Current state: **HISTORICAL RECORD / CURRENT ARTIFACT RETRIEVAL UNCONFIRMED**

### P6a — Runtime / CORS

- Historically recorded workflow run: `33728695806`
- Historically recorded artifact: `9882965299`
- Historically recorded artifact digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`
- Candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- Current state: **HISTORICAL RECORD / CURRENT ARTIFACT RETRIEVAL UNCONFIRMED**

No P1/P3/P6 closure here depends on relabeling those historical runtime artifacts as current.

## Current-candidate packet

### P3 — Artifact contract

Required retained evidence:

- candidate SHA and tree SHA;
- protocol identity/version;
- artifact schema version;
- complete required-field validation;
- record uniqueness/cardinality checks;
- canonical matrix checks;
- exclusion/deviation consistency;
- per-record environment fingerprint requirements;
- cryptographic artifact digest and deterministic sidecar;
- exact producing workflow run and artifact identity.

**Current state: CLOSED / VERIFIED.**

Evidence:

- candidate `7c1cc4bb…`, tree `586c00d6…`;
- canonical pre-freeze schema blob `41a90485246bbc1e7e13829fc1791133da5c3d4c`, schema version `1.0`;
- pilot artifact schema blob `c620d3755a645c5f2ad14124f42ce07a1c670c5f`, schema version `1.0`;
- main workflow run `33939955138`;
- source artifact `9961526468`, ZIP SHA-256 `ed947f8a2f21a1e1122a6e8950240ea4a3ebdec7aad04c4231698de2f250285b`, inner evidence SHA-256 `d6b7c85a80a2ecf8e857431ab1b132d2dd703176cb481c0e67fbc0d067fe3175`;
- source-bound registry artifact `9961526662`, ZIP SHA-256 `d7f592b45e76978600b6f1a4f22cac4b97dfe5f60605accbd99b61c50e149e93`;
- exact-candidate tests passed required fields, exclusion consistency, environment/hash constraints, canonical coordinates, four-condition balance, duplicate rejection, 180-record/seed matrix integrity, FFCR/recovery semantics, and adversarial artifact-integrity rejection.

See `docs/experiment/P3_ARTIFACT_CONTRACT_ATTESTATION_2026-09-05.md`.

### P4 — Blinding and custody

Required retained evidence:

- blinding-key operational procedure;
- custody/access separation;
- bijection/label mapping verification;
- mock-key or equivalent non-production operational verification;
- no cleartext condition leakage in retained pre-freeze surfaces;
- explicit custody record and timestamps;
- exact implementation/configuration identity.

**Current state: OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT.**

Main run `33939574283` and artifacts `9961339739` / `9961339938` establish synthetic operational behavior with a mock key. They do not establish actual human/key custody or access separation. That missing operational fact remains a real blocker and is not inferable from CI.

### P5 — Reproducibility and provenance

Required retained evidence:

- exact candidate/source/tree identity;
- protocol identity and protocol blob digest;
- analysis implementation identity;
- analysis configuration identity;
- dependency lock identity;
- Python/runtime/toolchain identity;
- topology generator and RNG seeds;
- environment fingerprint;
- exact workflow run/artifact identity;
- deterministic reproduction result.

**Current state: OPEN / CURRENT-CANDIDATE EVIDENCE PRESENT.**

Run `33939955138` supplies the candidate/tree, protocol, dependency-lock, runtime/toolchain, RNG/topology, environment-fingerprint, producer/artifact, and deterministic-reproduction portions. The analysis control plan and P8 lock record still require final analysis implementation SHA/configuration SHA binding at the analysis-lock boundary. P5 is therefore not promoted to CLOSED yet.

### P6 — Durable evidence custody

Required retained evidence:

- archive target identity;
- archived artifact bytes;
- archive object/content digest;
- independent retrieval event;
- recomputed digest after retrieval;
- equality result;
- retrieval timestamp and provenance;
- durable location/reference.

**Current state: CLOSED / VERIFIED.**

The finalized P3/P5 and P4 source/registry artifacts were stored in Google Drive folder `1cbmvw8abh6m09M9YZRbRZ4kvsBlH2BLL`, retrieved independently as raw ZIP bytes, and SHA-256 re-hashed. Every retrieved digest exactly matched its original GitHub artifact digest. See `docs/experiment/P6_DURABLE_CUSTODY_ATTESTATION_2026-09-05.md`.

### P7 — Scientific binding

The adopted scientific target remains:

- primary contrast: `dgaf` vs `null`;
- primary endpoint: FFCR;
- statistical unit: root seed;
- estimand: paired seed-level FFCR difference;
- direction: higher FFCR favors DGAF;
- primary inference: two-sided 95% percentile paired bootstrap;
- bootstrap resamples: `10,000`;
- deterministic bootstrap seed: `20260823`;
- alpha: `0.05`;
- directional support: positive estimate with CI entirely above zero.

These definitions are protocol/control decisions, not evidence that the effect exists.

**Current state: ADOPTED / FINAL BINDING OPEN.** P4 and final P5 binding remain prerequisites.

### P8 — Analysis lock

Required final lock tuple:

```text
candidate_sha
apparatus_source_sha
protocol_identity + protocol_blob_sha
analysis_implementation_sha
analysis_configuration_sha
artifact_schema_identity
primary_contrast
estimand
bootstrap_parameters
missing/exclusion rules
multiplicity policy
freeze identity
```

No post-unblinding modification is permitted without invalidating the lock and triggering a new governance decision.

**Current state: OPEN / FAIL-CLOSED.**

### P9 — Independent verification

Independent verification must inspect the fully bound current evidence chain, including candidate/apparatus/deployment identity, P3, P4, P5, P6, P7, P8, invariants/adversarial cases, and historical/non-transferable boundaries.

Historical P9 evidence for `a43219b4…` is not current P9 evidence.

**Current state: OPEN.**

## Freeze and authorization barrier

No freeze is created by this packet. No authorization is granted by this packet. No unblinding is permitted. No empirical observation is created or counted.

The remaining transition is:

`P4 + final P5 binding → P7 final binding → P8 → P9 → immutable freeze → explicit authorization → blinded pilot`

P2/P6a remain separately historical/current-retrieval-limited runtime evidence and must not be silently promoted.

**Empirical N remains 0.**

## Historical evidence exclusion

The prior completion workflow artifacts from run `33572123862` and prior P9 artifacts from run `33572123857` were produced for candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`. They remain historical/non-transferable and are not promoted into this packet.

## Source references

- `docs/governance/EVIDENCE_OPERATING_PRINCIPLES.md`
- `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md`
- `docs/experiment/PDMAL_ANALYSIS_CONTROL_PLAN.md`
- `docs/experiment/NEW_CANDIDATE_MANIFEST.md`
- `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md`
- `docs/evidence/PDMAL_EVIDENCE_INDEX.md`
- `docs/evidence/PDMAL_DEPLOYMENT_IDENTITY_VERIFICATION_2026-09-05.md`
- `docs/experiment/P3_ARTIFACT_CONTRACT_ATTESTATION_2026-09-05.md`
- `docs/experiment/P6_DURABLE_CUSTODY_ATTESTATION_2026-09-05.md`
- `experiments/pdmal_pilot/artifact_schema.py`
- `experiments/pdmal_pilot/pilot_artifact_schema.py`
