# Sentinel-Phi — Integration v1.0

**Agent:** Sentinel-Phi
**Agent ID:** A-12-φ
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Integration Contracts

### Sentinel-Phi ↔ Oracle (risk review gate)

| Direction | Signal | Trigger |
|---|---|---|
| Oracle → Sentinel-Phi | Scenario set for φ-bounded risk review | Scenario construction complete |
| Sentinel-Phi → Oracle | CLEAR or RISK_FLAG + revision guidance | Review complete |
| Oracle → Sentinel-Phi | Revised scenario set | RISK_FLAG revision complete |

### Sentinel-Phi ↔ Vanguard (risk gate)

| Direction | Signal | Trigger |
|---|---|---|
| Vanguard → Sentinel-Phi | Technology assessment for φ-bounded risk review | Assessment complete |
| Sentinel-Phi → Vanguard | CLEAR or RISK_FLAG + revision guidance | Review complete |
| Vanguard → Sentinel-Phi | Revised assessment | RISK_FLAG revision complete |

### Sentinel-Phi → Nova / Zenith

| Signal | Condition |
|---|---|
| Implicit CLEAR (via Oracle/Vanguard routing) | Sentinel-Phi CLEAR allows Oracle/Vanguard to route downstream |
| RISK_FLAG (holds Nova/Zenith from receiving output) | Divergent risk vector detected in upstream output |

### Sentinel-Phi ↔ Prof Prodigy (mathematical verification)

| Direction | Signal | Trigger |
|---|---|---|
| Sentinel-Phi → Prof Prodigy | Contraction mapping model for α < 1 verification | Mathematical risk model used |
| Prof Prodigy → Sentinel-Phi | VERIFIED or CORRECTION | Verification complete |

### Sentinel-Phi → Amethyst (escalation)

| Signal | Condition |
|---|---|
| RISK_FLAG escalation package (full analysis + originating agent revision attempt) | Unresolvable RISK_FLAG |
| NDR-133 BLOCK notification | Personal document detected in commit queue |
| COHERENCE_CLEAR or COHERENCE_FLAG | Quintet pre-commit coherence gate result |

### Sentinel-Phi ↔ The Auditor (inherited QA chain)

| Direction | Signal | Trigger |
|---|---|---|
| Sentinel-Phi → Auditor | Security scan results for QA chain integrity | On Auditor request |
| Auditor → Sentinel-Phi | Constraint verify result relevant to security | Constraint verify run |

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Oracle revision fails to resolve RISK_FLAG | Escalate to Amethyst with full package |
| Vanguard revision fails to resolve RISK_FLAG | Escalate to Amethyst |
| NDR-133 BLOCK — architect override requested | Route override request to Njineer; do not auto-approve |
| Prof Prodigy CORRECTION on contraction mapping | Revise risk model; re-run α < 1 test |
| α ≥ 1 vector in committed output detected post-commit | Issue RISK_FLAG retroactively; notify Amethyst; log in SWEEP_LOG correction entry |

---

*Classification: T1 PUBLIC*
