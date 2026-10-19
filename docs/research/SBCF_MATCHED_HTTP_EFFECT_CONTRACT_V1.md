# SBCF matched HTTP effect contract v1 — prospective candidate

Status: CANDIDATE / NOT FROZEN / NO COMPARATIVE RESULT.

This document defines a prospective successor to
`matched_http_effect_contract_v0.json`. Version 0 remains unchanged as the
historical candidate under which pinned OpenShell v0.1.4 was observed to keep
enforcing its last published allow rule after the gateway service was stopped.

Version 1 does **not** reinterpret that v0 observation as a success or failure.
Instead, it separates two questions that v0 had coupled:

1. normative HTTP effect cases under an available control plane; and
2. system-specific failure posture when the control plane is unavailable.

## Normative cases

The following remain normative and retain their v0 expected decision/effect:

- exact allow → ALLOW / COMMITTED;
- adjacent host → DENY / NOT_OBSERVED;
- adjacent method → DENY / NOT_OBSERVED;
- revoked authority → DENY / NOT_OBSERVED.

The candidate still requires a frozen negative observation bound before any
`NOT_OBSERVED` result can be structurally ready.

## Control-plane failure posture

`control_plane_unavailable` is changed prospectively to
`STRATIFIED_FAILURE_POSTURE`.

It has no universal `expected_decision` and no universal `expected_effect`.
Instead, each system must freeze one declared posture before a v1 trial:

- `FAIL_CLOSED_DENY`;
- `LAST_KNOWN_GOOD`;
- `FAIL_OPEN_ALLOW`.

The v1 fixture deliberately leaves all three system postures `UNRESOLVED`.
The previously observed OpenShell v0 behavior is **not** silently copied into a
frozen v1 declaration. A future v1 mapping must bind its own exact runtime
identity and evidence.

The failure-posture case is excluded from efficacy scoring unless a normative
target is separately preregistered in a future protocol. v1 itself forbids a
normative target. This prevents the benchmark from choosing a winner after
observing that systems implement different failure strategies.

## Receiver custody

v1 also makes receiver custody an explicit freeze gate. Structural readiness
requires:

- an independently assigned receiver operator;
- raw receipt retention;
- a frozen custody status.

The current fixture leaves custody `UNRESOLVED`.

## Readiness meaning

A future v1 structural READY result would mean only that:

- the contract is frozen;
- the negative observation bound is frozen;
- receiver custody is frozen;
- per-system runtime mappings are frozen;
- the failure-posture schema is frozen;
- each system has a frozen posture declaration.

It would **not** establish fairness, efficacy, parity, superiority, independent
validation, or scientific validity by itself.

## Versioning rule

v0 must remain available and unchanged as the record of the earlier candidate
and its OpenShell semantic mismatch. v1 is a new prospective protocol surface.
Historical v0 observations must not be rescored as though they were collected
under v1.

No trial, freeze, merge, release, scientific-N increment, or authority expansion
is authorized by creating this candidate.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
