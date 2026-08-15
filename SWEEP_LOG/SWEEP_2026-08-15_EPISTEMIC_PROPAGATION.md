# SWEEP — 2026-08-15 — Epistemic Propagation Audit

**Type:** Cross-repository epistemic consistency sweep
**Status:** OPEN — follow-up propagation work remains
**Scope:** Gold Star / S-Tier terminology, project-local certification language, evidence classification, mathematical-label integrity
**Related correction:** `BOOTSTRAP.md` commit `253c9d13abb56802f2b87591c6de99f123ddb3dd`

## Findings

| Surface | Finding | Classification | Action |
|---|---|---|---|
| Gold-star-standards certification index | Historical tier assignments could be read as current certification | HISTORICAL | Corrected |
| Gold-star-standards rubrics | Rubric scores previously carried certification/production-readiness implications | HISTORICAL / PROJECT-LOCAL | Corrected |
| Amethyst Eval Stack Gold Star tier | Tier description implied validated safety properties | PROJECT-LOCAL | Corrected |
| ai-governance-frameworks Gold Star framework | “Validated/evidence-based” language exceeded demonstrated evidence | HISTORICAL / HYPOTHESIS | Corrected |
| DGAF BOOTSTRAP | Gold Star/S-Tier and persona approvals could act as inherited authority claims | PROJECT-LOCAL | Corrected |
| DGAF CROSS_REF | Search confirms Gold Star and attestation terminology propagates through registry, agent, QA, and sweep surfaces | TRACEABILITY RISK | Follow-up required |
| DGAF SWEEP_LOG | Historical closure records already contain useful evidence-boundary distinctions | VERIFIED GOOD | Preserve; append corrections rather than rewriting history |

## Canonical Evidence Boundary

Current material should use:

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

A project-local score, tier, persona sign-off, or approval is not an automatic evidence upgrade.

## Specific Audit Rule

1. Preserve historical records.
2. Do not rewrite historical PASS/Gold Star/S-Tier events as though they were never made.
3. Correct current-facing interpretations that turn those historical events into independent certification claims.
4. Label mathematical constructs according to what the implementation actually computes.
5. Label numerical thresholds by provenance rather than presenting arbitrary engineering parameters as derived laws.
6. Separate project-local mappings from compliance with external standards or law.

## Remaining Propagation Targets

- `CROSS_REF.md`
- `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`
- agent specifications and QA rubrics that use attestation terminology
- README/governance surfaces
- stale/superseded sweep references

**Sweep conclusion:** The ecosystem has a meaningful historical evidence trail, but several authority labels propagated farther than the evidence warranted. The correction strategy is classification and traceability, not deletion of historical work.
