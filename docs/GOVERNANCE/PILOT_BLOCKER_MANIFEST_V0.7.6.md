# PDMAL v0.7.6 Pilot Blocker Manifest

This document explains the machine-readable `PILOT_BLOCKER_MANIFEST_V0.7.6.json` record.

The JSON manifest is a dated, fail-closed checkpoint for the remaining path from current apparatus testability to an authorized empirical pilot. It consolidates the controlling open blockers tracked in Issues #277, #295, #309, #310, #316, and #320 without changing their authority or independently adjudicating them.

## Current boundary

- Current v0.7.6 contract rehearsal: **available for non-empirical testing**.
- Current merged-main live regression: **PASS at the recorded checkpoint**.
- Final candidate: **NOT DESIGNATED**.
- Freeze: **NOT ESTABLISHED**.
- Pilot authorization: **NOT GRANTED**.
- Empirical execution: **PROHIBITED**.
- Empirical N: **0**.

## Why this exists

The remaining prerequisites are distributed across several governance, security, cloud-admission, retention, and continuity tracks. The machine-readable manifest makes four facts explicit for each blocker:

1. what repository preparation is already available;
2. what external or administrative fact is still missing;
3. which role or authority must establish that fact;
4. which downstream gates remain blocked until it is accepted.

This reduces handoff ambiguity. It does not collapse distinct authorities into one self-certified repository record.

## Validation contract

`scripts/validate_pilot_blocker_manifest.py` fails closed if the checkpoint is silently promoted. Its negative controls require rejection when, among other cases:

- an open external blocker is marked satisfied;
- pilot authorization is changed to granted;
- empirical pilot execution is changed to permitted;
- the explicit authorization step is removed from the required sequence.

The validator runs inside `External Acceptance Readiness Validation` alongside the existing inert-template checks.

## Updating this manifest

Do not edit `satisfied`, controlling-state values, or downstream permission fields merely because an issue receives new comments or CI turns green. A blocker can be promoted only when the authority named by its governing issue has produced the required evidence and that evidence has been accepted under the applicable contract.

When the recorded `main_commit_sha` changes due to a new authoritative readiness checkpoint, update both the JSON checkpoint and the validator's expected checkpoint in the same reviewed change.

The manifest itself does not establish P4, designate a candidate, freeze the protocol, grant authorization, execute P9, or increase empirical N.
