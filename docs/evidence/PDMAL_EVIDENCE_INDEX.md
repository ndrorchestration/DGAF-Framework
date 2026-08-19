---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-19
applies_to_sha: 915e454e27eb2770e7f40a067a881b0783feaae4
verification_evidence:
  - PR #65 merge baseline 915e454e27eb2770e7f40a067a881b0783feaae4
  - Runtime Run #14 (32112658368)
  - Durable artifact checksum verified from Run #14 artifact 9315467977
  - Blinding operational verification Run 32113226935 / artifact 9328114023
scope_note: >
  This index is synchronized to the PR #65 merge baseline
  915e454e27eb2770e7f40a067a881b0783feaae4. Individual evidence remains
  scoped to its exact tested SHA; later documentation commits do not
  retroactively change or promote historical evidence.
---

# PDMAL Evidence Index

## Purpose

This index records the evidence boundary for the PDMAL pre-freeze control plane. GitHub is authoritative for exact implementation and CI evidence; Notion is authoritative for governance state and cross-project control state. Evidence is never promoted by documentation alone.

## Merge Baseline Record

PR #65 was merged into `main` at commit `915e454e27eb2770e7f40a067a881b0783feaae4`. This is the repository merge baseline / freeze target baseline, not the eventual freeze commit and not empirical evidence. Subsequent documentation synchronization commits remain distinct provenance events.

## Evidence Boundary

A passing run is scoped to its exact executed SHA. Later commits do not inherit verification automatically.

## Current Evidence

| Evidence | Status | Exact executed SHA | Run / artifact | Scope |
|---|---|---|---|---|
| Environment lock | VERIFIED | `7ba0e1c` | Pre-freeze runner validation | Locked installation / resolver reproducibility |
| PDMAL implementation | VERIFIED | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` | Run #74 (`32111556449`) | ConsensusTask implementation and artifact integrity |
| Runtime characterization | OPERATIONALLY CHARACTERIZED | `a0ff248` | Run #14 (`32112658368`) | 72/72 seed matrix trials; ceiling characterization |
| Blinding operational verification | CLOSED / PASS | `1d8c62386ea09f09c1dac768e1e59d4df284edee` | Run `32113226935`, artifact `9328114023` | Synthetic custody dry-run; no production secret access; no empirical data |
| Durable retention | OPEN | — | Release pending | Durable archive requires published release assets and checksum verification |

## Runtime Characterization

Run #14 (`32112658368`) completed the registered 72/72 runtime characterization matrix. The retained artifact is `runtime_characterization.json` and its authoritative file SHA-256 is:

`f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea`

The earlier recorded digest beginning `42da1112` was incorrect and is superseded. Direct extraction of artifact `9315467977` from Run #14 produced `runtime_characterization.json` with SHA-256 `f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea`; the accompanying `runtime_characterization.json.sha256` sidecar contains the same digest.

The runtime characterization is operational evidence only. It does not authorize empirical execution.

## Blinding Gate

The dedicated blinding operational test passed on the specified synthetic custody dry-run under workflow run `32113226935` with artifact `9328114023`. No production secret was accessed and no empirical data were collected. This closes the blinding operational verification control without changing the empirical boundary.

## Retention Gate

The durable retention gate remains OPEN until the research archive is established and independently verified according to `docs/experiment/PDMAL_RETENTION_POLICY.md`. The intended release assets are:

- `runtime_characterization.json`
- `runtime_characterization.json.sha256`

The release must be created against source commit `a0ff248eadb736f9b5835f2436791dc6ab5f66cc`, workflow run `32112658368`, with the authoritative file SHA above recorded in the release description. The gate closes only after the published release asset is independently checked and the sidecar digest matches.

The eventual pilot raw dataset is a separate future research record; it does not yet exist and cannot be represented as already archived.

## Empirical Boundary

Empirical data remains `0`. No pilot execution is authorized until the protocol freeze and explicit pilot authorization are complete.

## Evidence Rule

`IMPLEMENTED` does not mean `VERIFIED`; `VERIFIED` does not mean `OPERATIONALLY CHARACTERIZED`; operational verification does not mean empirical support. Documentation alone cannot promote a gate.
