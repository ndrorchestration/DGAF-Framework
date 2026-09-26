
# DGAF Operator Self-Test

Status: **INTERNAL ENGINEERING VALIDATION ONLY**

This runbook lets the project operator exercise the current DGAF/AOSS Stage-A
apparatus before external review. It is designed to answer a narrow engineering
question:

> Does the current implementation recognize the expected frozen state, pass its
> covered regressions, fail closed under a deliberate invalid state, recover
> after restoration, and refuse unauthorized collection?

A passing operator self-test does **not** establish independent validation,
external validation, canonical DGAF efficacy, scientific replication,
production certification, or High-Assurance authorization.

## One-command Windows path

Create a fresh full clone, then run the wrapper from that checkout. This keeps
the operator's working tree untouched and avoids Windows line-ending state from
an older checkout:

```powershell
git clone --no-hardlinks https://github.com/ndrorchestration/DGAF-Framework.git DGAF-Framework-selftest
Set-Location .\DGAF-Framework-selftest
git fetch --unshallow
git checkout --detach origin/main
git status --short --branch
```

The final status must show a clean detached checkout. Then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_dgaf_operator_selftest.ps1 -RefreshDependencies
```

The wrapper:

1. requires Python 3.12;
2. creates an isolated virtual environment at
   `%USERPROFILE%\.venvs\dgaf-operator-selftest` when needed;
3. installs the repository's pinned test toolchain plus the project-pinned
   NetworkX version;
4. creates or reuses a dedicated ACP checkout at
   `%USERPROFILE%\DGAF-ACP-SelfTest`;
5. checks out the frozen ACP target
   `dbab7c1afafec524ce7c18157de2089cafe79c87`;
6. creates a disposable exact-byte DGAF clone for the byte-sensitive checks;
7. refuses to proceed when either source checkout is dirty;
8. launches the bounded Python operator runner.

On later runs, when dependencies are already installed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_dgaf_operator_selftest.ps1
```

## Direct Python path

The underlying cross-platform runner is:

```text
scripts/run_dgaf_operator_selftest.py
```

Example:

```bash
python scripts/run_dgaf_operator_selftest.py \
  --dgaf-root . \
  --acp-root /path/to/frozen/agent-control-plane
```

The ACP checkout must be a full, clean repository at:

```text
dbab7c1afafec524ce7c18157de2089cafe79c87
```

## What the suite checks

The runner records and evaluates:

- Python 3.12 execution;
- DGAF and ACP repository existence;
- full-clone state rather than shallow history;
- absence of Git replace-object refs;
- clean DGAF and ACP worktrees;
- exact frozen ACP commit identity;
- current DGAF HEAD identity;
- AOSS static preflight acceptance of the expected frozen source state;
- preservation of `outcomes_generated=false`;
- preservation of `scientific_n_increment=0`;
- preservation of `external_validation_established=false`;
- preservation of `canonical_dgaf_efficacy=NOT_ESTABLISHED`;
- DGAF quick regression behavior;
- all discovered `tests/test_aoss*.py` modules supported by the host;
- on Windows, exercises the custody implementation and verifies the expected
  `O_NOFOLLOW_REQUIRED` refusal without filesystem side effects;
- explicit refusal of `collect` with
  `COLLECTION_IMPLEMENTATION_NOT_ACCEPTED`;
- deliberate dirty-worktree injection and expected
  `DGAF_WORKTREE_DIRTY` refusal;
- successful preflight again after the deliberate probe is removed;
- final clean DGAF worktree.

The dirty-worktree probe is removed in a `finally` path so an expected
negative test does not intentionally leave the repository modified.

## Evidence packet

Each run writes outside the repository by default:

```text
%USERPROFILE%\DGAF-Operator-SelfTest-Results\<UTC-run-id>\
```

The retained packet contains:

- `operator_selftest_report.json` — machine-readable result;
- `operator_selftest_report.json.sha256` — SHA-256 sidecar;
- `operator_selftest_summary.md` — human-readable summary;
- `logs/*.json` — command, return code, stdout, stderr, and timestamps for
  consequential checks.

The report declares:

```text
evidence_class=INTERNAL_OPERATOR_ENGINEERING_VALIDATION
independent_validation_established=false
external_validation_established=false
canonical_dgaf_efficacy=NOT_ESTABLISHED
high_assurance=NOT_AUTHORIZED
scientific_n_increment=0
```

These boundaries are part of the test contract rather than optional prose.

## How to interpret outcomes

### PASS

A PASS means the covered implementation behaved as expected in the observed
operator environment, including the required negative/fail-closed probes.

It may be logged as internal engineering validation for the exact DGAF HEAD,
ACP commit, Python/runtime environment, and retained evidence packet.

It must not be promoted to independent validation.

### FAIL

A FAIL means at least one expected behavior did not occur. Preserve the evidence
packet. Do not edit the report into a PASS. Diagnose the failed control, make
the correction through normal repository review, then run a fresh test.

### BLOCKED

A prerequisite problem such as the wrong ACP commit, a dirty source checkout,
missing Python 3.12, or missing dependencies should be treated as a blocked
operator run rather than evidence that the underlying DGAF behavior passed or
failed. The wrapper reports prerequisite errors before the retained runner
packet exists; preserve the terminal output and correct the prerequisite before
starting a fresh run.

## Relationship to external review

This suite is deliberately useful preparation for Issue #929 but cannot close
it. The external reviewer must still independently retrieve and verify the
accepted source identities, disclose relevant relationships/conflicts, retain
their own consequential evidence, and report ACCEPT/REJECT/BLOCKED findings
without a pre-filled conclusion.

The operator evidence packet can be used to debug DGAF before that handoff. It
must not be given to the reviewer as a required result or substituted for the
reviewer's independently retained evidence.
