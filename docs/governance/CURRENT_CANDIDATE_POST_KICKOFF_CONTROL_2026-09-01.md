> **Historical snapshot / superseded for present-state use — 2026-09-05:** This post-kickoff record preserves the 2026-09-01 candidate/control state and exact evidence then under review. It is not current authority. The current designated runtime candidate is `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`; use `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md`, `docs/experiment/NEW_CANDIDATE_MANIFEST.md`, and `docs/CURRENT_STATE.md` for present state.

# Current-Candidate Post-Kickoff Control — 2026-09-01

This is a non-authorizing control record created after the completion-audit kickoff documentation commit.

## Critical identity distinction

The completion-audit documentation commit `4062006d13e0f8211bfd57eb0be92d24ed349b03` is documentation-only and is not promoted to runtime candidate status merely because it is on `main`.

The current mainline runtime candidate remains `92ff830b1c67413df745e37087e6447c9c251b9a` with exact tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` and production deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` for the current P2/P6a evidence.

The separate controlled completion candidate is now `a43219b4ed91fff8615f6c655ab3d17ca871fc29` on `completion/2026-09-01-exact-candidate`. It has exact-candidate PDMAL instrumentation evidence and scoped P9 independent-verification evidence. These identities are separate and no evidence transfers automatically.

## New execution requirement

Because documentation and completion work continue on `main` and the completion branch, any future candidate-scoped verification must explicitly resolve whether it targets:

1. the existing mainline runtime candidate `92ff830b…`, or
2. the controlled completion candidate `a43219b…`, or
3. a newly selected candidate explicitly rebound through governance.

No evidence from an existing deployment may be silently rebound to a different candidate.

## Latest exact-candidate verification

PDMAL instrumentation run `33572123862` completed successfully against exact candidate `a43219b…`. The latest rerun produced artifact `9825740072` with ZIP digest `sha256:1a9f520bac2bf12ca8386c5c050489620028657866e4fee66e64905507ec31ae` and evidence registry artifact `9825740649` with ZIP digest `sha256:c6c2fda4ce18d476ef95927a1430193ef34631dcce928c15695d43826678a205`.

P9 run `33572123857` completed successfully against exact candidate `a43219b…`. The latest P9 evidence artifact is `9825660346` with ZIP digest `sha256:cf5e475c31bd9258731dcec3e6f36588f9fbfa80c3bb787419b54770ccae7976`, and its independent canonicalization/hash path plus authority-identity regression passed.

The trusted completion controller is active on `main`. Its successful evaluation bound the triggering workflow evidence to `a43219b…` and returned `OPEN_GAPS`; no freeze or pilot authorization was granted.

## Disposition

- Existing P2/P6a evidence: remains valid for exact candidate `92ff830b…` / deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.
- P3: exact-candidate structural/dry-run evidence present; broader closure remains governed separately.
- P4: OPEN — dry-run blinding evidence is not operational closure.
- P5: OPEN — dry-run reproducibility evidence is not full closure.
- P6: OPEN / FAIL-CLOSED — durable external archive round-trip remains required.
- P7: technically adjudicated / formally OPEN; authority adoption and exact freeze binding remain required.
- P8: OPEN / FAIL-CLOSED.
- P9: scoped PASS for `a43219b…`; broader closure remains open.
- Freeze: not established.
- Authorization: not granted.
- Empirical N: 0.

## Cross-references

- `P1_TO_P9_EVIDENCE_MATRIX.md`
- `P8_VERIFICATION_CHECKLIST.md`
- `P9_LATEST_RECONCILIATION_2026-09-01.md`
- `../CURRENT_STATE.md`
