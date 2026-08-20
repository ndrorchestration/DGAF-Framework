---
status: ACTIVE
 authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-20
applies_to_sha: 3510b86889cd341f7a7cf9ab684fd37b2fafd758
---

# DGAF-Framework / PDMAL — Current State

This is the concise operational snapshot. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact executed SHA. The frozen experimental apparatus is bound to freeze commit `3510b86889cd341f7a7cf9ab684fd37b2fafd758`; subsequent documentation-only commits do not modify or redefine that frozen apparatus.

## Current authoritative state

| Gate | Status | Evidence / note |
|---|---|---|
| PR #75 | MERGED | `a44e42cd3040a822656e724c8b47aa02221baf3f` |
| Executor implementation | CLOSED | `75a7f18c2d5268075e6fc8064eb9a79018845da0`; `run_pilot.py` invokes `ConsensusTask` |
| Executor acceptance | CLOSED | 2 seeds × 180 trials = 360 acceptance observations; all SUCCESS; N remains 0 |
| Freeze | CLOSED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Frozen apparatus | VERIFIED | Exact executor/component SHAs recorded in `FREEZE_MANIFEST.md` |
| Blinding operational verification | CLOSED / PASS | Run `32113226935`; synthetic custody verification only |
| Runtime characterization | VERIFIED FOR CHARACTERIZATION | Run `32112658368`; artifact `9315467977`; 300s ceiling characterized |
| Environment | VERIFY | Frozen lock specifies Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1; current dev environment may differ |
| Security adversarial suite | FINAL VERIFICATION | Security report controls should be executable tests against the frozen apparatus; no apparatus modification after freeze |
| Primary contrast | MUST BE CLOSED BEFORE PILOT | Must be explicitly adjudicated before authorization/execution |
| Topology fingerprints | VERIFY / RECONCILE | Fingerprint provenance exists; final frozen values must be checked against the freeze manifest and protocol |
| Durable retention | VERIFY / RECONCILE | Retention policy exists; pilot archive location and checksum procedure must be directly verified |
| Analysis implementation | MUST BE FROZEN BEFORE UNBLINDING | Statistical plan exists; implementation/configuration SHA must be recorded before unblinding |
| Pilot authorization | NOT GRANTED | Separate governance decision after pre-authorization verification |
| Empirical data | 0 | Acceptance/characterization observations are not pilot data |

## Frozen apparatus boundary

Freeze commit: `3510b86889cd341f7a7cf9ab684fd37b2fafd758`.

Executor implementation: `75a7f18c2d5268075e6fc8064eb9a79018845da0`.

Post-freeze rule: do not modify the experimental apparatus. Verification tests may be added/run externally. If verification identifies an apparatus defect requiring code changes, the freeze must be invalidated and a new freeze created after repair and re-verification.

## Pilot matrix

```text
Conditions:      null, simple, static, dgaf
Topologies:      ring, pdmal, random_regular, small_world, complete
Failure counts:  0, 1, 2, 3, 4, 5, 6, 8, 10
Trials/seed:     180
Pilot seeds:     50
Expected pilot records: 9,000
Out of scope:    dgaf_pdmal
```

## Evidence boundary

The 360-observation executor acceptance run demonstrates that the frozen task path can execute and produce valid artifacts. It does not establish PDMAL efficacy. Empirical N remains `0` until an explicitly authorized pilot is executed.

Runtime characterization and blinding evidence remain scoped to their exact workflow runs and artifacts. They are operational/governance evidence, not efficacy evidence.

## Immediate next actions

1. Complete environment verification in the locked Python 3.12.0 environment.
2. Run the final one-seed smoke test against the frozen apparatus.
3. Formalize and execute the remaining security/adversarial tests without modifying frozen experimental code.
4. Reconcile primary contrast, topology fingerprints, and durable-retention controls against the frozen manifest/protocol.
5. Freeze the statistical analysis implementation/configuration SHA before unblinding.
6. Produce the pre-authorization verification record.
7. Obtain explicit pilot authorization.
8. Execute the 50-seed pilot only after authorization.
9. Validate and lock raw data before unblinding.
10. Perform formal unblinding, then execute the frozen analysis.

**Empirical data remains 0. No pilot authorization is currently granted.**
