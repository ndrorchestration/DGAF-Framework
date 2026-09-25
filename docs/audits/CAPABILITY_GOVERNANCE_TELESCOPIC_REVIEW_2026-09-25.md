# Capability Governance Telescopic Review — 2026-09-25

> **Status:** INITIAL PROJECT-LOCAL STRUCTURAL REVIEW / NON-CERTIFYING  
> **Scope:** Draft Capability Governance Protocol and Design Track  
> **Method:** Canonical GATE-TEL 4-altitude × 8-dimension review  
> **Scientific-state effect:** NONE

## Summary

The draft is directionally coherent with DGAF's existing governance formalism and local MCP boundary. The strongest areas are authority separation, non-widening delegation, commit-time revalidation, and recovery semantics.

The highest-value unresolved areas are machine-checkable authorization semantics, canonicalization rules, data-flow composition, policy-conflict semantics, runtime identity, and concrete conformance evidence.

No conclusion here establishes production security, completeness, independent certification, or efficacy.

## 1. Intent Alignment

**Macro:** PASS-WITH-GAPS — system intent is clear: provider-neutral governance of authority and side effects.  
**Mid:** PASS-WITH-GAPS — PDP, PEP, broker, adapters, verifier, and evidence plane have distinct intended roles.  
**Tactical:** OPEN — schemas exist for capability manifests only; authorization/workflow/receipt schemas remain unwritten.  
**Quantum:** OPEN — failure intent for unknown execution, stale state, replay, and partial execution is specified but not yet tested.

Priority: convert the remaining core objects into machine-readable contracts before adding providers.
## 2. Provenance Integrity

**Macro:** PASS-WITH-GAPS — protocol explicitly inherits the Agent Governance Transition Specification and Telescopic Lens.  
**Mid:** OPEN — expert-panel findings and standards mappings are not yet bound to a durable design-decision record.  
**Tactical:** PASS-WITH-GAPS — draft local MCP manifests identify their source document but are unsigned.  
**Quantum:** OPEN — no canonical digest test vectors exist yet.

Priority:
- add canonicalization specification;
- generate deterministic digest fixtures;
- record source/version lineage for protocol revisions.

## 3. Boundary Clarity

**Macro:** PASS — provider, capability, adapter/transport, risk, policy, and evidence are separated.  
**Mid:** PASS-WITH-GAPS — PDP/PEP/broker boundaries are explicit, but deployment boundary is intentionally not selected.  
**Tactical:** PASS-WITH-GAPS — the existing four MCP operations remain bounded and non-authorizing.  
**Quantum:** OPEN — exact handling of malformed manifests, unknown fields, stale state, and degraded dependencies requires conformance tests.

Priority: preserve deferred product/deployment choices until the core protocol is validated.
## 4. Coherence

**Macro:** PASS-WITH-GAPS — the protocol is compatible with G1-G16 from the agent-governance transition formalism.  
**Mid:** PASS-WITH-GAPS — workflow authorization and data-flow governance close composition gaps conceptually.  
**Tactical:** OPEN — role-capability registry and runtime capability manifests use related but not identical meanings of "capability."  
**Quantum:** OPEN — conflict semantics between role authority, runtime authorization, workflow policy, and provider constraints are not executable yet.

Priority: define an explicit mapping:
```text
functional role capability != runtime invocation capability
```
and specify where the two may reference each other without authority inheritance.

## 5. Coverage

**Macro:** PASS-WITH-GAPS — major security and distributed-systems failure classes are represented.  
**Mid:** OPEN — economic authority, temporal authority, federated governance, and offline operation remain profile/research items.  
**Tactical:** OPEN — only capability-manifest schema exists.  
**Quantum:** OPEN — adversarial corpus has not yet been implemented.

Priority: threat-model and conformance harness before new live connectors.
## 6. Calibration

**Macro:** PASS — the protocol repeatedly states non-transfer and non-certification boundaries.  
**Mid:** PASS-WITH-GAPS — optional profiles are separated from core, reducing overclaiming.  
**Tactical:** OPEN — risk-vector values are descriptive and not yet empirically calibrated to approval thresholds.  
**Quantum:** OPEN — no measured false-allow/false-deny, latency, or operator-burden data exists.

Priority: do not convert the risk vector into a universal numeric score until empirical use cases justify one.

## 7. Sovereignty

**Macro:** PASS-WITH-GAPS — governance authority remains distinct from provider transport and model output.  
**Mid:** PASS-WITH-GAPS — credential broker and separation-of-duty design preserve boundary control conceptually.  
**Tactical:** OPEN — workload identity, proof-of-possession, and signing trust roots are not implemented.  
**Quantum:** OPEN — tenant, delegation, and runtime identity substitution attacks need executable tests.

Priority: treat identity and trust-root selection as explicit profiles, not hidden implementation assumptions.
## 8. Evolvability

**Macro:** PASS — provider-neutral capability identity supports adapter replacement.  
**Mid:** PASS-WITH-GAPS — staged design track defers proxying, federation, and hosted operation.  
**Tactical:** OPEN — schema compatibility and version-negotiation rules are still minimal.  
**Quantum:** OPEN — migration behavior for renamed/deprecated/revoked capabilities is not specified.

Priority:
- specify lifecycle transitions;
- define compatibility rules;
- add deprecation/revocation test fixtures;
- require evidence that an adapter change does not widen authority.

## Cross-altitude blockers

The current design SHOULD NOT advance to a general MCP/API proxy until:
1. authorization, delegation, workflow, receipt, and reconciliation schemas exist;
2. canonicalization/digest test vectors pass;
3. core G1-G16 invariants are linked to conformance tests;
4. at least one adversarial confused-deputy/composition test is executable;
5. bounded local MCP behavior remains unchanged under the PEP prototype;
6. a second adapter type demonstrates transport independence.

## Disposition

**Current state:** structurally promising, intentionally incomplete.  
**Next justified work:** machine-readable core contracts + threat model + conformance harness.  
**Not justified yet:** broad connector expansion, hosted multi-tenant service, general proxy, certification claims.
