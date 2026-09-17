# Needle Template Registry

<!-- DGAF Governance Layer: docs/needle/TEMPLATE_REGISTRY.md -->
<!-- Status: CURRENT CROSS-REFERENCE / HISTORICAL INTERNAL REVIEW SNAPSHOT | Updated: 2026-09-17 | Owner: ndrorchestration -->
<!-- Historical review provenance: P-30 PASS | COLLEEN 1-1-1-1 PASS | Apogee Composite Avg: 0.958 | snapshot 2026-06-13 -->
<!-- METRICS SNAPSHOT: 2026-06-13 (NMS-003). Metrics below are dated and may be stale. -->

## Purpose

This registry is the canonical project cross-reference between Needle.app workflow
templates, DGAF NDR patterns, NIST AI RMF controls, and ISO/IEC 42001 clauses.
Registry inclusion records internal review, provenance, and link verification at the
stated snapshot. It does not establish certification, endorsement, compliance, or standards conformance.

Historical P-30, COLLEEN, and Apogee labels below are retained as internal review
provenance. Current authority semantics resolve through functional DGAF roles and
project-local evidence; a historical persona or gate label does not grant current
authority.

**Partner Directory:** [needle.app/partners-directory/ndr-ai-orchestration](https://needle.app/partners-directory/ndr-ai-orchestration)

---

## Registry Table

| Template ID | Template Name | NDR Pattern(s) | NIST AI RMF Crosswalk | ISO/IEC 42001 Crosswalk | Needle Link | Internal Registry Status |
|---|---|---|---|---|---|---|
| NT-01 | Evaluate LLM Output Quality | P-03, P-11 | GOVERN 1.7, MEASURE 2.5 | §8.4 | [Run →](https://needle.app/workflow-templates/evaluate-ai-output-quality) | INTERNAL REVIEW PASS — 2026-06 snapshot |
| NT-02 | Generate Grounded KB Answers | P-05 | MANAGE 2.2 | §8.4 | [Run →](https://needle.app/workflow-templates/generate-grounded-knowledge-base-answers) | INTERNAL REVIEW PASS — 2026-06 snapshot |
| NT-03 | KB Answer With Quality Check | P-05, P-11, P-30 | MEASURE 2.9 | §9.1 | [Run →](https://needle.app/workflow-templates/kb-answer-with-quality-check) | INTERNAL REVIEW PASS — 2026-06 snapshot |
| NT-04 | Define AI Governance Specification | P-03, P-30 | GOVERN 1.7 | §6.1, §9.1 | [Run →](https://needle.app/workflow-templates/implement-governance-multi-agent-orchestration) | INTERNAL REVIEW PASS — 2026-06 snapshot |
| NT-05 | Test Governance API Gates | P-03, P-30 | GOVERN 1.7, MEASURE 2.5, MEASURE 2.9, MANAGE 2.2 | §8.4, §9.1 | [Run →](https://needle.app/workflow-templates/test-governance-api-gates) | CANONICAL PROBE |

---

## Historical Internal Review Summary

These scores are dated project-internal review records. They are not third-party
certification, external endorsement, or proof of standards conformance.

| Template | Composite Score | Internal Verdict | Recorded By / Date |
|---|---|---|---|
| NT-01 | 0.955 | PASS | Ender — 2026-06-09 |
| NT-02 | 0.944 | PASS | Ender — 2026-06-09 |
| NT-03 | 0.970 | PASS | Ender — 2026-06-09 |
| NT-04 | 0.962 | PASS | Ender — 2026-06-09 |

Attestation/review records: [ai-prompt-systems-portfolio/docs/qa/](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/docs/qa)

---

## Pattern Reference

| NDR Pattern | Name | Role in Template Execution |
|---|---|---|
| P-03 | Governance Contract Test | Validates template outputs against a declared governance spec |
| P-05 | Tri-Phase CI Gate | Enforces retrieve → generate → evaluate pipeline integrity |
| P-11 | 11Q Attestation Scoring | Records project-internal output-quality scoring across 11 dimensions |
| P-30 | Apogee Attestation Gate | Historical internal verification gate used for the dated registry review |

For current authority mapping, legacy `Apogee` review semantics resolve to
`role.evidence-verification-reviewer` through `governance/persona_role_lineage.v1.json`.
That role is a scoped verification function and does not create execution,
authorship, normative authorization, certification, or standards-conformance authority.

---

## NIST AI RMF Crosswalk

The table is a project crosswalk to relevant NIST AI RMF concepts. It identifies
where a template may exercise behavior related to a control; it does not claim that
the template, repository, or operator is NIST-certified, compliant, or conformant.

| NIST Function | Control | Mapped Templates |
|---|---|---|
| GOVERN | 1.7 — Human oversight documentation | NT-01, NT-04 |
| MEASURE | 2.5 — Output reliability measurement | NT-01 |
| MEASURE | 2.9 — Combined eval + audit chain | NT-03 |
| MANAGE | 2.2 — RAG as hallucination mitigation | NT-02 |

---

## ISO/IEC 42001 Crosswalk

The table is a project crosswalk to potentially relevant ISO/IEC 42001 clauses.
It is not a certification statement, management-system audit, or claim that the
listed requirements have been satisfied in an accredited conformity-assessment sense.

| Clause | Requirement | Mapped Templates |
|---|---|---|
| §6.1 | AI risk identification and treatment | NT-04 |
| §8.4 | Operational control of AI systems | NT-01, NT-02 |
| §9.1 | Monitoring, measurement, analysis | NT-03, NT-04 |

---

## Inclusion Criteria

A template may be added to this project registry only when:

1. NDR pattern cross-reference is confirmed in `docs/ndr_patterns_unified.json`.
2. A documented project-internal evidence/verification review is completed; any legacy P-30/Apogee record is treated as historical review provenance rather than certification.
3. NIST/ISO crosswalk mappings are checked against the applicable primary standard/framework text and labeled as crosswalks rather than conformance claims.
4. The Needle template URL is confirmed stable by the template owner.
5. The applicable project-local semantic/logical/visual/ethical QA record is retained with its scope and date.

Registry inclusion does not transfer DGAF authorization or evidence state into a
template and does not substitute for independent review where independence is a
claim requirement.

---

## Ecosystem Links

- [NDR Pattern Registry (Unified)](../NDR_PATTERN_REGISTRY_UNIFIED.md)
- [NDR Patterns JSON](../ndr_patterns_unified.json)
- [Workspace Bootstrap](../WORKSPACE_BOOTSTRAP.md)
- [Ecosystem Inventory](../ECOSYSTEM_INVENTORY.md)
- [ai-governance-frameworks: NIST/ISO docs](https://github.com/ndrorchestration/ai-governance-frameworks/tree/main/docs/needle-templates)
- [ai-prompt-systems-portfolio: Prompt specs](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/specs/needle)
- [Historical internal review records](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/docs/qa)
- [Needle Partner Directory](https://needle.app/partners-directory/ndr-ai-orchestration)

---

## Last Measured Metrics

> **Snapshot:** NMS-003 — 2026-06-13 7 PM EDT | Session S071 | Window: Mar 15 – Jun 13, 2026

| Template | Views | Uses | Runs | Use Rate | Run/Use |
|----------|-------|------|------|----------|---------|
| NT-01 Evaluate LLM Output Quality | 3,613 | 479 | 1,064 | 13.3% | 2.22x |
| NT-02 Generate Grounded KB Answers | 3,453 | 444 | 1,394 | 12.9% | 3.14x |
| NT-03 KB Answer With Quality Check | 2,491 | 229 | 476 | 9.2% | 2.08x |
| NT-04 Define AI Governance Specification | 1,777 | 159 | 320 | 8.9% | 2.01x |
| NT-05 Test Governance API Gates | 93 | — | — | — | — |
| **90d Totals** | **11,374** | **1,311** | **3,254** | **11.5%** | **2.48x** |

Historical metrics snapshot recorded 2026-06-13 under legacy session owner label `Agent Amethyst` / S071. This attribution is provenance only, not current authority.
