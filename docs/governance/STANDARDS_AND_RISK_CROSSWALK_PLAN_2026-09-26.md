# Standards and Risk Crosswalk Plan — 2026-09-26

> **Status:** SOURCE-MAPPING PLAN / NON-CERTIFYING  
> **Effect:** No compliance, conformity, certification, authorization, or legal conclusion is established.

## Scope

DGAF will maintain bounded mappings between its implemented controls and external governance/risk frameworks. A crosswalk records relationship, not compliance.

Initial targets:

- NIST AI Risk Management Framework;
- ISO/IEC 42001;
- OWASP Top 10 for Agentic Applications;
- EU AI Act Article 14, only where the requirement is applicable to the system/use context.

## Mapping vocabulary

Each entry MUST use one of:

- `DIRECT_SUPPORT` — the DGAF control directly implements or evidences the mapped requirement within stated scope;
- `PARTIAL_SUPPORT` — covers part but not all of the requirement;
- `RELATED` — conceptually relevant but not implementation evidence for the requirement;
- `NOT_COVERED` — no current DGAF control is established;
- `NOT_APPLICABLE` — applicability analysis establishes exclusion for the stated context.

Unknown applicability remains `NOT_COVERED` or an explicit unresolved state; it must not be silently marked `NOT_APPLICABLE`.

## Required fields

Each mapping record should bind:

```text
external_framework
external_control_or_requirement
source_version_or_date
source_reference
dgaf_control_id
dgaf_artifact
mapping_status
scope
evidence_class
limitations
last_verified
reviewer
```

## Initial DGAF mapping families

### Governance / identity / delegation

Candidate DGAF sources:

- agent authority matrix and invariant;
- Action Admission authority contract;
- role/capability registry;
- external dependency admission;
- revocation/replay contracts.

### Risk mapping / consequence

Candidate sources:

- action classes and effect classifications;
- correlated-verification threat model;
- state-space / blocked-transition machinery;
- failure-mode and assurance registries.

### Measurement / assurance

Candidate sources:

- epistemic evidence standard;
- verification artifacts;
- audit catalog;
- operator self-test;
- retained execution receipts.

### Management / intervention

Candidate sources:

- fail-closed admission;
- blocked-state projection;
- revocation;
- no-retry/manual recovery semantics;
- operator-facing next-admissible-action surfaces.

### Agentic-security risks

OWASP mappings must be evidence-specific, particularly for:

- goal hijacking;
- tool misuse;
- privilege abuse;
- supply-chain vulnerabilities;
- code execution;
- memory/context poisoning;
- insecure inter-agent communication;
- cascading failures;
- human-agent trust exploitation;
- rogue agents.

A named control without adversarial evidence is not automatically `DIRECT_SUPPORT`.

## Legal/compliance boundary

EU AI Act mappings are technical traceability aids only. They are not legal advice and MUST NOT be presented as a legal determination of applicability or compliance.

ISO/IEC 42001 mappings are implementation-support relationships only unless an authorized conformity/certification process independently establishes more.

NIST mappings are framework alignment, not certification.

OWASP mappings are risk/control relationships, not assurance of absence of the mapped vulnerability.

## Acceptance criteria

A crosswalk is publishable when:

1. every external row has an exact authoritative source reference;
2. every DGAF mapping points to a concrete repository artifact;
3. mapping status and evidence class are explicit;
4. gaps remain visible;
5. the document passes claim/truth-layer review;
6. no crosswalk entry promotes DGAF's scientific or validation state.

## Current status

This plan establishes the schema and boundary only. The complete source-verified crosswalk remains to be populated.
