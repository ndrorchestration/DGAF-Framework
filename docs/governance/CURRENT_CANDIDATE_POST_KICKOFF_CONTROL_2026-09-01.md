# Current-Candidate Post-Kickoff Control — 2026-09-01

This is a non-authorizing control record created after the completion-audit kickoff documentation commit.

## Critical identity distinction

The completion-audit documentation commit `4062006d13e0f8211bfd57eb0be92d24ed349b03` is documentation-only and is not promoted to runtime candidate status merely because it is on `main`.

The current mainline runtime candidate remains `92ff830b1c67413df745e37087e6447c9c251b9a` with exact tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` and production deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` for the current P2/P6a evidence.

A separate controlled completion candidate `562753b3053b3566b0fcad1b0b1df151d7de119a` on `completion/2026-09-01-exact-candidate` has a scoped P9 independent-verification PASS via run `33567199896`. These identities are separate and no evidence transfers automatically.

## New execution requirement

Because documentation and completion work continue on `main` and the completion branch, any future candidate-scoped verification must explicitly resolve whether it targets:

1. the existing mainline runtime candidate `92ff830b…`, or
2. the controlled completion candidate `562753b…`, or
3. a newly selected candidate explicitly rebound through governance.

No evidence from an existing deployment may be silently rebound to a different candidate.

## Latest P9 disposition

Run `33567199896` completed successfully against exact candidate `562753b…` and verified:

- exact checkout identity (`HEAD == GITHUB_SHA`);
- independent `jq -S -c` + `sha256sum` canonicalization/hash agreement;
- authority-identity regression (`4 passed`);
- retained/uploaded P9 evidence artifact `9823570326` with ZIP digest `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`.

This is **scoped P9 verification**, not full P9 closure, freeze, authorization, or empirical evidence.

## Disposition

- Existing P2/P6a evidence: remains valid for exact candidate `92ff830b…` / deployment `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.
- P3/P4/P5/P6 current-cycle evidence: open until bound to the selected pilot candidate.
- P7: adopted / final exact binding open.
- P8: open / fail-closed.
- P9: scoped PASS for `562753b…`; broader closure remains open.
- Freeze: not established.
- Authorization: not granted.
- Empirical N: 0.

## Cross-references

- `P1_TO_P9_EVIDENCE_MATRIX.md`
- `P8_VERIFICATION_CHECKLIST.md`
- `P9_LATEST_RECONCILIATION_2026-09-01.md`
- `../CURRENT_STATE.md`
