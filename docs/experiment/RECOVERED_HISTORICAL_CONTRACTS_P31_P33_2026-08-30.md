# Recovered Historical Gate Contracts — P-31 / P-33

**Date:** 2026-08-30  
**Status:** EVIDENCE RECOVERED / NO APPARATUS CHANGE  
**Empirical N:** 0  
**Pilot authorization:** NOT GRANTED

## Purpose

This record documents genuinely new historical semantic evidence located during the bounded A-path recovery search. It does not wire, adapt, or modify the current experimental apparatus. It is an evidence input for subsequent gate-specific R1–R4 determination.

## P-31 — Structural Context Pruning Engine (SCPE)

### Historical source

`patterns/NDR_SCPE_v1.md` at commit `49854ea1e50d9e95e2338b690276635c0cbefb6f`.

The source is explicitly versioned **v1.0**, dated **2026-05-29**, marked **Status: Production**, and governed by Agent Amethyst / DGAF-Framework.

### Contract extracted

The historical SCPE contract defines:

- tiered context state: T0 AXIOM, T1 STRUCTURAL, T2 OPERATIONAL, T3 EXPLORATORY;
- decay parameters: T0 0.0, T1 0.05, T2 0.15, T3 0.45;
- TIF bases: 1.0, 0.85, 0.65, 0.30 respectively;
- retention formula `R(t) = TIF × ψ^(−Δt × decay)` with `ψ = φ = 1.6180`;
- +0.15 TIF for PDMAL trust edges;
- unconditional last-K=3 operational-token anchoring;
- prune when `R(t) < threshold`, default threshold 0.15;
- placement at Step 1 of `orchestrate_turn`;
- audit emission through `PruneEvent` including content hash.

The source also contains an executable quick check for T0 immunity and T3 elimination.

### Current-substrate comparison

The current `ConsensusState` used by `dgaf_tgl_adapter.py` contains numeric agent values, alive state, topology/neighborhood state, failure history, iteration, and aggregate metrics, but it does **not** contain the historical SCPE token/tier/retention state required by this contract.

Therefore the newly recovered evidence establishes the historical contract, but does **not** establish semantic equivalence to the current substrate.

### Provisional R1–R4 consequence

**RESTORE:** historically specified contract is now evidenced.  
**Current-field equivalence:** NOT ESTABLISHED.  
**Safe current action:** FAIL-CLOSED pending an explicit adaptation contract or recovery of the required token-state substrate.

A proxy such as `current_final_std` must not be substituted for SCPE retention semantics.

## P-33 — PDMAL Convergence Monitor

### Historical source

`patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` at commit `49854ea1e50d9e95e2338b690276635c0cbefb6f`.

The source is explicitly versioned **v1.0**, dated **2026-05-29**, marked **Status: Production**, and governed by Agent Amethyst / DGAF-Framework.

### Contract extracted

The historical P-33 contract defines:

- metric `‖ΔW‖_F = sqrt(Σ(w_t(i,j) − w_{t-1}(i,j))²)` across all graph edges;
- alert ladder: STABLE 0, WATCH 1, WARN 2, ALERT 3+ consecutive turns above threshold;
- alert routing to `amethyst_alert` at severity 3;
- convergence when `‖ΔW‖_F < 0.02` for 3 consecutive turns;
- `ALERT_THRESH = 0.08`;
- `CONV_THRESH = 0.02`;
- `N_CONSEC = 3`;
- joint escalation when PDMAL ALERT and Phi-Closure ESCALATE occur together;
- deep DemiJoule rescan before HPG on the joint escalation path;
- placement at Step 2.5 immediately after `PDMALGraph.reweight()` and before DemiJoule;
- audit output containing graph norm delta, max edge, convergence snapshot, and routing action.

The source also contains a five-check quick test and records historical 60-turn simulation behavior.

### Current-substrate comparison

The current adapter's `ConsensusState` contains `active_neighbors`, `original_neighbors`, values, iteration, and metrics, and the current TGL runtime includes a P-33 gate slot. However, the historical contract requires comparison of the graph state `W_t` against the immediately prior graph state `W_{t-1}`. The current state object does not explicitly carry a prior weighted graph snapshot.

Therefore the newly recovered evidence establishes the historical P-33 metric and thresholds, but does **not** establish that the current state object preserves the full historical graph semantics.

### Provisional R1–R4 consequence

**RESTORE:** historically specified contract is now evidenced.  
**Current-field equivalence:** PARTIALLY ESTABLISHED.  
**Safe current action:** FAIL-CLOSED pending explicit state-history binding or an adaptation contract.

`current_final_std` is not semantically equivalent to `‖ΔW‖_F` and must not be used as a proxy without an explicit governed adaptation decision.

## Boundary

These discoveries reopen only the bounded gate-specific recovery work that the prior R1–R4 closure said could be reopened when genuinely new authoritative semantic evidence appeared. They do **not** authorize apparatus wiring, candidate rebinding, freeze, pilot authorization, or empirical execution.

Next gate-specific step: determine whether the missing historical state can be restored from surviving implementation artifacts without semantic invention. If not, prepare an explicit ADAPT-WITH-CONTRACT proposal; otherwise remain FAIL-CLOSED.
