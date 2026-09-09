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
from pathlib import Path
from typing import Any, Callable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by CI environment setup
    raise SystemExit("PyYAML is required for claim-surface reconciliation") from exc

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


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ValueError("evidence/claims.json must contain a top-level claims list")
    return data


def load_card_index(path: Path = CARD_INDEX) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("cards"), list):
        raise ValueError("CLAIM_CARD_INDEX.yaml must contain a top-level cards list")
    return data


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


def _default_card_loader(card_path: str) -> dict[str, Any]:
    path = (ROOT / card_path).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"card path escapes repository root: {card_path}") from exc
    if not path.is_file():
        raise FileNotFoundError(card_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"card is not an object: {card_path}")
    return data


def _mapping_state_failures(
    canonical_claim: dict[str, Any],
    card_entry: dict[str, Any],
    card: dict[str, Any] | None,
) -> list[str]:
    failures: list[str] = []
    status = canonical_claim.get("status")
    if status not in {"HYPOTHESIS", "BLOCKED"}:
        return failures

    claim_class = (card or card_entry).get("claim_class")
    evidence_maturity = (card or card_entry).get("evidence_maturity")
    validation_status = (card or card_entry).get("validation_status")
    if claim_class in PROMOTED_CARD_CLASSES:
        failures.append(
            f"{card_entry.get('id')}: canonical {status} claim cannot be mapped to {claim_class} card class"
        )
    if evidence_maturity in PROMOTED_MATURITY:
        failures.append(
            f"{card_entry.get('id')}: canonical {status} claim cannot be mapped to {evidence_maturity} maturity"
        )
    if validation_status in PROMOTED_VALIDATION:
        failures.append(
            f"{card_entry.get('id')}: canonical {status} claim cannot be mapped to {validation_status} validation"
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
    for entry in card_index.get("cards", []):
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
                failures.append(f"{card_id}: unmapped canonical_claim_id={canonical_claim_id}")
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
                for field in ("claim_class", "evidence_maturity", "validation_status"):
                    if entry.get(field) != card.get(field):
                        failures.append(
                            f"{card_id}: index/card {field} mismatch: {entry.get(field)!r} != {card.get(field)!r}"
                        )

        if canonical_claim is not None:
            failures.extend(_mapping_state_failures(canonical_claim, entry, card))

    return failures


def main() -> int:
    failures: list[str] = []
    registry = load_registry()
    card_index = load_card_index()
    failures.extend(validate_claim_surfaces(registry, card_index))

    # Guard explicit production annotations against obvious stubs/placeholders.
    pattern = re.compile(r"evidence_mode\(\s*['\"]production['\"]")
    for path in iter_sources():
        text = path.read_text(encoding="utf-8", errors="replace")
        if not pattern.search(text):
            continue
        lowered = text.lower()
        for marker in FORBIDDEN_PRODUCTION_MARKERS:
            if marker in lowered:
                failures.append(f"{path.relative_to(ROOT)}: production source contains forbidden marker {marker!r}")

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
        1
        for card in card_index["cards"]
        if isinstance(card, dict) and card.get("relationship") == "SPECIFICATION_ONLY"
    )
    print("TRUTH-LAYER VALIDATION: PASS")
    print(f"Operational claims checked: {len(registry['claims'])}")
    print(f"Evidence Cards checked: {len(card_index['cards'])} ({mapped} mapped, {specified} specification-only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
