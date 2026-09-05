# P4 Mode T External Assumptions Evidence — 2026-09-05

**Status:** SOURCE-BACKED DESIGN EVIDENCE / NOT A P4 CLOSURE RECORD  
**Issue:** #287  
**Design lineage:** reconstructed from PR #288 after the #291 tlock checksum verification merge.  
**Scientific state:** P4-A OPEN · P7 OPEN · P8 OPEN / FAIL-CLOSED · P9 NOT EXECUTED · FREEZE NOT ESTABLISHED · AUTHORIZATION NOT GRANTED · empirical N=0.

## Purpose

Record authoritative external facts that constrain the proposed solo Mode T design. These facts support design decisions only. They do not establish that GitHub Actions plus drand/tlock is sufficient custody.

## GitHub-hosted runner facts

### Fresh hosted environment per job

GitHub documents that, except for single-CPU runners, each GitHub-hosted runner is a new virtual machine. GitHub also documents that when a hosted job begins it provisions a new VM and automatically decommissions it when the job finishes.

Sources: [GitHub-hosted runners concepts](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners) and [using GitHub-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners).

**Design consequence:** standard GitHub-hosted runners are preferable to self-hosted runners for Mode T because the accepted design requires an ephemeral execution environment. `ubuntu-slim` is not equivalent to the full-VM runner class and must not be substituted without a separate review.

### The job itself has administrative privilege

GitHub documents that Linux and macOS hosted VMs support passwordless `sudo`; Windows hosted VMs run as administrators with UAC disabled.

Source: [GitHub-hosted runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).

**Design consequence:** Mode T must not rely on OS-user separation between workflow steps. All steps in the same job are effectively inside one administrative trust domain. The real key/mapping/nonces therefore must remain inside one frozen trusted helper process and must never be placed in a location, environment variable, command-line argument, or file intentionally shared with later steps.

### Re-runs are a real control path

GitHub documents that people with write permission can re-run workflows. Re-runs use the same `GITHUB_SHA` and `GITHUB_REF` as the original event. GitHub also exposes `GITHUB_RUN_ATTEMPT`, which starts at 1 and increments for each re-run, while `GITHUB_RUN_ID` does not change across attempts of the same workflow run.

Sources: [Re-running workflows and jobs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) and [GitHub Actions variables](https://docs.github.com/en/actions/reference/workflows-and-actions/variables).

**Design consequence:** a Mode T empirical execution must reject `GITHUB_RUN_ATTEMPT != 1`. A successful or partially usable first attempt must never be rerun under the same authorization.

### Debug logging can be enabled on a re-run

GitHub documents runner-diagnostic and step-debug logging and states that anyone able to run the workflow can enable the additional debugging when re-running a workflow.

Source: [Enabling debug logging](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging).

**Design consequence:** rejecting all re-run attempts is required but not sufficient. The accepted first attempt must also guard against debug mode before secret generation, and the helper must never emit plaintext protected material even under ordinary diagnostic verbosity.

### Caches are cross-run storage and must not contain secrets

GitHub documents that dependency caches persist independently of the clean hosted runner and explicitly says not to store sensitive information in a cache. Cache contents are restored as untrusted input.

Sources: [Dependency-caching concepts](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching) and [dependency-caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching).

**Design consequence:** the Mode T execution job must not save or restore caches after the secret-generation boundary. Secret-bearing or potentially secret-derived temporary paths must never be included in a cache key or cache path.

### Logs and workflow runs are not immutable evidence

GitHub documents that users with write access can delete workflow runs and can delete workflow logs.

Sources: [Deleting a workflow run](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/delete-a-workflow-run), [workflow-runs REST API](https://docs.github.com/en/rest/actions/workflow-runs), and [workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs).

**Design consequence:** GitHub Actions timestamps/run history alone cannot be the sole anti-cherry-picking or analysis-lock evidence. Reservation, authorization, authorization-consumption, execution-start, ciphertext/commitment, and analysis-lock records need prompt retention in the independently preserved P6 evidence channel or another append-only/non-unilateral evidence path before they are relied on scientifically.

### Secret masking is defense-in-depth, not the custody boundary

GitHub provides `::add-mask::` to redact a value from logs, and warns that masking must occur before a value is output.

Source: [GitHub workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands).

**Design consequence:** the helper may register generated printable identifiers/nonces for masking as defense-in-depth, but Mode T must be safe even if masking is incomplete. Raw key/mapping/nonces must never be intentionally emitted to stdout/stderr, step outputs, summaries, artifacts, environment variables, or command-line arguments.

## drand/tlock facts

### Timelock security model

drand documents timelock encryption as encryption to a future beacon round. The future randomness required for decryption is not released until that round. drand also explicitly states a security limitation: if a threshold number of network nodes are malicious, they can generate future random values and decrypt future ciphertexts early.

Source: [drand timelock encryption documentation](https://docs.drand.love/docs/timelock-encryption/).

**Design consequence:** Mode T cannot claim unconditional time security. The accepted threat model must explicitly adopt the drand threshold-network assumption for the selected chain.

### Current mainnet timelock chain identity

The drand `tlock` project documents the current mainnet timelock-capable quicknet chain hash as:

`52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`

It documents a 3-second frequency and recommends using the chain hash rather than only a beacon name when public-key integrity matters.

Source: [drand/tlock](https://github.com/drand/tlock).

**Design consequence:** the chain hash must be frozen explicitly. Mode T must not rely on an unqualified network alias.

### Current released tlock version and exact Linux amd64 checksum

GitHub reports `drand/tlock` release `v1.2.0` as the latest published release, dated 2024-08-21.

Source: [drand/tlock v1.2.0](https://github.com/drand/tlock/releases/tag/v1.2.0).

PR #291 independently retrieved the fixed release checksum manifest and `tlock_1.2.0_linux_amd64.tar.gz` on a GitHub-hosted runner, recomputed SHA-256 locally, and required exact equality. The accepted provenance-bound run is `33998500757` at PR head `5ed111114ef7dd5af096ba26faa764c9cb6f6618`, merged as `b79435571af98c21c6da7d8212fb9e7dcd00b2e9`.

The exact published and recomputed digest is:

`0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57`

Accepted evidence artifact `9978767726` is named by that PR head, independently reports the same head SHA in artifact metadata, and has ZIP digest `sha256:06e84f537743c92069544885a81372244cd9f866b709d899f571f3b279e778e4`.

**Design consequence:** the previously open release-archive checksum blocker is now verified for this exact release asset. Future implementation still must pin and reverify this exact digest before use; no floating `latest`, branch, runtime package-manager resolution, or unverified download is acceptable. This checksum result does not authorize execution or establish custody sufficiency.

### Ciphertext chain-hash trust must be disabled

`tlock` exposes a `Strict()` mode. Its source states that a newly constructed `Tlock` trusts the chain hash found in ciphertext metadata by default and may switch to it during decryption; `Strict()` disables that behavior.

Source: [tlock chain-selection implementation](https://github.com/drand/tlock/blob/main/tlock.go).

**Design consequence:** the Mode T continuity/decryption path must use strict chain binding. A ciphertext-supplied chain identity must never override the frozen quicknet chain hash.

## Design correction: reserve then authorize an exact run

The external facts above expose a stronger execution-order requirement than the initial #287 sketch.

A unique empirical execution should use a **run-reservation → exact-run authorization → authorization-consumption → execution** sequence:

1. dispatch the frozen workflow into a pre-secret reservation/wait state;
2. obtain immutable GitHub metadata including `GITHUB_RUN_ID`, `GITHUB_RUN_ATTEMPT=1`, frozen `GITHUB_SHA`, and workflow identity;
3. create a separate authorization record that binds the exact reserved `GITHUB_RUN_ID`, candidate/freeze identities, and allowed first attempt;
4. independently retain that reservation/authorization evidence before secret generation;
5. let the same reserved run retrieve and validate that exact authorization;
6. publish and independently retain a single-use authorization-consumption record while `secret_instantiation_status` is still `NOT_EXECUTED`;
7. reject every different run ID, every `GITHUB_RUN_ATTEMPT != 1`, and every attempt to consume an already-consumed authorization;
8. only then permit P4-T-X protected-material generation.

This reduces rerun/multi-run ambiguity because authorization is bound to an already existing run identity rather than to a reusable workflow definition alone. The consumption record also closes the crash window between secret generation and later execution evidence: a crash after consumption invalidates the authorization rather than allowing a silent retry.

It does **not** eliminate all trust concerns: a repository owner can delete GitHub workflow history, so reservation/authorization/consumption evidence still requires independent retention or transparency evidence.

## Remaining UNKNOWN / BLOCKING questions

The reviewed authoritative GitHub documentation establishes fresh VM lifecycle, administrative privilege, rerun/debug controls, cache behavior and deletability of run/log evidence. It does **not**, in the sources reviewed here, explicitly document a supported repository-owner mechanism for attaching an interactive shell to the live standard GitHub-hosted VM or snapshotting its memory.

Therefore the claim “a repository owner cannot inspect live runner memory” remains **UNKNOWN**, not PASS. Promotion must either:

- obtain authoritative evidence sufficient to bound that capability; or
- choose an architecture whose scientific validity does not depend on assuming an undocumented inability to inspect live memory.

Also still unresolved:

- exact minimum release-margin / final analysis-lock-window policy;
- independent source for server-time-to-drand-round verification;
- acceptable behavior if the drand round is delayed or network retrieval fails;
- exact P6/transparency mechanism used for reservation/authorization/consumption/analysis-lock anti-deletion evidence;
- final runtime verification policy for the already checksum-pinned tlock asset and its strict chain binding.

The exact tlock v1.2.0 Linux amd64 release-archive checksum is **not** among the remaining blockers; that narrow supply-chain identity was verified by #291. No broader P4 state is promoted by association.

## Current conclusion

The external evidence makes the Mode T proposal more concrete but **does not yet establish sufficient custody**.

The strongest current design is:

`P4-T-A mechanism closure → frozen run reservation → exact run authorization → transparent single-use authorization consumption → P4-T-X secret instantiation in attempt 1 only → independently retained ciphertext/commitment evidence → P4-T-L analysis lock before release → P4-B continuity audit`

Until the remaining UNKNOWN items are resolved and synthetic adversarial tests pass, P4-T-A remains OPEN.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
