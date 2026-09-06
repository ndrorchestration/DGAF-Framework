# P4 Mode T — Side-effect-free Sigstore verifier boundary

Date: 2026-09-06  
Issues: #287 / #296 / #310 / #316  
Parent PR: #323  
Status: **VERIFIER CONTRACT / NO REAL BUNDLE VERIFICATION EXECUTED BY CI**

Controlling state remains **P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

PR #323 deliberately accepts a normalized `VerifiedTransparencyContext` rather than implementing Sigstore cryptography itself. That separation is useful, but it leaves an important trust seam if production code can populate verification booleans directly.

This tranche removes that caller-asserted cryptography seam without creating a second Sigstore implementation. It extracts only the existing verification behavior already designed in #299:

- exact Cosign executable SHA-256 verification;
- `cosign verify-blob` over existing artifact and bundle bytes;
- exact certificate identity;
- exact GitHub Actions OIDC issuer;
- bundle/transparency material normalization;
- handoff into #323's retention contract.

It does **not** extract #299's signing path, OIDC token request, public Rekor submission, or timing experiment.

## Deduplication rule

#299/#296 remains the canonical controlled public-signing/timing apparatus. This module reuses its pinned Cosign verification model rather than developing a second signing or transparency client.

No new public-transparency experiment issue is created by this tranche.

## `mode_t_sigstore_verifier.py`

The verifier requires:

1. an existing Cosign executable whose bytes match the reviewed SHA-256;
2. an existing public/non-secret record artifact;
3. an existing Sigstore bundle;
4. the exact expected certificate identity;
5. the GitHub Actions OIDC issuer `https://token.actions.githubusercontent.com`;
6. a positive `cosign verify-blob` result before any normalized verification context is returned.

The reviewed Cosign identity reused from #299 is:

```text
version policy: v3.1.3
linux-amd64 SHA-256: 4629c757b7618056f8ddd7e2625ae9fdd94c0372a65049520bc7d9df9efc7f71
```

The module additionally requires exactly one transparency-log entry, a non-negative log index, a non-empty log identity, and inclusion proof or inclusion promise material before normalization.

## Trust interpretation

A real successful call to `verify_sigstore_bundle(...)` can establish that the supplied artifact/bundle passed the reviewed local Cosign verification command and can produce the normalized cryptographic predicates consumed by #323.

That is still narrower than real P6 retention. The verifier itself performs no external write and therefore cannot establish that an independently controlled durable copy exists.

It also does not promote Rekor `integratedTime` into independent temporal-order proof. `integratedTime` remains metadata only.

## CI boundary

The dedicated CI lane validates the interface with deterministic local fixtures and mocks the Cosign process result. This proves command construction, exact executable hashing, fail-closed parser behavior, handoff to #323, and non-promotion semantics.

**CI PASS must not be described as a real Sigstore cryptographic verification.** No authentic signed bundle fixture is supplied by this tranche and no public Rekor action is performed.

A real cryptographic evidence claim requires an actual artifact/bundle generated or retrieved through the separately controlled evidence process and an actual pinned Cosign execution whose result and bytes are retained.

## Negative controls

Tests reject or constrain:

- wrong Cosign executable digest before subprocess execution;
- unexpected OIDC issuer before subprocess execution;
- non-zero Cosign verification result;
- multiple transparency entries where the contract expects exactly one;
- missing inclusion material;
- any interpretation that cryptographic verification establishes external retention, time order, freeze, pilot authorization, or empirical N>0.

Static CI guards prohibit `sign-blob`, OIDC write permission, Google authentication, freeze/authorization promotion markers, and external-signing behavior from entering this workflow.

## Remaining real blockers

This tranche does not close:

- independently retained and re-verifiable R/A/C admission-policy evidence under #316;
- actual Sigstore bundle verification for a real Mode-T public record;
- independent durable external retention/retrieval;
- duplicate/one-C-per-authorization adjudication on the real external evidence source;
- independent L-before-release time/order evidence if that predicate remains required;
- independent security review;
- authenticated Confidential Space execution and independently reverified PRE/POST evidence;
- repository merge-enforcement configuration.

**P4 OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
