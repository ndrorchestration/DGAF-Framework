# AWCP & Symphony Historical Cross-Reference

## Current authority boundary

> **Historical local source:** `AI Governance Research Plan Outline` (Google Drive)  
> **Current status:** HISTORICAL / PROVISIONAL CROSS-REFERENCE · NOT RUNTIME AUTHORITY  
> **Reconciled:** September 9, 2026

This file preserves an earlier local cross-reference between external research and the
NDR/DGAF ecosystem. It does **not** establish AWCP, Symphony, MediHive, or their
reported results as Hensel-authored frameworks, DGAF subsystems, peer control planes,
deployed protocols, or DGAF evidence.

Current ownership remains:

- **DGAF:** governance, authorization, evidence maturity, and fail-closed state transition;
- **`agent-control-plane`:** framework-neutral execution contract;
- **PDMAL:** scoped empirical topology research;
- **current evaluator/harness surfaces:** evidence generation and evaluation.

Historical NDR names such as NDR-Stasis, PhiLattice, Yggdrasil, Amethyst, DemiJoule,
Apogee, and Geodesic Echo remain lineage unless an owning current source explicitly
binds them to a live mechanism.

## Source attribution

The local research outline cited external papers. Their mechanisms and results must stay
attributed to those sources rather than being rewritten as DGAF equivalents or project
accomplishments.

- **AWCP — Agent Workspace Collaboration Protocol:** external work by Xiaohang Nie,
  Zihan Guo, Youliang Chen, Yuanjian Zhou, and Weinan Zhang; arXiv `2602.20493`.
- **Symphony — A Decentralized Multi-Agent Framework for Scalable Collective
  Intelligence:** external work by Ji Wang, Kashing Chen, Xinyuan Song, Ke Zhang,
  Lynn Ai, Eric Yang, and Bill Shi; arXiv `2508.20019`.
- **MediHive — A Decentralized Agent Collective for Medical Reasoning:** external work
  by Xiaoyang Wang and Christopher C. Yang; arXiv `2603.27150`.

Similarity to an NDR/DGAF design idea is a **cross-reference**, not evidence of common
authorship, implementation inheritance, priority, equivalence, or result transfer.

## Agent Workspace Collaboration Protocol (AWCP)

The AWCP paper introduces temporary workspace delegation between a Delegator and a
remote Executor, using a lightweight control plane, pluggable transports, direct shared
workspace operation, and an open-source reference implementation. Those are properties
of the external AWCP work, not DGAF implementation facts.

The local outline's stronger statement that AWCP is the **first** protocol to formalize
workspace delegation is not adopted here as an NDR/DGAF priority claim. Any novelty or
priority statement should be attributed to and evaluated within the external paper's own
literature boundary.

| External AWCP concept | NDR/DGAF disposition |
|---|---|
| Delegator → Executor workspace projection | Useful comparison for execution-contract / runtime-adapter design |
| Files as interface | Useful comparison for workspace grounding and provenance |
| Lifecycle/session state machines | External protocol design; no silent import into DGAF state authority |
| Workspace/control separation | Useful comparison for `agent-control-plane` adapter boundaries |

The earlier cross-reference's **69.6% reduction in coordination failures** is **not an
AWCP or DGAF result established by this file**. The local outline itself described that
number through a different protocol (SEMAP) and then analogized lifecycle guidance to
AWCP. Similarity does not permit metric transfer.

## Symphony

The Symphony paper introduces a decentralized capability ledger, Beacon-selection for
task allocation, and weighted result voting. These remain properties of the external
Symphony framework unless separately implemented and tested inside the NDR ecosystem.

The earlier cross-reference incorrectly presented metaphorical NDR mappings as if they
were current equivalents. They are now explicitly comparison-only:

| External Symphony concept | NDR/DGAF disposition |
|---|---|
| Beacon-selection | Candidate comparison for capability/routing mechanisms; no `Index 11` property inferred |
| Capability-match score | Candidate comparison for routing/evaluation; no Geodesic Echo equivalence established |
| Weighted result voting | Candidate comparison for synthesis; no CP-WBFT equivalence established here |
| Decentralized ledger | Candidate comparison for shared-state/provenance; no current Yggdrasil authority inferred |

Symphony's reported benchmark gains remain **external Symphony evidence**. They are not
DGAF, PhiLattice, PDMAL, or NDR performance results and must not be used as such without
a new owning experiment.

## MediHive

The previous table contained a concrete dataset/metric error: it labeled **84.3% as
PubMedQA accuracy**. The cited MediHive paper reports **84.3% on MedQA** and **78.4% on
PubMedQA**. Both remain external MediHive results, not DGAF evidence.

No MediHive result validates a DemiJoule, Metacollaboration, Apogee, triadic-governance,
or other NDR mechanism merely because the local outline drew an analogy.

## Retained design value

The useful engineering questions survive without unsupported ownership or efficacy
transfer:

- how to delegate a workspace with explicit scope and state;
- how to preserve file/version provenance during delegated execution;
- how to separate workspace control from transport/runtime details;
- how to define lifecycle transitions and recovery semantics;
- how to match capability to task requirements;
- how to aggregate independent outputs without conflating consensus with truth;
- how to compare centralized and decentralized routing under explicit baselines.

These should be implemented, if warranted, through current owners rather than by
reviving AWCP or Symphony as NDR peer control planes by name.

## Evidence and scientific boundary

`awcp_ownership = EXTERNAL_RESEARCH`  
`symphony_ownership = EXTERNAL_RESEARCH`  
`medihive_ownership = EXTERNAL_RESEARCH`  
`awcp_runtime_authority_in_dgaf = NOT_ESTABLISHED`  
`symphony_runtime_authority_in_dgaf = NOT_ESTABLISHED`  
`awcp_priority_claim_first_workspace_delegation = NOT_ADOPTED_AS_NDR_CLAIM`  
`historical_69_6_percent_gain = NOT_ESTABLISHED_FOR_AWCP_OR_DGAF_BY_THIS_SOURCE`  
`symphony_benchmark_results = EXTERNAL_SOURCE_ONLY`  
`medihive_medqa_84_3_percent = EXTERNAL_SOURCE_ONLY`  
`medihive_pubmedqa_78_4_percent = EXTERNAL_SOURCE_ONLY`  
`scientific_state_effect = NONE`  
`empirical_authorization_effect = NONE`  
`canonical_dgaf_efficacy = NOT_ESTABLISHED`

## Primary source references

- Nie, X., Guo, Z., Chen, Y., Zhou, Y., & Zhang, W. (2026). *AWCP: A Workspace
  Delegation Protocol for Deep-Engagement Collaboration across Remote Agents*.
  arXiv:2602.20493.
- Wang, J., Chen, K., Song, X., Zhang, K., Ai, L., Yang, E., & Shi, B. (2025).
  *Symphony: A Decentralized Multi-Agent Framework for Scalable Collective
  Intelligence*. arXiv:2508.20019.
- Wang, X., & Yang, C. C. (2026). *MediHive: A Decentralized Agent Collective for
  Medical Reasoning*. arXiv:2603.27150.
