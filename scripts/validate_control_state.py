from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/experiment/NEW_CANDIDATE_MANIFEST.md"

CONTROL_DOCS = {
    "docs/CURRENT_STATE.md": "active apparatus state",
    "docs/CLAIM_EVIDENCE_INDEX.md": "claim/evidence control surface",
    "docs/experiment/NEW_CANDIDATE_MANIFEST.md": "candidate manifest",
    "docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md": "PDMAL control state",
    "docs/experiment/N1_OPERATIONAL_CHARACTERIZATION_GATE_2026-08-30.md": "N=1 gate",
    "docs/experiment/FREEZE_MANIFEST.md": "freeze manifest",
    "docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md": "P1-P9 matrix",
}


def read(path: str | Path) -> str:
    target = ROOT / path if isinstance(path, str) else path
    if not target.is_file():
        raise AssertionError(f"missing canonical control document: {target}")
    return target.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path}: missing required value {needle!r}")


def manifest_identity(manifest: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key in (
        "apparatus_source_sha",
        "apparatus_source_tree_sha",
        "deployment_id",
        "deployment_url",
        "allowed_origin",
    ):
        match = re.search(rf"^{re.escape(key)}:\s*(\S+)\s*$", manifest, flags=re.MULTILINE)
        if match:
            fields[key] = match.group(1)
    return fields


def main() -> int:
    failures: list[str] = []
    manifest = read(MANIFEST_PATH)
    identity = manifest_identity(manifest)

    apparatus_sha = identity.get("apparatus_source_sha")
    if not apparatus_sha:
        failures.append("candidate manifest: missing apparatus_source_sha")
    else:
        for path in CONTROL_DOCS:
            try:
                assert_contains(read(path), apparatus_sha, path)
            except AssertionError as exc:
                failures.append(str(exc))

    prior_sha_match = re.search(
        r"prior_candidate:\s*\n\s*sha:\s*(\S+)", manifest, flags=re.MULTILINE
    )
    prior_sha = prior_sha_match.group(1) if prior_sha_match else None
    if prior_sha:
        live_markers = (
            "current apparatus",
            "current candidate",
            "designated apparatus candidate",
            "candidate basis",
        )
        for path in CONTROL_DOCS:
            text = read(path)
            live_lines = [
                line.strip()
                for line in text.splitlines()
                if prior_sha in line and any(marker in line.lower() for marker in live_markers)
            ]
            if live_lines:
                failures.append(f"{path}: superseded candidate presented as live: {live_lines}")

    current_state = read("docs/CURRENT_STATE.md")
    for label in ("main", "apparatus source", "candidate identity", "deployment identity"):
        try:
            assert_contains(current_state.lower(), label.lower(), "docs/CURRENT_STATE.md")
        except AssertionError as exc:
            failures.append(str(exc))

    if failures:
        print("CONTROL STATE VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONTROL STATE VALIDATION PASSED")
    print(f"apparatus_sha={apparatus_sha}")
    print("superseded candidate is not presented as live")
    print("four-identity separation is present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
