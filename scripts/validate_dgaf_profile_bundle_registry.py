from __future__ import annotations

import fnmatch
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_dgaf_architecture_ownership_drift import candidates  # noqa: E402

BUNDLES = ROOT / "docs" / "architecture" / "DGAF_PROFILE_BUNDLE_REGISTRY.v1.json"
COMPONENTS = ROOT / "docs" / "architecture" / "DGAF_CORE_COMPONENT_REGISTRY.v1.json"


def canonical_profile_ids() -> set[str]:
    data = json.loads(COMPONENTS.read_text(encoding="utf-8"))
    return {str(item["id"]) for item in data["governed_profiles"]}


def _matching_profiles(path: str, profiles: list[dict[str, object]]) -> list[str]:
    matches: list[str] = []
    for profile in profiles:
        globs = profile.get("path_globs")
        if not isinstance(globs, list):
            continue
        if any(fnmatch.fnmatch(path, str(pattern)) for pattern in globs):
            matches.append(str(profile.get("id", "")))
    return matches


def validate_profile_bundles(path: Path = BUNDLES) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "dgaf-profile-bundle-registry.v1":
        errors.append("unexpected schema_version")

    profiles = data.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        return errors + ["profiles must be a non-empty list"]

    canonical = canonical_profile_ids()
    seen_ids: set[str] = set()
    for profile in profiles:
        profile_id = str(profile.get("id", ""))
        if profile_id not in canonical:
            errors.append(f"unknown profile id: {profile_id!r}")
        if profile_id in seen_ids:
            errors.append(f"duplicate profile id: {profile_id}")
        seen_ids.add(profile_id)

        globs = profile.get("path_globs")
        if not isinstance(globs, list) or not globs:
            errors.append(f"{profile_id}: path_globs must be non-empty")
        else:
            for pattern in globs:
                matched = [
                    p.relative_to(ROOT).as_posix()
                    for p in ROOT.rglob("*")
                    if p.is_file() and fnmatch.fnmatch(p.relative_to(ROOT).as_posix(), str(pattern))
                ]
                if not matched:
                    errors.append(f"{profile_id}: glob matches no files: {pattern}")

        sections = profile.get("sections")
        if not isinstance(sections, list) or not sections:
            errors.append(f"{profile_id}: sections must be non-empty")

        deps = profile.get("kernel_dependencies")
        if not isinstance(deps, list) or not deps:
            errors.append(f"{profile_id}: kernel_dependencies must be non-empty")

        if not profile.get("authority_boundary"):
            errors.append(f"{profile_id}: authority_boundary missing")

    for candidate in candidates()["PROFILE"]:
        matches = _matching_profiles(candidate, profiles)
        if len(matches) != 1:
            errors.append(f"{candidate}: expected exactly one profile bundle, got {matches}")

    return errors


def covered_profile_candidates(path: Path = BUNDLES) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    profiles = data["profiles"]
    covered: set[str] = set()
    for candidate in candidates()["PROFILE"]:
        if len(_matching_profiles(candidate, profiles)) == 1:
            covered.add(candidate)
    return covered


def main() -> int:
    errors = validate_profile_bundles()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    covered = covered_profile_candidates()
    print(f"DGAF profile bundle registry: PASS ({len(covered)} profile candidates covered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
