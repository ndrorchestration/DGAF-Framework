# DGAF-Framework — Governance & Standards Crosswalk Reference

> **Audience:** Auditors, AI risk reviewers, governance practitioners, and technical reviewers  
> **Entry point for:** NIST AI RMF project mapping · EU AI Act conceptual crosswalk · OWASP agentic-risk crosswalk · governance posture review  
> **Plain-English terminology:** [`docs/PUBLIC_TRANSLATION_LAYER.md`](./docs/PUBLIC_TRANSLATION_LAYER.md)  
> **Technical/agent-facing entry point:** [`README.technical.md`](./README.technical.md)  
> **Architect:** Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration)

---

## Scope and Evidence Boundary

The **Dynamic Governance Agentic Formation (DGAF)** is a structured multi-agent governance research and implementation framework. The repository contains governance specifications, selected executable controls, CI gates, role/authority contracts, audit records, evidence/provenance mechanisms, presentation-layer governance projections, and a bounded machine-readable recurring-assurance catalog.

Some DGAF artifacts are **mapped** to concepts in the NIST AI Risk Management Framework (AI RMF), Regulation (EU) 2024/1689 (the EU AI Act), ISO/IEC 42001, and the OWASP Top 10 for Agentic Applications. These mappings are project-local traceability aids. They are **not** a legal-compliance determination, certification, conformity assessment, security certification, or claim that every external requirement has been implemented or independently validated.

> **Terminology authority:** `docs/taxonomy/NDR_ACRONYM_REGISTRY.md`. Earlier DGAF/PDMAL expansions are historical provenance and must not be presented as current vocabulary authority.

DGAF includes an **executable governance spine for selected controls**. A policy is not assumed to be technically enforced unless a corresponding implementation and scoped verification evidence are identified. Likewise, a decision is not assumed to have a complete audit chain unless the relevant repository artifacts establish that chain.

**Current scientific boundary:** the canonical High-Assurance program remains **PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0**. This is separate from **Track A Epoch 002**, whose governed prospective blinded collection is **COMPLETE** at **50 paired inferential seed units / 2,250 blinded observations**. Its dataset lock is **ESTABLISHED** and bounded unblinding is **AUTHORIZED only for controlled mapping release/decryption**. The accepted Stage-1/Stage-2 materialization apparatus and prospective primary-analysis authorization tooling are tooling/preparation only: real materialization is **NOT ESTABLISHED**, repository `MATERIALIZATION_RECEIPT` is **NOT ESTABLISHED**, positive primary-analysis authorization is **NOT ESTABLISHED**, primary analysis is **NOT AUTHORIZED / NOT RUN**, `SCIENTIFIC_N_INCREMENT=0`, and canonical DGAF efficacy and independent validation remain **NOT_ESTABLISHED**. Track A Epoch 001 remains historical blinded-collection/custody-failure provenance and is not pooled into Epoch 002. See [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) for the live cross-track state.

**Current repository-control boundary:** protected `main` at the 2026-09-17 reconciliation is `6b89529da3e7ff13e14eaea415756579d859fb26`. The accepted assurance catalog remains `PARTIAL_CORE_FAMILIES_ONLY`; the Governance Command Center's Decision Frontier and Governance Map remain presentation-only projections. Neither documentation, UI state, catalog membership, nor standards mapping alters scientific or authorization state.

---

## Repository Assurance Inventory

DGAF now contains a versioned repository-local recurring-assurance inventory:

- `registry/audit_catalog.v1.json` — bounded machine-readable catalog;
- `registry/audit_catalog.py` — deterministic loading, validation, and coverage-gap helpers;
- focused tests under `tests/` for catalog structure, exact implementation bindings, and workflow coverage behavior.

Accepted progression:

1. **PR #780** established the initial bounded catalog and validator.
2. **PR #782** added deterministic discovery of current `.github/workflows/*.yml|*.yaml` definitions not exactly bound by catalog implementation paths.
3. **PR #785** added seven source-verified recurring assurance families while preserving `coverage.status = PARTIAL_CORE_FAMILIES_ONLY`.

Interpretation rules:

- **Cataloged recurring assurance** means the repository has an explicit current mapping for that family and implementation path.
- **Unmapped / unclassified** means only that the current catalog has not adjudicated that workflow; it is not evidence that the workflow is non-assurance.
- **Protected-branch requiredness** is a separate repository property. Current protected-main readback identifies **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard** as required contexts.
- A workflow can be a recurring assurance family without being a required merge context.
- Catalog coverage does not establish exhaustive security, governance, scientific, compliance, or audit coverage.

Known catalog gaps include wider workflow/script/test classification, exact job/workflow/ruleset mapping, shared-dependency and independence analysis, external-runtime ingress assurance, presentation-projection coverage, and historical family-versus-execution-instance reconciliation.

---

## Governance Presentation Surfaces

The Governance Command Center now includes accepted presentation-only Semantic Control Field components:

- **Decision Frontier — PR #776**: exposes current governed state, supporting evidence/provenance, blocking boundary, nearest admissible transition, unreachable transitions, consequence preview, and receipt semantics.
- **Governance Map — PR #779**: exposes ordered vertical escalation, explicitly named lateral relationships, and global field conditions derived from the normalized governance model.

These surfaces improve inspectability but do not independently grant authority, establish evidence, or create a new state engine. They intentionally avoid readiness percentages and continuous/manifold implications where no formal semantics exist.

Any later State-Space Explorer remains candidate work until merged into protected `main`. Conceptual tensor/manifold research is non-authoritative guidance unless exact representation semantics are implemented and verified.

---

## NIST AI RMF Project Mapping

NIST AI RMF 1.0 defines four Core functions: **GOVERN, MAP, MEASURE, and MANAGE**. The table below records DGAF artifacts that are conceptually or operationally relevant to those functions; it is not a NIST certification or completeness claim.

| NIST AI RMF Function | DGAF project relation | Example artifacts | Evidence boundary |
|---|---|---|---|
| **GOVERN** | Role/authority definitions, pattern governance, claim/evidence controls, promotion gates, and explicit control-state projections | `governance/role_capability_registry.v1.json` · `registry/audit_catalog.v1.json` · Decision Frontier / Governance Map | Mapping and repository implementation are artifact-specific; no framework-wide NIST conformance claim. |
| **MAP** | Ecosystem/context mapping and project-local risk/architecture decomposition | `CROSS_REF.md` · `docs/gates/TELESCOPIC_LENS.md` | Supports project context mapping; completeness against AI RMF MAP outcomes has not been independently established. |
| **MEASURE** | Evaluation gates, structured evidence, recurring-assurance inventory, per-record audit data, and scoped test artifacts | `docs/gates/GATE_1111.md` · `components/evaluate_router_v1_1.py` · repository CI/evidence artifacts | Passing repository tests establishes only their declared scope; it does not validate all AI-risk measures or outcomes. |
| **MANAGE** | Fail-closed gates, escalation/authority controls, recovery patterns, and project-local risk-response mechanisms | `docs/gates/ACOUSTIC_GATES.md` · `docs/protocols/MDAR_PROTOCOL_v1.md` · role/authority contracts | Mechanism existence does not establish risk-reduction efficacy or organizational AI RMF adoption. |

**Continuous improvement** is a DGAF project activity, but it is **not a fifth AI RMF Core function**. NIST describes ongoing monitoring and improvement within the four-function risk-management process.

---

## EU AI Act Conceptual Crosswalk

The EU AI Act imposes obligations according to regulated role, system classification, use context, and other legal conditions. DGAF has **not** been assessed here for applicability, provider/deployer status, high-risk classification, conformity, or legal compliance. The table is therefore a conceptual engineering crosswalk only.

| EU AI Act provision | External requirement theme | DGAF project relation | Status / limitation |
|---|---|---|---|
| **Article 9** | Risk management system for high-risk AI systems | Project-local risk/gate specifications, escalation controls, evidence records, and iterative review mechanisms | Relevant design concepts only; no Article 9 compliance determination. |
| **Article 12** | Record-keeping / automatic logging for high-risk AI systems | SWEEP_LOG, Git history, structured evaluation/audit records, recurring-assurance catalog, and per-record logs in selected components | Repository logging may support traceability; it does not establish all Article 12 technical logging requirements. |
| **Article 13** | Transparency and information to deployers | Public/internal documentation, structured artifacts, role/authority descriptions, state projections, and evidence-status disclosure | Partial conceptual crosswalk; no finding that all required instructions/information are present. |
| **Article 14** | Human oversight | Human override, HITL gates, explicit authority boundaries, and fail-closed escalation in selected workflows | Mechanism-level relation only; no Article 14 conformity assessment. |
| **Article 17** | Quality management system | Governance procedures, QA/evidence workflows, change history, role assignments, assurance inventory, and documentation controls | DGAF artifacts may inform a QMS; this repository is not asserted to constitute a complete Article 17 QMS. |
| **Article 40** | Harmonised standards | External standards may be referenced during design/review | DGAF's internal S-TIER/legacy Gold Star labels are **not harmonised standards** and are not evidence of Article 40 conformity. |
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
| **ASI03 — Identity & Privilege Abuse** | Explicit functional authority boundaries and signer/identity verification work | Production signer/trust admission remains separately gated; no complete privilege-security claim. |
| **ASI04 — Agentic Supply Chain Vulnerabilities** | Dependency locking, provenance checks, Sigstore verification work, IP/dependency hygiene | Verification mechanisms are scoped; final production trust policy and external admission evidence remain open. |
| **ASI05 — Unexpected Code Execution (RCE)** | Action/tool gates, human authorization boundaries, fail-closed execution contracts | No claim of comprehensive RCE prevention. |
| **ASI06 — Memory & Context Poisoning** | Session/provenance records, evidence boundaries, controlled rehydration guidance | Supports traceability and contamination detection concepts; mitigation efficacy is not established. |
| **ASI07 — Insecure Inter-Agent Communication** | Functional role/protocol contracts and controlled handoff specifications | Does not establish secure transport, authentication, or complete inter-agent communications security. |
| **ASI08 — Cascading Failures** | Fail-closed gates, recovery/Saga patterns, crash/retry controls | Structural mechanisms exist; empirical reduction of cascading failures remains unproven. |
| **ASI09 — Human-Agent Trust Exploitation** | Claim hygiene, uncertainty disclosure, human override, and evidence-state separation | Supports calibrated-trust practices; no effectiveness certification. |
| **ASI10 — Rogue Agents** | Authority constraints, human override, veto/escalation and execution boundaries | No claim that rogue-agent behavior is eliminated. |

The repository may also contain older OWASP/agentic threat terminology. Historical labels should not be presented as the current OWASP Top 10 taxonomy unless explicitly versioned and mapped.

---

## Audit and Provenance Surfaces

DGAF provides complementary trace surfaces. Their presence improves inspectability, but **coverage is not assumed universal**.

1. **Machine-readable assurance catalog** — maps selected recurring assurance families, implementation paths, bounded verdicts, decision effects, non-effects, failure behavior, and known gaps.
2. **Workflow coverage-gap scanner** — identifies current workflow definitions not exactly represented in the accepted catalog without inferring their assurance role.
3. **SWEEP_LOG / session records** — where present, record session-level decisions and changes.
4. **CHANGELOG.md** — records selected semantic/project history.
5. **Git commit and pull-request history** — records versioned repository mutations and review/CI lineage.
6. **Evidence/control-state artifacts** — bind selected claims, candidates, workflow runs, artifacts, or gates to explicit identities.
7. **Governance Command Center / ORBIT projections** — expose current state and provenance for inspection but are not independent authorities.

For a particular claim or decision, reconstruct only the chain actually supported by retained artifacts. Missing links must remain **UNKNOWN / NOT VERIFIED / UNCLASSIFIED**, not be filled by inference.

---

## Evidence Interpretation Rules

- **Mapped** means a project artifact has a documented relationship to an external concept or requirement.
- **Cataloged recurring assurance** means an accepted machine-readable mapping exists for the selected family/path; it does not imply branch-protection requiredness.
- **Implemented** means a relevant mechanism exists in repository code/configuration.
- **Verified** means a bounded test/check succeeded for its declared identity and scope.
- **Authorized** means a governing record permits the bounded action it names; it does not mean the action already occurred or succeeded.
- **Empirically supported** requires admissible observations under the applicable controlled protocol.
- **Unmapped / unclassified** means the repository has not yet made the requested assurance-role determination.
- None of these labels automatically means **legally compliant**, **certified**, **secure**, **safe**, **effective**, **deployed**, or **production healthy** beyond the evidence actually retained.

For current experimental authority and gate status, use [`docs/CURRENT_STATE.md`](./docs/CURRENT_STATE.md) first, then the exact governing artifacts for the relevant High-Assurance or workload-specific track.

---

## Governance Contacts and Functional Authority

Current machine/agent authority is role-based. Persona labels are compatibility/provenance identifiers and do not independently grant an authority seat.

| Role | Current identity / authority source |
|---|---|
| **Architect / Human Authority** | Hensel, Andrew Vance · [@ndrorchestration](https://github.com/ndrorchestration) |
| **Governance Orchestrator** | `role.governance-orchestrator` · `governance/role_capability_registry.v1.json` |
| **Evidence & Verification Reviewer** | `role.evidence-verification-reviewer` · `governance/role_capability_registry.v1.json` |
| **Security & Containment Gate** | `role.security-containment-gate` · `governance/role_capability_registry.v1.json` |
| **Continuity & Archive Coordinator** | `role.continuity-archive-coordinator` · `governance/role_capability_registry.v1.json` |
| **Historical persona lineage** | [`governance/persona_role_lineage.v1.json`](./governance/persona_role_lineage.v1.json) |

---

*License: Apache 2.0 · See [NOTICE](./NOTICE) for full attribution*  
*Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)*  
*README.governance v1.7 · assurance-catalog / semantic-control-field reconciliation · 2026-09-17*
