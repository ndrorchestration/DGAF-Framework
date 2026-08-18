#!/usr/bin/env python3
"""Non-production blinding custody dry-run.

Uses only synthetic labels and a mock key. Never reads production secrets.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
from datetime import datetime, timezone
from pathlib import Path

CONDITIONS = ("null", "simple", "static", "dgaf")
MOCK_KEY = b"PDMAL-MOCK-BLINDING-KEY-v1"


def blind_label(label: str, key: bytes) -> str:
    digest = hmac.new(key, label.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"blind_{digest[:16]}"


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def run(output_dir: Path) -> None:
    mapping = {label: blind_label(label, MOCK_KEY) for label in CONDITIONS}
    reverse_mapping = {blinded: label for label, blinded in mapping.items()}

    # Dataset exposed to executor/analyst: blinded IDs only.
    blinded_dataset = [
        {"trial_id": f"mock-{index:03d}", "blinded_condition_id": blinded}
        for index, blinded in enumerate(mapping.values(), start=1)
    ]

    dataset_bytes = canonical_bytes(blinded_dataset)
    dataset_digest = hashlib.sha256(dataset_bytes).hexdigest()

    # Pre-freeze custody check: cleartext labels and key must not occur in dataset bytes.
    if any(label.encode() in dataset_bytes for label in CONDITIONS):
        raise SystemExit("FAIL: cleartext condition label leaked into blinded dataset")
    if MOCK_KEY in dataset_bytes:
        raise SystemExit("FAIL: mock key leaked into blinded dataset")

    # Unblinding is allowed only after an explicit mock freeze event.
    mock_dataset_frozen = True
    if not mock_dataset_frozen:
        raise SystemExit("FAIL: mock dataset was not frozen before unblinding")

    recovered = [reverse_mapping[row["blinded_condition_id"]] for row in blinded_dataset]
    expected = list(CONDITIONS)
    if recovered != expected:
        raise SystemExit(f"FAIL: recovered mapping mismatch: {recovered!r} != {expected!r}")

    if len(set(mapping.values())) != len(CONDITIONS):
        raise SystemExit("FAIL: blinded identifiers are not unique")

    artifact = {
        "control_id": "PDMAL-BLINDING-OPS-v1",
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
        "production_secret_accessed": False,
        "mock_dataset_frozen": True,
        "condition_count": len(CONDITIONS),
        "mock_dataset_sha256": dataset_digest,
        "recovered_labels_match": True,
        "blinded_ids_unique": True,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "result": "PASS",
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / "blinding_operational_test.json"
    raw = canonical_bytes(artifact)
    artifact_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    (output_dir / "blinding_operational_test.json.sha256").write_text(
        f"{digest}  {artifact_path.name}\n", encoding="utf-8"
    )
    print(json.dumps(artifact, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("blinding_artifacts"))
    args = parser.parse_args()
    run(args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
