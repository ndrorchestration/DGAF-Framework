# Needle Template Registry
<!-- DGAF Governance Layer: docs/needle/TEMPLATE_REGISTRY.md -->
<!-- Status: GOLD STAR CERTIFIED | Last Updated: 2026-06-12 | Session: S070 | Owner: ndrorchestration --><!-- P-30: PASS | COLLEEN 1-1-1-1: PASS | Apogee Composite Avg: 0.958 -->

## Purpose
This registry is the canonical cross-reference between Needle.app workflow
templates, DGAF NDR patterns, NIST AI RMF controls, and ISO 42001 clauses.
Templates listed here are endorsed runnable implementations of their
corresponding NDR patterns. All templates have passed Apogee Attestation Gate
(P-30), COLLEEN 1-1-1-1 audit, and Needle URL verification.

**Partner Directory:** [needle.app/partners-directory/ndr-ai-orchestration](https://needle.app/partners-directory/ndr-ai-orchestration)

---

## Registry Table

| Template ID | Template Name | NDR Pattern(s) | NIST AI RMF Controls | ISO 42001 | Needle Link | Status |
|---|---|---|---|---|---|---|
| NT-01 | Evaluate LLM Output Quality | P-03, P-11 | GOVERN 1.7, MEASURE 2.5 | §8.4 | [Run →](https://needle.app/workflow-templates/evaluate-ai-output-quality) | ⭐ GOLD STAR |
| NT-02 | Generate Grounded KB Answers | P-05 | MANAGE 2.2 | §8.4 | [Run →](https://needle.app/workflow-templates/generate-grounded-knowledge-base-answers) | ⭐ GOLD STAR |
| NT-03 | KB Answer With Quality Check | P-05, P-11, P-30 | MEASURE 2.9 | §9.1 | [Run →](https://needle.app/workflow-templates/kb-answer-with-quality-check) | ⭐ GOLD STAR |
| NT-04 | Define AI Governance Specification | P-03, P-30 | GOVERN 1.7 | §6.1, §9.1 | [Run →](https://needle.app/workflow-templates/implement-governance-multi-agent-orchestration) | ⭐ GOLD STAR |
| NT-05 | Test Governance API Gates | P-03, P-30 | GOVERN 1.7, MEASURE 2.5, MEASURE 2.9, MANAGE 2.2 | §8.4, §9.1 | [Run →](https://needle.app/workflow-templates/test-governance-api-gates) | 🟡 CANONICAL PROBE |

---

## P-30 Attestation Summary

| Template | Composite Score | Verdict | Ratified |
|---|---|---|---|
| NT-01 | 0.955 | PASS | Ender — 2026-06-09 |
| NT-02 | 0.944 | PASS | Ender — 2026-06-09 |
| NT-03 | 0.970 | PASS | Ender — 2026-06-09 |
| NT-04 | 0.962 | PASS | Ender — 2026-06-09 |

Attestation records: [ai-prompt-systems-portfolio/docs/qa/](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/docs/qa)

---

## Pattern Reference

| NDR Pattern | Name | Role in Template Execution |
|---|---|---|
| P-03 | Governance Contract Test | Validates template outputs against declared governance spec |
| P-05 | Tri-Phase CI Gate | Enforces retrieve → generate → evaluate pipeline integrity |
| P-11 | 11Q Attestation Scoring | Scores template output quality across 11 dimensions |
| P-30 | Apogee Attestation Gate | Final verification gate before template achieves registry inclusion |

---

## NIST AI RMF Alignment

| NIST Function | Control | Satisfied By |
|---|---|---|
| GOVERN | 1.7 — Human oversight documentation | NT-01, NT-04 |
| MEASURE | 2.5 — Output reliability measurement | NT-01 |
| MEASURE | 2.9 — Combined eval + audit chain | NT-03 |
| MANAGE | 2.2 — RAG as hallucination mitigation | NT-02 |

---

## ISO 42001 Alignment

| Clause | Requirement | Satisfied By |
|---|---|---|
| §6.1 | AI risk identification and treatment | NT-04 |
| §8.4 | Operational control of AI systems | NT-01, NT-02 |
| §9.1 | Monitoring, measurement, analysis | NT-03, NT-04 |

---

## Inclusion Criteria
A template may be added to this registry only when:
1. NDR pattern cross-reference confirmed in `docs/ndr_patterns_unified.json`
2. Apogee Lens review completed (P-30 satisfied, composite ≥ 0.90)
3. NIST/ISO control mapping verified against primary standard text
4. Needle template URL confirmed stable (verified by template owner)
5. COLLEEN 1-1-1-1 gate passed (semantic, logical, visual, ethical)

---

## Ecosystem Links
- [NDR Pattern Registry (Unified)](../NDR_PATTERN_REGISTRY_UNIFIED.md)
- [NDR Patterns JSON](../ndr_patterns_unified.json)
- [Workspace Bootstrap](../WORKSPACE_BOOTSTRAP.md)
- [Ecosystem Inventory](../ECOSYSTEM_INVENTORY.md)
- [ai-governance-frameworks: NIST/ISO docs](https://github.com/ndrorchestration/ai-governance-frameworks/tree/main/docs/needle-templates)
- [ai-prompt-systems-portfolio: Prompt specs](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/specs/needle)
- [Apogee Attestation Records](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/docs/qa)
- [Needle Partner Directory](https://needle.app/partners-directory/ndr-ai-orchestration)
