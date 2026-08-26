---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-26
applies_to_sha: 15373831aa27aa37a2e21462a304f2b93b12216a
---

# DGAF/PDMAL — Forward Plan (post Control & Evidence Architecture Audit)

> **Purpose.** The sequenced, prioritized forward plan synthesized from the 4-node
> expert panel (2026-08-26). It turns the audit map (PR #102) into an executable
> roadmap with a single **freeze-admissibility gate**.
>
> **Panel execution note (verification discipline).** Nodes 2 (Evidence) and 4
> (Security) returned live-verified plans (read `origin/main @ 1537383`). Nodes 1
> (Governance) and 3 (Lifecycle) hit iteration caps because they explored a *stale
> legacy extracted copy* of the repo (`DGAF-Framework-LEGACY/...`, HEAD `3510b86`,
> 2026-08-21 sprint) instead of the live tree; their output was discarded. Their
> lanes (A3/A5/A6) were recovered from the audit and the two verified nodes. All
> predicate conditions below were re-confirmed against live `main` by the parent.
>
> **What this document does NOT claim:** that freeze is admissible, that pilot is
> authorized, or that N=0 is empirically established. It claims only that a plan
> exists. **N = 0. PRE-FREEZE. Pilot NOT GRANTED.** Merge ≠ freeze; execution ≠
> empirical validation.

## Principle (anti-bureaucracy, from the meta-review)
Extend existing authoritative artifacts. New artifacts strictly limited to:
1. The CI-emitted **Candidate Evidence Manifest** (A1) — machine output, not a doc.
2. **A4 External-Reader Reconstruction harness doc** — the one genuinely NEW doc the
   audit justifies (Layer-2 C was absent).
Everything else extends `CURRENT_STATE.md`, `FREEZE_MANIFEST.md`, `FREEZE_PREDICATES.yaml`,
`evidence/claims.json`, `validate_evidence_truth_layer.py`, `claim-hygiene.yml`, and
the `pdmal-pre-freeze-runner.yml` workflow. No 35-doc expansion.

---

## Phase 0 — Foundations (PRE-FREEZE-safe; CI/docs only; do now)

| id | title | serves | why | cost | blast_radius | dependency | deferral |
|----|-------|--------|-----|------|--------------|------------|----------|
| A1 | CI-emitted Candidate Evidence Manifest | Repository Truth (1), Provenance (2), Repro (3), Archival (P6) | Dims 1/2 are hand-typed today (`FREEZE_PREDICATES.yaml: current_main_sha: CURRENT_MAIN_AT_VERIFICATION` is an unresolved placeholder). One machine-emitted snapshot replaces four prose assertions. | low (~1 job + 1 script, no new doc) | CI-only, additive, **artifact-only, no commit** | none | now |
| A8 | Claim→artifact-SHA-256 citation | Incentive compat (M8), C2 | Nothing enforces a claim→artifact binding; `validate_evidence_truth_layer.py` checks `run_id`/`dataset`, not SHA. | low (schema + validator extend) | `evidence/` + truth-layer CI | none (foundation for A7) | now |
| A5 | Doc-lint later-state guard | M5 State-Transition Integrity | Docs can claim FROZEN/AUTHORIZED/EXECUTED while system is earlier; no gate enforces the vocabulary. (Legacy `FREEZE_MANIFEST.md` wrongly said FROZEN — live one is PRE-FREEZE, but the gap is real.) | low | doc-lint CI | none | now |
| A3 | Retained negative-state proof | M6 Negative-State Observability | N=0 / no-auth / no-freeze are **asserted in docs only**; `run_pilot.py` enforces non-occurrence but emits no retained proof of absence. | med (emit empty execution-attempt + authorization log) | CI-only | none | now |
| E8 | `.gitattributes` LF pin for hashed files | M4 byte-stability | CRLF injection observed during verification; file-content hashes must be platform-stable or reproducibility is illusory. | low | repo config | none | now |

**Phase 0 flips:** E1, E6, E7, M5, M6, C2.

---

## Phase 1 — Independence & Adversarial (after Phase 0 green)

| id | title | serves | why | cost | blast_radius | dependency | deferral |
|----|-------|--------|-----|------|--------------|------------|----------|
| A2 | Independent second canonicalization + hash | M4 monoculture, P9 | ≥5 modules all reduce to `hashlib.sha256` + stdlib `json`; the two canonicalizers *diverge* on a trailing newline (duplication without independence). Second path must differ on runtime (Node), serialization (CBOR), hash (SHA3-256/blake2b). | med (report-only first, then fail-closed) | CI | A1 | defer (post-Phase-0) |
| A7 | Standing adversarial claim-injection CI + blinding-key-exposure observability | C1, C3, C5 | `claim-hygiene.yml` is static word-lint only; never injects a known-false claim and confirms rejection. Real `PDMAL_BLINDING_KEY` exposure not independently observable in CI. | med | CI | A8 | defer |
| A4 | External-Reader Reconstruction harness (NEW doc) | C4, Layer-2 C | No mechanism lets a skeptic re-derive a claim from retained artifacts on blinded data alone. | med (1 doc + reuse existing validators, no new code) | docs + CI-readonly | none | defer |
| A6 | Append-only / quarantine lint for evidence | M7 Reversibility | Reversibility is a documented principle (agent-spec supersede; `CURRENT_STATE.md` rule 4) but not code-enforced. | low | doc-lint CI | none | defer |

**Phase 1 flips:** E3, E4, C1, C3, C4, C5, M7.

---

## Phase 2 — Human-decision gates (NOT doable by panel; block freeze)

| id | decision | why it blocks | current |
|----|----------|---------------|---------|
| E5 | Promote `pdmal-*` / `epistemic-*` gates to **required** status checks? | Today only `PPTL CI` is required (`strict: true`); all pdmal/epistemic gates are advisory, so "many green checks" don't gate merge. Freeze on advisory gates overstates assurance. | **NO** (verified live) |
| E2b | Hash-pin `requirements-epistemic.txt` (the toolchain that renders verdicts)? | Runtime is hash-pinned (#98); the verification toolchain is range-bounded (`pytest>=8,<10`). Asymmetry: the judge is looser than the judged. | **NO** |
| Pilot authorization | Separate governance transition (authority decision) | Even with all evidence gates green, pilot remains NOT GRANTED. | **NOT GRANTED** |

---

## Unified Freeze-Admissibility Predicate

Freeze is admissible **only if ALL hold AND are machine-emitted, not asserted**:

**Evidence path (Node 2):** E1 (repo truth CI-emitted) · E2 (runtime lockfile verified) · E3 (independent non-sha256/non-Python path) · E4 (one canonical serializer) · E6 (retained beyond run) · E7 (N=0/PRE-FREEZE/NOT_GRANTED machine-asserted) · E8 (byte-stable hashes).

**Security/incentive (Node 4):** C1 (adversarial injection rejects known-false) · C2 (every empirical claim cites artifact SHA) · C3 (blinding-key exposure observable) · C4 (external reconstruction demonstrated) · C5 (fail-closed on reward-gaming).

**Meta-governance (recovered lanes):** M5 (doc-gate on state vocabulary) · M6 (negative states observable) · M7 (reversibility enforced).

**Plus human gates:** E5 (gates required) · E2b (verification toolchain pinned) · Pilot authorization granted.

**Current status: NONE hold.** Freeze is inadmissible on *evidence* grounds
independently of pilot authorization. This is a second, separate reason from
`authorization: NOT GRANTED` — and it is the more actionable one, because every
E/C/M condition is reachable by PRE-FREEZE-safe CI/doc work (Phases 0–1).

---

## Recommended sequence (what to do next)

1. **Authorize Phase 0** (A1, A8, A5, A3, E8) — all PRE-FREEZE-safe, CI/doc only, no
   pilot, no freeze commit. This alone flips 6 of the ~14 admissibility conditions.
2. **Defer Phase 1** until Phase 0 is green in CI.
3. **You decide E5 / E2b** (required-check promotion + verification-toolchain pinning)
   — these are governance/policy calls, not engineering.
4. **Freeze remains blocked** until Phases 0–1 green AND pilot authorization granted.

## What this does NOT claim
No freeze created. P7 OPEN/pending authority; P8 OPEN/fail-closed. Pilot NOT
GRANTED. N=0 (asserted; M6 evidence not yet retained). Merge ≠ freeze; execution ≠
empirical validation. The corrected candidate basis (`83e1678`) requires
candidate-scoped re-verification before any closure claim. This is a plan, not a
result.
