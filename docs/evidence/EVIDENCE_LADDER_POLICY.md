---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL evidence control
last_verified: 2026-08-18
---

# Evidence Ladder Policy

This policy defines the distinction between implementation, CI verification, operational characterization, operational verification, experimental validation, and empirical support.

## Evidence levels

| Level | Meaning | Minimum evidence |
|---|---|---|
| IMPLEMENTED | Code or configuration exists in the repository | Source artifact and reviewable provenance |
| CI-VERIFIED | Automated contract checks pass under a known environment and exact SHA | Passing workflow run tied to executed SHA |
| OPERATIONALLY CHARACTERIZED | Runtime/resource behavior has been measured | Dedicated characterization artifact with integrity record |
| OPERATIONALLY VERIFIED | A required human/procedural control has been exercised successfully | Retained operational test record |
| EXPERIMENTALLY VALIDATED | A controlled experiment has been executed and analyzed under the frozen protocol | Frozen protocol, authorized execution, raw data, analysis, provenance |
| EMPIRICALLY SUPPORTED | Results are replicated or independently corroborated beyond the originating execution | Independent replication or equivalent external evidence |

## Promotion rules

1. A lower evidence level cannot be silently promoted to a higher level.
2. A historical CI result applies only to the exact executed SHA and environment recorded by that run.
3. Documentation alone cannot close a technical or operational gate.
4. A workflow's presence is not execution evidence.
5. An artifact's existence is not validation evidence unless the artifact records the procedure that generated it and the relevant integrity/provenance identifiers.
6. Every promotion requires an explicit evidence record identifying the claim, evidence unit, executed source, and remaining limitations.
7. Negative or failed evidence remains part of the historical record and is not deleted merely because a later correction succeeds.

## Authority boundaries

- **GitHub:** implementation, source history, CI runs, workflow artifacts, exact tested SHA.
- **Notion:** governance state, decisions, panel adjudication, cross-project control-plane summary.
- **Freeze packet:** consolidated release evidence for protocol-freeze review.

No source may override another source's authority boundary.

## Required evidence fields

Where practical, retained evidence should identify:

```text
claim/control
status/evidence class
executed commit SHA
workflow/run ID
artifact ID and digest where applicable
environment identifier
creation timestamp
limitations or unresolved dependencies
```

## Application to PDMAL

Examples:

- `ConsensusTask` source exists → **IMPLEMENTED**.
- Run #74 passes the contract suite for `08500a7` → **CI-VERIFIED**.
- Runtime characterization artifact demonstrates observed seed runtimes below 300 s → **OPERATIONALLY CHARACTERIZED**.
- Blinding dry-run succeeds with protected mapping and logged custody → **OPERATIONALLY VERIFIED**.
- A properly authorized 50-seed pilot is executed, frozen, unblinded, and analyzed → **EXPERIMENTALLY VALIDATED**.

**Permanent rule:** no empirical execution occurs before protocol freeze and explicit authorization.
