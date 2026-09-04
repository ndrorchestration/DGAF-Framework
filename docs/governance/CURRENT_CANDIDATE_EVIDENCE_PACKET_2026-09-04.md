# Current-Candidate Evidence Packet — 2026-09-04

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
**Purpose:** Define the exact evidence packet required for the verified executable runtime candidate without promoting historical evidence or generating empirical observations.

## Operating practice

The evidence process follows `docs/governance/EVIDENCE_OPERATING_PRINCIPLES.md`: identity before inference, evidence before status, unknown stays unknown, verification is distinct from efficacy, and independent challenge precedes irreversible transitions. These are operating practices for the existing P1–P9 process, not additional gates.

## Identity boundary

| Identity | Value | Role |
|---|---|---|
| Corrected apparatus source | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | Canonical provenance anchor |
| Consolidated control-state anchor | `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` | Consolidated control-state lineage anchor |
| Main tip at packet creation | `363d203c839746e89a7a6d3f6ba608730d42deea` | Current repository `main` tip |
| Verified executable runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Candidate identity referenced by historical P2/P6a records |
| Candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | Exact candidate tree referenced by prior records |
| Historical deployment reference | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | Prior deployment identity referenced by repository records |
| Deployment source SHA | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | Prior recorded source match |

## Historical runtime evidence — provenance retained, live retrieval not independently confirmed

Repository records previously cited the following P2/P6a evidence for the exact candidate/deployment pair. In the current verification pass, the Actions run/artifact lookup endpoints did **not** return those records. Therefore this packet preserves the identifiers as **historical repository assertions**, not as newly re-verified live artifacts.

### P2 — Execution Contract / Runtime

- Historically recorded workflow run: `33730195621`
- Historically recorded artifact: `9883521704`
- Historically recorded artifact digest: `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`
- Candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- Repository-record state: **HISTORICAL / NOT CURRENTLY RETRIEVABLE VIA THIS VERIFICATION PATH**

### P6a — Runtime / CORS

- Historically recorded workflow run: `33728695806`
- Historically recorded artifact: `9882965299`
- Historically recorded artifact digest: `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`
- Candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- Repository-record state: **HISTORICAL / NOT CURRENTLY RETRIEVABLE VIA THIS VERIFICATION PATH**

No current claim in this packet depends on independently re-verifying those run/artifact endpoints. Any future promotion of P2/P6a to currently verified evidence must include a successful retrieval path or a separately retained immutable evidence copy with independent provenance.

## Required current-candidate packet

### P3 — Artifact contract

Required retained evidence:

- candidate SHA and tree SHA;
- protocol identity/version;
- artifact schema version;
- complete required-field validation;
- record uniqueness/cardinality checks;
- canonical matrix checks;
- exclusion/deviation consistency;
- per-record environment fingerprint;
- cryptographic artifact digest and deterministic sidecar;
- exact producing workflow run and artifact identity.

**Current state:** OPEN. No current-candidate P3 execution artifact is asserted by this record.

### P4 — Blinding and custody

Required retained evidence:

- blinding-key operational procedure;
- custody/access separation;
- bijection/label mapping verification;
- mock-key or equivalent non-production operational verification;
- no cleartext condition leakage in retained pre-freeze surfaces;
- explicit custody record and timestamps;
- exact implementation/configuration identity.

**Current state:** OPEN. The repository control specification exists, but operational closure is not inferred from specification presence.

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

**Current state:** OPEN. Current repository specifications define the required binding; a fresh current-candidate packet is still required.

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

Repository-local artifact retention and a sidecar digest alone do not close P6.

**Current state:** OPEN / FAIL-CLOSED.

### P7 — Scientific binding

The current adopted scientific target is:

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

**Current state:** ADOPTED / FINAL BINDING OPEN.

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

**Current state:** OPEN / FAIL-CLOSED.

### P9 — Independent verification

Independent verification must inspect the fully bound current evidence chain, including:

- candidate/apparatus/deployment identity;
- P3 artifact evidence;
- P4 operational custody evidence;
- P5 reproducibility evidence;
- P6 durable round-trip evidence;
- P7 scientific binding;
- P8 locked analysis identity;
- invariants and adversarial cases;
- historical/non-transferable boundaries.

Historical P9 evidence for `a43219b4…` is not current P9 evidence.

**Current state:** OPEN.

## Freeze and authorization barrier

No freeze is created by this packet. No authorization is granted by this packet. No unblinding is permitted. No empirical observation is created or counted.

The required transition remains:

`P3 → P4/P5/P6 → P7 final binding → P8 → P9 → immutable freeze → explicit authorization → blinded pilot`

**Empirical N remains 0.**

## Historical evidence exclusion

The prior completion workflow artifacts from run `33572123862` and the prior P9 artifacts from run `33572123857` were produced for candidate `a43219b4ed91fff8615f6c655ab3d17ca871fc29`. They remain historical/non-transferable and are not promoted into this packet.

## Source references

- `docs/governance/EVIDENCE_OPERATING_PRINCIPLES.md`
- `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md`
- `docs/experiment/PDMAL_ANALYSIS_CONTROL_PLAN.md`
- `docs/experiment/NEW_CANDIDATE_MANIFEST.md`
- `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md`
- `docs/evidence/PDMAL_EVIDENCE_INDEX.md`
- `experiments/pdmal_pilot/artifact_schema.py`
