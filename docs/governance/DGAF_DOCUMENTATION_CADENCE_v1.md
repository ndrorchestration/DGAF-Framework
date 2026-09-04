# DGAF Documentation Cadence v1.0

**Status:** Audit/control proposal; non-authoritative until ratified
**Date:** 2026-09-04

## Lifecycle

Documentation follows: **capture → classify → bind → review → publish → verify → supersede/archive**.

## Event classes

| Event | Required documentation action |
|---|---|
| New concept | Assign identity, taxonomy class, owner, status, and temporal origin |
| New pattern | Register pattern ID, layer, trigger, authority, implementation/evidence boundary |
| Agent change | Update identity, formation, authority, variant/lineage and dependent rubrics |
| Formula/threshold change | Create impact set; require mathematical and authority review |
| Implementation change | Bind source commit; refresh applicable tests/evidence |
| Evidence run | Record run ID, candidate identity, configuration, timestamp, artifacts, epistemic status |
| Governance decision | Record decision authority, effective time, scope, rationale, supersession |
| Retirement/supersession | Preserve prior artifact and explicitly bind replacement |

## Recurring sweeps

- **Session-level:** terminology, changed identifiers, new evidence, unresolved exceptions.
- **Commit-level:** impact-set detection for high-impact documentation changes.
- **Release-level:** registry/version/digest reconciliation and historical boundary check.
- **Pre-freeze:** complete transversal sweep across identity, taxonomy, pattern, agentic, layer, implementation, evidence, and governance domains.
- **Post-freeze:** only explicitly authorized changes may alter the frozen boundary; documentation of changes must preserve pre-freeze state.

## Temporal rule

A later edit does not retroactively change what an earlier artifact meant. Historical records retain their original source identity and time scope; current summaries must point to them without silently rewriting their status.

## Documentation freshness

Freshness is not equivalent to authority. A recently edited document can remain contradictory, derivative, historical, or unverified.

## Completion rule

A documentation family is not complete merely because every directory contains a file. Completeness requires coverage of required dimensions plus resolved or explicitly recorded gaps.
