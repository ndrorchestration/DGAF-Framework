# Epistemic Supersession Register

**Status:** Active documentation control record  
**Scope:** ndrorchestration ecosystem  
**Purpose:** Preserve historical claims while preventing superseded or unsupported language from being mistaken for current verified specifications.

## 1. Current evidence discipline

Project artifacts must distinguish among:

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

These labels describe evidence state, not prestige. A project-local definition is not an external standard. A computed result is not automatically independently verified. A CI pass is evidence of the checks that ran, not certification. A historical artifact remains historical unless its underlying claim is re-established.

## 2. Superseded ecosystem language

The following classes of language have been identified during the 2026 documentation sweep and must not be propagated as current fact without new evidence:

| Superseded pattern | Current treatment |
|---|---|
| "DGAF-certified" | Project relationship only unless an independently defined certification process and evidence are supplied. |
| "DGAF-governed" used as external authority | Replace with the actual repository-local relationship. |
| "Gold Star" / "Platinum Star" as external certification | Treat as project-local rubric/history unless independently validated. |
| "industry first" | Historical or hypothesis unless supported by a documented comparative search. |
| "production-ready" | Require explicit operational evidence; do not infer from repository existence or tests. |
| "validated" | Reserve for claims with a documented validation method and evidence. |
| Numeric percentages/multipliers without a denominator or derivation | Mark unsupported/fabricated precision until the measurement basis is documented. |
| Mathematical terminology used as metaphor for a simpler mechanism | Label as metaphor or rename the mechanism to its implemented behavior. |

## 3. Known repository actions

The following documentation corrections have been applied during the current sweep:

- `junior-apogee-app` — README reconciled with evidence standards.
- `sentinel-governance` — README reconciled with evidence standards.
- `resumeapex-eval` — README reconciled with evidence standards; statistical values distinguished as targets rather than achieved validation.
- `AI-Prompt-Engineer` — classified as a historical portfolio archive; retired Agent Lavender attribution and historical authority language were contextualized.
- `AHG-Zeta-Pell-Autonomous-Lattice` — audit findings recorded separately; Pass 2 remains focused on the unaudited chaos/FML and Three-Regime sections and the 4→2 recovery trace.

## 4. Historical records

Historical issues, commits, notebooks, and archived repositories are not to be silently rewritten solely to make terminology appear consistent with the present state. When an artifact is immutable or archived, preserve it and classify its claims as historical/deprecated where appropriate.

`gold-star-qa-framework` is archived and therefore cannot be edited through the normal issue workflow. Its historical certification terminology is not current authority.

## 5. AHG Zeta-Pell boundary

AHG Zeta-Pell and PDMAL are currently separate tracks. Similar use of constants or convergence language does not establish a technical merge.

Current audit findings include:

- conflicting expansions of AHG;
- misleading "Hecke Operator" terminology for a stochastic admission threshold;
- unsupported 150x/180x/200x jitter claims without a defined 1x baseline;
- hardcoded benchmark values whose local derivation is not demonstrated;
- a silver-ratio premise that is valid mathematics but does not by itself prove the claimed stability theorem.

These findings should remain attached to the AHG audit rather than being generalized to PDMAL without evidence.

## 6. Taxonomy and vocabulary

The taxonomy/vocabulary layer is part of the epistemic control surface. Definitions must identify whether a term is:

1. a standard external technical term;
2. a project-defined term;
3. an analogy/metaphor;
4. a hypothesis;
5. deprecated terminology.

Project acronyms must have one canonical expansion per active system. Historical expansions may be preserved in changelogs/audit records but must not remain ambiguous in current specifications.

## 7. Repository metadata

GitHub repository descriptions are a separate documentation layer from README files. The current sweep identified stale descriptions including certification, governance-authority, and production-readiness language. These descriptions require repository-settings write access to reconcile; they must not be represented as corrected until the metadata itself changes.

## 8. PDMAL platinum-notation supersession

The current mathematical-notation policy distinguishes two different quantities that must not be conflated:

- **pP / Platinum Mean** — a project-defined notation for the regular-hendecagon unit-side circumradius,
  \(pP = 1/(2\sin(\pi/11)) \approx 1.774732842\). This is intentionally retained as the project's **Platinum Mean** notation; it is not the standard plastic constant.
- **ρP / plastic constant** — the standard mathematical constant \(\rho_P \approx 1.3247179572447454\), the real root of \(x^3=x+1\).

Earlier repository material uses **1.7747 / 1.77473** under labels such as "Platinum Ratio" and, in some artifacts, assigns that value a verified mathematical role. Those references must now be classified according to the definition actually intended. Where they refer to the hendecagon circumradius, they are historical uses of the project-defined **pP / Platinum Mean**; where they incorrectly identify that value as the plastic constant or another standard mathematical constant, that claim is superseded and must not be propagated.

Known affected historical/current-surface artifacts include:

- `docs/formalism/constants/11Q-derivation.md`
- `docs/formalism/hensel-general-formalism.md`
- `docs/registry/PLATINUM_REGISTRY_TIERS_v1.md`
- `docs/architecture/platinum-convergence-audit-v1.md`
- related pattern, substrate, gate, agent, and registry documents surfaced by the repository-wide `Platinum Ratio` search.

Treatment:

**RETAIN PROVENANCE → CLASSIFY SEMANTICS → SUPERSEDE INCORRECT IDENTIFICATION → PREVENT DOWNSTREAM MISUSE**

Do not silently delete historical evidence. Any artifact that presents `1.7747`/`1.77473` as the plastic constant, or assigns it an unsupported current mathematical authority, must be revised or explicitly marked historical/superseded. Artifacts using the value for the defined hendecagon circumradius may retain it when explicitly labeled **pP / Platinum Mean** and given its defining equation. Until that semantic remediation is complete, affected material remains a documentation-consistency finding and must not be used to support unrelated current mathematical claims.

This notation correction does **not** establish PDMAL convergence, global contraction, production robustness, security, baseline superiority, or empirical efficacy. The contraction monitor remains an observational proxy; unweighted Forman–Ricci has no discriminating variance on the current unweighted topology; and the real-trace `Da` threshold remains uncalibrated.

## 9. Public-surface publication rule

Historical or internal material must not be promoted to a public-facing GitHub surface merely because it is available or technically accurate in isolation. Public artifacts must pass the repository's Public Surface QA Standard for audience relevance, usefulness, placement, navigation, professional representation, privacy/disclosure, community fit, maintainability, identity integrity, and reader friction.

Personal/private Notion records and internal operational-control pages are not public GitHub navigation targets by default. Internal records may inform public documentation without becoming public destinations.

## 10. Operating rule

When evidence conflicts with inherited project language:

**preserve the evidence → classify the claim → correct the current surface → retain historical provenance → do not upgrade the claim without new evidence.**

This register is a documentation-control artifact, not a certification statement.
