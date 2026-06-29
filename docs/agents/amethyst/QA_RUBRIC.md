# QA Rubric — Agent Amethyst

**Agent:** Agent Amethyst (Amethyst-Conductor)  
**Role Domain:** Meta-Orchestration  
**Formation:** Conductor (all formations)  
**Rubric Version:** 1.0  
**Authority:** Njineer + Amethyst sign-off required for changes  
**Last Updated:** 2026-06-29

---

## Purpose

This rubric defines the quality criteria, pass thresholds, and failure modes for evaluating Amethyst's meta-orchestration outputs in any given session. It is the operational contract against which Apogee scores Amethyst artifacts.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **Commit Gate Integrity** | 20% | ≥ 0.90 | Did Amethyst correctly gate or ungate each commit? No false approvals on sovereign files. No unilateral override of Sentinel hard-veto without Njineer confirmation. |
| D2 | **Normative Decision Quality** | 20% | ≥ 0.85 | Are decisions traceable to DGAF canon, AXIS policy, or explicit Njineer instruction? No invented authority. |
| D3 | **Orchestration Coverage** | 15% | ≥ 0.80 | Were all required agents activated for the formation? Did Amethyst correctly call Trio vs. Quintet vs. Extended? |
| D4 | **BLG Surface + Closure** | 15% | ≥ 0.85 | Were all BLGs surfaced at P-02? Were closure artifacts committed before the BLG was marked CLOSED? |
| D5 | **Phase Sequencing Fidelity** | 15% | ≥ 0.88 | Did execution follow the canonical phase order? No phase skips. Gate receipts present for P-11 and P-15. |
| D6 | **Drift Prevention** | 10% | ≥ 0.80 | Did Amethyst maintain state across turns? No unexplained context resets. |
| D7 | **Role Boundary Compliance** | 5% | ≥ 0.95 | Amethyst did not score artifacts (Apogee lane). Did not impersonate another agent. |

**Composite Score Formula:**  
`Score = Σ(Dim_score × Dim_weight)`  
Pass: ≥ 0.85 composite for routine commits; ≥ 0.90 for seal commits (P-15).

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **False commit approval** | Sovereign file modified without Sentinel + Njineer confirmation | Hard rollback via Reciprocity; re-gate with full Quintet |
| F2 | **Phase skip** | Phase N+2 executed before Phase N+1 artifacts committed | Surface as BLG; re-execute missing phase before proceeding |
| F3 | **Authority fabrication** | Amethyst cites a policy that does not exist in DGAF canon | Sentinel flags; Apogee D2 score drops to 0; Njineer review required |
| F4 | **Drift cascade** | Context reset causes Amethyst to contradict a prior session decision | COLLEEN surfaces delta; Amethyst re-anchors to P-21 state log |
| F5 | **Formation under-activation** *(non-obvious)* | Amethyst uses Trio formation for a sovereign file touch, missing Reson + Sentinel | Sentinel veto fires; Quintet re-assembled; Reson score re-run |

---

## Gate Ownership

| Gate | Amethyst Role |
|------|---------------|
| P-02 | BLG surface confirmation |
| P-11 | Receives Apogee 11Q score; decides go/no-go |
| P-15 | Final seal sign-off (requires Reson ≥ 0.75, Sentinel PASS) |
| P-21 | State anchor emission (session-close) |

---

## Scoring Cadence

- **Per-session:** Apogee runs D1–D7 at session close and logs to `CERTIFICATION_INDEX`.
- **Per-seal commit:** D1 + D5 + D7 re-scored at P-15 before merge.
- **Quarterly:** Full 7-dimension audit against last 4 sessions.

---

*Rubric authority: Amethyst-Conductor. Changes require Njineer confirmation.*
