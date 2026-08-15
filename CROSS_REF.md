# CROSS_REF.md

> **Last reviewed:** 2026-08-15  
> **Purpose:** Canonical cross-reference index for project-local patterns, files, agents, and terminology.

## Epistemic policy

This index distinguishes project records from externally validated facts. A registry entry, agent attestation, Gold Star/S-Tier label, owner approval, benchmark label, or historical sweep result is **not by itself** independent scientific validation, certification, legal compliance, or production readiness.

Use the following evidence states consistently:

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

- **DEFINED:** specified but not necessarily implemented.
- **IMPLEMENTED:** present in executable code or an operational artifact.
- **COMPUTED:** produced by a reproducible calculation/run.
- **VERIFIED:** supported by an appropriate reproducible test or independent evidence.
- **ATTESTED:** recorded by a project reviewer/agent; not necessarily independently recomputed.
- **HISTORICAL:** retained for provenance and no longer asserted as current state.
- **HYPOTHESIS:** proposed mechanism awaiting validation.
- **METAPHOR:** explanatory analogy, not a literal technical/mathematical implementation.
- **UNSUPPORTED:** presently lacks sufficient evidence.
- **DEPRECATED:** superseded terminology/design.

## NDR Pattern Registry

**Canonical source:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`

| Pattern | Name | Current evidence state |
|---|---|---|
| P-01 | Fan-Out Trace Sink w/ Dead-Letter | Project registry; implementation evidence must be checked in source/tests |
| P-02 | Async-Persist Ring Buffer | Project registry; implementation evidence must be checked in source/tests |
| P-03 | Governance Contract Test | Project registry; implementation evidence must be checked in source/tests |
| P-04 | Parametrized Corpus | Project registry; implementation evidence must be checked in source/tests |
| P-05 | Tri-Phase CI Gate | Project registry; implementation evidence must be checked in source/tests |
| P-06 | Topology × Orchestration Matrix Lab | Project registry / research artifact |
| P-07 | Dual-Agent Persistent Sweep Loop | Project registry / workflow artifact |
| P-08 | Triad Taxonomy | Project registry / specification |
| P-09 | Triumvirate Mandate Schema | Project registry / specification |
| P-10 | Session Graduation Check | Project registry / specification |
| P-11 | 11Q Attestation Scoring | Project-local attestation mechanism |
| P-12–P-26 | Stasis patterns | Historical/project registry; individual pattern evidence varies |
| P-27 | Adaptive-Weighting-with-Confidence-Gates | Project registry |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | Project registry |
| P-29 | Sentinel-Annotated Risk Pass | Project registry |
| P-30 | Apogee-Attestation-Gate | Project-local attestation mechanism |
| P-31 | SCPE — Structural Context Pruning Engine | Project registry; implementation status requires source verification |
| P-32 | Fibonacci Phi-Closure Gate | Project registry; mathematical/empirical claims require separate evidence |
| P-33 | PDMAL Convergence Monitor | Project registry; do not infer PDMAL lineage from AHG terminology |
| P-34 | Empirical-Threshold-Sweep-over-ML-Classifier | Project-local evaluation artifact; results require run provenance |
| P-35 | Procluding Premise Gate | Canonical project-local pattern; owner attestation is not external certification |
| P-36 | Gate Priority Schema | Canonical project-local specification |
| P-37 | Stochastic-Deterministic Saga Boundary | Registered project-local pattern |
| P-38 | Circuit-Breaker with HITL Escalation | Registered project-local pattern |
| P-39 | ACRFence — Atomic Checkpoint-Restore with Effect Fence | Registered project-local pattern |
| P-40 | Atomix — Transactional Tool Boundary | Registered project-local pattern |
| P-41 | Sentinel-Phi HITL Durable Queue | Registered project-local pattern |
| P-42 | Adaptive Harmonic Governance (AHG) | **Specified; implementation pending unless independently verified** |

## AHG / P-42 vocabulary

**Canonical expansion:** **AHG = Adaptive Harmonic Governance.**

Earlier uses of **Adaptive Hierarchical Governance** and **Adaptive Harmonic-Hierarchical Hybrid (AH3)** are historical/deprecated terminology unless a source explicitly identifies them as historical.

The following are project-defined terms. They must not be presented as established control-theory quantities without derivation and validation.

| Term | Meaning / evidence boundary |
|---|---|
| Cognitive Phase Energy (φ) | Project-defined governance signal |
| Phase Velocity (vφ) | Project-defined rate-of-change quantity |
| Phase Acceleration (aφ) | Project-defined second-derivative quantity |
| State Vector (xt) | Project-defined state representation |
| Productive Divergence (Dp) | Project-defined useful disagreement category |
| Destabilizing Entropy (De) | Project-defined harmful-divergence category |
| Conductor Archetype | Project-defined operating-mode abstraction |
| Phase Intent (It) | Project-defined broadcast/control packet |
| Compliance Coefficient (αi) | Project-defined weighting parameter |
| Mission Utility (J) | Project-defined objective function |
| Recovery Score (Rc) | Project-defined recovery criterion |
| Governance Momentum (M) | Project-defined hysteresis term |
| Hysteresis Band | Project-defined transition buffer |
| Sidecar Monitor | Project observability component |
| Heartbeat | Project-local compressed agent signal |
| MPHG | Model Predictive Harmonic Governance; roadmap terminology |
| Cognitive Control Plane | Project abstraction over task execution |

### P-42 operating ranges

The φ ranges below are **project-defined parameters**, not universal stability laws. Any claim that a particular range guarantees stability requires an explicit derivation and empirical validation.

| Range | Project mode |
|---|---|
| 1.0–1.15 | Convergent / execution |
| 1.15–1.45 | Adaptive / vigilant |
| 1.45–1.70 | Divergent / exploratory |
| >1.70 | Project-defined high-tension regime |

## AHG conductor archetypes

These are project role mappings, not independent authority claims.

| Archetype | Project agent mapping | Intended bias |
|---|---|---|
| Executor | Professor Prodigy | Precision execution |
| Explorer | Herald | Hypothesis generation |
| Sentinel | DemiJoule | Validation / constraint checking |
| Synthesizer | Herald / COLLEEN | Integration |
| Auditor | Apogee Lens | Contradiction discovery |
| Tribunal | Amethyst | Convergence / failure resolution |

## Turn-sequence cross-reference

Paths are references to intended/current implementation surfaces. Runtime status must be established from current source and tests, not from this table alone.

| Step | Component | Pattern | File | Evidence note |
|---|---|---|---|---|
| 0 | Procluding Premise Gate | P-35 | `docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md` | Project-local gate |
| 1 | SCPE.prune() | P-31 | `scpe_ensemble_v14.py` | Verify current implementation |
| 2 | COLLEEN schema diff | P-04 | `colleen_schema_diff.py` | Verify current implementation |
| 3 | Reciprocity arbitration | P-06 | `reciprocity_arbiter.py` | PDMAL relationship requires source evidence |
| 4 | DemiJoule safety gate | P-03 | `dgaf_semantic_gate.py` | Verify current tests |
| 5 | Phi-closure gate | P-32 | `phi_closure_gate.py` | Parameters are project choices unless derived |
| 6 | HPG gate | P-29 | `hpg_ionian_gate.py` | Verify current implementation |
| 7 | Prodigy verifier | P-05 | `prodigy_verifier.py` | Verify current threshold and tests |
| 8 | Apogee artifact review | P-30 | `amethyst_dual_lock.py` | Attestation ≠ independent certification |
| 9 | Amethyst seal | P-08 | `orchestration_firewall.py` | Verify current audit implementation |
| 10 | AHG phase observation | P-42 | `ahg_conductor.py` | **Planned unless current source proves otherwise** |

## File index

| Path | Role | Evidence status |
|---|---|---|
| `SESSION_ANCHOR.md` | Session/project state | Current-state document; timestamp required |
| `CO_ORCH_QUEUE.md` | Work queue | Current-state document |
| `SWEEP_LOG/` | QA/audit history | Historical records; conclusions remain time-scoped |
| `CROSS_REF.md` | Cross-reference index | Canonical index |
| `ENSEMBLE_ROSTER.md` | Agent roles | Project-local roster |
| `CHANGELOG.md` | Version history | Historical record |
| `DEFERRED_ITEMS.md` | Deferred work | Current-state document |
| `README.md` | Public overview | Public summary; must not overstate validation |
| `README.governance.md` | Governance architecture | Project-local reference |
| `README.technical.md` | Technical implementation | Project-local reference |
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | Pattern registry | Registry source of truth |
| `docs/ndr_patterns_unified.json` | Machine-readable registry | Registry mirror; should be kept synchronized |
| `docs/theory/AHG_ARCHITECTURE.md` | P-42 specification | Specification; not proof of implementation |
| `patterns/P-42_AHG.md` | P-42 pattern card | Specification; not proof of implementation |
| `components/ahg_conductor.py` | P-42 conductor | Planned unless source/tests show implementation |
| `components/ahg_sidecar.py` | P-42 sidecar | Planned unless source/tests show implementation |

## PDMAL boundary

PDMAL is a separate technical track. The current audited PDMAL evidence is the dodecahedral-graph lattice work represented by `lattice_harness.py` and `lattice_formalization_corrected.md`.

Do **not** infer that AHG Zeta-Pell, PDMAL, or other similarly named artifacts are one mathematical system merely because they share terms such as φ, convergence, governance, or lattice. A bridge must be explicitly specified and independently evidenced.

## State-anchor claims

State labels such as `0 BLGs`, `Active`, `Locked`, `Wired`, `Stable`, `T0 immune`, or `Mandatory` are not permanent facts. They are valid only with a current source/test/log supporting the claim.

| Goal / claim | Source | Required evidence |
|---|---|---|
| zero-open-BLG state | `orchestration_firewall.py` / current logs | Current telemetry or reproducible test |
| authority-chain validity | `authority_chain_valid()` | Current test evidence |
| append-only behavior | firewall implementation/tests | Current test evidence |
| observable boundary invariants | boundary tests | Current test run |
| premise-first classification | SCPE implementation | Current source/tests |
| φ range monitoring | P-42 components | **Not current until implementation is verified** |

## Evaluation terminology

Benchmark names and percentages must never be used as proof that the named benchmark was actually run. The authoritative evidence is the corresponding test code plus a reproducible run artifact.

| Term | Meaning | Evidence requirement |
|---|---|---|
| `role_boundary_coherence` | Project evaluation metric | Labeled/reproducible run |
| `contraction_proof_fidelity` | Project evaluation metric | Mathematical test + reproducible run |
| `governance_schema_conformance` | Project evaluation metric | Corpus/test run |
| `audit_hallucination_rate` | Project evaluation metric | Ground-truth labeled corpus |
| `taubench_banking_mitigation` | Project evaluation metric | Actual benchmark run |
| `DGAF_EVAL_TASKS` | Evaluation registry | Current source |
| `thinking_tokens` | Reasoning-budget parameter | Current client/config |

## Historical terminology rule

Historical sweep logs, old deadlines, attestation percentages, tier labels, and previous nomenclature remain preserved for provenance. They must not be silently promoted to current state.

In particular:

- Old deadlines are historical unless a current document re-establishes them.
- “Ratified,” “A-TIER,” “Gold Star,” and “S-Tier” are project-local status labels unless an external standard explicitly says otherwise.
- Exact percentages require a source run, not a copied literal.
- Mathematical vocabulary must describe the implemented operation; metaphorical names must be marked as metaphor.
- A planned component must not be described elsewhere as active merely because a specification exists.

## Known cleanup items

- Verify whether `patterns/P-35_AHG.md` still exists before deleting it; the former index claimed it was stale, but deletion must be based on the current tree rather than documentation.
- Reconcile this index against `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` and `docs/ndr_patterns_unified.json` after registry changes.
- Audit README and sweep-log copies for deprecated AHG expansions and unsupported benchmark/status claims.
- Preserve historical evidence while correcting current-state labels.

*Reviewed 2026-08-15 as part of the repository-wide epistemic, temporal, terminology, and traceability audit.*
