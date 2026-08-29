# CHANGELOG.md

## [2026-08-29] — Public Documentation Surface Refactor

### Documentation architecture and reader experience

- Refocused the root `README.md` as a public project entry point organized around identity, value, architecture, current status, evidence, research tracks, and contribution paths.
- Refocused `README.technical.md` as an engineer/researcher-facing implementation map rather than an agent-session and audit-log surface.
- Reworked `README.governance.md` to distinguish DGAF governance design from external legal/regulatory compliance and certification claims.
- Reworked contributor and workspace guidance to reduce internal-process overload and improve task-oriented navigation.
- Reworked component, PPTL, roster, and team-wiki documentation to separate implementation descriptions from historical attestation, authority, and efficacy claims.
- Added `docs/governance/DOCUMENTATION_STYLE_GUIDE.md` defining audience, hierarchy, claim presentation, temporal scope, navigation, and public-facing writing rules.
- Added `docs/governance/PUBLIC_DOCUMENTATION_INFORMATION_ARCHITECTURE.md` defining the repository's landing → project → technical → research → evidence → historical information architecture.
- Added `docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md` defining Current / Historical / Superseded / Reference Only / Draft treatment for retained records.
- Added `docs/HISTORICAL_RECORDS_INDEX.md` as a navigation layer for preserved project history.
- Expanded `PUBLIC_SURFACE_QA_STANDARD.md` to include explicit communication-quality, hierarchy, reader-friction, and historical-placement controls.
- Classified obsolete `DEFERRED_ITEMS.md` and `CI_CD_TEMPLATES.md` snapshots as historical records rather than current operational sources.
- Preserved technical specifications, experiment protocols, evidence records, and audit history at their appropriate depth rather than flattening them into public-facing prose.

### Claim and provenance discipline

- Replaced prominent historical `S-TIER`, `Gold Star`, certification, compliance, and production-readiness presentation with scoped descriptions on high-level surfaces.
- Preserved historical evidence while preventing current documentation from silently inheriting obsolete status claims.
- Distinguished engineering verification from experimental authorization and empirical efficacy throughout public-facing documentation.

### Experimental boundary

- **No implementation or experimental state is changed by the documentation refactor.**
- Current PDMAL status remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.
- Historical verification remains scoped to the exact source, environment, deployment, run, and artifact that produced it.

---

## [2026-08-25] — Ecosystem Boundary Alignment

### Pattern Commons / commercialization / cross-disciplinary governance

- Established `docs/PATTERN_COMMONS_ARCHITECTURE.md` as the DGAF-side architectural boundary for an ecosystem-level Pattern Commons.
- Established `docs/GOVERNANCE/DGAF_COMMERCIALIZATION_OPENNESS_BOUNDARY.md` defining evidence-preserving openness and controlled commercial/private/security boundaries.
- Added `docs/GOVERNANCE/DGAF_TRADEMARK_AND_CERTIFICATION_POLICY.md` as a proposed future governance policy; no active DGAF certification program is claimed.
- Clarified that NDR is a pattern namespace/family within the broader Pattern Commons, not the universal pattern corpus.
- Clarified that `registry/PATTERN_REGISTRY_v2.md` is a distinct DGAF orchestration-pattern namespace and is not a competing NDR registry merely because it contains the word “registry”.
- Added repository-level cross-links for Pattern Commons, commercialization/openness, trademark/certification, and the canonical cross-reference index.
- Updated contributor guidance to require registry/provenance searches, semantic-equivalence checks, evidence boundaries, and openness/security classification.
- Corrected public README merge-conflict markers and refreshed its ecosystem/commercialization documentation spine.
- Preserved the Apache-2.0 license boundary and its separate trademark reservation; no proprietary restriction has been retroactively imposed on already-public open-source material.
- Confirmed `.github/FUNDING.yml` already exposes GitHub Sponsors; sponsorship is treated as funding rather than certification or ownership.
- No existing pattern artifact was moved, deleted, or reclassified solely for commercialization. Asset-by-asset classification remains an audit task.

### Epistemic boundary

Commercial status, repository visibility, sponsorship, project attestation, and trademark/certification status are independent dimensions and must not be used as evidence of technical validity or empirical support.

---

## [2026-08-18] — Post-v0.7.5 Pre-Freeze Status

### DGAF/PDMAL runtime-characterization and pilot readiness

- Published and retained the `v0.7.5-pdmal-runtime-characterization` release as the immutable runtime-characterization baseline.
- Closed the synthetic blinding operational test; no production secret was accessed and no empirical pilot data was generated.
- Merged security hardening PR **#70** into `main`.
- Security baseline established at commit `93f535c1eb822244ab4e7d3646cadfb9e28a9876`.
- PR **#65 — Epistemic Alignment + Evidence Card architecture** remains open and is blocked by merge conflicts because its branch predates the #70 merge.
- PR #65 must be rebased/updated against current `main`, conflicts resolved, and CI rerun before merge.
- Release asset provenance remains split into two byte-level checks: SHA-256 of the published ZIP and SHA-256 of the authoritative inner runtime artifact.
- Expected inner-artifact digest from the authoritative CI provenance record is `f6db24e5dd2659d4395c0752845e23f1823aa674980abb20074d4d443de01250`; this value remains an expected reference until the released inner artifact is freshly hashed.
- Added `docs/PROJECT_STATUS.md` as the current authoritative operational gate board and provenance handoff.
- Pilot remains PRE-FREEZE and **not authorized**.
- Empirical data remains **0**.

### Provenance rule

The v0.7.5 release identity, published release-asset SHA-256, inner runtime-artifact SHA-256, and eventual post-#65 freeze HEAD SHA are distinct identities and must not be substituted for one another.
