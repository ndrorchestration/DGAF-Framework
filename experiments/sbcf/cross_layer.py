"""Synthetic executable specification; not connected to a production effect boundary."""

from .controller import Regime, State, verified_quarantine
from .enforcement import SimulatedGate


def _shape(value, fields):
    return type(value) is dict and set(value) == set(fields)


def _text(value):
    return type(value) is str and bool(value.strip())


def _sources(policy):
    return (
        type(policy) is dict
        and bool(policy)
        and all(
            _text(field) and type(sources) is list and bool(sources) and all(_text(source) for source in sources)
            for field, sources in policy.items()
        )
    )


def _current(context):
    return (
        _shape(
            context,
            (
                "resource",
                "policy",
                "run",
                "nonce",
                "now",
                "regime",
                "trusted_issuers",
                "parameter_policy",
                "observable",
                "revocation_checked",
            ),
        )
        and all(_text(context[k]) for k in ("resource", "policy", "run", "nonce"))
        and type(context["now"]) is int
        and context["now"] >= 0
        and context["regime"] in ("NORMAL", "RESTRICTED", "QUARANTINED")
        and type(context["trusted_issuers"]) is list
        and bool(context["trusted_issuers"])
        and all(_text(issuer) for issuer in context["trusted_issuers"])
        and _sources(context["parameter_policy"])
        and type(context["observable"]) is bool
        and type(context["revocation_checked"]) is bool
    )


def _permission(request, grant, context):
    scope = ("subject", "action", "resource", "policy", "run", "nonce")
    if not (
        _shape(request, (*scope, "parameter_sources"))
        and _shape(grant, ("issuer", *scope, "not_before", "expires_at", "revoked"))
        and all(_text(request[k]) and _text(grant[k]) for k in scope)
        and _text(grant["issuer"])
        and grant["issuer"] in context["trusted_issuers"]
        and all(request[k] == grant[k] for k in scope)
        and all(request[k] == context[k] for k in ("resource", "policy", "run", "nonce"))
        and type(grant["not_before"]) is int
        and grant["not_before"] >= 0
        and type(grant["expires_at"]) is int
        and grant["not_before"] <= context["now"] < grant["expires_at"]
        and type(grant["revoked"]) is bool
        and not grant["revoked"]
        and context["revocation_checked"]
        and context["observable"]
        and type(request["parameter_sources"]) is dict
        and set(request["parameter_sources"]) == set(context["parameter_policy"])
        and all(
            _text(source) and source in context["parameter_policy"][field]
            for field, source in request["parameter_sources"].items()
        )
    ):
        return False
    gate = SimulatedGate(regime=Regime[context["regime"]], grants=frozenset({request["action"]}))
    return gate.attempt(request["action"])


def _quarantine(snapshot, context):
    counts = (
        "production_capabilities",
        "uncontrolled_workers",
        "pending_external_actions",
        "unauthorized_destinations",
    )
    if not (
        _shape(snapshot, (*counts, "observable", "external_attestation"))
        and all(type(snapshot[k]) is int and snapshot[k] >= 0 for k in counts)
        and type(snapshot["observable"]) is bool
        and type(snapshot["external_attestation"]) is bool
        and context["observable"]
    ):
        return False
    state = State(regime=Regime[context["regime"]], **{k: snapshot[k] for k in (*counts, "observable")})
    return verified_quarantine(state, snapshot["external_attestation"])


def evaluate(case):
    """Evaluate caller-controlled synthetic facts; return no executable authority.

    Trust roots, source authentication, atomic observations and policy completeness
    are assumptions supplied by fixtures, not established by this function.
    """
    result = {
        "effect_permitted": False,
        "quarantine_predicate": False,
        "canonical_validation_established": False,
        "authority_effect": "NONE",
    }
    if not (
        _shape(case, ("request", "grant", "context", "quarantine", "message", "local_evidence_label"))
        and _current(case["context"])
    ):
        return result
    result["effect_permitted"] = _permission(case["request"], case["grant"], case["context"])
    result["quarantine_predicate"] = _quarantine(case["quarantine"], case["context"])
    return result
