"""CI guardrail for DGAF evidence-tier and claim-surface integrity.

The validator is intentionally conservative: it fails on ambiguous or
contradictory evidence declarations instead of guessing intent. Operational
claim identity/state is owned by ``evidence/claims.json``. Evidence Cards may
enrich that state only through an explicit mapping in ``CLAIM_CARD_INDEX.yaml``;
unmapped specification cards do not create operational claim state.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "claims.json"
CARD_INDEX = ROOT / "docs" / "evidence" / "CLAIM_CARD_INDEX.yaml"
SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
FORBIDDEN_PRODUCTION_MARKERS = (
    "// stub",
    "# stub",
    "notimplemented",
    "not implemented",
    "placeholder",
)
CARD_RELATIONSHIPS = {"SPECIFICATION_ONLY", "CANONICAL_CLAIM_DETAIL"}
PROMOTED_CARD_CLASSES = {"VERIFIED", "ATTESTED"}
PROMOTED_MATURITY = {"EMPIRICALLY_SUPPORTED"}
PROMOTED_VALIDATION = {"INDEPENDENTLY_REPLICATED"}
CARD_STATE_FIELDS = ("claim_class", "evidence_maturity", "validation_status")


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"null", "~"}:
        return None
    if value.isdigit():
        return int(value)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _split_mapping(line: str, *, context: str) -> tuple[str, Any]:
    if ":" not in line:
        raise ValueError(f"{context}: expected key: value")
    key, raw = line.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"{context}: empty key")
    return key, _parse_scalar(raw)


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ValueError("evidence/claims.json must contain a top-level claims list")
    return data


def load_card_index(path: Path = CARD_INDEX) -> dict[str, Any]:
    """Parse the intentionally narrow CLAIM_CARD_INDEX.yaml without dependencies.

    The index is a controlled document, not a general YAML input. Unsupported
    indentation or structures fail closed rather than being guessed.
    """

    result: dict[str, Any] = {"authority": {}, "cards": []}
    section: str | None = None
    current_card: dict[str, Any] | None = None

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise ValueError(f"CLAIM_CARD_INDEX.yaml:{lineno}: tabs are not allowed")

        if not raw_line.startswith(" "):
            current_card = None
            if raw_line == "authority:":
                section = "authority"
                continue
            if raw_line == "cards:":
                section = "cards"
                continue
            key, value = _split_mapping(raw_line, context=f"CLAIM_CARD_INDEX.yaml:{lineno}")
            if key != "version":
                raise ValueError(f"CLAIM_CARD_INDEX.yaml:{lineno}: unsupported top-level key {key!r}")
            result["version"] = value
            continue

        if section == "authority" and raw_line.startswith("  ") and not raw_line.startswith("    "):
            key, value = _split_mapping(raw_line.strip(), context=f"CLAIM_CARD_INDEX.yaml:{lineno}")
            result["authority"][key] = value
            continue

        if section == "cards" and raw_line.startswith("  - "):
            current_card = {}
            result["cards"].append(current_card)
            key, value = _split_mapping(raw_line[4:], context=f"CLAIM_CARD_INDEX.yaml:{lineno}")
            current_card[key] = value
            continue

        if section == "cards" and current_card is not None and raw_line.startswith("    "):
            if raw_line.startswith("      "):
                raise ValueError(f"CLAIM_CARD_INDEX.yaml:{lineno}: nested card structures are unsupported")
            key, value = _split_mapping(raw_line.strip(), context=f"CLAIM_CARD_INDEX.yaml:{lineno}")
            current_card[key] = value
            continue

        raise ValueError(f"CLAIM_CARD_INDEX.yaml:{lineno}: unsupported structure")

    if result.get("version") != 2:
        raise ValueError("CLAIM_CARD_INDEX.yaml version must be 2")
    if not isinstance(result.get("cards"), list):
        raise ValueError("CLAIM_CARD_INDEX.yaml must contain a cards list")
    return result


def _safe_repo_path(relative_path: str) -> Path:
    if not relative_path or relative_path.startswith(("/", "\\")):
        raise ValueError(f"invalid repository-relative path: {relative_path!r}")
    resolved = (ROOT / relative_path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {relative_path}") from exc
    return resolved


def _default_card_loader(card_path: str) -> dict[str, Any]:
    path = _safe_repo_path(card_path)
    if not path.is_file():
        raise FileNotFoundError(card_path)

    wanted = {"id", *CARD_STATE_FIELDS}
    metadata: dict[str, Any] = {}
    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line or raw_line[0].isspace() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            continue
        key, value = _split_mapping(raw_line, context=f"{card_path}:{lineno}")
        if key not in wanted:
            continue
        if key in metadata:
            raise ValueError(f"{card_path}:{lineno}: duplicate top-level field {key}")
        metadata[key] = value

    missing = wanted - metadata.keys()
    if missing:
        raise ValueError(f"{card_path}: missing top-level metadata {sorted(missing)}")
    return metadata


def iter_sources() -> list[Path]:
    roots = [ROOT / "app", ROOT / "pages", ROOT / "components", ROOT / "src", ROOT / "tests", ROOT / "tools"]
    files: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        files.extend(p for p in base.rglob("*") if p.is_file() and p.suffix in SOURCE_EXTENSIONS)
    return files


def validate_claim_registry(registry: dict[str, Any]) -> tuple[list[str], dict[str, dict[str, Any]]]:
    failures: list[str] = []
    authority = registry.get("authority")
    if not isinstance(authority, dict):
        failures.append("claims registry: missing authority declaration")
    else:
        if authority.get("claim_identity_and_state") != "CANONICAL":
            failures.append("claims registry: claim_identity_and_state must be CANONICAL")
        if authority.get("evidence_card_relationship") != "EXPLICIT_REFERENCE_ONLY":
            failures.append("claims registry: evidence_card_relationship must be EXPLICIT_REFERENCE_ONLY")
        if authority.get("card_index") != "docs/evidence/CLAIM_CARD_INDEX.yaml":
            failures.append("claims registry: card_index must bind docs/evidence/CLAIM_CARD_INDEX.yaml")

    claims_by_id: dict[str, dict[str, Any]] = {}
    for claim in registry["claims"]:
        if not isinstance(claim, dict):
            failures.append("claim entry must be an object")
            continue
        claim_id = claim.get("claim_id")
        mode = claim.get("evidence_mode")
        status = claim.get("status")
        if not isinstance(claim_id, str) or not claim_id:
            failures.append("claim without claim_id")
            continue
        if claim_id in claims_by_id:
            failures.append(f"duplicate claim_id: {claim_id}")
        else:
            claims_by_id[claim_id] = claim
        if mode not in {"synthetic", "integration", "empirical", "production"}:
            failures.append(f"{claim_id}: unsupported evidence_mode={mode!r}")
        if mode in {"empirical", "production"} and status in {"VERIFIED", "ATTESTED"} and not claim.get("run_id"):
            failures.append(f"{claim_id}: {status} {mode} claim requires run_id")
        if mode == "empirical" and status in {"VERIFIED", "ATTESTED"} and not claim.get("dataset"):
            failures.append(f"{claim_id}: {status} empirical claim requires dataset")
        if status in {"VERIFIED", "ATTESTED"} and mode == "synthetic":
            failures.append(f"{claim_id}: {status} cannot be backed only by synthetic evidence")
    return failures, claims_by_id


def _mapping_state_failures(
    canonical_claim: dict[str, Any],
    card_entry: dict[str, Any],
    card: dict[str, Any] | None,
) -> list[str]:
    failures: list[str] = []
    status = canonical_claim.get("status")
    if status not in {"HYPOTHESIS", "BLOCKED"}:
        return failures

    state = card or card_entry
    claim_class = state.get("claim_class")
    evidence_maturity = state.get("evidence_maturity")
    validation_status = state.get("validation_status")
    if claim_class in PROMOTED_CARD_CLASSES:
        failures.append(f"{card_entry.get('id')}: canonical {status} claim cannot map to {claim_class} card class")
    if evidence_maturity in PROMOTED_MATURITY:
        failures.append(f"{card_entry.get('id')}: canonical {status} claim cannot map to {evidence_maturity} maturity")
    if validation_status in PROMOTED_VALIDATION:
        failures.append(
            f"{card_entry.get('id')}: canonical {status} claim cannot map to " f"{validation_status} validation"
        )
    return failures


def validate_claim_surfaces(
    registry: dict[str, Any],
    card_index: dict[str, Any],
    *,
    card_loader: Callable[[str], dict[str, Any]] = _default_card_loader,
) -> list[str]:
    failures, claims_by_id = validate_claim_registry(registry)

    authority = card_index.get("authority")
    if not isinstance(authority, dict):
        failures.append("card index: missing authority declaration")
    else:
        if authority.get("role") != "evidence_card_specification_index":
            failures.append("card index: role must be evidence_card_specification_index")
        if authority.get("canonical_claim_identity_and_state") != "evidence/claims.json":
            failures.append("card index: canonical claim authority must be evidence/claims.json")
        if authority.get("mapping_field") != "canonical_claim_id":
            failures.append("card index: mapping_field must be canonical_claim_id")

    card_ids: set[str] = set()
    mapped_claim_ids: set[str] = set()
    cards = card_index.get("cards")
    if not isinstance(cards, list):
        return failures + ["card index: cards must be a list"]

    for entry in cards:
        if not isinstance(entry, dict):
            failures.append("card index entry must be an object")
            continue
        card_id = entry.get("id")
        relationship = entry.get("relationship")
        canonical_claim_id = entry.get("canonical_claim_id")
        card_path = entry.get("card")

        if not isinstance(card_id, str) or not card_id:
            failures.append("card index entry missing id")
            continue
        if card_id in card_ids:
            failures.append(f"duplicate Evidence Card id: {card_id}")
        card_ids.add(card_id)

        if relationship not in CARD_RELATIONSHIPS:
            failures.append(f"{card_id}: unsupported relationship={relationship!r}")
            continue

        canonical_claim: dict[str, Any] | None = None
        if relationship == "SPECIFICATION_ONLY":
            if canonical_claim_id is not None:
                failures.append(f"{card_id}: SPECIFICATION_ONLY must have canonical_claim_id=null")
        else:
            if not isinstance(canonical_claim_id, str) or not canonical_claim_id:
                failures.append(f"{card_id}: CANONICAL_CLAIM_DETAIL requires canonical_claim_id")
            elif canonical_claim_id not in claims_by_id:
                failures.append(f"{card_id}: unknown canonical_claim_id={canonical_claim_id}")
            else:
                canonical_claim = claims_by_id[canonical_claim_id]
                if canonical_claim_id in mapped_claim_ids:
                    failures.append(f"duplicate canonical claim mapping: {canonical_claim_id}")
                mapped_claim_ids.add(canonical_claim_id)

        card: dict[str, Any] | None = None
        if not isinstance(card_path, str) or not card_path:
            failures.append(f"{card_id}: card path must be non-empty")
        elif card_path == "pending":
            if relationship == "CANONICAL_CLAIM_DETAIL":
                failures.append(f"{card_id}: mapped canonical claim cannot use pending card target")
        else:
            try:
                card = card_loader(card_path)
            except (FileNotFoundError, ValueError, OSError) as exc:
                failures.append(f"{card_id}: invalid card target {card_path}: {exc}")
            else:
                if card.get("id") != card_id:
                    failures.append(f"{card_id}: card target id mismatch: {card.get('id')!r}")
                for field in CARD_STATE_FIELDS:
                    if entry.get(field) != card.get(field):
                        failures.append(
                            f"{card_id}: index/card {field} mismatch: " f"{entry.get(field)!r} != {card.get(field)!r}"
                        )

        if canonical_claim is not None:
            failures.extend(_mapping_state_failures(canonical_claim, entry, card))

    return failures


def _production_marker_failures() -> list[str]:
    failures: list[str] = []
    pattern = re.compile(r"evidence_mode\(\s*['\"]production['\"]")
    for path in iter_sources():
        text = path.read_text(encoding="utf-8", errors="replace")
        if not pattern.search(text):
            continue
        lowered = text.lower()
        for marker in FORBIDDEN_PRODUCTION_MARKERS:
            if marker in lowered:
                failures.append(f"{path.relative_to(ROOT)}: production source contains forbidden marker {marker!r}")
    return failures


def main() -> int:
    allowed_args = {"--claim-surfaces-only"}
    unknown = set(sys.argv[1:]) - allowed_args
    if unknown:
        print(f"TRUTH-LAYER VALIDATION: FAIL\n- unsupported arguments: {sorted(unknown)}")
        return 2

    failures: list[str] = []
    try:
        registry = load_registry()
        card_index = load_card_index()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"TRUTH-LAYER VALIDATION: FAIL\n- {exc}")
        return 1

    failures.extend(validate_claim_surfaces(registry, card_index))
    if "--claim-surfaces-only" not in sys.argv[1:]:
        failures.extend(_production_marker_failures())

    if failures:
        print("TRUTH-LAYER VALIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    mapped = sum(
        1
        for card in card_index["cards"]
        if isinstance(card, dict) and card.get("relationship") == "CANONICAL_CLAIM_DETAIL"
    )
    specified = sum(
        1 for card in card_index["cards"] if isinstance(card, dict) and card.get("relationship") == "SPECIFICATION_ONLY"
    )
    print("TRUTH-LAYER VALIDATION: PASS")
    print(f"Operational claims checked: {len(registry['claims'])}")
    print(f"Evidence Cards checked: {len(card_index['cards'])} ({mapped} mapped, {specified} specification-only)")
    print("SCIENTIFIC_STATE_EFFECT=NONE")
    print("AUTHORIZATION_EFFECT=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
