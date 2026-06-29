# DGAF Framework — Team Wiki

> **Last updated:** 2026-06-28 · S071 · Amethyst autonomous batch

---

## §1 · Overview

The DGAF (Dynamic Governance and Autonomous Framework) orchestrates multi-agent workflows under a formally governed pattern registry. All execution flows through NDR patterns enforced by Amethyst (host), DemiJoule (supervisor), and Apogee Lens (verifier).

## §2 · Agent Roster

| Agent | Role | Authority |
|-------|------|-----------|
| Amethyst | Host, coordinator, working-memory refresher | Space instruction tier |
| Apogee Lens | Final verifier for portfolio-grade output | Portfolio governance rules |
| DemiJoule | Runtime supervisor, ethics/safety | DGAF/PDMAL constraints |
| COLLEEN | Archive confirmation, Drive integration | Advisory |
| Ender / Njineer | Human ratification authority | Architect |

## §3 · Pattern Registry

Canonical source: `docs/ndr_patterns_unified.json`  
Human-readable: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md`  
Current watermark: **P-41** · Schema **v2.2** · Session **S071**

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

## §5 · Governance Rules

- All repos claiming DGAF governance must carry a `GOVERNANCE.md` with DGAF version, protocol anchor to `GOVERNANCE_CONSTITUTION.md`, φ = 1.61818, and applicable NDR patterns.
- Personal document firewall (NDR-133) is BLOCKING-ABSOLUTE. Architect override only. No resume/CV/audit files to GitHub.
- Stasis block (P-12–P-26, 133 patterns) migration window: 2026-06-13 → 2026-07-13.
- FLAG-01, FLAG-04, FLAG-05 await Njineer response before resolution.
- DriftWatch production deployment requires explicit push trigger from Architect.

## §6 · Session Log

| Session | Watermark | Key Additions |
|---------|-----------|---------------|
| S069 | P-36 | P-35, P-36, CRUCIBLE_CHARTER, STASIS_CANONICAL_SPEC |
| S066 | P-34 | P-34 Empirical-Threshold-Sweep |
| S042 | P-33 | P-31 SCPE, P-32 Phi-Closure, P-33 PDMAL |
| S071 | **P-41** | P-37 Saga, P-38 Circuit-Breaker, P-39 ACRFence, P-40 Atomix, P-41 HITL Queue · Schema v2.2 |

---

*Governed by DGAF · Amethyst host · φ = 1.61818*
