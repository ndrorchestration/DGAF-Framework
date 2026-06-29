# NDR Gate Priority Schema — P-36 v1

> **S071 Amendment · 2026-06-28** — BLOCKING list extended to include P-37, P-38, P-39, P-40.

## BLOCKING Patterns (execution halts until satisfied)

| ID | Name | Layer | Added |
|----|------|-------|-------|
| P-35 | Procluding Premise Gate | 0 | S069 |
| P-03 | Governance Contract Test | 2 | S040 |
| P-11 | 11Q Attestation Scoring | 5 | S033 |
| P-30 | Apogee-Attestation-Gate | 5 | S035 |
| P-27 | Adaptive-Weighting-with-Confidence-Gates | 7 | S033 |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | 7 | S033 |
| P-29 | Sentinel-Annotated Risk Pass | 8 | S034 |
| P-32 | Fibonacci Phi-Closure Gate | 9 | S042 |
| P-01 | Fan-Out Trace Sink w/ Dead-Letter | 1 | S040 |
| P-37 | Saga Boundary Declaration | 10 | **S071** |
| P-38 | Circuit-Breaker Gate | 10 | **S071** |
| P-39 | ACRFence — Atomic Checkpoint-Resume Fence | 10 | **S071** |
| P-40 | Atomix — Tool-Call Transaction Boundary | 11 | **S071** |

## ADVISORY Patterns

All other registered patterns. See `ndr_patterns_unified.json` for full list.

## Special Classes

- `BLOCKING-ABSOLUTE` — NDR-133 Personal Document Firewall. Architect override only.
- `DEGRADED-MODE-SKIPPABLE` — P-12–P-26 Stasis Block. Skippable only in degraded mode.
- `ADVISORY` with CI override — P-05 Tri-Phase CI Gate is BLOCKING in CI context.

## Evaluation Order

Layer 0 → 0.5 → 1 → 2 → 3 → ... → 11. Within the same layer, BLOCKING patterns evaluate before ADVISORY.

---

*Watermark: P-41 · Schema v2.2 · Session S071 · Amethyst*
