# Canonical Candidate Identity Chain — DGAF/PDMAL (2026-08-30)

**Authoritative source for apparatus/candidate identity.** All P3–P9 records MUST bind to the
identities declared here, not to historical SHAs cited in older issues.

## Current experimental candidate (post-#151 reconciliation)

| Role | SHA | Tree | Notes |
|------|-----|------|-------|
| Designated apparatus commit | `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` | — | PR #151 squash-merge into `main` |
| Designated apparatus tree | — | `dd662325149c42843d5ca99178ca4399fde6f440` | **experiments bind here** |
| Designation-record commit | `02c146d1e0cdc423948ac0dfa11e98f812edfb44` | `a2610c72…` | this manifest doc (metadata, NOT apparatus) |

**Canonical rule:** the *designated apparatus tree* `dd662325` is the identity P3–P8/P9 verification
binds to. The merge commit `05fa286` is the apparatus commit; `02c146d` is only the record that
designated it. These are three distinct identities — never conflate.

## Historical (superseded) identities — DO NOT use as current

| SHA | Was | Now |
|-----|-----|-----|
| `303f4424d2198f0d0cf76305c589263dd1e417dc` | production engineering source / P2-P6a verification boundary | HISTORICAL production; P2/P6a VERIFIED scope only, does NOT extend to experimental candidate |
| `2ec12b214c64775c105d4abb69fdbab77a5de52c` | prior `main` documentation tip | HISTORICAL |
| `c6157158bf0ee4840e99a381a4b99bd2febe2302` | pre-remediation designated candidate | HISTORICAL / PRE-REMEDIATION; its P3–P9 package is NOT transferred (see `CANDIDATE_RECONCILIATION_RECORD.md`) |
| `874db1a…` / `4b62916…` | prior freeze attempts | HISTORICAL; self-declared PRE-FREEZE, not authoritative freezes |

## Provenance principle

> A commit is not a deployment. A deployment is not runtime verification. Runtime verification is
> not empirical efficacy. A designated candidate is not authorized. (Echoes `docs/EVIDENCE_STATUS_2026-08-30.md`.)

**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0. New candidate designated; not frozen,
not authorized, empirical N=0.
