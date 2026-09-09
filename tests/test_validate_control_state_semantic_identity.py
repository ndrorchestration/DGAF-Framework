from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_control_state as validator

EXPECTED_SHA = "2a54a67d84870e4eeb71b8aaf04413e0ca492ba1"
OTHER_SHA = "0" * 40


@pytest.mark.parametrize("path", list(validator.CONTROL_DOCS))
def test_live_control_documents_bind_semantic_apparatus_identity(path: str) -> None:
    text = (validator.ROOT / path).read_text(encoding="utf-8")
    assert validator.semantic_apparatus_source(path, text) == EXPECTED_SHA


def test_current_state_historical_occurrence_cannot_mask_wrong_authoritative_field() -> None:
    path = "docs/CURRENT_STATE.md"
    text = f"""# Current State

## Canonical High-Assurance provenance boundary

- apparatus source: `{OTHER_SHA}`
- apparatus source tree: `{'1' * 40}`

## Historical notes

Prior apparatus source: `{EXPECTED_SHA}`
"""

    with pytest.raises(AssertionError, match="does not match manifest apparatus source"):
        validator.assert_semantic_apparatus_binding(path, text, EXPECTED_SHA)


def test_claim_index_historical_occurrence_cannot_mask_wrong_top_metadata() -> None:
    path = "docs/CLAIM_EVIDENCE_INDEX.md"
    text = f"""# Claim / Evidence Index

**Corrected apparatus source:** `{OTHER_SHA}`

> **Reconciliation notice:** current authority follows exact evidence scope.

## Historical runtime-evidence binding

- Corrected apparatus source: `{EXPECTED_SHA}`
"""

    with pytest.raises(AssertionError, match="does not match manifest apparatus source"):
        validator.assert_semantic_apparatus_binding(path, text, EXPECTED_SHA)


def test_duplicate_authoritative_frontmatter_field_fails_closed() -> None:
    path = "docs/experiment/FREEZE_MANIFEST.md"
    text = f"""---
corrected_apparatus_source_sha: {EXPECTED_SHA}
corrected_apparatus_source_sha: {OTHER_SHA}
---

# Freeze Manifest
"""

    with pytest.raises(AssertionError, match="expected exactly one authoritative corrected_apparatus_source_sha"):
        validator.semantic_apparatus_source(path, text)


def test_manifest_identity_is_scoped_to_authoritative_yaml_block() -> None:
    path = "docs/experiment/NEW_CANDIDATE_MANIFEST.md"
    text = f"""# Manifest

Historical apparatus_source_sha: {OTHER_SHA}

```yaml
apparatus_source_sha: {EXPECTED_SHA}
apparatus_source_tree_sha: {'2' * 40}

deployment_binding:
  deployment_id: NONE
  deployment_url: NONE
  source_sha_match: NONE
```
"""

    identity = validator.manifest_identity(text)
    assert identity["apparatus_source_sha"] == EXPECTED_SHA
    assert identity["apparatus_source_tree_sha"] == "2" * 40


def test_unknown_control_surface_has_no_substring_fallback() -> None:
    path = "docs/UNKNOWN.md"
    text = f"historical apparatus {EXPECTED_SHA}\n"

    with pytest.raises(AssertionError, match="no semantic apparatus-source parser is defined"):
        validator.semantic_apparatus_source(path, text)
