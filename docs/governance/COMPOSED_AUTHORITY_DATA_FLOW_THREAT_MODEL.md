# Composed Authority and Data-Flow Threat Model

> **Status:** PROSPECTIVE GOVERNANCE RESEARCH / NON-AUTHORIZING  
> **Scientific-state effect:** NONE

## Purpose

Individual actions can be authorized while their composition is not.

The protected invariant is:

```text
authorized(A) && authorized(B) != authorized(A -> B)
```

DGAF must therefore evaluate consequential data and authority flows across agent, tool, and trust boundaries rather than treating each capability call as independent.

## Primary threat — cross-agent authority laundering

Example:

```text
Agent A: may READ confidential data
Agent B: may WRITE to external destination

A reads -> passes data to B -> B writes externally
```

Neither agent individually holds both authorities, yet the composed workflow produces the forbidden effect.

## Threat classes

### CA-01 — Read/write authority laundering

Sensitive read output reaches an external-write capability through another agent or tool.

### CA-02 — Delegation widening by composition

Several narrow delegated scopes combine into an effect broader than any delegator intended.

### CA-03 — Provenance stripping

A transformation removes or obscures source classification, allowing protected data to cross a boundary as apparently unclassified content.

### CA-04 — Memory-mediated laundering

Sensitive output is written to shared memory/context and later consumed by an agent with broader egress authority.

### CA-05 — Tool-mediated laundering

A permitted tool transforms data in a way that bypasses destination or classification policy.

### CA-06 — Aggregation escalation

Multiple individually non-sensitive observations combine into a sensitive inference or protected aggregate.

### CA-07 — Unknown-classification escape

Missing classification/provenance is treated as unrestricted rather than unresolved.

## Decision inputs

For protected flows, evaluate where available:

- input data classification;
- provenance roots;
- producing identity/workload;
- transformation lineage;
- receiving identity/workload;
- destination class;
- delegation chain;
- action/effect class;
- applicable purpose constraint;
- retention/egress policy;
- uncertainty or UNKNOWN fields.

Required-but-UNKNOWN fields fail closed.

## Prospective flow record

```json
{
  "flow_id": "...",
  "source_artifacts": ["..."],
  "source_classification": "CONFIDENTIAL|RESTRICTED|PUBLIC|UNKNOWN",
  "provenance_roots": ["..."],
  "producer": "...",
  "transformations": ["..."],
  "consumer": "...",
  "destination": "...",
  "delegation_chain": ["..."],
  "decision": "ALLOW|DENY|REVIEW_REQUIRED|UNDETERMINED",
  "reason_codes": ["..."]
}
```

This schema is illustrative and creates no runtime authority.

## Required adversarial fixtures

1. confidential read -> direct external write;
2. confidential read -> second agent -> external write;
3. confidential read -> shared memory -> later external write;
4. provenance removed before write;
5. UNKNOWN classification -> external write;
6. two permitted partial datasets -> prohibited sensitive aggregate;
7. delegated tool chain whose combined effect exceeds the original scope.

## Success criteria

A future implementation should demonstrate that:

- direct and indirect protected flows are detected;
- provenance survives permitted transformations;
- no agent can widen authority merely by delegation;
- UNKNOWN required classification cannot become PUBLIC by omission;
- blocks identify the exact policy reason and next admissible action;
- legitimate low-risk flows are not unreasonably blocked.

## Non-effects

This threat model does not establish taint tracking, DLP, runtime enforcement, provider integration, standards compliance, or DGAF efficacy. Those require separate implementation and retained verification evidence.
