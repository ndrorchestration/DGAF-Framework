# P4-B Mode T Synthetic Quicknet Behavior — 2026-09-05

**Status:** SYNTHETIC BEHAVIOR TRANCHE / NON-SECRET / NON-AUTHORIZING  
**Issue:** #295  
**Parent verifier work:** draft PRs #300 and #301  
**Scientific state:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Purpose

Exercise the strict P4-B continuity verifier against the real public drand quicknet transport while keeping all plaintext synthetic, random, local, and explicitly outside the protected DGAF custody path.

This tranche is intended to test behavior that offline source and wrong-chain fixtures cannot fully demonstrate:

- successful strict decryption on the frozen quicknet identity;
- fail-closed rejection of a wrong plaintext commitment after a successful decryption path;
- fail-closed TOO_EARLY classification for a genuinely future quicknet round with one verifier invocation and no retry;
- repeated verification producing byte-identical evidence without tracked repository mutation;
- explicit frozen-chain metadata preflight rejection;
- captured verifier stream and artifact-candidate scanning for synthetic plaintext canaries.

It does **not** use or create protected DGAF mapping material, pilot observations, treatment assignments, analysis keys, empirical results, or authorization state.

## Frozen identity

```yaml
tlock_version: v1.2.0
tlock_source_commit: 7b54141a9733fd6fa207587a11148280e6fb020d
quicknet_endpoint: https://api.drand.sh
quicknet_chain_hash: 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971
quicknet_scheme: bls-unchained-g1-rfc9380
quicknet_public_key_hex: 83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a
go_version: 1.22.12
gotoolchain: local
target_goos: linux
target_goarch: amd64
goamd64: v1
cgo_enabled: 0
```

The workflow uses immutable Node-24-native action pins already adopted by the parent verifier/reproducibility work.

## Synthetic fixture construction

`experiments/pdmal_pilot/mode_t_synthetic_quicknet_fixture.go` retrieves only public quicknet metadata and validates chain hash, scheme, and public key before constructing a fixture.

For each fixture it generates 32 random bytes locally and constructs a synthetic plaintext of the form:

```text
DGAF-SYNTHETIC-P4B-<random-hex>
```

That plaintext is not a DGAF secret and has no relationship to any mapping, assignment, outcome, key, pilot record, or empirical datum.

Two independent ciphertexts are created:

1. **available fixture** — target round is derived from approximately 30 seconds before fixture creation and must be at or below the current round;
2. **future fixture** — target round is derived from approximately 60 seconds after fixture creation and must be strictly above the current round.

Encryption is local. The public quicknet endpoint is used only for network metadata and, during verification, public beacon signatures.

## Behavioral acceptance contract

The CI lane must fail unless all of the following are true.

### Correct-chain strict success

The available ciphertext is passed to the dedicated verifier with its separately written SHA-256 plaintext commitment.

The result must report:

- `status=PASS`;
- frozen chain identity;
- network metadata verified;
- public key verified;
- strict chain enforcement true;
- plaintext commitment match true;
- plaintext persisted false;
- plaintext emitted false;
- empirical collection false;
- freeze false;
- authorization false;
- empirical N=0.

The same ciphertext is then verified a second time under the same repository/run identity. The two JSON outputs must be byte-identical.

Tracked repository state must remain unchanged after both invocations.

### Wrong plaintext commitment

The already-available ciphertext is verified with an intentionally incorrect all-zero SHA-256 commitment.

The process must:

- exit fail-closed;
- emit no success stdout;
- classify the failure exactly as `PLAINTEXT_COMMITMENT_MISMATCH`;
- retain empirical N=0.

This demonstrates that successful decryption alone is insufficient for continuity acceptance.

### Future-round TOO_EARLY

The future ciphertext is passed to the verifier exactly once while its target round is still above the current round.

The process must:

- exit fail-closed;
- emit no success stdout;
- classify the failure exactly as `TOO_EARLY`;
- perform no workflow-level retry or wait-loop;
- retain empirical N=0.

The future ciphertext is retained as synthetic evidence, but the workflow does not later retry it after the round becomes available.

### Frozen metadata preflight

An additional offline test presents a network object whose chain hash differs from the frozen quicknet identity. The verifier metadata preflight must reject it before decryption and must not invoke chain switching.

## Plaintext canary boundary

Each synthetic plaintext is temporarily written to a mode-0600 local canary file solely so the workflow can scan:

- artifact candidates;
- captured verifier stdout;
- captured verifier stderr.

The workflow fails if either full synthetic plaintext canary appears in those surfaces. The canary files and captured local streams are deleted before artifact upload, and the verifier/fixture binaries are also deleted before upload.

This provides evidence against plaintext propagation into the **captured surfaces tested by this lane**. It does **not** prove:

- absence from transient hosted-runner memory;
- absence from provider-level infrastructure telemetry outside accessible job streams;
- secure erasure of every compiler/runtime/network buffer;
- a general hosted-runner confidentiality theorem.

Those remain separate trust-boundary questions.

## Retained evidence

The uploaded artifact may contain only non-secret synthetic evidence, including:

- synthetic tlock ciphertexts;
- plaintext SHA-256 commitments;
- fixture manifests containing hashes and public network metadata;
- PASS/FAIL classification JSON;
- build/tool/source identities;
- exact repository/run/attempt binding;
- file digest manifest;
- combined non-promoting evidence summary.

Synthetic plaintext canaries themselves are never uploaded.

## External side effects

This lane performs public quicknet reads only. It does not publish to Rekor or another transparency service, create a custody object, mutate a remote scientific record, or perform an irreversible public registration action.

The separate controlled Rekor experiment in #299 remains unexecuted.

## Epistemic boundary

A PASS supports this narrow claim:

> For the exact tested DGAF verifier source and frozen tlock/quicknet identities, a non-secret synthetic quicknet ciphertext could be strictly decrypted and matched to its precommitted SHA-256; an intentionally wrong plaintext commitment was rejected; a separate genuinely future-round ciphertext failed once as TOO_EARLY; repeated accepted verification was output-stable and did not modify tracked repository state; and the tested captured output/artifact surfaces did not contain the synthetic plaintext canaries.

A PASS does **not** establish accepted continuity for any real DGAF protected material.

## Remaining #295 blockers after a possible PASS

Even if this tranche passes, #295 remains open pending final decisions/evidence for at least:

- the exact accepted protected ciphertext and separately committed expected plaintext digest contract;
- accepted post-release run/attempt/tool/ciphertext/helper provenance;
- hosted-runner memory/confidentiality and cleanup assumptions for the real protected path;
- durable P6/transparency retention independent of ordinary deletable GitHub artifact storage;
- independent-operator reproducibility if required by final acceptance criteria;
- same-day final red-team/review of the accepted continuity path and its evidence boundary.

No real protected continuity verification, custody closure, freeze, P4 authorization, analysis lock, empirical execution, efficacy finding, or increase in N is created by this tranche.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
