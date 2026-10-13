# SBCF crash consistency and concurrency QA

Status: RESEARCH ONLY / FAIL-CLOSED / PRE-FREEZE. Issue #1338; stacked research candidate on draft #1340. Updated 2026-10-11.

## Local admission protocol

`WitnessedVerifier.admit` validates the signed envelope and declared state fields before writing. It opens the existing evidence database in read/write-only mode, attaches the existing witness database, sets `synchronous=FULL` on both, and acquires a single `BEGIN IMMEDIATE` transaction before reading either counter. Admission requires persistent, separate files and `journal_mode=DELETE` in both stores. WAL and other modes are rejected without automatic conversion. The admission row, evidence high-water and witness counter are written in this transaction and committed together. SQLite errors deny admission; closing an uncommitted connection rolls back its writes.

This uses SQLite's [attached-database atomicity](https://sqlite.org/lang_attach.html) and [multi-file rollback-journal commit protocol](https://sqlite.org/atomiccommit.html), under their filesystem, locking and flush assumptions. It is a local protocol, not a remote witness or independent trust anchor.

## Conservative recovery

A source/run whose two high-water values disagree cannot admit even a later sequence. There is no automatic healing or reconciliation endpoint. An older snapshot of only the evidence database therefore blocks subsequent admissions for the affected source/run, rather than quietly advancing both counters. Missing stores are not recreated by the admission API; corrupt or inaccessible stores deny admission. Construction initializes store schemas and can raise on corrupt databases. These are distinct behaviors.

Separate-store paths are resolved at construction; aliases, including existing hard links, are rejected. This is not protection against a hostile principal replacing files or modifying keys and counters.

## Verification

New `tests/test_sbcf_atomic_witness.py` contains 25 synthetic tests:

- A SQLite trigger aborts the witness write; admission and both high-water values remain unchanged. Removing the trigger permits a retry.
- Real child processes exit after each of the three SQL writes, immediately before commit and immediately after commit. Reopened stores agree; pre-commit attempts can be retried, committed attempts cannot replay.
- Four child processes compete for one source/run/sequence; exactly one succeeds. Existing four-thread duplicate tests also remain.
- Both directions of counter mismatch deny a later sequence. WAL in either store, missing stores, corrupt witness, memory-store configuration and hard-linked stores are tested.
- Invalid envelopes, undeclared fields, signature failures, non-finite values and out-of-range SQLite sequences do not advance counters.

Local Python 3.12.14 with the repository hash-locked QA toolchain: the complete SBCF group reports **86 passed, 3 strict xfailed, 37 subtests passed**. The red baseline was **12 failed, 3 passed** before implementation (15 initial tests; ten envelope/path/range cases were subsequently added).

The full repository `tests/` suite reports **2105 passed, 5 skipped, 3 xfailed, 7 warnings, 101 subtests passed** in 21.75 seconds. Black (Python 3.12 target), isort and changed-file whitespace checks pass. Hosted verification and the final exact head are recorded in the stacked draft PR receipt; local results do not substitute for that hosted observation.

The subprocess injections exercise application SQL/commit boundaries, not interruption inside SQLite's low-level commit, operating-system failure or physical power loss. Four competing processes are a bounded contention test, not sustained multiprocess stress. Disk-full, VFS faults, hostile filesystem replacement, independently managed custody and source-key compromise remain unverified.

## Preserved counterexamples

Three strict expected failures remain evidence of limitations, not completed protections:

1. The standalone `DurableEvidenceVerifier` can replay after its SQLite snapshot is rolled back.
2. Direct calls to `verifier.evidence.admit` bypass the witnessed transaction and can split the counters. The original fixture is retained, renamed and described accurately as a bypass counterexample; witnessed admission subsequently fences the mismatch.
3. Coordinated rollback of both host-local files can readmit an old event.

The 2026-10-09 baseline used two commits and demonstrated a split by directly advancing the evidence store. Its passing thread/signature tests did not establish atomicity. This candidate repairs the witnessed admission path within the stated local assumptions and preserves that bypass counterexample.

## Hosted failure audit — 2026-10-13

Three intermediate push runs failed during publication of this candidate. The implementation was uploaded before both legacy test expectations had been migrated. Publishing dependent files in separate commits exposed incomplete intermediate trees to CI; this was a publication sequencing mistake. The first failure remains preserved and is not replaced by the later green result.

| Run / job | Exact input commit | Hosted result | Unmigrated expectations |
| --- | --- | --- | --- |
| [38160709486 / 114532837687](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160709486/job/114532837687) | `d0d0a4463e4f1908908bcf2137a7d671c54a76a9` | 2 failed, 59 passed, 3 xfailed | Both mismatch tests still expected later admission |
| [38160710638 / 114532840736](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160710638/job/114532840736) | `079be2f644dd3a34c9ecbfa69e57d747e8267e0b` | 2 failed, 84 passed, 3 xfailed | New 25-test harness present; both legacy expectations unchanged |
| [38160711846 / 114532844515](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160711846/job/114532844515) | `3360056055632b3b7287ebdb6280e15a8b8d3eda` | 1 failed, 85 passed, 3 xfailed | Evidence-store rollback test still expected admission of sequence 3 |
| [38160713056](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160713056) | `041c7f1903a5f03c60c0d37f36514e4e37b6eec8` | PASS | Both legacy expectations now require denial |

**Classification:** incomplete test-contract migration at intermediate commits. The workflow executed the exact failing SHA, installed its hash-locked dependencies, passed formatting and returned exit code 1 for failed assertions. It failed closed. The assertion failures do not support an additional implementation repair: each observed `False` is the intended conservative recovery fence. A nonfatal Black target-version warning appeared before pytest; it was not the failed step and the finished workflow already specifies Python 3.12.

**Minimal reproduction:** an untouched worktree at the first failing SHA reproduced **2 failed, 59 passed, 3 xfailed, 37 subtests passed** (exit 1). Changing only `assert admit(verifier, 8)` and `assert admit(make(tmp_path),3)` to their `assert not` forms produced **61 passed, 3 xfailed, 37 subtests passed** (exit 0), with no implementation change. This modified tree is explicitly separate from the immutable first-failure SHA. A fresh run at code head `a283e17bfbc2696bda372a63eff7153bf2e406ba` produced **86 passed, 3 xfailed, 37 subtests passed** (exit 0).

Hosted failures used Ubuntu 24.04 image `20261004.327.1`, Python 3.12.15, pytest 9.1.1 and pluggy 1.6.0. Local reproduction used Python 3.12.14 and a newly installed full hash-locked QA environment; it is not a claim of identical hosted OS or patch version. The previous local virtual environment was absent on resume and was rebuilt before the checks.

The [evidence manifest](sbcf_ci_evidence/2026-10-11/manifest.json) binds input-file SHA-256 values, all failed job steps, three preserved decoded UTF-8 log exports with byte lengths and SHA-256 values, exact reproduction outputs and the two-assertion patch. These are decoded connector exports, not hashes of GitHub's compressed log-download bytes. Direct check-run/annotation endpoints were rejected by the connector allowlist; standalone annotations were not inspected. The accessible job logs contain assertion traces and the terminal exit-code error.

All **15 observed workflows** at code head `a283e17bfbc2696bda372a63eff7153bf2e406ba` completed successfully (10 PR runs, 5 push runs). This includes the previously pending [PDMAL pre-freeze runner 38160736737](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160736737). That historical-runtime-evidence job does not independently validate SBCF. Original exact-head SBCF [push run 38160717455](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160717455) and [PR run 38160736666](https://github.com/ndrorchestration/DGAF-Framework/actions/runs/38160736666) both passed. A documentation/evidence receipt may follow this verified code head; no implementation, test, fixture or workflow change is needed for this audit.

Next action: preserve this failure record during review; publish future dependent code/test migrations as one complete Git commit through a supported multi-file write path. Lower-level SQLite interruption, externally evidenced reconciliation and independent review remain separate open tasks.

## Windows follow-up and resource-lifetime repair — 2026-10-13

RDC on neontic tested an isolated checkout of receipt head `afec9763f90309c840fcffa446153121bcdcdeb9`, leaving the existing dirty DGAF workspace untouched. Windows x64, CPython 3.12.10, SQLite 3.49.1 and pytest 9.1.1 produced **1 failed, 85 passed, 3 xfailed, 37 subtests passed**. The failing case was `test_missing_store_is_not_recreated_during_admission[events.db]`: unlink raised `PermissionError: WinError 32` because the evidence connection remained open. Initial Windows log SHA-256: `41a357bdfa86d3200193bbe590aeeb9d52db0261d8b6971b68369896b42466d4`.

`sqlite3.Connection`'s transaction context commits/rolls back but does not close the connection. `DurableEvidenceVerifier` now uses an outer `contextlib.closing` context for initialization and admission, preserving transaction completion before deterministic connection closure. Admission rules, signed-envelope semantics, counters, schema and expected failures are unchanged. The existing Windows missing-store case is the regression test; it is not weakened or skipped.

With only the durable module changed (source SHA-256 `1f0f1237423bedd32dbd633bbe03470b9991bee9f371eb5817ddae7c9c8165b5`), the complete Windows SBCF group returned **86 passed, 3 xfailed, 37 subtests passed** (exit 0); log SHA-256 `9adbd058e92a064754dcde7032008acafb31f6f2871db21162c188f065559fd8`. Linux Python 3.12.14 full `tests/` returned **2105 passed, 5 skipped, 3 xfailed, 7 warnings, 101 subtests passed** in 34.89 seconds. Formatting/whitespace checks passed. These results identify a modified tree from the parent, not an unchanged parent-head result.

The research workflow now also runs the existing SBCF group on Windows 2022/Python 3.12. Its platform-independent pytest wheel subset is hash-locked from the canonical CI lock, with pytest's Windows-only colorama dependency explicitly pinned and hashed. A fresh virtual environment prevents dependence on preinstalled runner packages; no Linux-specific product dependency lock is applied to Windows. The initial hosted Windows job at `6aded8398a48e512ca6558521fc25b4cbb1192b4` passed but reused preinstalled colorama 0.4.6. That dependency-coverage limitation prompted the fresh-environment refinement. Hosted results must be observed at the resulting exact candidate head and recorded in its draft PR.

### Bounded native SQLite storage-fault observations

A disposable local probe constrained `max_page_count` and installed a test-only padding trigger separately in each store. SQLite itself raised `SQLITE_FULL` (code 13), rather than a mocked exception. In both cases the witnessed admission returned false, admission/high-water/counter state remained unchanged, and removing the trigger permitted one retry while a duplicate was rejected. This exercises SQLite capacity-error handling, not physical disk exhaustion, VFS write/fsync interruption, kernel crash or power loss.

The probe ran at the parent checkout plus the exact durable-source bytes above. Initial probe launch needed its script import path corrected; its own SQLite helper contexts also required deterministic closure for Windows disposable-directory cleanup. Those probe setup failures are separate from the preserved production missing-store failure. Local result SHA-256: `3b6c38dd56d46b67cf4d221282fc0624631c506b4e70dd84c4b8066ec3f5de5a`; probe script SHA-256 `9e1f111524008ef9d53a074728e39053bb121f86d2dc903c12f4421d969c5332`. This is supplementary same-owner verification, not independent validation.

A separate disposable Windows Git fixture reproduced issue #1344's distinction: clean working tree and filtered object equal to committed LF blob `4046bd727402fc1a4dfb9899724f8fd293644a6e`, while raw CRLF blob `0a3e3b3e37d3566317ed559ddd5b08d7b6db4877` differs. Full AOSS preflight was not executed, no candidate/freeze/custody hashes were changed, and issue #1344 remains open in its separate controlled review lane.

SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED. No live enforcement, scientific inference, release or main merge is established.
