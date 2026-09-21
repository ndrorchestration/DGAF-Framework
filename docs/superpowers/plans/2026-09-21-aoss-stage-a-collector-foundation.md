# AOSS Stage-A Collector Foundation Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task after owner review. Do not delegate unless the owner selects delegation.

**Goal:** Deliver a non-collecting preflight and custody foundation that makes the accepted collector design implementable without inventing unresolved policy semantics.

**Architecture:** Read-only preflight verifies immutable repository evidence. A separate custody module handles exclusively created, explicitly synthetic attempts during development. The command-line entrypoint exposes preflight only and rejects collection until a later accepted mapping and executable binding exist.

**Tech Stack:** Python 3.10-compatible standard library for the new foundation; pytest for tests. Existing authorization validator retains its jsonschema dependency. No claim of a locked collection runtime is made by this tranche.

**Spec:** docs/superpowers/specs/2026-09-21-aoss-stage-a-collector-design.md at design commit 1360a3f005e955aa39ac2f9fd8067f054cd4df29.

## Global Constraints

- ACP commit: dbab7c1afafec524ce7c18157de2089cafe79c87.
- Accepted receipt: 6baea5a6b6a316add6292cc647f5b455eb235ce3.
- Accepted authorization: 854b9d5adb33c6ee6158a63017f133f20b90742e.
- Protected design basis: 807216df1bd5b28c677b8c42822975b2941c1211.
- Adapter apparatus: 69821cdcc1b9b9432b7001c6f52c867f9669f54d.
- No ACP execution/import from preflight; no observer callback or source mutation.
- Do not edit existing authorization, receipt, policy, adapter, baseline or frozen contracts.
- No accepted-study attempt, source episode, outcome, analysis or whole-study replay receipt is created by development tests.
- Scientific-N increment remains 0; all efficacy and assurance exclusions remain.
- Stage-A policy-input reconstruction remains unresolved and blocks collection.
- The fixture bundle remains APPARATUS_FIXTURES_NOT_COLLECTED_OUTCOMES.

## Scope and handoff

This is the first independently testable tranche of the approved collector design.
It does not purport to implement the complete collector. Driver, semantic mapping,
runtime lock, accepted executable binding, actual replay and analysis require a
subsequent plan once the mapping is recovered or prospectively accepted.
Do not write guessed policy predicates to make an end-to-end demonstration pass.

## Review Focus

1. Git replacement objects, shallow history or moving refs must not manufacture accepted lineage (Task 1).
2. Dirty/untracked source or contract bytes must not pass a committed-blob-only check (Task 1).
3. Symlink ancestors, path traversal and concurrent creation must not overwrite evidence (Task 2).
4. Incomplete writes or crash leftovers must never be labeled complete or silently reused (Task 2).
5. A successful static preflight must not be exposed as collection readiness or execute ACP (Task 3).

## Task 1: Read-only evidence preflight

**Files:** Create `scripts/aoss_stage_a/__init__.py`,
`scripts/aoss_stage_a/preflight.py`, `tests/test_aoss_stage_a_preflight.py`.
**Consumes:** Explicit DGAF and ACP filesystem paths plus the fixed accepted identities above.
**Produces:** inspect_preflight(dgaf: Path, acp: Path) -> dict[str, object];
PreflightError with a stable reason code. No writable destination argument.

- [ ] Write failing tests using real temporary Git repositories and explicit test
  identities supplied to a private pure verification helper, while the public
  entrypoint always uses the accepted constants. Helpers live in the test module.
  Cover ancestry, commit parents, first-and-only event paths, exact authorization
  JSON, exact receipt JSON, all nine contract blobs, adapter bytes and policy/
  comparator executable bindings. The test repo must use actual Git objects,
  not a mocked command runner.
- [ ] Start with these public-boundary tests:

```python
def test_missing_acp_checkout_fails_closed(tmp_path):
    from scripts.aoss_stage_a.preflight import inspect_preflight, PreflightError
    with pytest.raises(PreflightError, match="ACP_REPOSITORY_MISSING"):
        inspect_preflight(DGAF_ROOT, tmp_path / "absent")

def test_preflight_has_no_outcome_destination():
    from scripts.aoss_stage_a.preflight import inspect_preflight
    assert list(inspect.signature(inspect_preflight).parameters) == ["dgaf", "acp"]
```

- [ ] Run python -m pytest -q tests/test_aoss_stage_a_preflight.py and confirm the
  new module is absent. Then add a minimal module and run tests again until
  failures identify missing behavior rather than import errors.
- [ ] Implement subprocess Git calls as argument arrays with check=True and
  GIT_NO_REPLACE_OBJECTS=1. Reject shallow repositories and any refs/replace
  entries. Resolve commits by full SHA; check worktree status including
  untracked files, and verify tracked file bytes against the expected blobs.
  Require accepted receipt ancestry in the inspected DGAF revision rather than
  requiring HEAD equal the receipt commit, so additive tooling can be reviewed.
  Reject altered event history even when current JSON happens to match.
- [ ] Reuse the expected authorization/receipt contract via a verifier loaded
  from its trusted accepted revision, not a caller-supplied module. Alternatively
  compare immutable JSON and binding bytes directly; do not import ACP.
  Verify nine contract identities plus separate adapter, policy, comparator,
  replay schema and custody-contract identities from their accepted sources.
- [ ] Return a JSON-serializable report with inspected commits, per-check
  booleans, failures and explicit non-authority fields:

```python
{
    "record_type": "AOSS_STAGE_A_STATIC_PREFLIGHT",
    "static_identity_checks": "PASS",
    "collection_readiness": "NOT_ESTABLISHED",
    "mapping_binding": "NOT_ESTABLISHED",
    "runtime_binding": "NOT_ESTABLISHED",
    "scientific_n_increment": 0,
    "outcomes_generated": False,
}
```

  Never return PASS if any required static identity check failed. A missing
  runtime/mapping binding prevents readiness even when static checks pass.

- [ ] Add real-Git negative cases: wrong ACP commit, dirty tracked file,
  untracked import-shadow file, changed contract, authorization path modified
  and restored, receipt wrong parent, replaced object and shallow clone.
  Ensure snapshots of both trees are byte-identical before and after inspection.
- [ ] Run tests to green; commit only the three Task 1 files.

## Task 2: Exclusive synthetic custody primitives

**Files:** Create scripts/aoss_stage_a/custody.py and
tests/test_aoss_stage_a_custody.py.
**Consumes:** Synthetic test payloads and a trusted local parent directory.
**Produces:** canonical_bytes(value: object) -> bytes;
digest_bytes(data: bytes) -> str;
reserve_synthetic_attempt(parent: Path, attempt_id: str) -> Path;
write_object(attempt: Path, payload: object) -> str.
These primitives are not wired to a production collection command.

- [ ] Write failing tests before code:

```python
def test_canonical_bytes_are_exact():
    assert canonical_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}\n'

def test_nonfinite_payload_rejected():
    with pytest.raises(ValueError):
        canonical_bytes({"value": float("nan")})

def test_attempt_cannot_be_reused(tmp_path):
    path = reserve_synthetic_attempt(tmp_path, "case-1")
    assert (path / "SYNTHETIC_TEST_ONLY").is_file()
    with pytest.raises(FileExistsError):
        reserve_synthetic_attempt(tmp_path, "case-1")
```

- [ ] Implement canonical serialization with UTF-8, sorted keys, compact
  separators, allow_nan=False and exactly one trailing newline. Use explicit
  ensure_ascii=False for this new bundle convention; do not alter the adapter.
  digest_bytes returns lowercase 64-character SHA-256 without a prefix.
- [ ] Validate attempt IDs against `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`.
  Reject traversal, separators, symlink parent components and existing attempt
  paths. On supported POSIX environments use directory file descriptors and
  O_NOFOLLOW/O_EXCL to prevent check-then-open symlink substitution. Fail
  explicitly on platforms without those protections; do not claim Windows
  support from path-string checks.
- [ ] Create reservation directory exclusively; write a synthetic marker and
  immutable STARTED event before any payload. Failed reservation leaves a
  blocked incomplete directory. No cleanup-and-retry convenience method.
- [ ] Write each object exclusively under objects/<sha256>.json. For an existing
  object, require exact bytes before treating it as deduplicated. fsync data and
  relevant directory entries. A partial write stays invalid; no COMPLETE state
  is provided by this foundation.
- [ ] Add tests for symlink parent/destination/object, concurrent reservation,
  existing corrupt same-name object, simulated write failure, missing synthetic
  marker and disallowed identifiers. Verify originals remain unchanged.
- [ ] Run python -m pytest -q tests/test_aoss_stage_a_custody.py to green and commit.

## Task 3: Non-collecting command and evidence output

**Files:** Create scripts/run_aoss_v0_6_stage_a.py and
tests/test_aoss_stage_a_cli.py.
**Consumes:** Task 1 inspect_preflight; no Task 2 attempt allocation in preflight.
**Produces:** A preflight subcommand writing only a report to stdout.
A collect subcommand always fails with COLLECTION_IMPLEMENTATION_NOT_ACCEPTED.

- [ ] Write subprocess tests before code:

```python
def test_collect_is_disabled(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(CLI), "collect"],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert completed.returncode != 0
    assert "COLLECTION_IMPLEMENTATION_NOT_ACCEPTED" in completed.stderr
    assert list(tmp_path.iterdir()) == []
```

- [ ] Add a preflight test using temporary real repositories from Task 1.
  Place a sentinel ACP package on the import path that raises if imported;
  preflight must still perform only Git/file inspection. Snapshot the working
  directory and both repositories and prove no file writes.
- [ ] Implement argparse with required subcommands. preflight requires
  --dgaf-root and --acp-root. Emit report JSON to stdout; return nonzero for
  static identity failure. On static success retain collection_readiness=
  NOT_ESTABLISHED, with no run token or executable permission.
- [ ] Reject collect before resolving or importing any source-driver code;
  there is no accepted driver in this tranche.
- [ ] Run all three new test files and existing AOSS authorization/adapter/
  policy/baseline tests. Commit the command and tests.

## Task 4: Reviewable integration and handoff

**Files:** Create docs/research/AOSS_V0_6_STAGE_A_COLLECTOR_FOUNDATION.md.
Add .github/workflows/aoss-stage-a-collector-foundation.yml only after inspecting
the repository workflow conventions. Do not modify frozen registries.

- [ ] Document the exact non-collecting interface:

```bash
python scripts/run_aoss_v0_6_stage_a.py preflight --dgaf-root . --acp-root ../agent-control-plane
python scripts/run_aoss_v0_6_stage_a.py collect
```

  Explain that the first reports static evidence only and the second is expected
  to fail. List mapping, driver, runtime lock and executable acceptance as open.

- [ ] Add CI that checks out the exact PR head with full history and runs the
  new synthetic unit tests and existing AOSS regression tests using repository
  test dependency conventions. Do not execute ACP or create a study artifact.
  CI evidence is development evidence only, not collection acceptance.
- [ ] Run:

```bash
python -m pytest -q tests/test_aoss_stage_a_preflight.py tests/test_aoss_stage_a_custody.py tests/test_aoss_stage_a_cli.py tests/test_aoss_v0_6_stage_a_collection_authorization.py tests/test_aoss_v0_6_acp_adapter.py tests/test_aoss_v0_6_stage_a_decision_policy.py tests/test_aoss_v0_6_stage_a_acp_direct_baseline.py
git diff --check
```

  Apply the repository's changed-Python static checks and CI gates. Report any
  unavailable dependency or unrelated failure explicitly. Never rerun a real
  study to make tests pass.

- [ ] Review the diff for changed frozen files, hidden ACP imports, mock-only
  assertions, authority upgrades and production-like test labels. Open an
  implementation PR with exact head, tests and remaining blockers.
- [ ] Stop before collection. The next plan requires an accepted predicate
  mapping and concrete source-driver recipes; that review must address
  terminal-plus-blocked, terminal-plus-stale, duplicate terminals, source-order
  ambiguity and absent authority without conditioning rules on outcomes.

## Coverage review

This tranche covers design preflight, synthetic custody and the execution stop.
It intentionally does not implement source generation, policy reconstruction,
runtime locking, replay or analysis. Those requirements remain visible here
rather than being marked complete by a static PASS. No empirical state changes.
