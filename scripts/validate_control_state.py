from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APPARATUS_SHA = "d56b5b3c44e39ddb8c883259584432ab39259306"
APPARATUS_TREE_SHA = "8c13900c4ce2a503414f9dddf1d7ef7debead57e"
DEPLOYMENT_ID = "dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb"
DEPLOYMENT_URL = "https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app"
ALLOWED_ORIGIN = "https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app"
SUPERSEDED_CANDIDATE = "05fa286614bd80576c1f7f4b01f1bdd7fe57ef37"

CONTROL_DOCS = {
    "docs/CURRENT_STATE.md": "active apparatus state",
    "docs/CLAIM_EVIDENCE_INDEX.md": "claim/evidence control surface",
    "docs/experiment/NEW_CANDIDATE_MANIFEST.md": "candidate manifest",
    "docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md": "PDMAL control state",
    "docs/experiment/N1_OPERATIONAL_CHARACTERIZATION_GATE_2026-08-30.md": "N=1 gate",
    "docs/experiment/FREEZE_MANIFEST.md": "freeze manifest",
    "docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md": "P1-P9 matrix",
    "docs/DRIFT_CORRECTION_NOTE_2026-08-31.md": "documentation drift correction note",
    "docs/evidence/PDMAL_EVIDENCE_INDEX.md": "evidence index",
}

# Phrases that, if present, assert a STALE SHA is the CURRENT apparatus/candidate.
# These must never appear with a non-current SHA (02e4c958 is pre-#170 P-31/P-33
# only; 05fa286 is the superseded post-#151 candidate). The current apparatus is
# d56b5b3c (PR #170).
FORBIDDEN_LIVE_PHRASES = {
    "docs/DRIFT_CORRECTION_NOTE_2026-08-31.md": [
        "Current apparatus source: `02e4c958",
        "Current `main` documentation tip: `34e1a057",
    ],
    "docs/evidence/PDMAL_EVIDENCE_INDEX.md": [
        "current designated apparatus candidate is `05fa286",
        "Current post-#151 apparatus candidate | DESIGNATED / NOT FROZEN | `05fa286",
    ],
}


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        raise AssertionError(f"missing canonical control document: {path}")
    return target.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise AssertionError(f"{path}: missing required value {needle!r}")


def main() -> int:
    failures: list[str] = []

    for path in CONTROL_DOCS:
        try:
            text = read(path)
            assert_contains(text, APPARATUS_SHA, path)
        except AssertionError as exc:
            failures.append(str(exc))

        try:
            text = read(path)
            for forbidden in FORBIDDEN_LIVE_PHRASES.get(path, []):
                if forbidden in text:
                    raise AssertionError(
                        f"{path}: forbidden stale-SHA-as-current phrase present: {forbidden!r}"
                    )
        except AssertionError as exc:
            failures.append(str(exc))

        try:
            text = read(path)
            if SUPERSEDED_CANDIDATE in text:
                live_lines = []
                for line in text.splitlines():
                    lowered = line.lower()
                    if SUPERSEDED_CANDIDATE in line and any(
                        marker in lowered
                        for marker in (
                            "current apparatus",
                            "current candidate",
                            "designated apparatus candidate",
                            "current post-#151 apparatus candidate",
                            "candidate basis",
                            "current post-#151",
                        )
                    ):
                        live_lines.append(line.strip())
                if live_lines:
                    raise AssertionError(
                        f"{path}: superseded candidate presented as live: {live_lines}"
                    )
        except AssertionError as exc:
            failures.append(str(exc))

    manifest = read("docs/experiment/NEW_CANDIDATE_MANIFEST.md")
    for value in (APPARATUS_TREE_SHA, DEPLOYMENT_ID, DEPLOYMENT_URL, ALLOWED_ORIGIN):
        try:
            assert_contains(manifest, value, "docs/experiment/NEW_CANDIDATE_MANIFEST.md")
        except AssertionError as exc:
            failures.append(str(exc))

    current_state = read("docs/CURRENT_STATE.md")
    for identity_label in ("`main` tip", "apparatus source", "candidate identity", "deployment identity"):
        try:
            assert_contains(current_state, identity_label, "docs/CURRENT_STATE.md")
        except AssertionError as exc:
            failures.append(str(exc))

    if failures:
        print("CONTROL STATE VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONTROL STATE VALIDATION PASSED")
    print(f"apparatus_sha={APPARATUS_SHA}")
    print(f"deployment_id={DEPLOYMENT_ID}")
    print("superseded candidate is not presented as live")
    print("four-identity separation is present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
