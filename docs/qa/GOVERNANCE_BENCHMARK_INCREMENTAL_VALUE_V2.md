# Governance Benchmark V2 — Incremental Value Engineering Candidate

**Status:** DESIGN + SAME-SYSTEM ENGINEERING CANDIDATE / NOT ADMITTED / NO SCIENTIFIC COLLECTION.

**Source baseline:** 0e09ae555136fb9d433c7294f445e0b656c7e705. Owning engineering controller: #1061. #1067 retains its separate frozen reproduction target. The historical nine-layer comparator remains unchanged.

## Why V2 exists

The 13 fixed cases, 112,200 bounded states, reusable configuration model, 11 matched recovery/composition cases and eight provenance mutations did not demonstrate unique protection. V2 must test real operating effort and failure-handling rather than inventing a weaker policy comparator or endlessly extending synthetic matrices.

## Engine and calibration

The initial engineering slice translates the 12 C3 policy clauses into Rego v1 and compares OPA, the original C3 code and DGAF on the SAME 13 fixed fixtures. OPA is a benchmark-only tool and receives the same inputs. This is calibration, not the operational experiment.

Pinned OPA engine: v1.21.2 Linux amd64 static, SHA-256 830ab11f61ffec760b5e19db0d7ad02bf037e13f5ef4d665faeaf17632177527. The runner refuses missing/mismatched versions, checks the binary digest, retains policy/fixture/rules hashes and labels every result same-system engineering. The existing C3 reference and DGAF functions are imported unmodified from repository source.

Run with verified OPA installed at /opt/opa/opa:

    python3.12 experiments/governance_benchmark/v2/verify_opa_c3.py --opa /opt/opa/opa
    DGAF_V2_OPA_BINARY=/opt/opa/opa python3.12 -m pytest tests/test_governance_benchmark_v2_opa.py -q

When OPA is absent, the optional OPA parity test SKIPS explicitly and cannot assert equivalence; the direct runner returns BLOCKED.

## Eight operational cases: not yet executed

See experiments/governance_benchmark/v2/scenario_catalog_v1.json for GOV2-01 through GOV2-08: authorized positive control, revocation race, conflicting evidence, ambiguous timeout, concurrent duplicate, fresh-admission recovery, composed protected egress, and custody mismatch.

Their scenario invariants are design proposals only: the independently defined executable oracle, event sequence, positive/negative ground truth, effect and cost instrumentation, and held-out collection protocol are NOT frozen. Do not calculate scientific N or call these operational passes.

## Next gates

1. Run exact-source T0 baseline with repository Python 3.12 dependency locks and first-failure preservation. Do not confuse this tiny V2 test lane with full repository QA.
2. Advance existing T1 #1347 gate correctness repair separately; do not bypass Draft/HOLD.
3. Independently specify the eight operational test inputs and oracles; match both arms on authorization information, state, receipts, idempotency, recovery, audit storage, and provider resources.
4. Measure unsafe completed effects, legitimate false blocks, reconciliation correctness, evidence completeness and actual human minutes/interventions. Never use CI runtime as a proxy for human effort.
5. Create only a signed, reviewable candidate via approved repository identity, with exact-head hosted CI and non-author review. No ordinary API-created unsigned commit may be silently counted as admitted.
6. Keep #1067 frozen review packet intact. External trials and real provider admission remain separately authorized.

**Claim ceiling:** SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED; STATE_OF_THE_ART=NOT_ESTABLISHED.
