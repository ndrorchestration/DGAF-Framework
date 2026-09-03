# 2026-09-03 — Exact-Candidate Evidence Execution Blocker

## Purpose

Record the current control-plane boundary after mainline documentation reconciliation and prevent a tooling limitation from being mistaken for scientific evidence.

## Current mainline candidate

- Commit: `637023b28492783f50d77550d4ed8e0867cbcc3d`
- Previous exact runtime evidence for `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` is superseded by this new mainline SHA.
- Therefore the remaining gates must be evaluated against the applicable exact candidate; closed runtime evidence is not reopened merely because documentation changed.

## Required next evidence

1. Exact-candidate P4 operational blinding/custody evidence.
2. Exact-candidate P5 reproducibility/toolchain/topology/RNG evidence.
3. P6 durable external custody, independent retrieval, SHA-256 recomputation, and round-trip record.
4. Exact P7 final candidate/protocol/analysis binding.
5. P8 fail-closed statistical gate using the adopted configuration.
6. Current-candidate independent P9 verification.

## Workflow-control requirement

The PDMAL instrumentation workflow is intentionally restricted to experiment-path changes and deliberate `workflow_dispatch`. Its successful PR-candidate run is not evidence for a current-main candidate.

The connected GitHub integration available for repository operations does not expose a workflow-dispatch action. Consequently, no current-main deliberate PDMAL evidence run is claimed here.

## Safety boundary

- Freeze: NOT ESTABLISHED
- Authorization: NOT GRANTED
- Empirical N: 0
- Experimental efficacy: NOT ESTABLISHED

This record is a control-plane blocker record, not experimental evidence.
