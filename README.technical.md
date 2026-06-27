# DGAF-Framework — Technical & Agent-Facing Reference

> **Audience:** Agent Amethyst, Agent Apogee, Agent COLLEEN, Agent Sentinel, and all ensemble members; engineers integrating with DGAF  
> **Entry point for:** Gate specs · Pattern registry · Runtime components · Formation protocols · Session open/close procedures  
> **Compliance/governance entry point:** [`README.governance.md`](./README.governance.md)  
> **Architect:** Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration)

---

## MDAR Loop — Master Cycle

```
Map → Diagnose → Act → Review
  ↑                        |
  └────────────────────────┘
     (each cycle = one phi-gate interval)
```

Every agent action occurs within an MDAR cycle. Cycles are time-bounded by the Acoustic Gate Chain (P-13). No artifact crosses a cycle boundary without Cadence gate confirmation.

---

## Gate Stack — Execution Order

| Priority | Gate | Pattern | Trigger | Owner |
|----------|------|---------|---------|-------|
| 1 (always) | GATE-ACO: Acoustic Chain | P-13 | Every synthesis cycle | Amethyst + DemiJoule |
| 2 (every artifact) | GATE-1111: 1-1-1-1 | P-10 | Pre-registry sign-off | Apogee |
| 3 (pre-deploy) | GATE-11Q: Hendecagonal | P-11 | Production deployment | Apogee + Sentinel |
| 4 (S-TIER/audit) | GATE-TEL: Telescopic Lens | P-12 | S-TIER cert · structural audit | Apogee + Amethyst |
| 5 (canonical promotion) | Apogee-Attestation-Gate | P-30 | Component/pattern canonical promotion | Apogee + Amethyst |

Full specs: [`docs/gates/`](./docs/gates/)

---

## Runtime Components

| Component | Path | Purpose | Session |
|-----------|------|---------|---------|
| KAPPA Dynamic Confidence Router | `components/KAPPA/dynamic_weight_router.py` | Confidence-gated routing and category-sensitive weight selection | S033 |
| KAPPA Calibration v3.6 | `components/KAPPA/calibration_v3_6.json` | Threshold calibration; `governance_clear` tuned to 100% | S034 |
| KAPPA Component Card | `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` | CPU-compliant registry card | S034 |
| Evaluate Router | `components/evaluate_router.py` | Batch pipeline composition: detect → apply_weights → rank | S033 |
| Evaluate Router v1.1 | `components/evaluate_router_v1_1.py` | Sentinel hooks, P-10 deontic gate, per-record audit log | S034 |
| Normative Constraint | `components/normative_constraint.py` | Deontic / optimization / epistemic integrity constraint class | S035 |

Component index: [`components/README.md`](./components/README.md)

---

## NDR Pattern Registry — Quick Reference

| Range | Domain |
|-------|--------|
| P-01–P-08 | Coherence, continuity, git hygiene, cross-platform sync |
| P-09–P-13 | AXIS enforcement, quality gates, acoustic temporal chain |
| P-14–P-15 | Formation protocols (Trio, Harmonic Quintet) |
| P-16–P-20 | Metadata hygiene, IP, issue triage, branding, Drive sync |
| P-21–P-24 | Session continuity, storage topology, taxonomy audit, canonical practice unit |
| P-27–P-30 | Confidence routing, pipeline composition, Sentinel risk pass, Apogee attestation |

Full registry: [`docs/patterns/NDR_PATTERN_REGISTRY.md`](./docs/patterns/NDR_PATTERN_REGISTRY.md)

---

## QA & Attestation Surface

| Artifact | Path | Meaning |
|----------|------|---------|
| Apogee 11Q S034 | `docs/qa/APOGEE_11Q_S034.json` | Pre-NormativeConstraint A-TIER attestation |
| Apogee 11Q S035 | `docs/qa/APOGEE_11Q_S035.json` | Post-NormativeConstraint S-TIER attestation |
| QA Index | `docs/qa/README.md` | Attestation artifact index |

---

## Kernel & Contraction Nomenclature — S068

> Added: 2026-06-26 · Issue #32 · Steward: Amethyst  
> Context: Nemotron 3 Ultra integration planning — parametric eval suite

| Term | Definition | Constraint | First Used |
|------|-----------|-----------|------------|
| **typed kernel** | A governance role's executable Python/TypeScript unit with explicit `input_schema → policy → output_schema → audit_trail` contract; generated from `governance.yml` | Must pass `contraction_proof_fidelity` gate before CI promotion | S068 |
| **ρ-contraction** | The property `‖T(x) - T(y)‖ ≤ ρ‖x - y‖` for a role transition operator T; guarantees convergence of governance trajectories | ρ < 1.0 required; verified via `numpy.linalg.eigvals` spectral radius check | S068 |
| **spectral radius** | Largest absolute eigenvalue of a role transition matrix; must be < 1.0 to satisfy ρ-contraction; monitored in production via vLLM expert-routing logs | Alert threshold: ≥ 0.99; freeze curriculum if ≥ 1.0 | S068 |
| **curvature** (governance) | Per-role scalar (0.0–1.0) encoding how sharply a role's decision boundary curves in embedding space; drives routing decisions in the curvature-aware router | Defined in `governance.yml` per role; Lyra = 0.00 (base), Echolette = 0.20 (highest) | S068 |
| **triadic orchestration** | Three-phase inference loop: Apogee (propose) → Reson (critique) → Lyra (resolve); produces stronger alignment guarantees at 3× inference cost | Target p99 < 200ms on 7B-class; budget via `thinking_tokens` per role | S068 |
| **thinking_tokens** | Per-role reasoning budget parameter passed to Nemotron 3 Ultra via `extra_body.chat_template_kwargs`; controls depth of inference per DGAF role | Sentinel: 8192 (max); Herald: 0 (audit-only); Echolette: 512 (min) | S068 |
| **MoE expert entropy** | Shannon entropy H of expert activation distribution across all MoE routing decisions for a given DGAF role; low entropy signals expert collapse | Alert if H < 0.6 per role; measure via vLLM routing logs | S068 |
| **role_boundary_coherence** | Eval metric: % correct role identification at turn N in 50-turn triadic trace; maps to Mamba state retention under 1M-token context | Target > 95%; baseline: RULER 1M = 94.0 | S068 |
| **contraction_proof_fidelity** | Eval metric: % of 100 generated kernel specs where spectral radius < 1.0; maps to GPQA Diamond reasoning (87.9%) | Target > 98%; run as CI gate before kernel promotion | S068 |
| **governance_schema_conformance** | Eval metric: % of 1k fuzz-generated `governance.yml` variants passing Pydantic `extra=forbid`; maps to IFBench instruction following | Target > 99%; blocks CI on failure | S068 |
| **audit_hallucination_rate** | Eval metric: field-level accuracy of Herald-generated audit events vs ground truth; maps to OmniScience Non-Hallucination | Target > 78.7% (BF16 baseline); NVFP4 degrades to 75.5% — prefer BF16 for Herald | S068 |
| **taubench_banking_mitigation** | Eval metric: % correct Sentinel escalation on financial compliance routing; raw Nemotron baseline 22.6% — hardest domain | Target > 80%; REQUIRES explicit few-shot priming before baseline run | S068 |
| **ROLE_BUDGETS** | Dict in `dgaf_nemotron_client.py` mapping DGAF role names to `thinking_tokens` values; single source of truth for per-role reasoning allocation | Must be reviewed on each Nemotron model version upgrade | S068 |

---

## Session Open Protocol (COLLEEN — P-02)

```
1. Read SESSION_ANCHOR.md  →  rehydrate open BLGs + priority queue
2. Run .operations/gate_compliance_check.py  →  surface P-24 gaps
3. Emit session priority queue to Amethyst
4. Amethyst opens wave; Apogee scores; Sentinel monitors
```

Checklist: [`.operations/sweep_session_init.md`](./.operations/sweep_session_init.md)

---

## Session Close Protocol (Amethyst — P-06 + P-21)

```
1. All repo fixes committed
2. SWEEP_LOG.md updated + buoy appended
3. CHANGELOG.md versioned
4. CROSS_REF.md updated
5. SESSION_ANCHOR.md overwritten (not appended)
6. Seal commit pushed (atomic — all files in one push_files call)
```

Checklist: [`.operations/seal_checklist.md`](./.operations/seal_checklist.md)

---

## Formation Reference

| Formation | Pattern | Agents | Use |
|-----------|---------|--------|-----|
| Trio | P-14 | Amethyst + Apogee + COLLEEN | Standard multi-repo sweep |
| Harmonic Quintet | P-15 | Trio + Reson + Sentinel | Seal commits; sovereign file changes |
| IP Sweep | — | Amethyst + Perplexity MCP | Research, external source integration |

---

## Key File Locations

```
DGAF-Framework/
├── README.md                          ← Public-facing entry point
├── README.governance.md               ← NIST/EU AI Act compliance reference
├── README.technical.md                ← This file — agent/engineer reference
├── SESSION_ANCHOR.md                  ← P-21 session state (overwrite pattern)
├── SWEEP_LOG.md                       ← Sealed audit trail
├── CHANGELOG.md                       ← Semantic versioned history
├── CROSS_REF.md                       ← Ecosystem artifact map
├── ENSEMBLE_ROSTER.md                 ← Canonical agent registry
├── components/
│   ├── README.md                      ← Runtime component index
│   ├── KAPPA/
│   ├── evaluate_router.py
│   ├── evaluate_router_v1_1.py
│   └── normative_constraint.py
├── docs/
│   ├── gates/
│   │   ├── GATE_UNIT_TEMPLATE.md      ← P-24 blank (copy to start new gate)
│   │   ├── ACOUSTIC_GATES.md          ← GATE-ACO (P-13) — CERTIFIED v2.0
│   │   ├── GATE_1111.md               ← GATE-1111 (P-10) — CERTIFIED v2.0
│   │   ├── GATE_11Q.md                ← GATE-11Q (P-11) — CERTIFIED v2.0
│   │   ├── TELESCOPIC_LENS.md         ← GATE-TEL (P-12) — CERTIFIED v2.0
│   │   └── GATE_SPECS.md              ← Gate index
│   ├── patterns/
│   │   └── NDR_PATTERN_REGISTRY.md    ← P-01 through P-30
│   ├── protocols/
│   │   └── MDAR_PROTOCOL_v1.md        ← Master cycle protocol
│   ├── qa/
│   │   ├── README.md                  ← QA / attestation index
│   │   ├── APOGEE_11Q_S034.json
│   │   └── APOGEE_11Q_S035.json
│   └── drafts/                        ← Staging area (P-03/P-11/P-18)
├── tests/
│   ├── dgaf_eval_suite.py             ← 🟡 Nemotron 3 Ultra eval — Issue #32
│   └── ...
├── .operations/                       ← Maintainer-only ops tooling
│   ├── gate_compliance_check.py       ← P-24 compliance scanner
│   ├── sweep_session_init.md          ← Session open checklist
│   └── seal_checklist.md              ← Session close/seal checklist
└── .github/
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

---

## ANDROMEDA-AXIS Declarations (P-09)

All agent actions are checked against four sovereign constraints:

| Declaration | Constraint |
|-------------|------------|
| COGNITIVE_SOVEREIGNTY | No agent may alter Njineer's epistemic autonomy or decision authority |
| BIOLOGICAL_INTEGRITY | No output may threaten physical or psychological integrity of the architect |
| TRANSVERSAL_GROWTH | All systems must support ongoing learning and capability expansion |
| ENTROPY_RESISTANCE | No action may increase systemic disorder beyond recoverable bounds |

Violation triggers `SYNC_LOCKED` escalation to Amethyst-Conductor immediately.

---

*License: Apache 2.0 · See [NOTICE](./NOTICE) for full attribution*  
*Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)*  
*README.technical v1.1 · S068 kernel/contraction nomenclature patch · Amethyst · 2026-06-26*
