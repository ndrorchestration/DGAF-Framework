# Track A Epoch 002 Locked Primary Analysis Execution Procedure

Status: **PROSPECTIVE TOOLING / EXECUTION REQUIRES ACCEPTED PRIMARY-ANALYSIS AUTHORIZATION**

This procedure governs the local execution of the already-frozen Track A Epoch 002 primary analysis. It does not modify the preregistration, analysis implementation, materialized input, or authorization record.

## Preconditions

Execution is admissible only when all of the following are true:

1. The canonical `PRIMARY_ANALYSIS_AUTHORIZATION_RECORD` exists on protected `main` as a creation-only immutable event.
2. The authorization record validates against the accepted `MATERIALIZATION_RECEIPT`.
3. The frozen analysis blob remains `d4495f7cdf211b974039ec0e66292dc62ea0881f`.
4. The frozen analysis configuration SHA-256 remains `a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73`.
5. The requirements lock blob remains `00c1f779e97030f9b25ae494642edb31b5b09de5`.
6. The local runtime exactly matches the analysis lock: Python `3.12.0` and NumPy `2.5.1`.
7. The external materialized input SHA-256 exactly matches the admitted materialization evidence.
8. No canonical locked-analysis result record already exists.

Any failed precondition stops execution.

### Windows lock-instantiation rule

The accepted requirements lock is frozen by Git blob identity `00c1f779e97030f9b25ae494642edb31b5b09de5` and must not be regenerated or edited after authorization. On Windows, pip may otherwise discover platform-only transitive packages that were not part of the accepted resolved lock. Therefore the operator autopilot installs the frozen package set with `--require-hashes --no-deps`.

This does not change the analysis dependency identity: it prevents a new platform-specific resolution step and installs only packages already named and hashed in the authorized lock.

The execution runner also imports the repository authorization validator, which depends on `jsonschema`. That dependency is governance tooling, not part of the frozen numerical analysis package set. The Windows operator path therefore provisions `jsonschema==4.26.0` and its non-numerical dependencies into a separate `governance-support` directory and exposes that directory only through a temporary `PYTHONPATH` while the runner validates authorization and executes. The autopilot fails closed if that support overlay contains a NumPy package, preventing it from replacing or shadowing the frozen NumPy `2.5.1` environment.

The repository CI includes a Windows runner that verifies the exact frozen-lock installation mode, Python `3.12.0`, NumPy `2.5.1`, the unchanged requirements blob, a NumPy-free governance support overlay, and the non-executing authorization preflight.

## One-command Windows operator path

For the accepted Windows operator environment, use:

`scripts/run_track_a_epoch_002_primary_analysis_autopilot.ps1`

The autopilot is the preferred nontechnical path. It:

1. reads the retained materialized input from the operator-controlled user-profile location by default;
2. verifies GitHub CLI authentication and the expected DGAF repository origin;
3. fetches protected `main` and creates an isolated detached worktree;
4. finds exact Python `3.12.0`, or if absent provisions the official `python` 3.12.0 NuGet package side-by-side in the DGAF user-local runtime directory, verifying the NuGet client and provisioned Python executable signatures; this avoids Windows Installer product-version conflicts and does not modify or uninstall any existing Python installation;
5. creates/reuses an isolated analysis virtual environment from the already-resolved hash-locked requirements using `--require-hashes --no-deps`, preserving the authorized lock blob byte-for-byte and preventing Windows-only resolver expansion from changing the frozen dependency set;
6. runs the non-executing authorization/runtime preflight;
7. executes the frozen primary analysis only if no retained output bundle already exists;
8. resumes from an existing complete retained output without re-executing analysis;
9. validates and prepares the non-numerical, content-addressed result record;
10. creates a one-file result-admission commit in an isolated worktree, validates the exact event, confirms protected `main` has not moved, pushes the branch, and opens a draft result-admission PR;
11. never prints the estimate, confidence interval, or preregistered classification.

If protected `main` moves during result admission, the autopilot retries admission without re-running the empirical analysis. If the local output is partial or ambiguous, it fails closed instead of overwriting or re-executing.

Default local paths are derived from `$env:USERPROFILE`; no username-specific path is stored in the repository.

## Local preflight

After the authorization event has been accepted on protected `main`, use the exact locked analysis environment and run:

```text
python scripts/run_track_a_epoch_002_locked_primary_analysis.py --preflight-only
```

Preflight does not read the materialized input and does not execute the analysis.

## Local execution

The retained materialized input remains outside the repository. Execute:

```text
python scripts/run_track_a_epoch_002_locked_primary_analysis.py \
  --input <external-track_a_epoch_002_unblinded_analysis_input.json> \
  --output-dir <external-empty-result-directory>
```

The runner refuses repository-local input/output paths and refuses to overwrite an existing result.

The local output bundle contains:

- the exact authorization-event identity;
- the admitted materialized-input digest;
- frozen analysis/config identities;
- exact runtime versions;
- the locked primary estimate, confidence interval, and preregistered classification;
- explicit non-promotion fields preserving canonical DGAF efficacy, independence, and High-Assurance boundaries.

The runner prints only the output path and SHA-256, not the statistical result.

## Post-execution boundary

Execution does **not** by itself establish canonical DGAF efficacy, independent validation, or High-Assurance authorization. The local output must next be admitted through a separate, content-addressed `LOCKED_ANALYSIS_RESULT_RECORD` event before interpretation.

No exploratory comparison may be relabeled confirmatory after outcome inspection.
