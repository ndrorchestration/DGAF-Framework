---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_sha: c6157158bf0ee4840e99a381a4b99bd2febe2302
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run that produced it. Candidate verification does
  not inherit historical verification automatically. Production provenance
  is closed for the merged engineering source, while experimental evidence
  for the designated candidate remains separately gated.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current documentation lineage | CURRENT | `main` | Active control/documentation lineage |
| Current designated pre-freeze candidate | DESIGNATED / NOT FROZEN | `c6157158…` / `experimental-candidate/2026-08-30-reconciled` | Exact target for the next candidate-scoped evidence cycle |
| Production source provenance | CLOSED / VERIFIED | `303f4424…` → Vercel `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8` | Engineering/production source; not the current experimental candidate |
| Historical experimental verification boundary | HISTORICAL / CANDIDATE-SCOPED | `ac8ea267…` | Historical pre-freeze apparatus evidence; not silently promoted |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b868…` | Historical apparatus only |
| P8 checklist ancestor | HISTORICAL LINEAGE | `2a80f819…` | Ancestor of integrated engineering source; not a competing apparatus identity |
| Corrected pilot runner | IMPLEMENTED / EVIDENCE GATED | `pilot_artifact_schema.py` + runner controls | Explicit FFCR outcome, schema/sidecar validation, matrix semantics; current candidate execution evidence still gated |
| TGL contract | CURRENT ENGINEERING CONTROL / VERIFIED | `303f4424…` lineage | Repaired semantics validated in engineering CI; not experimental authorization |
| Environment lock | VERIFY | CI dependency/runtime configuration | Final candidate must bind exact environment fingerprint |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368` | Operational characterization, not efficacy evidence |
| Blinding operational verification | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935` | Synthetic/control evidence only |
| Artifact contract | IMPLEMENTED / OPEN | `pilot_artifact_schema.py` + tests | Structural contract implemented; fresh current-candidate execution evidence required |
| Security controls | VERIFIED FOR ENGINEERING SCOPE | Current Governance/PDMAL security CI | Does not substitute for P4 operational custody |
| Topology provenance | VERIFY | `PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` | Recompute/bind against exact designated candidate |
| Durable retention | OPEN | Policy present | Operational archive + independent retrieval/hash proof required |
| Primary contrast | ADJUDICATED / BINDING PENDING | `dgaf` vs `null`; FFCR; paired seed | Scientific target selected; exact candidate/freeze binding remains required |
| Analysis lock | OPEN / FAIL-CLOSED | P8 control plan | Exact final candidate/configuration binding required |
| P2 runtime | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33300481208`; artifact `9728767844`; candidate `303f4424…` | Authenticated five-case matrix passed; retained as exact prior-candidate evidence only |
| P6a CORS runtime | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33302495240`; artifact `9729387603`; candidate `303f4424…` | Four live CORS cases passed; retained as exact prior-candidate evidence only |
| Independent verification | NOT EXECUTED | P9 design | Must verify the designated candidate evidence chain independently |

## Candidate identity reconciliation

The SHA discrepancy has been resolved as a lineage issue rather than two competing mainline apparatus trees.

- `2a80f819…` is an ancestor of `303f4424…` and represents the earlier P8 checklist lineage.
- `303f4424…` is the integrated engineering/production source and the exact source bound by the verified prior P2/P6a runtime evidence.
- `255d76f6…` was the mainline documentation/evidence tip observed during reconciliation and descended from `303f4424…`.
- `c6157158…` is the explicitly designated current pre-freeze candidate and is the target for fresh candidate-scoped evidence.

## P2 evidence boundary

P2 is **VERIFIED** for the exact runtime boundary exercised by run `33300481208`, job `99227568599`, artifact `9728767844`, digest `sha256:cdbf23bf2a754034c9f5f5651b9242c22814669962a43bd59c409a0f7bf610a5`, candidate `303f4424d2198f0d0cf76305c589263dd1e417dc`, and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`.

All five required cases passed and the artifact records `all_pass = true`. This is exact prior-candidate evidence. It is **not** current-candidate evidence for `c6157158…`.

## P6a evidence boundary

P6a is **VERIFIED** for run `33302495240`, artifact `9729387603`, digest `sha256:4abaf5d1c32930738296a85d38f5489b2068127795e2ce5e2c30565f2308533c`, candidate `303f4424…`, and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. It remains exact prior-candidate runtime/CORS evidence and does not silently transfer to `c6157158…`.

## Current candidate execution boundary

The designated candidate is `c6157158bf0ee4840e99a381a4b99bd2febe2302`. A candidate-specific Vercel deployment must reach READY with exact Git source SHA `c6157158…` before candidate-scoped runtime evidence can be accepted.

The first observed deployment for `c6157158…` was `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ` and was still `BUILDING` at inspection time. Therefore no current-candidate P2/P6a completion is claimed from that deployment.

## Evidence boundary

Historical acceptance, characterization, synthetic blinding, topology, security, P2, and P6a runtime evidence may establish engineering or operational properties. None establishes empirical PDMAL efficacy. Empirical N remains `0` until the explicit authorization chain is completed and a valid paired pilot observation is accepted.

## Remaining gate sequence

1. Obtain a READY deployment whose source SHA exactly matches `c6157158…`.
2. Fresh P2 runtime verification on `c6157158…`.
3. Fresh P6a CORS verification on `c6157158…`.
4. Candidate-scoped P3 artifact-contract execution evidence.
5. P4 operational blinding/custody verification.
6. P5 environment/topology/RNG reproducibility verification.
7. P6 durable archive/retrieval/hash verification.
8. P7 exact scientific/protocol/apparatus/analysis binding.
9. P8 exact analysis lock and closure.
10. Independent P9 verification.
11. New immutable freeze and independent freeze verification.
12. Explicit pilot authorization.
13. Authorized blinded pilot execution.

**Prior P2/P6a: VERIFIED at `303f4424…`. Current candidate: `c6157158…`, designated but not yet runtime-verified. P3–P6 evidence-gated. P8 OPEN / FAIL-CLOSED. P9 NOT EXECUTED. Empirical N: 0. Pilot authorization: NOT GRANTED. Freeze: NOT CREATED.**
