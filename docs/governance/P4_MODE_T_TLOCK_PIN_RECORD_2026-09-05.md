# P4 Mode T tlock / drand Pin Record — 2026-09-05

**Status:** DESIGN PIN / RELEASE-ASSET CHECKSUM VERIFIED / NOT EXECUTED  
**Issue:** #287  
**Scope:** Source-backed identities and synthetic supply-chain verification only. No real secret or empirical execution.

## drand quicknet identity

Reviewed drand documentation identifies current mainnet `quicknet` as:

```yaml
beacon_id: quicknet
chain_hash: 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971
period_seconds: 3
genesis_time_unix: 1692803367
scheme_id: bls-unchained-g1-rfc9380
public_key: 83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a
```

Source: [drand quicknet launch record](https://docs.drand.love/blog/2023/10/16/quicknet-is-live/).

The chain hash, period, genesis time, scheme and public key are protocol identities. A future runtime must verify the remote `/info` response against the frozen tuple rather than accept an endpoint name alone.

## tlock release source identity

GitHub currently reports `drand/tlock` `v1.2.0` as the latest release.

The tag resolves as:

```yaml
tag: v1.2.0
annotated_tag_object_sha: 6a94bf6b8200ab67f2b80af8000a55db64998d94
source_commit_sha: 7b54141a9733fd6fa207587a11148280e6fb020d
tag_signature_verified_by_github: true
published_at: 2024-08-21T08:23:59Z
```

Authoritative GitHub API evidence:

- [Tag ref](https://api.github.com/repos/drand/tlock/git/ref/tags/v1.2.0)
- [Annotated tag object](https://api.github.com/repos/drand/tlock/git/tags/6a94bf6b8200ab67f2b80af8000a55db64998d94)
- [Latest release](https://api.github.com/repos/drand/tlock/releases/latest)

## Release artifact pin — VERIFIED FOR THE EXACT RELEASE ASSET

PR #291 added a read-only synthetic supply-chain workflow that downloaded the fixed `v1.2.0` release `checksums.txt` and `tlock_1.2.0_linux_amd64.tar.gz`, extracted the published checksum for that exact filename, recomputed SHA-256 locally, and required exact equality.

Accepted immutable evidence boundary:

```yaml
selected_binary: tlock_1.2.0_linux_amd64.tar.gz
selected_binary_sha256: 0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57
binary_pin_status: VERIFIED_FOR_EXACT_RELEASE_ASSET
verification_pr_head: 5ed111114ef7dd5af096ba26faa764c9cb6f6618
verification_run_id: 33998500757
verification_job_id: 101393082707
verification_artifact_id: 9978767726
verification_artifact_sha256: 06e84f537743c92069544885a81372244cd9f866b709d899f571f3b279e778e4
verification_merge_commit: b79435571af98c21c6da7d8212fb9e7dcd00b2e9
```

The evidence record reported identical published and recomputed digests and `match=true`. Its artifact name and artifact metadata were both bound to PR head `5ed111114ef7dd5af096ba26faa764c9cb6f6618`.

An earlier successful checksum run used GitHub's synthetic pull-request merge SHA in its artifact label and is retained only as superseded preliminary evidence. It is not the accepted provenance boundary.

This closes the narrow release-archive checksum blocker only. It does **not** establish that the selected binary is authorized for empirical execution, that the drand threshold-network assumption is satisfied, that hosted-runner memory is inaccessible, or that P4-T custody is sufficient.

## Strict chain requirement

The `tlock` source documents that a newly created Tlock trusts chain-hash metadata supplied by ciphertext by default and exposes `Strict()` to disable that switching behavior.

Source: [tlock chain-selection implementation](https://github.com/drand/tlock/blob/main/tlock.go).

Future decryption/continuity verification must use the frozen quicknet identity and strict chain binding. Ciphertext metadata is evidence to validate, not authority to select another chain.

## Security boundary

The drand timelock documentation explicitly states that a threshold number of malicious network nodes could compute future randomness and decrypt timelocked ciphertext early.

Source: [drand timelock encryption documentation](https://docs.drand.love/docs/timelock-encryption/).

This threshold-network trust assumption must remain visible in any final P4-T review. A successful checksum verification or synthetic `tle` test cannot prove the network assumption.

**Disposition:** source/chain pinning and the exact Linux amd64 release-archive checksum are verified for design purposes. No tlock binary has been executed by this record, and P4-T-A remains OPEN.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
