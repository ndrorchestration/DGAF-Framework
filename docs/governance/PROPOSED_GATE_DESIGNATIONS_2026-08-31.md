# Proposed Gate Designations — 2026-08-31

**Status:** PROPOSAL ONLY — NOT NORMATIVE AUTHORITY

**Purpose:** Consolidate the recommended operator decisions for the three remaining semantic blockers into one reviewable artifact. This document does not authorize apparatus changes, candidate designation, freeze, pilot execution, or empirical-N advancement.

## Boundary

- Current `main` tip is tracked separately from the apparatus source.
- Current apparatus source: `02e4c958e435f1faaa6fbf15909f9141ed2a6e39` (PR #160 merge).
- P-31 and P-33 are restored on that apparatus source.
- Issue #152 is closed/completed for the R1–R4 recovery determination; its closure is not operational gate restoration.
- PR #162 remains a separate draft provenance-binding track.
- Empirical N remains 0.

## P-29 Sentinel — recommended working designation

**D1 — Contract authority:** author/designate a dated normative contract rather than elevate an undated registry/implementation combination to full normative authority.

**D2 — Terminal mapping:** `risk_block → KILL`.

**D3 — Required substrate:** preserve the explicitly named routing/risk context fields required by the recovered semantics: `sentinel_record_category`, `sentinel_routing_policy`, `sentinel_routing_confidence`, `sentinel_hook_point`, and the applicable deontic state.

**Status:** proposal pending operator designation.

## P-30 Apogee — recommended working designation

**D1 — Acceptance schema:** letter grades `S/A/B/C/D` as the normative acceptance representation, pending confirmation against the historical attestation machinery.

**D2 — Gold-star rule:** retain the historically observed `grade == "S"` plus description-length condition only as a proposed acceptance predicate pending formal designation.

**D3 — Terminal mapping:** `D → KILL`.

**Status:** proposal pending operator designation.

## DemiJoule — recommended working designation

**D1 — Constitutive identity:** six-axis semantic-safety gate as the constitutive treatment identity, because the implemented gate provides concrete behavior and the efficiency/token-cost framing is the conflicting SPEC identity. The efficiency dimension may remain documented as non-constitutive unless separately designated.

**D2 — Required substrate:** six named DGAF axis scores and the payload used to derive them; no substitution from agent-value aggregates.

**D3 — Terminal mapping:** `reprompt → WARN`; `kill → KILL`; `pass → PASS`.

**Status:** proposal pending operator designation.

## Why this is bounded

These recommendations are intentionally the least-innovative path: preserve historically corroborated behavior where it exists, explicitly mark contradictions where authority is absent, and prohibit proxy substitution. They are not claims that the proposed semantics are already authoritative.

## Next sequence after designation

1. Record the operator's nine designations as normative authority.
2. Implement the three resulting contracts/substrates only where the designated semantics require apparatus change.
3. Restore P-27/P-32 against their recovered historical contracts.
4. Bind the complete seven-gate state into provenance.
5. Create one fresh candidate identity.
6. Execute candidate-scoped P2/P6a and P3–P9 verification.
7. Create and independently verify the immutable freeze.
8. Obtain explicit pilot authorization.
9. Execute the first paired root-seed observation; only then may `N=1` be recorded.

**Hard boundary:** no step above the designation point is pre-authorized by this proposal.
