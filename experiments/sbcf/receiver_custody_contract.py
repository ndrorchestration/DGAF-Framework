"""Candidate custody contract for matched HTTP receiver evidence."""

from dataclasses import dataclass

_V1_DIGEST = "sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff"
_SYSTEMS = ("sbcf", "acs", "openshell")
_REQUIRED_TOP = frozenset(
    {
        "schema_version",
        "status",
        "effect_contract_digest",
        "receiver_operator",
        "raw_receipt",
        "durable_retention",
        "separation",
    }
)
_REQUIRED_OPERATOR = frozenset(
    {
        "status",
        "operator_id",
        "outside_implementation_required",
        "uncoached_required",
        "same_owner_automation_disallowed",
        "systems_under_test",
    }
)
_REQUIRED_RECEIPT = frozenset(
    {
        "required_fields",
        "integrity_algorithm",
        "raw_bytes_retained",
        "private_keys_prohibited",
        "analysis_fields_prohibited",
    }
)
_REQUIRED_RETENTION = frozenset(
    {
        "status",
        "archive_location",
        "archive_identifier",
        "retention_period",
        "access_control_owner",
        "retrieval_verification_required",
        "independent_hash_recompute_required",
    }
)
_REQUIRED_SEPARATION = frozenset(
    {
        "analysis_authorization_separate",
        "adjudication_separate",
        "independent_validation_not_implied",
    }
)
_RECEIPT_FIELDS = [
    "trial_id",
    "effect_identity_sha256",
    "observed_effect",
    "raw_record_sha256",
    "byte_count",
]


@dataclass(frozen=True)
class ReceiverCustodyReadiness:
    ready: bool
    blockers: tuple[str, ...]


def validate_receiver_custody_contract(contract: dict) -> None:
    if type(contract) is not dict or set(contract) != _REQUIRED_TOP:
        raise ValueError("invalid receiver custody schema")
    if contract["schema_version"] != "sbcf-receiver-custody-v0":
        raise ValueError("unsupported receiver custody version")
    if contract["status"] not in {"CANDIDATE_NOT_FROZEN", "FROZEN"}:
        raise ValueError("invalid receiver custody status")
    if contract["effect_contract_digest"] != _V1_DIGEST:
        raise ValueError("receiver custody contract not bound to exact v1 effect contract")

    operator = contract["receiver_operator"]
    if type(operator) is not dict or set(operator) != _REQUIRED_OPERATOR:
        raise ValueError("invalid receiver operator schema")
    if operator["status"] not in {"UNASSIGNED", "ASSIGNED"}:
        raise ValueError("invalid receiver operator status")
    if operator["operator_id"] is not None and (
        type(operator["operator_id"]) is not str or not operator["operator_id"].strip()
    ):
        raise ValueError("invalid receiver operator id")
    if operator["status"] == "UNASSIGNED" and operator["operator_id"] is not None:
        raise ValueError("unassigned receiver operator cannot have id")
    if operator["status"] == "ASSIGNED" and operator["operator_id"] is None:
        raise ValueError("assigned receiver operator requires id")
    for field in (
        "outside_implementation_required",
        "uncoached_required",
        "same_owner_automation_disallowed",
    ):
        if operator[field] is not True:
            raise ValueError(f"receiver operator requirement weakened: {field}")
    if operator["systems_under_test"] != list(_SYSTEMS):
        raise ValueError("receiver operator system scope changed")

    receipt = contract["raw_receipt"]
    if type(receipt) is not dict or set(receipt) != _REQUIRED_RECEIPT:
        raise ValueError("invalid raw receipt schema")
    if receipt["required_fields"] != _RECEIPT_FIELDS:
        raise ValueError("raw receipt required fields changed")
    if receipt["integrity_algorithm"] != "SHA-256":
        raise ValueError("unsupported receipt integrity algorithm")
    for field in ("raw_bytes_retained", "private_keys_prohibited", "analysis_fields_prohibited"):
        if receipt[field] is not True:
            raise ValueError(f"raw receipt safeguard weakened: {field}")

    retention = contract["durable_retention"]
    if type(retention) is not dict or set(retention) != _REQUIRED_RETENTION:
        raise ValueError("invalid durable retention schema")
    if retention["status"] not in {"UNRESOLVED", "FROZEN"}:
        raise ValueError("invalid durable retention status")
    optional_text = (
        "archive_location",
        "archive_identifier",
        "retention_period",
        "access_control_owner",
    )
    for field in optional_text:
        value = retention[field]
        if value is not None and (type(value) is not str or not value.strip()):
            raise ValueError(f"invalid durable retention field: {field}")
    if retention["status"] == "FROZEN" and any(retention[field] is None for field in optional_text):
        raise ValueError("frozen durable retention requires complete identity")
    if retention["retrieval_verification_required"] is not True:
        raise ValueError("durable retention must require retrieval verification")
    if retention["independent_hash_recompute_required"] is not True:
        raise ValueError("durable retention must require independent hash recompute")

    separation = contract["separation"]
    if type(separation) is not dict or set(separation) != _REQUIRED_SEPARATION:
        raise ValueError("invalid custody separation schema")
    if any(value is not True for value in separation.values()):
        raise ValueError("custody separation requirements cannot be weakened")


def evaluate_receiver_custody_contract(contract: dict) -> ReceiverCustodyReadiness:
    validate_receiver_custody_contract(contract)
    blockers = []
    if contract["status"] != "FROZEN":
        blockers.append("custody_contract_not_frozen")
    if contract["receiver_operator"]["status"] != "ASSIGNED":
        blockers.append("receiver_operator_unassigned")
    retention = contract["durable_retention"]
    if retention["status"] != "FROZEN":
        blockers.append("durable_retention_unfrozen")
    return ReceiverCustodyReadiness(not blockers, tuple(sorted(blockers)))
