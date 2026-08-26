# Registry Claim Review — 2026-08-16

The deterministic claim-hygiene audit identified two current registry summaries that require wording review:

1. `junior-apogee-app` — **“Production-ready AI agent evaluation and QA platform...”**
   - Current repository evidence does not establish a production-readiness claim for this registry entry.
   - Recommended status language: describe the implemented capability and explicitly separate deployment/runtime verification from the product description.

2. `ai-governance-frameworks` — **“Validated frameworks for AI governance...”**
   - The word “validated” is broader than the repository evidence supports when presented without scope.
   - Recommended language: describe the repository as a **curated collection/reference implementation** of named governance frameworks, with source authority and external-framework scope stated explicitly.

This document records the finding; it does not itself alter the registry values.

Audit provenance:

- Workflow: `Claim Hygiene Audit`
- Run: `31976921517`
- Source commit: `3823a8b0f8992490c47c9495cc436138b3fefdf0`
- Retained artifact: `claim-hygiene-evidence-3823a8b0f8992490c47c9495cc436138b3fefdf0`
- Artifact digest: `sha256:09e8153ecf124ce601816919b506946b701e97cc3911b152fe5ad0ab80e1afe6`
- Total textual matches: `342`

The audit is intentionally contextual: the presence of terms such as `verified`, `validated`, or `proven` in standards, historical logs, test states, or explicit negative claims is not itself an overclaim.
