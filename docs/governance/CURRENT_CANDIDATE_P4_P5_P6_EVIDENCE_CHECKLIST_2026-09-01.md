# Current-Candidate P4/P5/P6 Evidence Checklist — 2026-09-01

## Scope

Non-authorizing evidence-planning/control record for the current runtime candidate. This document does not create empirical observations, freeze the apparatus, grant authorization, unblind any condition, or change empirical N.

## Exact identity boundary

- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Current runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`
- Candidate tree: `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- P2/P6a verified deployment: `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`

## P4 — Security / blinding

### Implementation evidence

- Current runner requires an externally supplied `PDMAL_BLINDING_KEY` for pilot mode.
- Missing blinding key fails closed.
- Condition identifiers are HMAC-derived and emitted as blinded identifiers.
- Pilot execution removes the blinding key from the process environment after obtaining it, reducing downstream exposure.

### Current-cycle closure evidence still required

- [ ] Exact candidate-bound execution demonstrating the blinding procedure.
- [ ] Evidence of operational key custody and access separation.
- [ ] Independent recomputation/verification of blinded-condition bijection without exposing the key in retained public evidence.
- [ ] Evidence that no premature unblinding occurred.
- [ ] Exact candidate/deployment/protocol identity attached to the retained record.

## P5 — Provenance / reproducibility

### Implementation evidence

- Separate topology and failure RNG streams are derived deterministically.
- Runner records an environment fingerprint from runtime versions.
- Pilot artifact records require a frozen commit SHA and environment fingerprint.
- Artifact records bind experiment ID, protocol version, candidate SHA, seed, and environment fingerprint.

### Current-cycle closure evidence still required

- [ ] Exact-candidate reproducibility execution retained.
- [ ] Independently recomputed environment fingerprint.
- [ ] Topology/failure stream separation independently checked at the candidate boundary.
- [ ] Deterministic rerun comparison retained.
- [ ] Exact protocol/environment/dependency identity captured without secret disclosure.

## P6 — Durable evidence custody

### Implementation evidence

- `PDMAL_ARCHIVE_ROOT` is required for pilot-mode retention.
- Retention requires a full freeze SHA.
- Archive writes are checksum-verified immediately after copy.
- Retrieval and independent SHA-256 round-trip verification are implemented.

### Current-cycle closure evidence still required

- [ ] Current-candidate evidence artifact placed into the configured durable archive.
- [ ] Independent retrieval from that archive.
- [ ] Independently recomputed SHA-256 equality across source/archive/retrieved bytes.
- [ ] Retention manifest bound to the exact applicable freeze/candidate identity.
- [ ] No secret values included in retained evidence.

## Independence rule

CI may validate validators and deterministic implementation properties. Current P4/P5/P6 closure requires evidence-level observations on the actual candidate-bound artifacts/environment/custody path, with independent checks where the predicate requires them.

## Promotion rule

No P4/P5/P6 gate may be promoted from `OPEN` merely because implementation exists, a historical artifact exists, a documentation commit succeeds, a deployment is healthy, or a related prior candidate passed the same conceptual check.

## Current boundary

**P4 OPEN · P5 OPEN · P6 OPEN / FAIL-CLOSED**  
**PRE-FREEZE · NOT AUTHORIZED · empirical N = 0**
