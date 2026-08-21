---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-20
applies_to_sha: c1862ffc22b2b877794e146a753075057f920132
---

# PDMAL Current Control State

This is the operational gate record. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. The historical implementation freeze at `3510b868...` remains historical evidence only because material pilot-runner corrections were required.

## Gate board

| Control | State | Evidence / blocker |
|---|---|---|
| Historical implementation freeze | SUPERSEDED FOR CORRECTED RUNNER | `3510b868...`; retained as historical evidence |
| Corrected runner | CANDIDATE | `fec7a6f...`; requires CI and re-freeze |
| Frozen pilot artifact schema | CANDIDATE | `pilot_artifact_schema.py` |
| Security adversarial controls | CANDIDATE | `test_security_controls.py`; requires CI execution |
| Environment lock | VERIFY | Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1 |
| Topology provenance | VERIFY | Reconcile final fingerprints against manifest/protocol |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Existing 300s ceiling evidence is non-empirical |
| Blinding primitive | VERIFIED | Deterministic HMAC primitive exists |
| Blinding operational custody | OPEN | Protected mapping/access-control mechanism requires direct evidence |
| Durable retention | VERIFY | Archive destination/checksum path requires direct evidence |
| Primary contrast | OPEN / MUST CLOSE | Explicit methodological adjudication required |
| Analysis implementation | PENDING FREEZE | Exact implementation/configuration SHA not recorded |
| Protocol freeze | PENDING RE-FREEZE | New freeze required after corrected runner verification |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | 0 | No authorized pilot execution |

## Corrected-runner boundary

The old freeze cannot be silently reused because the live audit found material runner defects: no exact frozen-SHA binding and pilot artifacts labeled as pre-freeze while exposing the real condition. Those defects are corrected on the pre-authorization branch. The corrected runner is therefore a new freeze candidate.

## Critical path

1. CI/security suite.
2. Fresh Python 3.12.0 environment verification.
3. One-seed smoke test and pilot-artifact schema validation.
4. Topology fingerprint reconciliation.
5. Durable retention verification.
6. Primary-contrast adjudication.
7. Analysis implementation/configuration SHA freeze.
8. New freeze manifest.
9. Pre-authorization verification record.
10. Explicit pilot authorization.

**No empirical execution is authorized by this state record.**
