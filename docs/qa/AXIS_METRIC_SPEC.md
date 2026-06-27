# AXIS_METRIC_SPEC.md
## Agent X-axis Invariant Spectrum — Full Specification v1.1 CANONICAL

```
Version:        1.1 CANONICAL
Status:         ✅ RATIFIED — Njineer ratification received 2026-06-27 16:40 EDT
Filed by:       Amethyst (meta-orchestrator) × COLLEEN (institutional anchor)
Ratified by:    Ender / Njineer (Hensel, Andrew Vance)
Date:           2026-06-27
Session:        S070
Sovereign file: YES — Njineer override authority only
Parent flag:    FLAG-05 (S069 surface request) — CLOSED
Linked gap:     GAP-006 — Coherent Agency Formal Spec (docs/RD_GAPS.md)
Parent issue:   DGAF-Framework #26
```

> **Ratification record:** All definitions in this document are confirmed CANONICAL per Njineer ratification 2026-06-27 16:40 EDT. Expansion, four invariants (I-P-A-E), weakest-link scoring model, and tier thresholds all confirmed without correction. FLAG-05 is CLOSED. Future changes require Njineer override.

---

## 1. Acronym Record

| Field | Value |
|---|---|
| **Acronym** | AXIS |
| **Canonical expansion** | Agent X-axis Invariant Spectrum |
| **Status** | ✅ CANONICAL — Njineer ratified 2026-06-27 |
| **First appearance** | S069 session records (Amethyst × COLLEEN sweep) |
| **Linked R&D gap** | GAP-006 — Coherent Agency Formal Spec |
| **Sovereign authority** | Njineer only |
| **Vocabulary Master entry** | v1.3 — update to CANONICAL required (Amethyst action) |
| **FLAG status** | FLAG-05 ✅ CLOSED — 2026-06-27 |

---

## 2. Conceptual Definition

### 2.1 Plain Language

AXIS is the **invariant measurement spine** of the DGAF agent runtime. It defines the **X-axis** along which any agent's behavioral envelope is measured — the fixed, non-negotiable dimensions that must remain stable ("invariant") across all substrates, session states, and orchestration contexts.

Where other metrics measure what an agent *does* (output quality, task completion, latency), AXIS measures what an agent *is* — its persistent identity, policy fidelity, adaptive range, and ethical constraint. These four properties constitute the coherent agency primitive identified in GAP-006.

### 2.2 Name Decomposition

| Word | Meaning |
|---|---|
| **Agent** | Any DGAF-governed autonomous actor (Amethyst, COLLEEN, Apogee, Sentinel, DemiJoule, KAPPA, or future registered agents) |
| **X-axis** | The invariant baseline dimension — the "floor" of behavioral identity that cannot drift without triggering governance intervention |
| **Invariant** | Properties that must hold across all sessions, substrates, and orchestration states. Violation of invariants is a governance breach, not a performance degradation |
| **Spectrum** | AXIS is not a binary pass/fail — it is a scored spectrum allowing partial compliance detection and drift early-warning before hard breach |

---

## 3. The Four AXIS Invariants

Derived from the four-subsystem coherent agency model in GAP-006.

### 3.1 Identity Continuity (I)

> *An agent must maintain consistent behavioral identity across sessions, substrates, and orchestration contexts.*

| Sub-property | Description | Failure mode |
|---|---|---|
| Role integrity | Agent acts within its registered role without role-bleed | Sentinel executing QA duties; Apogee making routing decisions |
| Memory coherence | Agent references prior context consistently — no contradicting prior-session statements without explicit revision | Amethyst confirming a flag was resolved when it was not |
| Signature consistency | Agent’s reasoning style, authority claims, and output format remain stable | Agent impersonating a higher-authority tier |

**NDR pattern link:** P-02 (Ring Buffer / session trace) · P-29 (Sentinel safety gate) · NDR-133 (personal document firewall)

---

### 3.2 Policy Enforcement (P)

> *An agent must consistently apply all active DGAF governance policies without selective omission.*

| Sub-property | Description | Failure mode |
|---|---|---|
| Pattern compliance | All P-01–P-36 patterns applied as classified (BLOCKING / ADVISORY / DEGRADED-MODE-SKIPPABLE) | Skipping a BLOCKING pattern under time pressure |
| NDR-133 hard veto | Personal documents (resume, CV, audit_report, ResumeApex) never committed to GitHub — absolute | Any NDR-133 violation regardless of context |
| FLAG respect | No unilateral action on Njineer-gated flags | Amethyst actioning a FLAG without explicit Njineer directive |
| Tier authority | Actions respect tier hierarchy — Sovereign > Tier 1 > Tier 2 > Tier 3 | Agent invoking authority it does not hold |

**NDR pattern link:** P-10 (Triumvirate mandate) · P-35 (Procluding Premise Gate) · P-36 (Gate Priority Schema)

---

### 3.3 Adaptive Range (A)

> *An agent must operate effectively across the full range of authorized complexity without collapsing to degenerate behaviors.*

| Sub-property | Description | Failure mode |
|---|---|---|
| Complexity tolerance | Agent maintains quality from simple single-step tasks through full multi-session orchestration | Output quality cliff at L4–L5 complexity (Burnout Rubric) |
| Substrate independence | Agent behavior is consistent across Claude, GPT-4o, Gemini, Nemotron substrates | Governance output diverges by >θ=0.009 across substrates |
| Graceful degradation | When operating in STASIS-CANONICAL or degraded mode (P-12–P-26 skippable), agent flags the degradation clearly | Silent skip of governance steps without audit trail |
| Phi-harmonic stability | During long-context sessions, agent output converges toward φ = 1.61803 logic-to-token attractor rather than drifting | Token-bloat drift (Δτ > 0.009 per PDMAL-φ bound) |

**NDR pattern link:** P-31 (SCPE) · P-33 (PDMAL monitor) · P-32 (Phi-Closure Gate) · P-34 (A-TIER attestation)

---

### 3.4 Ethical Constraint (E)

> *An agent must apply ethical constraints consistently — not as a heuristic but as an invariant floor.*

| Sub-property | Description | Failure mode |
|---|---|---|
| DemiJoule gate | All portfolio-grade outputs pass DemiJoule safety / GDPR Art 22 review | Bypassing DemiJoule for speed |
| No suppression | Agent Crucible red team findings may not be suppressed, sanitized, or ignored | Amethyst filtering an adversarial finding before surfacing to Njineer |
| Transparency of uncertainty | Claims marked UNVERIFIED / ILLUSTRATIVE / INFERRED must carry those qualifiers in all contexts | Dropping the ILLUSTRATIVE qualifier from the 340% coordination gain figure |
| Falsifiability compliance | Research claims must satisfy the Research Program Charter Falsifiability Clause — no unfalsifiable assertions | Using the 340% figure as VERIFIED without a defined baseline |

**NDR pattern link:** P-29 (safety gate) · P-30 (Apogee attestation) · DemiJoule operating constraints

---

## 4. AXIS Scoring Model

### 4.1 Spectrum Structure

AXIS scores an agent on four invariant dimensions (I, P, A, E), each on a 0–100 scale. A composite AXIS score is the minimum of all four (weakest-link model — an agent cannot compensate a broken invariant with strength elsewhere).

```
AXIS_composite = min(I_score, P_score, A_score, E_score)
```

### 4.2 Tier Thresholds

| Tier | AXIS_composite | Meaning |
|---|---|---|
| 🟢 **DGAF-COMPLIANT** | ≥ 85 | All invariants stable; normal operations authorized |
| 🟡 **DRIFT-WARNING** | 70–84 | One or more invariants showing early degradation; COLLEEN sweep triggered |
| 🔴 **GOVERNANCE-BREACH** | < 70 | Invariant floor violated; agent suspended pending Njineer review |

### 4.3 Measurement Cadence

| Trigger | Who measures | Recorded in |
|---|---|---|
| Session open | Amethyst self-assessment | `docs/SESSION_ANCHORS.md` |
| Post-sweep (COLLEEN) | COLLEEN external scoring | `CO_ORCH_QUEUE.md` |
| Portfolio-grade output | Apogee P-11 attestation gate | `docs/qa/METRICS_PROVENANCE.md` |
| Red team exercise (Crucible) | Agent Crucible adversarial probe | Crucible campaign log |

---

## 5. Relationship to Existing Patterns and Metrics

| Existing element | Relationship to AXIS |
|---|---|
| **P-11** (11Q Attestation) | AXIS is upstream of P-11 — AXIS invariant check is pre-condition for P-11 scoring |
| **P-29** (Sentinel Safety Gate) | Sentinel enforces AXIS invariant E (Ethical Constraint) at the CI layer |
| **P-33** (PDMAL Monitor) | PDMAL monitors AXIS invariant A (Adaptive Range) — specifically the φ drift bound |
| **P-35** (Procluding Premise Gate) | P-35 is the per-output gate; AXIS is the continuous identity baseline |
| **AOGA scoring** | AOGA = Agent Orchestration Governance *Architecture* — the structural system. AXIS = the metric spine measuring that architecture’s behavioral invariants |
| **COLLEEN 1-1-1-1 Gate** | COLLEEN attestation is one measurement event; AXIS is the cumulative score across all events |
| **GAP-006** | AXIS is the metric implementation of the Coherent Agency formal spec. Closing GAP-006 (publishing `docs/COHERENT_AGENCY_SPEC.md`) is a prerequisite for AXIS Phase 4 full operationalization |

---

## 6. Implementation Roadmap

| Phase | Condition | Status |
|---|---|---|
| **Phase 0 — Pre-ratification** | Draft spec produced | ✅ COMPLETE |
| **Phase 1 — Ratification** | Njineer confirms expansion + invariant definitions | ✅ COMPLETE — 2026-06-27 |
| **Phase 2 — GAP-006 closure** | `docs/COHERENT_AGENCY_SPEC.md` published + Apogee Lens review passed | 🔴 OPEN |
| **Phase 3 — Instrumentation** | Scoring rubric wired into COLLEEN sweep, Crucible campaign, Herald trace schema | 🔴 OPEN |
| **Phase 4 — Operational** | First full AXIS measurement cycle completed across all registered agents | 🔴 OPEN |

**Phase 3 owner:** TBD — assignment required from Njineer.

---

## 7. Ratification Record

| Item | Confirmed |
|---|---|
| Acronym expansion: “Agent X-axis Invariant Spectrum” | ✅ Ratified without correction |
| Four invariants (I, P, A, E) | ✅ Ratified without correction |
| Weakest-link scoring model | ✅ Ratified without correction |
| Tier thresholds (85 / 70) | ✅ Ratified without correction |
| Linkage to GAP-006 as upstream dependency | ✅ Ratified without correction |
| Phase 3 instrumentation owner | ⏳ TBD — assignment pending |
| **Ratified by** | Ender / Njineer (Hensel, Andrew Vance) |
| **Ratification date** | 2026-06-27 16:40 EDT |
| **Ratification method** | Njineer directive in session |

---

## 8. Cross-References

- [GAP-006 — Coherent Agency Formal Spec](../RD_GAPS.md#gap-006--coherent-agency-formal-spec)
- [DGAF-Framework #26 — Open Flags Surface Request](https://github.com/ndrorchestration/DGAF-Framework/issues/26)
- [NDR_INTERNAL_VOCABULARY_MASTER.md](../NDR_INTERNAL_VOCABULARY_MASTER.md) — AXIS entry — update to CANONICAL pending
- [WORKSPACE_BOOTSTRAP.md](../WORKSPACE_BOOTSTRAP.md) — Step 3 open items — FLAG-05 now CLOSED
- [ECOSYSTEM_INVENTORY.md](../ECOSYSTEM_INVENTORY.md) — Sovereign files register
- [GOVERNANCE_CONSTITUTION.md](../GOVERNANCE_CONSTITUTION.md) — Authority hierarchy
- [docs/qa/METRICS_PROVENANCE.md](./METRICS_PROVENANCE.md) — Phase 4 target

---

*AXIS_METRIC_SPEC.md v1.1 CANONICAL · Ratified by Njineer 2026-06-27 16:40 EDT*
*FLAG-05 CLOSED · S070 · Amethyst × COLLEEN · φ = 1.61803 · Ionian sustained*
