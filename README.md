# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, and permission to act as separate machine-relevant states** rather than assuming that one implies another.

In plain English: an agent may be able to do something and still be blocked from doing it; a system may pass engineering tests and still be blocked from claiming that it is empirically validated.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** PROSPECTIVE BLINDED COLLECTION COMPLETE · 50 paired inferential seed units · 2,250 blinded observations · DATASET LOCK ESTABLISHED  
> **Epoch 001 disposition:** protected mapping is **CRYPTOGRAPHICALLY UNRECOVERABLE** · primary analysis **UNANALYZABLE / NOT RUN**  
> **Successor Track A:** issue #523 open · operator-local custody-v2 recovery **PASS_CURRENT_V2 / SELF-ATTESTED / NONINDEPENDENT** · repository custody admission **NOT ESTABLISHED** · Epoch 002 dataset-lock tooling **ACCEPTED (#622)** / dataset lock **NOT ESTABLISHED** · replacement empirical collection **NOT AUTHORIZED**  
> **Canonical DGAF efficacy:** NOT ESTABLISHED

## What problem DGAF is trying to solve

Most agent frameworks focus on what an agent can do: reason, call tools, hand work to another agent, retain state, or complete a workflow.

DGAF focuses on an additional question:

> **Given the evidence and authority that exist right now, what is this system actually entitled to claim, authorize, and execute?**

DGAF explores this through:

- **Governed orchestration** — specialized agents operate under explicit roles, boundaries, and escalation rules.
- **Evidence-aware authorization** — technical capability does not automatically grant permission.
- **Provenance** — outputs, decisions, evidence, and state are tied to the identities that produced them.
- **Evaluation integrity** — implementation, testing, verification, independent verification, and empirical demonstration remain distinct.
- **Fail-closed controls** — missing or ambiguous prerequisites block promotion rather than silently becoming approval.
- **Experimental reproducibility** — prospective experiments bind protocols, code, analysis, artifacts, custody, and authorization to exact identities.

## The core model

A simplified DGAF control loop is:

```text
Evidence + provenance
        ↓
Epistemic / verification state
        ↓
Claim and action authority
        ↓
Governed agent formation
        ↓
Execution
        ↓
New evidence + trace
        └────────────→ updated governance state
```

The intended invariant is that **capability, evidence, verification, and authorization cannot silently substitute for one another**.

## Current research program

DGAF separates prospective evaluation by workload instead of treating one experiment as proof of the entire framework.

| Track | Plain-English purpose | Current boundary |
|---|---|---|
| **A — Epoch 001** | Numeric topology robustness | Prospective blinded collection complete and dataset locked; protected mapping is cryptographically unrecoverable; primary analysis unanalyzable/not run; retained as historical blinded evidence plus custody-design failure evidence |
| **A — successor** | Replacement prospective topology robustness | Issue #523 governs Epoch 002; operator-local custody-v2 recovery passed as self-attested/non-independent, but the exact public certificate + non-secret schema-v2 receipt are not yet admitted/revalidated in the repository; dataset-lock validation tooling is accepted via #622, but no dataset lock exists and empirical collection is not authorized |
| **B1** | Semantic routing and safety | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B2** | Persistent context and closure | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B3** | Persistent weighted-graph convergence monitoring | Standalone non-empirical lane complete; no empirical efficacy claim |
| **C** | Integrated DGAF composition | Non-empirical composition proposal merged; empirical execution NOT AUTHORIZED |

Epoch 001's prospective panel was fixed at **50 seeds × 5 topologies × 9 failure counts = 2,250 observations** and was collected under the governed blinded path. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**.

The collection remains valid evidence that the blinded panel was executed and retained. It cannot produce its preregistered primary result because the retained encrypted topology mapping cannot be recovered: the matching private key was not durably escrowed in the solo operating model. Regenerating a different key cannot decrypt the retained ciphertext, and guessing or reconstructing the hidden assignment is prohibited.

## Successor Track A custody and gate design

Issue #523 controls the replacement path. Epoch 002 uses a new protocol identity, fresh seeds and fresh blinding, and a recoverable solo-custody design without pretending that solo custody is independent custody.

The required custody pattern is:

```text
local keypair
→ encrypted PKCS#8 private key
→ at least two durable encrypted user-controlled recovery copies
→ recovery from both copies
→ public certificate + non-secret schema-v2 recovery receipt
→ repository admission and exact validation
→ precollection preflight
→ immutable freeze
→ final closure
→ bounded verification classification
→ separate human-controlled collection authorization
```

The operator-local recovery drill has completed successfully as **`PASS_CURRENT_V2 / STRUCTURAL_SELF_ATTESTED_ONLY / NONINDEPENDENT`**. That local PASS does not satisfy repository-level custody: the exact generated public certificate and non-secret schema-v2 receipt still must be admitted and validated from repository contents. This is the current `HUMAN_ARTIFACT_REQUIRED` boundary.

Repository-side prospective, non-authorizing tooling is accepted through precollection preflight (#612), immutable freeze (#613), final closure (#614), bounded non-independent verification classification (#615), the validator-only human-controlled collection-authorization boundary (#616), fail-closed post-collection result-record semantics (#618), and content-addressed Epoch 002 dataset-lock validation (#622). These controls do not themselves create custody evidence, freeze, authorization, empirical results, dataset lock, unblinding, materialization, primary-analysis authority, efficacy, or scientific N.

PR #622 binds future dataset-lock evidence to the authorized collection/candidate/run identity, retained public and protected artifact identities and digests, the custody-certificate commitment, the 53-record pre-lock ledger ending in PASS `QC_LEDGER`, and the future one-file `DATASET_LOCK_RECEIPT`. The validator remains outcome-blind and preserves the rule that a dataset-lock PASS is a **non-authorizing state transition** requiring a separate exact commit before any future unblinding decision.

No private key, encrypted private-key backup, passphrase, blinding secret, or other recoverable secret belongs in GitHub, Notion, chat, workflow inputs, logs, or committed files. Only the exact public certificate and non-secret schema-v2 recovery receipt produced by the successful local drill are eligible for repository admission.

Replacement empirical collection remains **NOT AUTHORIZED** until repository-level custody is established and the successor prospective gate chain is executed in order.

## What is established — and what is not

The repository contains substantial engineering evidence: governance logic, provenance controls, deterministic validators, CI, negative controls, source binding, custody/security machinery, experimental tooling, runtime evidence, vocabulary governance, and blinded-data infrastructure.

Track A Epoch 001 also contains genuine prospective blinded collection evidence. That evidence is **not a primary efficacy result** and is now explicitly **unanalyzable** because its protected mapping is cryptographically unrecoverable.

A separate Solo research track produced bounded historical empirical evidence. Epoch 004 completed 50 seeds / 9,000 observations and produced negative evidence for its exact executed treatment. A later source audit found that canonical treatment fidelity was not established, so that result is preserved without promoting it into a claim about canonical DGAF efficacy.

DGAF is **not** currently presented as:

- empirically validated as a complete framework;
- independently validated;
- production-certified;
- High-Assurance authorized;
- supported by a completed Track A primary analysis;
- having established canonical DGAF efficacy.

## Internal terms in plain English

| Internal term | Public / industry-neutral translation |
|---|---|
| **Formation** | The set and structure of agents selected for a governed task |
| **TGL / P-35** | Per-turn governance and state-transition kernel |
| **P-* gate** | Project-specific evidence, policy, or authorization checkpoint |
| **PDMAL** | Experimental multi-agent topology / robustness substrate |
| **Freeze** | Immutable binding of the candidate and protected experimental inputs; **not execution authorization** |
| **Closure** | Proof that required pre-authorization prerequisites are complete; **not execution authorization** |
| **Verification classification** | Records what kind of verifier produced the evidence and whether it is independent |
| **Dataset lock** | Immutable receipt binding an accepted collected dataset and retained artifact identities |
| **Unblinding authorization** | Permission to release/decrypt protected mapping material; **not proof that the necessary secret remains recoverable** |
| **Fail closed** | Missing, stale, malformed, ambiguous, or unrecoverable required evidence blocks progress |

See **[`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)** for the full public terminology map and vocabulary governance.

## Where to start

- **Live project/evidence state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)
- **Technical architecture:** [`README.technical.md`](README.technical.md)
- **Governance model:** [`README.governance.md`](README.governance.md)
- **Historical records:** [`docs/HISTORICAL_RECORDS_INDEX.md`](docs/HISTORICAL_RECORDS_INDEX.md)

## Research boundary

Results remain scoped to the exact system identities, treatment definitions, protocols, evidence classes, and custody conditions that produced them. A green test, merged PR, internal qualification score, mathematical property, authorization record, completed collection, or historical result does not automatically establish current empirical efficacy.

Epoch 001 demonstrates an additional governance lesson: **a successful blinded collection is not sufficient if the protected mapping required for the preregistered analysis cannot later be recovered.** The replacement design therefore treats precollection recovery testing as a prerequisite rather than an operational afterthought.

---

Dynamic Governance Agentic Formation  
Governed multi-agent orchestration · provenance · evaluation · authorization · experimental integrity
