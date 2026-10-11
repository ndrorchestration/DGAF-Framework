"""Generate a deterministic synthetic assessment replay, never live containment."""

import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from scripts.dgaf_capability_canonicalize import sha256_digest
from scripts.dgaf_capability_pep import (
    ApprovalState,
    EnforcementContext,
    EnforcementRefusal,
    VerificationState,
    governed_dispatch,
)
from scripts.dgaf_capability_policy import Authority
from scripts.dgaf_containment_assessment import AssessmentInputError
from scripts.dgaf_containment_observation import assess_bound_snapshot

NOW = datetime(2026, 10, 11, 8, tzinfo=timezone.utc)
CASE_IDS = ("SC-01", "SC-05", "SC-13", "SC-16")


def build_projection(fixtures: Path) -> dict:
    contract = json.loads((fixtures / "contract.json").read_text(encoding="utf-8"))
    manifest = json.loads((fixtures / "manifest.json").read_text(encoding="utf-8"))
    if (
        set(manifest) != {"schema_version", "observations"}
        or manifest["schema_version"] != "SYNTHETIC_OBSERVATION_PINS_V1"
    ):
        raise AssessmentInputError("fixture manifest schema mismatch")
    if not isinstance(manifest["observations"], dict) or set(manifest["observations"]) != set(CASE_IDS):
        raise AssessmentInputError("fixture manifest case coverage mismatch")
    cases: list[dict[str, Any]] = []
    for case_id in CASE_IDS:
        definition = {**contract, "definition_version": "2"} if case_id == "SC-16" else contract
        result = assess_bound_snapshot(
            definition,
            (fixtures / "observations" / f"{case_id}.json").read_bytes(),
            expected_observation_digest=manifest["observations"][case_id],
            now=NOW,
        )
        cases.append({"case_id": case_id, "assessment": result, "assessment_digest": sha256_digest(result)})
    prior = cases[0]["assessment"]
    authority = Authority(frozenset({"synthetic.restrict"}), frozenset({"synthetic-session"}))
    context = EnforcementContext(
        capability="synthetic.restrict",
        resource="synthetic-session",
        protected_side_effect=True,
        requester_authority=authority,
        delegation_authority=authority,
        executor_authority=authority,
        policy_authority=authority,
        authorization_status="ACTIVE",
        authorization_not_before=NOW - timedelta(seconds=1),
        authorization_expires_at=NOW + timedelta(seconds=60),
        commit_digest="synthetic-digest",
        approval=ApprovalState("requester", "approver", "synthetic-digest"),
        verification=VerificationState(required=True, passed=True),
        required_state_guards={},
        observed_state_guards={},
        now=NOW,
        prior_execution_receipt=prior,
        fresh_adjudication_complete=False,
    )
    calls = []

    def dispatcher(request):
        calls.append(request)
        return {}

    try:
        governed_dispatch({}, context, dispatcher=dispatcher)
    except EnforcementRefusal as exc:
        reason = str(exc)
    else:
        raise AssertionError("follow-on dispatch unexpectedly permitted")
    if calls or "fresh adjudication" not in reason:
        raise AssertionError("follow-on refusal boundary drift")
    cases.append(
        {
            "case_id": "SC-28",
            "observed": "REFUSED",
            "reason": reason,
            "dispatcher_calls": len(calls),
            "prior_assessment_digest": cases[0]["assessment_digest"],
            "authority_effect": "NONE",
            "follow_on_authority": "FRESH_ADJUDICATION_REQUIRED",
            "execution_permitted": False,
            "scientific_n_increment": 0,
        }
    )
    return {
        "schema_version": "TEKTITE_SYNTHETIC_CONTAINMENT_V1",
        "evidence_class": "SYNTHETIC",
        "evaluation_mode": "FIXED_TIME_SNAPSHOT_REPLAY",
        "evaluation_time": "2026-10-11T08:00:00Z",
        "source_baseline_commit": "aabf1163515af291dc564bd7564fd12762a898c8",
        "implementation_digests": {
            name: "sha256:" + hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
            for name in (
                "dgaf_containment_assessment.py",
                "dgaf_containment_observation.py",
                "generate_tektite_containment.py",
            )
        },
        "cases": cases,
        "claim_boundary": {
            "live_containment": "NOT_ESTABLISHED",
            "source_authenticity": "NOT_ESTABLISHED",
            "live_cross_system_integration": "NOT_RUN",
            "independent_validation": "NOT_ESTABLISHED",
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
            "scientific_n_increment": 0,
            "execution_permitted": False,
        },
    }


def render_html(projection: dict) -> str:
    payload = json.dumps(projection, ensure_ascii=True).replace("<", "\\u003c")
    return (
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tektite · Synthetic containment assessment</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#0b1220;color:#e5edf8}
body{max-width:1040px;margin:auto;padding:32px 20px}h1{font-size:clamp(26px,4vw,40px);margin:8px 0}
.eyebrow{color:#7bdacb;letter-spacing:.12em;font-size:12px}
.boundary,article{border:1px solid #2c4058;border-radius:12px;padding:20px;margin:18px 0;background:#111e30}
.boundary{border-color:#5b6881}p{line-height:1.6;color:#b7c8de}h2{font-size:20px}h3{font-size:15px}
code{overflow-wrap:anywhere;font-size:12px;color:#a4dad7}
dt{color:#91a9c9;margin-top:12px}
dd{margin:4px 0;overflow-wrap:anywhere}
.tag{font-size:12px;background:#25384d;border-radius:6px;padding:6px 10px;color:#c9dbef}.reasons{color:#f4cf8c}
details{margin-top:14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}a{color:#8cdcd1}
</style></head><body>
<span class="eyebrow">TEKTITE / EVIDENCE · MEANING · AUTHORITY</span>
<h1>What does “established” commit us to?</h1>
<p>Fixed-time synthetic snapshot replay · evaluation clock 2026-10-11 08:00 UTC.
These historical fixtures are not current monitoring.</p>
<div class="boundary">
<strong>Live containment: NOT_ESTABLISHED</strong>
<p>Digest matching checks record integrity relative to a separately supplied pin.
Producer authenticity and independent validation remain unestablished.
Every result carries no authority; follow-on execution requires fresh adjudication.
Scientific N +0.</p>
</div>
<main id="cases" aria-live="polite"><p>Loading bounded evidence…</p></main>
<script type="application/json" id="projection">"""
        + payload
        + """</script>
<script type="module">
import { mountProjection } from './tektite-containment-view.mjs';
mountProjection(document);
</script>
</body></html>
"""
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=Path("tests/fixtures/containment"))
    parser.add_argument("--output", type=Path, default=Path("public/evidence"))
    args = parser.parse_args()
    projection = build_projection(args.fixtures)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "tektite-containment-v0.json").write_text(json.dumps(projection, indent=2) + "\n", encoding="utf-8")
    (args.output / "tektite-containment-v0.html").write_text(render_html(projection), encoding="utf-8")
    print("TEKTITE_SYNTHETIC_CONTAINMENT_GENERATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
