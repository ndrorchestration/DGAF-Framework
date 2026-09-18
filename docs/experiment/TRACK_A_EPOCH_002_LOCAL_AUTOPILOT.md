# Track A Epoch 002 — Local Materialization Autopilot

Status: **PROSPECTIVE TOOLING ONLY**

Scientific/control effect: **NONE**

`PRE-FREEZE / FAIL-CLOSED / PRIMARY ANALYSIS NOT AUTHORIZED / N=0`

## Purpose

This is the lowest-friction operator path when ChatGPT cannot directly invoke
the local DGAF MCP bridge.

One local command performs the controlled secret-bearing materialization on the
operator machine and then creates a **draft, one-file GitHub evidence-admission
PR** containing only the canonical non-secret materialization evidence.

The autopilot deliberately stops there.

It does not create the repository `MATERIALIZATION_RECEIPT`, does not authorize
primary analysis, and does not run primary analysis.

## Required local configuration

The accepted bridge still requires these local environment variables:

```text
DGAF_PUBLIC_ARCHIVE
DGAF_PROTECTED_ARCHIVE
DGAF_CUSTODY_PRIVATE_KEY
DGAF_MATERIALIZATION_OUTPUT_DIR
DGAF_RETENTION_ID
```

Values are local paths/identifiers only. Never put the private-key bytes,
passphrase, decrypted mapping, or protected plaintext into GitHub, ChatGPT,
Notion, CI variables, or the PR.

The materialization output directory must be outside the repository and must
not already contain the five canonical bundle members.

## One-command Windows path

From a local DGAF checkout:

```powershell
.\scripts\run_track_a_epoch_002_local_autopilot.ps1
```

The wrapper creates an isolated Python virtual environment if needed, installs
the repository CI dependencies needed by the accepted validators/materializer,
and invokes the Python autopilot.

Before any decryption/materialization, the Python autopilot requires:

- `git`;
- GitHub CLI `gh` with a valid `github.com` login;
- `openssl`;
- all five local DGAF environment variables;
- the expected `ndrorchestration/DGAF-Framework` origin;
- a PASS from the canonical `--tooling-only` materialization validator.

If any preflight fails, no materialization occurs.

## Encrypted custody key

The accepted materializer invokes OpenSSL directly. If the custody private key
is encrypted, OpenSSL may ask for its passphrase **locally in the terminal**.

That prompt is intentional. The passphrase is not routed through ChatGPT,
GitHub, the MCP adapter, the evidence file, or the PR.

After local entry, the rest of the sequence remains automatic.

## Automated sequence

```text
preflight local commands / repo / GitHub auth
  -> canonical tooling-only validator
  -> verify_inputs
  -> local materialize
  -> get_evidence
  -> fetch latest origin/main
  -> isolated temporary Git worktree
  -> copy exactly one canonical evidence file
  -> commit exactly one path
  -> canonical --validate-evidence-admission
  -> recheck that origin/main did not move
  -> push evidence branch
  -> create DRAFT evidence-admission PR
  -> STOP
```

If `origin/main` moves while the admission commit is being prepared, the
autopilot discards only the temporary admission worktree/branch and retries
against the newer `origin/main`. The locally retained materialization bundle is
not discarded or regenerated.

The retry count is bounded and fail-closed.

## Secret boundary

The only file copied into the Git worktree is:

```text
docs/experiment/track_a_runs/TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json
```

The autopilot checks both Git status and the staged diff before commit. The
canonical evidence-admission validator must PASS before the branch is pushed.

The local unblinded analysis input, sidecar, manifest, operator execution
receipt, protected archive, private key, and decrypted protected data remain
outside the repository.

## What happens after the PR appears

The draft evidence-admission PR is intentionally reviewable rather than
self-merging. A GitHub-capable orchestration layer can then:

1. verify the exact PR head;
2. wait for all required CI/check families;
3. transition and merge the one-file evidence event if valid;
4. prepare the separate one-file `MATERIALIZATION_RECEIPT` event;
5. stop again before the separate primary-analysis authorization event.

That preserves the governed event boundaries while removing the manual
"download helper / run command / upload evidence JSON" handoff.

## Non-effects

Running or accepting this autopilot tooling does not itself establish
materialization. Only a successful local run followed by accepted repository
evidence and the later immutable repository receipt can establish that state.

At the autopilot stop boundary:

```text
MATERIALIZATION_EVIDENCE = PR CREATED / NOT YET ACCEPTED
MATERIALIZATION_RECEIPT = NOT ESTABLISHED
PRIMARY_ANALYSIS = NOT AUTHORIZED / NOT RUN
SCIENTIFIC_N_INCREMENT = 0
CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED
```
