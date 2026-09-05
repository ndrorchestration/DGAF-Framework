# P4 Mode T tlock Supply-Chain Verification — 2026-09-05

**Status:** SYNTHETIC SUPPLY-CHAIN VERIFICATION LANE / PENDING EXACT-HEAD CI  
**Issue:** #287  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Close one narrow Mode-T design blocker without instantiating custody or touching the empirical apparatus: independently recompute the SHA-256 of the official `drand/tlock` v1.2.0 Linux amd64 release archive and compare it with the checksum published in that release's `checksums.txt`.

This verification is engineering/supply-chain evidence only. It does not establish the drand threshold-network assumption, hosted-runner memory confidentiality, P4 custody sufficiency, freeze, authorization, or efficacy.

## Frozen release identity

```yaml
project: drand/tlock
version: "1.2.0"
release_tag: v1.2.0
asset_name: tlock_1.2.0_linux_amd64.tar.gz
checksum_manifest: checksums.txt
source_release: https://github.com/drand/tlock/releases/tag/v1.2.0
```

The earlier Mode-T design review recorded the signed tag/source identities and quicknet chain identity separately. This lane is limited to the release-archive content checksum that remained OPEN because the prior tool environment could not independently retrieve the release bytes.

## Workflow

`.github/workflows/p4-mode-t-tlock-supply-chain.yml` performs the following on a standard GitHub-hosted runner:

1. downloads the exact v1.2.0 `checksums.txt` and Linux amd64 archive from the fixed release URL;
2. extracts the checksum for the exact archive filename;
3. recomputes SHA-256 locally with `sha256sum`;
4. requires exact equality;
5. emits a non-secret evidence record containing the published and recomputed digests;
6. uploads only the checksum manifest and verification record as a 30-day Actions artifact.

The artifact-upload action is pinned to exact commit `ea165f8d65b6e75b540449e92b4886f43607fa02` rather than a floating tag.

## Acceptance rule

This blocker may move from `OPEN` to `VERIFIED FOR THE EXACT RELEASE ASSET` only when all of the following are true:

- the exact-head workflow concludes SUCCESS;
- the evidence record reports `match=true`;
- `published_sha256` and `computed_sha256` are identical 64-character lowercase hex values;
- the workflow run and artifact identities are retained in a follow-up exact-boundary record;
- no other P4 state is promoted by association.

Any download failure, missing manifest entry, malformed checksum, digest mismatch, workflow failure, or missing evidence artifact remains fail-closed.

## Non-effects

This lane does **not**:

- execute `tlock`;
- generate, encrypt, decrypt, or expose a blinding secret;
- create a condition mapping or commitment nonce;
- execute an empirical workload;
- establish hosted-runner memory confidentiality;
- establish Sigstore/Rekor sufficiency;
- choose the final analysis-lock window;
- close P4, P7, P8, or P9;
- create a freeze;
- grant pilot authorization;
- change empirical N.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
