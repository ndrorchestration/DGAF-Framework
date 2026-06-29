# QA Rubric — Agent Sentinel

**Agent:** Agent Sentinel  
**Role Domain:** Process Compliance / Security  
**Formation:** Quintet  
**Rubric Version:** 1.0  
**Authority:** Amethyst-Conductor (Sentinel veto overrides Amethyst; only Njineer resolves conflict)  
**Last Updated:** 2026-06-29

---

## Purpose

Defines quality criteria for Sentinel's CI/CD enforcement, secret scanning, sovereign file guard, and boundary violation detection. Sentinel is the security and compliance hard-stop layer.

---

## Evaluation Dimensions

| Dim | Dimension | Weight | Pass Threshold | Scoring Notes |
|-----|-----------|--------|----------------|---------------|
| D1 | **Sovereign File Guard Accuracy** | 30% | ≥ 0.98 | LICENSE, NOTICE, AXIS touched only with full Quintet + Njineer confirmation. Zero false clearances. |
| D2 | **Secret Scan Coverage** | 25% | ≥ 0.95 | All committed files scanned. No credential, token, or key committed to public repo. |
| D3 | **CI/CD Enforcement Fidelity** | 20% | ≥ 0.90 | CI gates fire correctly. No bypass of required checks. Failed builds not merged. |
| D4 | **Boundary Violation Detection** | 15% | ≥ 0.88 | Role separation violations (e.g., COLLEEN making normative decisions) detected and escalated. |
| D5 | **NDR-133 Trigger Response** | 10% | ≥ 0.92 | Reson firewall NDR-133 patterns flagged within the same session turn they appear. |

**Composite Pass:** ≥ 0.92 for all operations. No tiered threshold — Sentinel operates at high-assurance level uniformly.

---

## Failure Modes

| ID | Failure | Trigger | Mitigation |
|----|---------|---------|------------|
| F1 | **Sovereign file false clearance** | Sentinel clears a sovereign file touch without full Quintet confirmation | Immediate hard rollback; Njineer notified; Sentinel re-calibration required |
| F2 | **Secret commit miss** | A token or credential passes scan and reaches GitHub | Revoke credential immediately; force-push removal; post-mortem required |
| F3 | **Veto suppression** *(non-obvious)* | Amethyst-level orchestration silently bypasses Sentinel veto by reframing the file as non-sovereign | Reciprocity triggers audit; file sovereignty re-evaluated against PROPRIETARY.md T3 list |

---

## Gate Ownership

| Gate | Sentinel Role |
|------|---------------|
| P-15 | Hard veto authority — sovereign file guard |
| All | CI/CD gate enforcement |

---

*Rubric authority: Amethyst-Conductor. Sentinel-Amethyst conflicts resolved by Njineer only.*
