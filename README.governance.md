# DGAF-Framework — Governance & Standards Crosswalk Reference

> **Audience:** Auditors, AI risk reviewers, governance practitioners, and technical reviewers  
> **Entry point for:** NIST AI RMF project mapping · EU AI Act conceptual crosswalk · OWASP agentic-risk crosswalk · governance posture review  
> **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md)  
> **Technical/agent-facing entry point:** [`README.technical.md`](./README.technical.md)  
> **Architect:** Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration)

---

## Scope and Evidence Boundary

The **Dynamic Governance Agentic Formation (DGAF)** is a structured multi-agent governance research and implementation framework. The repository contains governance specifications, selected executable controls, CI gates, role/authority contracts, audit records, and evidence/provenance mechanisms.

Some DGAF artifacts are **mapped** to concepts in the NIST AI Risk Management Framework (AI RMF), Regulation (EU) 2024/1689 (the EU AI Act), and the OWASP Top 10 for Agentic Applications. These mappings are project-local traceability aids. They are **not** a legal-compliance determination, certification, conformity assessment, security certification, or claim that every external requirement has been implemented or independently validated.

> **Terminology authority:** `docs/taxonomy/NDR_ACRONYM_REGISTRY.md`. Earlier DGAF/PDMAL expansions are historical provenance and must not be presented as current vocabulary authority.

DGAF includes an **executable governance spine for selected controls**. A policy is not assumed to be technically enforced unless a corresponding implementation and scoped verification evidence are identified. Likewise, a decision is not assumed to have a complete audit chain unless the relevant repository artifacts establish that chain.

**Current scientific boundary:** the canonical High-Assurance program remains **PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0**. This is separate from **Track A Epoch 001**, whose governed prospective blinded collection is complete with **50 paired inferential seed units / 2,250 blinded raw observations**, dataset lock and unblinding authorization established, and materializer/receipt/custody-preflight/primary-analysis-authorization tooling merged and validated. The matching custody-key handoff is **NOT ESTABLISHED**, the unblinded analysis input is **NOT YET MATERIALIZED**, primary analysis is **NOT AUTHORIZED / NOT RUN**, and canonical DGAF efficacy remains **NOT ESTABLISHED**. See [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) for the live cross-track state. Governance documentation or standards mapping does not alter either boundary.

---

## NIST AI RMF Project Mapping

NIST AI RMF 1.0 defines four Core functions: **GOVERN, MAP, MEASURE, and MANAGE**. The table below records DGAF artifacts that are conceptually or operationally relevant to those functions; it is not a NIST certification or completeness claim.

| NIST AI RMF Function | DGAF project relation | Example artifacts | Evidence boundary |
|---|---|---|---|
| **GOVERN** | Role/authority definitions, pattern governance, claim/evidence controls, and promotion gates | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` · `ENSEMBLE_ROSTER.md` · `docs/taxonomy/NDR_ACRONYM_REGISTRY.md` | Mapping and repository implementation are artifact-specific; no framework-wide NIST conformance claim. |
| **MAP** | Ecosystem/context mapping and project-local risk/architecture decomposition | `CROSS_REF.md` · `docs/gates/TELESCOPIC_LENS.md` | Supports project context mapping; completeness against AI RMF MAP outcomes has not been independently established. |
| **MEASURE** | Evaluation gates, structured evidence, per-record audit data, and scoped test artifacts | `docs/gates/GATE_1111.md` · `components/evaluate_router_v1_1.py` · repository CI/evidence artifacts | Passing repository tests establishes only their declared scope; it does not validate all AI-risk measures or outcomes. |
| **MANAGE** | Fail-closed gates, escalation/authority controls, recovery patterns, and project-local risk-response mechanisms | `docs/gates/ACOUSTIC_GATES.md` · `docs/protocols/MDAR_PROTOCOL_v1.md` · role/authority contracts | Mechanism existence does not establish risk-reduction efficacy or organizational AI RMF adoption. |

**Continuous improvement** is a DGAF project activity, but it is **not a fifth AI RMF Core function**. NIST describes ongoing monitoring and improvement within the four-function risk-management process.

---

## EU AI Act Conceptual Crosswalk

The EU AI Act imposes obligations according to regulated role, system classification, use context, and other legal conditions. DGAF has **not** been assessed here for applicability, provider/deployer status, high-risk classification, conformity, or legal compliance. The table is therefore a conceptual engineering crosswalk only.

| EU AI Act provision | External requirement theme | DGAF project relation | Status / limitation |
|---|---|---|---|
| **Article 9** | Risk management system for high-risk AI systems | Project-local risk/gate specifications, escalation controls, evidence records, and iterative review mechanisms | Relevant design concepts only; no Article 9 compliance determination. |
| **Article 12** | Record-keeping / automatic logging for high-risk AI systems | SWEEP_LOG, Git history, structured evaluation/audit records, and per-record logs in selected components | Repository logging may support traceability; it does not establish all Article 12 technical logging requirements. |
| **Article 13** | Transparency and information to deployers | Public/internal documentation, structured artifacts, role/authority descriptions, and evidence-status disclosure | Partial conceptual crosswalk; no finding that all required instructions/information are present. |
| **Article 14** | Human oversight | Human override, HITL gates, explicit authority boundaries, and fail-closed escalation in selected workflows | Mechanism-level relation only; no Article 14 conformity assessment. |
| **Article 17** | Quality management system | Governance procedures, QA/evidence workflows, change history, role assignments, and documentation controls | DGAF artifacts may inform a QMS; this repository is not asserted to constitute a complete Article 17 QMS. |
| **Article 40** | Harmonised standards | External standards may be referenced during design/review | DGAF's internal S-TIER/Gold Star labels are **not harmonised standards** and are not evidence of Article 40 conformity. |
| **Article 72** | Post-market monitoring for high-risk AI systems | Runtime telemetry, audit/provenance concepts, and monitoring designs may inform future post-market processes | No verified Article 72 post-market monitoring system is claimed. |

**Correction note:** an earlier version of this README described Article 72 as a penalties/non-compliance provision. Article 72 concerns post-market monitoring. Administrative penalties are addressed elsewhere in the Regulation, including Article 99 in the consolidated text. DGAF does not implement or enforce statutory penalties.

---

## Ethical and Normative Control Layer

The active P-10 implementation artifact is `components/normative_constraint.py`. It implements project-local deontic states such as `permitted`, `obligated`, `forbidden`, and `escalate`, together with score-ceiling and epistemic-integrity checks for selected governance-facing evaluation flows.

This is **implementation evidence for that component**, not evidence that DGAF satisfies every ethical, regulatory, or governance requirement associated with those concepts.

Promotion and attestation mechanisms elsewhere in the repository should be interpreted in the same way: a gate establishes only the decision/evidence contract actually implemented and tested by that gate.

---

## OWASP Top 10 for Agentic Applications 2026 — Project Crosswalk

OWASP's 2026 Agentic Top 10 uses the ASI01–ASI10 taxonomy below. DGAF artifacts are listed as **potential mitigation relationships**, not as proof that the corresponding risk is eliminated or that DGAF has passed an OWASP security certification.

| OWASP 2026 risk | DGAF project relation | Current evidence boundary |
|---|---|---|
| **ASI01 — Agent Goal Hijack** | Input/governance constraints, authority checks, epistemic gates | Candidate mitigation relationship; adversarial effectiveness not established by this mapping. |
| **ASI02 — Tool Misuse & Exploitation** | Tool/role boundaries, HITL gates, effect/reversibility controls | Selected mechanisms exist; comprehensive tool-misuse prevention is not claimed. |
| **ASI03 — Identity & Privilege Abuse** | Explicit agent authority boundaries and signer/identity verification work | Production signer/trust admission remains separately gated; no complete privilege-security claim. |
| **ASI04 — Agentic Supply Chain Vulnerabilities** | Dependency locking, provenance checks, Sigstore verification work, IP/dependency hygiene | Verification mechanisms are scoped; final production trust policy and external admission evidence remain open. |
| **ASI05 — Unexpected Code Execution (RCE)** | Action/tool gates, human authorization boundaries, fail-closed execution contracts | No claim of comprehensive RCE prevention. |
| **ASI06 — Memory & Context Poisoning** | Session/provenance records, evidence boundaries, controlled rehydration guidance | Supports traceability and contamination detection concepts; mitigation efficacy is not established. |
| **ASI07 — Insecure Inter-Agent Communication** | Agent role/protocol contracts and controlled handoff specifications | Does not establish secure transport, authentication, or complete inter-agent communications security. |
| **ASI08 — Cascading Failures** | Fail-closed gates, recovery/Saga patterns, crash/retry controls | Structural mechanisms exist; empirical reduction of cascading failures remains unproven. |
| **ASI09 — Human-Agent Trust Exploitation** | Claim hygiene, uncertainty disclosure, human override, and evidence-state separation | Supports calibrated-trust practices; no effectiveness certification. |
| **ASI10 — Rogue Agents** | Authority constraints, human override, veto/escalation and execution boundaries | No claim that rogue-agent behavior is eliminated. |

The repository may also contain older OWASP/agentic threat terminology. Historical labels should not be presented as the current OWASP Top 10 taxonomy unless explicitly versioned and mapped.

---

## Audit and Provenance Surfaces

DGAF provides several complementary trace surfaces. Their presence improves inspectability, but **coverage is not assumed universal**.

1. **SWEEP_LOG / session records** — where present, record session-level decisions and changes.
2. **CHANGELOG.md** — records selected semantic/project history.
3. **Git commit and pull-request history** — records versioned repository mutations and review/CI lineage.
4. **Evidence/control-state artifacts** — bind selected claims, candidates, workflow runs, artifacts, or gates to explicit identities.

For a particular claim or decision, reconstruct only the chain actually supported by retained artifacts. Missing links must remain **UNKNOWN / NOT VERIFIED**, not be filled by inference.

---

## Evidence Interpretation Rules

- **Mapped** means a project artifact has a documented relationship to an external concept or requirement.
- **Implemented** means a relevant mechanism exists in repository code/configuration.
- **Verified** means a bounded test/check succeeded for its declared identity and scope.
- **Authorized** means a governing record permits the bounded action it names; it does not mean the action already occurred or succeeded.
- **Empirically supported** requires admissible observations under the applicable controlled protocol.
- None of these labels automatically means **legally compliant**, **certified**, **secure**, **safe**, or **effective** beyond the evidence actually retained.

For current experimental authority and gate status, use [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) first, then the exact governing artifacts for the relevant High-Assurance or workload-specific track.

---

## Governance Contacts

| Role | Identity |
|---|---|
| **Architect / Sovereign Authority** | Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration) |
| **Meta-Orchestrator** | Agent Amethyst |
| **Evidence Governor** | Agent Apogee |
| **Safety / Veto Authority** | Agent Sentinel |
| **Registry / Continuity** | Agent COLLEEN |
| **Full ensemble** | [`ENSEMBLE_ROSTER.md`](./ENSEMBLE_ROSTER.md) |

---

*License: Apache 2.0 · See [NOTICE](./NOTICE) for full attribution*  
*Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)*  
*README.governance v1.5 · public-state reconciliation · 2026-09-08*
