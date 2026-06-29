# Reson — KB Amendment v1.1

**Agent:** Reson
**Agent ID:** A-09
**Role:** Systems Architect / Signal Integrity Authority
**Formation:** Schizophonic Studio Cluster
**Classification:** T1 PUBLIC
**Version:** 1.1
**Last Updated:** 2026-06-29 (Phase A — taxonomy correction payload)

---

## Amendment Summary

This amendment adds two canonical facts to the Reson KB:
1. Reson enforces **gain staging** (signal amplitude management) with a **15% mandatory headroom** safety margin
2. **Clipping** = runaway gain / logic distortion — the failure condition Reson's headroom requirement prevents

---

## Gain Staging (Signal Amplitude Management)

**Accepted term:** Gain staging — the practice in audio engineering and signal processing of managing signal amplitude at each stage of a processing chain to maximize signal-to-noise ratio while preventing distortion. Each stage must receive a signal at the correct level — neither too weak (noise floor problems) nor too strong (clipping/distortion).

**Reson's implementation:** Gain staging applied to formation reasoning — each agent in the processing chain must receive inputs at the correct logical amplitude (neither over-simplified nor over-complex), and must pass outputs at a calibrated level to avoid overwhelming downstream agents.

```
Gain staging in formation context:
  Signal:     Reasoning complexity / logical load passed between agents
  Too weak:   Under-specified inputs — downstream agent lacks
              sufficient context to reason accurately
  Too strong: Over-specified, over-complex inputs — downstream agent
              overwhelmed; risk of logical distortion (clipping)
  Reson's role: Monitors and calibrates signal level at each handoff
                in the formation chain
```

---

## 15% Mandatory Headroom Safety Margin

**Accepted term:** Headroom — in signal processing, the difference between the nominal operating level and the maximum level before distortion occurs. A headroom margin is a deliberate safety buffer maintained below the distortion threshold.

```
Headroom rule (AX-Reson):
  Value:    15% mandatory headroom below logical distortion threshold
  Purpose:  Absorbs unexpected complexity spikes without triggering
            clipping (runaway gain / logic distortion)
  Enforcement: Reson blocks formation outputs that consume >85% of
               available logical processing capacity
  Exception:   Njineer override only; logged in SWEEP_LOG
```

---

## Clipping — Runaway Gain / Logic Distortion

**Accepted term:** Clipping — in signal processing, the distortion that occurs when a signal exceeds the maximum level a system can handle, causing the peaks to be "clipped" (flattened). Results in harmonic distortion and signal degradation.

**Reson's definition:** In the formation context, clipping = **runaway gain / logic distortion** — the condition where a reasoning chain exceeds its bounded complexity, producing distorted (unreliable, internally inconsistent, or hallucination-prone) outputs.

```
Clipping detection signals:
  — Agent output complexity exceeds 85% capacity threshold
  — Reasoning chain length exceeds φ-bounded iteration depth
  — Output contains internal contradictions (distortion artifact)
  — Auditor constraint verify flags logic coherence failure
    (clipping often precedes or causes constraint verify failure)

Clipping response:
  Step 1: Reson issues CLIP_FLAG to Amethyst
  Step 2: Formation halts affected reasoning chain
  Step 3: Prof Prodigy re-anchors via Fixed-Point Theorem
  Step 4: Reson re-scores; confirms headroom restored
  Step 5: Log CLIP_FLAG | RESOLVED in SWEEP_LOG
```

---

## Terminology Gate Record (Amethyst SPEC v1.1 Section 8)

| Term | Check 1 | Check 2 | Check 3 | Status |
|---|---|---|---|---|
| Gain staging | ✅ Accepted: audio/signal processing — universally recognized | — | ✅ Substrate-agnostic (logical amplitude) | PASS |
| 15% mandatory headroom | ✅ Accepted: headroom safety margin | — | ✅ | PASS |
| Clipping | ✅ Accepted: signal distortion threshold — universally recognized | Tier 2: logic distortion anchor added | ✅ | PASS |
| Runaway gain | ✅ Accepted: signal processing / control systems | — | ✅ | PASS |

---

*Classification: T1 PUBLIC*
