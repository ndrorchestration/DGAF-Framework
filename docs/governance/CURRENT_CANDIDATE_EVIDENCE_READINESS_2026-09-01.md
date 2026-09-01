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
- Prior P9 `33567199896` is scoped exclusively to `562753b…`.
- Fresh P9 run for `a43219b…`: `33572123857`, completed successfully.
- Fresh PDMAL dry run for `a43219b…`: `33572123862`, completed successfully.
- No prior candidate evidence transfers to `a43219b…` without explicit re-binding.

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

## Current completion-candidate P3–P6 evidence

Fresh exact-candidate PDMAL run `33572123862` succeeded on `a43219b4ed91fff8615f6c655ab3d17ca871fc29`.

- P3: VERIFIED in the workflow registry; artifact `9825367738`, ZIP digest `sha256:51b89e5321674ff19eecc53a4445237677025649fe36ed5ddc762835a24c2c6c`.
- P4: VERIFIED at workflow/synthetic scope; the blinding secret was present without disclosure and masked output was generated. Full operational custody/separation closure remains distinct.
- P5: VERIFIED in the workflow registry; RNG stream separation, deterministic reproduction, exact artifact binding, and environment fingerprint were recorded. Inner CSV digest: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.
- P6: VERIFIED at workflow custody scope; the exact artifact was downloaded and the inner CSV checksum was recomputed successfully. Durable external archive closure remains separate.
- Structural/artifact suite: `19 passed`.
- Controller evaluation promoted P3/P4/P5/P6 as exact-candidate evidence while keeping P2/P7/P8/P9 blocking.

The prior mainline PDMAL dry run `33516447975` remains supporting evidence only for `da40b085…`; it does not substitute for the fresh exact-candidate run.

## P7 / P8 / P9

- P7 scientific target: adopted; exact final candidate/protocol/analysis/freeze binding remains open.
- P8: OPEN / FAIL-CLOSED until current candidate TGL/P-35 and analysis/protocol bindings are verified.
- P9 current scoped pass: run `33572123857` against `a43219b…` completed successfully. It verified exact checkout identity, independent `jq -S -c` + `sha256sum` canonicalization/hash, 4 authority-identity regression tests, external authorization representation, and no empirical execution request. Artifact `9825316781`; ZIP digest `sha256:15e5ba72dd524f90b0bb3499c9b0b3f7de602f0e1905b0734183e830c22af671`.
- P9 independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.
- Broader P9 closure remains open because the full evidence graph, including current-candidate runtime/binding and analysis-lock prerequisites, is not yet closed.

## Candidate reseed rule

Any commit after a candidate-bound verification creates a new exact candidate identity for closure purposes. Documentation-only changes are still candidate identity changes when committed to the controlled completion branch because the verification boundary is the exact Git commit under test. Evidence must therefore be regenerated or explicitly re-established for the new SHA rather than inherited.

## Historical-priority boundary

The historical-priority adjudication remains a separate research track. It does not authorize execution and must not be strengthened by post-cutoff implementation evidence.

## Critical path

`select intended candidate → current-cycle P2/P6a binding if needed → P3/P4/P5/P6 evidence → P7 exact binding → P8 verification → broader P9 closure → immutable freeze → explicit authorization → blinded pilot`

## Hard boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**

No state in this record authorizes empirical execution or unblinding.
