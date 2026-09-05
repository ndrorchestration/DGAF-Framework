import pytest

from scripts import validate_p4_mode_t_preconditions as guard

SHA40 = "a" * 40
SHA64 = "b" * 64
CHAIN = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"


def _payload():
    return {
        "github_run_id": 123456,
        "github_run_attempt": 1,
        "authorization_run_id": 123456,
        "authorization_attempt": 1,
        "github_sha": SHA40,
        "expected_github_sha": SHA40,
        "workflow_sha256": SHA64,
        "expected_workflow_sha256": SHA64,
        "helper_sha256": "c" * 64,
        "expected_helper_sha256": "c" * 64,
        "runner_class": "github-hosted-standard-vm",
        "debug_enabled": False,
        "timelock_chain_hash": CHAIN,
        "expected_timelock_chain_hash": CHAIN,
        "strict_chain_binding": True,
        "current_round": 1000,
        "release_round": 2000,
        "minimum_round_gap": 500,
        "p6_retention_status": "RESERVATION_AND_AUTHORIZATION_RETAINED",
        "authorization_status": "GRANTED_FOR_EXACT_RESERVED_RUN",
    }


def test_valid_public_preconditions_pass_without_secret_instantiation():
    result = guard.validate_preconditions(_payload())
    assert result["result"] == "PASS"
    assert result["secret_instantiation"] == "NOT_PERFORMED_BY_THIS_VALIDATOR"
    assert result["empirical_execution"] == "NOT_PERFORMED_BY_THIS_VALIDATOR"


def test_rerun_attempt_fails_closed():
    payload = _payload()
    payload["github_run_attempt"] = 2
    with pytest.raises(guard.ModeTPreconditionError, match="reruns fail closed"):
        guard.validate_preconditions(payload)


def test_authorization_cannot_transfer_to_another_run():
    payload = _payload()
    payload["authorization_run_id"] = 999999
    with pytest.raises(guard.ModeTPreconditionError, match="different GitHub run ID"):
        guard.validate_preconditions(payload)


def test_authorization_cannot_allow_rerun_attempt():
    payload = _payload()
    payload["authorization_attempt"] = 2
    with pytest.raises(guard.ModeTPreconditionError, match="authorization_attempt must equal 1"):
        guard.validate_preconditions(payload)


def test_runtime_sha_substitution_fails_closed():
    payload = _payload()
    payload["github_sha"] = "d" * 40
    with pytest.raises(guard.ModeTPreconditionError, match="GitHub SHA differs"):
        guard.validate_preconditions(payload)


def test_workflow_substitution_fails_closed():
    payload = _payload()
    payload["workflow_sha256"] = "d" * 64
    with pytest.raises(guard.ModeTPreconditionError, match="workflow digest differs"):
        guard.validate_preconditions(payload)


def test_helper_substitution_fails_closed():
    payload = _payload()
    payload["helper_sha256"] = "d" * 64
    with pytest.raises(guard.ModeTPreconditionError, match="helper digest differs"):
        guard.validate_preconditions(payload)


def test_debug_mode_fails_closed():
    payload = _payload()
    payload["debug_enabled"] = True
    with pytest.raises(guard.ModeTPreconditionError, match="debug mode"):
        guard.validate_preconditions(payload)


def test_nonstandard_runner_class_fails_closed():
    payload = _payload()
    payload["runner_class"] = "self-hosted"
    with pytest.raises(guard.ModeTPreconditionError, match="runner_class"):
        guard.validate_preconditions(payload)


def test_chain_substitution_fails_closed():
    payload = _payload()
    payload["timelock_chain_hash"] = "d" * 64
    with pytest.raises(guard.ModeTPreconditionError, match="chain hash differs"):
        guard.validate_preconditions(payload)


def test_non_strict_chain_binding_fails_closed():
    payload = _payload()
    payload["strict_chain_binding"] = False
    with pytest.raises(guard.ModeTPreconditionError, match="strict timelock chain binding"):
        guard.validate_preconditions(payload)


def test_past_release_round_fails_closed():
    payload = _payload()
    payload["release_round"] = payload["current_round"]
    with pytest.raises(guard.ModeTPreconditionError, match="must be in the future"):
        guard.validate_preconditions(payload)


def test_too_near_release_round_fails_closed():
    payload = _payload()
    payload["release_round"] = 1200
    with pytest.raises(guard.ModeTPreconditionError, match="minimum round gap"):
        guard.validate_preconditions(payload)


def test_missing_independent_retention_fails_closed():
    payload = _payload()
    payload["p6_retention_status"] = "NOT_RETAINED"
    with pytest.raises(guard.ModeTPreconditionError, match="P6"):
        guard.validate_preconditions(payload)


def test_generic_authorization_is_not_enough():
    payload = _payload()
    payload["authorization_status"] = "GRANTED"
    with pytest.raises(guard.ModeTPreconditionError, match="exact-run pilot authorization"):
        guard.validate_preconditions(payload)


@pytest.mark.parametrize(
    "forbidden_key",
    [
        "raw_blinding_key",
        "cleartext_mapping",
        "key_commitment_nonce",
        "mapping_commitment_nonce",
        "recovery_seed",
        "recovery_phrase",
        "plaintext_release_bundle",
    ],
)
def test_protected_material_fields_are_rejected_even_when_nested(forbidden_key):
    payload = _payload()
    payload["nested"] = {"deeper": {forbidden_key: "synthetic-canary"}}
    with pytest.raises(guard.ModeTPreconditionError, match="forbidden protected-material field"):
        guard.validate_preconditions(payload)
