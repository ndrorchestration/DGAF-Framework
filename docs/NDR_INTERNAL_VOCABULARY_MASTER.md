# NDR INTERNAL VOCABULARY MASTER LIBRARY

> **Epistemic status:** Canonical terminology registry; vocabulary mappings are not evidence of implementation or validation.
> **Last updated:** 2026-08-15 — epistemic standards pass

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

- BFT consensus characterization of PDMAL
- ungrounded percentage or `Nx` performance claims
- unverified mathematical-operator labels
- historical lifecycle benchmark values copied from generated artifacts
- historical agent capability descriptions not backed by current implementation/evaluation

See `docs/taxonomy/EPISTEMIC_VOCABULARY_STANDARD.md` for the full policy and `docs/taxonomy/TAXONOMY_ADDENDUM_8_AGENTS.md` for the historical taxonomy addendum.
