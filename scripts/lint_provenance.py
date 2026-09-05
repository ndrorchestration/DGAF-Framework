#!/usr/bin/env python3
"""Validate DGAF metric provenance and block unsupported VERIFIED promotion."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REGISTRY_REL = Path("docs/qa/METRICS_PROVENANCE.json")
ALLOWED_METRIC_STATUSES = {"VERIFIED", "DEPENDENCY_BLOCKED", "HISTORICAL_UNVERIFIED", "NON_REPRODUCIBLE"}
ALLOWED_DEPENDENCY_STATUSES = {"VERIFIED", "UNRESOLVED", "DEPRECATED", "SHADOW", "CONTRADICTORY"}
REQUIRED_VERIFIED_FIELDS = ("definition", "calculation_method", "unit", "score_range", "dataset_or_corpus", "baseline", "configuration_identity", "source_commit", "execution", "reproduction", "dependencies")
CLAIM_PATTERNS = {
    "M-P10-SPEED": re.compile(r"(?<!\d)(?:\+?340\s*%|3\.4\s*[x×])(?!\d)", re.I),
    "M-P11-HUMAN-REVIEW": re.compile(r"(?<!\d)21\s*%(?!\d)", re.I),
    "M-P29-LATENCY": re.compile(r"(?<!\d)62\s*%(?!\d)", re.I),
    "M-P29-TOKENS": re.compile(r"(?<!\d)42\s*%(?!\d)", re.I),
    "M-P34-945": re.compile(r"(?<!\d)94\.5\s*%(?!\d)", re.I),
    "M-P36-MTTE": re.compile(r"(?<!\d)58\.3\s*%(?!\d)", re.I),
    "M-P37-PRECISION": re.compile(r"(?<!\d)96\s*%(?!\d)", re.I),
    "M-P39-TRANSFER": re.compile(r"(?<!\d)95\s*%(?!\d)", re.I),
    "M-P40-F1": re.compile(r"(?<!\d)82\.6\s*%(?!\d)", re.I),
}
PROMOTION_WORDS = re.compile(r"\b(?:verified|validated|confirmed|proven|reproduced)\b", re.I)
QUALIFIERS = re.compile(r"\b(?:historical|legacy|unverified|not\s+verified|dependency[- ]blocked|conditional|attestation|attested|reported|claim(?:ed)?|provenance\s+incomplete|current\s+status)\b", re.I)
EXCLUDED_DIR_PARTS = {".git", "node_modules", "build", "dist", "__pycache__", "archive", "archives"}


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


def _missing(value: object) -> bool:
    return value is None or value == "" or value == [] or value == {}


def load_registry(root: Path) -> dict:
    path = root / REGISTRY_REL
    if not path.is_file():
        raise ValueError(f"missing provenance registry: {REGISTRY_REL}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {REGISTRY_REL}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("provenance registry root must be an object")
    return data


def validate_registry(data: dict) -> list[Finding]:
    findings: list[Finding] = []
    if data.get("schema_version") != 1:
        findings.append(Finding("ERROR", "schema_version must be 1"))
    if data.get("promotion_rule") != "ALL_DEPENDENCIES_VERIFIED_AND_REPRODUCIBLE":
        findings.append(Finding("ERROR", "promotion_rule must be ALL_DEPENDENCIES_VERIFIED_AND_REPRODUCIBLE"))

    dependencies = data.get("dependency_registry")
    metrics = data.get("metrics")
    if not isinstance(dependencies, list):
        findings.append(Finding("ERROR", "dependency_registry must be a list")); dependencies = []
    if not isinstance(metrics, list):
        findings.append(Finding("ERROR", "metrics must be a list")); metrics = []

    dep_status: dict[str, str] = {}
    for dep in dependencies:
        if not isinstance(dep, dict):
            findings.append(Finding("ERROR", "dependency entries must be objects")); continue
        dep_id = dep.get("dependency_id"); status = dep.get("epistemic_status")
        if not isinstance(dep_id, str) or not dep_id:
            findings.append(Finding("ERROR", "dependency entry missing dependency_id")); continue
        if dep_id in dep_status:
            findings.append(Finding("ERROR", f"duplicate dependency_id {dep_id}"))
        if status not in ALLOWED_DEPENDENCY_STATUSES:
            findings.append(Finding("ERROR", f"dependency {dep_id}: invalid epistemic_status {status!r}"))
        dep_status[dep_id] = str(status)

    seen: set[str] = set()
    for metric in metrics:
        if not isinstance(metric, dict):
            findings.append(Finding("ERROR", "metric entries must be objects")); continue
        metric_id = metric.get("metric_id")
        if not isinstance(metric_id, str) or not metric_id:
            findings.append(Finding("ERROR", "metric entry missing metric_id")); continue
        if metric_id in seen:
            findings.append(Finding("ERROR", f"duplicate metric_id {metric_id}"))
        seen.add(metric_id)
        status = metric.get("epistemic_status")
        if status not in ALLOWED_METRIC_STATUSES:
            findings.append(Finding("ERROR", f"{metric_id}: invalid epistemic_status {status!r}")); continue
        dep_ids = metric.get("dependencies")
        if not isinstance(dep_ids, list):
            findings.append(Finding("ERROR", f"{metric_id}: dependencies must be a list")); dep_ids = []
        unknown = [dep for dep in dep_ids if dep not in dep_status]
        if unknown:
            findings.append(Finding("ERROR", f"{metric_id}: unknown dependencies {unknown}"))

        reproduction = metric.get("reproduction"); execution = metric.get("execution")
        if status == "VERIFIED":
            missing_fields = [field for field in REQUIRED_VERIFIED_FIELDS if _missing(metric.get(field))]
            if missing_fields:
                findings.append(Finding("ERROR", f"{metric_id}: VERIFIED missing fields {missing_fields}"))
            blocking = [dep for dep in dep_ids if dep_status.get(dep) != "VERIFIED"]
            if blocking:
                findings.append(Finding("ERROR", f"{metric_id}: VERIFIED blocked by dependencies {blocking}"))
            if not isinstance(reproduction, dict) or reproduction.get("status") != "REPRODUCIBLE" or not reproduction.get("command"):
                findings.append(Finding("ERROR", f"{metric_id}: VERIFIED requires REPRODUCIBLE command"))
            if not isinstance(execution, dict) or any(_missing(execution.get(k)) for k in ("workflow_run_id", "artifact_id", "timestamp")):
                findings.append(Finding("ERROR", f"{metric_id}: VERIFIED requires workflow_run_id, artifact_id, and timestamp"))
        elif isinstance(reproduction, dict) and reproduction.get("status") == "REPRODUCIBLE" and not reproduction.get("command"):
            findings.append(Finding("ERROR", f"{metric_id}: REPRODUCIBLE requires a command"))

    missing_known = sorted(set(CLAIM_PATTERNS) - seen)
    if missing_known:
        findings.append(Finding("ERROR", f"registry missing known metric records: {missing_known}"))
    return findings


def _iter_markdown(root: Path) -> Iterable[Path]:
    for candidate in (root / "README.md", root / "docs"):
        if candidate.is_file():
            yield candidate; continue
        if not candidate.is_dir():
            continue
        for path in candidate.rglob("*.md"):
            rel_parts = set(path.relative_to(root).parts)
            if rel_parts & EXCLUDED_DIR_PARTS:
                continue
            yield path


def scan_surfaces(root: Path, data: dict) -> list[Finding]:
    """Warn on current-looking promotion language without rewriting historical records."""
    metric_status = {m["metric_id"]: m.get("epistemic_status") for m in data.get("metrics", []) if isinstance(m, dict) and isinstance(m.get("metric_id"), str)}
    findings: list[Finding] = []
    for path in _iter_markdown(root):
        rel = path.relative_to(root)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(lines, 1):
            if not PROMOTION_WORDS.search(line) or QUALIFIERS.search(line):
                continue
            for metric_id, pattern in CLAIM_PATTERNS.items():
                if pattern.search(line) and metric_status.get(metric_id) != "VERIFIED":
                    findings.append(Finding("WARNING", f"{rel}:{line_no}: {metric_id} appears with promotion language while registry status is {metric_status.get(metric_id)}"))
    return findings


def build_report(findings: list[Finding]) -> str:
    errors = sum(f.level == "ERROR" for f in findings); warnings = sum(f.level == "WARNING" for f in findings)
    lines = [f"metrics provenance: {errors} error(s), {warnings} warning(s)"]
    lines.extend(f"[{f.level}] {f.message}" for f in findings)
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--no-scan", action="store_true", help="validate registry only")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv); root = args.root.resolve()
    try:
        data = load_registry(root)
    except ValueError as exc:
        print(f"metrics provenance: 1 error(s), 0 warning(s)\n[ERROR] {exc}"); return 1
    findings = validate_registry(data)
    if not args.no_scan:
        findings.extend(scan_surfaces(root, data))
    print(build_report(findings))
    return 1 if any(f.level == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
