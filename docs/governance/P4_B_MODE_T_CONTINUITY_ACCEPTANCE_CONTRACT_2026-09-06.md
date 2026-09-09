# P4-B Mode T Continuity Acceptance Contract — 2026-09-06

## Status

Status: STRUCTURAL FINAL-EVIDENCE BINDING CONTRACT / SYNTHETIC TESTS ONLY / NOT FINAL
ADJUDICATION / ISSUE #295 OPEN.

Scientific boundary remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

Issue #295 requires the eventual protected continuity result to bind one exact identity
graph rather than a loose collection of individually plausible records. The contract in
`mode_t_continuity_acceptance.py` validates that graph without claiming that the
underlying protected execution, independent custody, or review has occurred.

## Bound identity graph

The packet binds:

1. exact repository and control-plane commit;
2. verifier path, Git blob SHA, source SHA-256, and binary SHA-256;
3. pinned tlock version/source commit and Go/target/CGO build identity;
4. exact continuity-report digest, GitHub run ID and attempt;
5. ciphertext digest and separately expected plaintext commitment;
6. strict-chain and non-leakage/non-promotion report fields;
7. retained and independently retrieved report digests;
8. retention/retrieval receipt digests, Sigstore bundle digest, TrustedRoot digest,
   retention location, and distinct producer/retrieval actor identities; and
9. an explicitly unexecuted independent-adjudication slot.

Exact-key validation rejects silent schema extension as well as omission. Cross-field
digest and identity checks reject substitution between repository, helper, report,
retention, and retrieval surfaces.

## Deliberate trust boundary

A successful function result is named `PASS_STRUCTURAL_BINDING_ONLY`. The module does
not perform the final protected continuity run, sign or upload a transparency record,
retrieve an external archive, cryptographically verify a bundle, authenticate an
independent actor, or adjudicate Issue #295.

Those operations must supply independently verified inputs through their accepted
mechanisms. Caller booleans do not become final authority merely because this schema
checks their shape. Final adjudication is deliberately required to remain
`NOT_EXECUTED` inside the structural packet so the producer cannot self-close its own
evidence.

## Fail-closed cases

Tests reject:

- repository, control-plane, helper, source, binary, tlock, toolchain, or target drift;
- continuity-report/run mismatch;
- retained or retrieved digest mismatch;
- identical producer and retrieval actors;
- absent cryptographic-bundle or independent-retrieval verification markers;
- plaintext persistence/emission or empirical-state promotion;
- self-asserted reviewer identity, adjudication digest, or final acceptance; and
- added or missing schema keys.

## What this advances

This closes the **design/implementation gap for a single final-evidence binding
contract**. It does not satisfy the three remaining Issue #295 acceptance predicates:

1. execute the eventual accepted protected continuity run and instantiate this packet
   with its exact identities;
2. retain, independently retrieve, and re-hash the accepted evidence through the final
   P6/transparency mechanism; and
3. obtain independent review and adjudication of the integrated path and retained
   evidence.

## Non-effects

No protected ciphertext, mapping, key, nonce, or plaintext is used. No external archive
or transparency entry is written. No reviewer is designated. Issue #295 remains open.
P4 is not closed; the final v0.7.6 candidate is not designated; P7/P8/P9 are not
promoted; freeze is not established; authorization is not granted; empirical N remains
zero.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 remains controlling.**
