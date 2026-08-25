# DGAF Contribution Comparison Matrix

**Status:** Research instrument — not a novelty claim  
**Date:** 2026-08-25  
**Review basis:** Primary/authoritative sources located in the 2026-08-25 landscape review

## Purpose

This matrix separates established capabilities from candidate distinctions. A row marked `candidate distinction` is a hypothesis requiring further source-level review and empirical or implementation evidence.

| Dimension | Established landscape | DGAF formulation | Current classification | Evidence needed |
|---|---|---|---|---|
| Agent orchestration | Multi-agent orchestration is established | Orchestration treated as one component of a governed lifecycle | established + synthesis | Mechanism comparison |
| Governance | AI/agent governance frameworks are established | Governance represented as executable controls and decision gates | partial overlap / candidate distinction | Concrete control comparison |
| Runtime enforcement | Runtime policies and action mediation exist | Governance intended to constrain operational transitions | **established overlap** | Runtime implementation comparison |
| Evaluation | Agent benchmarks and evaluation frameworks exist | Evaluation coupled to governance/evidence state | synthesis hypothesis | Comparative experiment |
| Provenance | Trusted provenance, trace provenance, logging, and replay evidence already exist | Evidence/provenance treated as a first-class claim-support layer | **strong overlap / unresolved distinction** | Schema + lifecycle comparison |
| Epistemic status | Unsupported-claim propagation and assurance are recognized problems | Claim status explicitly linked to governance and evidence requirements | candidate distinction | Prior-art + implementation analysis |
| Repository-operational governance | CI/CD assurance patterns are established | Repository artifacts, validators, gates, and evidence are intended to form one lifecycle | candidate distinction | End-to-end reproducibility study |
| Experimental authorization | Research protocols commonly define prerequisites | DGAF/PDMAL uses explicit authorization boundaries before empirical claims | synthesis / candidate distinction | Protocol comparison |
| System-level integration | Recent surveys explicitly seek unified, lifecycle-aware views of architecture, evaluation, governance, and trust | DGAF proposes an operational lifecycle joining these concerns with claim/evidence state | **candidate synthesis; not yet novel** | Full comparative architecture study |

## Source-level adjudication — 2026-08-25

### 1. Trace-based assurance

Paduraru, Bouruc, and Stefanescu's 2026 trace-based assurance framework explicitly combines agentic orchestration, machine-checkable contracts, deterministic replay, stress testing, fault injection, runtime governance, action mediation, and reproducible metrics. citeturn0search1turn0search4

**DGAF implication:** These mechanisms cannot be presented as individually novel DGAF inventions. Any contribution claim must focus on a demonstrable difference in integration, semantics, lifecycle, or implementation.

### 2. Runtime governance and trusted provenance

Mazzocchetti's 2026 Aegis work explicitly combines runtime action-boundary governance, trusted provenance, fail-closed execution, policy state, and governed authorization. Its reported evaluation is sandbox-bounded and itself avoids a general safety claim. citeturn0academia31turn0search0

**DGAF implication:** Runtime governance, trusted provenance, and fail-closed semantics are established overlap areas. DGAF should not claim these concepts as uniquely originating here.

### 3. Governance-to-runtime translation

Koch's 2026 work explicitly separates governance objectives, technical controls, runtime guardrails, and assurance evidence, providing a layered translation method from governance norms to executable controls. citeturn0academia33

**DGAF implication:** The governance-to-control translation problem is independently documented. DGAF's possible distinction must therefore reside elsewhere, if anywhere.

### 4. Proof-carrying agent actions

Wang's 2026 Proof-Carrying Agent Actions work describes portable action certificates, pre-action admissibility, approval, outcome closure, runtime receipts, provenance, and replay-ready proof across heterogeneous runtimes. citeturn0academia34

**DGAF implication:** Evidence-bearing action governance and provenance are active research territory. A DGAF claim around evidence-carrying operational decisions requires explicit mechanism-level differentiation.

### 5. Broader agentic-AI evaluation/governance landscape

Recent surveys explicitly organize agentic AI across architecture, interaction, explainability, security/safety, evaluation, governance, trustworthiness, and lifecycle-aware assessment. citeturn0search3turn0search5

**DGAF implication:** The broad integrated problem statement is not itself novel. The publication must identify a narrower, testable system contribution.

## Current contribution hypothesis

> DGAF may provide a distinctive integration in which orchestration, executable governance, evaluation, provenance, and explicit claim/evidence status are treated as one operational lifecycle.

This is a **hypothesis**, not an established novelty claim.

The strongest remaining candidate distinction is therefore **the explicit coupling of epistemic claim state to operational governance and repository-level evidence lifecycle**, rather than governance, runtime mediation, provenance, orchestration, or evaluation individually.

## Falsifiable comparative hypotheses

### H1 — Evidence-lifecycle coupling

**Claim:** A DGAF-style lifecycle that couples claim status, evidence requirements, governance gates, and repository artifacts can detect or prevent evidence-state violations that a governance-only baseline does not detect.

**Test requirement:** Define equivalent governance policies with and without claim/evidence-state coupling; measure detection of seeded evidence-state violations.

### H2 — Operational reproducibility

**Claim:** The DGAF artifact/gate model can reproduce governance decisions from versioned evidence with less ambiguity than an otherwise equivalent trace/log-only baseline.

**Test requirement:** Blind independent reconstruction of decisions from archived artifacts; measure decision agreement, missing evidence, and provenance ambiguity.

### H3 — System-level integration cost

**Claim:** Coupling governance and evidence state may improve auditability but impose measurable implementation and execution overhead.

**Test requirement:** Compare baseline and DGAF configurations on setup complexity, runtime overhead, artifact volume, and adjudication effort.

These are research hypotheses. They are not evidence of efficacy until tested.

## Prohibited claims at current evidence state

- DGAF is the first framework of its kind.
- DGAF uniquely solves agent governance.
- DGAF invented runtime governance, provenance, trace assurance, or action mediation.
- DGAF eliminates drift or hallucination.
- DGAF is empirically superior to existing approaches.
- PDMAL has demonstrated efficacy.

The PDMAL empirical state remains pre-freeze / unauthorized with empirical N = 0.

## Adjudication categories

Each future comparison should classify a DGAF mechanism as one of:

1. **Established** — substantially present in prior work.
2. **Adapted** — an existing mechanism applied or reformulated for DGAF.
3. **Synthesized** — known mechanisms integrated into a new system-level arrangement.
4. **Independently formulated** — a mechanism not located in the reviewed prior art, subject to continued search.
5. **Unresolved** — insufficient evidence to classify.

## Publication rule

A contribution claim becomes publication-ready only when its source evidence, implementation evidence, scope, limitations, and contradictory evidence have been recorded. Absence of a discovered prior source is not proof of novelty.
