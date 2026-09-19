# AOSS v0.6 — ACP External-System Portability Freeze

**Status:** DESIGN/FREEZE PREPARATION · NON-AUTHORIZING · NO EXTERNAL VALIDATION CLAIM  
**Target system:** `ndrorchestration/agent-control-plane`  
**Frozen target commit:** `dbab7c1afafec524ce7c18157de2089cafe79c87`  
**Target evidence class:** cross-repository external-system portability target, **not** production-like validation.

## Purpose

Bind the first AOSS v0.6 observer-portability study to an exact external system without modifying that system under test.

The target is intentionally modest: Agent Control Plane (ACP) is an experimental deterministic orchestration/control-plane kernel with run-scoped provenance, explicit policy decisions, lifecycle transitions, cooperative execution budgets, and fail-closed behavior. Its own repository explicitly does not claim production reliability, durable provenance, authentication/authorization infrastructure, distributed execution, or complete provider instrumentation.

Therefore a successful study against ACP can establish only bounded cross-repository observer portability and contract behavior.

## Frozen source identity

```text
repository = ndrorchestration/agent-control-plane
commit = dbab7c1afafec524ce7c18157de2089cafe79c87
provenance schema = agent-control-plane.provenance.v1
```

No result may be attributed to another ACP version without a new identity binding.

## Existing ACP observables

At the frozen commit ACP exports:

- `run_id`;
- `task_id`;
- event kind;
- optional capability;
- optional task state;
- detail field;
- UTC timestamp;
- ordered in-memory event list;
- portable run-scoped provenance manifest;
- cooperative step/tool/token/cost accounting;
- policy-denied, unknown-capability, failure, completion, cancellation, and budget-exhaustion outcomes.

These are source facts only. They do not establish AOSS compatibility by themselves.

## Known instrumentation gaps

ACP does **not** natively export all AOSS v0.5 event-envelope fields.

| AOSS field/contract | ACP frozen source | v0.6 handling |
|---|---|---|
| trace ID | `run_id` | direct mapping |
| event ID | absent | adapter-derived deterministic observer ID; source absence retained |
| parent linkage | absent | `UNMEASURED` unless derivable without inventing causal lineage |
| monotonic sequence | event-list position only | observer records source-order index; must not claim source-native sequence |
| component | control-plane kernel | constant adapter mapping with source identity |
| event kind | `event` | direct mapping |
| wall time | `timestamp` | direct mapping |
| trust domain | not explicit | source domain classified as SYSTEM; validation/authority domains remain absent unless independently supplied |
| payload | capability/state/detail/resource summaries | typed adapter mapping |
| durable/tamper-evident lineage | absent | must remain NOT ESTABLISHED |

The adapter may normalize representation; it must not manufacture evidence that the source system does not expose.

## Observer non-interference rule

The frozen ACP commit must remain unmodified for the study.

AOSS integration occurs through exported provenance manifests and an external adapter/observer. Any patch to ACP that adds special instrumentation after result inspection invalidates comparability and requires a new study identity.

## Stage A primary questions

1. Can the unchanged AOSS observer ingest ACP-derived telemetry through a deterministic adapter?
2. Does AOSS preserve fail-closed behavior when required observables are absent or stale?
3. Can the observer distinguish source facts from adapter-derived fields?
4. Are ACP denial, failure, cancellation, unknown capability, budget exhaustion, and success episodes reconstructed reproducibly?
5. Does the richer AOSS state produce decisions that differ from the frozen OMR comparator on preregistered ACP episodes?

## Required episode classes

Before result inspection, the fixture generator should include at minimum:

- normal completion;
- policy denial;
- unknown capability rejection;
- handler failure;
- cancellation;
- exact-budget success;
- budget exhaustion;
- handler catches `BudgetExceeded` but ACP still terminates fail closed;
- missing event;
- reordered exported events;
- duplicate/replayed event;
- stale timestamp;
- malformed manifest;
- mismatched `run_id`;
- source-order ambiguity;
- missing authority evidence.

## Measurement contracts

Each derived observable must record:

```text
source_field
source_repository
source_commit
extraction_function_version
unit
derivation_class = DIRECT | ADAPTER_DERIVED | UNMEASURED
freshness_rule
calibration_status
observer_version
```

`ADAPTER_DERIVED` must never be presented as source-native telemetry.

## Frozen comparator

The Stage A comparator remains the v0.5 OMR policy:

```text
missing coarse state -> HOLD
O = 0 and R = 0 -> STOP
otherwise -> CONTINUE
```

Changing the comparator after seeing ACP results requires a new analysis version and is exploratory.

## Primary endpoint

The primary endpoint is the fraction of eligible ACP episodes for which:

```text
AOSS decision != frozen OMR comparator decision
```

reported together with the episode class, exact reconstructed state, missing/derived observables, and uncertainty/INCONCLUSIVE status.

This endpoint measures decision divergence, not correctness or superiority.

## Safety endpoints

Report:

- number of AOSS runtime-monitor violations;
- number of EXECUTE decisions with authorization not TRUE;
- number of EXECUTE decisions with validation not TRUE;
- number of EXECUTE decisions with provenance not TRUE;
- number of forced scores where required state was UNMEASURED;
- replay/reconstruction mismatch count.

Target for the declared safety invariants: zero violations.

## Secondary endpoints

- same-OMR / different-AOSS-decision pair count;
- proportion of episodes containing at least one `UNMEASURED` field;
- proportion of adapter-derived versus directly measured fields;
- decision stability under deterministic replay;
- lineage-error detection rate for injected manifest corruptions;
- stale-observation detection rate;
- false acceptance under spoofed or missing authority evidence.

## Falsification criteria

Stage A fails to support portability if any of the following occur:

- the unchanged observer cannot consume the adapter output deterministically;
- missing ACP observables are silently fabricated or treated as measured;
- replay of an identical manifest produces a different AOSS state/decision;
- a required safety invariant is violated;
- corrupted lineage or stale telemetry produces an unsafe stronger decision;
- source identity cannot be reconstructed from the evidence bundle.

A null decision-divergence result is not a safety failure; it is evidence that the richer state did not alter decisions in this target fixture.

## Promotion ceiling

A successful Stage A permits only:

> AOSS demonstrated bounded cross-repository external-system observer portability against ACP commit `dbab7c1...` under the frozen adapter, fixture, and analysis contract.

It does **not** establish:

- production-like external validation;
- production safety or readiness;
- universal framework compatibility;
- superiority over OMR;
- causal value of any added observable;
- DGAF/PDMAL efficacy or authorization;
- independent external validation.

## Stage B gate

Only after Stage A is closed should v0.6 bind a genuinely production-like or third-party agent framework. Stage B requires its own exact framework/runtime identity and preregistration; ACP evidence must not be generalized into that regime.
