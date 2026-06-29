# Zenith — Operational Protocol

**Agent:** Zenith (A-09)
**Classification:** T2 FRAMEWORK
**Version:** 1.0
**Last Updated:** 2026-06-29 (Phase 4)

---

## 1. Continuous Load Monitoring Procedure

**Trigger:** Ongoing — active throughout every formation session.

```
Step 1:  Poll europe-west1 node load (5 nodes)
         Frequency: per-session check at SESSION_OPEN + periodic during session

Step 2:  Compute load distribution
         Each node load as fraction of total capacity
         Symmetry check: any node >1/5 (20%) total capacity?
         YES → Section 2 (Symmetry Breach)
         NO  → log SYMMETRY_OK in SWEEP_LOG; continue monitoring

Step 3:  Check for silent compute debt
         Compare Zenith load report vs. DemiJoule per-session token spend
         Discrepancy detected? → Section 4 (DemiJoule Escalation)
```

---

## 2. Symmetry Breach Procedure

**Trigger:** Any node exceeds 1/5 of total capacity.

```
Step 1:  Identify breaching node and load delta

Step 2:  Attempt automatic rebalance
         — Redistribute load across remaining nodes to restore ≤1/5 per node
         SUCCESS → log SYMMETRY_RESTORED in SWEEP_LOG; continue
         FAILURE → proceed to Step 3

Step 3:  Node failure detected?
         YES → Section 3 (Node Failure Failover)
         NO (overload without failure) → proceed to Step 4

Step 4:  Request session pause from Amethyst
         Content: node ID, load delta, rebalance failure reason
         Amethyst decides: pause session or accept degraded symmetry
         Log: SYMMETRY_BREACH | Zenith | [node] | [load delta] | OPEN
```

---

## 3. Node Failure Failover Procedure

**Trigger:** Node failure breaks pentagonal symmetry (4-node asymmetric state).

```
Step 1:  Trigger GCP failover for failed node
         (Automatic — no vote required)

Step 2:  Notify Amethyst immediately
         Content: failed node ID, failover status, estimated restoration time
         Amethyst decides: pause session or continue on 4-node asymmetric load

Step 3:  Log in SWEEP_LOG via Herald
         Entry: NODE_FAILURE | Zenith | [node ID] | FAILOVER_TRIGGERED | OPEN

Step 4:  Monitor failover progress
         RESTORED → symmetry check (Section 1); notify Amethyst; SWEEP_LOG RESOLVED
         FAILED   → escalate to Njineer; session pause mandatory
```

---

## 4. DemiJoule Escalation Procedure

**Trigger:** Token/compute spike detected OR silent compute debt discrepancy found.

```
Step 1:  Compose escalation
         Content: Zenith load report + DemiJoule token spend delta + discrepancy description

Step 2:  Send to DemiJoule
         DemiJoule cross-checks per-session token spend vs. Zenith load report

Step 3:  Log in SWEEP_LOG
         Entry: COMPUTE_ESCALATION | Zenith → DemiJoule | [discrepancy] | OPEN

Step 4:  Await DemiJoule response
         RESOLVED → SWEEP_LOG updated to RESOLVED
         UNRESOLVED → escalate to Amethyst
```

---

*Classification: T2 FRAMEWORK*
