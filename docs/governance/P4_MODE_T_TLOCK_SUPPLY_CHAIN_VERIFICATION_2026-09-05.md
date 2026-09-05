# P4 Mode T tlock Supply-Chain Verification — 2026-09-05

**Status:** SYNTHETIC SUPPLY-CHAIN VERIFICATION LANE / FRESH EXACT-HEAD VALIDATION REQUIRED  
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
5. emits a non-secret evidence record containing the PR-head evidence SHA, workflow GitHub SHA, published checksum, and recomputed checksum;
6. uploads only the checksum manifest and verification record as a 30-day Actions artifact named by the PR-head evidence SHA.

The artifact-upload action is pinned to exact commit `ea165f8d65b6e75b540449e92b4886f43607fa02` rather than a floating tag.

## Preliminary run — checksum verified, evidence packaging superseded

The first workflow execution on PR-head `ae0bc5e74d3bea806c8ae5621af78452710de4ad` completed successfully:

```yaml
workflow_run_id: 33998419801
job_id: 101392872824
published_sha256: 0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57
computed_sha256: 0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57
match: true
artifact_id: 9978745873
artifact_digest: sha256:8e685f46e2871ff6c7eb518d08d3255a771c4ad5062eec52a21b4a9cafe987c6
```

This establishes that the downloaded official release archive matched the checksum published in the official v1.2.0 manifest at that execution boundary.

However, the first artifact name used `${{ github.sha }}` under a pull-request event, which resolved to GitHub's synthetic PR merge SHA `04d88f2e511fa025e6ece839f1c89eaef8af198b` rather than the PR head. The artifact metadata itself correctly retained `head_sha=ae0bc5e74d3bea806c8ae5621af78452710de4ad`, but the filename ambiguity is avoidable and is not accepted as the final provenance form.

The workflow was therefore corrected to bind `EVIDENCE_SHA` to `github.event.pull_request.head.sha` for pull-request runs, with `github.sha` only as the workflow-event identity/fallback. A fresh exact-head run is required before final acceptance.

## Acceptance rule

This blocker may move from `OPEN` to `VERIFIED FOR THE EXACT RELEASE ASSET` only when all of the following are true:

- the corrected exact-head workflow concludes SUCCESS;
- the evidence record reports `match=true`;
- `published_sha256` and `computed_sha256` are identical 64-character lowercase hex values;
- the evidence record and artifact name bind the intended exact PR head;
- the workflow run and artifact identities are retained in a final exact-boundary record;
- no other P4 state is promoted by association.

Any download failure, missing manifest entry, malformed checksum, digest mismatch, workflow failure, evidence-SHA mismatch, or missing evidence artifact remains fail-closed.

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
