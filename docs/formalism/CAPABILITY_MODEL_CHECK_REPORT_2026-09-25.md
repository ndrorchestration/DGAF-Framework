# DGAF Capability Governance — Bounded Model-Check Report

> **Status:** PROSPECTIVE / NON-AUTHORIZING  
> **Scope:** draft PR #1041 capability-governance reference model  
> **Evidence class:** bounded local engineering/conformance evidence

## Result

The bounded model checker reports no findings for the current reference model.

Current focused result:
- `tests/test_capability_model_check.py`: **12/12 PASS**

Current broader capability-selected result:
- `python -m pytest tests -k capability -q`: **127 passed, 1 skipped**

These results do not establish production security, exhaustive formal verification, empirical efficacy, independent validation, scientific-N promotion, or High-Assurance authorization.
## Enumerated state space

The current checker evaluates:
- graph-path safety from `PROPOSED` through protected execution and closure;
- 128 authorization-guard Boolean combinations;
- 32 commit/replay combinations including consumed authorization;
- 4 receipt/unknown-outcome combinations;
- 2 audit-before-closure combinations;
- 32 workflow-composition combinations;
- 1,128 recovery/postcondition combinations;
- bounded two-worker idempotency claim interleavings plus digest-conflict and unknown-outcome cases.

The Boolean/product portions cover **1,330 bounded combinations** in addition to graph-path checks and explicit mutation/counterexample tests.
## Properties checked

The checker currently probes:
- authorization and commit revalidation cannot be bypassed on an execution path;
- executed state cannot bypass executing state;
- unknown execution outcome cannot directly re-execute or become executed;
- failed/inconclusive postconditions cannot close without recovery/escalation;
- authorization guard conjunction is fail-closed;
- commit-time authorization, digest, guard, consumption, and idempotency predicates are fail-closed;
- execution receipt and unknown-outcome predicates remain distinct;
- closure requires audit evidence;
- composition authorization is separate from individual action authorization;
- protected data cannot flow to an unapproved external destination in the bounded workflow model;
- partial execution preserves recovery semantics;
- competing same-digest idempotency claims produce one bounded reservation winner;
- one idempotency key cannot bind two action digests;
- unknown outcomes block retry until reconciliation.
## Mutation / counterexample checks

The tests deliberately mutate or replace safe behavior to confirm the checker detects:
- AUTHORIZED -> EXECUTING shortcut;
- EXECUTION_OUTCOME_UNKNOWN -> EXECUTING retry edge;
- postcondition failure -> direct CLOSED edge;
- an allow-all workflow-composition evaluator;
- a recovery classifier that erases execution history;
- an idempotency ledger that allows multiple competing reservation winners.

A passing reference model without counterexample sensitivity would be insufficient evidence.

## Boundary and next step

This is a small finite model, not a proof over arbitrary distributed implementations.

Next justified expansion:
1. persistent-state idempotency across process restart;
2. stronger concurrency/interleaving models;
3. larger workflow composition graphs and multi-hop data labels;
4. credential-broker trust-root/token-boundary state;
5. provider/runtime identity substitution;
6. degraded-mode and partition behavior.
