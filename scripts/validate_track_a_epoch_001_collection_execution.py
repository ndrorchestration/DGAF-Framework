#!/usr/bin/env python3
"""Static fail-closed validator for the Track A Epoch 001 execution workflow.

This validator never invokes the empirical runner. It proves that the execution
workflow remains manual-only, exact-authorization-bound, single-attempt guarded,
and protected-custody preserving.
"""
from __future__ import annotations

from pathlib import Path

WORKFLOW = Path('.github/workflows/track-a-epoch-001-collection-execution.yml')
AUTH_SHA = '659aaa4dea2dd42624747952f1a47f307e69a014'
CONFIRMATION = 'COLLECT_TRACK_A_EPOCH_001'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f'TRACK_A_COLLECTION_EXECUTION_VALIDATION: FAIL: {message}')


def main() -> int:
    text = WORKFLOW.read_text(encoding='utf-8')

    # Trigger surface: empirical collection must never run from PR/push CI.
    require('workflow_dispatch:' in text, 'workflow_dispatch trigger missing')
    require('\n  push:' not in text, 'push trigger is forbidden')
    require('\n  pull_request:' not in text, 'pull_request trigger is forbidden')
    require(CONFIRMATION in text, 'explicit dispatch confirmation token missing')
    require("inputs.confirmation == 'COLLECT_TRACK_A_EPOCH_001'" in text, 'job confirmation predicate missing')

    # Exact authorization identity and history are mandatory.
    require(f'AUTHORIZATION_SHA: {AUTH_SHA}' in text, 'authorization SHA binding missing or changed')
    require('fetch-depth: 0' in text, 'full Git history checkout required')
    require('persist-credentials: false' in text, 'checkout credentials must not persist')
    require('validate_track_a_epoch_001_collection_authorization.py' in text, 'authorization validator invocation missing')
    require('TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json' in text, 'one-file authorization shape proof missing')

    # Single-attempt/durable lease controls.
    require('RELEASE_TAG: track-a-epoch-001-collection-v1' in text, 'fixed collection release identity missing')
    require('gh release view "$RELEASE_TAG"' in text, 'duplicate release refusal missing')
    require('git ls-remote --exit-code --tags' in text, 'duplicate tag refusal missing')
    require('gh release create "$RELEASE_TAG"' in text and '--draft' in text, 'restricted draft execution lease missing')

    # Fresh topology key and exact runner execution contract.
    require('openssl rand -hex 32' in text, 'fresh topology blinding key generation missing')
    require('PDMAL_MODE=track_a_epoch_001' in text, 'exact PDMAL mode missing')
    require('PDMAL_PROTOCOL_FROZEN=1' in text, 'frozen protocol assertion missing')
    require('PDMAL_TRACK_A_EPOCH_001_AUTHORIZED=1' in text, 'Track A authorization assertion missing')
    require('PDMAL_UNBLINDING_AUTHORIZED=0' in text, 'unblinding must remain disabled')
    require('PDMAL_PILOT_AUTHORIZED=0' in text, 'High-Assurance/pilot authorization must remain disabled')
    require('PDMAL_HISTORICAL_POOLING=0' in text, 'historical pooling must remain disabled')
    require('PDMAL_EPOCH_004_SUBSTITUTION=0' in text, 'Epoch-004 substitution must remain disabled')
    require('run_track_a_epoch_001.py --execute' in text, 'empirical runner invocation missing')

    # Public/protected custody must remain distinct and protected plaintext must
    # never be retained or uploaded.
    require('PDMAL_TRACK_A_PUBLIC_OUTPUT_DIR' in text, 'public output root missing')
    require('PDMAL_TRACK_A_PROTECTED_OUTPUT_DIR' in text, 'protected output root missing')
    require('PDMAL_TRACK_A_RETENTION_PASSPHRASE' in text, 'dedicated protected-retention secret missing')
    require('--symmetric --cipher-algo AES256' in text, 'protected bundle encryption missing')
    require('track-a-epoch-001-protected.tar.gz.gpg' in text, 'encrypted protected artifact missing')
    require("rm -rf \"$protected_root\"" in text, 'protected plaintext deletion missing')
    require("name 'track_a_epoch_001_mapping_*.json'" not in text, 'unexpected malformed mapping scan token')
    require("-name 'track_a_epoch_001_mapping_*.json'" in text, 'post-encryption plaintext mapping scan missing')
    require('gh release upload "$RELEASE_TAG"' in text, 'durable retention upload missing')

    upload_block = text.split('gh release upload "$RELEASE_TAG"', 1)[1]
    require('track-a-epoch-001-protected-plaintext.tar.gz' not in upload_block, 'plaintext protected archive must never be uploaded')
    require('track_a_epoch_001_mapping_' not in upload_block, 'plaintext mapping files must never be uploaded')

    # Collection workflow may validate counts/flags, but must not aggregate or
    # summarize endpoint outcomes.
    require("manifest['expected_observations'] == 2250" in text, 'fixed prospective N validation missing')
    require("manifest['outcome_aggregation_performed'] is False" in text, 'no-aggregation proof missing')
    require("manifest['unblinding_authorized'] is False" in text, 'no-unblinding proof missing')
    require('ffcr_success' not in text, 'collection workflow must not inspect endpoint outcome values')

    print('TRACK_A_COLLECTION_EXECUTION_VALIDATION: PASS')
    print(f'AUTHORIZATION_SHA={AUTH_SHA}')
    print('EMPIRICAL_EXECUTION_DURING_VALIDATION=FALSE')
    print('UNBLINDING_AUTHORIZED=FALSE')
    print('HIGH_ASSURANCE_AUTHORIZED=FALSE')
    print('SCIENTIFIC_N_INCREMENT_DURING_VALIDATION=0')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
