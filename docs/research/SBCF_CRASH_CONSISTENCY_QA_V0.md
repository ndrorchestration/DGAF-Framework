# SBCF crash consistency and concurrency QA — 2026-10-09

Status: RESEARCH ONLY / FAIL-CLOSED / PRE-FREEZE. PR #1339; issue #1338.

## Experiment
Synthetic same-process concurrent duplicate admissions tested with four threads. A unique source/run/sequence was admitted once. An advanced witness rejected replay at the witness high-water mark. Invalid signatures did not advance the witness.

## Falsification
A fault-injection test simulates the evidence database committing sequence 2 while the witness remains at sequence 1. This produces inconsistent stores. The strict expected failure records a known crash-consistency defect; it MUST NOT count as a completed protection or as a real observed system crash.

## Next obligations
Define an atomic append/admit protocol or a conservative recovery rule that detects mismatched high-water values and locks down authorization pending reconciliation. Test process crash between every durable write, concurrent multiprocess writers, deleted/corrupt witness, rollback of both stores, and source identity compromise. Secure remote custody not established. No live enforcement, scientific inference, independent human review, or high assurance approval.
