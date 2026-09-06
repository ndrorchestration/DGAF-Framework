# P4-B Mode T Cross-Runner Reproducibility — 2026-09-05

**Status:** ENGINEERING REPRODUCIBILITY TRANCHE / NON-LIVE / NON-AUTHORIZING  
**Issue:** #295  
**Parent verifier prototype:** draft PR #300  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Test whether the exact P4-B strict continuity verifier source produces the same Linux/amd64 binary identity on two materially different GitHub-hosted Ubuntu runner images while holding the Go toolchain, tlock source/module graph, target architecture, CGO state, and build flags fixed.

This is stronger than rebuilding twice on one runner, but it is deliberately not described as independent-operator reproducibility: both environments remain under the GitHub Actions service/operator boundary.

## Frozen build identity

```yaml
tlock_version: v1.2.0
tlock_source_commit: 7b54141a9733fd6fa207587a11148280e6fb020d
go_version: 1.22.12
gotoolchain: local
target_goos: linux
target_goarch: amd64
goamd64: v1
cgo_enabled: 0
setup_go_commit: 924ae3a1cded613372ab5595356fb5720e22ba16
download_artifact_commit: 37930b1c2abaa49bbe596cd826c3c89aef350131
upload_artifact_commit: b7c566a772e6b6bfb58ed0dc250532a479d7789f
```

The pinned artifact actions both declare `node24`. They replace earlier pins that GitHub's 2026 runner compatibility layer would otherwise force from Node-20 actions onto Node 24.

The build command is fixed to:

```text
go build -mod=readonly -trimpath -buildvcs=false -ldflags=-buildid=
```

## Environmental diversity

The workflow builds independently on:

- `ubuntu-22.04`
- `ubuntu-24.04`

Each job checks out the exact DGAF evidence SHA, installs exact Go 1.22.12 with `GOTOOLCHAIN=local`, fetches the exact upstream tlock source commit, verifies the upstream module graph with `go mod verify`, overlays only the exact DGAF verifier source, and produces the fixed Linux/amd64 target.

The compiled binaries are **not uploaded**. Each runner records only source/module/toolchain provenance and the resulting binary SHA-256, then deletes the binary before artifact upload. The evidence SHA-256 sidecars contain relocation-safe basenames so they remain verifiable after artifact extraction into a different directory.

## Comparison contract

The final comparison job downloads only the two text provenance artifacts and fails unless both runners agree on:

- DGAF evidence SHA;
- tlock version/source commit;
- Go version and fixed target variables;
- verifier source SHA-256;
- upstream `go.mod` SHA-256;
- upstream `go.sum` SHA-256;
- final binary SHA-256.

The combined evidence record explicitly states:

```yaml
cross_runner_binary_identical: true
same_ci_operator: true
independent_operator_reproducibility_established: false
live_decryption_executed: false
empirical_data_collection: false
freeze_established: false
pilot_authorized: false
empirical_n: 0
```

If the binary digests differ, the workflow fails closed. A mismatch is a reproducibility defect to investigate; it is not normalized away and must not be reinterpreted as acceptable evidence.

## Initial fail-closed finding

The first comparison run did not reach the binary-digest equality check. Both Ubuntu builds completed successfully, but each sidecar contained its original build-directory path. After artifact relocation the comparator could not resolve that path, so the lane failed closed. The workflow was corrected to write basename-only sidecars before any reproducibility result was accepted.

That failure is retained as apparatus-debugging history and must not be described as evidence of either binary equality or binary inequality.

## Epistemic boundary

A PASS establishes only this narrower claim:

> Under two GitHub-hosted Ubuntu image families, with an exact fixed Go toolchain, exact upstream tlock source/module graph, identical verifier source, fixed target architecture, CGO disabled, and deterministic build flags, the produced verifier binary SHA-256 was identical for the tested repository head.

A PASS does **not** establish:

- independent operator or independent hardware reproducibility;
- reproducibility outside GitHub Actions;
- compiler/bootstrap trust;
- hosted-runner memory confidentiality;
- correct live quicknet decryption;
- post-release continuity for any DGAF protected material;
- P6 durable custody;
- freeze, authorization, empirical execution, or efficacy.

## Remaining #295 blockers after a possible PASS

Even if this tranche passes, #295 remains open pending at least:

- successful strict correct-quicknet synthetic/test decryption;
- explicit too-early and wrong-commitment execution evidence;
- independent-operator or otherwise separately controlled rebuild evidence if required for final acceptance;
- final protected ciphertext/plaintext-commitment binding contract;
- leakage and hosted-runner memory review for the accepted continuity path;
- exact final run/attempt/tool/ciphertext/helper provenance;
- P6/transparency retention of accepted continuity evidence.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
