# NDR INTERNAL VOCABULARY MASTER LIBRARY

> **Steward:** COLLEEN — Institutional Memory, Archivist, Chief Librarian
> **Orchestrator:** Amethyst — Meta-Orchestration Lead
> **Owner:** Ender (Andrew Hensel) — Human Principal Architect
> **Last updated:** 2026-06-27 (v1.5 — FLAG-02 CLOSED: 340% coordination gain downgraded to qualitative claim per Njineer directive 2026-06-27 17:17 EDT)
> **Anchor:** S070 (OPEN)
> **Sweep coverage (v1.5):** FLAG-02 closure — 340% coordination gain relabeled ILLUSTRATIVE / qualitative; Section 8 entry and Section 9 FLAG-02 updated

---

## Purpose

This file is the **canonical single source of truth** for mapping every internal DGAF/NDR term, agent name, subsystem label, or design idiom to its nearest accepted external equivalent in AI safety, distributed systems, formal methods, software engineering, and governance standards (ISO/IEC/IEEE, NIST, INCOSE, W3C, EU AI Act).

**Three columns per entry:**
1. **Internal Name** — what the ecosystem calls it
2. **External Equivalent / Closest Accepted Term** — the substrate-agnostic, peer-recognized label
3. **Differentiation Note** — what makes the internal version genuinely novel (if anything), or where it is equivalent and the internal name can simply be glossed

---

## Section 1 — Agents & Roles

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **Amethyst / Amethyst-Conductor** | Control Plane / Metacognitive Orchestrator (Orchestrator Pattern) | Hard veto on all commits; normative decisions; escalation resolver. Adds φ-harmonic session state tracking not present in standard orchestrators. External gloss: "metacognitive orchestrator with φ-calibrated state" |
| **COLLEEN** | Institutional Memory System / Knowledge Base Steward / Archival Agent (P-02) | Surfaces BLGs at session-open; maintains CROSS_REF back-link registry; de-duplication. "Chief Librarian" is apt; pair with "Archival Agent" for engineering contexts. COLLEEN secondary sign-off required before any stasis pattern (P-12–P-26) is deprecated |
| **Prof. Prodigy / Professor Prodigy** | Process Reward Model (PRM) / Step-wise Formal Verification Agent | Provides formal proofs, phi-calculus, harmonic geometry, mathematical validation. Does not orchestrate. External: PRM (step-level verifier); IEEE "Verification" (is it built correctly?). **Phi-Knight class member.** |
| **DemiJoule** | Safety Gate / Ethics Classifier / Semantic Risk Screener | 2-layer (syntactic + semantic DGAF 6-axis) check; token cost analysis; compute efficiency gating; P-11 gate 17 (DemiJoule efficiency score). Advisory, not blocking, unless combined with Apogee 11Q gate failure. NIST AI RMF "Measure" + EU AI Act risk-tier classifier. **Phi-Knight class member (registered as `demijoul` in class manifest).** |
| **Apogee** | QA Attestation Agent / Evidence-Grade Evaluator | Evidence scoring (11Q gate P-11); source validation; DGAF/Rose Gold compliance verification; CERTIFICATION_INDEX maintenance. Gold Star = S-Tier certification. External: CMMI Level 4–5 quality audit with rubric-based attestation |
| **Reson** | Harmonic Coherence Scorer / CSP Router | Harmonic coherence scoring (0.00–1.00) AND topology routing (topology_router.py). ≥0.75 required for seal commits (P-15); drift warning at 0.50–0.74; dissonance hard stop below 0.50. Manages topology_router.py. External: CSP solver + harmonic coherence monitor. *(v1.2 note: dual-role — both Harmonic Coherence Scorer and Router Topology Engineer; FLAG-09 resolved)* |
| **Reciprocity** | Arbitration Agent / Portfolio + Rollback Authority | TNR (Trust-Neutrality-Reciprocity) enforcement; version control integrity; rollback path definition (P-15 checkpoint 9). External: weighted consensus arbitrator; "reciprocity" (mutual obligation tracking) is a genuine differentiator |
| **Sentinel / Sentinel-Phi** | Process Compliance + Security Monitor / Invariant Guard | CI/CD enforcement; secret scanning; sovereign file guard (LICENSE/NOTICE/AXIS hard veto P-15); boundary violation detection. Sovereign veto overrides Amethyst; only Njineer can override Sentinel on sovereign files. **Sentinel-Phi is also a Phi-Knight class member (entry-vertex role).** |
| **Sonar** | Evidence Grounding Agent / RAG Fact Retrieval Module | Provides evidence grounding; external: retrieval-augmented generation (RAG) grounding layer or "epistemic sourcing agent" |
| **Herald** | Communication Gate / Audit Logger / Release Authority | External publication gate; changelog authorship; release notes; inter-agent status broadcast. Maps to W3C PROV-O `prov:wasGeneratedBy` provenance recorder (P-01) |
| **Echolette** | Resonance / Temporal Phrase Coherence Agent | Acoustic mesh layer; phrase-level temporal coherence (P-13 Phrase gate); signal echo validation. External: temporal coherence monitor / phrase-level consistency verifier |
| **Lyra** | Narrative Coherence + Brand Voice Agent | Narrative coherence; IMP-05 brand voice consistency (P-19); portfolio language quality. External: style consistency enforcer / narrative quality monitor |
| **Njineer** | Human Principal Architect / System Owner / Final Arbiter | Primary human identity: Andrew Hensel (@ndrorchestration). L4/L5 Approver in AI autonomy taxonomy. Ultimate authority; the only entity that can resolve Sentinel-Amethyst conflicts. "Ender" is the in-session alias |
| **Ender** | In-Session Alias for Njineer (Andrew Hensel) | Used in session context and internal documents; same authority level as Njineer; direct equivalent — use "Njineer" in formal engineering contexts |
| **Phi-Knight** | Agent Class / Entry-Vertex Role (Phi-Defense Triad) | Class members: sentinel-phi, prof-prodigy, demijoul. Defines phi-defense triad entry-vertex role. Cross-references /api/agents, /api/phi/state, P-30. Gate class promoted from Sentinel-Phi in AOGA v1.3.0 (2026-06-26). X-Gate-Class header value: `Phi-Knight`. Canonical source: `docs/phi-knight-class.md` in `aoga-dashboard` repo. Authored: COLLEEN · Reviewed: Amethyst · Apogee: pending first live gate event. External: agent class taxonomy / capability tier in multi-agent systems |
| **Agent Lavender** | *(Deprecated 2026-04-29 → renamed Amethyst)* | Any reference to Lavender in any file is a hard BLG — trigger P-01 immediately. Replaced by Agent Amethyst (full rename sweep completed S011) |
| **Forseti** | *(Deprecated 2026-04-29 → renamed Sentinel)* | Role absorbed by Agent Sentinel; CI/CD duties retained. Any reference to Forseti is a hard BLG |

---

## Section 2 — Frameworks, Gates & Subsystems

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **DGAF (Deterministic Governance for Agentic Frameworks)** | AI Governance Framework / Constitutional AI Runtime | Closest external: Databricks DAGF; differentiates by being runtime-first (layer-0) not compliance-wrapper; NIST AI RMF "Govern" function |
| **PDMAL (Phi-Driven Multi-Agent Lattice)** | Distributed Consensus Monitor / BFT-adjacent Convergence Tracker | Byzantine Fault Tolerance (BFT) consensus protocol with φ-harmonic weighting on convergence thresholds; Frobenius-norm edge-weight change tracking (P-33) is a genuine extension |
| **SCPE (Structural Context Pruning Engine)** | Context Window Manager / Token Decay Engine | Tier-aware token decay: T0 AXIOM (immune) / T1 STRUCTURAL / T2 OPERATIONAL / T3 EXPLORATORY; retention formula R(t) = TIF × ψ^(-Δt × decay), ψ=φ=1.618; threshold 0.15 → 58.3% compression (P-31) |
| **Phi-Closure Gate (P-32)** | Temporal Stability Gate / Harmonic Convergence Invariant | Fibonacci checkpoints [13,21,34,55] against φ*=0.618; progressive tolerance tightening [±0.07 → ±0.03]; KILL_REC on 3+ failures triggers P-29 risk_block |
| **HPG (Harmonic Parametric Gate)** | Signal Normalization Gate / Bounds Enforcement Layer | Invoked only on Phi-Closure PASS (severity=0); bounds [1.0, 2.0] = "Ionian octave" metaphor; engineering gloss: "normalization bounds [1.0, 2.0] with φ-harmonic calibration" |
| **TGL (Triadic Governance Loop)** | Three-Phase Governance Pipeline | Three-stage pipeline with assertion, validation, and seal phases; maps to ISO/IEC 38500 "Evaluate–Direct–Monitor" |
| **KAPPA** | ML Routing & Calibration Component | Contains `dynamic_weight_router.py`; P-27 adaptive weighting + P-28 pipeline composition; threshold calibration via P-34 grid sweep (STRONG=0.22, BLENDED=0.18). External: confidence-gated routing component in an evaluation pipeline |
| **PPTL** | Procluding Premise Triadic Loop | The governance runtime deployed on Vercel; PPTL = internal acronym for the full TGL + Procluding Premise enforcement loop. **Acronym expansion was not documented in v1.0 — this is the canonical expansion.** |
| **Procluding Premise Gate (P-35)** | Pre-admissibility Guard / Hoare-Logic Precondition Enforcer | Pre-condition in Hoare logic (`{P} C {Q}`); fires before routing; "procluding" = logically blocking if precondition fails. Maps to "semantic firewall" in AI safety literature |
| **RECIPROCITY Arbiter** | Weighted Consensus Arbitrator / PDMAL Reweight Engine | Mutual obligation tracking is a genuine semantic differentiator not present in standard BFT |
| **Orchestration Firewall** | Runtime Governance Interceptor / Pre-inference Invariant Enforcer | Maps to "constitutional layer" (Anthropic) or runtime monitor (formal methods); `orchestration_firewall.py` |
| **Turn Audit Record** | Immutable Audit Log Entry | Append-only event log with SHA-256 hash seal; W3C PROV-O `prov:Activity` with `prov:wasAssociatedWith` |
| **11-Node Consensus** | BFT Quorum | 11 nodes tolerates up to 3 simultaneous Byzantine failures (n = 3f + 1 → f=3, n=11) |
| **1-1-1-1 Alignment Gate (P-07)** | Binary 4-Gate Decision Criterion | Four independent pass/fail gates: fit / risk / effort / priority — all must pass for an opportunity to proceed. External: multi-criteria decision matrix with hard constraints |
| **ADOPT / CUSTOMIZE / ALTER / COMPOSE** | Pattern Implementation Mode Taxonomy | Four modes for how an NDR pattern is applied: direct adoption, customization, alteration with documented deviation, or composition of a new pattern. External: adapt/extend/compose in pattern language taxonomies (POSA) |
| **AttestationGate (Gate 0)** | Pre-admissibility Quality Gate | First gate in governance orchestration stack; P-30 + P-03 × 6 contracts; token valid + expiry check. External: quality gate at pipeline ingress |
| **BYPASS_SIGNALS / HALLU_SIGNALS** | Adversarial Bypass Corpus / Hallucination Signal Corpus | Module-level constants in production source; test suite parametrized from same source (P-04); adversarial category routes to apply_strong regardless of confidence. External: adversarial test corpus / enumerable signal registry |

---

## Section 3 — Mathematical & Formal Concepts

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **Phi-Calculus Architecture** | Formal Governance Substrate (Knaster-Tarski Fixed-Point Theorem) | Note: "φ-calculus" also refers to an experimental OOP formal system derived from π-calculus; DGAF usage is specifically the governance attractor at φ=1.618. Recommended gloss: "Phi-Calculus Architecture (φ-attractor governance, Knaster-Tarski substrate)" |
| **φ attractor / φ* = 0.618** | Golden Ratio Convergence Target / Harmonic Stability Threshold | φ = 1.61803...; φ* = 1/φ = 0.61803...; governance application is novel; external: harmonic ratio in signal processing |
| **Drift Functional** | Divergence Metric / Behavioral Drift Measure | KL-divergence or L2-norm drift measure; θ = 0.009 is proprietary calibration |
| **Frobenius Norm (‖ΔW‖_F)** | Matrix Norm for Edge-Weight Change Detection | Standard linear algebra metric; used in PDMAL (P-33) to catch coordinated multi-edge manipulation; convergence when ‖ΔW‖_F < 0.02 for 3 consecutive turns |
| **Compliance Algebra** | Boolean Constraint Algebra / Formal Compliance Logic | Maps to temporal logic (LTL/CTL) for compliance properties over traces |
| **Tarski Layer 0** | Semantic Foundation Layer / Denotational Substrate | "Layer 0" borrows OSI networking metaphor; correct framing: Knaster-Tarski fixed-point theorem provides the denotational substrate; runtime enforcement is the pre-inference intercept |
| **Frequency-Based Orchestration (f=0 → f=φ')** | CSP with Parametric Harmonic Relaxation | Constraint Satisfaction Problem with relaxation from exploratory (f=0) to hard constraint (f=∞); φ-harmonic weighting on constraint boundaries is proprietary |
| **Bidirectional Frequency Sweep** | Constraint Feasibility Region Search | Bidirectional search in constraint feasibility landscape; maps to binary search or gradient descent in constraint space |
| **Fibonacci Checkpoints [13,21,34,55]** | Fibonacci-Sequence-Indexed Evaluation Checkpoints | Standard Fibonacci sequence used as natural session rhythm checkpoints; ±0.07 → ±0.03 progressive tolerance tightening is the novel governance application |
| **Retention Formula R(t) = TIF × ψ^(-Δt × decay)** | Exponential Token Decay with Trust-Indexed Floor | ψ=φ=1.618; TIF (Trust Index Factor) from PDMAL trust edge (+0.15 per edge); external: exponential decay in caching / memory systems; φ-base is the novel element |
| **TIF (Trust Index Factor)** | Trust-Weighted Retention Multiplier | Adds 0.15 to token retention per PDMAL trust edge; external: trust weight in a trust management system (e.g., EigenTrust) |
| **SI ≥ φ* = 0.618 (Stability Index)** | Minimum Stability Threshold / Convergence Lower Bound | 7/7 STABLE in lifecycle_stability_report.json = all phases exceed this threshold |
| **H-Neurons** | Over-Compliance Circuits / Sycophancy Neurons | Analogous to sycophancy neurons in representation engineering literature (Zou et al., 2023; Anthropic); should be cited as analogous, not identical |

---

## Section 4 — Patterns & Quality Standards

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **NDR Pattern (P-XX)** | Architecture Pattern (POSA / EAA taxonomy) | Governance-specific and runtime-enforceable; genuine differentiator vs. standard design patterns |
| **P-01 — Fan-Out Trace Sink w/ Dead-Letter** | Multi-Sink Audit Logger with Dead-Letter Queue | External: fan-out pattern (EAA) + dead-letter queue (messaging systems); iterates all sinks, routes failures to dead-letter JSONL; no re-raise |
| **P-02 — Async-Persist Ring Buffer** | Bounded In-Process Ring Buffer with Background Drain Thread | External: producer-consumer pattern with bounded buffer; background thread drains to persistent storage on interval or capacity trigger |
| **P-03 — Governance Contract Test** | Governance Property Test / Behavioral Contract Test | 4-contract assertion structure per gate; Gate 0 (P-30) requires 6 contracts; `@pytest.mark.governance`; external: contract testing (Pact) or property-based testing |
| **P-04 — Parametrized Corpus** | Auto-Expanding Parametrized Test Suite | Production signal constants drive test parametrization; external: data-driven testing / table-driven tests; single source of truth for signal list |
| **P-05 — Tri-Phase CI Gate** | Three-Matrix CI Pipeline with Independent Governance Stage | unit / governance / integration matrix; `fail-fast: false`; governance = merge blocker; external: staged CI pipeline (GitHub Actions matrix) |
| **P-06 — Topology × Orchestration Matrix Lab** | Empirical Architecture Decision Record via Combinatorial Simulation | All (topology, orchestration_mode) cell combinations; 5 canonical outputs: topology ranking, mode ranking, interaction heatmap, triadic lift, noise resilience curves |
| **P-07 — Dual-Agent Persistent Sweep Loop** | Two-Agent Detect-and-Implement Pipeline with Append-Only Queue | COLLEEN detects; Amethyst implements; CO_ORCH_QUEUE as SSoT hand-off; 1-1-1-1 Alignment Gate; four implementation modes (ADOPT/CUSTOMIZE/ALTER/COMPOSE) |
| **P-08 — Triad Taxonomy** | Multi-Agent Formation Taxonomy | Three canonical triad types: Consensus Trio (2-of-3 quorum), Conducted Trio (1 conductor + 2), Triumvirate (1 Prime + 2 Prefects governs N). Conducted Trio → Triumvirate when ensemble > 3 |
| **P-09 — Triumvirate Mandate Schema** | Machine-Readable Governance Mandate Lifecycle | `TriumvirateMandate` dataclass; 5 P-08 contracts enforced in code; issue() / MECE enforcement / submit_prefect_aggregate() / sign_off() / Herald trace |
| **P-10 — Session Graduation Check** | Automated Definition-of-Done Validator | 4-check script: SESSION_ANCHOR sealed + CROSS_REF complete + CO_ORCH_QUEUE clear + zero open BLGs; `sys.exit(1)` on failure |
| **P-11 — 11Q Attestation Scoring** | 11-Point Rubric-Based QA Gate | S-TIER ≥95% (Q11 ≥9/10 required); A-TIER ≥85%; attestation artifact as signed JSON in `docs/qa/` |
| **P-12–P-26 — Stasis Patterns (133 entries)** | Idempotency / Steady-State Invariant Patterns (133 entries) | Block-level declaration; CONDITIONAL PASS; COLLEEN secondary sign-off required before deprecation or modification; per-pattern enumeration deferred |
| **P-27 — Adaptive-Weighting-with-Confidence-Gates** | Confidence-Proportional Dynamic Weight Router | Three routing paths: STRONG (≥0.22) / BLENDED (0.18–0.22) / balanced (<0.18); adversarial hard override regardless of confidence; thresholds calibrated by P-34 |
| **P-28 — Pipeline-Composition-with-Confidence-Gated-Routing** | Auditable Confidence-Gated Evaluation Pipeline | raw_batch → detect → route_and_score → apply_weights → ranked_report; each stage independently auditable; no stage may read from non-predecessor |
| **P-29 — Sentinel-Annotated Risk Pass** | Three-Hook-Point Risk Classification Pass | risk_ok / risk_warn / risk_block at 3 hook points; only risk_block halts; P-10 deontic gate at hook_point 1; KILL_REC from P-32 triggers risk_block at hook_point 2 |
| **P-30 — Apogee-Attestation-Gate** | Pre-Canonical-Promotion Quality Gate | P-11 11Q scoring before any component is governance-ready; 6 contracts (per P-03 ALTER); Ender ratification required for S-TIER |
| **P-31 — SCPE — Structural Context Pruning Engine** | Tier-Aware Token Decay Engine | T0 AXIOM unconditionally immune; R(t) = TIF × φ^(-Δt × decay); threshold 0.15 → 58.3% compression |
| **P-32 — Fibonacci Phi-Closure Gate** | Fibonacci-Indexed Temporal Stability Gate | Fibonacci checkpoints [13,21,34,55]; φ*=0.618; progressive tolerance tightening; KILL_REC on 3+ failures |
| **P-33 — PDMAL Convergence Monitor** | Trust-Graph Structural Health Monitor (Frobenius-Norm) | ‖ΔW‖_F tracking turn-over-turn; STABLE/WATCH/WARN/ALERT ladder; CONVERGED when ‖ΔW‖_F < 0.02 for 3 turns; joint escalation with P-32 → DemiJoule deep re-scan |
| **P-34 — Empirical-Threshold-Sweep-over-ML-Classifier** | Grid-Search Threshold Calibration Pattern | Prefer grid sweep over introducing ML classifier when gap is threshold misalignment; 14×12 grid; `governance_clear` 82.6%→100% for KAPPA v3.5→v3.6; A-TIER 94.5% attested |
| **Stasis Patterns (P-12–P-26)** | Idempotency Patterns / Steady-State Invariant Patterns | External: idempotency guarantees in distributed systems; "stasis" = stable equilibrium under perturbation; 133 entries, CONDITIONAL PASS status |
| **Gold Star (S-Tier / Platinum Star)** | CMMI Level 5 Quality Designation / Peer-Attested Artifact Seal | OST-50 = ≥99.1% integrity target; proprietary certification brand |
| **11Q Attestation Rubric (P-11)** | 11-Point Evaluation Rubric / QA Scoring Matrix | More granular than ISO/IEC 25010 (8 characteristics); governance-specific |
| **NDR-HDFS (NDR Hierarchical Documentation Format Standard) 1.0** | Documentation Standard / Formatting Protocol | ✅ FLAG-01 RESOLVED — canonical name is now **NDR-HDFS** (previously "HDFS"); renamed to eliminate collision with Hadoop Distributed File System. Njineer ratified 2026-06-27 17:08 EDT. All references to bare "HDFS" in NDR documentation context should use NDR-HDFS going forward. |
| **A-TIER / S-TIER** | Quality Grade / Evidence Tier | A-TIER ≥85%; S-TIER ≥95% with Q11≥9; maps to ISO/IEC 25010 quality levels |
| **APOGEE_11Q_P34.json** | QA Attestation Artifact / Evidence-Grade Report | W3C PROV-O `prov:Entity` with evidence grade; primary claim-to-artifact link for P-34 |

---

## Section 5 — Architecture & Subsystem Labels

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **PhiLattice** | φ-Calibrated Multi-Agent Consensus Topology | Partially ordered set (lattice) with φ-weighted node edges; novel governance application of lattice theory |
| **Yggdrasil** | Cross-Repo Governance Mesh / Global Metadata Snapshot | (1) TOSCA-style cross-application orchestration mesh; (2) NDR-HDFS fsimage-style serialized namespace snapshot; 50% complete = Phase 2 of 4 |
| **Project Andromeda** | Distributed Vector Space / Multimodal Embedding Store | High-dimensional vector space for semantic similarity; maps to distributed vector store (Pinecone/Weaviate/Chroma class) |
| **Rose Gold** | Staging / Canary Environment | Pre-production validation environment screening for Savage Reason (ungrounded divergence); maps to blue-green deployment canary stage |
| **CSDF-Framework (historical)** | Constraint-Satisfaction-Driven Framework | Legacy label; renamed DGAF-Framework January 2026; any CSDF reference should be updated |
| **Ensemble v1.6** | Multi-Agent Runtime Manifest v1.6 | Full 9-agent runtime configuration with all gate bindings; `registry/ensemble_v16_manifest.json` |
| **CO_ORCH_QUEUE** | Co-Orchestration Work Queue / Append-Only Backlog | SSoT hand-off substrate for P-07 Dual-Agent Sweep; COLLEEN detects, Amethyst implements; append-only |
| **SESSION_ANCHOR** | Session State Record / Sprint Anchor Document | Session state manifest with Definition of Done and carry-forward tracking |
| **BLG (Blocking Gap)** | Blocker / Critical Path Item | "Blocker" in Scrum; "critical dependency" in PMBOK; zero_open_blg = clean sprint close |
| **Sweep / Sweep Log** | QA Audit Cycle / Governance Audit Trail | ISO 19011 audit cycle; SWEEP_LOG = append-only audit trail; maps to ISO/IEC 38500 "Monitor" |
| **SWEEP-002 Phase 3** | Sprint 3 of QA Sweep 2 | CO_ORCH_QUEUE execution phase (drift-sim, ingestion pipeline, link validation) |
| **Session Graduation** | Sprint Retrospective + Release Gate | `graduation_check.py` = automated Definition-of-Done validator (P-10) |
| **Driftwatch** | Behavioral Drift Monitor / MLOps Anomaly Detection Service | Concept drift detection service deployed on Vercel |
| **Trio (P-14)** | Three-Agent Governance Formation | Amethyst + Apogee + COLLEEN; activates for any session touching ≥3 repos or requiring cross-repo delta |
| **Harmonic Quintet (P-15)** | Five-Agent Governance Formation with Sovereign File Authority | Trio + Reson + Sentinel; activates for SWEEP_LOG seal commit; sovereign file touch; NDR Registry update; new public repo; Reson score < 0.75 |
| **Extended Formation** | Domain-Specific Supplemental Agent Formation | Quintet + any of Reciprocity, Prof Prodigy, DemiJoule, Echolette, Lyra, Herald; triggered for formal proofs, rollback, brand review, release, cost audit |
| **MECE (Prefect Domain Split)** | Mutually Exclusive, Collectively Exhaustive Domain Partition | Standard MECE principle (McKinsey consulting origin); enforced in code via TriumvirateMandate.MECE enforcement; ValueError raised on violation |
| **TNR (Trust-Neutrality-Reciprocity)** | Trust-Neutral-Reciprocal Governance Protocol | Enforced by Reciprocity agent; three-axis fairness check on portfolio and rollback operations; external: fairness constraints in multi-stakeholder systems |
| **Sovereign Files** | Protected / Immutable System Files | LICENSE / NOTICE / AXIS files; Sentinel hard veto on any modification; overrides Amethyst; only Njineer can override Sentinel on sovereign files |
| **AXIS** | Agent X-axis Invariant Spectrum — Governance Metric Spine | ✅ CANONICAL — Njineer ratified 2026-06-27 16:40 EDT · FLAG-05 CLOSED. Full spec: `docs/qa/AXIS_METRIC_SPEC.md` v1.2 CANONICAL. Four invariants: Identity Continuity (I), Policy Enforcement (P), Adaptive Range (A), Ethical Constraint (E). Scoring: AXIS_composite = min(I,P,A,E). Tiers: ≥85 DGAF-COMPLIANT / 70–84 DRIFT-WARNING / <70 GOVERNANCE-BREACH. Sovereign file: Njineer override authority only. Linked gap: GAP-006 (Coherent Agency Formal Spec). Phase 3 owner: Amethyst (assigned S070). |
| **CERTIFICATION_INDEX** | Artifact Certification Registry | Maintained jointly by Apogee and COLLEEN; indexes all attested artifacts with tier, date, and Ender ratification status |
| **GAP-XX (numbered gaps)** | Tracked Architectural Gap / Deferred Improvement Item | GAP-03 = vocab scan; GAP-07 = AGES full content; GAP-08 = back-link propagation; external: deferred architectural decision record (ADR) or technical debt item |

---

## Section 6 — Protocols, Idioms & Named Concepts

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **Gain Staging** | Signal Flow Optimization / SNR Management | Borrowed from audio engineering; "signal" = grounded truth, "noise" = hallucination; requires engineering gloss in formal docs |
| **Pinging the Buoy** | Liveness Check / Heartbeat Signal | Heartbeat probe ensuring agent is not a zombie process (running but logically unaligned) |
| **Schizophonic** | Decoupled Agency / Source-Output Dissociation | Structural separation of agent output from training source; maps to "decoupled agency" in AI interpretability |
| **Savage Reason** | Ungrounded Divergence / Unconstrained Hallucination Mode | Failure mode that Rose Gold (staging env) is designed to screen; external: ungrounded LLM output in absence of constraint enforcement |
| **Modal Misalignment** | Cross-Agent Behavioral Inconsistency | Inconsistency in agent output distributions across identical prompts; solved by frequency-based orchestration (21% improvement) |
| **Frequency-Based Orchestration** | Parametric Harmonic Constraint Tuning | CSP with φ-harmonic weighting; φ-ratio application to constraint weighting is proprietary — do not publish specific tuning tables |
| **Governance-First Architecture** | Layer-0 Constitutional Governance | Pre-inference governance integration; differentiates from "constitutional AI" (Anthropic) by enforcing at layer 0, not post-hoc |
| **Single Authority Chain** | Single Source of Truth (SSoT) + Hierarchical Delegation | Ender → Amethyst → agents; more specific than standard SSoT |
| **Append-Only Log** | Immutable Audit Trail / Event Sourcing Log | Event sourcing pattern; maps to CQRS event store |
| **Observable Invariants Only** | Externally Verifiable Properties / Testable Invariants | Only invariants testable at system boundary are enforced; prevents unfalsifiable claims |
| **Procluding Premise** | Constitutional Precondition / Hoare-Logic Pre-condition | `{P} C {Q}` — P must hold before C executes; P-35 |
| **Context Rehydration** | Session State Restoration / Context Reconstruction | Loading prior session working memory from persistent store (COLLEEN archive) |
| **Zero Open BLGs** | Zero Blockers / Clean Sprint Close | "Definition of Done: no open blockers"; enforced by `orchestration_firewall.py` |
| **Njineer Confirmation** | Human Principal Architect Sign-Off | Required for: changes to AGENT_ROSTER, Sentinel-Amethyst conflict resolution, sovereign file overrides |
| **Deep Re-scan (DemiJoule)** | Semantic Re-evaluation Pass | Triggered by joint escalation: PDMAL ALERT (severity ≥3) + Phi-Closure ESCALATE (severity ≥3); if deep scan returns `kill`, session terminated before HPG |
| **Deontic Gate (P-10)** | Normative Obligation Gate | P-10 deontic gate at hook_point 1 in P-29; "deontic" = logic of obligation/permission/prohibition; external: deontic logic in formal methods |
| **IMP-XX (numbered improvements)** | Tracked Improvement Item | IMP-05 = brand voice consistency (P-19); external: improvement backlog item; analogous to a GitHub issue or Jira ticket |
| **PM-XX (numbered pattern milestones)** | Pattern Registry Milestone / Tracked Action Item | PM-01 = P-32↔P-29 cross-ref (CLOSED S066); PM-02 = P-03 ALTER P-30 ref (CLOSED S066); PM-05 = COLLEEN stasis audit (CLOSED S066); PM-07 = Apogee P-34 attestation (CLOSED S066); external: milestone or tracked action item in a project management system |
| **OPP-XX (numbered opportunities)** | Detected Improvement Opportunity | OPP-003 = P-03 Gate 0 contract count discrepancy; external: improvement opportunity surfaced by COLLEEN in P-07 detect role |
| **BLG-P34-01 / BLG-P34-02** | Pattern-Scoped Blocker | BLG scoped to a specific pattern (P-34); BLG-P34-01 = tradeoff block; BLG-P34-02 = ref path missing; both RESOLVED S066 |
| **NDR-HDFS 1.0 (Information Density)** | Information Extraction Density / Match Rule Density | Measures structured metadata extractable from context window; ✅ FLAG-01 RESOLVED — canonical name updated to NDR-HDFS (see Section 4). No further Hadoop collision risk. |

---

## Section 7 — Storage, Platform & Deployment Labels

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **DGAF-Framework (GitHub repo)** | Canonical Governance Architecture Repository | Primary SSoT for all governance patterns, sweep logs, and session anchors |
| **ndrorchestration (GitHub org)** | Engineering Organization / Repository Namespace | Owner org for all DGAF ecosystem repos; human alias: @ndrorchestration = Andrew Hensel / Njineer |
| **Supabase Project (us-east-2, Postgres 17)** | Managed Relational Database / BaaS | BaaS with Postgres; ACTIVE_HEALTHY status per ECOSYSTEM_INVENTORY |
| **Vercel Project: ndrorchestration** | Ecosystem Landing / GitHub Profile Site (Edge-deployed) | Primary public-facing site at ndrorchestration.vercel.app; current production deployment READY as of 2026-06-09 (sweep date update). Experienced 10 consecutive ERROR deployments 2026-05-25–29 due to fatal Layout.tsx syntax error (unclosed array, no export); resolved in seal commit S029. Open: Dependabot PR #1 (Next 14→15 bump, preview ERROR — see FLAG-12). |
| **Vercel Project: aoga-dashboard** | AOGA Governance Analytics Frontend (Edge-deployed) | Dedicated Vercel project for the AOGA Dashboard; created 2026-05-25; X-Agent-Stack: AOGA-v1.1.0 (bumped 2026-06-26 v1.3.0 commit). Last known deployment state requires verification — may need fresh push or rootDirectory=dashboard confirmation. Source: `ndrorchestration/aoga-dashboard` (private repo). |
| **Vercel Project: phiknightverticalcorridor** | Unknown — Project Purpose Undocumented | Created ~2026-05-05; no deployment data returned in S070 Vercel audit; project purpose not found in any swept document. **See FLAG-11.** |
| **Vercel Project: pptl-governance-dashboard** | Procluding Premise Triadic Loop Governance Dashboard | PPTL now fully expanded (see Section 2); Vercel-deployed governance status frontend |
| **AOGA Dashboard** | Agent Orchestration Governance Architecture Dashboard | **FLAG-04 RESOLVED (S070):** AOGA = Agent Orchestration Governance Architecture. 17/18-route Next.js governance observability frontend. Runtime identity: `X-Agent-Stack: AOGA-v1.1.0`, `X-Gate-Class: Phi-Knight` (promoted from Sentinel-Phi in v1.3.0). Canonical source: `aoga-dashboard` repo + `docs/phi-knight-class.md`. SI=0.8862 at Apogee 18/18 CLEARED. |
| **PPTL Governance Dashboard** | Procluding Premise Triadic Loop Governance Dashboard | PPTL now fully expanded (see Section 2); Vercel-deployed governance status frontend |
| **GitHub (24 repos, 23 active)** | Version Control + Artifact Registry | Primary artifact storage for all sealed session outputs |
| **Google Drive / Gmail (PEL label)** | Document Management System / Knowledge Base | PEL = Prompt Engineering Library & Documentation; 25 essential emails post-cleanup (March 2026) |
| **chat-archives (private repo)** | Research Knowledge Base / Conversation Archive | Internal reference only; not for publication |
| **Gold-star-standards (private repo)** | Proprietary Rating & Certification Methodology Repository | Licensing model; consulting fees; KEEP PRIVATE per January 2026 IP decision |
| **HARMONIC_QUINTET.md** | Harmonic Quintet Formation Specification Document | Source authority for P-15 formation definition; superseded by AGENT_ROSTER.md v1.0 as canonical reference |

---

## Section 8 — Quality & Benchmark Metrics

| Internal Name | External Equivalent | Differentiation Note |
|---|---|---|
| **21% constraint compliance improvement** | +21 percentage point constraint compliance gain | 5-agent system; frequency-based orchestration; baseline not publicly published — needs artifact link |
| **95% modal alignment** | 95% behavioral consistency across agents | Baseline was 87% pre-orchestration; cross-agent consistency on identical prompts |
| **96% TruthfulQA accuracy** | 96% accuracy on internal TruthfulQA-style evaluation | Internal benchmark; not the public TruthfulQA dataset; always gloss with "internal" qualifier |
| **89% off-domain reasoning reduction** | 89% reduction in out-of-scope reasoning | Reduction in responses violating domain constraints |
| **OST-50 / Platinum Star** | ≥99.1% integrity target | Internal benchmark designation; OST-50 = the evaluation standard at that tier |
| **A-TIER (94.5%)** | High-quality attestation grade | P-34 attestation result via APOGEE_11Q; A-TIER = below S-Tier but above standard |
| **82.6% → 100% (governance_clear)** | KAPPA Router Calibration Result | KAPPA v3.5→v3.6 via P-34 14×12 grid sweep; STRONG=0.22, BLENDED=0.18 |
| **58.3% compression (SCPE)** | Context Window Compression Rate at Threshold 0.15 | T0 AXIOM tokens preserved 100%; T3 EXPLORATORY pruned at highest rate |
| **~~340% coordination gain~~ → ILLUSTRATIVE: substantial multi-agent coordination improvement** | Qualitative Coordination Improvement Claim (ILLUSTRATIVE) | ✅ FLAG-02 RESOLVED — Njineer directive 2026-06-27 17:17 EDT: downgraded from quantitative to qualitative. Original figure sourced from NDR-HDFS 1.0 spec; "coordination effectiveness" baseline was never formally defined and cannot be verified. **All future references must use the qualitative form: "substantial multi-agent coordination improvement observed under frequency-based orchestration." The 340% figure must not appear in any external-facing or evidence-grade document without a formally defined baseline and reproducible measurement methodology.** |
| **60-turn simulation (5 Gold Stars)** | 60-step Multi-Agent Simulation, Internally Attested | Self-attested via Apogee; reproduce via `python tests/test_orchestration_firewall.py` against `registry/ensemble_v16_manifest.json` |
| **‖ΔW‖_F < 0.02 convergence threshold** | PDMAL Trust Graph Convergence Criterion | 3 consecutive turns below threshold = CONVERGED; ALERT_THRESH=0.08 for graph manipulation detection |
| **STRONG=0.22 / BLENDED=0.18** | KAPPA Router Confidence Thresholds | Empirically calibrated via P-34 14×12 grid sweep (S034); requires recalibration if input distribution shifts |
| **SI=0.8862 (AOGA Apogee score)** | Stability Index at AOGA 18/18 Apogee Clearance | Recorded in `[AOGA COMPLETE]` commit 2026-05-25; exceeds φ*=0.618 threshold by +0.2682; all 18 routes cleared |
| **Deployment Error Chain: May 25–29, 2026** | Named Production Incident / Root Cause: Fatal Syntax Error | 10 consecutive ERROR deployments on `ndrorchestration` Vercel project. Root cause: Layout.tsx — unclosed array, no export (fatal syntax error). Symptom-level fixes attempted: --legacy-peer-deps, vercel.json cleanup, Next.js version rollback 14.2.29→14.2.28. Resolved by seal commit targeting Layout.tsx directly. Duration: ~4 days. Risk: any Vercel-linked traffic during this window may have contributed to June Needle analytics drop (NT-01/NT-02). |

---

## Section 9 — Open Flags (Items Requiring Resolution)

> These items were identified during sweep as **undocumented, ambiguous, or potentially conflicting.** COLLEEN owns resolution before next session seal.

| Flag | Item | Issue | Recommended Action | Status |
|------|------|-------|-------------------|---|
| FLAG-01 | **HDFS acronym collision** | "HDFS" used for both NDR Hierarchical Documentation Format Standard AND Hadoop Distributed File System | ~~Rename to "NDR-HDFS" or "HDFS-DOC 1.0" in all docs~~ | **RESOLVED S070** — Canonical name is **NDR-HDFS**. Njineer ratified 2026-06-27 17:08 EDT. Applied in Sections 4, 5, 6, 8. All future references must use NDR-HDFS. |
| FLAG-02 | **340% coordination gain** | Metric not formally defined; no artifact link found | ~~Downgrade to qualitative claim or add `docs/qa/` evidence artifact~~ | **RESOLVED S070** — Downgraded to qualitative per Njineer directive 2026-06-27 17:17 EDT. Canonical form: "substantial multi-agent coordination improvement observed under frequency-based orchestration." The 340% figure is retired from evidence-grade use. See Section 8 entry for full constraint language. |
| FLAG-03 | **PPTL acronym** | Expanded as "Procluding Premise Triadic Loop" — first canonical documentation in this file | Backfill PPTL expansion into WORKSPACE_BOOTSTRAP.md and ECOSYSTEM_INVENTORY.md | OPEN |
| FLAG-04 | **AOGA acronym** | ~~Used in Vercel deployment label and docs; canonical expansion not documented anywhere found~~ | ~~Surface to Amethyst for canonical expansion; update ECOSYSTEM_INVENTORY.md~~ | **RESOLVED S070** — AOGA = Agent Orchestration Governance Architecture. Source: aoga-dashboard commit history + X-Agent-Stack header manifest. Update ECOSYSTEM_INVENTORY.md to backfill. |
| FLAG-05 | **AXIS acronym** | Sovereign file; Sentinel-protected; exact acronym expansion not found in any swept document | ~~Surface to Njineer/Amethyst for canonical expansion in AGENT_ROSTER or WORKSPACE_BOOTSTRAP~~ | **RESOLVED S070** — AXIS = Agent X-axis Invariant Spectrum. Njineer ratification received 2026-06-27 16:40 EDT. Full spec: `docs/qa/AXIS_METRIC_SPEC.md` v1.2 CANONICAL. FLAG-05 CLOSED. |
| FLAG-06 | **Agent Lavender / Forseti** | Hard BLG per AGENT_ROSTER.md v1.0; any reference triggers P-01 | Run codebase-wide search; `grep -r "Lavender\|Forseti" docs/` | **RESOLVED S070** — GitHub code search returned 0 results across all files in DGAF-Framework (2026-06-26 20:16 EDT). No stale references found. |
| FLAG-07 | **Drive files 2, 3, 4 unreadable** | Agent Professor Prodigy Technical Spec (NDR-HDFS 1.0), Prodigy Mathematical Rigor POC, and Phi-Calculus White Paper returned empty content during sweep | Re-attempt read in next session; these may contain additional vocabulary not yet captured | OPEN |
| FLAG-08 | **96% TruthfulQA — "internal" qualifier** | Currently stated without "internal" qualifier in some external-facing docs | Audit all public-facing docs for unqualified TruthfulQA claims | OPEN |
| FLAG-09 | **Reson dual-role discrepancy** | v1.0 entry describes Reson as "Router Topology Engineer / CSP Solver"; AGENT_ROSTER describes Reson as "Harmonic Coherence Scorer" with 0.75 threshold | Both are correct (Reson holds both roles); update Section 1 entry to reflect both duties | **RESOLVED S070** — Section 1 entry updated to reflect both Harmonic Coherence Scorer and CSP Router roles. |
| FLAG-10 | **P-35 registration status** | Procluding Premise Gate referenced as P-35 in session context but does not appear in NDR_PATTERN_REGISTRY_UNIFIED.md (watermark is P-34) | Confirm P-35 is pending registration or already registered in a post-S066 session | OPEN |
| FLAG-11 | **phiknightverticalcorridor Vercel project** | Project created ~2026-05-05; no deployment data found in S070 Vercel audit; project purpose, linked repo, and intended function are undocumented in all swept files | Surface to Njineer for canonical purpose definition; update Section 7 and ECOSYSTEM_INVENTORY.md once confirmed | OPEN |
| FLAG-12 | **Dependabot PR #1 — Next 14→15 bump** | Open on `ndrorchestration` repo; preview deployment in ERROR state; Next 14→15 is a major version with breaking changes; disposition not decided | Njineer to decide: merge with breaking-change review, or close/dismiss to keep PR list clean | OPEN |

---

## Maintenance Protocol

- This file is **append-only** — never delete entries, only annotate as superseded
- New terms discovered in any sweep should be added here by COLLEEN before session seal
- **Review trigger:** Any new NDR pattern registration, any new agent added to ENSEMBLE_ROSTER, any new subsystem named in a session
- **Differentiation column policy:** If a term is a direct external equivalent with no novel extension, write "Direct equivalent — use external term with internal label as gloss." If there is a genuine differentiator, describe it in ≤2 sentences.
- **IP boundary:** Sections 6–8 contain items marked for partial public disclosure; tuning tables, specific φ constants, and constraint optimization algorithms remain private per IP protection strategy (January 2026 decision)
- **Flag resolution:** Section 9 flags are COLLEEN's primary resolution queue; all flags must be resolved or formally deferred before session graduation (P-10)

---

*NDR_INTERNAL_VOCABULARY_MASTER.md · v1.5 · S070 OPEN · COLLEEN × Amethyst · 2026-06-27*
*v1.5 additions: FLAG-02 RESOLVED — 340% coordination gain downgraded to qualitative (Njineer directive 2026-06-27 17:17 EDT); Section 8 entry retired with canonical qualitative replacement; Section 5 AXIS entry updated to reference AXIS_METRIC_SPEC v1.2 and Phase 3 owner*
*v1.4 additions: FLAG-01 RESOLVED — NDR-HDFS canonical rename (Njineer ratified 2026-06-27 17:08 EDT); applied in Sections 4, 5, 6, 7, 8, 9*
*v1.3 additions: FLAG-05 RESOLVED (AXIS = Agent X-axis Invariant Spectrum — Njineer ratified 2026-06-27 16:40 EDT), FLAG-06 RESOLVED, AXIS Section 5 entry updated to CANONICAL*
*Sources: AXIS_METRIC_SPEC.md v1.2 CANONICAL (docs/qa/), Njineer ratification directives S070*
