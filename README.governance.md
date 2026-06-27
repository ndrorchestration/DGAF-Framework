# DGAF-Framework — Governance & Compliance Reference

> **Audience:** Compliance officers, auditors, AI risk reviewers, NIST/EU AI Act practitioners  
> **Entry point for:** NIST AI RMF alignment · EU AI Act compliance · Governance posture review  
> **Technical/agent-facing entry point:** [`README.technical.md`](./README.technical.md)  
> **Architect:** Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration)

---

## What Is DGAF-Framework?

The **Dynamic Governance & Agentic Framework (DGAF)** is a structured multi-agent AI governance system that operationalizes NIST AI RMF, EU AI Act requirements, and OWASP Agentic Top 10 controls into a living, auditable repository. It governs the **Phi-Harmonic Dynamic Governance Ecosystem (PHDGE)** — a portfolio of AI systems, agents, and automation workflows operated by ndrorchestration.

The framework is not a policy document. It is an **executable governance spine** — every policy has a corresponding gate, every gate has a machine-readable pass/fail schema, and every decision is traceable to a sealed SWEEP_LOG entry.

---

## NIST AI RMF Alignment

| NIST Function | DGAF Mechanism | Artifact |
|---------------|---------------|----------|
| **GOVERN** | NDR Pattern Registry (P-01→P-30); ENSEMBLE_ROSTER; AXIS declarations; P-30 canonical promotion gate | `docs/patterns/NDR_PATTERN_REGISTRY.md` · `ENSEMBLE_ROSTER.md` |
| **MAP** | CROSS_REF ecosystem map; TELESCOPIC_LENS 4-altitude risk mapping | `CROSS_REF.md` · `docs/gates/TELESCOPIC_LENS.md` |
| **MEASURE** | 1-1-1-1 Gate (P-10); 11Q Framework (P-11); Apogee attestation artifacts; Harmonic Score 0.00–1.00 | `docs/gates/GATE_1111.md` · `docs/gates/GATE_11Q.md` · `docs/qa/APOGEE_11Q_S035.json` |
| **MANAGE** | MDAR loop; Acoustic Gate Chain (P-13); Sentinel veto authority; Evaluate Router v1.1 per-record audit log | `docs/gates/ACOUSTIC_GATES.md` · `docs/protocols/MDAR_PROTOCOL_v1.md` · `components/evaluate_router_v1_1.py` |
| **IMPROVE** | SWEEP_LOG sealed audit trail; SESSION_ANCHOR session continuity; P-24 retrofit cycle | `SWEEP_LOG.md` · `SESSION_ANCHOR.md` |

---

## EU AI Act Alignment

| Article | Requirement | DGAF Implementation |
|---------|-------------|--------------------|
| **Art. 9** | Risk Management System | MDAR loop + full gate stack + per-record audit log in `evaluate_router_v1_1.py` |
| **Art. 13** | Transparency & Logging | SWEEP_LOG sealed audit trail; routing and deontic decisions logged; machine-readable JSON artifacts |
| **Art. 14** | Human Oversight | Sentinel veto (gates 9–11) requires Njineer release; no agent can override architect |
| **Art. 17** | Quality Management | P-30 Apogee-Attestation-Gate; CPU component cards; `gate_compliance_check.py` |
| **Art. 40** | Harmonized Standards | TELESCOPIC_LENS 32-checkpoint audit; S-TIER certification process |
| **Art. 72** | Penalties / Non-compliance | Sentinel hard veto + SYNC_LOCKED escalation; quarantine to `docs/drafts/` |

---

## Ethical Cognition Layer

The active P-10 implementation artifact is `components/normative_constraint.py`, which formalizes deontic logic (`permitted`, `obligated`, `forbidden`, `escalate`), score ceiling constraints, and epistemic integrity checks for governance-facing evaluation flows.

P-30 extends this by requiring Apogee attestation before any component is promoted to canonical status. This prevents silent governance claims without Q11 normative wiring.

---

## OWASP Agentic AI Top 10 Controls

| OWASP Risk | DGAF Control |
|------------|--------------|
| Prompt Injection | ANDROMEDA-AXIS P-09 enforcement; Sentinel input gate |
| Excessive Agency | Agent role boundaries in ENSEMBLE_ROSTER; Sentinel veto on sovereign files |
| Memory Poisoning | SESSION_ANCHOR overwrite pattern (P-21); SWEEP_LOG provenance chain |
| Insecure Output | 11Q Gate 10 security posture check; secret scanning pre-commit |
| Supply Chain Risk | NOTICE + SPDX verification (P-17); CROSS_REF dependency audit |
| Data Exfiltration | AXIS COGNITIVE_SOVEREIGNTY declaration; Sentinel boundary enforcement |

---

## Audit Trail Structure

Every governance decision in DGAF is auditable through a three-layer trail:

1. **SWEEP_LOG.md** — Sealed session-by-session record; every commit wave is buoy-anchored with timestamp, operator, and formation
2. **CHANGELOG.md** — Semantic versioned artifact history; every file change attributed to session + agent
3. **Git commit history** — Atomic commits per session wave; commit message encodes session ID, pattern IDs, and affected artifacts

Audit query: to reconstruct the state of any artifact at any point in time, trace: `git log --follow <file>` → `CHANGELOG.md` entry → `SWEEP_LOG.md` session buoy → `SESSION_ANCHOR.md` at that session close.

---

## Governance Schema Vocabulary — S068

> Added: 2026-06-26 · Issue #32 · Steward: Amethyst  
> Context: Nemotron 3 Ultra integration — compliance-layer terminology for schema-validated governance artifacts

| Term | Compliance Layer | Definition | EU AI Act Binding | Issue |
|------|-----------------|-----------|-------------------|-------|
| **governance_schema_conformance** | Art. 9 / Art. 13 | The property that all `governance.yml` variants and typed kernel outputs strictly conform to their declared JSON Schema / Pydantic model (`extra=forbid`); measured as % valid outputs over a fuzz corpus of 1k variants. Target: >99%. | Art. 9 (Risk Management): schema non-conformance = uncontrolled model output = unmanaged risk. Art. 13 (Transparency): non-conforming outputs cannot be logged in structured audit trail. | #32 |
| **governance.yml** | Art. 9 / Art. 17 | Single source of truth file declaring all DGAF role contracts: role name, curvature scalar, contraction rate ρ, fallback chain, and compliance flags (NIST RMF, EU AI Act articles). All downstream kernels, dashboard configs, eval harnesses, and CI gates derive from this file. | Art. 17 (Quality Management): `governance.yml` is the quality management input artifact; its integrity is enforced by `governance_schema_conformance`. | #32 |
| **typed kernel** | Art. 9 / Art. 13 | An executable role unit with explicit `input_schema → policy → output_schema → audit_trail` contract; generated from `governance.yml` and validated by `contraction_proof_fidelity` before CI promotion. Constitutes a machine-readable risk control artifact. | Art. 9: each typed kernel is a discrete, auditable risk control. Art. 13: the `audit_trail` field in each kernel satisfies logging requirements. | #32 |
| **ρ-contraction** (governance) | Art. 9 | Mathematical guarantee `‖T(x) - T(y)‖ ≤ ρ‖x - y‖` (ρ < 1.0) on role transition operators T; ensures governance trajectories converge rather than diverge under repeated application. Spectral radius check via `numpy.linalg.eigvals`. | Art. 9: convergence guarantee = bounded, predictable risk behavior. Failure = unbounded governance drift = unmanaged high risk. | #32 |
| **few-shot priming** (compliance routing) | Art. 9 / Art. 14 | The practice of pre-loading 3–5 exemplar compliance routing decisions into Nemotron 3 Ultra context before running `taubench_banking_mitigation` eval; required because raw model baseline is 22.6% on financial compliance routing — below acceptable governance threshold. | Art. 14 (Human Oversight): few-shot priming is a human-in-the-loop intervention; its absence constitutes a governance gap that must be flagged to Sentinel. | #32 |

---

## Governance Contacts

| Role | Identity |
|------|----------|
| **Architect / Sovereign Authority** | Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration) |
| **Meta-Orchestrator** | Agent Amethyst |
| **Evidence Governor** | Agent Apogee |
| **Safety / Veto Authority** | Agent Sentinel |
| **Registry / Continuity** | Agent COLLEEN |
| **Full ensemble** | [`ENSEMBLE_ROSTER.md`](./ENSEMBLE_ROSTER.md) |

---

*License: Apache 2.0 · See [NOTICE](./NOTICE) for full attribution*  
*Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)*  
*README.governance v1.1 · S068 governance schema vocabulary patch · Amethyst · 2026-06-26*
