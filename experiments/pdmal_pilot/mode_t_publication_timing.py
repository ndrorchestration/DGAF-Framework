"""Synthetic upload transport measurement; never durable custody or authorization."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import urllib.request
from pathlib import Path
from time import monotonic_ns

CLASS = "P4_MODE_T_SYNTHETIC_PUBLICATION_TIMING_NOT_AUTHORIZATION"
ACTION = "ea165f8d65b6e75b540449e92b4886f43607fa02"
ROOT = Path("test-artifacts")
STATE = ROOT / "publication-start.json"
FIXTURE = ROOT / "publication-fixture.bin"
OUTPUT = ROOT / "p4-mode-t-publication-timing.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def identity() -> dict:
    head = os.environ["EVIDENCE_SHA"]
    require(re.fullmatch(r"[0-9a-f]{40}", head) is not None, "invalid exact head")
    return {
        "control_plane_sha": head,
        "repository": os.environ["GITHUB_REPOSITORY"],
        "run_id": int(os.environ["GITHUB_RUN_ID"]),
        "run_attempt": int(os.environ["GITHUB_RUN_ATTEMPT"]),
        "workflow_ref": os.environ["GITHUB_WORKFLOW_REF"],
        "action_commit": ACTION,
    }


def prepare() -> None:
    from mode_t_timing_study import _load_tlock_encryption_stage

    source = ROOT / "p4-mode-t-timing-encryption.json"
    _load_tlock_encryption_stage(source)
    raw = source.read_bytes()
    evidence = json.loads(raw)
    sizes = evidence["ciphertext_sizes_bytes"]
    require(
        isinstance(sizes, list) and len(sizes) == evidence["sample_count"],
        "size sample mismatch",
    )
    require(
        all(type(n) is int and 1024 <= n <= 1048576 for n in sizes),
        "invalid ciphertext sizes",
    )
    size = max(sizes)
    prefix = (CLASS + "\n").encode()
    fixture = (prefix + b"." * size)[:size]
    FIXTURE.write_bytes(fixture)
    state = {
        **identity(),
        "evidence_class": CLASS,
        "fixture_bytes": size,
        "size_selection": "maximum synthetic ciphertext size in this run",
        "encryption_evidence_sha256": hashlib.sha256(raw).hexdigest(),
        "fixture_sha256": hashlib.sha256(fixture).hexdigest(),
        "artifact_name": "p4-mode-t-publication-fixture-"
        + os.environ["EVIDENCE_SHA"]
        + "-"
        + os.environ["GITHUB_RUN_ID"]
        + "-"
        + os.environ["GITHUB_RUN_ATTEMPT"],
    }
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
        stream.write("artifact_name=" + state["artifact_name"] + "\n")
    state["start_monotonic_ns"] = monotonic_ns()
    STATE.write_text(json.dumps(state), encoding="utf-8")


def validate_metadata(
    state: dict, metadata: dict, artifact_id: int, digest: str
) -> None:
    require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, "invalid upload digest")
    require(
        artifact_id > 0 and metadata.get("id") == artifact_id, "artifact ID mismatch"
    )
    require(metadata.get("name") == state["artifact_name"], "artifact name mismatch")
    require(metadata.get("digest") == "sha256:" + digest, "artifact digest mismatch")
    require(metadata.get("expired") is False, "artifact expired or unknown")
    run = metadata.get("workflow_run", {})
    require(run.get("id") == state["run_id"], "artifact run mismatch")
    require(run.get("head_sha") == state["control_plane_sha"], "artifact head mismatch")


def load_stage(path: Path) -> dict:
    raw = path.read_bytes()
    digest, filename = path.with_suffix(".json.sha256").read_text().split()
    require(
        filename == path.name and digest == hashlib.sha256(raw).hexdigest(),
        "publication sidecar mismatch",
    )
    data = json.loads(raw)
    require(
        all(data.get(k) == v for k, v in identity().items()),
        "publication identity mismatch",
    )
    require(
        data.get("evidence_class") == CLASS and data.get("status") == "PASS",
        "publication not PASS",
    )
    require(
        data.get("api_metadata_verified") is True, "publication metadata unverified"
    )
    for field in (
        "durable_custody",
        "external_transparency_verified",
        "coverage_complete",
        "w_proposal_eligible",
        "numeric_w_selected",
        "protocol_frozen",
        "pilot_authorized",
        "empirical_data_collection",
    ):
        require(data.get(field) is False, "publication invalid control: " + field)
    require(data.get("proposed_w_seconds") is None, "publication selected W")
    require(
        type(data.get("duration_ms")) in (int, float)
        and math.isfinite(data["duration_ms"])
        and data["duration_ms"] >= 0,
        "invalid publication duration",
    )
    require(
        type(data.get("start_monotonic_ns")) is int
        and type(data.get("end_monotonic_ns")) is int,
        "missing monotonic interval",
    )
    require(
        0 < data["start_monotonic_ns"] <= data["end_monotonic_ns"],
        "invalid monotonic interval",
    )
    require(
        data["duration_ms"]
        == (data["end_monotonic_ns"] - data["start_monotonic_ns"]) / 1_000_000,
        "duration mismatch",
    )
    require(
        re.fullmatch(r"sha256:[0-9a-f]{64}", data.get("artifact_digest", ""))
        is not None,
        "invalid artifact digest",
    )
    require(
        type(data.get("artifact_id")) is int and data["artifact_id"] > 0,
        "invalid artifact ID",
    )
    return {**data, "evidence_content_sha256": digest}


def finish() -> None:
    # Capture before API retrieval so verification latency is not upload latency.
    ended = monotonic_ns()
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
        require(
            all(state.get(k) == v for k, v in identity().items()),
            "measurement identity mismatch",
        )
        started = state["start_monotonic_ns"]
        require(
            type(started) is int and 0 < started <= ended, "invalid monotonic interval"
        )
        require(
            hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == state["fixture_sha256"],
            "fixture changed",
        )
        artifact_id = int(os.environ["PUBLICATION_ARTIFACT_ID"])
        digest = os.environ["PUBLICATION_ARTIFACT_DIGEST"]
        expected_url = f"https://github.com/{state['repository']}/actions/runs/{state['run_id']}/artifacts/{artifact_id}"
        require(
            os.environ["PUBLICATION_ARTIFACT_URL"] == expected_url,
            "artifact URL mismatch",
        )
        request = urllib.request.Request(
            f"https://api.github.com/repos/{state['repository']}/actions/artifacts/{artifact_id}",
            headers={
                "Authorization": "Bearer " + os.environ["GH_TOKEN"],
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            metadata = json.load(response)
        validate_metadata(state, metadata, artifact_id, digest)
        evidence = {
            **state,
            "status": "PASS",
            "end_monotonic_ns": ended,
            "duration_ms": (ended - started) / 1_000_000,
            "measurement_scope": "action boundary including runner step transition overhead; excludes API verification",
            "artifact_id": artifact_id,
            "artifact_url": expected_url,
            "artifact_digest": "sha256:" + digest,
            "api_metadata_verified": True,
            "sample_count": 1,
            "durable_custody": False,
            "external_transparency_verified": False,
            "coverage_complete": False,
            "w_proposal_eligible": False,
            "numeric_w_selected": False,
            "proposed_w_seconds": None,
            "protocol_frozen": False,
            "pilot_authorized": False,
            "empirical_data_collection": False,
        }
        raw = (json.dumps(evidence, sort_keys=True, indent=2) + "\n").encode()
        OUTPUT.write_bytes(raw)
        OUTPUT.with_suffix(".json.sha256").write_text(
            hashlib.sha256(raw).hexdigest() + "  " + OUTPUT.name + "\n",
            encoding="utf-8",
        )
    finally:
        FIXTURE.unlink(missing_ok=True)


if __name__ == "__main__":
    {"prepare": prepare, "finish": finish}[sys.argv[1]]()
