---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-21
applies_to_sha: 23ab411d6113b3281f011f6891fb9335c7b6972e
scope_note: >
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run that produced it. Candidate verification does
  not inherit historical verification automatically.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current repository | CURRENT | `23ab411d6113b3281f011f6891fb9335c7b6972e` | v1.8.0 pre-authorization hardening release |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` | Historical apparatus only |
| Corrected runner | CANDIDATE | PR #77 lineage | Requires refresh/re-verification against current main |
| Environment lock | VERIFY | Python 3.12.0; NumPy 2.5.1; NetworkX 3.6.1 | Fresh candidate environment verification required |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368` | Operational characterization, not empirical efficacy |
| Blinding operational verification | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935` | Synthetic custody only; production key custody remains separate |
| Artifact contract | PARTIAL | Pilot schema + tests | Runtime inline validation and candidate verification remain required |
| Durable retention | OPEN | Archive destination not established | Direct write/retrieval/hash evidence required |
| Primary contrast | OPEN | `PRIMARY_CONTRAST_ADJUDICATION.md` | Scientific decision required before freeze |
| Analysis lock | OPEN | No final implementation/configuration SHA | Must close before unblinding |
| Independent verification | NOT EXECUTED | P9 audit design | Must verify candidate-scoped evidence |

## Runtime characterization provenance

The latest repository reconciliation records:

- Release ZIP SHA-256: `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20`
- Inner `runtime_characterization.json` SHA-256: `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`
- Run: `32112658368`
- Artifact: `9315467977`

These values supersede the earlier conflicting `f6db...` record in this control-plane registry. A fresh byte-level recomputation from the release asset should be performed before the final freeze packet when the release asset is available; this registry does not convert a recorded digest into new evidence.

## Evidence boundary

Acceptance, runtime-characterization, synthetic blinding, topology, and security-test evidence may establish engineering or operational properties. None establishes empirical PDMAL efficacy. Empirical N remains `0` until an explicitly authorized 50-seed pilot occurs.
