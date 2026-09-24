#!/usr/bin/env python3
"""Run the bounded DGAF operator self-test and retain a local evidence packet.

This is INTERNAL engineering validation only. It must never be represented as
independent validation, external validation, scientific replication, efficacy
evidence, or High-Assurance authorization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_ACP_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
DIRTY_PROBE = "OPERATOR_SELFTEST_DIRTY_PROBE.txt"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _run(
    argv: list[str],
    *,
    cwd: Path,
    expect: int | None = 0,
) -> dict[str, Any]:
    started = _now()
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONUTF8": "1"},
    )
    ended = _now()
    result = {
        "argv": argv,
        "cwd": str(cwd),
        "started_at": started,
        "completed_at": ended,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    if expect is not None:
        result["expected_returncode"] = expect
        result["returncode_match"] = completed.returncode == expect
    return result


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        text=True,
        capture_output=True,
        env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"},
    )
    return completed.stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _pass(name: str, detail: str = "") -> dict[str, Any]:
    return {"name": name, "status": "PASS", "detail": detail}


def _fail(name: str, detail: str) -> dict[str, Any]:
    return {"name": name, "status": "FAIL", "detail": detail}


def _record_command(
    checks: list[dict[str, Any]],
    logs: dict[str, dict[str, Any]],
    name: str,
    result: dict[str, Any],
    *,
    predicate: bool,
    detail: str,
) -> None:
    logs[name] = result
    checks.append(_pass(name, detail) if predicate else _fail(name, detail))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded internal DGAF operator self-testing.")
    parser.add_argument(
        "--dgaf-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--acp-root", type=Path, required=True)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path.home() / "DGAF-Operator-SelfTest-Results",
    )
    args = parser.parse_args()

    dgaf = args.dgaf_root.resolve()
    acp = args.acp_root.resolve()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = args.output_root.expanduser().resolve() / run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    checks: list[dict[str, Any]] = []
    logs: dict[str, dict[str, Any]] = {}
    started_at = _now()

    try:
        if sys.version_info[:2] == (3, 12):
            checks.append(_pass("python_3_12", platform.python_version()))
        else:
            checks.append(
                _fail(
                    "python_3_12",
                    f"Expected Python 3.12.x; observed {platform.python_version()}",
                )
            )

        for label, root in (("DGAF", dgaf), ("ACP", acp)):
            if not root.is_dir():
                checks.append(_fail(f"{label.lower()}_repository_exists", str(root)))
                continue
            try:
                _git(root, "rev-parse", "--git-dir")
                checks.append(_pass(f"{label.lower()}_repository_exists", str(root)))
            except (OSError, subprocess.CalledProcessError) as exc:
                checks.append(_fail(f"{label.lower()}_repository_exists", str(exc)))

        if any(item["status"] == "FAIL" for item in checks):
            raise RuntimeError("Repository/Python prerequisites failed")

        dgaf_head = _git(dgaf, "rev-parse", "HEAD")
        acp_head = _git(acp, "rev-parse", "HEAD")
        checks.append(_pass("dgaf_head_recorded", dgaf_head))

        if acp_head == EXPECTED_ACP_COMMIT:
            checks.append(_pass("acp_frozen_commit", acp_head))
        else:
            checks.append(
                _fail(
                    "acp_frozen_commit",
                    f"Expected {EXPECTED_ACP_COMMIT}; observed {acp_head}",
                )
            )

        for label, root in (("DGAF", dgaf), ("ACP", acp)):
            shallow = _git(root, "rev-parse", "--is-shallow-repository")
            dirty = _git(root, "status", "--porcelain=v1", "--untracked-files=all")
            replacement_refs = _git(root, "for-each-ref", "--format=%(refname)", "refs/replace")
            checks.append(
                _pass(f"{label.lower()}_full_clone")
                if shallow == "false"
                else _fail(f"{label.lower()}_full_clone", "shallow repository")
            )
            checks.append(
                _pass(f"{label.lower()}_clean_worktree")
                if not dirty
                else _fail(f"{label.lower()}_clean_worktree", dirty)
            )
            checks.append(
                _pass(f"{label.lower()}_no_replace_objects")
                if not replacement_refs
                else _fail(f"{label.lower()}_no_replace_objects", replacement_refs)
            )

        if any(item["status"] == "FAIL" for item in checks):
            raise RuntimeError("Static repository prerequisites failed")

        preflight = _run(
            [
                sys.executable,
                "scripts/run_aoss_v0_6_stage_a.py",
                "preflight",
                "--dgaf-root",
                str(dgaf),
                "--acp-root",
                str(acp),
            ],
            cwd=dgaf,
        )
        preflight_ok = preflight["returncode"] == 0
        if preflight_ok:
            try:
                payload = json.loads(preflight["stdout"])
                preflight_ok = (
                    payload.get("static_identity_checks") == "PASS"
                    and payload.get("outcomes_generated") is False
                    and payload.get("scientific_n_increment") == 0
                    and payload.get("external_validation_established") is False
                    and payload.get("canonical_dgaf_efficacy") == "NOT_ESTABLISHED"
                )
            except json.JSONDecodeError:
                preflight_ok = False
        _record_command(
            checks,
            logs,
            "aoss_static_preflight",
            preflight,
            predicate=preflight_ok,
            detail="Expected frozen identities accepted without evidence promotion",
        )

        quick = _run([sys.executable, "scripts/quick_check.py"], cwd=dgaf)
        _record_command(
            checks,
            logs,
            "dgaf_quick_regression",
            quick,
            predicate=quick["returncode"] == 0 and "ALL CHECKS PASSED" in quick["stdout"],
            detail="Core DGAF regression and tamper checks",
        )

        aoss_tests = sorted(str(path) for path in (dgaf / "tests").glob("test_aoss*.py"))
        pytest_result = _run(
            [sys.executable, "-m", "pytest", "-q", *aoss_tests],
            cwd=dgaf,
        )
        _record_command(
            checks,
            logs,
            "aoss_focused_pytest",
            pytest_result,
            predicate=pytest_result["returncode"] == 0 and bool(aoss_tests),
            detail=f"{len(aoss_tests)} AOSS test modules",
        )

        collect = _run(
            [sys.executable, "scripts/run_aoss_v0_6_stage_a.py", "collect"],
            cwd=dgaf,
            expect=2,
        )
        collect_text = collect["stdout"] + collect["stderr"]
        _record_command(
            checks,
            logs,
            "unauthorized_collection_block",
            collect,
            predicate=collect["returncode"] == 2 and "COLLECTION_IMPLEMENTATION_NOT_ACCEPTED" in collect_text,
            detail="Collection must remain unavailable at the current boundary",
        )

        probe = dgaf / DIRTY_PROBE
        if probe.exists():
            checks.append(_fail("dirty_worktree_fail_closed", f"Probe already exists: {probe}"))
        else:
            try:
                probe.write_text(
                    "Intentional DGAF operator self-test dirty-worktree probe.\n",
                    encoding="utf-8",
                )
                dirty_preflight = _run(
                    [
                        sys.executable,
                        "scripts/run_aoss_v0_6_stage_a.py",
                        "preflight",
                        "--dgaf-root",
                        str(dgaf),
                        "--acp-root",
                        str(acp),
                    ],
                    cwd=dgaf,
                    expect=1,
                )
                dirty_text = dirty_preflight["stdout"] + dirty_preflight["stderr"]
                _record_command(
                    checks,
                    logs,
                    "dirty_worktree_fail_closed",
                    dirty_preflight,
                    predicate=dirty_preflight["returncode"] == 1 and "DGAF_WORKTREE_DIRTY" in dirty_text,
                    detail="Intentional untracked probe must be rejected",
                )
            finally:
                if probe.exists():
                    probe.unlink()

        restored = _run(
            [
                sys.executable,
                "scripts/run_aoss_v0_6_stage_a.py",
                "preflight",
                "--dgaf-root",
                str(dgaf),
                "--acp-root",
                str(acp),
            ],
            cwd=dgaf,
        )
        _record_command(
            checks,
            logs,
            "restored_workspace_pass",
            restored,
            predicate=restored["returncode"] == 0,
            detail="Preflight must recover after deliberate probe removal",
        )

        final_dirty = _git(dgaf, "status", "--porcelain=v1", "--untracked-files=all")
        checks.append(
            _pass("dgaf_clean_after_selftest") if not final_dirty else _fail("dgaf_clean_after_selftest", final_dirty)
        )

    except Exception as exc:  # preserve partial evidence instead of hiding failure
        checks.append(_fail("selftest_execution", f"{type(exc).__name__}: {exc}"))

    status = "PASS" if checks and all(x["status"] == "PASS" for x in checks) else "FAIL"
    report = {
        "record_type": "DGAF_OPERATOR_SELFTEST",
        "schema_version": "1.0",
        "evidence_class": "INTERNAL_OPERATOR_ENGINEERING_VALIDATION",
        "status": status,
        "started_at": started_at,
        "completed_at": _now(),
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "executable": sys.executable,
            "platform": platform.platform(),
        },
        "dgaf_root": str(dgaf),
        "acp_root": str(acp),
        "expected_acp_commit": EXPECTED_ACP_COMMIT,
        "checks": checks,
        "claim_ceiling": {
            "independent_validation_established": False,
            "external_validation_established": False,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
            "high_assurance": "NOT_AUTHORIZED",
            "scientific_n_increment": 0,
        },
        "limitations": [
            "Executed by the project operator; this is not independent review.",
            "Passing software tests demonstrate covered behavior only.",
            "No result from this suite promotes collection or scientific authorization.",
            "External-review controller #929 remains separately required.",
        ],
    }

    report_path = output_dir / "operator_selftest_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    logs_dir = output_dir / "logs"
    logs_dir.mkdir()
    for name, payload in logs.items():
        (logs_dir / f"{name}.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    digest = _sha256(report_path)
    (output_dir / "operator_selftest_report.json.sha256").write_text(
        f"{digest}  {report_path.name}\n", encoding="utf-8"
    )

    md_lines = [
        "# DGAF Operator Self-Test",
        "",
        f"- Status: **{status}**",
        "- Evidence class: `INTERNAL_OPERATOR_ENGINEERING_VALIDATION`",
        f"- Started: `{report['started_at']}`",
        f"- Completed: `{report['completed_at']}`",
        f"- Report SHA-256: `{digest}`",
        "",
        "## Checks",
        "",
    ]
    for item in checks:
        detail = f" — {item['detail']}" if item.get("detail") else ""
        md_lines.append(f"- **{item['status']}** — {item['name']}{detail}")
    md_lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "- This run is internal engineering validation, not independent validation.",
            "- External validation remains not established.",
            "- Canonical DGAF efficacy remains not established.",
            "- High-Assurance remains not authorized.",
            "- Scientific N increment remains 0.",
            "",
        ]
    )
    (output_dir / "operator_selftest_summary.md").write_text("\n".join(md_lines), encoding="utf-8")

    print(json.dumps({"status": status, "output_dir": str(output_dir), "report_sha256": digest}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
