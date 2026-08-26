# DGAF-Framework — Technical & Agent-Facing Reference

> **Claim-status boundary:** This document is a technical/project reference, not a certification, validation, regulatory-conformance statement, or efficacy report. Project-local gate names, targets, thresholds, and attestation labels describe internal procedures or historical records unless current claim-specific evidence says otherwise.
>
> **Current certification policy:** There is no active DGAF certification program. See [`docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](./docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md).

> **Audience:** Agent Amethyst, Agent Apogee, Agent COLLEEN, Agent Sentinel, and all ensemble members; engineers integrating with DGAF  
> **Entry point for:** Gate specs · Pattern registry · Runtime components · Formation protocols · Session open/close procedures  
> **Compliance/governance entry point:** [`README.governance.md`](./README.governance.md)  
> **Architect:** Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration)

---

## MDAR Loop — Project Protocol

```
Map → Diagnose → Act → Review
  ↑                        |
  └────────────────────────┘
     (each cycle = one project-defined interval)
```

The MDAR loop is a project orchestration protocol. Claims about improved correctness, convergence, safety, or efficacy require separate evidence.

---

## Gate Stack — Project Execution Order

| Priority | Gate | Pattern | Trigger | Owner |
|----------|------|---------|---------|-------|
| 1 (always) | GATE-ACO: Acoustic Chain | P-13 | Every synthesis cycle | Amethyst + DemiJoule |
| 2 (every artifact) | GATE-1111: 1-1-1-1 | P-10 | Pre-registry sign-off | Apogee |
| 3 (pre-deploy) | GATE-11Q: Hendecagonal | P-11 | Proposed production deployment | Apogee + Sentinel |
| 4 (deep audit) | GATE-TEL: Telescopic Lens | P-12 | Project-local structural audit | Apogee + Amethyst |
| 5 (canonical promotion) | Apogee-Attestation-Gate | P-30 | Component/pattern canonical promotion | Apogee + Amethyst |

Full specifications: [`docs/gates/`](./docs/gates/). Gate PASS states are project-local control results unless explicitly supported by separate current evidence.

---

## Runtime Components

| Component | Path | Purpose | Status note |
|-----------|------|---------|------------|
| KAPPA Dynamic Confidence Router | `components/KAPPA/dynamic_weight_router.py` | Confidence-gated routing and category-sensitive weight selection | Implementation artifact; efficacy requires separate evaluation |
| KAPPA Calibration v3.6 | `components/KAPPA/calibration_v3_6.json` | Threshold calibration | Project configuration; not evidence of optimality |
| KAPPA Component Card | `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` | CPU-oriented registry card | Project metadata |
| Evaluate Router | `components/evaluate_router.py` | Batch pipeline composition: detect → apply_weights → rank | Implementation artifact |
| Evaluate Router v1.1 | `components/evaluate_router_v1_1.py` | Sentinel hooks, P-10 deontic gate, per-record audit log | Implementation artifact |
| Normative Constraint | `components/normative_constraint.py` | Deontic / optimization / epistemic integrity constraint class | Implementation artifact |

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
| Apogee 11Q S034 | `docs/qa/APOGEE_11Q_S034.json` | Historical/project-local attestation artifact |
| Apogee 11Q S035 | `docs/qa/APOGEE_11Q_S035.json` | Historical/project-local attestation artifact |
| QA Index | `docs/qa/README.md` | Attestation artifact index |

An attestation record is not automatically an independent certification or validation result.

---

## Kernel & Contraction Nomenclature — S068

> Added: 2026-06-26 · Issue #32 · Steward: Amethyst  
> Context: Nemotron 3 Ultra integration planning — parametric eval suite

| Term | Definition | Constraint / interpretation | First Used |
|------|-----------|----------------------------|------------|
| **typed kernel** | A governance role's executable Python/TypeScript unit with explicit `input_schema → policy → output_schema → audit_trail` contract; generated from `governance.yml` | Contract/property definition; CI promotion requires the project's named check | S068 |
| **ρ-contraction** | A mathematical property `‖T(x) - T(y)‖ ≤ ρ‖x - y‖` for an operator T | ρ < 1 is a sufficient condition for convergence for the stated mathematical model; project monitoring does not by itself establish that the deployed system satisfies the premise | S068 |
| **spectral radius** | Largest absolute eigenvalue of a role transition matrix | A spectral-radius check is a bounded mathematical check; production monitoring does not by itself prove convergence of the real system | S068 |
| **curvature** (governance) | Per-role scalar used by the project router | Project-local modeling variable; empirical meaning requires validation | S068 |
| **triadic orchestration** | Three-phase project inference loop: Apogee (propose) → Reson (critique) → Lyra (resolve) | Design pattern; stronger alignment or performance claims require comparative evidence | S068 |
| **thinking_tokens** | Per-role reasoning budget parameter | Configuration parameter; not a measure of reasoning quality by itself | S068 |
| **MoE expert entropy** | Shannon entropy H of expert activation distribution across routing decisions | Diagnostic metric; thresholds are project parameters unless calibrated | S068 |
| **role_boundary_coherence** | Eval metric for role identification across a defined trace | Target values are hypotheses/benchmarks until reproduced and validated | S068 |
| **contraction_proof_fidelity** | Eval metric defined by the project for generated kernel specifications | A CI result supports the tested corpus/procedure only; it is not proof of deployed-system convergence | S068 |
| **governance_schema_conformance** | Eval metric for fuzz-generated `governance.yml` variants | Test-specific conformance result; not general compliance | S068 |
| **audit_hallucination_rate** | Field-level accuracy of generated audit events versus ground truth | Evaluation metric; benchmark values are evidence only for the stated test scope | S068 |
| **taubench_banking_mitigation** | Project eval metric for financial compliance routing | Evaluation target; no regulatory-compliance claim follows from the target itself | S068 |
| **ROLE_BUDGETS** | Dict mapping DGAF role names to reasoning-budget values | Configuration source of truth for the project implementation | S068 |

---

## Session Open Protocol (COLLEEN — P-02)

```
1. Read session-state reference → rehydrate open BLGs + priority queue
2. Run .operations/gate_compliance_check.py → surface P-24 gaps
3. Emit session priority queue to Amethyst
4. Amethyst opens wave; Apogee scores; Sentinel monitors
```

Operational session state belongs in the private operational boundary. The public repository should contain only sanitized reproducibility/governance material.

Checklist: [`.operations/sweep_session_init.md`](./.operations/sweep_session_init.md)

---

## Session Close Protocol (Amethyst — P-06 + P-21)

```
1. All repo fixes committed
2. SWEEP_LOG.md updated + buoy appended
3. CHANGELOG.md versioned
4. CROSS_REF.md updated
5. Operational session state sealed in its designated boundary
6. Seal commit pushed
```

Checklist: [`.operations/seal_checklist.md`](./.operations/seal_checklist.md)

---

## Formation Reference

| Formation | Pattern | Agents | Use |
|-----------|---------|--------|-----|
| Trio | P-14 | Amethyst + Apogee + COLLEEN | Standard multi-repo sweep |
| Harmonic Quintet | P-15 | Trio + Reson + Sentinel | Seal commits; sovereign file changes |
| IP Sweep | — | Amethyst + Perplexity MCP | Research, external source integration |

Formation names and role assignments are project architecture. They do not establish independent capability claims about an agent implementation.

---

## Key File Locations

```
DGAF-Framework/
├── README.md                          ← Public-facing entry point
├── README.governance.md               ← Governance reference
├── README.technical.md                ← This technical reference
├── CHANGELOG.md                       ← Semantic versioned history
├── CROSS_REF.md                       ← Ecosystem artifact map
├── ENSEMBLE_ROSTER.md                 ← Canonical agent registry
├── components/                        ← Runtime components
├── docs/gates/                        ← Project gate specifications
├── docs/patterns/                     ← Project pattern registry
├── docs/qa/                           ← Attestation/evidence artifacts
├── scripts/claim_hygiene_check.py    ← Blocking public claim-hygiene scanner
└── .github/workflows/ip-hygiene.yml  ← IP/claim hygiene CI
```

Operational internals and live session state must remain outside the public reproducibility boundary unless intentionally sanitized.

---

## ANDROMEDA-AXIS Declarations (P-09)

All agent actions are checked against four project sovereign constraints:

| Declaration | Constraint |
|-------------|------------|
| COGNITIVE_SOVEREIGNTY | No agent may alter the architect's epistemic autonomy or decision authority |
| BIOLOGICAL_INTEGRITY | No output may threaten physical or psychological integrity |
| TRANSVERSAL_GROWTH | Systems should support ongoing learning and capability expansion |
| ENTROPY_RESISTANCE | No action should increase systemic disorder beyond recoverable bounds |

These are project governance declarations, not externally certified safety guarantees.

---

## Evidence and Claim Discipline

Public technical claims should be read together with:

- [`docs/CLAIM_EVIDENCE_INDEX.md`](./docs/CLAIM_EVIDENCE_INDEX.md)
- [`docs/evidence/EVIDENCE_LADDER_POLICY.md`](./docs/evidence/EVIDENCE_LADDER_POLICY.md)
- [`docs/EPISTEMIC_EVIDENCE_STANDARD.md`](./docs/EPISTEMIC_EVIDENCE_STANDARD.md)
- [`docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md`](./docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md)

A design, implementation, test, bounded mathematical result, historical attestation, and independently validated empirical result are distinct evidence states and must not be collapsed.

---

*License: Apache 2.0 · See [NOTICE](./NOTICE) for attribution and project IP boundary*  
*Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)*  
*README.technical — epistemically bounded revision · 2026-08-25*
