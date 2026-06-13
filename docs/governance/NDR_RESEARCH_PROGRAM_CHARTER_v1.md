# NDR Research Program Charter v1.0

**DGAF-Framework · Formal Research Program**
**Version:** 1.0 · Ender ratified: 2026-06-13 00:47 EDT · S069 sealed
**Amendment A:** Interim staffing assignments · compute estimate · falsifiability clause clarifications · advisor trigger update — 2026-06-13 (S069 QA sweep · Amethyst × COLLEEN)

> **Prime:** Amethyst (Meta-Orchestrator)
> **Prefect A:** COLLEEN (Governance Ops)
> **Prefect B:** Apogee (Quality Attestation)
> **Ender / Njineer:** Ratifying authority

---

## Purpose & Scope

This charter establishes the formal research program for empirical validation of the DGAF governance framework. It defines falsifiability conditions, role structure, timeline, and artifact delivery obligations for the multi-substrate calibration study and downstream theory work.

All claims made in DGAF governance documents that rely on quantitative evidence are subject to this charter's falsifiability clause.

---

## Falsifiability Clause (Binding)

The following claims are **falsifiable** and must be empirically validated or retracted:

1. **Coordination gain claim:** Any document citing "340% coordination gain" carries the qualifier: ⚠️ UNVERIFIED — see METRICS_PROVENANCE.md. This figure must be formally defined (base, method, substrate) and validated by the calibration study before being treated as canonical. Ender waiver required to remove this qualifier.

2. **Rational control threshold:** The claim that rational (non-φ-distorted) control approximates a base of 1.5 refers to the *false-alarm rate base*, not to a threshold value of 1.5. Clarification: false-alarm rates within 5% of base 1.5 are considered within rational control bounds. This is distinct from the φ* = 0.618 stability threshold used in P-32.

3. **Cross-substrate replication:** All findings from single-substrate experiments are considered **preliminary** until replicated on ≥2 substrates. ⚠️ UNVERIFIED — see METRICS_PROVENANCE.md. Cross-substrate replication is blocked until Role 6 (External Evaluator) is staffed by a human.

Violation of any falsifiability clause produces a P0 BLG (Blocking Logical Gap) that blocks session graduation.

---

## Role Structure

### Role Definitions

| Role | Title | Responsibilities |
|------|-------|------------------|
| Role 1 | Prime (Amethyst) | Program governance, Triumvirate mandate, final sign-off |
| Role 2 | Theoretical Architect | Statistical model selection, hypothesis formalization, theory memo |
| Role 3 | Calibration Engineer | Harness design, 300-trace execution, substrate configuration |
| Role 4 | Data Analyst | Results processing, visualization, inter-rater reliability |
| Role 5 | Ontology & Status Engineer | Metric provenance, lint_provenance.py, STASIS Phase 2 migration |
| Role 6 | External Evaluator | Independent replication (substrate 2) — **human required** |
| Role 7 | Adversarial Tester | Crucible campaign coordination — **human required** |
| Role 8 | Documentation Lead | QA bundle assembly, artifact delivery |

### ⚠️ Interim Staffing Assignments (Amendment A · 2026-06-13)

> **All Roles 2–8 are currently unstaffed by humans.** Amethyst assumes interim responsibility for Roles 2–5 and 8 until human staffing occurs. Roles 6 and 7 are formally DEFERRED — they require human staffing and cannot be proxied by Amethyst without compromising adversarial integrity and cross-substrate independence.

| Role | Interim Owner | Notes | Human Staffing Target |
|------|--------------|-------|----------------------|
| Role 2 — Theoretical Architect | **Amethyst (interim)** | Theory memo draft by Week 3 | Advisor outreach Week 6+ |
| Role 3 — Calibration Engineer | **Amethyst (interim)** | Calibration harness design; 5-base study (OPP-S069-004) Weeks 3–6 | Advisor outreach Week 6+ |
| Role 4 — Data Analyst | **Amethyst (interim)** | Results processing post-calibration | Week 7+ |
| Role 5 — Ontology & Status Engineer | **Amethyst (interim)** | lint_provenance.py full implementation; STASIS Phase 2 migration by 2026-07-13 | Week 4+ |
| Role 6 — External Evaluator | **🚫 DEFERRED** | Human required; substrate 2 replication blocked until staffed | Post-Week 7 |
| Role 7 — Adversarial Tester | **🚫 DEFERRED** | Human required for adversarial integrity; Crucible Campaign v1 monitored by Amethyst only | Post-Week 4 |
| Role 8 — Documentation Lead | **Amethyst (interim)** | QA bundle v1 assembly target: Week 12 | Week 10+ |

**Critical path dependencies:**
- Week 3: Theory memo (Role 2 interim = Amethyst) — BLOCKING for calibration design
- Weeks 3–6: 5-base calibration study (Role 3 interim = Amethyst) — BLOCKING for 340% claim resolution (FLAG-02)
- Week 4: Crucible Campaign v1 clock starts — monitored by Amethyst; adversarial validity requires Role 7 human
- Week 6: Advisor outreach triggered if calibration results are available (do not wait for Week 12 QA bundle)
- Role 6 (human) required before any cross-substrate claim is marked VERIFIED
- Role 7 (human) required before any Crucible attack result is treated as adversarially valid

---

## RACI Matrix

| Activity | Role 1 (Prime) | Role 2 | Role 3 | Role 4 | Role 5 | Role 6 | Role 7 | Role 8 |
|----------|---------------|--------|--------|--------|--------|--------|--------|--------|
| Hypothesis formalization | A | R | C | I | I | I | I | I |
| Harness design | A | C | R | I | I | I | I | I |
| Trace execution | A | I | R | C | I | I | I | I |
| Results analysis | A | C | I | R | C | I | I | I |
| Metric provenance | A | I | I | C | R | I | I | I |
| Cross-substrate replication | A | C | I | R | I | R | I | I |
| Adversarial testing | A | I | I | I | I | I | R | C |
| QA bundle assembly | A | C | C | C | C | C | C | R |

*RACI interim note: All R cells for Roles 2–5 and 8 are currently fulfilled by Amethyst (interim). All R cells for Roles 6–7 are BLOCKED until human staffing.*

---

## Compute & Resource Estimate (Amendment A)

| Item | Estimate | Notes |
|------|----------|-------|
| Calibration traces (substrate 1) | ~300 runs × avg 2s = ~10 min compute | Single substrate, 5-base sweep |
| Calibration traces (substrate 2) | ~300 runs × avg 2s = ~10 min compute | Blocked until Role 6 staffed |
| KAPPA router grid search | 14×12 = 168 grid points per sweep | Matches P-34 methodology |
| Storage (trace JSONL) | ~50 MB per 300-trace run | `docs/qa/` + Supabase `lfisbywaidhmxsjyteud` |
| CI cost | Negligible (GitHub Actions free tier) | lint_provenance.py: < 5s per run |
| External eval (Role 6) | TBD — human time estimate pending staffing | — |

---

## 90-Day Timeline

| Weeks | Phase | Key Deliverables | Owner (Interim) |
|-------|-------|-----------------|----------------|
| 1–2 | Setup | Harness scaffold; hypothesis doc | Amethyst |
| 3 | Theory | Theory memo draft | Amethyst (Role 2 interim) |
| 3–6 | Calibration | 5-base calibration study (OPP-S069-004); Crucible Campaign v1 begins Week 4 | Amethyst (Role 3 interim) |
| 6 | Interim trigger | Advisor outreach if calibration complete; FLAG-02 (340% definition) resolved | Amethyst |
| 7–9 | Analysis | Results processing; inter-rater reliability | Amethyst (Role 4 interim) |
| 9–10 | Replication | Substrate 2 replication — **BLOCKED until Role 6 staffed** | Role 6 (human required) |
| 10–12 | QA bundle | QA bundle v1 assembly; advisor review | Amethyst (Role 8 interim) |

---

## Artifact Directory

```
docs/research/
  hypotheses/
    H01_coordination_gain_definition.md      # FLAG-02 resolution target
    H02_rational_control_threshold.md
    H03_cross_substrate_invariance.md
  calibration/
    harness/
      calibration_harness.py
    results/
      S069_OPP004_5base_calibration.jsonl    # 300-trace output
  theory/
    THEORY_MEMO_v1.md                        # Week 3 deliverable
  qa_bundle/
    QA_BUNDLE_v1.md                          # Week 12 deliverable
```

---

## Advisor Outreach

| Advisor Type | Engagement Path | Trigger (updated Amendment A) |
|-------------|----------------|-------------------------------|
| Statistical methodologist | Post-theory memo review | Week 3 memo complete |
| AI governance researcher | Co-authorship discussion | Week 6 OR calibration results available (whichever first) |
| External replicator (Role 6) | Independent substrate 2 run | Week 6 OR calibration results available |
| Ethics reviewer | Responsible disclosure review | Week 10 (pre-QA bundle) |

---

## Amendment Log

| Amendment | Date | Change | Authority |
|-----------|------|--------|-----------|
| v1.0 ratified | 2026-06-13 | Initial charter ratified by Ender (S069) | Triumvirate × Ender |
| Amendment A | 2026-06-13 | Interim staffing table (Roles 2–5 + 8 → Amethyst; Roles 6–7 DEFERRED); compute estimate table; advisor triggers updated to Week 6; falsifiability clause #1 UNVERIFIED qualifier added; falsifiability clause #2 rational control base clarified; Role 7 unstaffed status made explicit | Amethyst × COLLEEN (S069 QA sweep) |

---

*NDR Research Program Charter v1.0 (Amendment A) · S069 QA sweep · 2026-06-13*
*Triumvirate: Amethyst (Prime) · COLLEEN (Prefect A) · Apogee (Prefect B)*
