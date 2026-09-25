# DGAF Capability Governance Protocol

> **Status:** PROSPECTIVE FORMAL SPECIFICATION / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Design principle:** Govern authority and side effects, not transports or vendor APIs.  
> **Depends on:** `AGENT_GOVERNANCE_TRANSITION_SPEC.md`, `../gates/TELESCOPIC_LENS.md`, `../../governance/role_capability_registry.v1.json`

## Purpose

This specification defines a provider-neutral capability-governance layer for AI agents, multi-agent formations, applications, plugins, connectors, MCP servers, APIs, SDKs, CLIs, and other tool providers.

DGAF MUST treat provider, capability, transport, effect/risk, policy, identity, and evidence as distinct dimensions. No transport or integration mechanism grants authority by itself.

Canonical abstraction:

```text
Provider -> Capability -> Adapter/Transport -> Effect/Risk -> Policy
```

A capability may be implemented through MCP, REST, GraphQL, SDK, CLI, plugin, connector, or another admitted adapter without changing its governance identity, provided implementation trust requirements remain satisfied.

## Reference architecture

```text
Human / Application
  -> Agent Formation
  -> Workflow Authorization
  -> Governance Engine (PDP)
  -> Capability Gateway (PEP)
       -> Data-Flow Guard
       -> Credential Broker
       -> Provider Adapter
       -> Provider
  -> Postcondition Verifier
  -> Evidence / Audit Plane
```

The PDP decides. The PEP enforces. The credential broker holds or exchanges secrets. Provider adapters invoke external systems. The evidence plane records decision and execution evidence without becoming an execution authority.

## Trust boundary

The minimal trusted computing base SHOULD include:

- action canonicalization and digest generation;
- policy decision and obligation evaluation;
- authorization verification;
- commit-time revalidation;
- capability enforcement;
- credential brokering;
- execution receipt capture;
- postcondition state handling;
- revocation enforcement;
- integrity protection for policy, manifests, and audit records.

Agents, model outputs, retrieved content, tool descriptions, provider responses, plugin metadata, and external documentation MUST be treated as untrusted inputs unless separately verified.

## Capability identity and manifest

Every governed capability SHOULD have a signed, versioned manifest with a stable provider-neutral identifier.

Minimum fields SHOULD include:

- capability identifier and semantic version;
- provider and provider resource type;
- operation;
- adapter/transport implementation identity;
- risk/effect vector;
- preconditions;
- constraints;
- commit-time guards;
- postconditions;
- recovery semantics;
- verification class;
- audit obligations;
- lifecycle state;
- manifest signer and integrity digest.

Registration does not grant visibility. Visibility does not grant invocation. Invocation does not grant delegation.

Recommended permission verbs:
`DISCOVER`, `INSPECT_SCHEMA`, `REQUEST_AUTHORIZATION`, `INVOKE`, `DELEGATE`.

## Risk vector

Risk MUST NOT be represented by a single total ordering such as READ < WRITE.

A capability SHOULD classify at least:

```text
access          = read | write | delete | privilege_change
sensitivity     = public | internal | confidential | PII | regulated
reversibility   = reversible | compensable | irreversible
externality     = none | internal | external
blast_radius    = low | medium | high
financial       = none | low | high
privilege       = none | elevate | credential_change
```

Policies MAY add domain-specific dimensions. Unknown or missing required risk attributes MUST NOT silently weaken the decision.

## Identity model

Protected actions SHOULD distinguish:

- human principal;
- initiating principal;
- logical agent identity;
- agent instance;
- model identity/version;
- runtime/workload identity;
- executing principal/tool identity;
- workflow identity;
- delegation identity;
- tenant/security-domain identity;
- provider and target-resource identity.

Effective authority MUST NOT be inferred solely from executor privilege.

For delegated execution:

```text
effective_authority =
  requester_authority
  INTERSECT delegation_chain
  INTERSECT executor_authority
  INTERSECT current_policy
```

This is a confused-deputy control and extends the non-widening delegation invariant.

## Authorization object

An authorization SHOULD bind:

- subject and initiating principal;
- capability identifier and version;
- target/resource scope;
- material parameters or canonical action digest;
- delegation chain;
- policy identity/version;
- validity window;
- audience;
- tenant/security domain;
- budgets/quotas where applicable;
- data-classification and egress constraints;
- approval requirements and approval identity;
- proof-of-possession binding where supported.

Authorizations SHOULD be short-lived, revocable, audience-bound, and non-transferable by default.

Provider credentials SHOULD NOT be exposed directly to agents when a brokered model is available.

## Exact-action approval

Human or delegated approval for a protected action SHOULD bind to a canonical digest:

```text
H(capability, version, resource, parameters, actor,
  agent, delegation_chain, policy_version, state_guards, nonce)
```

Material substitution, target drift, policy drift, state-guard failure, expiry, revocation, or replay MUST invalidate the approval.

## Workflow and composition semantics

Action authorization is not automatically compositional.

```text
Authorized(A) AND Authorized(B) -/-> Authorized(A then B)
```

A governed workflow SHOULD have its own identity, dependency graph, accumulated data labels, aggregate cost/risk, destination boundaries, and recovery policy.

DGAF SHOULD evaluate composition risks including:

- sensitive-read followed by external-write exfiltration;
- privilege transfer through a higher-authority executor;
- aggregate blast radius across individually low-risk actions;
- cyclic delegation or approval laundering;
- partial completion leaving an unsafe intermediate state.

Workflow authorization MAY be required even when all component actions are individually authorized.

## Data-flow governance

DGAF SHOULD track material data classifications across read, transform, summarize, store, transmit, and publish operations.

A data-flow guard SHOULD support:

- source classification;
- taint/lineage propagation;
- egress destination policy;
- redaction/DLP obligations;
- retention limits;
- model-context contamination controls;
- cross-tenant/cross-domain restrictions.

## Execution semantics

Every side-effecting invocation SHOULD bind:

- workflow ID;
- invocation ID;
- action digest;
- idempotency key;
- attempt number;
- current authorization identity.

Execution state MUST distinguish at least:
`NEW`, `EXECUTING`, `EXECUTED`, `FAILED`, `EXECUTION_OUTCOME_UNKNOWN`, and `PARTIALLY_EXECUTED` where applicable.

A timeout or lost response MUST NOT automatically imply failure when the provider may have completed the action.

Unknown execution outcomes require reconciliation before unsafe retry.

## Commit-time revalidation

Volatile predicates MUST be revalidated immediately before the protected side effect when required by policy.

Examples include:

- authorization not expired/revoked/consumed;
- policy version still admitted;
- target identity unchanged;
- repository/file/version state unchanged;
- provider adapter identity still admitted;
- delegation chain still valid;
- budgets/rate limits still available;
- required verifier/provider health acceptable.

Required predicates that are FALSE, UNKNOWN, missing, stale, or identity-mismatched fail closed unless an explicitly authorized escalation path applies.

## Recovery and postconditions

Capabilities SHOULD declare recovery class:
`REVERSIBLE`, `COMPENSATABLE`, or `IRREVERSIBLE`.

Postcondition verification SHOULD classify capabilities as:

- `VERIFIABLE`;
- `BEST_EFFORT`;
- `UNVERIFIABLE`.

A transport-level success response is not sufficient evidence of the intended side effect when stronger provider evidence is available.

Postcondition failure MUST NOT erase historical execution.

Composed workflows MUST define one or more of:

- retry;
- rollback;
- compensation;
- containment;
- escalation;
- accepted partial state under separate authority.

## Policy conflict semantics

Concrete DGAF policy profiles MUST define deterministic conflict resolution. A default-deny profile SHOULD prefer explicit deny over allow and MUST define how obligations, exceptions, and break-glass rules interact.

Policy engines, policy authors, approvers, executors, and credential brokers SHOULD remain separate authorities where practical.

An agent MUST NOT broaden the policy governing itself through an ordinary capability invocation.

## Provider and supply-chain trust

Capability-manifest trust does not imply implementation trust.

Higher-risk profiles SHOULD bind:

- manifest digest;
- adapter/binary/container digest;
- dependency lock or attestation;
- runtime/workload identity;
- policy version;
- provider endpoint/audience identity.

Provider adapters MUST NOT be permitted to modify their own governing manifest or policy through the same trust path.

Tool metadata, MCP descriptions, OpenAPI text, plugin manifests, provider output, and retrieved content MUST be treated as data rather than instructions with authority.

## Availability and degraded mode

Fail-closed behavior MUST be explicit per dependency and capability.

Profiles SHOULD define outcomes for:

- PDP unavailable;
- PEP unavailable;
- credential broker unavailable;
- provider unreachable;
- audit sink unavailable;
- postcondition verifier unavailable;
- revocation service unavailable;
- network partition or rate limit.

No degraded-mode rule may silently widen authority.

## Audit and evidence

Audit integrity and audit confidentiality are separate requirements.

Audit records SHOULD bind:

- initiating and executing identities;
- workflow and invocation identities;
- capability and manifest versions;
- policy and authorization identities;
- action digest;
- provider/adapter/runtime identity;
- decision and obligations;
- execution outcome;
- provider receipt;
- postcondition state;
- recovery state;
- timestamps and relevant state guards.

Secrets MUST NOT enter the audit plane.

Sensitive values SHOULD use privacy-preserving representations appropriate to the verification need rather than reversible logging.

## Telescopic Lens conformance

This protocol MUST be reviewed using the canonical 4-altitude x 8-dimension Telescopic Lens.

The eight dimensions are:

1. Intent Alignment
2. Provenance Integrity
3. Boundary Clarity
4. Coherence
5. Coverage
6. Calibration
7. Sovereignty
8. Evolvability
Review MUST consider each dimension at Macro, Mid, Tactical, and Quantum altitudes. A passing GATE-TEL review establishes project-local structural consistency only; it does not establish production security, completeness, efficacy, or independent certification.

## Profiles and scope control

The core protocol SHOULD remain smaller than the full possible feature set.

Core profile:

- canonical capability identity;
- PDP/PEP separation;
- scoped authorization;
- non-widening delegation;
- exact-action binding;
- commit-time revalidation;
- fail-closed enforcement;
- execution receipts;
- postcondition state;
- audit/provenance linkage.

Optional profiles MAY cover:

- credential exchange and proof-of-possession;
- data-flow/DLP enforcement;
- multi-tenant/federated operation;
- plugin sandboxing;
- financial authority;
- offline/partitioned operation;
- formal-policy engines;
- advanced supply-chain attestation.

DGAF SHOULD NOT build a general-purpose provider proxy until the core protocol has conformance tests and at least two independently implemented adapter paths.

## Initial conformance requirements

A reference implementation MUST demonstrate at minimum:

1. unauthorized invocation is blocked at the PEP;
2. expired/revoked authorization is blocked;
3. changed action digest invalidates approval;
4. delegation cannot widen capability, resource, duration, budget, or approval scope;
5. stale target state fails commit-time revalidation;
6. replay does not duplicate a side effect;
7. unknown execution outcome enters reconciliation rather than blind retry;
8. sensitive-read plus prohibited external-write is blocked when the data-flow profile is enabled;
9. provider receipt and postcondition state are recorded separately;
10. audit records preserve identities and policy/version provenance without secrets.

## Standards posture

DGAF SHOULD reuse established standards where they fit, while keeping the protocol provider-neutral. Candidate mappings include OAuth authorization and token exchange mechanisms, proof-of-possession, workload identity, policy engines, API description formats, MCP transport, supply-chain attestations, and sandboxed execution.

Standards mapping MUST distinguish:

- normative dependency;
- optional interoperability profile;
- implementation example;
- emerging/non-final mechanism.

## Non-transfer statement

This specification does not authorize external side effects, alter current scientific state, establish production readiness, or convert conceptual DGAF agents into runtime agents.

It is a design contract for future governed execution and interoperability.
