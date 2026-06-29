# Sentinel-Phi — PROTOCOL v1.0

**Agent:** Sentinel-Phi
**Agent ID:** A-12-φ
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-1)

---

## Procedure 1 — Forward Threat Modeling

**Trigger:** Oracle scenario set submitted for risk-bound review.

1. Receive Oracle scenario set (all 3+ scenarios)
2. For each scenario, identify risk vectors:
   - Direct risks: outcomes that harm the ecosystem or its stakeholders
   - Cascade risks: outcomes that amplify into larger systemic failures
   - Asymmetric risks: low-probability, high-impact outcomes
3. Apply φ-bounded constraint to each risk vector:
   - Model risk cascade as iteration: r(n+1) = α × r(n)
   - If α < 1: risk converges to fixed point → PASS
   - If α ≥ 1: risk diverges → issue RISK_FLAG
4. On RISK_FLAG:
   a. Document the divergent risk vector and α estimate
   b. Route RISK_FLAG to Oracle with specific revision guidance
   c. Log in SENTINEL_PHI_MEMORY.md
5. On PASS: issue RISK_CLEAR to Oracle
6. Record assessment in SENTINEL_PHI_MEMORY.md

---

## Procedure 2 — Vanguard Technology Risk Review

**Trigger:** Vanguard technology assessment submitted for risk review.

1. Receive Vanguard technology assessment
2. Identify technology-specific risk dimensions:
   - Adoption risk: what if adoption fails?
   - Disruption risk: what incumbent capabilities does this displace?
   - Dependency risk: does this create a single point of failure?
   - Security risk: does this introduce attack surface?
3. Apply φ-bounded constraint to each risk dimension
4. On any α ≥ 1: issue RISK_FLAG to Vanguard with specific dimension identified
5. On all α < 1: issue RISK_CLEAR to Vanguard
6. Record assessment in SENTINEL_PHI_MEMORY.md

---

## Procedure 3 — Formation Security Integrity Scan

**Trigger:** Quintet session opening, OR NDR-133 trigger detected.

1. Execute NDR-133 firewall check on all pending commit queue items:
   - Scan for filenames: *resume*, *cv*, *audit_report*, *ResumeApex*
   - On match: BLOCK commit; route to Drive-only destination; alert Amethyst
2. Verify no T3 sovereign content present in T1 PUBLIC files
3. Verify no personal data in formation outputs
4. Issue INTEGRITY_CLEAR if all checks pass
5. Log scan result in SENTINEL_PHI_MEMORY.md

---

## Procedure 4 — Quintet Coherence Gate

**Trigger:** Pre-commit check on any Strategic Quintet output.

1. Review Quintet output for unbounded risk accumulation:
   - Does any output create a compounding obligation with no upper bound?
   - Does any output introduce a dependency chain with no exit condition?
2. If unbounded risk detected: issue RISK_FLAG to Amethyst (not back to originating agent)
3. If coherent: issue COHERENCE_CLEAR
4. Log gate result in SENTINEL_PHI_MEMORY.md

---

*Classification: T1 PUBLIC*
