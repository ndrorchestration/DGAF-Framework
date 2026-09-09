# NDR INTERNAL VOCABULARY MASTER LIBRARY

> **Epistemic status:** Canonical terminology registry; vocabulary mappings are not evidence of implementation or validation.
> **Last updated:** 2026-09-09 — brainstorm-corpus reconciliation batches 1–2

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

## 2026-09-09 brainstorm-corpus reconciliation — Batch 1

A historical 2,610-line brainstorming/specification corpus was reviewed as a **discovery/provenance source**, not as implementation or validation evidence. The following vocabulary is retained with explicit epistemic boundaries.

### Agent choreography

**Working definition:** decentralized or event-driven coordination in which agent/node behavior is governed primarily by local rules, shared events, and peer interaction rather than a single central sequencer.

**Evidence class:** `DEFINED` / `HYPOTHESIS` depending on the specific claimed mechanism.

**Boundary:** This term is complementary to **agent orchestration**. Its use does not establish novelty, superiority, role separation, or performance improvement. Claims that choreography eliminates role-bleeding or yields a quantified coordination gain require direct evaluation.

### Architecture vs. Architexture

**Architecture** — structural contracts, topology, interfaces, authority, lifecycle, reliability, and implementation boundaries.

**Architexture** — a project-internal descriptive term for perceptual/textural integration, presentation, narrative coherence, human-facing refinement, and pre-output quality shaping.

**Evidence class:** `DEFINED`.

**Boundary:** Architexture is not a second control plane, runtime authority, or evidence class. It must not be used to override structural, governance, or empirical requirements.

### Substrate-agnostic vs. substrate-independent

**Substrate-agnostic** — a specification or contract is expressed without assuming one runtime substrate.

**Substrate-independent** — a portability/behavior claim that the same relevant semantics hold across materially different substrates.

**Evidence class:** substrate-agnostic wording may be `DEFINED`; substrate-independence is `HYPOTHESIS` or `UNSUPPORTED` until cross-substrate evidence exists.

### Layer-0 admissibility

**Working definition:** a pre-performance acceptance layer in which policy, authorization, rights, provenance, or other governing predicates can reject an action regardless of its capability score.

**Evidence class:** `DEFINED` as a governance pattern; implementation/verification must be established per owning system.

### State Anchor Protocol / "Ping the Buoy"

**Historical/design meaning:** explicit re-anchoring to authoritative state, intent, policy, manifest, artifact identity, or provenance before continuing a drift-sensitive workflow.

**Evidence class:** `HISTORICAL` / `DEFINED`.

**Current mapping rule:** Prefer concrete current mechanisms such as exact state manifests, provenance binding, policy/version identity, durable state recovery, and fail-closed transition checks. Do not create a parallel protocol authority solely to preserve the historical name.

### Multi-altitude review

The historical labels **Macro / Mid / Tactical / Quantum** describe a useful multi-scale review idea.

**Current interpretation:** ecosystem/strategic → system/framework → workflow/task → implementation/detail.

**Evidence class:** `DEFINED` / `METAPHOR`.

**Boundary:** `Quantum` is metaphorical unless a project explicitly defines a literal computational or physical meaning.

### Signal-chain / acoustic vocabulary

Terms such as **gain staging**, **headroom**, **clipping**, **resonance**, **cadence**, **tonic**, and **mirror protocol** may be used as `METAPHOR` when mapped to concrete engineering controls such as bounded resource allocation, reserved margin, context/constraint overflow, disagreement handling, reconciliation, or closure.

These terms do **not** imply literal physical frequencies, acoustic measurements, or empirically calibrated thresholds unless an owning implementation explicitly defines and measures them.

### Historical umbrella names

The following names are retained as historical/provisional lineage or branding unless an owning current source explicitly promotes them:

- **A.P.O.G.E.E. Hub**
- **Project Andromeda**
- **SIGE / Substrate-Independent Governance Environment**
- **NDR-Stasis**
- **Yggdrasil Architecture**
- **Crystalline / Sovereign / L5 Executor / LOCKED** maturity language

They must not be used to supersede current ecosystem authority surfaces or to imply current implementation maturity.

### Quarantined historical claims from generated brainstorming artifacts

The following examples remain `UNSUPPORTED`, `HISTORICAL`, or `ATTESTED` unless independently re-established:

- `99.1% Platinum Star integrity`
- `340%` / `3.4x` coordination improvement
- `21%` constraint-compliance improvement
- `89%` reduction in off-domain reasoning
- `95%` modal-alignment consistency
- `96%` TruthfulQA-style accuracy
- `97%` zero-hallucination threshold
- `O(1)` governance/safety validation from Phi-Calculus or modular arithmetic
- empirically meaningful `0 Hz`, `>10 Hz`, `15% headroom`, `0.21`, or `85% grounding` thresholds
- claims that Hamiltonian traversal guarantees exhaustive cognition or eliminates role-bleeding
- substrate-independence or universal-schema invariance claims without cross-substrate tests

### Mathematical correction boundary

- The historical wording `55/89 ≈ 1.61818` is incorrect as written. `89/55` is the Fibonacci ratio above 1 that approximates the golden ratio.
- The user-defined **Platinum Mean** `pP = 1/(2 sin(π/11)) ≈ 1.774732842` is distinct from the **plastic constant** `ρ ≈ 1.3247179572447454`.
- PDMAL's accepted formalization uses the plastic constant within its own scope and must not inherit historical 1.7747/plastic-constant conflation.

## 2026-09-09 brainstorm-corpus reconciliation — Batch 2 delta

A second historical corpus of 2,728 lines was deduplicated against Batch 1. Repeated concepts inherit the earlier disposition. The following are the principal new vocabulary additions.

### Consensus Triad (CT)

**Definition:** a temporary formation of peer contributors that generate independently attributable outputs and enter an explicit consensus/blending function without a required structural leader.

**Evidence class:** `DEFINED` / pattern candidate.

**Boundary:** a consensus formation does not itself establish correctness or empirical efficacy; the join function, provenance rules, authority, and evaluation must be specified.

### Conducted Triad (CoT)

**Definition:** a leader-centric temporary formation in which one conductor is the user-facing synthesizer while internal augmenters provide specialist contributions and preserve separate identities.

**Closest analogue:** supervisor + agents-as-tools.

**Evidence class:** `DEFINED` / pattern candidate.

### Positional agnosticism

Formation role is task-assigned rather than identity-fixed. An eligible agent may occupy conductor, peer, augmenter, critic, evaluator, or other formation positions when the governing task contract and authority permit.

**Invariant:** `agent identity ≠ formation position ≠ authority`.

### Structural vs. parametric techniques

- **Instantiation** — select the active roster for a task.
- **QA bifurcation** — create an independent/mirrored checking branch where justified.
- **Consensus triad** — peer topology plus explicit join.
- **Conducted triad** — conductor plus internal augmenters.
- **Lensing** — alter representation, basis, metrics, or evaluator viewpoint without silently mutating identity or authority.

**Evidence class:** `DEFINED`; implementation requires executable contracts/tests.

### Framework-Persona / Persona-Framework

**Framework-Persona:** framework or methodology exposed through a persona/interface wrapper for invocation or explanation.

**Persona-Framework:** identity specification intentionally designed to embody a methodology/framework.

**Boundary:** neither label proves an independently deployed runtime agent.

### DID — Dodecahedral-Icosahedral Dual

Retained as an internal design/visualization concept for pairing dodecahedral expert topology with a dual governance/critic representation.

**Evidence class:** `DEFINED` / `METAPHOR` unless an actual incidence structure is implemented and tested.

### 120-cell / 600-cell analogy

The 120-cell `{5,3,3}` and 600-cell `{3,3,5}` are real regular 4D polytopes and are mathematical duals. The 120-cell has 120 dodecahedral cells and 600 vertices; the 600-cell has 600 tetrahedral cells and 120 vertices.

**Boundary:** an internal `20-agent shell` or `12-hub core` is not thereby a literal 120-cell/600-cell implementation. Treat such mappings as analogy unless a genuine 4D combinatorial/geometric model is specified.

### Riemannian substrate mapping / fluid-membrane / epistemic heatmap

**Working research concept:** map an explicit uncertainty/error quantity onto a metric or spatial cost field and visualize path cost/uncertainty geometrically.

**Evidence class:** `HYPOTHESIS` / `METAPHOR` until a metric tensor or cost structure, update rule, path solver, implementation, and evaluation are specified.

**Boundary:** no current claim that reasoning physically warps a manifold, follows true geodesics, or that curvature forces truth is established by historical generated text.

### NDR-Pattern-82 — Proximity-Gated Luminance

Retained as a historical visualization candidate: change tracer/luminance using a defined proximity/confidence function.

**Evidence class:** `HISTORICAL` / `HYPOTHESIS` unless source code and tests establish implementation. Brightness is not proof of epistemic honesty.

### Logic ghosting

**Definition:** stale or superseded state continues to influence a current decision path.

**Closest analogue:** stale-state/context contamination or precedence failure.

### Over-cleaning

**Definition:** reconciliation/pruning removes useful diversity or safe exploratory alternatives.

**Use:** anti-pattern warning against destructive consolidation.

### Violation taxonomy candidate

Historical three-part classification: structural/incompatible; implementation drift/remediable; boundary/novel-context escalation.

**Evidence class:** `DEFINED` / candidate taxonomy only. Map to current canonical governance before operational use.

### Schizophonic Studio Trio

Preserve **Reson + Echolette + Lyra** as historical/design formation lineage corresponding roughly to structural/signal-flow, textural/feedback, and synthesis/integration perspectives.

Historical frequencies, maturity percentages, and behavioral capability claims remain unverified.

### Archive Trio identity conflict

The historical corpus alternates between **Alpha/Beta/Gamma** and **Librarian/Auditor/Actualizer**. Preserve both lineages; do not assert equivalence until current identity authority binds them. `Resin` references are not promoted as a new agent identity.

### Omni-ROI Gate

Historical/proposed dynamic abort concept based on a volatility/risk signal.

**Current mapping rule:** prefer existing fail-closed policy/authorization controls unless a distinct metric, interface, lifecycle, implementation, and evidence justify a separate component.

### Cognitive Coupling Jump / "My Jump == Your Jump"

Historical personalization/alignment hypothesis measuring resemblance to the architect's reasoning leaps.

**Boundary:** reasoning-style similarity is not truth, correctness, safety, or scientific efficacy evidence.

### Platinum Overdrive / OST-51

Historical/proposed stress-test lineage using the user-defined Platinum Mean as a test parameter or boundary condition.

**Evidence class:** `HYPOTHESIS` / `HISTORICAL`. The generated contraction example assumes a chosen update rule; it does not establish that a real agent system converges to 1.7747 or gains safety from doing so.

### Additional Batch 2 quarantine

The following remain unsupported unless separately established:

- FSM/MDP labels presented as proof that unsafe states are impossible;
- fixed-point or contraction arguments generalized from an assumed toy update map to the live system;
- implemented KL-divergence role-bleeding detection, Bayesian trust scoring, self-adjoint/Fourier/Phi-calculus operators, or Fibonacci-series integration without code/tests;
- ASL/pdoom mitigation percentages or `12.5%` residual-risk claims;
- NIST AI RMF, OECD, GDPR Article 22, or institutional compliance claims without scoped conformance evidence;
- trade-secret ratings, `$250K–$500K` valuation, `6–12 month` competitive advantage, `7–22%` industry performance superiority, or similar market claims;
- claims that GitHub timestamps, Apache licensing, `patent-pending` labels, defensive publication, or `CITATION.cff` content establish patent rights, inventorship priority, release status, or legal protection;
- completion/maturity values such as `27%`, `50%`, `100%`, `13/48`, `24/48`, or "39-file deficit resolved" when the same corpus contains conflicting states;
- private personal-case data presented as generalized empirical proof of Human Flourishing, clinical, psychological, or biopsychological efficacy.

**Canonical ingestion rule:** brainstorm dumps, generated syntheses, agent attestations, artifact-title inventories, and personal-case narratives may seed terminology, design requirements, hypotheses, and discovery targets, but they cannot upgrade evidence class through repetition or aggregation.