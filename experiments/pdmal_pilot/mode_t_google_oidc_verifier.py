"""Fail-closed Google OIDC signature verification for DGAF Mode-T attestation.

The verifier trusts only the reviewed Google Cloud Attestation discovery endpoint,
requires its issuer and JWKS URI to match exact reviewed values, rejects redirects
and JWT-supplied key locations, handles normal ``kid`` rotation by one authenticated
refresh, never uses an expired key cache, and records non-secret source digests.

Success authenticates the JWT signature and Google issuer only. The separate
Confidential Space claim contract still decides workload admission; this module does
not establish P4 custody, freeze, authorization, or empirical evidence.
"""
from __future__ import annotations

import base64
from dataclasses import asdict, dataclass
import hashlib
import json
import re
import ssl
import time
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPSHandler, HTTPRedirectHandler, Request, build_opener

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from mode_t_confidential_space_attestation import (
    GOOGLE_CLOUD_ATTESTATION_ISSUER,
    VerifiedTokenContext,
)

DISCOVERY_URL = GOOGLE_CLOUD_ATTESTATION_ISSUER + "/.well-known/openid-configuration"
EXPECTED_JWKS_URI = (
    "https://www.googleapis.com/service_accounts/v1/metadata/jwk/"
    "signer@confidentialspace-sign.iam.gserviceaccount.com"
)
EXPECTED_ALGORITHM = "RS256"
PRODUCTION_TRANSPORT = "HTTPS_SYSTEM_CA_HOSTNAME_VERIFIED"
SYNTHETIC_TRANSPORT = "SYNTHETIC_INJECTED_FETCHER"
MAX_DOCUMENT_BYTES = 1_048_576
MAX_TOKEN_BYTES = 262_144
DEFAULT_CACHE_TTL_SECONDS = 300
MAX_CACHE_TTL_SECONDS = 3600
DEFAULT_HTTP_TIMEOUT_SECONDS = 5.0
_B64URL_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class GoogleOIDCVerificationError(ValueError):
    """Raised when Google OIDC key authentication or JWT verification fails."""


@dataclass(frozen=True)
class FetchedDocument:
    requested_url: str
    final_url: str
    status: int
    body: bytes
    headers: Mapping[str, str]


@dataclass(frozen=True)
class KeySourceProvenance:
    discovery_url: str
    jwks_uri: str
    discovery_sha256: str
    jwks_sha256: str
    fetched_at_unix: int
    expires_at_unix: int
    kid: str
    jwk_sha256: str
    transport_authentication: str
    algorithm: str = EXPECTED_ALGORITHM


@dataclass(frozen=True)
class VerifiedGoogleOIDCToken:
    claims: Mapping[str, Any]
    token_context: VerifiedTokenContext
    key_source: KeySourceProvenance

    def evidence(self) -> dict[str, Any]:
        """Return retention-safe verification evidence; never include token/key bytes."""
        production_key_source = self.key_source.transport_authentication == PRODUCTION_TRANSPORT
        return {
            "token_sha256": self.token_context.token_sha256,
            "signature_verified": self.token_context.signature_verified,
            "verified_at_unix": self.token_context.verified_at_unix,
            "key_source": asdict(self.key_source),
            "production_key_source_authenticated": production_key_source,
            "freeze_established": False,
            "pilot_authorized": False,
            "empirical_data_collection": False,
            "empirical_n": 0,
        }


@dataclass(frozen=True)
class _KeyRecord:
    public_key: rsa.RSAPublicKey
    jwk_sha256: str


@dataclass(frozen=True)
class _KeyCache:
    keys: Mapping[str, _KeyRecord]
    discovery_sha256: str
    jwks_sha256: str
    fetched_at_unix: int
    expires_at_unix: int


def _fail(message: str) -> GoogleOIDCVerificationError:
    return GoogleOIDCVerificationError(message)


def _b64u(value: Any, label: str) -> bytes:
    if not isinstance(value, str) or not value or "=" in value:
        raise _fail(f"{label} must be non-empty unpadded base64url")
    if _B64URL_RE.fullmatch(value) is None or len(value) % 4 == 1:
        raise _fail(f"{label} is not canonical base64url")
    try:
        raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except Exception as exc:
        raise _fail(f"{label} is not valid base64url") from exc
    canonical = base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
    if canonical != value:
        raise _fail(f"{label} is not canonical base64url")
    return raw


def _uint(value: Any, label: str) -> int:
    raw = _b64u(value, label)
    if not raw:
        raise _fail(f"{label} is empty")
    return int.from_bytes(raw, "big")


def _json(raw: bytes, label: str) -> Any:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _fail(f"{label} is not UTF-8") from exc

    def no_dupes(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise _fail(f"{label} contains duplicate key {key!r}")
            out[key] = value
        return out

    try:
        return json.loads(text, object_pairs_hook=no_dupes)
    except GoogleOIDCVerificationError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise _fail(f"{label} is not valid JSON") from exc


def _canonical_digest(value: Mapping[str, Any]) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for key, value in headers.items():
        if str(key).lower() == name.lower():
            return str(value)
    return None


def _ttl(headers: Mapping[str, str]) -> int:
    control = (_header(headers, "cache-control") or "").lower()
    if "no-store" in control or "no-cache" in control:
        return 0
    ttl = DEFAULT_CACHE_TTL_SECONDS
    for item in control.split(","):
        item = item.strip()
        if item.startswith("max-age="):
            try:
                ttl = int(item.split("=", 1)[1].strip().strip('"'))
            except ValueError as exc:
                raise _fail("JWKS max-age is malformed") from exc
            if ttl < 0:
                raise _fail("JWKS max-age is negative")
            break
    age_raw = _header(headers, "age")
    if age_raw is not None:
        try:
            age = int(age_raw)
        except ValueError as exc:
            raise _fail("JWKS Age is malformed") from exc
        if age < 0:
            raise _fail("JWKS Age is negative")
        ttl = max(0, ttl - age)
    return min(ttl, MAX_CACHE_TTL_SECONDS)


def _exact_https(url: str, host: str, path: str, label: str) -> None:
    p = urlparse(url)
    if (
        p.scheme != "https"
        or p.hostname != host
        or p.port not in (None, 443)
        or p.path != path
        or p.params
        or p.query
        or p.fragment
        or p.username is not None
        or p.password is not None
    ):
        raise _fail(f"{label} is outside the reviewed Google HTTPS endpoint")


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _https_fetch(url: str, timeout: float) -> FetchedDocument:
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "DGAF-ModeT-OIDC/1"},
        method="GET",
    )
    opener = build_opener(HTTPSHandler(context=ssl.create_default_context()), _NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            return FetchedDocument(
                url,
                response.geturl(),
                int(response.status),
                response.read(MAX_DOCUMENT_BYTES + 1),
                dict(response.headers.items()),
            )
    except HTTPError as exc:
        if 300 <= exc.code < 400:
            raise _fail(f"HTTPS redirect is forbidden for {url}") from exc
        raise _fail(f"HTTPS fetch returned {exc.code} for {url}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise _fail(f"HTTPS fetch failed for {url}") from exc


def _document(doc: FetchedDocument, expected: str, label: str) -> bytes:
    if doc.requested_url != expected or doc.final_url != expected:
        raise _fail(f"{label} URL/redirect mismatch")
    if doc.status != 200:
        raise _fail(f"{label} returned HTTP {doc.status}")
    if not doc.body or len(doc.body) > MAX_DOCUMENT_BYTES:
        raise _fail(f"{label} is empty or oversized")
    return doc.body


def _jwk(item: Any) -> tuple[str, _KeyRecord]:
    if not isinstance(item, Mapping):
        raise _fail("JWKS key must be an object")
    kid = item.get("kid")
    if not isinstance(kid, str) or not kid:
        raise _fail("JWKS key has no kid")
    if item.get("kty") != "RSA":
        raise _fail(f"JWKS key {kid!r} is not RSA")
    if item.get("use") != "sig":
        raise _fail(f"JWKS key {kid!r} is not restricted to signature use")
    if item.get("alg") != EXPECTED_ALGORITHM:
        raise _fail(f"JWKS key {kid!r} is not restricted to RS256")
    n = _uint(item.get("n"), f"JWK {kid} n")
    e = _uint(item.get("e"), f"JWK {kid} e")
    if e < 3 or e % 2 == 0:
        raise _fail(f"JWK {kid!r} has invalid exponent")
    try:
        key = rsa.RSAPublicNumbers(e, n).public_key()
    except (TypeError, ValueError) as exc:
        raise _fail(f"JWK {kid!r} is invalid RSA") from exc
    if not 2048 <= key.key_size <= 8192:
        raise _fail(f"JWK {kid!r} has unacceptable RSA key size")
    return kid, _KeyRecord(key, _canonical_digest(dict(item)))


class GoogleOIDCVerifier:
    """Stateful verifier supporting bounded authenticated JWKS caching and rotation.

    Passing ``fetcher`` is a synthetic-test seam. Evidence from that path is
    explicitly marked synthetic and cannot claim production HTTPS provenance.
    """

    def __init__(
        self,
        *,
        fetcher: Callable[[str, float], FetchedDocument] | None = None,
        timeout_seconds: float = DEFAULT_HTTP_TIMEOUT_SECONDS,
        max_clock_skew_seconds: int = 60,
    ) -> None:
        if timeout_seconds <= 0 or max_clock_skew_seconds < 0:
            raise _fail("invalid verifier timing policy")
        if fetcher is None:
            self._fetcher = _https_fetch
            self._transport_authentication = PRODUCTION_TRANSPORT
        else:
            self._fetcher = fetcher
            self._transport_authentication = SYNTHETIC_TRANSPORT
        self._timeout = timeout_seconds
        self._skew = max_clock_skew_seconds
        self._cache: _KeyCache | None = None

    def _fetch(self, url: str) -> FetchedDocument:
        try:
            result = self._fetcher(url, self._timeout)
        except GoogleOIDCVerificationError:
            raise
        except Exception as exc:
            raise _fail(f"key-source fetch failed for {url}") from exc
        if not isinstance(result, FetchedDocument):
            raise _fail("key-source fetcher returned invalid document")
        return result

    def _refresh(self, now: int) -> _KeyCache:
        _exact_https(
            DISCOVERY_URL,
            "confidentialcomputing.googleapis.com",
            "/.well-known/openid-configuration",
            "discovery",
        )
        d_raw = _document(self._fetch(DISCOVERY_URL), DISCOVERY_URL, "discovery")
        discovery = _json(d_raw, "discovery")
        if not isinstance(discovery, Mapping):
            raise _fail("discovery must be an object")
        if discovery.get("issuer") != GOOGLE_CLOUD_ATTESTATION_ISSUER:
            raise _fail("discovery issuer mismatch")
        algorithms = discovery.get("id_token_signing_alg_values_supported")
        if not isinstance(algorithms, list) or not all(
            isinstance(item, str) for item in algorithms
        ):
            raise _fail("discovery signing algorithms must be a list of strings")
        if EXPECTED_ALGORITHM not in algorithms:
            raise _fail("discovery does not advertise RS256")
        uri = discovery.get("jwks_uri")
        if uri != EXPECTED_JWKS_URI:
            raise _fail("discovery JWKS URI changed from reviewed endpoint")
        _exact_https(
            uri,
            "www.googleapis.com",
            "/service_accounts/v1/metadata/jwk/"
            "signer@confidentialspace-sign.iam.gserviceaccount.com",
            "JWKS",
        )
        j_doc = self._fetch(uri)
        j_raw = _document(j_doc, uri, "JWKS")
        jwks = _json(j_raw, "JWKS")
        if (
            not isinstance(jwks, Mapping)
            or not isinstance(jwks.get("keys"), list)
            or not jwks["keys"]
        ):
            raise _fail("JWKS must contain keys")
        keys: dict[str, _KeyRecord] = {}
        for item in jwks["keys"]:
            kid, record = _jwk(item)
            if kid in keys:
                raise _fail(f"JWKS contains duplicate kid {kid!r}")
            keys[kid] = record
        cache = _KeyCache(
            keys=keys,
            discovery_sha256=hashlib.sha256(d_raw).hexdigest(),
            jwks_sha256=hashlib.sha256(j_raw).hexdigest(),
            fetched_at_unix=now,
            expires_at_unix=now + _ttl(j_doc.headers),
        )
        self._cache = cache
        return cache

    def _key(self, kid: str, now: int) -> tuple[_KeyRecord, _KeyCache]:
        cache = self._cache
        if cache is None or now >= cache.expires_at_unix:
            cache = self._refresh(now)
        record = cache.keys.get(kid)
        if record is not None:
            return record, cache
        # A missing kid can be normal Google rotation. Refresh exactly once from
        # the authenticated source, then fail if the requested key is still absent.
        cache = self._refresh(now)
        record = cache.keys.get(kid)
        if record is None:
            raise _fail(f"JWT kid {kid!r} absent from refreshed Google JWKS")
        return record, cache

    def verify(
        self,
        token: str | bytes,
        *,
        verified_at_unix: int | None = None,
    ) -> VerifiedGoogleOIDCToken:
        now = int(time.time()) if verified_at_unix is None else verified_at_unix
        if not isinstance(now, int) or isinstance(now, bool) or now < 0:
            raise _fail("verified_at_unix must be a non-negative integer")
        if isinstance(token, str):
            try:
                raw_token = token.encode("ascii")
            except UnicodeEncodeError as exc:
                raise _fail("JWT must be ASCII") from exc
        elif isinstance(token, bytes):
            raw_token = token
        else:
            raise _fail("JWT must be str or bytes")
        if len(raw_token) > MAX_TOKEN_BYTES:
            raise _fail("JWT is oversized")
        try:
            compact = raw_token.decode("ascii")
        except UnicodeDecodeError as exc:
            raise _fail("JWT must be ASCII") from exc
        parts = compact.split(".")
        if len(parts) != 3 or any(not part for part in parts):
            raise _fail("JWT compact serialization is malformed")
        h_seg, p_seg, s_seg = parts
        header = _json(_b64u(h_seg, "JWT header"), "JWT header")
        if not isinstance(header, Mapping) or header.get("alg") != EXPECTED_ALGORITHM:
            raise _fail("JWT alg must be exactly RS256")
        if header.get("typ") not in (None, "JWT"):
            raise _fail("JWT typ must be JWT when present")
        kid = header.get("kid")
        if not isinstance(kid, str) or not kid:
            raise _fail("JWT kid is missing")
        if any(name in header for name in ("jku", "jwk", "x5u", "crit")):
            raise _fail("JWT header contains forbidden key source or critical extension")

        record, cache = self._key(kid, now)
        try:
            record.public_key.verify(
                _b64u(s_seg, "JWT signature"),
                f"{h_seg}.{p_seg}".encode("ascii"),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except InvalidSignature as exc:
            raise _fail("JWT signature verification failed") from exc
        except Exception as exc:
            raise _fail("JWT cryptographic verification failed") from exc

        claims = _json(_b64u(p_seg, "JWT payload"), "JWT payload")
        if (
            not isinstance(claims, Mapping)
            or claims.get("iss") != GOOGLE_CLOUD_ATTESTATION_ISSUER
        ):
            raise _fail("signed JWT issuer is not Google Cloud Attestation")

        def timestamp(name: str) -> int:
            value = claims.get(name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise _fail(f"signed JWT {name} must be an integer")
            return value

        iat = timestamp("iat")
        nbf = timestamp("nbf")
        exp = timestamp("exp")
        if iat > now + self._skew or nbf > now + self._skew:
            raise _fail("signed JWT is future/not-yet-valid beyond allowed skew")
        if exp <= now - self._skew:
            raise _fail("signed JWT is expired")
        if exp <= iat or exp <= nbf:
            raise _fail("signed JWT time interval is invalid")

        token_sha = hashlib.sha256(raw_token).hexdigest()
        return VerifiedGoogleOIDCToken(
            claims=dict(claims),
            token_context=VerifiedTokenContext(True, token_sha, now),
            key_source=KeySourceProvenance(
                discovery_url=DISCOVERY_URL,
                jwks_uri=EXPECTED_JWKS_URI,
                discovery_sha256=cache.discovery_sha256,
                jwks_sha256=cache.jwks_sha256,
                fetched_at_unix=cache.fetched_at_unix,
                expires_at_unix=cache.expires_at_unix,
                kid=kid,
                jwk_sha256=record.jwk_sha256,
                transport_authentication=self._transport_authentication,
            ),
        )


def verify_google_confidential_space_token(token: str | bytes) -> VerifiedGoogleOIDCToken:
    """Production trust entry point using authenticated HTTPS and the system clock.

    Tests may instantiate ``GoogleOIDCVerifier(fetcher=...)`` and pass an explicit
    verification time, but operational lifecycle code must call this function so a
    caller cannot inject either an alternate key source or a caller-selected clock.
    """
    return GoogleOIDCVerifier().verify(token)