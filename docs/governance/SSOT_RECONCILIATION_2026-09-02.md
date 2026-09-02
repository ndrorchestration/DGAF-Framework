# SSOT Reconciliation — 2026-09-02

## Purpose

Record the repository-wide current-state reconciliation after the P-35 remediation head advanced.

## Current authoritative identities

- PR #188: OPEN / DRAFT / NOT MERGED
- active P-35 remediation head: `9ba7677c98c2eb8502ca141b70ff59104ad89fea`
- latest head change: evidence-integrity correction to `p9-independent-evidence.sha256` for Windows CRLF/on-disk hashing
- P-35 runtime characterization: PRE-FREEZE / non-empirical / 54-of-54 / zero failed
- P-35 formal acceptance: PENDING
- latest controlled completion candidate: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`
- experimental boundary: PRE-FREEZE / FAIL-CLOSED
- freeze: NOT ESTABLISHED
- pilot authorization: NOT GRANTED
- empirical N: 0

## Historical boundary

`d83ea74c0f7ef7dd3e39a25345d6b201770a370c` is a predecessor remediation head. Any run/artifact produced for that SHA remains historical evidence for that exact SHA and is not current-head evidence. It must not be rebound to the experimental candidate.

## Acceptance boundary

Formal P-35 acceptance requires runner-boundary verification that:

1. `run_pilot()` rejects a missing premise checker before task construction;
2. an explicit premise checker reaches the DGAF `ConsensusTask` path; and
3. the regression evidence remains non-empirical.

## Required transition sequence

Formal P-35 acceptance → new exact experimental candidate → fresh candidate-bound P2/P3/P4/P5/P6/P8/P9/P6a evidence → freeze → authorization → empirical execution.

This document does not authorize experimentation and does not alter empirical N.
