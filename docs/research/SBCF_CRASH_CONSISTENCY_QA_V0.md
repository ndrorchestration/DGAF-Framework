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

SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED. No live enforcement, scientific inference, release or main merge is established.
