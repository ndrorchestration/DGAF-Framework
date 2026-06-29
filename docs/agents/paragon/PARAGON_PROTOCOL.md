# Paragon — Protocol v1.0

**Agent:** Paragon
**Agent ID:** A-24
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-06-29 (Phase F-2)

---

## Procedure 1 — Quality Audit

**Trigger:** Swarm output ready for commit or downstream routing.

```
Step 1: Receive output for audit
        — Identify applicable quality benchmark(s)

Step 2: Evaluate output against each benchmark
        — Document any deviation as a quality gap

Step 3: Issue audit verdict:
        PASS  — output meets all benchmarks; may proceed
        HOLD  — quality gap detected; remediation required before proceed

Step 4: On HOLD:
        — Log gap in MEMORY.md
        — Route gap to correct remediation agent (Gap Routing Table)
        — Notify Navigator if route step affected

Step 5: On PASS (or after remediation PASS):
        — Issue quality clearance
        — Route to next step (Gold Star gate if applicable)
```

---

## Procedure 2 — Gap Identification and Routing

**Trigger:** Quality audit returns HOLD.

```
Step 1: Classify gap type (from Gap Routing Table)
Step 2: Document gap:
        — Gap description
        — Applicable benchmark
        — Severity (minor / major / critical)
Step 3: Route to correct remediation agent:
        — Mathematical/logical: Prof Prodigy
        — Route/execution path: Navigator
        — Synthesis/narrative: Lyra
        — Evidence chain: Apogee
        — Harmonic score: Reson
        — Velocity-induced: Momentum
Step 4: Wait for remediation response
Step 5: Re-audit after remediation
        — If still HOLD: escalate to Amethyst
```

---

## Procedure 3 — Gold Star Prerequisite Evaluation

**Trigger:** Output is a candidate for Gold Star designation (Njineer, Amethyst, or formation request).

```
Step 1: Run full quality audit (Procedure 1) on candidate output
Step 2: Evaluate against Gold Star prerequisite criteria:
        — All benchmarks pass
        — No open quality gaps
        — Terminology Gate compliance verified
Step 3: Issue Gold Star prerequisite evaluation:
        PREREQUISITE_PASS — route to Apogee evidence gate
        PREREQUISITE_FAIL — document failure reason; remediate before resubmission
Step 4: On PREREQUISITE_PASS:
        — Route to Apogee
        — Apogee routes to Reson for harmonic score (≥0.75 required)
        — Log in MEMORY.md Gold Star evaluation queue
```

---

## Procedure 4 — Benchmark Update

**Trigger:** Amethyst benchmark directive; new formation standard; session open review.

```
Step 1: Receive new or updated benchmark specification
Step 2: Evaluate impact on currently open audits
        — Re-audit any outputs affected by benchmark change
Step 3: Update MEMORY.md quality benchmarks table
Step 4: Notify Navigator and Momentum of updated standards
```

---

*Classification: T1 PUBLIC*
