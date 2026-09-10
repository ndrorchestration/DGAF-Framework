# TLA+ Runtime Pin Reliability — 2026-09-10

## Disposition

Governance CI keeps TLA+ Tools v1.7.4 as the accepted stable formal-model tool and preserves exact executable-byte verification. The runtime verification path no longer depends on GitHub's release-metadata API being available or below an unauthenticated rate limit.

## Trigger

During final exact-head validation of Track A Epoch 002 runner PR #591, one Governance CI attempt reached the TLA+ release-metadata lookup and received HTTP 403 from the public GitHub API. A same-head rerun subsequently passed the same metadata check, byte checks, and TLC model check. The event therefore exposed CI availability coupling rather than a repository-code, TLA+ byte-identity, or model-check defect.

## Accepted identity contract

Each Governance CI run must independently establish the downloaded executable identity using all of:

- release tag and canonical download path: `v1.7.4` / `https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar`;
- exact size: `2274532` bytes;
- SHA-1: `bee4a54f3ee3d4afc347c3240ec2d9e93b075104`;
- SHA-256: `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`;
- successful execution of the existing DGAF containment TLC model check.

The SHA-1 was recorded as upstream-published when stable v1.7.4 was adopted in PR #557. SHA-256 is the stronger local executable-byte identity. Runtime correctness does not require re-querying mutable service metadata before checking immutable downloaded bytes.

## Fail-closed behavior

The workflow fails if the canonical download fails after bounded retries, byte size differs, either digest differs, TLC fails, or the formal-model evidence cannot be produced. No fallback tool version, alternate asset, checksum bypass, or model-check skip is allowed.

A regression test rejects reintroduction of the TLA+ release-API dependency and requires the exact URL, size, digests, and TLC invocation to remain present.

## Scientific boundary

This is CI reliability and supply-chain integrity maintenance only. It does not establish custody, freeze, authorization, empirical execution, efficacy, or scientific N.

**PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0.**
