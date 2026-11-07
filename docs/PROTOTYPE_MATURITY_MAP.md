# DGAF Prototype Maturity and Evidence Map

**Purpose:** Help a reader distinguish functioning implementation, bounded test evidence, local experimental results, replay, UI projection, proposed control, and independently verified deployment. This is a **documentation classification**, not a new authority state or certification.

**Evidence precedence:** [CURRENT_STATE.md](CURRENT_STATE.md) and the exact source/issue/PR evidence control any consequential interpretation. This map records a bounded documentation review of available source and open controllers as of **2026-11-06**; it does **not** claim whole-repository reverification. In particular, a proposed fix in an open PR is not an accepted mainline correction.

## Interpreting maturity without overstating it

| Level | Meaning | Reasonable claim | Claim not justified by the level alone |
| --- | --- | --- | --- |
| **Concept / proposal** | Specified model, diagram, contract, or unmerged draft | A proposed design exists | The design works in deployed software |
| **Source / reference implementation** | Real implementation code available for inspection | The code implements described paths | All paths are secure or production-ready |
| **Bounded same-system test** | Tests or demonstrations run under project/owner control | Covered behavior was observed in an exact scope | Independent verification or general efficacy |
| **Replay / simulated projection** | Retained fixture or model illustrates a flow | The modeled or historical relationship can be inspected | Live cross-system execution |
| **Locally executed experiment** | Real experiment or locked analysis performed in controlled scope | That exact event occurred under recorded custody | Independent replication, canonical efficacy, or High-Assurance N increment |
| **Independently accepted evidence** | Qualifying external evidence returned, verified, and adjudicated under the relevant contract | Only the exact externally accepted predicate | Automatic release, certification, or universal security |

No current public overview should silently reclassify a row into a stronger level.

## What a technical evaluator can actually inspect

| Surface | Observed / recorded maturity | What it means | Important limit / controller |
| --- | --- | --- | --- |
| **DGAF bounded public demo** | Executed same-system engineering demonstration with accepted receipt evidence | An ephemeral audit-counter action can be admitted with valid authority and denied with revoked authority | Not a production-wide AAR issuer or independent validation; [walkthrough](DEMO_WALKTHROUGH.md) |
| **DGAF → ACP trace in demo** | **Static, replay-only** evidence fixture | Explains DGAF admission versus ACP bounded execution contract, postcondition, and lineage | Not live ACP execution, mutation, distributed/global lineage authority, or a new permission |
| **Capability-governance reference lane** | Bounded accepted source/reference implementation, including PDP/PEP separation | Demonstrates architectural division of policy decision, policy enforcement, receipts, transports, and recovery | Does not prove universal correctness/security or all-integrations coverage; [technical reference](../README.technical.md) |
| **Governance Command Center** | Accepted **presentation-only** views | Decision Frontier, Governance Map, and State-Space Explorer display interpreted state and blockers | A display cannot grant authority, infer a continuous readiness score, or admit science |
| **Assurance catalog and workflow scanner** | Accepted, explicitly **partial** repository inventory | Maps selected recurring assurance families and highlights unmapped workflows | Catalog membership does not equal required branch protection, complete assurance coverage, or control efficacy |
| **Track A Epoch 001** | Prospective blinded collection executed and locked; **unanalyzable** primary result | Collected 50 paired seed units / 2,250 raw observations; custody failure documented | Protected mapping unrecoverable; primary analysis not run; see [research explainer](RESEARCH_PROGRAM_EXPLAINER.md) |
| **Track A Epoch 002** | Locally executed locked primary analysis, result receipt and bounded same-system interpretation; exact-scope lifecycle closed | Governed successor research execution occurred with recorded custody | Not independent replication, canonical efficacy, or N promotion |
| **AOSS Stage-A review packet** | Accepted review-preparation and identity-binding apparatus | A qualifying reviewer has the documented inputs needed to attempt the specified external review | External review **NOT EXECUTED**; [#929](https://github.com/ndrorchestration/DGAF-Framework/issues/929) |
| **DGAF-on-DGAF testing** | Same-system engineering execution and adjudication | Covered mutations, negative controls and replays can detect implementation issues | A self-assessment is not independent validation; [#1022](https://github.com/ndrorchestration/DGAF-Framework/issues/1022) |
| **Comparator benchmark** | Bounded tests / systematic input enumeration; independent reproduction packet prepared | Parity on 13 fixtures and 112,200 declared bounded input states | No unique allow/deny superiority; [#1067](https://github.com/ndrorchestration/DGAF-Framework/issues/1067) open |
| **Outside-operator usability trial** | Public test packet ready; trial not completed by eligible outside operator | A reproducible request for one uninvolved operator exists | Usability gate unsatisfied; [#1210](https://github.com/ndrorchestration/DGAF-Framework/issues/1210) |
| **DGAF v1 release** | **HOLD** | Release gates are specified and under review | Not authorized for v1 release; [#1421](https://github.com/ndrorchestration/DGAF-Framework/issues/1421) |

For the demo, the approved exact-scope behavior includes a receipt with `authority_effect=NONE` and `follow_on_authority=FRESH_ADJUDICATION_REQUIRED`. An execution receipt is not an authorization artifact for the next action.

## Known prototype limits and active corrective work

### Control-plane concurrency: #1548

[Issue #1548](https://github.com/ndrorchestration/DGAF-Framework/issues/1548) records a reproduced repeated-expansion accounting defect: reentry can increase concurrency accounting, while termination releases only one slot. This is **liveness/resource accounting evidence**, not a demonstrated unauthorized effect. [PR #1563](https://github.com/ndrorchestration/DGAF-Framework/pull/1563) contains a proposed remediation. Verification and merge status must be checked separately.

### Sealed-PASS admission semantics: #1561 / #1562

[PR #1561](https://github.com/ndrorchestration/DGAF-Framework/pull/1561) contains negative tests characterizing insufficient semantic admission checks for purportedly sealed `PASS` evidence; [PR #1562](https://github.com/ndrorchestration/DGAF-Framework/pull/1562) proposes tighter rejection. Neither the existence of a seal nor a successful isolated test can replace an exact check of what inputs, gates and verifier semantics that seal actually covers. Proposed fixes do not count as admitted protected-main safeguards.

### Legacy API route: #1551

[Issue #1551](https://github.com/ndrorchestration/DGAF-Framework/issues/1551) identifies a prototype Next.js route that may return unqualified approval-like `PASS` despite stubbed checks and label reversible base64-derived output as a `seal_hash`. The described token is **not a cryptographic signature or audit seal**. Deployed reachability and exploitation were **not verified**. [PR #1553](https://github.com/ndrorchestration/DGAF-Framework/pull/1553) proposes stricter non-authorizing handling.

Do **not** use this legacy route's output as independent authorization, scientific validation, a verified execution receipt, or production security evidence.

### Gate 0 release hold: #1421

[Controller #1421](https://github.com/ndrorchestration/DGAF-Framework/issues/1421) requires preregistered bounded release criteria, independent acceptance, exact-source evaluation, known-blocker disposition, and release-admission sign-off. Current recorded state is **HOLD**; none of the prototype demonstrations or internal testing above substitutes for that process.

## Interpret the word “PASS” by its owner and scope

“PASS” may refer to a unit test, a fixed fixture, an evidence syntax check, a bounded policy admission, a postcondition, or a locally performed experiment. To interpret one safely, record:

1. **What passed?** Exact predicate, action class, fixture, test and source identity.
2. **Who checked it?** Implementer, same-system CI, uncoached operator, or eligible independent verifier.
3. **What does it authorize?** Often **nothing** beyond recording the result.
4. **What was not checked?** Reachability, persistence, external integrations, threat-model cases, independence, or deployment state.
5. **What would advance it?** A separate admissible acceptance or authorization transition under the controlling contract.

## Where the real authority lives

- [Current state](CURRENT_STATE.md): current-facing scoped evidence and scientific boundaries; its whole-record `last_verified` date must not be updated from partial review alone.
- [Technical reference](../README.technical.md): component and implementation architecture.
- [Governance reference](../README.governance.md): authority contracts and conceptual risk/standards mapping.
- [Research explainer](RESEARCH_PROGRAM_EXPLAINER.md): experimental design, interpretation, custody, and scientific-N distinctions.
- [Historical records](HISTORICAL_RECORDS_INDEX.md): event-time provenance; not automatically current authority.

**Invariant:** `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`; `DGAF_V1_RELEASE=HOLD`.
