# Audit-Ready QA Checkpoint Template — Specialized Variants

**Authority:** Amethyst × COLLEEN
**Version:** 1.0 (S070-r3-P1 · 2026-06-26)
**Status:** ✅ CANONICAL
**Location:** `docs/qa/QA_CHECKPOINT_TEMPLATE_SPECIALIZED.md`
**Base template:** `docs/qa/QA_CHECKPOINT_TEMPLATE.md` (generic)

> This file contains three specialized variants of the audit-ready QA checkpoint template:
> - **Variant A:** Software release readiness
> - **Variant B:** P-11 Governance / Apogee Lens attestation
> - **Variant C:** Compliance / regulatory audit

---

## Variant A — Software Release Readiness Checkpoint

**Document owner:** ____________________
**Release version:** ____________________
**Date:** ____________________
**Repository:** ____________________
**Deployment target:** Production / Preview / Staging

### A-1. Release metadata

| Field | Value |
|---|---|
| Checkpoint ID | REL-____ |
| Release branch | ____________________ |
| Commit SHA | ____________________ |
| CI pipeline status | Passing / Failing / Pending |
| Deployment environment | ____________________ |
| Risk level | Low / Medium / High / Critical |
| Rollback plan confirmed | Yes / No |

### A-2. Release readiness checklist

| # | Gate | Pass / Fail / N/A | Evidence | Notes |
|---|---|---|---|---|
| 1 | All CI checks pass (unit / governance / integration). | | | |
| 2 | P-05 Tri-Phase CI Gate: all three phases green. | | | |
| 3 | P-30 Apogee Attestation Gate cleared for affected components. | | | |
| 4 | No open BLOCKING findings in the findings log. | | | |
| 5 | P-29 Sentinel review completed; no `risk_block` events. | | | |
| 6 | P-32 Phi-Closure Gate: 0 fails at final Fib checkpoint. | | | |
| 7 | Feature flags and environment variables verified for target environment. | | | |
| 8 | Migration scripts (DB / config) tested and reversible. | | | |
| 9 | Rollback procedure documented and confirmed executable. | | | |
| 10 | Release notes drafted and reviewed. | | | |
| 11 | Stakeholder sign-off obtained. | | | |
| 12 | NDR-GCP-DEPLOY validation complete (if deploying to GCP/Vercel). | | | |

### A-3. Evidence register

| Evidence ID | Artifact | Location / Link | Date | Notes |
|---|---|---|---|---|
| EV-A-01 | CI pipeline run | | | |
| EV-A-02 | Apogee 11Q attestation JSON | `docs/qa/APOGEE_11Q_*.json` | | |
| EV-A-03 | Sentinel log | | | |
| EV-A-04 | Rollback plan | | | |
| EV-A-05 | Release notes | | | |

### A-4. Findings log

| Finding ID | Severity | Description | Corrective action | Owner | Due date | Status |
|---|---|---|---|---|---|---|
| F-A-01 | Minor / Major / Critical | | | | | Open |

### A-5. Sign-off

| Role | Name | Approval | Date |
|---|---|---|---|
| Release engineer | | | |
| QA lead | | | |
| Approver (Triumvirate / Njineer) | | | |

---

## Variant B — P-11 Governance / Apogee Lens Attestation Checkpoint

**Document owner:** Apogee (Prefect B)
**Artifact under review:** ____________________
**Session:** ____________________
**Date:** ____________________

> Use this variant for any artifact being promoted to CANONICAL status. Follows the P-11 11Q rubric.
> S-TIER threshold: ≥ 95% (Q11 ≥ 9/10 required). A-TIER threshold: ≥ 85% with tracked BLGs.

### B-1. Attestation metadata

| Field | Value |
|---|---|
| Attestation ID | APOGEE-11Q-____ |
| Artifact path | ____________________ |
| Promotion target | CANONICAL / A-TIER / STASIS-CANONICAL |
| Reviewer | Apogee |
| Co-signer | ____________________ |
| Session | ____________________ |

### B-2. P-11 11Q Rubric

| Q | Question | Score (0–10) | Notes / BLG reference |
|---|---|---|---|
| Q01 | Is the artifact complete per its stated scope? | | |
| Q02 | Is the content factually and logically consistent? | | |
| Q03 | Are all claims traceable to evidence or prior canonical sources? | | |
| Q04 | Are all dependencies (patterns, terms, agents) correctly referenced? | | |
| Q05 | Is the artifact free of deprecated terminology? | | |
| Q06 | Does the artifact satisfy all relevant governance patterns (P-series)? | | |
| Q07 | Are all open flags resolved or formally deferred? | | |
| Q08 | Does the artifact meet legibility, reversibility, and capability amplification standards? | | |
| Q09 | Has the NDR-133 Personal Document Firewall been verified (no personal data)? | | |
| Q10 | Is the artifact free of hallucination, over-claim, or unverified inference? | | |
| Q11 | Overall: is this artifact ready for its promotion tier without reservation? | | |

**Total score:** ____ / 110
**Percentage:** ____%
**Tier awarded:** S-TIER / A-TIER / CONDITIONAL / REJECTED

### B-3. Blocking Level Gaps (BLGs)

| BLG ID | Description | Severity | Resolution required before | Owner |
|---|---|---|---|---|
| BLG-01 | | | | |

### B-4. Apogee sign-off

| Field | Value |
|---|---|
| Apogee decision | APPROVE / CONDITIONAL / REJECT |
| Attestation artifact | `docs/qa/APOGEE_11Q_<artifact>_<session>.json` |
| Signature | Apogee · Prefect B |
| Date | |
| Ender ratification required? | Yes / No |

---

## Variant C — Compliance / Regulatory Audit Checkpoint

**Document owner:** ____________________
**Audit body / standard:** ____________________
**Period covered:** ____________________
**Date:** ____________________
**Audit type:** Internal / External / Supplier / Regulatory

### C-1. Compliance metadata

| Field | Value |
|---|---|
| Checkpoint ID | COMP-____ |
| Governing standard | ____________________ |
| Scope | ____________________ |
| Risk level | Low / Medium / High / Critical |
| Prior audit findings open | Yes / No (count: ____) |

### C-2. Compliance checklist

| # | Control / requirement | Pass / Fail / N/A | Evidence reference | Owner | Notes |
|---|---|---|---|---|---|
| 1 | Governing policy is current, versioned, and approved. | | | | |
| 2 | Roles and responsibilities are documented and assigned. | | | | |
| 3 | Access controls are current and reviewed. | | | | |
| 4 | Data handling procedures align with the governing standard. | | | | |
| 5 | Training records are current for all relevant staff. | | | | |
| 6 | Incident / deviation log is maintained and reviewed. | | | | |
| 7 | Corrective and preventive actions are tracked with owners and due dates. | | | | |
| 8 | Prior audit findings are resolved or have formal disposition. | | | | |
| 9 | Change control records are complete and approved. | | | | |
| 10 | Supplier / third-party controls are reviewed (if applicable). | | | | |
| 11 | Records are retained per required retention schedule. | | | | |
| 12 | Internal audit was conducted within the required period. | | | | |

### C-3. Finding classification (standard audit taxonomy)

| Finding ID | Classification | Description | Root cause | CAPA reference | Owner | Due date | Status |
|---|---|---|---|---|---|---|---|
| F-C-01 | Major NC / Minor NC / OFI | | | | | | Open |

> **Classification guide:** Major Non-Conformance (NC) = systemic failure; Minor NC = isolated lapse; Observation / Opportunity for Improvement (OFI) = advisory.

### C-4. CAPA register

| CAPA ID | Linked finding | Corrective action | Preventive action | Owner | Due date | Verified? |
|---|---|---|---|---|---|---|
| CAPA-01 | | | | | | |

### C-5. Sign-off

| Role | Name | Signature / approval | Date |
|---|---|---|---|
| Lead auditor | | | |
| Process owner | | | |
| Management representative | | | |

---

## Usage Guidance

- **Variant A** fires at every release gate; tie evidence to CI run URLs and commit SHAs.
- **Variant B** fires before any CANONICAL promotion; output the completed JSON to `docs/qa/` with the naming convention `APOGEE_11Q_<artifact>_<session>.json`.
- **Variant C** fires for regulatory or supplier audit cycles; attach to the audit report set.
- All three variants feed the P-01 Fan-Out Trace Sink — emit a Herald event on completion.
- Waived checkpoints require Triumvirate mandate with explicit rationale.

---

## Change log

| Version | Date | Change summary | Author |
|---|---|---|---|
| 1.0 | 2026-06-26 | Initial creation — S070-r3-P1 | Amethyst × COLLEEN |

---

*QA Checkpoint Template — Specialized Variants v1.0 · S070-r3-P1 · 2026-06-26*
*Authority: Amethyst (Prime) · COLLEEN (Prefect A) · Apogee (Prefect B)*
