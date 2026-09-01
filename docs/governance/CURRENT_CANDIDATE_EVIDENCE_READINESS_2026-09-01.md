# DGAF/PDMAL — Current-Candidate Evidence Readiness — 2026-09-01

## Scope

This record is a non-authorizing control/evidence assessment for the current runtime and completion candidates. It does not create empirical observations, freeze the apparatus, grant authorization, or change empirical N.

## Exact identity chains

### Mainline runtime candidate

- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Corrected apparatus tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`
- Current runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a`
- Current runtime candidate tree: `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- Current P2/P6a production deployment: `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`
- Candidate lineage: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1 → 92ff830b1c67413df745e37087e6447c9c251b9a`

### Completion candidate

- Latest completion candidate before reseed: `562753b3053b3566b0fcad1b0b1df151d7de119a`
- Latest reseeded completion candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`
- Branch: `completion/2026-09-01-exact-candidate`
- PR: `#187`
- The prior P9 result `33567199896` is scoped exclusively to `562753b…`.
- Fresh P9 run for `a43219b…`: `33572123857`, queued at the latest reconciliation check.
- No prior P9 result transfers to `a43219b…`.

## Verified mainline runtime evidence

### P2
- Run: `33509348174`
- Artifact: `9800942933`
- Digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`
- State: VERIFIED
- Required matrix: 5/5 passed
- Fail-closed case: `valid_missing_audit` → HTTP 503 / `BLOCKED`

### P6a
- Run: `33509416955`
- Artifact: `9800972819`
- Digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`
- State: VERIFIED
- Required matrix: 4/4 passed
- Allowed-origin preflight: HTTP 204
- Disallowed-origin preflight: HTTP 403

## P3–P6 current-candidate rule

The mainline PDMAL dry-run `33516447975` is valid supporting evidence for candidate `da40b085…` only. It does not close P3–P6 for `92ff830b…` or the completion candidates.

The completion branch contains the PDMAL instrumentation workflow and has been reseeded with candidate `a43219b…`. Its resulting workflow evidence must be judged exclusively by the exact new run SHA/artifact pair. The P9 workflow for this candidate is also independently triggered and remains subject to exact-SHA reconciliation.

P3, P4, P5, and P6 remain open for the intended pilot candidate until fresh exact-candidate evidence is retained and reconciled.

## P7 / P8 / P9

- P7 scientific target: adopted; exact final candidate/protocol/analysis/freeze binding remains open.
- P8: OPEN / FAIL-CLOSED until current candidate TGL/P-35 and analysis/protocol bindings are verified.
- P9: `562753b…` has scoped independent verification PASS from run `33567199896`; fresh candidate `a43219b…` has run `33572123857` queued. Broader P9 closure remains conditional on the full evidence graph and final candidate selection.

## Candidate reseed rule

Any commit after a candidate-bound verification creates a new exact candidate identity for closure purposes. Documentation-only changes are still candidate identity changes when committed to the controlled completion branch because the verification boundary is the exact Git commit under test. Evidence must therefore be regenerated or explicitly re-established for the new SHA rather than inherited.

## Historical-priority boundary

The historical-priority adjudication remains a separate research track. It does not authorize execution and must not be strengthened by post-cutoff implementation evidence.

## Critical path

`select intended candidate → current-cycle P3/P4/P5/P6 evidence → P7 exact binding → P8 verification → P9 scoped + broader closure → new immutable freeze → explicit authorization → blinded pilot`

## Hard boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**

No state in this record authorizes empirical execution or unblinding.
