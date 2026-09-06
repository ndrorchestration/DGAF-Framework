from __future__ import annotations

import base64
import json
import unittest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from mode_t_confidential_space_attestation import (
    AttestationExpectation,
    PRE_EXECUTION,
    verify_confidential_space_attestation,
)
from mode_t_google_oidc_verifier import (
    DISCOVERY_URL,
    EXPECTED_JWKS_URI,
    FetchedDocument,
    GOOGLE_CLOUD_ATTESTATION_ISSUER,
    GoogleOIDCVerificationError,
    GoogleOIDCVerifier,
)

NOW = 1_800_000_000
C_SHA = "1" * 64
IMAGE_DIGEST = "sha256:" + ("4" * 64)
AUDIENCE = "dgaf-mode-t-admission-v1"
SUBJECT = "https://www.googleapis.com/compute/v1/projects/dgaf/zones/us-central1-a/instances/310"
SERVICE_ACCOUNTS = ("dgaf-mode-t@dgaf.iam.gserviceaccount.com",)
CONTAINER_ARGS = ("/app/dgaf-mode-t",)
ENV = {"DGAF_RUN_BINDING": "synthetic-run-310"}


def b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def uint_b64(value: int) -> str:
    return b64u(value.to_bytes((value.bit_length() + 7) // 8, "big"))


def public_jwk(private_key, kid: str, *, use: str = "sig", alg: str = "RS256") -> dict:
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "RSA",
        "kid": kid,
        "use": use,
        "alg": alg,
        "n": uint_b64(numbers.n),
        "e": uint_b64(numbers.e),
    }


def good_claims(*, issuer: str = GOOGLE_CLOUD_ATTESTATION_ISSUER) -> dict:
    return {
        "iss": issuer,
        "oemid": 11129,
        "aud": AUDIENCE,
        "sub": SUBJECT,
        "google_service_accounts": list(SERVICE_ACCOUNTS),
        "swname": "CONFIDENTIAL_SPACE",
        "hwmodel": "GCP_INTEL_TDX",
        "attester_tcb": ["INTEL"],
        "secboot": True,
        "dbgstat": "disabled-since-boot",
        "iat": NOW - 30,
        "nbf": NOW - 30,
        "exp": NOW + 300,
        "eat_nonce": [C_SHA],
        "submods": {
            "confidential_space": {
                "support_attributes": ["LATEST", "STABLE", "USABLE"],
                "monitoring_enabled": {"memory": False},
            },
            "container": {
                "image_digest": IMAGE_DIGEST,
                "args": list(CONTAINER_ARGS),
                "cmd_override": [],
                "env": dict(ENV),
                "env_override": {},
                "restart_policy": "Never",
            },
        },
    }


def sign_token(
    private_key,
    kid: str,
    claims: dict,
    *,
    algorithm_header: str = "RS256",
    extra_header: dict | None = None,
) -> str:
    header = {"alg": algorithm_header, "kid": kid, "typ": "JWT"}
    if extra_header:
        header.update(extra_header)
    header_segment = b64u(json.dumps(header, separators=(",", ":")).encode())
    payload_segment = b64u(json.dumps(claims, separators=(",", ":")).encode())
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{header_segment}.{payload_segment}.{b64u(signature)}"


class FakeGoogleKeySource:
    def __init__(self, keys: list[dict]) -> None:
        self.keys = keys
        self.discovery_issuer = GOOGLE_CLOUD_ATTESTATION_ISSUER
        self.discovery_jwks_uri = EXPECTED_JWKS_URI
        self.algorithms = ["RS256"]
        self.cache_control = "public, max-age=300"
        self.age: str | None = None
        self.fail = False
        self.final_url_override: dict[str, str] = {}
        self.status_override: dict[str, int] = {}
        self.calls: list[str] = []

    def fetch(self, url: str, timeout: float) -> FetchedDocument:
        del timeout
        self.calls.append(url)
        if self.fail:
            raise OSError("synthetic source outage")
        if url == DISCOVERY_URL:
            body = json.dumps(
                {
                    "issuer": self.discovery_issuer,
                    "jwks_uri": self.discovery_jwks_uri,
                    "id_token_signing_alg_values_supported": self.algorithms,
                },
                separators=(",", ":"),
            ).encode()
            headers = {"cache-control": "no-store"}
        elif url == EXPECTED_JWKS_URI:
            body = json.dumps({"keys": self.keys}, separators=(",", ":")).encode()
            headers = {"cache-control": self.cache_control}
            if self.age is not None:
                headers["age"] = self.age
        else:
            raise OSError(f"unexpected URL {url}")
        return FetchedDocument(
            requested_url=url,
            final_url=self.final_url_override.get(url, url),
            status=self.status_override.get(url, 200),
            body=body,
            headers=headers,
        )


class GoogleOIDCVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key1 = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.key2 = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def make(self, *, key=None, kid: str = "kid-1"):
        key = key or self.key1
        source = FakeGoogleKeySource([public_jwk(key, kid)])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        token = sign_token(key, kid, good_claims())
        return source, verifier, token

    def assert_rejected(self, verifier: GoogleOIDCVerifier, token: str, *, now: int = NOW):
        with self.assertRaises(GoogleOIDCVerificationError):
            verifier.verify(token, verified_at_unix=now)

    def test_accepts_authenticated_rs256_and_retains_key_source_provenance(self) -> None:
        source, verifier, token = self.make()
        verified = verifier.verify(token, verified_at_unix=NOW)
        self.assertTrue(verified.token_context.signature_verified)
        self.assertEqual(verified.claims["iss"], GOOGLE_CLOUD_ATTESTATION_ISSUER)
        self.assertEqual(verified.key_source.discovery_url, DISCOVERY_URL)
        self.assertEqual(verified.key_source.jwks_uri, EXPECTED_JWKS_URI)
        self.assertEqual(verified.key_source.kid, "kid-1")
        self.assertEqual(verified.key_source.algorithm, "RS256")
        self.assertEqual(
            verified.key_source.transport_authentication,
            "HTTPS_SYSTEM_CA_HOSTNAME_VERIFIED",
        )
        self.assertEqual(source.calls, [DISCOVERY_URL, EXPECTED_JWKS_URI])
        evidence = verified.evidence()
        self.assertNotIn("token", evidence)
        self.assertFalse(evidence["pilot_authorized"])
        self.assertEqual(evidence["empirical_n"], 0)

    def test_authenticated_signature_result_feeds_current_pre_execution_contract(self) -> None:
        _, verifier, token = self.make()
        verified = verifier.verify(token, verified_at_unix=NOW)
        result = verify_confidential_space_attestation(
            verified.claims,
            AttestationExpectation(
                phase=PRE_EXECUTION,
                audience=AUDIENCE,
                subject=SUBJECT,
                expected_service_accounts=SERVICE_ACCOUNTS,
                image_digest=IMAGE_DIGEST,
                binding_sha256=C_SHA,
                expected_args=CONTAINER_ARGS,
                expected_env=ENV,
            ),
            verified.token_context,
        )
        self.assertEqual(result["attestation_contract"], "PASS")
        self.assertEqual(result["attestation_phase"], PRE_EXECUTION)
        self.assertEqual(result["authorization_consumption_sha256"], C_SHA)
        self.assertIsNone(result["output_manifest_sha256"])

    def test_rejects_altered_signature(self) -> None:
        _, verifier, token = self.make()
        h, p, s = token.split(".")
        signature = bytearray(base64.urlsafe_b64decode(s + "=" * (-len(s) % 4)))
        signature[0] ^= 1
        self.assert_rejected(verifier, f"{h}.{p}.{b64u(bytes(signature))}")

    def test_rejects_algorithm_confusion(self) -> None:
        source = FakeGoogleKeySource([public_jwk(self.key1, "kid-1")])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        token = sign_token(self.key1, "kid-1", good_claims(), algorithm_header="HS256")
        self.assert_rejected(verifier, token)
        self.assertEqual(source.calls, [])

    def test_rejects_jwt_supplied_key_source(self) -> None:
        _, verifier, _ = self.make()
        token = sign_token(
            self.key1,
            "kid-1",
            good_claims(),
            extra_header={"jku": "https://attacker.invalid/jwks.json"},
        )
        self.assert_rejected(verifier, token)

    def test_rejects_wrong_signed_issuer(self) -> None:
        source = FakeGoogleKeySource([public_jwk(self.key1, "kid-1")])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        token = sign_token(self.key1, "kid-1", good_claims(issuer="https://example.invalid"))
        self.assert_rejected(verifier, token)

    def test_rejects_expired_signed_token(self) -> None:
        source = FakeGoogleKeySource([public_jwk(self.key1, "kid-1")])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        claims = good_claims()
        claims["iat"] = NOW - 600
        claims["nbf"] = NOW - 600
        claims["exp"] = NOW - 61
        self.assert_rejected(verifier, sign_token(self.key1, "kid-1", claims))

    def test_rejects_discovery_issuer_substitution(self) -> None:
        source, verifier, token = self.make()
        source.discovery_issuer = "https://example.invalid"
        self.assert_rejected(verifier, token)

    def test_rejects_discovery_jwks_uri_substitution(self) -> None:
        source, verifier, token = self.make()
        source.discovery_jwks_uri = "https://attacker.invalid/jwks.json"
        self.assert_rejected(verifier, token)
        self.assertEqual(source.calls, [DISCOVERY_URL])

    def test_rejects_malformed_discovery_algorithm_metadata(self) -> None:
        source, verifier, token = self.make()
        source.algorithms = None  # type: ignore[assignment]
        self.assert_rejected(verifier, token)

    def test_rejects_redirected_authenticated_source(self) -> None:
        source, verifier, token = self.make()
        source.final_url_override[DISCOVERY_URL] = "https://example.invalid/discovery"
        self.assert_rejected(verifier, token)

    def test_rejects_duplicate_kid(self) -> None:
        source = FakeGoogleKeySource(
            [public_jwk(self.key1, "same"), public_jwk(self.key2, "same")]
        )
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        self.assert_rejected(verifier, sign_token(self.key1, "same", good_claims()))

    def test_authenticated_rotation_refreshes_once_for_new_kid(self) -> None:
        source = FakeGoogleKeySource([public_jwk(self.key1, "old")])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        verifier.verify(sign_token(self.key1, "old", good_claims()), verified_at_unix=NOW)
        source.keys = [public_jwk(self.key2, "new")]
        verified = verifier.verify(
            sign_token(self.key2, "new", good_claims()),
            verified_at_unix=NOW + 1,
        )
        self.assertEqual(verified.key_source.kid, "new")
        self.assertEqual(
            source.calls,
            [DISCOVERY_URL, EXPECTED_JWKS_URI, DISCOVERY_URL, EXPECTED_JWKS_URI],
        )

    def test_unknown_kid_and_refresh_outage_fail_closed(self) -> None:
        source = FakeGoogleKeySource([public_jwk(self.key1, "old")])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        verifier.verify(sign_token(self.key1, "old", good_claims()), verified_at_unix=NOW)
        source.fail = True
        self.assert_rejected(
            verifier,
            sign_token(self.key2, "new", good_claims()),
            now=NOW + 1,
        )

    def test_valid_cache_survives_outage_only_until_expiry(self) -> None:
        source, verifier, token = self.make()
        verifier.verify(token, verified_at_unix=NOW)
        source.fail = True
        verifier.verify(token, verified_at_unix=NOW + 299)
        self.assert_rejected(verifier, token, now=NOW + 300)

    def test_age_header_reduces_cache_lifetime(self) -> None:
        source, verifier, token = self.make()
        source.age = "250"
        verifier.verify(token, verified_at_unix=NOW)
        source.fail = True
        verifier.verify(token, verified_at_unix=NOW + 49)
        self.assert_rejected(verifier, token, now=NOW + 50)

    def test_rejects_jwk_not_restricted_to_signature_use(self) -> None:
        source = FakeGoogleKeySource([public_jwk(self.key1, "kid-1", use="enc")])
        verifier = GoogleOIDCVerifier(fetcher=source.fetch)
        self.assert_rejected(verifier, sign_token(self.key1, "kid-1", good_claims()))


if __name__ == "__main__":
    unittest.main()
