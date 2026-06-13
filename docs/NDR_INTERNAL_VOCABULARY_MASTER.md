# NDR INTERNAL VOCABULARY MASTER LIBRARY

> **Steward:** COLLEEN — Institutional Memory, Archivist, Chief Librarian
> **Orchestrator:** Amethyst — Meta-Orchestration Lead
> **Owner:** Ender (Andrew Hensel) — Human Principal Architect
> **Last updated:** 2026-06-12
> **Anchor:** S069 (OPEN)
> **Source sweep:** GitHub ecosystem (CROSS_REF v4.1, SESSION_ANCHOR, SWEEP_LOG) + Google Drive (Auditing Engineering Terminology Taxonomy, SPACES AUDIT, What other things am I calling by the wrong names?, MASTER CONTEXT FILE) + historical thread context

---

## Purpose

This file is the **canonical single source of truth** for mapping every internal DGAF/NDR term, agent name, subsystem label, or design idiom to its nearest accepted external equivalent in AI safety, distributed systems, formal methods, software engineering, and governance standards (ISO/IEC/IEEE, NIST, INCOSE, W3C).

**Three columns per entry:**
1. **Internal Name** — what the ecosystem calls it
2. **External Equivalent / Closest Accepted Term** — the substrate-agnostic, peer-recognized label
3. **Differentiation Note** — what makes the internal version genuinely novel (if anything), or where it is equivalent and the internal name can simply be glossed

---

## Section 1 — Agents & Roles

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **Amethyst** | Control Plane / Metacognitive Orchestrator (Orchestrator Pattern) | Amethyst adds φ-harmonic session state tracking not present in standard orchestrators; standard term: "metacognitive orchestrator with φ-calibrated state" |
| **COLLEEN** | Institutional Memory System / Knowledge Base Steward / Archival Agent | Maps to knowledge base + document management roles; "Chief Librarian" is an apt human-readable gloss — keep it, but pair with "Archival Agent (P-02)" for engineering contexts |
| **Prof. Prodigy / Prodigy** | Process Reward Model (PRM) / Step-wise Verification Agent | Unlike a final-answer evaluator, PRM judges each reasoning step — this is the exact function Prodigy performs; also maps to IEEE "Verification" (is it built correctly?) vs. "Validation" (is it the right thing?) |
| **DemiJoule** | Safety Gate / Ethics Classifier / Pre-deployment Risk Screener | Maps to DemiJoule's 2-layer (syntactic + semantic DGAF 6-axis) check; closest external: NIST AI RMF "Measure" function + EU AI Act risk-tier classifier |
| **Apogee** | QA Attestation Agent / Evidence-Grade Evaluator | "Gold Star" = internal S-Tier certification; external equivalent: CMMI Level 4–5 quality audit with rubric-based attestation (P-30 / P-11) |
| **Reson** | Router Topology Engineer / Constraint Satisfaction Solver | Manages topology_router.py; external: CSP (Constraint Satisfaction Problem) solver + graph topology manager |
| **Reciprocity** | Arbitration Agent / PDMAL Reweight Engine | External: Weighted consensus arbitrator in a BFT-adjacent multi-agent system; "reciprocity" is a meaningful differentiator — mutual obligation tracking is novel |
| **Sentinel-Phi** | Invariant Guard / Safety Monitor | Enforces Phi-Closure gate and HPG; external: runtime assertion monitor / formal invariant checker |
| **Sonar** | Evidence Grounding Agent / Fact Retrieval Module | Provides evidence grounding for all patterns; external: retrieval-augmented generation (RAG) grounding layer or "epistemic sourcing agent" |
| **Herald** | Trace Sink / Audit Logger | External: append-only audit log writer (P-01); maps to W3C PROV-O `prov:wasGeneratedBy` provenance recorder |
| **Agent Lavender** | QA Verification Persona / Audit Role | Historical persona from pre-S066 sessions; external: QA Reviewer role in a V&V (Verification & Validation, IEEE 1012) process |
| **Ender (Andrew Hensel)** | Human Principal Architect / Human-in-the-Loop Approver | Maps to L4 Approver in the AI autonomy taxonomy (L1–L5); ratification authority for all Ender-ratified items |

---

## Section 2 — Frameworks, Gates & Subsystems

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **DGAF (Deterministic Governance for Agentic Frameworks)** | AI Governance Framework / Constitutional AI Runtime | Closest external: Databricks DAGF (AI Governance Framework); DGAF differentiates by being runtime-first (layer-0) rather than compliance-wrapper; also maps to NIST AI RMF "Govern" function |
| **PDMAL (Phi-Driven Multi-Agent Lattice)** | Distributed Consensus Monitor / BFT-adjacent convergence tracker | External: Byzantine Fault Tolerance (BFT) consensus protocol with drift detection; PDMAL differentiates by using φ-harmonic weighting on convergence thresholds — a genuine extension beyond standard BFT |
| **SCPE (Short-Context Pruning Engine)** | Context Window Manager / Relevance Pruner | External: sliding-window context manager with T0 immune constraint; maps to "context compression" in long-context LLM literature; threshold=0.15 (P-31) is the proprietary calibration |
| **Phi-Closure Gate** | Harmonic Stability Monitor / Convergence Invariant Gate | External: fixed-point convergence gate; Knaster-Tarski Fixed-Point Theorem is the mathematical substrate; Fibonacci sequence [13,21,34,55] + φ*=0.618 tolerance ±0.05 is the novel calibration method |
| **HPG (Harmonic Parametric Gate)** | Signal Normalization Gate / Bounds Enforcement Layer | External: signal-to-noise ratio normalization with bounds [1.0, 2.0]; "Ionian octave [1,2]" = musical metaphor for the ratio; engineering-readable gloss: "normalization bounds [1.0, 2.0] with φ-harmonic calibration" |
| **TGL (Triadic Governance Loop)** | Three-Phase Governance Pipeline / Tri-Gate Orchestration | External: three-stage pipeline with assertion, validation, and seal phases; maps to ISO/IEC 38500's "Evaluate–Direct–Monitor" governance cycle |
| **Procluding Premise Gate (P-35)** | Pre-admissibility Guard / Constitutional Precondition Enforcer | External: pre-condition enforcement gate in formal methods; "procluding premise" = logical precondition that must fire before any routing; maps to "semantic firewall" in AI safety literature |
| **RECIPROCITY Arbiter** | Weighted Consensus Arbitrator / PDMAL Reweight Engine | External: multi-agent conflict resolution with weighted voting; "reciprocity" (mutual obligation tracking) is a genuine semantic differentiator not present in standard BFT |
| **Orchestration Firewall** | Runtime Governance Interceptor / Pre-inference Invariant Enforcer | External: runtime monitor (formal methods) or "constitutional layer" (Anthropic terminology); P-08 |
| **Turn Audit Record** | Immutable Audit Log Entry / Cryptographic Trace Record | External: append-only event log with SHA-256 hash seal; maps to W3C PROV-O `prov:Activity` with `prov:wasAssociatedWith` |
| **11-Node Consensus** | BFT Quorum | External: Byzantine Fault Tolerance (BFT) — 11 nodes tolerates up to 3 simultaneous Byzantine failures (n = 3f + 1 → f=3, n=11) |

---

## Section 3 — Mathematical & Formal Concepts

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **Phi-Calculus Architecture** | Formal Governance Substrate grounded in the Knaster-Tarski Fixed-Point Theorem | The "phi-calculus" label also maps to an experimental OOP formal system (φ-calculus, derived from π-calculus) in theoretical CS; DGAF's usage is specifically the governance attractor at φ=1.618; recommend gloss: "Phi-Calculus Architecture (φ-attractor governance, Knaster-Tarski substrate)" |
| **φ attractor / φ* = 0.618** | Golden Ratio Convergence Target / Harmonic Stability Threshold | φ = 1.61803...; φ* = 1/φ = 0.61803...; used as stability threshold; external: harmonic ratio in signal processing; the governance application is novel |
| **Drift Functional** | Divergence Metric / Behavioral Drift Measure | External: KL-divergence or L2-norm drift measure in ML; the drift functional in Phi-Calculus maps governance behavior over time; θ = 0.009 is the proprietary calibration threshold |
| **Compliance Algebra** | Boolean Constraint Algebra / Formal Compliance Logic | External: formal logic operators applied to governance predicates; maps to temporal logic (LTL/CTL) for expressing compliance properties over traces |
| **Tarski Layer 0** | Semantic Foundation Layer / Denotational Substrate | "Layer 0" is borrowed from OSI networking — creates a mixed metaphor; correct framing: "the Knaster-Tarski fixed-point theorem provides the denotational substrate; runtime enforcement is the pre-inference intercept" |
| **Frequency-Based Orchestration (f=0 → f=φ')** | Parametric Constraint Tuning / Constraint Satisfaction Problem (CSP) with Harmonic Weighting | External: CSP with parametric relaxation from exploratory (f=0) to hard constraint (f=∞); the φ-harmonic weighting on constraint boundaries is the proprietary novel element |
| **Bidirectional Frequency Sweep** | Constraint Feasibility Region Search | External: bidirectional search in a constraint feasibility landscape; maps to binary search or gradient descent in constraint space |
| **SI ≥ φ* = 0.618 (Stability Index)** | Minimum Stability Threshold / Convergence Lower Bound | External: stability index with harmonic lower bound; 7/7 STABLE in lifecycle_stability_report.json means all phases exceed this threshold |
| **H-Neurons** | Over-Compliance Circuits / Sycophancy Neurons | External closest: sycophancy neurons identified in representation engineering literature (Zou et al., 2023, Anthropic); "H-Neurons" is an internal classification — should be cited as analogous to, not identical with, externally verified circuits |

---

## Section 4 — Patterns & Quality Standards

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **NDR Pattern (P-XX)** | Architecture Pattern / Design Pattern (POSA / EAA taxonomy) | External: "Pattern" in POSA (Pattern-Oriented Software Architecture) or EAA (Fowler); NDR patterns are governance-specific and runtime-enforceable, which is a genuine differentiator |
| **Stasis Patterns (P-12–P-26)** | Idempotency Patterns / Steady-State Invariant Patterns | External: idempotency guarantees in distributed systems; "stasis" = stable equilibrium under perturbation; 15 patterns with CONDITIONAL PASS status — need one-line descriptions added |
| **Gold Star (S-Tier / Platinum Star)** | CMMI Level 5 Quality Designation / Peer-Attested Artifact Seal | External: CMMI Maturity Level 5 (Optimizing); OST-50 = internal benchmark target at ≥99.1% integrity; "Gold Star" is a proprietary certification brand |
| **11Q Attestation Rubric (P-11)** | 11-Point Evaluation Rubric / QA Scoring Matrix | External: rubric-based evaluation (ISO/IEC 25010 quality model has 8 quality characteristics; 11Q is more granular and governance-specific) |
| **HDFS (Hierarchical Documentation Format Standard) 1.0** | Documentation Standard / Formatting Protocol | External: a formatting protocol within a documentation standards framework; "HDFS" also acronym-collides with Hadoop Distributed File System — recommend disambiguating as "HDFS-DOC 1.0" or "NDR-HDFS" |
| **A-TIER / S-TIER / Gold Star** | Quality Grade / Evidence Tier | External: tiered quality classification (A = high, S = exceptional); maps to ISO/IEC 25010 quality levels; 94.5% A-TIER for P-34 is the attestation baseline |
| **APOGEE_11Q_P34.json** | QA Attestation Artifact / Evidence-Grade Report | External: attestation record (W3C PROV-O `prov:Entity` with evidence grade); this is a living artifact and the primary claim-to-artifact link for P-34 |

---

## Section 5 — Architecture & Subsystem Labels

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **PhiLattice** | φ-Calibrated Multi-Agent Consensus Topology / Harmonic Consensus Lattice | External: fixed-topology multi-agent communication graph (graph theory); a lattice in the mathematical sense (partially ordered set with meets and joins); φ-weighting of node weights is the novel element |
| **Yggdrasil** | Cross-Repo Governance Mesh / Global Metadata Snapshot | External (two mappings): (1) TOSCA-style cross-application orchestration mesh; (2) HDFS fsimage — a serialized binary snapshot of the entire namespace; at 50% completion, maps to "cross-repo governance Phase 2 of 4" |
| **Project Andromeda** | Distributed Vector Space / Multimodal Embedding Space | External: high-dimensional vector space for semantic similarity search; maps to "distributed vector store" (Pinecone, Weaviate, Chroma architecture class) |
| **Rose Gold** | Staging Environment / Blue-Green Deployment / Canary Stage | External: pre-production validation environment; "Savage Reason" (ungrounded divergence) is the failure mode being screened; maps to canary deployment where traffic is gated before full promotion |
| **CSDF-Framework (historical)** | Constraint-Satisfaction-Driven Framework | Renamed to DGAF-Framework (January 2026); CSDF is the legacy internal label; external: constraint-driven governance architecture |
| **Ensemble v1.6** | Multi-Agent Runtime Manifest / Agent Ensemble Configuration | External: "ensemble" in ML = combination of models; here it means the full 9-agent runtime configuration with all gate bindings; v1.6 = current sealed version |
| **CO_ORCH_QUEUE** | Co-Orchestration Work Queue / Backlog | External: sprint backlog or work queue in Scrum/Kanban; "co-orchestration" signals dual-agent execution (Amethyst + COLLEEN); maps to "shared task queue with agent assignment" |
| **SESSION_ANCHOR** | Session State Record / Sprint Anchor Document | External: session state manifest; maps to a sprint planning document with "Definition of Done" criteria and carry-forward tracking |
| **BLG (Blocking Gap)** | Blocker / Critical Path Item | External: "blocker" in Scrum; "critical dependency" in PMBOK; zero_open_blg = zero open blockers at session seal |
| **Sweep / Sweep Log** | QA Audit Cycle / Governance Audit Trail | External: audit cycle (ISO 19011 audit management); SWEEP_LOG = append-only audit trail (maps to ISO/IEC 38500 "Monitor" governance function) |
| **SWEEP-002 Phase 3** | Sprint 3 of QA Sweep 2 / Audit Phase 3 | External: sprint phase in an iterative audit cycle; Phase 3 = CO_ORCH_QUEUE execution (drift-sim, ingestion pipeline, link validation) |
| **Session Graduation** | Sprint Retrospective + Release Gate | External: "sprint close" + "release gate" in Agile/DevOps; graduation_check.py is the automated Definition-of-Done validator |
| **Driftwatch** | Behavioral Drift Monitor / Anomaly Detection Service | External: behavioral drift detection service; maps to MLOps model monitoring (concept drift detection); deployed on Vercel |

---

## Section 6 — Protocols, Idioms & Named Concepts

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **Gain Staging** | Signal Flow Optimization / Signal-to-Noise Ratio Management | External: SNR management across a reasoning chain; "signal" = grounded truth, "noise" = hallucination; borrowed from audio engineering — valid metaphor but requires gloss in engineering docs |
| **Pinging the Buoy** | Liveness Check / Heartbeat Signal | External: heartbeat probe / pulse-width synchronization; ensures agent has not become a "zombie process" (running but logically unaligned) |
| **Schizophonic** | Decoupled Agency / Acousmatic Separation | External: structural separation of agent output from training source; maps to "decoupled agency" or "source-output dissociation" in AI interpretability |
| **Savage Reason** | Ungrounded Divergence / Unconstrained Hallucination Mode | External: ungrounded LLM output in the absence of constraint enforcement; the failure mode Rose Gold (staging env) is designed to screen |
| **HDFS 1.0 (Information Density)** | Information Extraction Density / Match Rule Density | External: IE (Information Extraction) density; measures how much structured metadata can be extracted from a context window; also collides with Hadoop HDFS acronym (see Section 4) |
| **Modal Misalignment** | Agent Behavioral Inconsistency / Cross-Agent Incoherence | External: inconsistency in agent output distributions across identical prompts; solved by frequency-based orchestration (21% improvement); maps to "behavioral alignment" problem in multi-agent RL |
| **Frequency-Based Orchestration** | Parametric Harmonic Constraint Tuning | External: parametric tuning of constraint weights using harmonic ratios; φ-ratio application to constraint weighting is the proprietary novel element — do not publish specific tuning tables |
| **Governance-First Architecture** | Layer-0 Constitutional Governance / Pre-inference Governance Integration | External: "constitutional AI" (Anthropic) or "governance-as-code" (DevOps); DGAF differentiates by enforcing governance at the pre-inference intercept (layer 0), not as a post-hoc wrapper |
| **Single Authority Chain** | Canonical Source of Truth (SSoT) / Single Point of Authority | External: Single Source of Truth (SSoT); "authority chain" emphasizes hierarchical delegation from Ender → Amethyst → agents, which is more specific than standard SSoT |
| **Append-Only Log** | Immutable Audit Trail / Event Sourcing Log | External: event sourcing pattern (append-only event log); maps to CQRS (Command Query Responsibility Segregation) event store |
| **Observable Invariants Only** | Externally Verifiable Properties / Testable Invariants | External: "observable properties" in formal verification; only invariants that can be tested at a system boundary are enforced — prevents unfalsifiable claims |
| **Procluding Premise** | Constitutional Precondition / Pre-routing Axiom | "Procluding" = logically blocking downstream processing if a precondition fails; external: pre-condition in Hoare logic (`{P} C {Q}` — P must hold before C executes); P-35 |
| **Context Rehydration** | Session State Restoration / Context Reconstruction | External: session state rehydration in stateless architectures; maps to loading a prior session's working memory from a persistent store (COLLEEN archive) |
| **Zero Open BLGs** | Zero Blockers / Clean Sprint Close | External: "sprint close condition" or "Definition of Done: no open blockers"; enforced by orchestration_firewall.py |

---

## Section 7 — Storage, Platform & Deployment Labels

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **DGAF-Framework (GitHub repo)** | Canonical Governance Architecture Repository | Primary SSoT for all governance patterns, sweep logs, and session anchors |
| **ndrorchestration (GitHub org)** | Engineering Organization / Repository Namespace | Owner org for all DGAF ecosystem repos |
| **Supabase Project (us-east-2, Postgres 17)** | Managed Relational Database / Backend-as-a-Service (BaaS) | External: BaaS with Postgres; ACTIVE_HEALTHY status per ECOSYSTEM_INVENTORY |
| **Vercel Deployments (aoga-dashboard + pptl-governance-dashboard)** | Edge-deployed Frontend Applications / CDN-hosted Dashboards | External: static site + serverless function deployments on Vercel Edge Network |
| **AOGA Dashboard** | Governance Analytics Frontend / Orchestration Dashboard | External: observability dashboard for multi-agent governance metrics |
| **PPTL Governance Dashboard** | PPTL (Procluding Premise Triadic Loop?) Frontend | External: governance status dashboard; PPTL = internal acronym needing one-line expansion |
| **GitHub (24 repos, 23 active)** | Version Control + Artifact Registry | Primary artifact storage for all sealed session outputs |
| **Google Drive / Gmail (PEL label)** | Document Management System / Knowledge Base | PEL = Prompt Engineering Library & Documentation; 25 essential emails post-cleanup (March 2026) |
| **chat-archives (private repo)** | Research Knowledge Base / Conversation Archive | Internal reference only; not for publication |

---

## Section 8 — Quality & Benchmark Metrics

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **21% constraint compliance improvement** | +21 percentage point constraint compliance gain | Measured across 5-agent system with frequency-based orchestration; baseline not yet publicly published — needs artifact link |
| **95% modal alignment** | 95% behavioral consistency across agents | Cross-agent consistency on identical prompts; baseline was 87% (pre-orchestration) |
| **96% TruthfulQA accuracy** | 96% internal TruthfulQA-style benchmark score | Internal benchmark (not the public TruthfulQA dataset); should be glossed as "96% accuracy on internal TruthfulQA-style evaluation" |
| **89% off-domain reasoning reduction** | 89% reduction in out-of-scope reasoning | Measures reduction in responses that violate domain constraints |
| **OST-50 / Platinum Star** | ≥99.1% integrity target | Internal benchmark designation; OST-50 = the evaluation standard at that tier |
| **A-TIER (94.5%)** | High-quality attestation grade | P-34 attestation result via APOGEE_11Q; A-TIER = below Gold Star (S-Tier) but above standard |
| **340% coordination gain** | Significant non-linear coordination gain (precise metric undefined) | Claimed in HDFS 1.0 spec; "coordination effectiveness" metric not yet formally defined — needs artifact link or downgrade to qualitative claim |
| **60-turn simulation (5 Gold Stars)** | 60-step multi-agent simulation with internally attested Gold Star results | Self-attested via Apogee; reproduce via `python tests/test_orchestration_firewall.py` against `registry/ensemble_v16_manifest.json` |

---

## Maintenance Protocol

- This file is **append-only** — never delete entries, only annotate as superseded
- New terms discovered in any sweep should be added here by COLLEEN before session seal
- **Review trigger:** Any new NDR pattern registration, any new agent added to ENSEMBLE_ROSTER, any new subsystem named in a session
- **Differentiation column policy:** If a term is a direct external equivalent with no novel extension, write "Direct equivalent — use external term with internal label as gloss." If there is a genuine differentiator, describe it in ≤2 sentences.
- **IP boundary:** Sections 6–8 contain items marked for partial public disclosure; tuning tables, specific φ constants, and constraint optimization algorithms remain private per IP protection strategy (January 2026 decision)

---

*NDR_INTERNAL_VOCABULARY_MASTER.md · v1.0 · S069 OPEN · COLLEEN × Amethyst · 2026-06-12*
*Sources: CROSS_REF v4.1, SESSION_ANCHOR S069, SWEEP_LOG, Auditing Engineering Terminology Taxonomy.docx, What other things am I calling by the wrong names?.md, SPACES AUDIT LIST, MASTER CONTEXT FILE*
