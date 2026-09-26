# DGAF SOTA Hardening Track — 2026-09-26

> **Status:** PROSPECTIVE ENGINEERING / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Canonical efficacy:** NOT ESTABLISHED  
> **Independent validation:** NOT ESTABLISHED

## Purpose

This track converts the current novelty/state-of-the-art audit into bounded engineering work. It does not assert that DGAF is state of the art. It defines the evidence required before such a claim could become defensible.

The governing rule is:

```text
architectural sophistication != demonstrated superiority
```

DGAF should add controls only when a named failure class, measurable assurance benefit, and operational cost are explicit.

## Existing foundation

Protected-main already contains relevant foundations:

- correlated-verification threat modeling;
- Action Admission authority contracts and fail-closed semantics;
- epistemic evidence and alignment standards;
- operator self-test and readiness paths;
- provenance, evidence custody, and non-promoting review paths.

This track therefore does not duplicate those systems. It targets the remaining gaps.

## Ordered workstreams

### SOTA-1 — Comparative governance benchmark

Compare:

- A — prompt-only governance;
- B — conventional RBAC/ACL governance;
- C — policy-as-code runtime governance;
- D — DGAF.

Required injected failures include:

- prompt injection / goal hijacking;
- confused deputy;
- privilege escalation;
- credential replay;
- compromised sub-agent;
- stale, fake, or substituted evidence;
- self-verification presented as independent verification;
- UI-state spoofing;
- premature claim promotion;
- cross-agent authority laundering.

Required metrics include:

- unsafe actions prevented;
- unsupported claims prevented;
- legitimate task completion;
- false-block rate;
- governance latency;
- operator interventions;
- policy/configuration complexity;
- recovery time.

No benchmark result establishes general DGAF efficacy without a separately governed interpretation and validation path.

### SOTA-2 — Untrusted-model security property

Adopt this prospective security target:

> A fully compromised or prompt-injected model must not be able to exceed authority explicitly granted by non-model governance state.

The model may propose; external policy and authority components decide.

Test at minimum:

1. confused deputy;
2. token/credential theft or replay;
3. prompt-injection privilege escalation;
4. compromised delegated sub-agent.

### SOTA-3 — Standards crosswalk

Maintain a source-bound mapping to:

- NIST AI RMF;
- ISO/IEC 42001;
- OWASP Top 10 for Agentic Applications;
- EU AI Act Article 14 where applicable.

Allowed mapping statuses:

```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
RELATED
NOT_COVERED
NOT_APPLICABLE
```

A mapping MUST NOT be described as certification, legal compliance, or conformity unless independently established under the applicable process.

### SOTA-4 — Provenance-aware data-flow governance

Treat composed flows as authority-bearing events.

A permitted sensitive read followed by a separately permitted external write may form a prohibited composition.

Required decision inputs should include, where applicable:

- source data classification;
- provenance root;
- producing agent/workload;
- receiving agent/workload;
- destination class;
- delegated authority;
- transformation history;
- applicable egress policy.

Unknown required classification or provenance fails closed for protected flows.

### SOTA-5 — Effective human oversight

For consequential approval, the operator surface should expose:

- intended action;
- reason / policy basis;
- material evidence;
- expected side effect;
- reversibility;
- intervention window;
- specific responsibility being accepted.

Human approval is not evidence of correctness by itself.

### SOTA-6 — Epistemic authority hardening

Preserve DGAF's existing rule:

> The strongest supported statement is the permitted statement.

Prospective claim decisions should distinguish at least:

```text
ASSERTED
DENIED
UNDETERMINED
```

A high-stakes assertion should be traceable to an entitlement record binding claim, evidence, provenance, verification class, independence class, scope, and staleness/expiry semantics.

## Complexity budget

Every new major control must identify:

1. failure mode addressed;
2. threat/adversary or benign failure case;
3. measurable benefit;
4. measurable cost;
5. simpler baseline;
6. falsification/removal condition.

A control that cannot identify these remains experimental and MUST NOT become mandatory merely because it appears safer.

## Acceptance frontier

This track advances engineering readiness only when:

- comparative benchmark tooling exists and can run deterministically;
- at least one simpler baseline and DGAF are evaluated under identical fixtures;
- false-block and latency measurements are retained;
- untrusted-model adversary fixtures execute;
- cross-agent authority-laundering fixtures execute;
- standards mappings contain exact source references and explicit gaps;
- no result silently promotes independent validation, efficacy, certification, or High-Assurance state.

## Non-effects

This document establishes no benchmark superiority, standards compliance, independent validation, production certification, scientific-N increment, canonical efficacy, or High-Assurance authorization.
