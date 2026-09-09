# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** is an experimental framework for governed multi-agent AI systems. It treats **capability, evidence, verification, authority, and permission to act as separate machine-relevant states** rather than assuming that one implies another.

In plain English: an agent may be able to do something and still be blocked from doing it; a system may pass engineering tests and still be blocked from claiming that it is empirically validated.

> **Canonical High-Assurance research status:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N = 0  
> **Track A Epoch 001:** PROSPECTIVE COLLECTION COMPLETE · 50 paired inferential seed units · 2,250 blinded observations · DATASET LOCK ESTABLISHED · UNBLINDING AUTHORIZED  
> **Track A post-collection boundary:** custody-key handoff NOT ESTABLISHED · unblinded analysis input NOT YET MATERIALIZED · primary analysis NOT AUTHORIZED / NOT RUN  
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
| **A** | Numeric topology robustness | Preregistered; analysis locked; hardened runner merged; preflight/freeze/closure established; verification PASS as developer self-attested/non-independent; collection complete; blinded dataset locked; unblinding authorized; custody-key handoff and unblinded-input materialization still pending; primary analysis not authorized/run |
| **B1** | Semantic routing and safety | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B2** | Persistent context and closure | Standalone non-empirical lane complete; no empirical efficacy claim |
| **B3** | Persistent weighted-graph convergence monitoring | Standalone non-empirical lane complete; no empirical efficacy claim |
| **C** | Integrated DGAF composition | Non-empirical composition proposal merged; empirical execution NOT AUTHORIZED |

Track A's prospective scientific panel was fixed at **50 seeds × 5 topologies × 9 failure counts = 2,250 observations** and has now been collected under the governed blinded collection path. The accepted scientific unit count is **50 paired inferential seed units / 2,250 blinded raw observations**. Collection completion is not analysis completion: the separately held custody key has not yet been handed off through the accepted path, the unblinded analysis input has not been materialized, and the locked primary analysis has not been authorized or run.

## What is established — and what is not

The repository contains substantial engineering evidence: governance logic, provenance controls, deterministic validators, CI, negative controls, source binding, custody/security machinery, experimental tooling, and blinded-data infrastructure.

Track A now also contains prospective blinded empirical collection evidence under its exact frozen protocol and authorization chain. That evidence is **not yet a primary result**. The post-collection sequence remains fail-closed: matching custody-key handoff → controlled materialization → immutable unblinded-input receipt → separate primary-analysis authorization → locked primary analysis.

A separate Solo research track produced bounded historical empirical evidence. Epoch 004 completed 50 seeds / 9,000 observations and produced negative evidence for its exact executed treatment. A later source audit found that canonical treatment fidelity was not established, so that result is preserved without promoting it into a claim about canonical DGAF efficacy.

DGAF is **not** currently presented as:

- empirically validated as a complete framework;
- independently validated;
- production-certified;
- High-Assurance authorized;
- supported by a completed Track A primary analysis;
- having established canonical DGAF efficacy.

## Internal terms in plain English

DGAF has accumulated project-specific names over its development history. Those names remain useful inside the governance system, but they should not be prerequisites for understanding the project.

| Internal term | Public / industry-neutral translation |
|---|---|
| **Formation** | The set and structure of agents selected for a governed task |
| **TGL / P-35** | Per-turn governance and state-transition kernel |
| **P-* gate** | Project-specific evidence, policy, or authorization checkpoint |
| **PDMAL** | Experimental multi-agent topology / robustness substrate |
| **Freeze** | Immutable binding of the candidate and protected experimental inputs; **not execution authorization** |
| **Closure** | Proof that required pre-authorization prerequisites are complete; **not execution authorization** |
| **Verification classification** | Records what kind of verifier produced the evidence and whether it is independent |
| **Collection authorization** | Explicit permission to collect the preregistered prospective observations; **not evidence that collection already happened** |
| **Dataset lock** | Immutable receipt binding the accepted collected dataset and its retained artifact identities |
| **Unblinding authorization** | Permission to release/decrypt the protected topology mapping for the exact locked dataset; **not permission to run the primary analysis** |
| **Fail closed** | Missing, stale, malformed, or ambiguous required evidence blocks progress |

See **[`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)** for the full public terminology map.

## Where to start

- **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](docs/PUBLIC_TRANSLATION_LAYER.md)
- **Live project/evidence state:** [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
- **Technical architecture:** [`README.technical.md`](README.technical.md)
- **Governance model:** [`README.governance.md`](README.governance.md)
- **Historical records:** [`docs/HISTORICAL_RECORDS_INDEX.md`](docs/HISTORICAL_RECORDS_INDEX.md)

## Research boundary

Results remain scoped to the exact system identities, treatment definitions, protocols, evidence classes, and custody conditions that produced them. A green test, merged PR, internal qualification score, mathematical property, authorization record, completed collection, or historical result does not automatically establish current empirical efficacy.

---

Dynamic Governance Agentic Formation  
Governed multi-agent orchestration · provenance · evaluation · authorization · experimental integrity
