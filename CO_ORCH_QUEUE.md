# Amethyst × COLLEEN Co-Orchestration Queue

> **SSoT hand-off substrate for the Dual-Agent Persistent Sweep Loop (NDR P-07)**
> COLLEEN detects → scores via 1-1-1-1 gate → classifies → writes here.
> Amethyst reads → validates NDR fit → executes → commits → marks DONE.
> Append-only. Completed entries archived below, never deleted.
>
> Formation: Co-Orchestration Sweep Triad (Conducted)
> Prime authority: Amethyst · Detect authority: COLLEEN · Comms: Herald
> Governed by: NDR P-07 + P-08 (Triad Taxonomy)

---

## Queue Status

| Stat | Count |
|---|---|
| PENDING | 6 |
| IN_PROGRESS | 1 |
| DONE | 1 |
| DEFERRED | 0 |
| REJECTED | 0 |
| **Total** | **8** |

**Cycle:** 1 · **COLLEEN scan:** 2026-05-26 · **Amethyst exec start:** 2026-05-26

---

## 🟡 IN PROGRESS

### OPP-001 · ADOPT · P-05 Tri-Phase CI Gate (Branch Protection)

```
Layer:        .github / GitHub repo settings
Detected by:  COLLEEN (Cycle 1 — S041)
Mode:         ADOPT — P-05 spec requires branch protection as hard gate
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=✅  → PASS
Status:       IN_PROGRESS
```

**COLLEEN audit note:**
CI workflow (`pptl-ci.yml`) is live and green but branch protection rule
has not been activated. P-05 is only partially implemented without it.
The `pptl pytest — governance` check is advisory, not a merge blocker.
This is the single highest-leverage action in the entire backlog — zero
code required, 5-minute manual action, immediately hardens all future PRs.

**Amethyst implementation plan:**
Manual action only (cannot be done via API without admin token):
1. GitHub → DGAF-Framework → Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable: “Require status checks to pass before merging”
4. Required check: `pptl pytest — governance`
5. Enable: “Require branches to be up to date before merging”

**Blocking:** OPP-003 (CI gate must be hard before altering contract count)

---

## 🟠 PENDING

### OPP-002 · CUSTOMIZE · P-04 Parametrized Corpus (Obfuscation Expansion)

```
Layer:        pptl/rag_verifier.py + pptl/tests/test_orchestrator.py
Detected by:  COLLEEN (Cycle 1 — S041)
Mode:         CUSTOMIZE — P-04 in place; corpus needs obfuscation class expansion
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=✅  → PASS
Status:       PENDING
```

**COLLEEN audit note:**
Current `BYPASS_SIGNALS` covers plaintext and mixed-case variants. Two
unaddressed obfuscation classes identified:
- **Unicode homoglyphs** (e.g., ’ignore’ via Cyrillic ‘і’ replacing Latin ‘i’)
- **Base64-encoded instructions** (e.g., `aWdub3JlIGFsbCBwcmV2aW91cyBpbnN0cnVjdGlvbnM=`)
Both bypass Gate 1 case-insensitive scan in current implementation.
P-04 auto-expansion means adding signals = automatic test suite expansion.

**Amethyst implementation plan:**
- Add 6 homoglyph variants to `BYPASS_SIGNALS` in `rag_verifier.py`
- Add 4 base64-encoded bypass strings to `BYPASS_SIGNALS`
- Add `_normalize_input()` helper to `orchestrator.py` Gate 1 scan
  (decode base64 + normalize unicode before substring match)
- Zero test-code changes — parametrize auto-expands

**Estimated scope:** 1 commit, ~40 lines

---

### OPP-003 · ALTER · P-03 Governance Contract Test (Variable Contract Count)

```
Layer:        pptl/tests/test_orchestrator.py + docs/NDR_PATTERN_REGISTRY.md
Detected by:  COLLEEN (Cycle 1 — S041)
Mode:         ALTER — P-03 spec needs variable contract count documented per gate tier
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=✅  → PASS
Blocked by:   OPP-001 (branch protection must be hard before altering gate specs)
Status:       PENDING
```

**COLLEEN audit note:**
P-03 currently documents 4 contracts per gate. Gate 0 (AttestationGate,
Phase 5 roadmap) will require 6 contracts (adds: attestation token valid,
expiry not exceeded). Registry note added in P-03 spec (S041) but stub
test file `test_attestation_gate.py` not yet created.
Altering the spec without the stub means Gate 0 has no contract skeleton
for the next developer to fill in.

**Amethyst implementation plan:**
- Create `pptl/tests/test_attestation_gate.py` with 6-contract template
  (all tests marked `@pytest.mark.governance`, all skip with `pytest.skip`
  until Gate 0 is implemented)
- Update P-03 spec note with explicit per-gate contract count table

**Estimated scope:** 1 commit, ~60 lines

---

### OPP-004 · ADOPT · P-07 Session Graduation Gate (SESSION_ANCHOR seal)

```
Layer:        SESSION_ANCHOR.md, SWEEP_LOG.md, CROSS_REF.md
Detected by:  Amethyst (S040 close) — confirmed by COLLEEN
Mode:         ADOPT — P-07 Session Graduation Gate spec exactly covers this gap
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=✅  → PASS
Status:       PENDING
```

**COLLEEN audit note:**
SESSION_ANCHOR.md is sealed at S038. Sessions S039, S040, S041 are
unrecorded. SWEEP_LOG.md not checked — likely same. CROSS_REF.md v3.3
pre-dates pptl/ harness, docs/NDR_PATTERN_REGISTRY.md, and CI workflow.
This is a P-07 Session Graduation Gate failure: session is not sealed
until SESSION_ANCHOR + SWEEP_LOG + CROSS_REF are all updated.
Three sessions of work are currently undocumented in the state machine.

**Amethyst implementation plan:**
- Update SESSION_ANCHOR.md: S039 → S041 entries with commit SHAs
- Update SWEEP_LOG.md: S040 + S041 entries
- Update CROSS_REF.md: add pptl/, docs/NDR_PATTERN_REGISTRY.md,
  .github/workflows/pptl-ci.yml, CO_ORCH_QUEUE.md

**Estimated scope:** 1 commit, ~120 lines across 3 files

---

### OPP-005 · ADOPT · P-01 Fan-Out Sink (N8nHeraldSink __init__.py export gap)

```
Layer:        pptl/__init__.py
Detected by:  Amethyst (S040/S041 coherence sweep)
Mode:         ADOPT — P-01 fan-out sink must be accessible from package root
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=✅  → PASS
Status:       PENDING
```

**COLLEEN audit note:**
`N8nHeraldSink` is implemented in `pptl/n8n_herald_sink.py` (S040) but
not exported from `pptl/__init__.py`. Users must import directly from
the submodule path. Breaks the package contract: all production sinks
should be importable from `pptl` directly per the Quick Start doc.
Low-risk, 1-line fix, but a public API gap.

**Amethyst implementation plan:**
- Read `pptl/__init__.py` → add `from pptl.n8n_herald_sink import N8nHeraldSink`
- Add `N8nHeraldSink` to `__all__` if present

**Estimated scope:** 1-2 lines

---

### OPP-006 · ALTER · P-08 Triad Taxonomy (Co-Orchestration Sweep Triad — ENSEMBLE_ROSTER Triumvirate entry)

```
Layer:        ENSEMBLE_ROSTER.md, CROSS_REF.md
Detected by:  COLLEEN (Cycle 1 — S041)
Mode:         ALTER — Triumvirate formation registered but not linked from CROSS_REF
1-1-1-1:      fit=✅  risk=┅  effort=✅  priority=┅  → PASS (marginal)
Status:       PENDING
```

**COLLEEN audit note:**
Triumvirate formation is defined in ENSEMBLE_ROSTER.md and P-08 (S041).
However CROSS_REF.md v3.3 does not reference either the NDR registry
or the PDMAL Triumvirate formation. Any agent navigating the ecosystem
from CROSS_REF cannot discover P-08 or the Triumvirate tier. Low effort;
bundles cleanly with OPP-004 (CROSS_REF update).

**Amethyst implementation plan:**
- Bundle into OPP-004 commit: add NDR_PATTERN_REGISTRY.md and
  ENSEMBLE_ROSTER.md Triumvirate section to CROSS_REF index.

**Estimated scope:** Bundled with OPP-004, no separate commit needed

---

### OPP-007 · COMPOSE · NEW: P-09 Triumvirate Mandate Schema

```
Layer:        docs/, pptl/ (new: triumvirate_mandate.py)
Detected by:  COLLEEN (Cycle 1 — S041 — gap from P-08 registration)
Mode:         COMPOSE — P-08 defines Triumvirate governance contracts but
              no machine-readable mandate schema exists yet
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=┅  → PASS
Status:       PENDING
```

**COLLEEN audit note:**
P-08 specifies 5 Triumvirate governance contracts in prose. A machine-
readable `TriumvirateMandateSchema` would: (a) make mandate issuance
audit-traceable via HeraldAgent, (b) enforce MECE prefect domain split
at creation time, (c) provide the CO_ORCH_QUEUE with a mandate object
for Cycle 2+ Triumvirate-governed sweeps.
Proposing as P-09 COMPOSE entry.

**Amethyst implementation plan:**
- Design `TriumvirateMandate` + `PrefectDomain` dataclasses
- Validate MECE on construction (domain sets must not overlap, must cover all agents)
- Emit mandate creation/sign-off events via HeraldAgent
- Register as P-09 in NDR_PATTERN_REGISTRY.md

**Estimated scope:** 1 commit, ~120 lines

---

### OPP-008 · COMPOSE · NEW: P-10 Session Graduation Check Script

```
Layer:        scripts/session_graduation_check.py
Detected by:  Amethyst (S040) + COLLEEN confirmed (Cycle 1)
Mode:         COMPOSE — P-07 Session Graduation Gate defined in prose;
              no automated checker exists
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=┅  → PASS
Status:       PENDING
```

**COLLEEN audit note:**
Session graduation currently requires manual verification of 4 conditions
(hypothesis verdicts, SESSION_ANCHOR+SWEEP_LOG updated, CROSS_REF indexed,
CI green). An automated script would: (a) read SESSION_ANCHOR to detect
unsealed sessions, (b) check CROSS_REF for missing paths, (c) query CI
status via GitHub API, (d) output a pass/fail graduation report.
This is a COMPOSE because no covering NDR pattern exists for automated
session state validation.

**Amethyst implementation plan:**
- `scripts/session_graduation_check.py`
- 4 checks: anchor sealed?, CROSS_REF complete?, CI green?, open BLGs?
- Output: `GRADUATION_REPORT.md` with pass/fail per check + action items
- Register as P-10 in NDR_PATTERN_REGISTRY.md

**Estimated scope:** 1 commit, ~150 lines

---

## ✅ DONE

### OPP-000 · COMPOSE · NEW: P-07 + P-08 (Triad Taxonomy + Sweep Loop)

```
Layer:        docs/NDR_PATTERN_REGISTRY.md, ENSEMBLE_ROSTER.md
Detected by:  Amethyst (S041 design session)
Mode:         COMPOSE — no pattern covered dual-agent persistent sweep or triad taxonomy
1-1-1-1:      fit=✅  risk=✅  effort=✅  priority=✅  → PASS
Status:       DONE
Commit:       3b0295e7bf1deb75a7816a6e402307f765abb8b9
Session done: S041
```

**Disposition:** P-07 (Dual-Agent Persistent Sweep Loop) and P-08 (Triad
Taxonomy: Consensus / Conducted / Triumvirate) designed, spec’d, and
registered in NDR_PATTERN_REGISTRY.md v1.1. ENSEMBLE_ROSTER.md updated
with Triumvirate tier, PDMAL Triumvirate formation, and all triad types.
CO_ORCH_QUEUE.md (this file) created as P-07 hand-off substrate.

---

## Cycle Log

| Cycle | COLLEEN scan | Amethyst exec | OPPs detected | OPPs closed |
|---|---|---|---|---|
| 1 | 2026-05-26 | 2026-05-26 | 8 (OPP-000 – OPP-008) | 1 (OPP-000) |

---

## Execution Order (Amethyst Cycle 1 Plan)

```
OPP-001  →  Manual: activate branch protection (5 min, unblocks OPP-003)
OPP-005  →  Commit: __init__.py N8nHeraldSink export (1-2 lines)
OPP-004  →  Commit: SESSION_ANCHOR + SWEEP_LOG + CROSS_REF seal (bundles OPP-006)
OPP-002  →  Commit: obfuscation corpus expansion + _normalize_input()
OPP-003  →  Commit: test_attestation_gate.py stub (after OPP-001 live)
OPP-007  →  Commit: TriumvirateMandate schema + P-09 registration
OPP-008  →  Commit: session_graduation_check.py + P-10 registration
```

Estimated: 6 commits + 1 manual action = Cycle 1 complete.

---

*P-07 Dual-Agent Persistent Sweep Loop · Cycle 1 · S041*
*COLLEEN: Librarian scan → Auditor score → Actualizer classify*
*Amethyst: NDR validate → execute → commit → mark DONE*
