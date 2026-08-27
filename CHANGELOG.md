# CHANGELOG.md

> **Steward:** COLLEEN · **Orchestrator:** Amethyst

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

---

## [Post-S077] — 2026-06-29

### Autonomous Sprint — Amethyst execution authority

#### AHG v1.2 — External Review Integration
- **`docs/theory/AHG_ARCHITECTURE.md` → v1.2:**
  - Canonical φ computation via logistic normalization: φ(t) = 1 + 0.8·σ(S(t)); range bounded [1.0, 1.8]
  - Stability Index S(t) = w_1·D_e + w_2·N + w_3·C + w_4·R (only D_e enters; D_explore, D_correct excluded)
  - D disaggregated into D_explore, D_correct, D_e (three named subtypes; D_correct is Apogee Auditor fuel)
  - 7-state regime table (Grounded / Flow / Vigilance / Expansion / Integration / Introspection / Tension)
  - Integration band (1.60–1.70) explicitly named — NDR-STASIS φ=1.618 aligned as peak productive phase
  - Tension threshold revised 1.70 → 1.80 (1.70–1.80 is now Introspection, not Tribunal)
  - §2.7 Cognitive Phase Space (3D manifold: Exploration↔Exploitation, Consensus↔Dissent, Confidence↔Uncertainty)
  - §6 Performance Claims — falsifiable eval targets added (20–40% hallucination reduction; Time-to-Stability; Entropy Recovery Rate)
  - Tribunal recovery protocol updated to consult 3D phase position for path selection
  - Heartbeat payload expanded to include D_explore_signal, D_correct_signal
- **`patterns/P-42_AHG.md` → v1.2:** 7-state regime table; D_correct in vocabulary; Tension threshold 1.80
- **`CHANGELOG.md`:** This entry
- **Source:** External AHG-MAS peer review document (Adaptive Harmonic Governance: A Stability-Guided Framework for Multi-Agent Systems)

#### P-42 Collision Fix (prev commit b705834)
- `patterns/P-42_AHG.md` created (renumbered from P-35)
- **`docs/theory/AHG_ARCHITECTURE.md` v1.1**
- `CROSS_REF.md` v4.4
- `docs/ndr_patterns_unified.json` v2.2
- `docs/ECOSYSTEM_INVENTORY.md` updated
- `ENSEMBLE_ROSTER.md`, `SESSION_ANCHOR.md` updated

#### P-35_AHG.md deletion (prev commit 6b6033e)
- Stale `patterns/P-35_AHG.md` deleted

#### Earlier commits
- `e410ae4`: `CROSS_REF.md` v4.3 + `SESSION_ANCHOR.md` + `ENSEMBLE_ROSTER.md`
- `e34af32`: `docs/theory/AHG_ARCHITECTURE.md` v1.0 + `patterns/P-35_AHG.md` (stale, now deleted)
- `5ed1a85`: `docs/agents/PROFESSOR_PRODIGY_KB.md` v1.0
- `b8cf383`: `DEFERRED_ITEMS.md` — S-01–S-08
- `dd2f319`: entrepreneur-hub sweep-reminder + preflight

---

## [S071] — 2026-06-28

- P-37 Stochastic-Deterministic Saga Boundary registered
- P-38 Circuit-Breaker with HITL Escalation registered
- P-39 ACRFence registered
- P-40 Atomix Transactional Tool Boundary registered
- P-41 Sentinel-Phi HITL Durable Queue registered
- Layer 10 (Resilience & Recovery) and Layer 11 (Transactional Integrity) established
- Registry watermark advanced to P-41
- `topology_router.py` v3.6.0 — 8/8 TC passing
- `lifecycle_stability_report.json` created

---

## [S070-r3-P1] — 2026-06-26

- CONSENSUS_TRIAD and CONDUCTED_TRIAD formation patterns registered
- PDMAL-φ / PDMAL-D variant status canonicalized
- Triadic telemetry guidance appended to unified registry
- Eval Terminology Index (S068) added to CROSS_REF
- `docs/lifecycle_harness_v2.md` created
- `docs/ECOSYSTEM_INVENTORY.md` created

---

## [S069] — 2026-06-13 · Ender ratified

- P-35 Procluding Premise Gate registered and ratified
- P-36 Gate Priority Schema registered and ratified
- STASIS-CANONICAL status ratified (migration window 2026-06-13 → 2026-07-13)
- `ndr_patterns_unified.json` v2.1
- v3 named session patterns absorbed into unified registry
- `ndr-pattern-registry-v3.md` deleted

---

## [S066] — 2026-05-30 · Ender ratified

- P-34 Empirical-Threshold-Sweep A-TIER 94.5% attested
- Phase 3 unified merge — Triumvirate
- Registry watermark advanced to P-41

---

*CHANGELOG · Amethyst × COLLEEN · Updated 2026-08-25*
