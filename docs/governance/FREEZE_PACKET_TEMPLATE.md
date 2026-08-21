# DGAF/PDMAL Freeze Packet Template

**State:** TEMPLATE / NOT A FREEZE

This template is a controlled assembly point for candidate-scoped evidence. Presence of this file never authorizes a freeze or pilot.

## Candidate identity

```text
candidate_sha: <immutable Git SHA>
protocol_sha256: <sha256>
runner_sha256: <sha256>
schema_sha256: <sha256>
configuration_sha256: <sha256>
vercel_project: <project>
vercel_deployment_id: <deployment>
deployment_source_sha: <sha>
environment_fingerprint: <fingerprint>
```

## Predicate evidence

| Predicate | Required evidence | Status | Evidence reference |
|---|---|---|---|
| P1 | exact candidate identity and integrity | OPEN | |
| P2 | candidate-bound runtime execution | OPEN | |
| P3 | candidate artifacts + schema/sidecar validation | OPEN | |
| P4 | operational blinding/security evidence | OPEN | |
| P5 | complete provenance/reproducibility chain | OPEN | |
| P6 | durable archive/retrieval/hash round trip | OPEN | |
| P7 | primary contrast and scientific target adjudicated | OPEN | |
| P8 | locked analysis specification | OPEN | |
| P9 | independent verification | NOT_EXECUTED | |

## Scientific lock

```text
primary_endpoint: <FFCR or explicitly approved endpoint>
primary_contrast: <pending adjudication>
estimand: <pending adjudication>
direction: <pending adjudication>
secondary_endpoints: <locked list>
bootstrap_method: <locked>
bootstrap_replicates: <locked>
confidence_level: <locked>
multiplicity: <locked>
exclusion_rules: <locked>
stopping_rules: <locked>
unblinding_procedure: <locked>
```

## Custody

```text
archive_location: <external durable location>
archive_event_id: <event>
archive_timestamp_utc: <timestamp>
retrieval_event_id: <event>
retrieved_sha256: <sha256>
round_trip_result: PASS | FAIL
```

## Verification

```text
independent_verifier: <authorized verifier>
verification_event_id: <event>
verification_timestamp_utc: <timestamp>
verification_result: PASS | FAIL
```

## Authorization boundary

```text
new_freeze_created: false
pilot_authorized: false
empirical_n: 0
```

These values may only change through the separately authorized governance transition. This template must never be edited to make evidence appear complete.
