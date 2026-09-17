# IMP-05 Brand Specification

**Pattern:** P-19 — IMP-05-Branding-Consistency  
**Version:** 1.1  
**Maintained by:** `role.governance-orchestrator` under the DGAF functional role/capability contract  
**Last updated:** 2026-09-17

---

## Brand Identity: Phi-Harmonic Pentagon

The IMP-05 brand identity provides presentation guidance for public-facing surfaces of the ndrorchestration ecosystem. It does not itself grant project authority, certify a repository, establish compliance, or transfer DGAF governance state into another project.

## Four Required Disclosure Elements (P-19 Checklist)

When a public repository or portfolio document presents itself as part of the Phi-Harmonic Pentagon ecosystem, use all four disclosure elements:

| # | Element | Format | Example |
|---|---------|--------|---------|
| 1 | **Phi-Harmonic Pentagon framing** | Section header or callout | `## 🔷 Phi-Harmonic Pentagon Ecosystem` |
| 2 | **ndrorchestration attribution** | Byline or copyright | `© 2025–2026 Ndr (ndrorchestration)` |
| 3 | **Functional governance boundary** | Role/contract statement | `Governance coordination: role.governance-orchestrator; authority remains project- and contract-scoped.` |
| 4 | **DGAF-Framework reference** | Markdown link | `[DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)` |

No persona label grants authority. Historical agent/persona names may be retained for provenance through `governance/persona_role_lineage.v1.json`, but current authority semantics must resolve through `governance/role_capability_registry.v1.json` and the applicable project-local contracts/evidence.

## DGAF Callout Block (Standard)

A repository may use this block only to describe a real, project-local DGAF relationship. A link or branding element alone does not establish that relationship.

```markdown
---
## 🔷 DGAF Governance Reference

This repository references the [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) for governance patterns and evidence-bound controls. Any project-local authority must be established by this repository's own current contracts and evidence; this notice does not transfer DGAF authorization, validation, certification, compliance, experimental state, or efficacy claims.

- **Governance coordination role:** `role.governance-orchestrator`
- **Authority contract:** `governance/role_capability_registry.v1.json`
- **Historical persona lineage:** `governance/persona_role_lineage.v1.json`
- **Ecosystem:** Phi-Harmonic Pentagon
- **License:** Apache 2.0
- **Attribution:** © 2025–2026 Ndr (ndrorchestration)
---
```

If a repository merely reuses DGAF patterns without a project-local governance binding, describe DGAF as a **pattern/reference source**, not as the repository's governing authority.

## Naming Convention — DGAF References

All references to the governance framework must use DGAF, not any prior acronym:

| ❌ Retired / Incorrect | ✅ Current / Correct |
|------------------------|----------------------|
| CSDF | DGAF |
| CyberShield Defense Framework | Dynamic Governance Agentic Formation Framework |
| CyberShield | DGAF-Framework |
| Any prior framework name | DGAF or DGAF-Framework |

**Rule:** First mention per document: `DGAF (Dynamic Governance Agentic Formation) Framework`. Subsequent mentions: `DGAF` or `DGAF-Framework`.

## IP-Safe Disclosure (Portfolio Repos)

Portfolio and public showcase repos must additionally include:

```markdown
> **IP Notice:** All examples are sanitized for public sharing. No client data, proprietary workflows, or confidential architectures are included. All intellectual property © Ndr (ndrorchestration).
```

## Audit Frequency

P-19 runs at every quarterly sweep and any time a new public repo is created. The audit checks branding consistency separately from governance authority, claim scope, certification/compliance language, and project-local evidence.
