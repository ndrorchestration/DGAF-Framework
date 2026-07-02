# DGAF Framework — Team Wiki

> **Last updated:** 2026-07-02 · Post-S077 · Amethyst governance sweep

---

## §1 · Overview

The DGAF (Dynamic Governance Agentic Framework) is the **layer-0 governance architecture** for the ndrorchestration ecosystem, rooted at `~/DGAF-Framework`. It orchestrates multi-agent workflows under a formally governed pattern registry. All execution flows through NDR patterns enforced by Amethyst (host), DemiJoule (supervisor), and Apogee Lens (verifier).

> **Nomenclature canon** (locked 2026-07-02 in `SESSION_ANCHOR.md`):  
> • `NDR-HDFS` = NDR Hierarchical Dynamic Formation System (formerly FLAG-01) — the structural layer governing agent hierarchy and formation composition  
> • `qualitative` = interpretive/rubric-based evaluation mode (formerly FLAG-02)  
> • DGAF = layer-0 governance architecture — not a framework addon; the root control plane

---

## §2 · Agent Roster — Amethyst-Lattice v3.1 (11 canonical agents)

> Authoritative source: `ENSEMBLE_ROSTER.md` (Post-S077, 2026-06-29)  
> Agent count: **11 canonical** (6 with full detail sheets + 5 operational components)

| Agent | Layer | Role | Status |
|---|---|---|---|
| **Amethyst** | L5 | Host, meta-orchestrator, working-memory refresher, tribunal | ✅ Active |
| **COLLEEN** | L5 | Institutional anchor, 1-1-1-1 Alignment Gate, steward | ✅ Active |
| **Apogee Lens** | L4 | QA orchestrator, NIST AI RMF compliance, P-30 attestation authority | ✅ On-call |
| **DemiJoule** | L4 | Runtime supervisor, ethics/safety, AXIS enforcement | ✅ On-call |
| **Herald** | L3 | Explorer / Synthesizer | 🔴 Blocked (`VITE_GEMINI_API_KEY` — S-01) |
| **Professor Prodigy** | L3 | Executor / Phi-calculus | 🟡 KB specified, implementation pending |
| **Agent Sentinel** | L3 | Safety/veto gate, 11Q gates 9–11 | ⬜ Card pending |
| **KAPPA v3.6** | L3 | Confidence-gated dynamic weight router | ⬜ Component card in `KAPPA/` |
| **NormativeConstraint v1.0** | L3 | P-10 deontic/ethical cognition layer | ⬜ Component card exists |
| **Reson #1** | L3 | Schizophonic Studio signal chain — #1 | ⬜ Studio trio |
| **Echolette #2 / Lyra #3** | L3 | Schizophonic Studio signal chain — #2/#3 | ⬜ Studio trio |
| **Ender / Njineer** | — | Human ratification authority, Architect | ✅ Active |

---

## §3 · Pattern Registry

Canonical source: `docs/ndr_patterns_unified.json`  
Human-readable: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
Current watermark: **P-42** · Schema **v2.2** · Session **Post-S077**

Newest pattern: **P-42 AHG** (Acoustic Harmonic Gate) — filed 2026-06-29

---

## §4 · Resilience Stack

### §4.1 · Core Gates (Layer 0–5)

- **P-35** Procluding Premise Gate — blocks execution if premise is unsound
- **P-36** Gate Priority Schema — defines evaluation order for all gates
- **P-30** Apogee-Attestation-Gate — final quality gate before portfolio output
- **P-11** 11Q Attestation Scoring — quantitative quality scoring

### §4.2 · Confidence & Routing (Layer 7–8)

- **P-27** Adaptive-Weighting-with-Confidence-Gates — routes by confidence threshold (STRONG: 0.22, BLENDED: 0.18)
- **P-28** Pipeline-Composition-with-Confidence-Gated-Routing — composes pipelines conditionally
- **P-29** Sentinel-Annotated Risk Pass — annotates risk at 3 hook points before irreversible actions

### §4.3 · Convergence & Compression (Layer 9)

- **P-31** SCPE — Structural Context Pruning Engine (58.3% compression, T0-immune)
- **P-32** Fibonacci Phi-Closure Gate — φ-checkpoints at Fib[13, 21, 34, 55]
- **P-33** PDMAL Convergence Monitor — joint escalation with P-32

### §4.4 · Distributed Resilience Stack (Layer 10–11) · *Added S071*

Five patterns form an interlocking contract for durable, fault-tolerant multi-step execution:

| Pattern | Layer | Class | Role |
|---------|-------|-------|------|
| **P-37** Saga Boundary Declaration | 10 | ADVISORY | Declares step sequence, compensators, stochastic/deterministic split. Must precede P-38. |
| **P-38** Circuit-Breaker Gate | 10 | BLOCKING | Trips on ≥3 failures → suspends execution, fires P-29 + P-37 compensators. States: CLOSED / OPEN / HALF-OPEN (30s probe). |
| **P-39** ACRFence | 10 | BLOCKING | Atomically writes SHA-256 checkpoint before each tool call. Next call blocked until ACK. Restarts resume from last ACK'd checkpoint. |
| **P-40** Atomix | 11 | BLOCKING | BEGIN → EXECUTE → COMMIT \| ROLLBACK per tool call. Idempotency key required for all writes. Compensator sourced from P-37. |
| **P-41** HITL Durable Approval Queue | 11 | ADVISORY | Holds irreversible approvals across restarts. TIMED_OUT → P-38. No irreversible action fires without APPROVED state. |

**Interlock sequence:** P-37 choreographs the saga → P-38 isolates failures → P-39 makes checkpoints durable → P-40 makes individual calls transactional → P-41 gates all irreversible human decisions.

### §4.5 · Acoustic Harmonic Gate (Layer 12) · *Added Post-S077*

- **P-42** AHG — Acoustic Harmonic Gate. Phi-harmonic resonance verification before synthesis output. Newest canonical pattern.

---

## §5 · Governance Rules

- All repos claiming DGAF governance must carry a `GOVERNANCE.md` with DGAF version, protocol anchor to `GOVERNANCE_CONSTITUTION.md`, φ = 1.61818, and applicable NDR patterns.
- Personal document firewall (NDR-133) is BLOCKING-ABSOLUTE. Architect override only. No resume/CV/audit files to GitHub.
- Stasis block (P-12–P-26, 133 patterns) migration window: 2026-06-13 → **2026-07-13** ⚠️ EXPIRING.
- NDR-HDFS (formerly FLAG-01) and qualitative evaluation (formerly FLAG-02) are canonical — see `SESSION_ANCHOR.md` nomenclature canon.
- FLAG-05 (AXIS pattern scope) awaits Njineer content decision (S-03 in DEFERRED_ITEMS.md).
- DriftWatch production deployment requires explicit push trigger from Architect.

---

## §6 · Session Log

| Session | Watermark | Key Additions |
|---------|-----------|---------------|
| S042 | P-33 | P-31 SCPE, P-32 Phi-Closure, P-33 PDMAL |
| S066 | P-34 | P-34 Empirical-Threshold-Sweep |
| S069 | P-36 | P-35, P-36, CRUCIBLE_CHARTER, STASIS_CANONICAL_SPEC |
| S071 | P-41 | P-37 Saga, P-38 Circuit-Breaker, P-39 ACRFence, P-40 Atomix, P-41 HITL Queue · Schema v2.2 |
| Post-S077 | **P-42** | AHG (P-42), ENSEMBLE_ROSTER v3.1, agent count locked at 11 canonical, ndr_patterns_unified.json v2.2 |
| 2026-07-02 | — | Nomenclature canon locked (NDR-HDFS, qualitative, DGAF layer-0); SESSION_ANCHOR.md updated; DEFERRED_ITEMS.md patched |

---

*Governed by DGAF · Amethyst host · φ = 1.61818*  
*Updated 2026-07-02 by Agent Amethyst × COLLEEN — synced to Post-S077, P-42 watermark, 11-agent roster*
