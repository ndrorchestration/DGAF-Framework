# DGAF/PDMAL Project Status

**Status date:** 2026-08-20  
**Repository:** `ndrorchestration/DGAF-Framework`  
**Current main:** `df7d5fd8c8595cbb9d0c04caeaace13738d760ae`  
**Pilot status:** PRE-FREEZE; authorization not granted

## Purpose

This document is the current operational status record for the DGAF/PDMAL experimental track. It supersedes informal status summaries while preserving historical release and session records.

## Current Gate Board

| Gate / control | Status | Evidence / state |
|---|---|---|
| v0.7.5 runtime characterization | CLOSED | Published release `v0.7.5-pdmal-runtime-characterization` |
| Durable retention | PUBLISHED | GitHub Release exists with runtime characterization asset |
| Blinding operational test | CLOSED | Verified synthetic custody dry-run; no production secret or empirical data |
| Environment lock | CLOSED | Runs #67/#68 |
| Topology provenance | VERIFIED | Runs #67/#68 |
| Artifact schema/integrity | VERIFIED | Run #74 |
| ConsensusTask implementation | VERIFIED | Run #74; SHA `08500a7` |
| Runtime 300-second ceiling | VERIFIED | Characterized maximum 646 ms; mean 503 ms |
| Evidence Card schema | PRESENT | `docs/evidence/EVIDENCE_CARD_SCHEMA.json` |
| Evidence Index | RECONCILED | Corrected SHA prefix `5b94a07c...` |
| Protocol matrix | FROZEN IN DESIGN | `4 × 5 × 9 = 180` observations/seed; 9,000 for 50 seeds |
| `dgaf_pdmal` | OUT OF SCOPE | Explicitly excluded from the pilot scope |
| Empirical data | ZERO | No pilot data generated |
| Security hardening #70 | MERGED | Main baseline `93f535c1eb822244ab4e7d3646cadfb9e28a9876` |
| Epistemic architecture #65 | MERGED | Main baseline `915e454e27eb2770e7f40a067a881b0783feaae4`; PR #65 merged 2026-08-19 |
| PR #75 | MERGED | Squash-merged at `a44e42cd3040` on 2026-08-20; 113 files, 7427 insertions; executor gap remains OPEN |
| Release ZIP SHA-256 | VERIFIED | `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20` — computed from downloaded `pdmal-runtime-characterization-4a7d00b84693807306f639e9c818f4604517e840.zip` on 2026-08-20; prior record `cbd2cb...` was INCORRECT — corrected |
| Inner artifact SHA-256 | VERIFIED | `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea` — computed from extracted `runtime_characterization.json`; ZIP-shipped sidecar confirms; prior record `f6db24e...` was INCORRECT — corrected |
| Freeze manifest | UPDATED | Post-#65 freeze HEAD `915e454e`; release asset digests verified and corrected on 2026-08-20; freeze commit not yet created |
| Protocol freeze | BLOCKED | Depends on #65, provenance checks, and freeze commit |
| Pilot authorization | NOT GRANTED | Must reference the final freeze state |

## Provenance Identities

These identities must remain separate:

1. **v0.7.5 release/tag identity** — immutable runtime-characterization baseline.
2. **Published release asset identity** — SHA-256 of the ZIP asset itself.
3. **Inner runtime artifact identity** — SHA-256 of `runtime_characterization.json` if that is the authoritative artifact contained by the ZIP.
4. **Pilot freeze identity** — post-#65 Git `HEAD` SHA that defines the exact state authorized for the pilot.

The expected inner-artifact SHA supplied by the prior CI provenance record is:

```text
f6db24e5dd2659d4395c0752845e23f1823aa674980abb20074d4d443de01250
```

This value is **expected provenance**, not a substitute for a fresh local computation. The ZIP's SHA-256 must also be computed independently because the ZIP and its contents are different byte objects.

**Correction (2026-08-20):** Fresh computation from the downloaded release asset yields different values:
- ZIP SHA-256: `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20` (prior record `cbd2cb...` was INCORRECT)
- Inner artifact SHA-256: `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea` (prior record `f6db24e...` was INCORRECT)
- ZIP-shipped sidecar `runtime_characterization.json.sha256` confirms the inner SHA.

## Release Baseline

Release: `v0.7.5-pdmal-runtime-characterization`  
Release title: `PDMAL Runtime Characterization Artifact – v0.7.5`

The release is treated as an immutable historical baseline. Subsequent governance and security changes are not retroactively attributed to that release.

## Post-Release Repository State

### PR #70 — Security hardening

Merged into `main`.

```text
93f535c1eb822244ab4e7d3646cadfb9e28a9876
```

The change addresses the workflow permissions/code-scanning issue and establishes the current security baseline.

### PR #65 — Epistemic Alignment + Evidence Card architecture

Merged into `main` at `915e454e27eb2770e7f40a067a881b0783feaae4` on 2026-08-19.

```text
915e454e27eb2770e7f40a067a881b0783feaae4
```

The change delivers epistemic alignment policy, claim/evidence distinctions, Evidence Card architecture, validation controls, and associated documentation.

### PR #75 — Evidence architecture + governance doc updates

Open against `main`. Head `22b769a` (rebased on `origin/main` `df7d5fd`). Contains 4 modified governance/evidence documents (CURRENT_STATE.md, PDMALESPERIMENT_INDEX.md, FREEZE_MANIFEST.md, PDMAMESPERIMENT_PROTOCOL.md). PR-scope markdownlint clean. mergeable=True, mergeable_state=blocked pending CI `pptl pytest — governance`.

### PR #42 — Fractal Agency enumeration

Separate research-characterization track. It does not block the immediate security/evidence hardening sequence.

## Required Final Sequence

```text
1. Merge PR #75 (evidence architecture + governance docs)
2. Verify post-#75 HEAD on main
3. Download the published v0.7.5 ZIP
4. Compute ZIP SHA-256
5. Extract authoritative inner artifact
6. Compute inner artifact SHA-256 and compare to expected provenance
7. Populate freeze manifest
8. Mark protocol/spec frozen in the freeze commit
9. Record pilot authorization
10. Execute the 50-seed blinded pilot
```

No step in this sequence establishes empirical validity before the pilot is run and analyzed.

## Cryptographic Verification Procedure

Use the exact filename shown by the GitHub release UI.

```bash
curl -L -o release.zip '<published-release-asset-download-url>'
sha256sum release.zip
unzip release.zip runtime_characterization.json
sha256sum runtime_characterization.json
```

Record both computed digests. The inner artifact is expected to match:

```text
42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea
```

**Correction (2026-08-20):** The prior expected value `f6db24e5dd2659d4395c0752845e23f1823aa674980abb20074d4d443de01250` was INCORRECT. Fresh computation from the downloaded release asset yields `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`. The ZIP-shipped sidecar `runtime_characterization.json.sha256` independently confirms this value.

Do not claim the gate is closed until the actual computed values are recorded.

## Freeze Manifest Requirements

The final freeze manifest should record at minimum:

```yaml
freeze_commit_sha: <post-#65 HEAD>
protocol_blob_sha: <protocol file/blob identity at freeze>
spec_blob_sha: <task spec file/blob identity at freeze>
runner_blob_sha: <pilot runner identity at freeze>
lockfile_blob_sha: <full lockfile identity at freeze>
runtime_artifact_id: 9315467977
runtime_artifact_digest: 42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea (corrected; prior f6db24e... was INCORRECT)
runtime_release_tag: v0.7.5-pdmal-runtime-characterization
release_asset_filename: pdmal-runtime-characterization-4a7d00b84693807306f639e9c818f4604517e840.zip
release_asset_sha256: ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20 (corrected; prior cbd2cb... was INCORRECT)
release_inner_artifact: runtime_characterization.json
release_inner_artifact_sha256: 42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea (corrected; prior f6db24e... was INCORRECT)
blinding_run_id: 32113226935
blinding_artifact_id: 9315675249
blinding_artifact_digest: <verified blinding artifact digest>
freeze_timestamp_utc: <UTC timestamp>
authorization_record: <authorization record link>
```

## Epistemic Boundary

The repository currently establishes engineering, provenance, governance, and runtime-characterization evidence at the levels documented above. It does **not** establish empirical validity of the DGAF/PDMAL hypothesis.

```text
Empirical validity:   NOT ESTABLISHED
Pilot authorization:  NOT GRANTED
Empirical data:       0
```

The blinded pilot, once authorized and executed, is an empirical test. Its outcome must remain distinct from prior engineering verification and provenance evidence.
