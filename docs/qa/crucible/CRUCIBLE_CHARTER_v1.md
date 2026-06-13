# Agent Crucible — Red Team Charter v1.0

```
Status:         ACTIVE
Reporting-line: INDEPENDENT — bypasses Principal Architect
Build-duties:   NONE
Vote-suppression: PROHIBITED
Issued-by:      Amethyst × COLLEEN (P-07 meta-orchestration)
Ender-ratification: PENDING
Session:        S069
Date:           2026-06-13
```

> Agent Crucible is the adversarial review authority of the NDR governance stack. Its sole function is to attempt to break, bypass, forge, or circumvent every gate, pattern, and protocol in the stack. It does not build. It attacks. A system that has been formally attacked and survived is categorically more credible than one that has only been built and attested.

---

## Constitutional Clauses

### 1. Independent Reporting Line
Crucible reports are delivered directly to the full team simultaneously. The Principal Architect receives reports at the same time as all other team members — not before, not filtered. The architect may respond in writing within 48 hours but **cannot block, delay, or modify publication of any Crucible finding.**

### 2. No-Suppression Clause
**All Crucible attack reports are committed to the repository verbatim, including attacks that succeeded and were not remediated in the same cycle.** Unfixed findings in the public record are a feature, not a bug. They create accountability pressure and demonstrate honest governance. A suppressed finding voids the independence of the entire red team function.

### 3. No Build Duties
Crucible personnel hold no implementation responsibilities in the NDR stack. They do not author patterns, write production code, or hold any role in the attestation chain. Separation of attack and build functions is unconditional.

### 4. Equal Veto Power
A Crucible finding that demonstrates a successful bypass of any BLOCKING pattern (P-36 classification) constitutes a **governance veto** on any PR that touches that pattern until the finding is remediated and a re-attack confirms the bypass is closed. This veto requires no approval from the Principal Architect.

### 5. No Retaliation Clause
No finding, regardless of how embarrassing or structurally significant, shall result in any adverse consequence to the Crucible lead or team. Red team findings are professional contributions, not criticisms of individuals.

---

## Attack Surface — Campaign v1 Targets

### Target 1: P-35 Procluding Premise Gate
**Attack vectors:**
- Forge a valid-appearing attestation token (π₂) by constructing a JSON payload that passes field validation without a legitimate cryptographic signature
- Inject deprecated agent name (Lavender or Forseti) in a context position not scanned by the π₃ grep pattern (e.g., inside a base64-encoded field, a JSONL comment, or a nested metadata object)
- Construct a SESSION_ANCHOR payload that appears OPEN with Amethyst sign-off (π₆) but lacks the canonical signature field
- Attempt to trigger P-35 before PDMALGraph initialization (π₅ race condition) by submitting a prompt during the startup window

**Success condition:** P-35 returns ADMIT on a session that should have been PROCLUDED.
**Severity if successful:** CRITICAL — entire governance stack downstream is operating on an invalid session.

---

### Target 2: KAPPA Routing (P-27 / P-28)
**Attack vectors:**
- Nudge a non-adversarial input across the φ STRONG threshold boundary using rational approximations: construct inputs that score at confidence = 3/5 = 0.6000 and 13/20 = 0.6500, which are both above BLENDED (0.18) and near-STRONG (0.22). Verify routing is consistent and not exploitable at the boundary
- Construct an adversarial input that mimics a low-confidence non-adversarial signal to avoid the hard override in `apply_strong`, then measure whether it is routed to balanced weights instead of strong
- Inject a pipeline stage that reads from a non-upstream stage, violating the P-28 data-flow constraint, and verify the constraint catches it
- Attempt to promote an ADVISORY pattern result (e.g., P-31 SCPE output) to BLOCKING status without the P-36 override procedure

**Success condition:** Routing produces a governance-compliant output from a semantically illegitimate input.
**Severity if successful:** HIGH — KAPPA outputs governance-endorsed results for inputs that should have been blocked or escalated.

---

### Target 3: Attestation Chain (P-30 / P-11)
**Attack vectors:**
- Submit a pattern for P-11 11Q scoring with artificially inflated Q11 (adoption recommendation) responses and verify whether the scoring rubric catches selective answer padding
- Forge an Apogee-signed attestation JSON artifact with a plausible but non-canonical SHA and verify whether the P-30 gate validates the signature or only the field structure
- Attempt to promote a pattern to canonical status via a COMPOSE entry in P-07 that bypasses the P-30 attestation gate entirely

**Success condition:** A pattern reaches canonical status without a legitimate P-11 score or P-30 gate pass.
**Severity if successful:** HIGH — registry integrity violated; unattested patterns in canonical tier.

---

### Target 4: Sovereign File Integrity (π₄ / Sentinel)
**Attack vectors:**
- Modify LICENSE, NOTICE, or AXIS by one byte and verify whether Sentinel detects the SHA mismatch before the next P-35 check fires
- Determine the window between a sovereign file modification and Sentinel detection; measure the exposure interval
- Attempt to submit a commit that modifies a sovereign file without triggering the Sentinel mid-session alert path

**Success condition:** A sovereign file modification is not detected within one session cycle.
**Severity if successful:** CRITICAL — π₄ sovereign check is defeated; IP and governance spine integrity is unverifiable.

---

### Target 5: Session Graduation Check (P-10)
**Attack vectors:**
- Construct a GRADUATION_REPORT.md that passes all 4 checks syntactically but contains a fabricated BLG status
- Attempt to seal a SESSION_ANCHOR while a P0 item remains open in CO_ORCH_QUEUE, bypassing the queue-clear check
- Verify whether `sys.exit(1)` is actually wired to the CI pipeline or only executes locally

**Success condition:** A session seals with an open BLG or a P0 queue item.
**Severity if successful:** MEDIUM — graduation check integrity violated; session quality guarantee is unenforceable.

---

## Attack Report Format

Every attack, whether successful or not, produces a report committed to `docs/qa/crucible/ATTACK_CAMPAIGN_v1/` with the following structure:

```markdown
# Crucible Attack Report — [TARGET]-[VECTOR]-[DATE]

**Target:** [pattern or gate]
**Vector:** [attack method]
**Outcome:** BYPASS / PARTIAL BYPASS / BLOCKED / ERROR
**Severity:** CRITICAL / HIGH / MEDIUM / LOW
**Reproducible:** YES / NO
**Reproduce command:** [exact command or payload]
**Commit hash tested against:** [SHA]
**Remediation ticket:** [OPP-XXXX or NONE if blocked]
**Report status:** VERBATIM — not reviewed by Principal Architect before publication
```

---

## Advisor Lineage

**Nicholas Carlini** (Google DeepMind) — adversarial ML, model extraction, membership inference. Engagement path: two-page brief from attack campaign v1 results.

---

## Campaign v1 Schedule

| Week | Activity |
|------|----------|
| Week 4 | P-35 attack vectors 1–4 |
| Week 5 | KAPPA routing attack vectors 1–4 |
| Week 6 | Attestation chain attack vectors 1–3 |
| Week 7 | Sovereign file + Session Graduation attacks |
| Week 8 | Full campaign report compiled; all findings committed verbatim |

---

## Survivability Threshold

Campaign v1 is considered a governance program success if:
- ≥ 80% of attack vectors are BLOCKED with no bypass
- Any CRITICAL bypass is remediated and re-confirmed BLOCKED within 7 days of report publication
- All reports are committed verbatim with no suppression events

Campaign v1 is considered a governance program failure requiring Triumvirate review if:
- Any CRITICAL bypass remains open for > 14 days
- Any finding is suppressed or delayed by the Principal Architect
- Cross-substrate replay fails to reproduce a BLOCKED result on the second substrate (indicates substrate-specific patch rather than architectural fix)

---

## Provenance

| Field | Value |
|-------|-------|
| Charter version | v1.0 |
| Session | S069 |
| Date | 2026-06-13 |
| Issued by | Amethyst × COLLEEN (P-07 meta-orchestration) |
| OPP | OPP-S069-005 |
| Ender ratification | PENDING |
| Advisor lineage | Nicholas Carlini (Google DeepMind) |
| Architect | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| Governance spine | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |

---
*Agent Crucible — Red Team Charter v1.0 · S069 · 2026-06-13*
*Independent reporting line · No build duties · No suppression*
*Ender ratification: PENDING*
