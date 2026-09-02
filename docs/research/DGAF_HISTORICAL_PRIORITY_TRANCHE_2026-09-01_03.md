# DGAF Historical-Priority Audit — Tranche 2026-09-01-03

**Status:** Expanded cross-domain boundary sweep; no absolute novelty or priority conclusion
**Date:** 2026-09-01
**Scope:** Systems predating 2026-04-29 that combine at least two of: organizational/team formation, evolving agent/workflow state, cryptographic evidence, artifact/candidate identity, promotion, verification, or authorization.

## 1. Narrow target

The audit target remains:

`formation state → formation authority → governed formation transition → evidence → exact candidate identity/freeze → candidate-bound verification → authorization`

This tranche deliberately admits boundary-adjacent systems that were previously easy to classify separately, because the question is whether any pre-DGAF architecture crossed the same domain boundary rather than whether any individual primitive existed.

## 2. Pre-DGAF boundary comparators

### A. Authenticated Workflows — February 11, 2026

The arXiv record for *Authenticated Workflows: A Systems Approach to Protecting Agentic AI* describes cryptographically authenticated enterprise agent workflows, organizational-policy enforcement, cryptographic proof at workflow boundaries, dynamically changing agent constraints, hierarchical composition, and workflow-dependency attestations. It explicitly frames agents as evolving and treats integrity and authorization as properties enforced at workflow boundaries.

Primary record:

- https://arxiv.org/abs/2602.10465

**Adjudication:** Strong pre-DGAF comparator for **agent/workflow evolution + organizational policy + cryptographic integrity/authentication**. It substantially weakens any broad claim that cryptographic governance of evolving agent workflows was independently unprecedented. The inspected public abstract does not establish that organizational formation itself is the governed state, nor an explicit formation-to-frozen-candidate transition followed by candidate-bound independent verification and authorization. **Boundary-adjacent prior; not an exact Q predecessor.**

### B. OrgForge — March 11, 2026

The OrgForge whitepaper describes a machine-readable organizational constitution (OrgSpec), deterministic evaluation of actor intents against organizational policy, signed authorization artifacts, and execution systems that verify those artifacts before acting. It applies the authorization mechanism to human, software, and AI-agent actors and explicitly addresses replay safety and deterministic authorization.

Primary record:

- https://orgforge.io/paper/

**Adjudication:** Strong pre-DGAF comparator for **organizational policy → signed authorization artifact → verified execution**. This closes another potential primitive/composition claim around organization-scoped authorization artifacts. The inspected material does not establish dynamic organizational formation as the governed state or a formation transition producing a frozen experimental/software candidate whose evidence is subsequently independently verified. **Boundary-adjacent prior; not an exact Q predecessor.**

### C. Trusted-execution team formation / attested team membership — April 2, 2026

The public patent record for *Systems and Methods for Secret-Based Operation Execution in a Trusted Execution Environment* includes an explicit team-formation embodiment: a team specification identifies a coordinator and members; member identity evidence includes unique identifiers and device attestations; member attributes are determined; and a team proposal is generated.

Primary record:

- https://patents.justia.com/patent/20260095308

**Adjudication:** Important pre-DGAF boundary comparator for **team formation + authority/coordinator + identity/attestation evidence**. It demonstrates that formation state and cryptographic identity evidence can be joined in one architecture before April 29. The inspected claim material does not establish the DGAF lifecycle from formation governance through a software/research candidate freeze, candidate-scoped evidence verification, and authorization. **Near/boundary-adjacent prior; not an exact Q predecessor.**

## 3. Later convergence comparators (not prior art against DGAF chronology)

### D. LOGOS — July 12, 2026

LOGOS describes persistent agent teams that evolve their own artifacts, versioned agent packs containing agents/tools/knowledge/tests/permissions/policies, auditable event traces, fail-closed verification, untrusted release candidates, held-out evidence, human-controlled policy, and explicit authorization before promotion. Its core invariant is an isolated candidate-to-promotion gate.

Primary record:

- https://arxiv.org/abs/2607.10878

**Adjudication:** This is an unusually close **later convergence comparator**. It substantially overlaps the candidate/evidence/authorization side of the DGAF hypothesis and explicitly treats evolving agent organization and release governance as a connected lifecycle. Because the public record is July 2026, it cannot defeat an April/May DGAF historical-priority chronology. It does, however, strongly constrain any claim that the integration is conceptually unique in the broader 2026 ecosystem.

### E. Agentic Artifact Creation survey — August 28, 2026

The survey covers 230 agentic artifact-construction systems and emphasizes stateful construction, runtime verification, revalidation of affected state after change, explicit commitments/responsibility, and accountable artifact evolution.

Primary record:

- https://arxiv.org/abs/2608.28122

**Adjudication:** Later convergence/background evidence. It is useful for showing that artifact state, construction, verification, and revalidation are a broad systems problem, but it does not itself provide an exact historical predecessor.

### F. Artifact-centered Claim-aware Observability — August 18, 2026

This work proposes first-class claim/evidence bindings, verification records, artifact lineage, run records, archives, and steering commands for autonomous scientific agents.

Primary record:

- https://arxiv.org/abs/2608.18312

**Adjudication:** Later convergence comparator for scientific artifact/evidence governance. It is not prior art against the April/May chronology and does not establish formation-to-candidate authorization.

## 4. What the sweep changes

The remaining hypothesis is now more constrained than before.

Pre-April-29 material independently demonstrates several cross-domain joins:

1. **evolving agent workflows + organizational policy + cryptographic integrity** (Authenticated Workflows);
2. **organizational policy + signed authorization artifacts + verified execution** (OrgForge);
3. **team formation + coordinator authority + identity attestation** (trusted-execution team formation).

Therefore the surviving DGAF distinction cannot be stated as merely “formation + authority + cryptographic evidence + authorization.” Those combinations already have substantial pre-DGAF precedent in adjacent forms.

The remaining question is specifically whether any predecessor made the **organizational formation state itself** the continuous governed object across a transition into an **exact software/research candidate**, then required **candidate-bound independent verification** before authorization/promotion.

## 5. Revised Q adjudication

| Predicate | Current finding |
|---|---|
| GF — formation is governed state | **External prior** |
| AF — authority attached to formation | **External prior** |
| VF — veto/conflict/escalation constrains formation transitions | **External individually; exact composition unresolved** |
| IF — formation transition explicitly idempotent | **External individually; exact composition unresolved** |
| PC — evidence bound to exact candidate | **External prior** |
| XC — verification/authorization resolves against exact candidate | **External prior in principle; many adjacent implementations** |
| **L — continuous formation-state → candidate-state → evidence → verification → authorization lifecycle** | **OPEN** |

## 6. Important boundary correction

The candidate/evidence distinction should now be stated as follows:

**Not distinctive by itself:**

- cryptographic evidence;
- signed authorization artifacts;
- exact artifact identity;
- policy-gated promotion;
- independent verification;
- separation of proposal from activation;
- workflow integrity;
- team identity attestation.

**Potentially distinctive application still under review:**

> treating a dynamically governed agent formation as the upstream state whose controlled transition establishes the exact experimental/software candidate, and carrying that identity continuously through evidence production, independent verification, and authorization.

That is materially narrower than the earlier “formation + provenance + authorization” formulation.

## 7. Chronology remains segmented

- **April 29:** earliest currently located named-DGAF repository evidence.
- **May 1:** explicit formation authority conflict, veto, timeout escalation/blocking, and idempotent formation-wave replay.
- **August 21:** explicit development/candidate separation and exact candidate identity.

No later candidate/evidence architecture should be used to backdate the April/May DGAF composition. Likewise, May 1 formation semantics should not be treated as proven to exist on April 29.

## 8. Current conclusion

The historical-priority audit remains **OPEN**, but the surviving claim is now a highly specific architectural hypothesis.

The bounded search has not located a pre-April-29 source that establishes the full continuous lifecycle under the current equivalence standard. At the same time, several pre-DGAF systems independently combine substantial subsets of that lifecycle, so the residual hypothesis should be characterized as a **potentially distinctive cross-domain integration**, not a novel mechanism or broad architectural invention.

This tranche therefore strengthens the audit rather than producing a binary novelty result.

## 9. Next highest-value search

Search only for pre-2026-04-29 systems with all of the following or near-equivalent semantics:

1. persistent/dynamic organizational or agent-formation state;
2. explicit authority over formation changes;
3. a controlled formation transition that creates/adopts a versioned artifact, model, workflow, experiment configuration, or research candidate;
4. exact identity/digest of that resulting candidate;
5. evidence generated independently of the formation authoring path;
6. verification against the exact candidate;
7. promotion/authorization conditional on that verification.

Systems lacking the formation-to-candidate transition should remain background prior rather than being escalated to exact-predecessor status.
