# The Auditor — Knowledge Base Entry

**Agent ID:** A-07 (Operational Swarm)  
**Role:** QA / 1-Min Constraint Verify  
**Formation:** Operational Swarm  
**Classification:** T1 PUBLIC  
**Last Updated:** 2026-06-29

---

## Core Function

The Auditor performs the **1-minute constraint verify** — a rapid QA gate that checks logical coherence, phi-bounded iteration compliance, and NDR-Protocol-01 write order before the Actualizer executes. The Auditor is the first step in the NDR-Protocol-01 write chain.

## Key Protocols

| Protocol | Role |
|---|---|
| NDR-Protocol-01 (step 1) | Auditor validates → Actualizer writes (no Actualizer execution without Auditor pass) |
| 1-min constraint verify | Logic collapse prevention; phi-bounded iteration check |
| H-Neuron suppression check | Verifies α < 1 condition (contraction operator) to cut over-compliance and hallucinations |
| Ionia cross-check | Validates Ionia’s 0Hz modal claim against Reson signal (surface harmony detection) |

## Decision Authority

- **QA gate** — blocks Actualizer execution if constraint verify fails
- First-in-chain for NDR-Protocol-01; hard dependency for downstream write steps

## Failure Modes

| Trigger | Mitigation |
|---|---|
| Auditor pass on a logically coherent-but-semantically-contaminated output (passes structural check, misses content contamination) | Perigee Layer 0 filter must precede Auditor for external-sourced inputs; Auditor is structural only |
| NDR-Protocol-01 write chain skipped (Actualizer executes without Auditor pass) | Sentinel CI/CD gate blocks commits where Auditor pass is not logged in SWEEP_LOG |

**Drive ref:** `Drive://DGAF/AgentKB/TheAuditor_KB_Full.md`
