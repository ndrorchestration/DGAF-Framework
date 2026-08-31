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


def field(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(\S+)\s*$", text, flags=re.MULTILINE)
    return match.group(1) if match else None


def nested_field(text: str, block: str, key: str) -> str | None:
    match = re.search(
        rf"^{re.escape(block)}:\s*\n(?P<body>(?:^[ \t]+.*\n?)*)",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        return None
    return field(match.group("body"), key)


def manifest_identity(manifest: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key in ("apparatus_source_sha", "apparatus_source_tree_sha"):
        value = field(manifest, key)
        if value:
            fields[key] = value

    # Only read deployment identity from the active deployment_binding block.
    # Historical deployment IDs elsewhere in the manifest must never satisfy
    # or invalidate the current deployment-state invariant.
    for key in ("deployment_id", "deployment_url", "deployment_target", "deployment_state", "source_sha_match"):
        value = nested_field(manifest, "deployment_binding", key)
        if value:
            fields[key] = value
    return fields


def main() -> int:
    failures: list[str] = []
    manifest = read(MANIFEST_PATH)
    identity = manifest_identity(manifest)

    apparatus_sha = identity.get("apparatus_source_sha")
    tree_sha = identity.get("apparatus_source_tree_sha")
    if not apparatus_sha:
        failures.append("candidate manifest: missing apparatus_source_sha")
    if not tree_sha:
        failures.append("candidate manifest: missing apparatus_source_tree_sha")

    if apparatus_sha:
        for path in CONTROL_DOCS:
            try:
                assert_contains(read(path), apparatus_sha, path)
            except AssertionError as exc:
                failures.append(str(exc))

    # Deployment identity must remain explicitly unresolved until an exact,
    # candidate-matched production deployment has actually been established.
    deployment_id = identity.get("deployment_id")
    deployment_url = identity.get("deployment_url")
    if deployment_id and deployment_url:
        unresolved = {"NONE_YET", "NONE", "NOT_ESTABLISHED"}
        if deployment_id not in unresolved and deployment_url not in unresolved:
            deployment_sha = identity.get("source_sha_match")
            if deployment_sha and deployment_sha not in {"true", "TRUE", "YES", "MATCHED"}:
                failures.append(
                    "candidate manifest: active deployment identity is concrete but source_sha_match is not affirmative"
                )

    prior_sha = None
    prior_match = re.search(
        r"prior_candidate:\s*\n\s*sha:\s*(\S+)", manifest, flags=re.MULTILINE
    )
    if prior_match:
        prior_sha = prior_match.group(1)

    if prior_sha:
        live_markers = (
            "current apparatus",
            "current candidate",
            "designated apparatus candidate",
            "candidate basis",
            "execution-valid candidate",
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

    # Governance invariants: no execution-valid state may coexist with N=0
    # unless the repository explicitly says the candidate remains pre-freeze.
    control_state = read("docs/governance/CONTROL_STATE_2026-08-31.yaml")
    if "empirical_n: 0" in control_state and "authorization: NOT_GRANTED" not in control_state:
        failures.append("control state: empirical_n=0 must retain authorization=NOT_GRANTED")
    if "freeze_status: NOT_CREATED" in manifest and "authorization: NOT GRANTED" not in manifest:
        failures.append("candidate manifest: NOT_CREATED freeze must retain NOT GRANTED authorization")

    if failures:
        print("CONTROL STATE VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONTROL STATE VALIDATION PASSED")
    print(f"apparatus_sha={apparatus_sha}")
    print(f"apparatus_tree_sha={tree_sha}")
    print("active deployment binding is internally scoped")
    print("superseded candidate is not presented as live")
    print("cross-document apparatus identity is present")
    print("pre-freeze authorization/N invariants are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
