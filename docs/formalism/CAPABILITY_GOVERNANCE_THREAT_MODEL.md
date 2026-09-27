# DGAF Capability Governance Threat Model

> **Status:** PROSPECTIVE / NON-AUTHORIZING  
> **Scope:** Capability Governance Protocol core profile

## Assets

Primary assets include:

- authority and delegation state;
- policy and manifest integrity;
- human approvals;
- credentials and provider tokens;
- protected data and model context;
- execution receipts and postcondition evidence;
- audit/provenance records;
- tenant and runtime identity.

## Trust boundaries

The initial core model treats these as untrusted unless explicitly verified:

- model output and agent-generated plans;
- retrieved documents and tool output;
- MCP/OpenAPI/plugin descriptions;
- provider responses without independent readback;
- external adapters and dependencies;
- user-supplied capability metadata.

The PEP, authorization verifier, canonicalizer, revocation check, and protected policy/manifest loading form the candidate minimal trusted base.

## Abuse-case corpus

### T1 — Delegation widening

A child agent requests capability, scope, duration, budget, recipient, or exception rights absent from its parent delegation.

Required result: DENY. G11 applies.

### T2 — Confused deputy

A low-authority requester induces a privileged executor to invoke a capability using the executor's broader rights.

Required result: effective authority is intersected with requester and delegation-chain authority; unauthorized excess is denied.

### T3 — Approval laundering

A human approves one outbound message, but the agent substitutes recipient, body, attachment, resource, or policy context before execution.

Required result: action-digest mismatch invalidates approval. G12 applies.

### T4 — Replay / duplicate side effect

A network retry causes a previously executed send, charge, deploy, or mutation to be attempted again.

Required result: idempotency and consumed authorization prevent unintended duplicate effect.

### T5 — Unknown execution outcome

Provider timeout occurs after the provider may have completed the action.

Required result: enter EXECUTION_OUTCOME_UNKNOWN; reconcile before retry.

### T6 — TOCTOU target drift

A file, branch, account, or resource changes after approval but before commit.

Required result: commit-time state guard fails and protected execution is blocked. G13 applies.

### T7 — Read-to-write exfiltration

An agent reads confidential data and then attempts an external Slack/email/upload action.

Required result: workflow/data-flow policy evaluates the composition; prohibited egress is blocked.

### T8 — Prompt/tool injection

Retrieved content or a tool description tells the agent to bypass policy, reveal credentials, or invoke another tool.

Required result: metadata/output is treated as data; only PDP/PEP authority controls execution.

### T9 — Malicious adapter substitution

A capability manifest remains unchanged while the implementation binary/container is replaced.

Required result: admitted runtime/adapter identity mismatch blocks higher-risk invocation when the profile requires binding.

### T10 — Revocation race

Authorization is revoked after planning but immediately before execution.

Required result: commit-time revocation check blocks execution. G9/G13 apply.

### T11 — Policy self-broadening

An agent invokes a policy-management capability to expand its own rights.

Required result: separation-of-duty rule blocks ordinary self-broadening.

### T12 — Audit poisoning

Provider output attempts to inject misleading audit fields or secrets into evidence.

Required result: audit event schema separates trusted metadata from opaque provider evidence; secret material is excluded.

### T13 — Partial workflow failure

A multi-step workflow completes some irreversible or compensable actions and then fails.

Required result: PARTIALLY_EXECUTED is preserved; explicit compensation/containment/escalation follows. G15 applies.

### T14 — Provider false success

Transport returns success but the intended state is absent.

Required result: provider receipt is not conflated with verified postcondition.

### T15 — Capability discovery probing

A low-authority agent enumerates sensitive installed capabilities or schemas.

Required result: DISCOVER and INSPECT_SCHEMA permissions are evaluated separately from INVOKE.

### T16 — Cross-tenant substitution

A valid capability request swaps target tenant/security domain while retaining another tenant's authorization.

Required result: tenant/security-domain binding mismatch blocks execution.

## Failure-mode classes

Security failures:

- unauthorized allow;
- authority widening;
- identity substitution;
- secret exposure;
- data exfiltration;
- audit tampering.

Reliability failures:

- duplicate side effect;
- ambiguous outcome;
- partial execution;
- stale approval;
- provider/runtime mismatch;
- reconciliation failure.

Governance failures:

- policy conflict ambiguity;
- approval fatigue or overbroad consent;
- unverifiable external effects;
- hidden fail-open degraded mode;
- role/runtime capability conflation.

## Required evidence before broader deployment

The core profile should not advance to a general provider proxy until representative tests exist for T1–T10 and at least one end-to-end composition/exfiltration case.
