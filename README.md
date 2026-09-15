# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, and permission to act as separate machine-relevant states** rather than assuming that one implies another.

In plain English: an agent may be able to do something and still be blocked from doing it; a system may pass engineering tests and still be blocked from claiming that it is empirically validated.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** PROSPECTIVE BLINDED COLLECTION COMPLETE · 50 paired inferential seed units · 2,250 blinded observations · DATASET LOCK ESTABLISHED  
> **Epoch 001 disposition:** protected mapping is **CRYPTOGRAPHICALLY UNRECOVERABLE** · primary analysis **UNANALYZABLE / NOT RUN**  
> **Successor Track A / Epoch 002:** custody, freeze, closure, bounded verification classification, collection authorization, dataset lock, and bounded unblinding **ACCEPTED/ESTABLISHED AT THEIR EXACT SCOPES** · blinded collection **COMPLETE** at 50 paired seed units / 2,250 observations · materialization tooling **ACCEPTED** · real materialization **NOT ESTABLISHED** · primary analysis **NOT AUTHORIZED / NOT RUN**  
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
| **A — Epoch 002 successor** | Replacement prospective topology robustness | Collection COMPLETE at 50 paired seed units / 2,250 observations; dataset lock ESTABLISHED; bounded unblinding AUTHORIZED for controlled mapping release/decryption only; Stage-1 and Stage-2 materialization tooling ACCEPTED; real materialization and materialization receipt NOT ESTABLISHED; primary analysis NOT AUTHORIZED / NOT RUN |
| **B1** | Semantic routing and safety | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B2** | Persistent context and closure | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B3** | Persistent weighted-graph convergence monitoring | Standalone non-empirical lane complete; no empirical efficacy claim |
| **C** | Integrated DGAF composition | Non-empirical composition proposal merged; empirical execution NOT AUTHORIZED |

Epoch 001's prospective panel was fixed at **50 seeds × 5 topologies × 9 failure counts = 2,250 observations**. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**.

That collection remains valid evidence that the blinded panel was executed and retained. It cannot produce its preregistered primary result because the retained encrypted topology mapping cannot be recovered: the matching private key was not durably recoverable in the solo operating model. Regenerating a different key cannot decrypt the retained ciphertext, and guessing or reconstructing the hidden assignment is prohibited.

## Successor Track A custody and gate design

Issue #523 controls the replacement path. Epoch 002 uses a distinct protocol identity, fresh seeds and blinding, and recoverable solo custody without presenting same-system custody as independent.

Repository custody, precollection preflight, immutable freeze, final closure, bounded non-independent verification classification, separate collection authorization, retained-evidence admission/QC, dataset lock, and bounded unblinding have advanced through separate governed events. The authorized operator-executed Codespace collection is complete at **50 paired seed units / 2,250 blinded observations**.

The current frontier is **controlled operator-side materialization of the real retained Epoch 002 evidence**. The accepted apparatus now includes:

- a PASS content-addressed dataset-lock receipt;
- a separate PASS unblinding decision bounded to `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`;
- PR #713's controlled Stage-1 materializer with wrong-key, archive-drift, duplicate-entry, traversal/link, and unexpected-member fail-closed behavior;
- PR #715's non-secret Stage-2 materialization evidence bundle with deterministic content-addressed output identities and atomic five-member publication.

Tooling acceptance does not claim that real materialization occurred. Until the exact retained material is processed under the accepted operator-controlled path and a separate immutable materialization receipt is admitted, preserve:

- `TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED`;
- `UNBLINDING = AUTHORIZED / BOUNDED TO CONTROLLED MAPPING RELEASE OR DECRYPTION`;
- `TRACK_A_EPOCH_002_MATERIALIZATION = NOT_ESTABLISHED`;
- `PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT RUN`;
- `SCIENTIFIC_N_INCREMENT = 0`;
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`;
- `INDEPENDENT_VALIDATION = NOT_ESTABLISHED`;
- `HIGH_ASSURANCE = PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`.

The remaining ordered sequence is:

`controlled local materialization → validated non-secret materialization evidence admission → immutable materialization receipt → separate primary-analysis authorization → locked analysis → interpretation/adjudication`

No private key, passphrase, blinding secret, protected plaintext mapping, decrypted protected data, or other recoverable secret material belongs in GitHub, Notion, chat, CI inputs, workflow logs, or committed files.

## What is established — and what is not

The repository contains substantial engineering evidence: governance logic, provenance controls, deterministic validators, CI, negative controls, source binding, custody/security machinery, experimental tooling, runtime evidence, vocabulary governance, and blinded-data infrastructure.

Track A Epoch 001 also contains genuine prospective blinded collection evidence. That evidence is **not a primary efficacy result** and is explicitly **unanalyzable** under the retained protected-mapping evidence.

Track A Epoch 002 has advanced further: the successor collection is complete, its dataset lock is established, and bounded unblinding is authorized. Those transitions still do **not** constitute a primary efficacy result; real materialization, a materialization receipt, separate primary-analysis authorization, locked analysis execution, and later interpretation remain distinct downstream events.

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
