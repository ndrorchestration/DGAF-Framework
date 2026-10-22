# DGAF v1 claims-and-evidence register (proposed seed)

**Status:** INITIAL NON-ADJUDICATED SEED. No claim is promoted by this file.
Controller: https://github.com/ndrorchestration/DGAF-Framework/issues/1421

| Claim | Candidate status | Evidence pointer | Independence | Limitations |
| --- | --- | --- | --- | --- |
| DGAF has executable governance contracts | TESTED_ONLY | Current main source and associated required CI; exact run and SHA must be attached per claim | Internal | Do not infer enforcement on untested deployment paths |
| Proposed AAR key-operation matrix distinguishes historical signature verification from issuance | TESTED_ONLY | Draft #1416 at `1c83d3f9c9714efae370ab080a3d39114456907a` | Operator/hosted CI only | Design-only; no admitted producer |
| PDMAL artifact publication guard denies execution before upload | TESTED_ONLY | Draft #1414 `a09781ee923aa9d5988302854a43889a51ba68bd` and #1419 QA | Operator + hosted CI | Unmerged, not protected-main or whole-repo containment |
| Durable cross-instance replay enforced | EXPLICITLY_NOT_CLAIMED | Issue #756 | None | Not implemented |
| Commit-time authoritative revocation enforced | EXPLICITLY_NOT_CLAIMED | Issue #757 | None | Not implemented |
| Independent efficacy or superiority validated | EXPLICITLY_NOT_CLAIMED | Issue #929 and comparative research | None admitted | Scientific N ceiling remains zero |
| High assurance or universal containment | EXPLICITLY_NOT_CLAIMED | DGAF control state | None admitted | Not authorized |

## Required fields on promotion
claim_id, exact_public_wording, supported_action_class, evidence_uri,
raw_artifact_digest_sha256, exact_source_commit, test_or_experiment_id,
verifier_identity, independence_class, reviewer_COI, scope, assumptions,
counterexample_search, limits, disposition, date, signoff.

**Rule:** missing verifier evidence, ambiguous source identity, or a failed
acceptance oracle defaults to TESTED_ONLY or EXPLICITLY_NOT_CLAIMED;
never silently upgrades to SUPPORTED. These seeded classifications are
planning annotations, not accepted public claims.
