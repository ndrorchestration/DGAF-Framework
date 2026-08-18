---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: 458bb346569937455b796977dc571af17b64da65
verification_evidence:
  - Runtime Run #14 (32112658368)
scope_note: >
  This index records evidence and gate state synchronized at
  458bb346569937455b796977dc571af17b64da65. Individual evidence
  remains scoped to its exact tested SHA; later documentation commits
  do not inherit verification automatically.
---

# PDMAL Evidence Index

## Purpose

This index records the evidence boundary for the PDMAL pre-freeze control plane. GitHub is authoritative for exact implementation and CI evidence; Notion is authoritative for governance state and cross-project control state. Evidence is never promoted by documentation alone.

## Evidence Boundary

A passing run is scoped to its exact executed SHA. Later commits do not inherit verification automatically.

## Current Evidence

| Evidence | Status | Exact executed SHA | Run / artifact | Scope |
|---|---|---|---|---|
| Environment lock | VERIFIED | `7ba0e1c` | Pre-freeze runner validation | Locked installation / resolver reproducibility |
| PDMAL implementation | VERIFIED | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` | Run #74 (`32111556449`) | ConsensusTask implementation and artifact integrity |
| Runtime characterization | OPERATIONALLY CHARACTERIZED | `a0ff248` | Run #14 (`32112658368`) | 72/72 seed matrix trials; ceiling characterization |
| Blinding operational verification | OPEN | — | No dedicated run yet | Synthetic dry-run required |
| Durable retention | OPEN | — | No durable archive verification yet | Research archive required |

## Runtime Characterization

Run #14 (`32112658368`) completed the registered 72/72 runtime characterization matrix. The retained artifact is `runtime_characterization.json` and its file SHA-256 is:

`42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`

The runtime characterization is operational evidence only. It does not authorize empirical execution.

## Blinding Gate

The blinding operational dry-run remains OPEN. The synthetic workflow must demonstrate that the blinding mechanism can execute without exposing the secret key and that custody evidence is retained.

## Retention Gate

The durable retention gate remains OPEN until the research archive is established and independently verified according to `docs/experiment/PDMAL_RETENTION_POLICY.md`.

## Empirical Boundary

Empirical data remains `0`. No pilot execution is authorized until the protocol freeze and explicit pilot authorization are complete.

## Evidence Rule

`IMPLEMENTED` does not mean `VERIFIED`; `VERIFIED` does not mean `OPERATIONALLY CHARACTERIZED`; operational verification does not mean empirical support. Documentation alone cannot promote a gate.
