# Documentation Synchronization Record — 2026-09-01

## Purpose

Record the documentation synchronization performed after the latest exact-candidate verification cycle. This record is itself historical provenance and does not alter experimental authorization or gate state.

## Controlled candidate at synchronization start

- Candidate SHA: `566273c6c2906bdf71827381493a26ee7697034c`
- Branch: `completion/2026-09-01-exact-candidate`
- PR: #187 (draft; unmerged)

## Documentation surfaces synchronized

### `README.md`

Updated to identify PR #187 and the controlled candidate, describe the PDMAL/P5/P9/completion-controller verification architecture, state the current gate board, and explicitly preserve the pre-freeze / fail-closed / N=0 boundary.

### `docs/PROJECT_STATUS.md`

Updated the project status date, current candidate, exact provenance rules, current gate states, recursive verification architecture, latest CI defect, and current closure sequence. Historical E2b/M6 evidence remains explicitly historical and non-transferable.

### `docs/CURRENT_STATE.md`

Replaced stale post-#160/post-#162 identity language with the current PR #187 control-plane candidate boundary. Recorded the superseded `cea9e49…` cycle, current verification machinery, the malformed one-seed PDMAL command, and the fail-closed closure sequence.

### `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md`

Reconciled the P1–P9 matrix to the current candidate and removed stale claims that the older `05fa286…` candidate was current. Current P2–P6/P6a/P9 remain open; P7 remains an external decision; P8 remains fail-closed.

### `docs/experiment/P5_REPRODUCIBILITY_RECORD.md`

The existing current version was inspected and confirmed to retain the required fresh-candidate boundary: P5 remains open until successful exact-candidate execution. No historical evidence was promoted.

## Latest engineering finding recorded

The latest PDMAL candidate-bound run passed its substantive deterministic structural tests, artifact generation/custody checks, and registry generation. The final one-seed structural dry-run command then failed because the embedded Python shell command is malformed by missing terminating quoting.

Classification: **CI implementation defect**.

This is not empirical failure, does not increase empirical N, and does not justify predicate promotion. The correct remediation is a narrowly scoped new candidate followed by a fresh complete verification cycle.

## Governance boundary preserved

- No evidence was copied across candidate SHAs.
- No gate was manually promoted.
- No freeze was created.
- No pilot authorization was granted.
- No blinding material was exposed.
- No empirical experiment was executed.
- Empirical N remains `0`.

## Next action

Repair the malformed PDMAL structural dry-run invocation using unambiguous shell quoting (preferably a heredoc), create the resulting new candidate, and rerun the candidate-bound PDMAL → P9 → completion-controller chain.