# Semantic Claim Review — 2026-08-16

## Purpose

The deterministic claim-language audit is a lexical detector. It identifies terms that require contextual review; it does not classify every occurrence as an overclaim.

The rerun after registry reconciliation completed successfully on main commit `802b4bafbb662ca59d99824f8d05d0f69f39309b`.

## Reviewed categories

### Legitimate / non-overclaiming occurrences

- Evidence-standard definitions such as `VALIDATED`, `VERIFIED`, and `EMPIRICALLY SUPPORTED`.
- Explicit negative statements and caveats such as “not independently validated.”
- Historical supersession/audit records that preserve the original wording while marking it corrected or historical.
- Test/assertion language describing a local fixture or schema operation.

### Residual candidates requiring focused review

1. `components/ensemble_v16.py` — “empirically validated knee — 58.3% compression.”
   - Requires provenance for the empirical source and protocol before being treated as an empirical claim.
2. `docs/formalism/PDMAL_MATH_VERIFIED_v1.md` — “0.1579 validated in prior analytic work.”
   - Requires scope/source identification; title and wording may imply broader validation than the retained record supports.
3. `pptl/triumvirate_mandate.py` — “Prefect domain split is MECE (validated at construction).”
   - Requires clarification of whether “validated” means an internal construction invariant or an independently validated claim.
4. `docs/qa/APOGEE_11Q_P34.json` — “empirically validated” attestation language.
   - Requires historical/evidence provenance reconciliation before being used as current efficacy evidence.
5. `docs/agents/prof-prodigy/*` — recurring “validated” terminology in agent-memory/formalization context.
   - Treat as project-local metadata unless a specific external/independent validation record is linked.

## Decision rule

These candidates are not automatically downgraded solely because the lexical audit found them. They require contextual evidence review. Any claim lacking a claim-specific source, scope, method, and retained evidence should be rewritten to calibrated language.

## Current registry remediation

The two concrete registry overclaims identified by the initial audit were corrected in `registry/ecosystem_registry.json` on commit `802b4baf`:

- Junior Apogee App: removed unsupported “Production-ready” wording.
- AI Governance Frameworks: replaced “Validated frameworks” with “Reference collection...” and explicitly declined to assert independent validation.

The deterministic follow-up audit is retained as workflow artifact `claim-hygiene-evidence-802b4bafbb662ca59d99824f8d05d0f69f39309b`, digest `sha256:0aecbb7bf2c6bf7b4e002e802dbedeb2dfdaf296310d04559d9a855be03649f8`.

## Scope boundary

This document is a repository-local epistemic control record. It does not constitute external scientific validation, legal certification, or independent assurance.
