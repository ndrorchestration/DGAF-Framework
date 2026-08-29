# Deferred Items — Owner Action Required

**Maintained by:** Agent Amethyst × COLLEEN  
**Last Updated:** 2026-08-29 · v1 control-plane planning pass  
**Status:** ACTIVE

These items are confirmed, understood, and intentionally parked. They require owner decisions, credentials, implementation sequencing, or hands-on access that should not be silently promoted into completed state.

---

## DGAF v1 — Intentionally deferred from control-plane core

The authoritative v1 architecture and placement are defined in:

- `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`
- `docs/architecture/DGAF_V1_FILE_TREE_PLAN.md`

The following remain deferred until the basic control plane is executable and independently tested:

| Item | Reason for deferral | Promotion condition |
|---|---|---|
| Semantic-diversity score as independence proof | Diversity is not equivalent to independent evidence | Validated methodological basis + calibration |
| Learned sycophancy classifier as authoritative gate | Requires model-facing validation and failure analysis | Adversarial benchmark + independent evaluation |
| Adaptive topology optimization | Conflates orchestration control with experimental topology selection | Separate experiment and baseline evidence |
| Automatic confidence increase from consensus | Risks correlated-consensus laundering | Independence/provenance method demonstrated |
| Autonomous policy learning | Governance authority must remain explicit | Separate governance design + bounded evaluation |
| Harmonic/geometric signals in authorization | No validated operational necessity | Controlled evidence establishes legitimate effect |
| PDMAL topology choice as control-plane policy | PDMAL is an experimental substrate, not generic governance | Explicit candidate-bound experiment |
| Provider-specific cost models as safety boundary | Pricing varies and is not a reliable safety primitive | Keep only as reporting metadata unless separately justified |
| Real-model/runtime adapters before deterministic harness | Live execution would obscure basic contract failures | Deterministic contract suite passes |

These are **deferred capabilities**, not defects in the current governance layer.

---

## Existing snoozed items

| # | Item | Repo / System | What's Needed |
|---|---|---|---|
| S-01 | `VITE_GEMINI_API_KEY` in Vercel | Driftwatch (Vercel dashboard) | Add environment variable in Vercel project settings |
| S-03 | FLAG-05 (AXIS pattern doc) | DGAF-Framework | Content decision on AXIS pattern scope |
| S-04 | FLAG-07 (Drive files) | External (Google Drive) | Owner access required to locate/link files |
| S-05 | FLAG-11 (Vercel project linkage) | Vercel | Credential/dashboard access required |
| S-06 | FLAG-12 (Dependabot PR) | TBD repo | Owner review/merge required |
| S-07 | Visual asset (60–90s motion graphic) | DGAF-Framework | Tooling choice + final approval |

---

## DGAF v1 implementation gates

These are not deferred features; they are the planned implementation sequence:

1. Schemas/contracts — GovernanceEnvelope, TaskState, BranchRecord, BudgetLedger, CommitRequest.
2. Deterministic lifecycle controller — legal transitions and fail-closed handling.
3. Scope inheritance — authority, tools, data, and remaining budget cannot increase downward.
4. Cycle control — canonical state identity and repeated-state termination.
5. Veto propagation — hard governance veto remains terminal for ordinary recursion.
6. Evidence retention — accepted, rejected, correlated, incomplete, and vetoing branches remain inspectable.
7. Plan/commit barrier — consequential actions require explicit authorization.
8. Deterministic mock harness — prove the contracts before live-provider integration.

Implementation placement is governed by `docs/architecture/DGAF_V1_FILE_TREE_PLAN.md`.

---

## ✅ Closed Items

| # | Item | Resolution |
|---|---|---|
| S-08 | SWEEP-EH-003 / T-EH-05 Needle + CTA | Resolved; active follow-up remains in `entrepreneur-hub/docs/TODO.md`. |
| S-02 | NDR-STASIS window closure | Resolved — Option A; migration work tracked separately under Issue #41. |

---

## Planning hygiene

Deferred does not mean discarded. Each deferred item must remain associated with a promotion condition and a canonical owner location. Do not create a second list elsewhere unless it is an evidence record with a distinct purpose.
