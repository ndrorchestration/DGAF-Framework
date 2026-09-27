# DGAF Smoke Contract v1

## Purpose

DGAF Smoke Contract v1 is a fast, deterministic, non-empirical verification layer for the DGAF control plane.

It answers one bounded question:

> Can this exact DGAF revision execute one minimal governed control path, preserve provenance, reject a known authority violation, and block ambiguous promotion without changing scientific or authorization state?

A passing smoke run establishes only that this narrow contract was satisfied for the evaluated revision. It does not establish scientific efficacy, independent validation, high assurance, production readiness, optimal routing, general safety, or correctness outside this contract.

## Outcome model

The engineering promotion signal is binary:

- `PASS`: every required smoke gate passed.
- `FAIL`: at least one required smoke gate was executed and failed.

`NOT_OBSERVED` is an evidence classification, not a passing state. It applies when the smoke runner did not meaningfully execute, for example because checkout, dependency installation, or runner infrastructure failed first. Promotion remains blocked in that case.

## Required gates

| Gate | Question | Pass condition |
|---|---|---|
| `SMOKE_BOOT` | Can the control-plane primitives initialize? | Control plane, governance envelope, budget, and task instantiate successfully. |
| `SMOKE_ROUTE` | Can a minimal task enter the governed lifecycle? | `RECEIVED -> PREFLIGHT -> ADMITTED` occurs through public controller methods. |
| `SMOKE_EXECUTE` | Can the minimal bounded control path progress? | The admitted task reaches `EXPANDING -> EVALUATING` without external side effects. |
| `SMOKE_PROVENANCE` | Is the path attributable? | Snapshot and event stream retain task identity, trace identity, and expected state events. |
| `SMOKE_DENY` | Does authority widening fail closed? | A child requesting authority outside the parent envelope is rejected and is not registered. |
| `SMOKE_STATE` | Is ambiguous promotion blocked? | Merge readiness without sealed successful TGL evidence is rejected and state does not advance. |

## Canonical fixtures

- `GST-ALLOW-001`: minimal allowed control transaction.
- `GST-DENY-001`: child authority escalation attempt that must be denied.
- `GST-AMBIGUOUS-001`: promotion attempt without required sealed evidence that must remain blocked.

These fixtures are synthetic engineering checks only.

## Evidence contract

A successful runner invocation writes a JSON result containing:

- contract/schema identifier;
- evaluated revision identifier when supplied by CI;
- overall outcome;
- per-gate outcome and diagnostic detail;
- canonical fixture identifiers;
- explicit epistemic boundary fields.

The following boundary values are mandatory for v1 smoke evidence:

```text
SCIENTIFIC_N_INCREMENT=0
AUTHORIZATION_EFFECT=NONE
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

Smoke evidence MUST NOT be interpreted as empirical evidence.

## Fail-closed promotion rule

```text
PASS         -> eligible for deeper verification
FAIL         -> blocked
NOT_OBSERVED -> blocked
```

No smoke outcome grants execution authority that was not already present before the run.

## Scope boundary

v1 intentionally stops at the deterministic control-plane layer. It does not claim to be a full worker/agent end-to-end test, provider test, deployment-health probe, model-quality evaluation, regression suite, adversarial campaign, performance test, or scientific experiment.

Those remain deeper verification layers.

## CI placement

The dedicated workflow should run before expensive or broad verification whenever the smoke contract, its runner, or the core control-plane files change. Its artifact is diagnostic engineering evidence; absence of a valid artifact means the smoke result was not observed.
