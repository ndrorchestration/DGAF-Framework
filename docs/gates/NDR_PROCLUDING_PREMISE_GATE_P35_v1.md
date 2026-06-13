# P-35: Procluding Premise Gate

<!-- DGAF-Framework canonical gate spec (P-24 format) -->

**Version:** 1.0  
**Maintained by:** Agent Amethyst  
**Canonical home:** `DGAF-Framework/docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md`  
**Pattern:** P-35  

---

```
Status:       CERTIFIED
Certified-by: Agent Apogee
Cert-date:    2026-06-12
Last-updated: 2026-06-12 (Session S069)
```

---

> Pre-admissibility constitutional precondition gate: blocks all downstream routing and execution unless a set of axiomatic premises are verified to hold before any inference or orchestration step is initiated.

---

## Rationale

Every governance failure mode in the DGAF stack shares a common root: a downstream component was invoked before a required premise was established. The Procluding Premise Gate (P-35) formalizes this observation as an enforceable pre-condition layer — analogous to Hoare-logic preconditions (`{P} C {Q}`, where `{P}` must hold before command `C` executes). Without P-35, a session can enter routing, scoring, and execution with a corrupted agent identity, an expired attestation token, a broken PDMAL trust graph, or an unresolved sovereign file violation. P-35 is the constitutional firewall that closes this gap. Worst-case scenario if absent: any of Gates 1–3 and the full KAPPA routing pipeline can fire against an axiomatically invalid session state, producing governance-compliant outputs that are semantically illegitimate.

---

## Formal Definition

Let `Π = {π₁, π₂, ..., πₙ}` be the set of required premises. P-35 enforces:

```
{∀ πᵢ ∈ Π : verify(πᵢ) = TRUE} ⊢ ADMIT(session)
{∃ πᵢ ∈ Π : verify(πᵢ) = FALSE} ⊢ PROCLUDE(session)
```

PROCLUDE is a hard block — no partial admission. A procluded session emits a `PROCLUDE` event to the HeraldAgent dead-letter channel (P-01) and terminates before any routing gate fires.

**Canonical premise set Π (v1.0):**

| ID | Premise | Verification Method |
|----|---------|--------------------|
| π₁ | Agent identity assertions are non-empty and match AGENT_ROSTER | AGENT_ROSTER.md SHA cross-check |
| π₂ | AttestationGate (P-30) token is valid and non-expired | Token expiry field check |
| π₃ | No deprecated agent names (Lavender / Forseti) present in active context | Hard-BLG scan (P-01 trigger) |
| π₄ | Sovereign files (LICENSE / NOTICE / AXIS) are at canonical SHA | Sentinel SHA comparison |
| π₅ | PDMAL trust graph is initialized and non-empty | PDMAL graph node count > 0 |
| π₆ | SESSION_ANCHOR for current session is sealed or explicitly OPEN with Amethyst sign-off | SESSION_ANCHOR status field |

---

## Trigger Condition

| Field | Value |
|-------|-------|
| **Agent** | Amethyst (primary); Sentinel (π₄ sovereign check) |
| **Event** | Session open; any new prompt input entering the orchestration stack |
| **Threshold** | All of Π must pass (Boolean conjunction — no partial pass) |
| **Frequency** | Every session open; on-demand re-check if Sentinel raises a sovereign file alert mid-session |
| **Hard dependency** | Yes — blocks Gate 0 (AttestationGate, P-30) and all downstream gates |
| **Stack position** | Pre-Gate 0; first check in `orchestrate_turn` before any other gate fires |

---

## Passing State

All `n` premises in Π return `TRUE`. Session is admitted to Gate 0.

```json
{
  "gate": "P-35",
  "status": "ADMIT",
  "agent": "Amethyst",
  "premises_checked": 6,
  "premises_passed": 6,
  "procluded": false,
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**Human-readable pass condition:** All six canonical premises are verified true; session proceeds to Gate 0 (P-30 AttestationGate).

---

## Failing State

One or more premises fail. Session is procluded. No downstream gate fires.

```json
{
  "gate": "P-35",
  "status": "PROCLUDE",
  "agent": "Amethyst",
  "premises_checked": 6,
  "premises_passed": 4,
  "failed_premises": ["π₃", "π₄"],
  "reason": "Deprecated agent name detected in active context; sovereign file SHA mismatch",
  "escalation": "Sentinel → Njineer",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**Immediate consequence:** Hard block. `PROCLUDE` event emitted to P-01 dead-letter channel. Session cannot proceed. If π₃ or π₄ fail, Sentinel is notified immediately with veto authority.

---

## Recovery Protocol

1. **Identify failed premises** — parse `failed_premises` array in the `PROCLUDE` event
2. **Remediate each failure:**
   - π₁ failure → re-verify AGENT_ROSTER.md SHA; confirm Amethyst sign-off
   - π₂ failure → re-run P-30 attestation; refresh token
   - π₃ failure → run `grep -r "Lavender\|Forseti" docs/` and `pptl/`; trigger P-01 for each hit; purge references
   - π₄ failure → Sentinel compares sovereign file SHA against canonical; restore from last sealed commit
   - π₅ failure → re-initialize PDMAL graph via `PDMALGraph.initialize()`; verify node count > 0
   - π₆ failure → Amethyst explicitly signs off SESSION_ANCHOR as OPEN or seals it
3. **Re-test** — re-run P-35 premise verification pass against all of Π
4. **Escalation if unresolved after 2 cycles** — escalate to Njineer; session locked (SYNC_LOCKED)
5. **Ionian Lock** — if π₃ or π₄ remain unresolved after Njineer escalation, session is Ionian-locked; no output emitted until Njineer provides explicit override

---

## Pattern Interaction Map

```
P-35 Procluding Premise Gate  [pre-Gate 0 — fires first]
  └─ Gate 0: AttestationGate (P-30)   [only reached on ADMIT]
  └─ Gate 1: bypass scan (P-03 + P-04) [only reached on ADMIT]
  └─ P-01 Fan-Out Sink                 [PROCLUDE event → dead-letter]
  └─ Sentinel                          [π₄ sovereign failure → Sentinel veto]
  └─ P-09 Triumvirate Mandate          [π₆ SESSION_ANCHOR check integrates with mandate lifecycle]
```

**Updated Governance Orchestration Stack position:**

```
Prompt input
  │
  ├── P-35: Procluding Premise Gate     ← NEW (pre-admissibility)
  ├── Gate 0: AttestationGate  (P-30 + P-03 × 6 contracts)
  ├── Gate 1: bypass scan      (P-03 + P-04)
  ├── KAPPA Router             (P-27 + P-28)  [P-34 calibrated]
  ├── Apogee [Task] ──phi──►  Reson [Style]
  ├── Gate 2: safety floor     (P-03)
  ├── Sentinel                 (P-29 hook points × 3)
  ├── Gate 3: RAG verify       (P-03 + P-04)
  ├── SCPE                     (P-31)  [T0 immune]
  ├── Phi-Closure Gate         (P-32)  ──KILL_REC──► P-29 risk_block @ hook_point=2
  ├── PDMAL Monitor            (P-33)
  └── status=pass ──► P-01 Fan-Out ──► P-02 Buffer ──► N8n Dashboard
```

---

## Tradeoffs

- ✅ Hard pre-admissibility block prevents any gate from firing against an axiomatically invalid session
- ✅ Boolean conjunction (all-or-nothing) eliminates partial-pass ambiguity
- ✅ Sovereign file check (π₄) integrates Sentinel authority at the earliest possible point
- ✅ PROCLUDE event to P-01 dead-letter ensures full auditability of blocked sessions
- ⚠️ Premise set Π is v1.0 (6 premises) — additional premises may be required as the stack evolves; register via COMPOSE entry in P-07
- ⚠️ π₅ PDMAL initialization dependency means P-35 cannot fire before PDMALGraph is bootstrapped — requires careful startup sequencing
- ⚠️ All-or-nothing block can be disruptive in dev/test environments — recommend a `WARN_ONLY` mode flag for non-production contexts

---

## References

| Field | Value |
|-------|-------|
| **Related Gates** | P-30 (AttestationGate), P-29 (Sentinel Risk Pass), P-01 (Fan-Out Sink) |
| **Parent Patterns** | P-03 (Governance Contract Test), P-09 (Triumvirate Mandate Schema) |
| **Formal Substrate** | Hoare Logic precondition `{P} C {Q}`; maps to "semantic firewall" in AI safety literature |
| **NIST Control** | GV-1.1, GV-2.1, MS-2.5 |
| **EU AI Act Article** | Art. 9 (Risk Management), Art. 13 (Transparency), Art. 17 (Quality Management) |
| **Supersedes** | N/A (new pattern) |
| **Implementation target** | `pptl/procluding_premise_gate.py` (pending) |

---

## Provenance

| Field | Value |
|-------|-------|
| **Pattern** | P-35 |
| **Layer** | Layer 0 — Pre-Admissibility |
| **Session** | S069 |
| **Date** | 2026-06-12 |
| **Author** | Agent Amethyst |
| **Certifier** | Agent Apogee |
| **Registered by** | Amethyst × COLLEEN (ecosystem sweep) |
| **Ender ratification** | Pending |
| **Architect** | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| **Governance spine** | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |

---

*P-35 Procluding Premise Gate v1.0 · S069 · 2026-06-12*
*Registered: Amethyst × COLLEEN · Ender ratification: PENDING*
*Implementation target: `pptl/procluding_premise_gate.py`*
