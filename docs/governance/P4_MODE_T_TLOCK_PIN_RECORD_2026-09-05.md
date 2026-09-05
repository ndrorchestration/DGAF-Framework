# P4 Mode T tlock / drand Pin Record — 2026-09-05

**Status:** DESIGN PIN / ARTIFACT CHECKSUM STILL OPEN  
**Issue:** #287  
**Scope:** Source-backed identities for synthetic design/review only. No real secret or empirical execution.

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

## Release artifact pin — OPEN

The release publishes `checksums.txt` plus platform archives including `tlock_1.2.0_linux_amd64.tar.gz`. The exact release-asset SHA-256 has **not yet been independently retrieved and retained through the available tooling in this review**.

Therefore:

```yaml
selected_binary: tlock_1.2.0_linux_amd64.tar.gz
selected_binary_sha256: null
binary_pin_status: OPEN / FAIL-CLOSED
```

No Mode T implementation may download and execute this artifact until the exact checksum is independently retrieved from the release evidence, recomputed against the downloaded bytes, and retained in the P4-T mechanism evidence packet.

## Strict chain requirement

The `tlock` source documents that a newly created Tlock trusts chain-hash metadata supplied by ciphertext by default and exposes `Strict()` to disable that switching behavior.

Source: [tlock chain-selection implementation](https://github.com/drand/tlock/blob/main/tlock.go).

Future decryption/continuity verification must use the frozen quicknet identity and strict chain binding. Ciphertext metadata is evidence to validate, not authority to select another chain.

## Security boundary

The drand timelock documentation explicitly states that a threshold number of malicious network nodes could compute future randomness and decrypt timelocked ciphertext early.

Source: [drand timelock encryption documentation](https://docs.drand.love/docs/timelock-encryption/).

This threshold-network trust assumption must remain visible in any final P4-T review. A successful synthetic `tle` test cannot prove the network assumption.

**Disposition:** source/chain pinning materially advanced; executable binary checksum remains OPEN. P4-T-A remains OPEN.
