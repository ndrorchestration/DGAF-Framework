# DGAF Research Program — Explanation and Evidence Boundaries

**Audience:** researchers, technical evaluators, independent reviewers, and collaborators.

**Status:** explanatory documentation, not an experimental protocol, scientific result, authorization event, or change to canonical state. For exact control status use [CURRENT_STATE.md](CURRENT_STATE.md), frozen protocols and linked GitHub controllers.

## 1. What question does the research ask?

DGAF explores whether a governed agent system can make **action authority**, **evidence admissibility**, **execution receipts**, and **permission to make stronger claims** separately inspectable and enforceable. The key comparative question is not whether DGAF can produce a familiar allow/deny decision. It is whether its explicit evidence-and-authorization lifecycle yields additional **measurable**, reproducible assurance over a well-designed conventional system with comparably strong rules.

A hypothesis is not a finding. Demonstrating bounded control behavior is not sufficient to claim unique policy-engine superiority, reduced incident rates, production security, or general efficacy.

### Why the comparator parity finding matters

The stronger policy-as-code comparison matched the bounded DGAF decision model on **13/13 fixed fixtures** and **112,200 systematically enumerated bounded input states** with zero allow/deny differences in that specified space.

These were **enumerated combinations of declared bounded inputs**, not 112,200 real-world agents, independent trials, or empirical participants. Policy equivalence here is a valuable *negative result for a simplistic novelty claim*: no difference in allow/deny output was demonstrated in that space.

An independent reviewer has **not** yet reproduced the frozen handoff ([#1067](https://github.com/ndrorchestration/DGAF-Framework/issues/1067)). Further experiments would need preregistered claim-level, provenance, lifecycle, recovery, safety and operational metrics, an appropriately strong comparator, and independent adjudication to support a stronger assurance claim. See [#1061](https://github.com/ndrorchestration/DGAF-Framework/issues/1061).

## 2. Keep the units and evidence classes separate

A research *seed*, an observation row, an agent, a replay, a PASS check, a reviewer, and a canonical scientific-N unit are **not fungible**.

| Quantity or label | What it means | What it does **not** establish |
| --- | --- | --- |
| 50 paired Track A seeds | Inferential units in the specified prospective paired experiment | 50 promoted canonical High-Assurance units |
| 2,250 observations | The 50 × 5 topologies × 9 failure-count raw design cells in the bounded Track A panel | 2,250 independent empirical replications |
| Accepted dataset lock | Identity/custody binding for a defined dataset | Unblinding, analysis, claim, or release authorization |
| Locally executed primary analysis | Execution under an accepted locked method in a defined operator context | An independently reproduced result or generalized efficacy |
| Same-system interpretation | Bounded interpretation under project-controlled evidence | Independent scientific evaluation |
| Outside-operator usability test | Potential observation of uncoached usability for one path | General usability or scientific validation |
| Canonical High-Assurance empirical N = 0 | Current count under its own admission contract | A denial that any engineering or experimental work occurred |

[Scientific-state admission contract](governance/SCIENTIFIC_STATE_ADMISSION_CONTRACT.md) and controller [#1259](https://github.com/ndrorchestration/DGAF-Framework/issues/1259) prohibit arithmetic or implicit promotion between these categories. An explicit, separately admitted scientific-state transition record is required for a qualifying state change. None is established by this document.

## 3. Epoch 001: an informative failure of custody

Track A Epoch 001 successfully completed a preregistered blinded collection and retained **2,250 blinded observations** from **50 paired seed units**. Its dataset lock was established.

The preregistered primary comparison required a protected mapping that connected blinded observations to their underlying topology assignments. The retained mapping ciphertext existed, but the corresponding private key was not durably recoverable under the solo-custody arrangement.

**Consequence:** the protected mapping was **cryptographically unrecoverable**. The preregistered primary analysis was **unanalyzable and not run**. Generating another key, inferring assignments after inspection, or treating blinded values as if they were unblinded would not be equivalent to the frozen protocol. Such reconstruction was prohibited.

**What the experiment *did* establish:** the blinded collection took place and the custody design had a decisive failure mode. It did **not** establish a primary outcome, treatment efficacy, or independent validation.

**Engineering lesson:** successful data collection does not establish analyzability. Recovery testing and durable, inspectable custody must be acceptance prerequisites *before* a subsequent blinded collection, not retroactive repairs.

## 4. Epoch 002: successor execution with a bounded result

A distinct successor protocol under [issue #523](https://github.com/ndrorchestration/DGAF-Framework/issues/523) used fresh seeds, blinding, and recoverable solo custody. The governing sequence separated:

1. protocol identity, precollection recovery testing, and immutable freeze;
2. custody and explicit authorization to collect;
3. prospective blinded collection and dataset lock;
4. separately authorized bounded mapping release/unblinding;
5. materialization of analysis-ready inputs and immutable receipt;
6. authorization to run the **locked** primary analysis;
7. local analysis execution and content-addressed result admission;
8. bounded same-system interpretation and creation-only post-interpretation disposition.

Epoch 002's recorded collection contains **50 paired seed units / 2,250 observations**, and its lifecycle reached **CLOSED_FOR_EXACT_PREREGISTERED_SCOPE** through [PR #881](https://github.com/ndrorchestration/DGAF-Framework/pull/881). Locked-result evidence is associated with [PR #851](https://github.com/ndrorchestration/DGAF-Framework/pull/851); bounded interpretation/adjudication with [PR #872](https://github.com/ndrorchestration/DGAF-Framework/pull/872).

The allowed interpretation is **same-system/nonindependent**, only for the exact preregistered scope. Neither 50 seeds nor 2,250 rows increment the canonical High-Assurance empirical N. The closed lifecycle does not authorize a rerun or a new experiment.

## 5. Other research lanes and why they do not pool automatically

The research program separates workloads and identities so that one narrow result cannot be used as a universal conclusion:

- **B1:** semantic routing and safety — standalone non-empirical lane.
- **B2:** persistent context and closure — standalone non-empirical lane.
- **B3:** weighted-graph convergence monitoring — standalone non-empirical lane.
- **C:** integrated DGAF composition — non-empirical proposal; empirical execution is not authorized.
- **Solo historical experiments:** exact-treatment and apparatus evidence with their own limitations. A negative result for a synthetic or source-mismatched treatment is not a result for canonical DGAF.

Any proposal to combine evidence must first specify an authorized protocol, identical measurement targets, independence criteria, custody, and exact treatment identities. No pooled efficacy estimate is asserted here.

## 6. Independent validation is a separate event

**AOSS Stage A:** An independent-review handoff exists ([PR #928](https://github.com/ndrorchestration/DGAF-Framework/pull/928)), with a later accepted evaluated-implementation identity addendum ([PR #1354](https://github.com/ndrorchestration/DGAF-Framework/pull/1354)). These provide review materials, **not a performed review**. Issue [#929](https://github.com/ndrorchestration/DGAF-Framework/issues/929) controls eligible reviewer engagement, conflicts disclosure, independently retained evidence, and separate adjudication. Review is **not executed**, and collection-execution readiness is **not established**.

**Governance comparator:** The frozen reproducibility package has its own independent reviewer gate [#1067](https://github.com/ndrorchestration/DGAF-Framework/issues/1067), which is also open. This is not interchangeable with the AOSS independent-review gate.

**Outside operator:** A technically capable uninvolved human following only the public instructions could establish bounded usability evidence under [#1210](https://github.com/ndrorchestration/DGAF-Framework/issues/1210). It would not, by itself, increment canonical scientific N or establish general validation.

## 7. What DGAF-on-DGAF can and cannot show

A system testing its own governance controls can create useful **engineering evidence**: it can run negative cases, expose counterexamples, confirm deterministic behavior, and preserve reproducible receipts. The recorded self-application work under [#1022](https://github.com/ndrorchestration/DGAF-Framework/issues/1022) and [PR #1049](https://github.com/ndrorchestration/DGAF-Framework/pull/1049) is still same-system evidence.

Repeated model judgments, local CI runs, or self-generated review packets cannot be reclassified as **independent validation** merely because their results agree. A genuinely qualifying outside reviewer and separately governed acceptance remain required.

## 8. How to assess a research claim responsibly

For each claim, ask: What exact treatment and source SHA were tested? What was the experimental unit? Was the method frozen before execution? Was the required data recoverably retained? Who performed and verified the action, and are they independent? Does the receipt assert execution, verified postconditions, analysis, or only intent? Was the precise claim separately admitted by the controlling scientific-state contract?

When an answer is absent or cannot be verified, hold the stronger claim. For implemented-versus-replayed demonstrations, consult the [prototype maturity map](PROTOTYPE_MATURITY_MAP.md). For original evidence chronology, consult the [historical index](HISTORICAL_RECORDS_INDEX.md).

**Current ceiling:** `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`.

---

## Appendix: retained detailed Track A research and custody record

The material below preserves the more granular research-status and tool/PR chronology moved out of the earlier public README for progressive disclosure. These entries are **scoped historical descriptions**, not authority to execute a new transition; consult [CURRENT_STATE.md](CURRENT_STATE.md) and live controllers for updates.

## Current research program

DGAF separates prospective evaluation by workload instead of treating one experiment as proof of the entire framework.

| Track | Plain-English purpose | Current boundary |
| --- | --- | --- |
| **A — Epoch 001** | Numeric topology robustness | Prospective blinded collection complete and dataset locked; protected mapping is cryptographically unrecoverable; primary analysis unanalyzable/not run; retained as historical blinded evidence plus custody-design failure evidence |
| **A — Epoch 002 successor** | Replacement prospective topology robustness | Collection COMPLETE at 50 paired seed units / 2,250 observations; dataset lock ESTABLISHED; bounded unblinding AUTHORIZED; materialization and immutable receipt ESTABLISHED; locked-primary-analysis authorization ACCEPTED; primary analysis EXECUTED locally under the frozen contract; content-addressed locked-result receipt ESTABLISHED via #851; interpretation/adjudication EXECUTED / ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT |
| **B1** | Semantic routing and safety | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B2** | Persistent context and closure | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B3** | Persistent weighted-graph convergence monitoring | Standalone non-empirical lane complete; no empirical efficacy claim |
| **C** | Integrated DGAF composition | Non-empirical composition proposal merged; empirical execution NOT AUTHORIZED |

Epoch 001's prospective panel was fixed at **50 seeds × 5 topologies × 9 failure counts = 2,250 observations**. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**.

That collection remains valid evidence that the blinded panel was executed and retained. It cannot produce its preregistered primary result because the retained encrypted topology mapping cannot be recovered: the matching private key was not durably recoverable in the solo operating model. Regenerating a different key cannot decrypt the retained ciphertext, and guessing or reconstructing the hidden assignment is prohibited.

## Successor Track A custody and gate design

Issue #523 controls the replacement path. Epoch 002 uses a distinct protocol identity, fresh seeds and blinding, and recoverable solo custody without presenting same-system custody as independent.

Repository custody, precollection preflight, immutable freeze, final closure, bounded non-independent verification classification, separate collection authorization, retained-evidence admission/QC, dataset lock, and bounded unblinding have advanced through separate governed events. The authorized operator-executed Codespace collection is complete at **50 paired seed units / 2,250 blinded observations**.

The Epoch 002 lifecycle is **closed for its exact preregistered scope** via PR #881. No rerun, historical pooling, claim promotion, or new empirical epoch is authorized by that closure. The accepted apparatus now includes:

- a PASS content-addressed dataset-lock receipt;
- a separate PASS unblinding decision bounded to `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`;
- the accepted local materialization chain through PRs #713/#715/#794/#797/#806/#809/#813;
- real non-secret materialization evidence admitted through PR #824;
- an immutable creation-only materialization receipt accepted through PR #826;
- fail-closed local locked-analysis runner tooling accepted through PR #831;
- the separate primary-analysis authorization event accepted through PR #828 with exact scope `LOCKED_PRIMARY_ANALYSIS_ONLY`;
- non-executing content-addressed result-admission tooling accepted through PR #835;
- lifecycle-aware result-admission tests accepted through PR #848;
- the creation-only locked-analysis result receipt accepted through PR #851 as `c0690e599d25304f1d920d5235adff04ba76094a`.

Current boundary:

- `TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED`;
- `UNBLINDING = AUTHORIZED / BOUNDED TO CONTROLLED MAPPING RELEASE OR DECRYPTION`;
- `TRACK_A_EPOCH_002_MATERIALIZATION = ESTABLISHED`;
- `TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT = ESTABLISHED`;
- `PRIMARY_ANALYSIS_AUTHORIZATION = ACCEPTED / LOCKED_PRIMARY_ANALYSIS_ONLY`;
- `PRIMARY_ANALYSIS = EXECUTED_LOCKED / RETAINED`;
- `LOCKED_ANALYSIS_RESULT = ESTABLISHED`;
- `INTERPRETATION_ADJUDICATION = EXECUTED / ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT`;
- `SCIENTIFIC_N_INCREMENT = 0`;
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`;
- `INDEPENDENT_VALIDATION = NOT_ESTABLISHED`;
- `HIGH_ASSURANCE = PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`.

The remaining ordered sequence is:

`closed Epoch 002 lifecycle → separate future proposal/preregistration/authorization if new empirical work is pursued`

No private key, passphrase, blinding secret, protected plaintext mapping, decrypted protected data, or other recoverable secret material belongs in GitHub, Notion, chat, CI inputs, workflow logs, or committed files.
