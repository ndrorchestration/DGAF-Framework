# PDMAL / DGAF-TGL Adapter Specification v0.7

## Status

**CANDIDATE / PRE-FREEZE / NOT APPROVED FOR PILOT**

This document defines the proposed Path A bridge between the numeric PDMAL consensus workload and the repository's verified text-oriented DGAF governance primitive. It is a candidate adapter contract, not an authorization to collect empirical data.

## Verified runtime primitive

At implementation commit `8677ea090b47b352a8acf76692f1aa548f6fe392`, the repository provides:

```text
module: pptl.triadic_governance_loop
class: TriadicGovernanceLoop
callable: run_turn(input_text: str, context: Optional[dict]) -> TurnAuditRecord
```

The returned `TurnAuditRecord` contains gate records, final turn status, timestamps, and a SHA-256 seal. The primitive does not directly consume numeric consensus vectors or return numeric consensus weights.

The previously proposed `dgaf.engine.run_governance_cycle` interface is not part of the verified repository contract and must not be used.

## Repository interface-consistency blocker

`pptl/orchestrator.py` references `TGLConfig` and `TurnContext`, while the verified `pptl/triadic_governance_loop.py` implementation exposes `TGLHooks`, `TriadicGovernanceLoop`, and `run_turn`. This discrepancy must be resolved or the adapter must pin and import the verified `run_turn` interface directly, with repository-wide integration tests updated accordingly.

No freeze may rely on an ambiguous runtime alias.

## Objective

Preserve the original research question while avoiding an invented numeric DGAF API:

> Does a DGAF-governed decision layer change consensus execution outcomes under the frozen PDMAL workload and failure model?

The adapter must therefore make the governance-to-consensus bridge explicit, deterministic, auditable, and bounded.

## Adapter boundary

Proposed module:

```text
experiments/pdmal_pilot/dgaf_tgl_adapter.py
```

The adapter is responsible only for:

1. canonicalizing numeric consensus state and failure/topology context;
2. producing a deterministic TGL input string and context object;
3. invoking the pinned `TriadicGovernanceLoop.run_turn` interface;
4. mapping the resulting audit record into a finite governance decision;
5. applying that decision to the consensus update operator.

The adapter must not perform statistical analysis, unblinding, or protocol authorization.

## Canonical adapter input

Each governance turn receives a structured state object containing:

```text
seed_id
condition = DGAF
iteration
agent_values: fixed-length numeric vector
alive: fixed-length boolean vector
original_neighbors: canonical adjacency lists
active_neighbors: derived adjacency lists
failure_history: ordered immutable failure events
failure_count_current
failure_count_total
current_final_std
current_mean
runtime_budget_remaining_ms
protocol_id
adapter_version
```

The vector length and node ordering are frozen by the topology implementation. No implicit dictionary ordering or non-canonical serialization is permitted.

## Deterministic serialization

The adapter constructs a canonical, versioned text representation from the above state:

```text
PDMAL_DGAF_ADAPTER_V1
protocol=<protocol-id>
adapter=<adapter-version>
iteration=<int>
values=<canonical IEEE-754 decimal representation>
alive=<bit-vector>
neighbors=<canonical sorted adjacency encoding>
failure_history=<canonical ordered encoding>
metrics=<canonical metric encoding>
budget_ms=<integer>
```

The same structured state must produce byte-identical `input_text` and equivalent context content across executions.

No natural-language paraphrasing or model-generated prompt text is permitted.

## TGL context

The `context` dictionary contains the same canonical state plus an explicit adapter namespace:

```text
context["pdmaltgl"]["schema_version"]
context["pdmaltgl"]["state"]
context["pdmaltgl"]["failure_history"]
context["pdmaltgl"]["metrics"]
context["pdmaltgl"]["decision_policy_id"]
```

The context is informational and auditable. It must not contain secrets.

## Governance decision vocabulary

The audit record is converted into exactly one of the following decisions:

```text
NO_CHANGE
CONSERVATIVE_MIX
ISOLATE_FAILED_NEIGHBORS
FAIL_CLOSED
```

No other decision values are valid.

The mapping is deterministic and based only on the returned `TurnAuditRecord` fields:

```text
FAIL_CLOSED
  if final_status in {KILL, KILL_REC}

CONSERVATIVE_MIX
  if final_status == WARN or final_status == ESCALATE

ISOLATE_FAILED_NEIGHBORS
  if final_status == PASS and the verified PDMAL convergence-monitor gate
  explicitly records a failure/recovery event requiring isolation

NO_CHANGE
  otherwise
```

The exact gate-to-decision precedence and any required gate-name filters must be frozen in the implementation before pilot use. The adapter must not inspect free-form audit text or notes to make decisions.

## Decision-to-consensus mapping

The numeric consensus engine applies the following frozen operators:

```text
NO_CHANGE
  α = 0.5 over active neighbors

CONSERVATIVE_MIX
  α = 0.2 over active neighbors

ISOLATE_FAILED_NEIGHBORS
  remove failed nodes from the active neighbor set and use α = 0.5

FAIL_CLOSED
  terminate the current attempt with AttemptStatus.FAILURE
```

No decision may modify topology beyond the explicitly defined `ISOLATE_FAILED_NEIGHBORS` action. No decision may invent new edges.

## Determinism requirements

For identical:

```text
state
failure history
protocol ID
adapter version
TGL source SHA
policy configuration
```

multiple runs must produce identical:

```text
serialized input
context representation
TGL decision
numeric update
```

Wall-clock timestamps and audit seals are retained as provenance but are not valid decision inputs.

## TGL hook configuration

The adapter must construct `TGLHooks` explicitly. Any hook used for experimental decision-making must be a repository-pinned deterministic callable with a documented signature and tests.

Hooks that are left unset produce `SKIP` and therefore cannot silently contribute to the DGAF decision.

The adapter must not rely on an unverified `IntegratedOrchestrator` path while the `TGLConfig`/`TurnContext` mismatch remains unresolved.

## Failure semantics

Adapter-level failures are classified as follows:

```text
TGL import/interface failure          → AttemptStatus.FAILURE
serialization contract violation      → AttemptStatus.FAILURE
invalid decision vocabulary           → AttemptStatus.FAILURE
TGL KILL / KILL_REC                    → governance FAIL_CLOSED
TGL execution timeout                 → AttemptStatus.TIMEOUT
```

No adapter exception may be converted into a successful trial.

## Provenance fields

Every adapter invocation must record:

```text
protocol_id
protocol_sha
experiment_commit_sha
adapter_version
TGL_source_sha
TGL_input_hash
TGL_audit_seal_hash
decision
decision_policy_id
iteration
seed_id
attempt
runtime_ms
```

The TGL source SHA must identify the exact repository commit containing the imported implementation.

## Contract tests required before implementation gate reopens

At minimum:

1. canonical serialization is deterministic;
2. identical state yields identical TGL input hash;
3. every `TurnStatus` maps to a valid decision;
4. invalid/unknown statuses fail closed;
5. `FAIL_CLOSED` terminates the attempt;
6. failed nodes are isolated only under the explicit decision;
7. no decision depends on timestamps or audit seal values;
8. TGL interface import is pinned and tested;
9. adapter works under multiprocessing `spawn` semantics;
10. 2-seed contract mode produces only validation artifacts and no pilot dataset.

## Non-goals

This adapter does not establish:

```text
DGAF efficacy
PDMAL superiority
real-world benefit
causal attribution beyond the frozen experiment
```

Those remain empirical questions.

## Approval gates

The adapter cannot be promoted to experimental use until:

```text
v0.7 panel approval
        ↓
repository interface mismatch resolved
        ↓
adapter implementation
        ↓
2-seed contract validation
        ↓
current-head CI verification
        ↓
runtime characterization
        ↓
protocol freeze
        ↓
explicit pilot authorization
```

Until those gates close, `PDMAL_MODE=pilot` remains fail-closed.
