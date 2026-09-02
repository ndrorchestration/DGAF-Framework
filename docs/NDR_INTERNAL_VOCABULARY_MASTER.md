# NDR INTERNAL VOCABULARY MASTER LIBRARY

> **Epistemic status:** Canonical terminology registry; vocabulary mappings are not evidence of implementation or validation.
> **Last updated:** 2026-09-02 — transversal dependency and candidate-state reconciliation

## Epistemic standard

This document maps internal names to the nearest useful external terminology. A mapping is a **translation aid**, not a claim of equivalence, novelty, correctness, capability, or validation.

Every substantive claim should be interpreted using the following evidence classes:

- **DEFINED** — terminology or intended role is explicitly specified.
- **IMPLEMENTED** — corresponding behavior exists in source code.
- **COMPUTED** — the value is produced by an identified calculation or test.
- **VERIFIED** — independently reproducible evidence supports the claim under a stated test procedure.
- **ATTESTED** — a project record reports the result, but independent recomputation has not been established.
- **HISTORICAL** — true only as a record of an earlier project state.
- **HYPOTHESIS** — proposed relationship requiring testing.
- **METAPHOR** — explanatory analogy; not an implementation claim.
- **UNSUPPORTED** — insufficient evidence; must not be presented as established fact.
- **DEPRECATED** — retained only for traceability.

### Vocabulary rules

1. A prestigious external term must not be used merely because it sounds analogous.
2. A mathematical identity does not establish an engineering property unless the property is derived or experimentally supported.
3. Percentages, `Nx` multipliers, benchmark values, and performance comparisons require a stated denominator, measurement procedure, and provenance.
4. Hard-coded benchmark literals are **ATTESTED** at most until their source telemetry and calculation are reproducible.
5. Agent/persona role descriptions describe intended function; they do not establish autonomous capability.
6. Historical attestations remain historical unless revalidated against the current implementation.
7. Cross-project terminology does not establish that two systems are the same system.
8. Where an external term is only an analogy, label it **METAPHOR** or **CLOSE ANALOGY**, not as an identity.
9. A historical identifier may remain in historical records for provenance but must not be silently reused as a current canonical label.

## Current terminology correction: FLAG-02

**FLAG-02 is a historical identifier.** It was previously associated with the 340% coordination-gain claim in S069/S072 governance records. Later governance reassigned the current evaluation-mode terminology to **qualitative**.

Therefore:

- Historical documents may retain `FLAG-02` when necessary to preserve provenance.
- Current/living documents must use **qualitative** for the evaluation mode.
- New documents must not introduce `FLAG-02` as a current identifier.
- `FLAG-02 = 340% coordination gain = CLOSED` is a historical session statement, not a current verification statement.

## Current status of the former 340% coordination-gain claim

The former 340% figure is **NOT A CURRENT VERIFIED RESULT**. It remains a historical/provenance item subject to the propagation consistency control and claim-evidence requirements.

Any current recurrence must either:

1. explicitly identify the statement as historical and preserve its provenance; or
2. use a current qualified formulation such as `unverified`, `illustrative`, or another qualifier that is actually applicable to the surrounding claim.

The repository must not treat proximity to a qualifier as semantic proof that the qualifier applies. Propagation checks are advisory QA controls and require contextual adjudication.

## High-priority corrections

### PDMAL — corrected external mapping

**Previous characterization:** "Distributed Consensus Monitor / BFT-adjacent Convergence Tracker" with wording that could imply PDMAL itself is a Byzantine Fault Tolerance consensus protocol.

**Canonical characterization:**

> **PDMAL (Phi-Driven Multi-Agent Lattice)** — a dodecahedral-graph lattice/control structure with mathematically specified topology and convergence-related measurements. The current verified artifacts establish graph properties, selected mathematical quantities, and harness calculations; they do **not** by themselves establish that PDMAL implements a complete Byzantine Fault Tolerance consensus protocol.

**Evidence class:** `VERIFIED` for the explicitly tested graph/math quantities; `DEFINED` for the broader architectural role; BFT equivalence: **UNSUPPORTED unless a separate implementation and fault-model evaluation establishes it.**

### Mathematical vocabulary

Names such as **Phi-Calculus**, **Tarski Layer**, **Harmonic**, **attractor**, **Ricci**, **Hecke**, **Lyapunov**, and **spectral** must identify the actual mathematical object or computation implemented. A mathematical name may be retained as an internal metaphor only when explicitly labeled `METAPHOR`.

In particular, a stochastic admission threshold must not be called a **Hecke operator** unless an actual Hecke operator or justified numerical approximation is implemented.

### Performance vocabulary

Claims such as `150x jitter`, `200x jitter`, `88.1% PAR`, `2-cycle recovery`, `340% coordination gain`, and similar values require:

`source telemetry → calculation → reproducible test → reported result`

Absent that chain, classify the claim as `ATTESTED`, `HISTORICAL`, `HYPOTHESIS`, or `UNSUPPORTED` as appropriate; do not call it a verified benchmark.

### Agent vocabulary

Agent names such as **Oracle**, **Sentience**, **Paragon**, **Vanguard**, **Navigator**, **Momentum**, **Equilibrium**, and similar labels describe intended roles unless implementation and evaluation evidence demonstrates the claimed capability. Terms such as "authority," "forecaster," "consciousness," "benchmark setter," or "stability analyst" must not be interpreted as empirical capability claims solely from the taxonomy.

## External-equivalent mapping convention

For each future entry, use this form:

| Internal term | External equivalent / closest analogue | Evidence class | Differentiation / limitation |
|---|---|---|---|
| `<name>` | `<peer-recognized term>` | `DEFINED / IMPLEMENTED / COMPUTED / VERIFIED / ...` | Explain the actual implementation and explicitly state where the analogy stops. |

**Rule:** If the internal implementation is substantially different from the external concept, prefer **"closest analogue"** over **"equivalent."**

## Historical terminology

The following are retained for traceability and must not be used as current capability claims without revalidation:

- historical BFT consensus characterization of PDMAL
- historical FLAG-02 identifier
- the former 340% coordination-gain claim
- ungrounded percentage or `Nx` performance claims
- unverified mathematical-operator labels
- historical lifecycle benchmark values copied from generated artifacts
- historical agent capability descriptions not backed by current implementation/evaluation

See `docs/taxonomy/EPISTEMIC_VOCABULARY_STANDARD.md` for the full policy and `docs/taxonomy/TAXONOMY_ADDENDUM_8_AGENTS.md` for the historical taxonomy addendum.

## Transversal Candidate-State Vocabulary — 2026-09-02

A **candidate** is the exact executable identity selected for a verification cycle. An **apparatus/source** is the provenance anchor from which the candidate lineage is derived. A **deployment** is an execution substrate identity and is not synonymous with a candidate. A **workflow head** is the CI execution identity and is not synonymous with either the candidate or deployment. An **artifact** is a retained evidence object produced by a scoped execution. A **freeze** is an immutable experimental identity. **Authorization** is a separate governance transition. **Empirical** denotes accepted observations produced only after the required freeze and authorization state exists.

Required identity tuple:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

Use:

- `ROLE DIFFERENCE` when two identities intentionally serve different semantic roles.
- `HISTORICAL` when a prior identity is retained for provenance and cannot close the current cycle.
- `TRANSVERSAL DRIFT` when live projections can reasonably be interpreted as different current states.
- `BLOCKING CONTRADICTION` when the discrepancy could permit invalid evidence transfer, closure, freeze, or authorization.
- `CANDIDATE-BOUND` only when evidence names the exact candidate that produced it.
- `CURRENT-CYCLE` only for evidence whose upstream dependencies all resolve to the selected candidate cycle.

### P-35 / P-42 namespace and remediation boundary

`P-35` is **Procluding Premise Gate**. `P-42` is **Adaptive Harmonic Governance (AHG)**. P-35 was retained as the canonical pre-admissibility name after the AHG collision was resolved by renumbering AHG to P-42.

The current remediation additionally requires an explicit `premise_check_fn` at the DGAF/TGL/ConsensusTask boundary. This is an **engineering dependency / wiring contract**. It is not a declaration of the PDMAL-specific constitutional premise policy. The latter remains an experimental-control dependency requiring explicit approval before pilot execution.

### Evidence-state ordering

The preferred lifecycle vocabulary is:

`DEFINED → IMPLEMENTED → TESTED → CANDIDATE-BOUND → VERIFIED → FROZEN → AUTHORIZED → EMPIRICAL`

These are non-equivalent states. A READY deployment is not runtime verification; verification is not freezing; freezing is not authorization; authorization is not an empirical observation.

### Cross-system rule

GitHub, Vercel, Notion, taxonomies, pattern registries, and retained evidence must use role-qualified identities and compatible status language. Shared URLs, shared repositories, branch ancestry, or behavioral similarity do not establish candidate equivalence.

**Canonical reconciliation addendum:** `docs/taxonomy/TRANSVERSAL_AGREEMENT_AND_DEPENDENCY_TAXONOMY_2026-09-02.md`
