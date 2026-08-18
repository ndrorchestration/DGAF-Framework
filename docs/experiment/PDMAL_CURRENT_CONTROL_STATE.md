# PDMAL Current Control State

_Last synchronized: 2026-08-18 02:51 EDT_

This document records the current evidence boundary for the PDMAL pre-freeze program. GitHub Actions evidence is authoritative for execution state; historical runs are not promoted to current-head evidence.

## Current branch

- Branch: `epistemic/evidence-architecture-v1`
- Workflow guard correction: `24d2df49bc49c1ec4ef66eeeaa1b5de168c2a77d`
- Fresh Actions run for that correction is not currently observable through the connected GitHub Actions API.

## Lockfile diagnosis

Run #51 (`32104280611`) executed commit `225f5c32a08f36c8a5f6bd63739bc20d6e5a24b4` and failed because the newline-only placeholder lockfile passed the previous `test -s` check. Resolver generation was skipped and `pytest` was unavailable.

The workflow guard has now been corrected to require:

- a non-empty lockfile;
- indented SHA-256 hash entries;
- pinned `numpy`;
- pinned `networkx`;
- pinned `pytest`;
- pinned `pandas`.

The lockfile itself must remain resolver-generated and must not be manually fabricated.

## Gate board

| Control | State |
|---|---|
| Historical adapter/contract CI | VERIFIED historically |
| Environment lock | OPEN |
| Topology provenance | IMPLEMENTED / fresh CI PENDING |
| Artifact schema | IMPLEMENTED |
| Artifact retention | 30-day workflow retention / long-term policy OPEN |
| Blinding custody | DOCUMENTED / operational test OPEN |
| Runtime characterization | OPEN |
| Experimental task adapter | NOT IMPLEMENTED |
| Protocol audit | COMPLETED |
| Protocol freeze | BLOCKED |
| Pilot authorization | NOT GRANTED |
| Empirical data | 0 |

## Critical path

1. Generate genuine hash-complete lock on a network-enabled GitHub runner.
2. Verify fresh current-head CI and successful `--require-hashes` installation.
3. Adjudicate and implement the real workload/task adapter.
4. Characterize runtime on the real workload.
5. Complete blinding operational verification and long-term retention decision.
6. Assemble freeze packet.
7. Freeze protocol and implementation.
8. Explicitly authorize the blinded pilot.
9. Execute empirical work only after authorization.

No empirical execution is authorized by this state record.
