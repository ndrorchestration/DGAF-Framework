# TGL / PR #132 Adversarial Review — 2026-08-28

## Purpose

This record captures the comprehensive adversarial review of PR #132 and the `ProcludingPremiseGate` contract failure. It is a diagnostic and governance record, not an experimental authorization record.

## Current disposition

- PR #132: **BLOCKED / DRAFT / UNMERGED**.
- Observed pre-freeze regression: **41 passed / 2 failed**.
- The failure is treated as a concrete contract-regression signal, not merely a test to rerun.
- The failure is reproducible at the TGL → P-35 boundary.
- No new experimental freeze is created by this review.
- Pilot authorization remains **NOT GRANTED**.
- Empirical N remains **0**.

## Root contract finding

The established P-35 interface requires a constructor carrying `invariants`, `session_id`, and `agent_id`, and exposes `evaluate(input_text, check_fn=...)`. PR #132 instead invokes a simplified constructor and `check()` method. The branch also fails to pass the configured `premise_check_fn` into P-35. These are distinct contract mismatches.

The violation path contains an additional latent mismatch where the TGL-side exception construction does not match the P-35 `PremiseViolationError` contract. A local constructor-only fix is therefore insufficient.

## TGL state-machine findings

`PASS`, `WARN`, `SKIP`, `ESCALATE`, and `KILL` must have explicit transition semantics. `SKIP` is not semantically homogeneous and must distinguish at least:

- `UNWIRED` — required governance was not invoked;
- `DEPENDENCY_SKIPPED` — an upstream gate prevented execution;
- `NOT_APPLICABLE` — the gate is intentionally outside the current path.

Required-gate absence must not be inferred solely from numeric step ranges. Requiredness should be declared through authoritative gate metadata.

Status reduction must be explicit rather than distributed through ad-hoc conditionals. The intended severity ordering is terminal KILL/KILL_REC, then ESCALATE, then WARN, then PASS, with gate-specific recovery semantics retained.

## Exception containment

Governance hook exceptions must remain contained by the TGL control plane and resolve to a governed fail-closed outcome. Arbitrary hook exceptions must not escape `run_turn()` as uncontrolled application exceptions.

## Audit and cryptographic provenance

The final sealed representation must be exactly the representation returned as authoritative audit state. A seal generated before a final Herald/gate record is appended is not sufficient if that final record is represented as part of the sealed gate set.

Canonical serialization should be deterministic and unambiguous. Field-delimiter concatenation must not permit ambiguous encodings through delimiter-bearing field values.

P-35 and TGL input identity should use the same full SHA-256 representation where the records describe the same governed input. Truncated secondary hashes must not be mistaken for the canonical input identity.

## PDMAL integration

The PDMAL adapter is an integration seam, not an alternate TGL API. Its contract requires exact canonical input identity, deterministic TGL invocation, explicit decision reduction, and bounded state transitions. TGL/PDMAL tests must exercise the real P-35 injection path rather than merely instantiate a compatible-looking object.

No change to the experimental treatment hooks, pilot runner authorization logic, blinding protocol, statistical plan, or freeze boundary is part of the remediation scope.

## CI/CD and deployment identity

A CI workflow must prove that the tree it executes is the same tree whose SHA it records as evidence. PR checkout refs and `GITHUB_SHA` must not be treated as interchangeable without an explicit equality assertion.

Self-modifying validation workflows require additional provenance controls. A workflow that writes lockfiles or other changes into the candidate must bind any redispatch to the actual candidate head rather than a fixed unrelated branch.

A Vercel deployment marked READY is deployment evidence, not proof of exact source-to-runtime identity or authenticated P2/P6a verification.

## Governance boundaries

P6/P6a evidence custody and runtime verification remain separate from P7 scientific adjudication and P8 analysis closure. A TGL code repair does not close P7/P8, create a freeze, or authorize the pilot.

Historical candidates, freezes, runs, deployments, and acceptance records retain their original scope. Documentation lineage on `main` does not redefine an experimental apparatus identity.

## Minimal remediation decision

PR #132 should be rebuilt or minimally corrected from the established post-#131 TGL implementation rather than continuing an incremental rewrite. The remediation should:

1. restore the established P-35 constructor contract;
2. restore `evaluate(..., check_fn=...)` injection;
3. restore fail-closed exception containment;
4. declare required and conditional gate semantics explicitly;
5. implement one deterministic status reducer;
6. distinguish unwired SKIP from dependency-caused SKIP;
7. seal the exact final audit representation;
8. add regression tests for all identified failure modes;
9. preserve PDMAL experimental and authorization boundaries;
10. leave unrelated architectural refactoring outside the PR.

## Required regression coverage

At minimum, candidate validation should cover:

- all required gates present;
- one required gate unwired;
- WARN propagation;
- WARN followed by PASS;
- terminal KILL;
- KILL_REC recovery semantics;
- Phi-Closure WARN/FAIL-closed conditional HPG SKIP;
- dependency-caused SKIP;
- unwired required HPG escalation;
- injected P-35 premise hook execution;
- premise violation event generation;
- hook exception containment;
- complete gate-record semantics;
- seal sensitivity to gate-record mutation;
- equality of sealed and returned final audit state;
- full SHA-256 identity consistency;
- explicit Herald sealing boundary;
- no experimental treatment-hook mutation.

## Remediation candidate boundary

PR #133 is the isolated remediation candidate. It is a draft candidate only and must be independently validated before any merge decision. Its existence does not alter the experimental candidate, freeze state, authorization state, or empirical N.

## Final governance statement

The adversarial review establishes a **TGL contract-coherence blocker**, not an experimental result. The system remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N = 0** until the independent governance sequence is completed.
