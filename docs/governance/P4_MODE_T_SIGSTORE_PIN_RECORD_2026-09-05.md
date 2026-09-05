# P4 Mode T Sigstore / Cosign Pin Record — 2026-09-05

**Status:** DESIGN PIN / NOT EXECUTED / NOT A P4 CLOSURE RECORD  
**Issue:** #287  
**Scope:** Candidate transparency-client supply-chain identities for synthetic Mode T design and review only.

## Selected client release

GitHub currently reports Sigstore Cosign `v3.1.3` as the latest published release, dated 2026-08-06.

The release notes state that v3.1.3 resolves `GHSA-fx35-mq7g-6g98`, a verification bypass involving an unexpected public key in a legacy bundle. A Mode T design that relies on bundle verification must therefore not intentionally pin an older vulnerable release when the corrected release is available.

Source: [Sigstore Cosign v3.1.3 release](https://github.com/sigstore/cosign/releases/tag/v3.1.3).

## Linux amd64 executable identity

GitHub release metadata reports the exact asset digest:

```yaml
cosign_version: "3.1.3"
asset_name: "cosign-linux-amd64"
asset_size_bytes: 141178250
asset_sha256: "4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71"
```

The associated Sigstore bundle asset is also digest-bound:

```yaml
bundle_asset_name: "cosign-linux-amd64.sigstore.json"
bundle_asset_sha256: "e16547fbee348eb23bd7e5a4d542b540395faea2e7bb1d18da01bbc3cc74d57d"
```

The release checksum manifest and its Sigstore bundle are:

```yaml
checksums_asset_name: "cosign_checksums.txt"
checksums_asset_sha256: "aec2a6f68d307b09ae196e388dc691a146fa8bdba7fcce9ca4ca41b918adfa63"
checksums_bundle_name: "cosign_checksums.txt.sigstore.json"
checksums_bundle_sha256: "976bcb216e45ed0274e464e2e16d81e84cc85a69b3ed6e3488c1e7cda116379a"
release_public_key_name: "release-cosign.pub"
release_public_key_sha256: "f4cea466e5e887a45da5031757fa1d32655d83420639dc1758749b744179f126"
```

Source: [GitHub release API for current Cosign release](https://api.github.com/repos/sigstore/cosign/releases/latest).

## Required runtime pinning rule

A future Mode T transparency workflow must not install Cosign from a floating package-manager reference, `latest`, or unverified download.

Before use it must:

1. download the exact `cosign-linux-amd64` asset for the frozen version;
2. compute SHA-256 locally;
3. require exact equality with the frozen asset digest above;
4. verify the release-signature/bundle path under the separately reviewed Sigstore verification policy;
5. record the exact client version and digest in the P4-T mechanism evidence;
6. fail closed before R/C/X/L transparency publication if any identity or verification step differs.

The GitHub release object currently reports `immutable: false`. A tag or release URL by itself is therefore not treated as the executable identity; the content digest remains authoritative for the frozen mechanism.

## Relationship to transparency evidence

Cosign is only the client used to create or verify public transparency evidence. It is not itself the independent custody authority and it does not prove that the hosted execution environment protects live process memory.

The accepted Mode T claim would still depend on:

- expected GitHub OIDC issuer/workflow identity;
- valid transparency-log inclusion evidence;
- independently verified log/time semantics;
- frozen repository/workflow/helper identities inside each signed canonical record;
- the separate P4-T no-unilateral-access argument.

## Current disposition

**Cosign client pin materially established for design purposes.**

No Cosign binary has been executed in the empirical apparatus, no transparency entry has been created for empirical evidence, and no P4/P7/P8/P9/freeze/authorization/empirical state has changed.
