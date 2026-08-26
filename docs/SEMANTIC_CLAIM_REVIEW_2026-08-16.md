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

## Focused triage status

### 1. `components/ensemble_v16.py` — “empirically validated knee — 58.3% compression.”

**Status: UNRESOLVED — evidence required.**

The current source wording makes a substantive empirical claim about a compression threshold. No claim-specific empirical protocol, dataset, or retained result was identified in the reviewed evidence boundary. Do not represent the 58.3% figure as empirically validated until that provenance is retained. Calibrated wording should be used if the source evidence cannot be recovered.

### 2. `docs/formalism/PDMAL_MATH_VERIFIED_v1.md` — “0.1579 validated in prior analytic work.”

**Status: CONTEXTUALLY RESOLVED / HISTORICAL.**

The document is explicitly marked **SUPERSEDED** and states that it is not the current mathematical authority. The 0.1579 value is subsequently derived directly as `30/190 ≈ 0.1579`, and the document explicitly limits the figure to structural graph density rather than resilience, superiority, convergence, or governance effectiveness. The remaining “validated in prior analytic work” wording is historical-context language inside a superseded document and is not treated as current efficacy evidence.

### 3. `pptl/triumvirate_mandate.py` — “Prefect domain split is MECE (validated at construction).”

**Status: CONTEXTUALLY RESOLVED / INTERNAL CONSTRUCTION INVARIANT.**

The implementation performs deterministic construction-time checks: domain names must differ and governed-agent sets must not overlap. Here “validated at construction” describes local invariant enforcement, not independent empirical validation of the governance design. The surrounding implementation and error paths support that interpretation. This occurrence is therefore not evidence of external efficacy or fitness.

### 4. `docs/qa/APOGEE_11Q_P34.json` — “empirically validated” attestation language

**Status: UNRESOLVED — provenance reconciliation required.**

The phrase remains a candidate until its historical source, scope, method, and retained evidence are identified. It must not be promoted as current empirical efficacy evidence merely because it appears in an attestation record.

### 5. `docs/agents/prof-prodigy/*` — recurring “validated” terminology in agent-memory/formalization context

**Status: UNRESOLVED / PROJECT-LOCAL METADATA.**

These occurrences are treated as project-local terminology unless a specific independent validation record is linked. They should not be interpreted as external validation by default. Any current substantive claim should be calibrated or linked to claim-specific evidence.

## Decision rule

These candidates are not automatically downgraded solely because the lexical audit found them. They require contextual evidence review. Any claim lacking a claim-specific source, scope, method, and retained evidence should be rewritten to calibrated language.

## Current registry remediation

The two concrete registry overclaims identified by the initial audit were corrected in `registry/ecosystem_registry.json` on commit `802b4baf`:

- Junior Apogee App: removed unsupported “Production-ready” wording.
- AI Governance Frameworks: replaced “Validated frameworks” with “Reference collection...” and explicitly declined to assert independent validation.

The deterministic follow-up audit is retained as workflow artifact `claim-hygiene-evidence-802b4bafbb662ca59d99824f8d05d0f69f39309b`, digest `sha256:0aecbb7bf2c6bf7b4e002e802dbedeb2dfdaf296310d04559d9a855be03649f8`.

## Scope boundary

This document is a repository-local epistemic control record. It does not constitute external scientific validation, legal certification, or independent assurance.

## Closure gate

Issue #59 remains **OPEN** until the unresolved candidates have either:

1. claim-specific source/scope/method/retained evidence recorded, or
2. the substantive current wording is calibrated so it no longer asserts unsupported validation.

A follow-up deterministic Claim Hygiene Audit must then pass with the resulting repository state retained as evidence.
