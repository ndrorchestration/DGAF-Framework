from __future__ import annotations

import copy
import unittest

from mode_t_confidential_space_launch import (
    LaunchContractError,
    REQUIRED_LAUNCH_POLICIES,
    validate_launch_contract,
)

DIGEST = "sha256:" + ("1" * 64)
REFERENCE = "us-docker.pkg.dev/dgaf01/mode-t/workload@" + DIGEST


def good_config() -> dict:
    return {
        "schema_version": "dgaf-mode-t-launch-v1",
        "project_id": "dgaf01",
        "zone": "us-central1-a",
        "instance_name": "dgaf-mode-t-admission-310",
        "service_account": "modet1@dgaf01.iam.gserviceaccount.com",
        "candidate_sha": "2" * 40,
        "freeze_sha256": "3" * 64,
        "workload_image_reference": REFERENCE,
        "workload_image_digest": DIGEST,
        "confidential_compute_type": "TDX",
        "shielded_secure_boot": True,
        "maintenance_policy": "TERMINATE",
        "confidential_space_image_family": "confidential-space",
        "metadata": {
            "tee-image-reference": REFERENCE,
            "tee-restart-policy": "Never",
            "tee-container-log-redirect": "false",
            "tee-monitoring-memory-enable": "false",
        },
        "launch_policies": dict(REQUIRED_LAUNCH_POLICIES),
        "automatic_restart": False,
        "delete_on_termination": True,
        "container_logs_expected": False,
        "memory_monitoring_expected": False,
        "operational_secret_in_metadata_or_env": False,
        "synthetic_admission_only": True,
        "empirical_n": 0,
    }


class ConfidentialSpaceLaunchContractTests(unittest.TestCase):
    def assert_rejected(self, mutate) -> None:
        config = good_config()
        mutate(config)
        with self.assertRaises(LaunchContractError):
            validate_launch_contract(config)

    def test_accepts_exact_predeclared_launch_contract_without_promotion(self) -> None:
        result = validate_launch_contract(good_config())
        self.assertEqual(result["launch_contract"], "PASS_PREDECLARED_ONLY")
        self.assertFalse(result["real_gcp_configuration_verified"])
        self.assertFalse(result["real_confidential_space_admission"])
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)

    def test_is_deterministic(self) -> None:
        first = validate_launch_contract(good_config())
        second = validate_launch_contract(good_config())
        self.assertEqual(first["launch_contract_sha256"], second["launch_contract_sha256"])

    def test_rejects_debug_confidential_space_image(self) -> None:
        self.assert_rejected(lambda c: c.__setitem__("confidential_space_image_family", "confidential-space-debug"))

    def test_rejects_non_tdx(self) -> None:
        self.assert_rejected(lambda c: c.__setitem__("confidential_compute_type", "SEV"))

    def test_rejects_secure_boot_disabled(self) -> None:
        self.assert_rejected(lambda c: c.__setitem__("shielded_secure_boot", False))

    def test_rejects_mutable_image_tag(self) -> None:
        def mutate(c):
            tagged = "us-docker.pkg.dev/dgaf01/mode-t/workload:latest"
            c["workload_image_reference"] = tagged
            c["metadata"]["tee-image-reference"] = tagged
        self.assert_rejected(mutate)

    def test_rejects_digest_reference_mismatch(self) -> None:
        self.assert_rejected(lambda c: c.__setitem__("workload_image_digest", "sha256:" + ("9" * 64)))

    def test_rejects_container_log_redirect(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-container-log-redirect", "cloud_logging"))

    def test_rejects_memory_monitoring(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-monitoring-memory-enable", "true"))

    def test_rejects_restart_policy_other_than_never(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-restart-policy", "OnFailure"))

    def test_rejects_operator_command_override(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-cmd", '["/bin/sh"]'))

    def test_rejects_operator_environment_override(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-env-PDMAL_BLINDING_KEY", "forbidden"))

    def test_rejects_added_capabilities(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-added-capabilities", '["CAP_SYS_ADMIN"]'))

    def test_rejects_mounts(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-mount", "type=tmpfs,source=tmpfs,destination=/tmp"))

    def test_rejects_service_account_impersonation_metadata(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("tee-impersonate-service-accounts", "other@dgaf01.iam.gserviceaccount.com"))

    def test_rejects_relaxed_launch_policy(self) -> None:
        def mutate(c):
            c["launch_policies"]["tee.launch_policy.allow_cmd_override"] = "true"
        self.assert_rejected(mutate)

    def test_rejects_logging_launch_policy(self) -> None:
        def mutate(c):
            c["launch_policies"]["tee.launch_policy.log_redirect"] = "always"
        self.assert_rejected(mutate)

    def test_rejects_monitoring_launch_policy(self) -> None:
        def mutate(c):
            c["launch_policies"]["tee.launch_policy.monitoring_memory_allow"] = "always"
        self.assert_rejected(mutate)

    def test_rejects_unreviewed_metadata(self) -> None:
        self.assert_rejected(lambda c: c["metadata"].__setitem__("custom-key", "custom-value"))

    def test_rejects_operational_secret_declaration(self) -> None:
        self.assert_rejected(lambda c: c.__setitem__("operational_secret_in_metadata_or_env", True))

    def test_rejects_empirical_or_non_synthetic_admission(self) -> None:
        self.assert_rejected(lambda c: c.__setitem__("empirical_n", 1))
        self.assert_rejected(lambda c: c.__setitem__("synthetic_admission_only", False))

    def test_input_is_not_mutated(self) -> None:
        config = good_config()
        original = copy.deepcopy(config)
        validate_launch_contract(config)
        self.assertEqual(config, original)


if __name__ == "__main__":
    unittest.main()
