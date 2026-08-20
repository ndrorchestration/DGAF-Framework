---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-20
applies_to_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
---

# PDMAL Current Control State

This document is the operational gate record. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA. The experimental apparatus was frozen at `3510b86889cd341f7a7cf9ab684fd37b2fafd758`; this post-freeze control record is documentation-only and does not modify that frozen apparatus.

## Gate board

| Control | State | Evidence / blocker |
|---|---|---|
| Environment lock | VERIFY | Frozen lock specifies Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1; verify in a fresh matching environment before pilot |
| Frozen executor | CLOSED | `75a7f18`; `run_pilot.py` invokes `ConsensusTask` |
| Executor acceptance | CLOSED | 2 seeds × 180 trials = 360; all SUCCESS; acceptance evidence only |
| Topology provenance | VERIFY | Fingerprint generation/provenance exists; reconcile final values against frozen manifest |
| Artifact schema/integrity | VERIFIED | Frozen component SHA and acceptance artifacts recorded |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368`; 300s ceiling characterized; not pilot evidence |
| Blinding custody | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935`; production secret not exposed |
| Security adversarial controls | FINAL VERIFICATION | Execute remaining controls externally against frozen apparatus |
| Durable retention | VERIFY | Policy exists; directly verify pilot archive destination/checksum path |
| Primary contrast | OPEN / MUST CLOSE | Explicit methodological adjudication required before pilot authorization |
| Analysis implementation | PENDING FREEZE | Statistical plan exists; implementation/configuration SHA must be frozen before unblinding |
| Protocol freeze | CLOSED | Freeze commit `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | 0 | No authorized pilot execution |

## Frozen apparatus rule

The frozen experimental apparatus is the implementation tree at freeze commit `3510b86889cd341f7a7cf9ab684fd37b2fafd758`, with executor implementation `75a7f18`. Post-freeze verification must not modify experimental apparatus code. If a verification finding requires an apparatus change, the freeze is invalidated and a new freeze must be established after repair and re-verification.

## Acceptance evidence boundary

The 360-observation acceptance run establishes execution-path fidelity, artifact production, provenance, and validation. It does not constitute empirical PDMAL evidence. Empirical N remains `0`.

## Critical path

1. Verify the locked Python 3.12.0 environment.
2. Run the final one-seed smoke test against the frozen apparatus.
3. Execute the remaining adversarial/security controls externally.
4. Reconcile primary contrast, topology fingerprints, and durable retention.
5. Freeze the analysis implementation/configuration SHA before unblinding.
6. Produce the pre-authorization verification record.
7. Obtain explicit pilot authorization.
8. Execute the 50-seed pilot.
9. Validate and lock raw data before unblinding.
10. Perform formal unblinding and execute the frozen analysis.

**No empirical execution is authorized by this state record.**
