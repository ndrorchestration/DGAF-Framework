# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, and permission to act as separate machine-relevant states** rather than assuming that one implies another.

In plain English: an agent may be able to do something and still be blocked from doing it; a system may pass engineering tests and still be blocked from claiming that it is empirically validated.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** PROSPECTIVE BLINDED COLLECTION COMPLETE · 50 paired inferential seed units · 2,250 blinded observations · DATASET LOCK ESTABLISHED  
> **Epoch 001 disposition:** protected mapping is **CRYPTOGRAPHICALLY UNRECOVERABLE** · primary analysis **UNANALYZABLE / NOT RUN**  
> **Successor Track A:** issue #523 open · repository custody-v2 **SATISFIED / SAME_SYSTEM_NONINDEPENDENT** · precollection preflight **ACCEPTED / PASS** · immutable freeze **NOT ESTABLISHED** · dataset-lock tooling **ACCEPTED (#622)** · unblinding-decision validation tooling **ACCEPTED (#627)** · dataset lock **NOT ESTABLISHED** · replacement empirical collection **NOT AUTHORIZED**  
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
| **A — Epoch 002 successor** | Replacement prospective topology robustness | Issue #523 governs the successor; repository custody-v2 is accepted as same-system/non-independent and precollection preflight is accepted/PASS; immutable freeze is the next separate gate; no successor dataset lock or unblinding event exists and empirical collection is not authorized |
| **B1** | Semantic routing and safety | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B2** | Persistent context and closure | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B3** | Persistent weighted-graph convergence monitoring | Standalone non-empirical lane complete; no empirical efficacy claim |
| **C** | Integrated DGAF composition | Non-empirical composition proposal merged; empirical execution NOT AUTHORIZED |

Epoch 001's prospective panel was fixed at **50 seeds × 5 topologies × 9 failure counts = 2,250 observations**. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**.

That collection remains valid evidence that the blinded panel was executed and retained. It cannot produce its preregistered primary result because the retained encrypted topology mapping cannot be recovered: the matching private key was not durably recoverable in the solo operating model. Regenerating a different key cannot decrypt the retained ciphertext, and guessing or reconstructing the hidden assignment is prohibited.

## Successor Track A custody and gate design

Issue #523 controls the replacement path. Epoch 002 uses a new protocol identity, fresh seeds and fresh blinding, and a recoverable solo-custody design without pretending that solo custody is independent custody.

The operator-local recovery drill completed successfully as **`PASS_CURRENT_V2 / STRUCTURAL_SELF_ATTESTED_ONLY / NONINDEPENDENT`**. Its exact public certificate and non-secret schema-v2 receipt were subsequently admitted and accepted in the repository by #644. Repository `real_custody_v2` is therefore **satisfied**, while the custody classification remains **`SAME_SYSTEM_NONINDEPENDENT`** and independent custody remains false.

The accepted public custody artifacts are:

- `docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem`
- `docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json`

Private keys, passphrases, encrypted backup copies, blinding secrets, protected plaintext mappings, and other recoverable secret material do not belong in GitHub, Notion, chat, CI inputs, workflow logs, or committed files.

The clean one-file precollection-preflight record was accepted by #651. It binds the exact candidate/source/custody identities and records `preflight_status = PASS` while explicitly preserving `collection_authorized = false` and `scientific_n_increment = 0`.

Repository-side prospective tooling is accepted through:

- precollection preflight (#612);
- immutable freeze (#613);
- final closure (#614);
- bounded non-independent verification classification (#615);
- separate human-controlled collection-authorization validation (#616);
- fail-closed post-collection result-record semantics (#618);
- content-addressed dataset-lock validation (#622);
- separate fail-closed human-controlled unblinding-decision validation (#627).

Tooling readiness does **not itself create** custody acceptance, preflight, freeze, closure, authorization, empirical results, dataset lock, unblinding, materialization, primary-analysis authority, efficacy, independent validation, High-Assurance authority, or scientific N. The bounded custody and preflight states above exist only because their separate evidence events were accepted.

## Ordered successor lifecycle

The scientific/control sequence is intentionally split into separate transitions:

```text
repository custody acceptance [SATISFIED]
→ precollection preflight [ACCEPTED / PASS]
→ immutable freeze [NEXT / NOT ESTABLISHED]
→ final closure
→ bounded verification classification
→ separate collection authorization
→ empirical collection
→ PASS QC
→ dataset lock
→ separate human-controlled unblinding decision
→ controlled local materialization
→ immutable materialization receipt
→ separate primary-analysis authorization
→ locked primary analysis
→ interpretation/adjudication
```

The immutable freeze is a provenance/immutability event, not collection authorization. The dataset-lock transition is non-authorizing and cannot authorize its own successor. A future PASS unblinding decision is bounded to controlled mapping release/decryption only and does not authorize primary analysis. Materialization remains a separate controlled operation and receipt, followed by a still-separate primary-analysis authorization.

Replacement empirical collection remains **NOT AUTHORIZED** until the remaining predecessor chain is executed and a separate collection-authorization event is accepted.

## What is established — and what is not

The repository contains substantial engineering evidence: governance logic, provenance controls, deterministic validators, CI, negative controls, source binding, custody/security machinery, experimental tooling, runtime evidence, vocabulary governance, and blinded-data infrastructure.

Track A Epoch 001 also contains genuine prospective blinded collection evidence. That evidence is **not a primary efficacy result** and is explicitly **unanalyzable** under the retained protected-mapping evidence.

For Track A Epoch 002, repository custody-v2 and precollection preflight are now established within their exact scopes. That does **not** establish immutable freeze, final closure, verification classification, collection authorization, empirical execution, dataset lock, unblinding, materialization, primary-analysis authority, independent validation, or efficacy.

A separate Solo research track produced bounded historical empirical evidence. Epoch 004 completed 50 seeds / 9,000 observations and produced negative evidence for its exact executed treatment. A later source audit found that canonical treatment fidelity was not established, so that result remains exact-treatment historical evidence rather than a claim about canonical DGAF efficacy.

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
| **Dataset lock** | Immutable receipt binding an accepted collected dataset and retained artifact identities; **not unblinding or analysis authorization** |
| **Unblinding decision** | Separate human-controlled permission for bounded treatment-identity release/decryption; **not materialization or analysis authorization** |
| **Materialization** | Deterministic construction of analysis-ready unblinded input; **not outcome aggregation or analysis** |
| **Primary-analysis authorization** | Separate permission to run the locked confirmatory analysis |
| **Fail closed** | Missing, stale, malformed, ambiguous, or unrecoverable required evidence blocks progress |

See **[`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)** for the full public terminology map and vocabulary governance.

## Where to start

- **Live project/evidence state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Compatibility status entrypoint:** [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
- **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)
- **Technical architecture:** [`README.technical.md`](README.technical.md)
- **Governance model:** [`README.governance.md`](README.governance.md)
- **Historical records:** [`docs/HISTORICAL_RECORDS_INDEX.md`](docs/HISTORICAL_RECORDS_INDEX.md)

## Research boundary

Results remain scoped to the exact system identities, treatment definitions, protocols, evidence classes, and custody conditions that produced them. A green test, merged PR, internal qualification score, mathematical property, authorization record, completed collection, or historical result does not automatically establish current empirical efficacy.

Epoch 001 demonstrates an additional governance lesson: **a successful blinded collection is not sufficient if the protected mapping required for the preregistered analysis cannot later be recovered.** The successor design therefore treats precollection recovery testing as a prerequisite rather than an operational afterthought.

---

Dynamic Governance Agentic Formation  
Governed multi-agent orchestration · provenance · evaluation · authorization · experimental integrity
