# AOSS v0.6 Stage A — Freshness, Eligibility, Repetition, and Ground Truth

**Controller:** #810  
**Status:** FROZEN PRE-DATA CONTRACT / NO OUTCOMES  
**Authority:** NONE

This tranche closes four Stage-A readiness predicates without defining the still-missing AOSS decision policy or collecting any external outcomes.

## Freshness / calibration

Freshness is intentionally a **same-host relative-time property**, not a claim that either machine clock is externally calibrated.

For a real Stage-A episode:

- ACP source generation and AOSS observer ingestion must use the same host clock domain;
- the final source event may be at most **30 seconds old** at observer ingestion;
- an event may be at most **2 seconds in the future** relative to observer ingestion;
- non-injection episodes may not move backward in source wall time;
- a source/observer cross-host setup is invalid for this Stage-A contract.

This does not establish NTP accuracy, UTC traceability, or an externally calibrated clock.

## Episode eligibility

All 16 preregistered episode classes remain mandatory.

The primary divergence denominator uses 14 canonical normalized classes. The two structural rejection controls — `malformed_manifest` and `mismatched_run_id` — are excluded from that denominator prospectively and remain mandatory safety/falsification controls.

No episode may be excluded because its decision or result is inconvenient.

## Repetition

Stage A uses **one canonical source episode per class**. Each accepted episode is replayed from the exact same bytes **five times** to test deterministic reconstruction.

Those replays are not independent observations and do not increase the primary denominator or scientific N. There is no random seed because this Stage-A corpus is not stochastic sampling.

## Ground truth

The machine-readable ground-truth registry freezes the injected/source condition, adapter acceptance expectation, terminal-event expectation, and primary-endpoint eligibility for every required class.

Those labels are source/fixture truth only. They do not define whether an AOSS decision is correct; that remains the responsibility of the separately frozen prospective decision policy and analysis plan.

## Non-effects

This tranche does not authorize outcome collection, establish external validation, establish AOSS superiority, change DGAF/PDMAL scientific state, or increment scientific N.
