from __future__ import annotations

import fnmatch
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_dgaf_architecture_ownership_drift import candidates  # noqa: E402

REGISTRY = ROOT / "docs" / "architecture" / "DGAF_ASSURANCE_BUNDLE_REGISTRY.v1.json"
COMPONENTS = ROOT / "docs" / "architecture" / "DGAF_CORE_COMPONENT_REGISTRY.v1.json"


def canonical_ids() -> set[str]:
    data = json.loads(COMPONENTS.read_text(encoding="utf-8"))
    ids: set[str] = set()
    for key in (
        "core_components",
        "assurance_components",
        "governed_profiles",
        "external_integrations",
    ):
        ids.update(str(item["id"]) for item in data[key])
    return ids


def _matches(path: str, bundle: dict[str, object]) -> bool:
    includes = bundle.get("include_globs")
    excludes = bundle.get("exclude_globs")
    if not isinstance(includes, list) or not includes:
        return False
    if not isinstance(excludes, list):
        return False
    included = any(fnmatch.fnmatch(path, str(pattern)) for pattern in includes)
    excluded = any(fnmatch.fnmatch(path, str(pattern)) for pattern in excludes)
    return included and not excluded


def validate_assurance_bundles(path: Path = REGISTRY) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "dgaf-assurance-bundle-registry.v1":
        errors.append("unexpected schema_version")

    bundles = data.get("bundles")
    if not isinstance(bundles, list) or not bundles:
        return errors + ["bundles must be a non-empty list"]

    ids = canonical_ids()
    seen: set[str] = set()
    for bundle in bundles:
        bundle_id = str(bundle.get("id", ""))
        if not bundle_id.startswith("AB-"):
            errors.append(f"invalid assurance bundle id: {bundle_id!r}")
        if bundle_id in seen:
            errors.append(f"duplicate assurance bundle id: {bundle_id}")
        seen.add(bundle_id)

        owner = bundle.get("primary_owner")
        if owner not in ids or not str(owner).startswith("A"):
            errors.append(f"{bundle_id}: invalid assurance primary owner {owner!r}")

        deps = bundle.get("secondary_dependencies")
        if not isinstance(deps, list):
            errors.append(f"{bundle_id}: secondary_dependencies must be a list")
        else:
            unknown = sorted(set(map(str, deps)) - ids)
            if unknown:
                errors.append(f"{bundle_id}: unknown dependencies {unknown}")

        profile = bundle.get("profile")
        if profile is not None and (profile not in ids or not str(profile).startswith("P-")):
            errors.append(f"{bundle_id}: invalid profile {profile!r}")

        includes = bundle.get("include_globs")
        excludes = bundle.get("exclude_globs")
        if not isinstance(includes, list) or not includes:
            errors.append(f"{bundle_id}: include_globs must be non-empty")
        if not isinstance(excludes, list):
            errors.append(f"{bundle_id}: exclude_globs must be a list")

        if not bundle.get("assurance_effect"):
            errors.append(f"{bundle_id}: assurance_effect missing")

    for artifact in candidates()["ASSURANCE"]:
        matches = [str(bundle["id"]) for bundle in bundles if _matches(artifact, bundle)]
        if len(matches) != 1:
            errors.append(f"{artifact}: expected exactly one assurance bundle, got {matches}")

    return errors


def covered_assurance_candidates(path: Path = REGISTRY) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    bundles = data["bundles"]
    covered: set[str] = set()
    for artifact in candidates()["ASSURANCE"]:
        matches = [bundle for bundle in bundles if _matches(artifact, bundle)]
        if len(matches) == 1:
            covered.add(artifact)
    return covered


def main() -> int:
    errors = validate_assurance_bundles()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    covered = covered_assurance_candidates()
    print(f"DGAF assurance bundle registry: PASS " f"({len(covered)} assurance candidates covered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
