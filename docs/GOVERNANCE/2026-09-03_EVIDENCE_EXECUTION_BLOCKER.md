# 2026-09-03 — Exact-Candidate Evidence Execution Blocker

## Purpose
Record the current control-plane boundary after mainline documentation reconciliation and prevent a tooling limitation from being mistaken for scientific evidence.

## Current mainline candidate
- Commit: `637023b28492783f50d77550d4ed8e0867cbcc3d`
- Previous exact runtime evidence for `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` is superseded by this new mainline SHA.
- Therefore P2/P6a must be re-established against the new candidate before being treated as current.

## Required next evidence
1. Exact-candidate P2 runtime verification.
2. Exact-candidate P6a CORS verification.
3. Exact-candidate P4 operational blinding/custody evidence.
4. Exact-candidate P5 reproducibility/toolchain/topology/RNG evidence.
5. P6 durable external custody, independent retrieval, SHA-256 recomputation, and round-trip record.
6. Exact P7 final candidate/protocol/analysis binding.
7. P8 fail-closed statistical gate using the adopted configuration.
8. Current-candidate independent P9 verification.

## Workflow-control requirement
The PDMAL instrumentation workflow is intentionally restricted to experiment-path changes and deliberate `workflow_dispatch`. Its successful PR-candidate run is not evidence for the current mainline candidate.

The connected GitHub integration available for repository operations does not expose a workflow-dispatch action. Consequently, no current-main deliberate PDMAL evidence run is claimed here.

## Safety boundary
- Freeze: NOT ESTABLISHED
- Authorization: NOT GRANTED
- Empirical N: 0
- Experimental efficacy: NOT ESTABLISHED

This record is a control-plane blocker record, not experimental evidence.
