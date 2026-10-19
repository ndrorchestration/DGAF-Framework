# Containment Admission Implementation Plan

> For agentic workers: use executing-plans, native execution, with one final fresh code review.

Goal: integrate bounded assessment, exact-byte observation intake and a Tektite synthetic projection.
Spec: `docs/superpowers/specs/2026-10-11-containment-admission-design.md`.
Architecture: existing assessment plus one fail-closed integrity wrapper; deterministic fixed-time projection and read-only static surface.
Tech stack: Python standard library, browser JavaScript, existing Next demo page.

## Global constraints

Synthetic snapshot only. Authority NONE. Fresh adjudication required. Execution false. N=0. No main merge, deployment or research-gate changes.

## Review focus

- Caller-supplied pin is not authenticated producer identity: keep authenticity NOT_ESTABLISHED.
- Parser ambiguities: reject duplicate keys, invalid encoding, non-finite numbers and oversized records.
- Fixed clock: label historical snapshot replay visibly; no current containment implication.
- Forged projection: reject authority elevation, inconsistent positive states and missing case coverage.
- Existing SBCF work: preserve unmerged branch and avoid importing its prototype trust claims.

## Task 1: admission and bound intake

- [x] Port the 26 existing tests and assessment to repository paths; run and preserve green result.
- [x] Write tests for `assess_bound_snapshot(contract, observation_bytes, *, expected_observation_digest, now) -> dict`: valid match returns EXPECTED_DIGEST_MATCH, source authenticity NOT_ESTABLISHED and no authority; missing/wrong pin or malformed raw records raise AssessmentInputError.
- [x] Run new tests RED, implement `scripts/dgaf_containment_observation.py`, run all containment tests GREEN.

## Task 2: retained projection and Tektite surface

- [x] Write failing tests for deterministic generator outputs and actual SC-01-to-PEP refusal.
- [x] Add separately pinned raw fixtures and `scripts/generate_tektite_containment.py`; output public JSON and HTML.
- [x] Add browser parser/renderer and tests: malformed or promoted records throw, five expected cases visible, failure state visible, values rendered as text.
- [x] Link static page from existing demo. Run Python tests, Node tests and Chromium browser checks.

## Task 3: review and repository candidate

- [x] Dispatch one fresh read-only reviewer on changed files, spec, plan and rulings.
- [x] TDD-fix important findings in one pass, verify full focused suite and exact payload hashes.
- [x] Create isolated branch/commit and draft PR from unchanged protected-main base. Inspect exact remote head/check outcomes without merging or deployment.
- [x] Save concise verification receipt and runnable handoff if repository write is unavailable.
