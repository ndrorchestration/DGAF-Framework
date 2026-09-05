> **Historical snapshot / superseded for present-state use — 2026-09-05:** This file preserves the 2026-09-01 candidate-readiness assessment and its then-current identities. It is not current gate authority. The current designated runtime candidate is `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`; present gate state is controlled by `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`, `docs/experiment/NEW_CANDIDATE_MANIFEST.md`, and `docs/CURRENT_STATE.md`. The historical P3/P5/P6/P9 dispositions below must not be reused as current state.

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
- Fresh PDMAL dry run for `a43219b…`: `33572123862`, completed successfully after rerun.
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

- P3: structural/dry-run evidence present; latest artifact `9825740072`, ZIP digest `sha256:1a9f520bac2bf12ca8386c5c050489620028657866e4fee66e64905507ec31ae`.
- P4: workflow/synthetic evidence present; blinding secret was present without disclosure and masked output was generated. Full operational custody/separation closure remains OPEN.
- P5: workflow/synthetic evidence present; RNG stream separation, deterministic reproduction, exact artifact binding, and environment fingerprint were recorded. Inner CSV digest: `c12098da63ae1508edbb350799360e1edccfebb16c9d0faf0db4d593ffea8ce2`.
- P6: workflow custody evidence present; the exact artifact was downloaded and the inner CSV checksum was recomputed successfully. Durable external archive closure remains OPEN / FAIL-CLOSED.
- Latest evidence-registry artifact: `9825740649`, ZIP digest `sha256:c6c2fda4ce18d476ef95927a1430193ef34631dcce928c15695d43826678a205`.
- Structural/artifact suite: `19 passed`.

The trusted external completion controller is conservative: it must not promote P4/P5/P6 from dry-run `VERIFIED` labels to closure because the current governance checklist requires candidate-bound operational evidence and, for P6, durable external archive retrieval and retention binding.

## P7 / P8 / P9

- P7 scientific target: technically adjudicated / proposed authoritative specification / **FORMALLY OPEN**. The authoritative traceability matrix records all 11 decisions as OPEN / pending authority adoption; exact candidate/protocol/analysis/freeze binding remains required.
- P8: OPEN / FAIL-CLOSED until current-candidate TGL/P-35 and analysis/protocol bindings are verified.
- P9 current scoped pass: run `33572123857` against `a43219b…` completed successfully. It verified exact checkout identity, independent `jq -S -c` + `sha256sum` canonicalization/hash, 4 authority-identity regression tests, external authorization representation, and no empirical execution request. Latest artifact `9825660346`; ZIP digest `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`.
- P9 independent canonical digest: `f235fc6ef241379f295676d257c22c7b17a47ace47377506fac9a7e5d490215a`.
- Broader P9 closure remains open because the full evidence graph, including current-candidate runtime/binding and analysis-lock prerequisites, is not yet closed.

## Trusted completion-controller state

Trusted controller run `33573171970` successfully evaluated candidate SHA `a43219b4ed91fff8615f6c655ab3d17ca871fc29` as immutable workflow-run input and reconciled P9. That run was produced before the later conservative controller fix `436da0a8fa5ea417778919a37d19eb12a8ad3285`, so its P4/P5/P6 promotability result is superseded by the fixed evaluator logic. No new external controller event was emitted by the subsequent reruns observed in this audit.

The current trusted-evaluator contract therefore treats the blocking set as at least: **P2 OPEN, P4 OPEN, P5 OPEN, P6 OPEN, P7 OPEN, P8 FAIL_CLOSED**, while P3 and scoped P9 have exact-candidate evidence present. Freeze and pilot authorization remain false.

## Candidate reseed rule

Any commit after a candidate-bound verification creates a new exact candidate identity for closure purposes. Documentation-only changes are still candidate identity changes when committed to the controlled completion branch because the verification boundary is the exact Git commit under test. Evidence must therefore be regenerated or explicitly re-established for the new SHA rather than inherited.

## Historical-priority boundary

The historical-priority adjudication remains a separate research track. It does not authorize execution and must not be strengthened by post-cutoff implementation evidence.

## Critical path

`select intended candidate → exact-candidate deployment + P2/P6a binding → P3/P4/P5/P6 closure evidence → P7 exact authority binding → P8 verification → broader P9 closure → immutable freeze → explicit authorization → blinded pilot`

## Hard boundary

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**

No state in this record authorizes empirical execution or unblinding.
