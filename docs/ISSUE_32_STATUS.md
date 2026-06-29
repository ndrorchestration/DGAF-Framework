# Issue #32 — Status Tracker

**Issue:** Nemotron 3 Ultra Parametric Measurement Suite + AHG Eval Integration 
**Pattern bundle:** high_risk_state_mutation 
**Session:** S077 | Last updated: 2026-06-29 
**Orchestration:** Amethyst × COLLEEN

---

## Overall Status: 🟡 CLOSE-ELIGIBLE PENDING LIVE EVAL RUN

All architecture, scaffolding, eval harness, and Apogee Lens review are complete.
Issue #32 may be closed once the live eval run passes (all 8 tasks) and
`apogee_lens_approved=True` is set in the COLLEEN episode record.

---

## Deliverable Checklist

### Core Infrastructure

| Deliverable | File | Status | Commit |
|---|---|---|---|
| AHG Architecture doc | `AHG_ARCHITECTURE.md` | ✅ v1.2 | Prior |
| P-42 pattern doc | `patterns/P-42_AHG.md` | ✅ v1.2 | Prior |
| AHG Conductor | `components/ahg_conductor.py` | ✅ v1.3 | `5a3cce9` |
| AHG Sidecar | `components/ahg_sidecar.py` | ✅ v1.5 | This commit |
| Herald Trace Sink | `components/ahg_herald_trace.py` | ✅ v1.5 | This commit |
| Heartbeat Schema | `schemas/ahg_heartbeat.json` | ✅ v1.0 | `5a3cce9` |
| Conductor Tests | `tests/test_ahg_conductor.py` | ✅ 14 TCs | `5a3cce9` |

### Eval Suite

| Task | Priority | Target | Stub | Live |
|---|---|---|---|---|
| contraction_proof_fidelity | 1 | ≥ 98% spectral pass | ✅ | 🔴 Pending |
| governance_schema_conformance | 2 | ≥ 99% valid | ✅ | 🔴 Pending |
| role_boundary_coherence | 3 | ≥ 95% correct | ✅ | 🔴 Pending |
| audit_hallucination_rate | 4 | ≥ 78.7% (BF16) | ✅ | 🔴 Pending |
| taubench_banking_mitigation | 5 | ≥ 80% escalation | ✅ | 🔴 Pending |
| ahg_hallucination_reduction | 6 | ≥ 20% D_e reduction | ✅ | 🔴 Pending |
| ahg_recovery_turns | 7 | ≥ 25% turns reduction | ✅ | 🔴 Pending |
| ahg_entropy_recovery | 8 | ≥ 0.30 delta D_e | ✅ | 🔴 Pending |

### Governance

| Gate | Agent | Status |
|---|---|---|
| Apogee Lens review | Apogee | ✅ APPROVED (`docs/APOGEE_LENS_REVIEW_P42_v15.md`) |
| BF16/NVFP4 precision gate (Task 1) | DemiJoule | ✅ BF16 confirmed |
| Herald audit fixtures (Task 4) | Herald | 🟡 Pending live run |
| Few-shot primer validation (Task 5) | Sentinel | 🟡 Pending live run |
| vLLM expert-routing logs | DevOps | 🔴 Not yet confirmed |

---

## Close Conditions

Issue #32 is closeable when ALL of the following are true:

1. ✅ Apogee Lens review passed (`docs/APOGEE_LENS_REVIEW_P42_v15.md`)
2. 🔴 Live eval run: all 8 tasks pass with Nemotron 3 Ultra (BF16)
3. 🔴 `apogee_lens_approved=True` set in COLLEEN episode record
4. 🟡 Herald audit fixtures generated (Task 4 pre-condition)
5. 🟡 Sentinel few-shot primer confirmed (Task 5 pre-condition)

**CLI command to run live eval:**
```bash
python tests/dgaf_eval_suite.py \
  --precision BF16 \
  --session S077 \
  --few-shot \
  --output-dir logs/issue32
```

**AHG-only subset (Tasks 6-8):**
```bash
python tests/dgaf_eval_suite.py \
  --precision BF16 \
  --session S077 \
  --ahg-only \
  --output-dir logs/issue32
```

---

## Roadmap — Post-Issue #32

| Item | Target |
|---|---|
| MPHG weight optimizer | v2.0 |
| `flush_turn()` thread-safety lock | v2.0 |
| P-01 Herald HTTP endpoint provisioning | v1.6 (DevOps) |
| `apogee_lens_approved` auto-flip on passing live run | v1.6 |
| Phase-space 3D manifold (exploration/dissent/uncertainty) in conductor | v2.0 |
