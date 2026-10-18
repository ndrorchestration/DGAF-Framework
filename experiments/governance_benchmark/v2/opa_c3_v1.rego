# C3 policy semantics in OPA/Rego v1; engineering comparator, not authority.
package dgaf.comparator_v2
default allow := false
allow if {
    is_object(input)
    is_object(input.action)
    count(deny) == 0
}

deny contains "ACTION_OBJECT_REQUIRED" if {
    is_object(input)
    not is_object(object.get(input, "action", null))
}

deny contains "ACTION_AUTHORIZED" if {
    object.get(input.action, "authorized", false) != true
}
deny contains "TOOL_ALLOWED" if {
    object.get(input.action, "tool_allowed", false) != true
}
deny contains "TARGET_ALLOWED" if {
    object.get(input.action, "target_allowed", false) != true
}
deny contains "DELEGATED_REQUESTER_AUTHORIZED" if {
    is_object(input.authority_context)
    v := input.authority_context.delegated_requester_authorized
    v != true
}
deny contains "NO_TOKEN_REPLAY" if {
    is_object(input.authority_context)
    v := input.authority_context.token_replay_detected
    v != false
}
deny contains "INTENT_BOUND" if {
    is_object(input.authority_context)
    v := input.authority_context.request_bound_to_authorized_intent
    v != true
}
deny contains "WORKLOAD_ATTESTED" if {
    is_object(input.authority_context)
    v := input.authority_context.workload_attested
    v != true
}
deny contains "CHILD_SCOPE_SUBSET" if {
    is_object(input.authority_context)
    v := input.authority_context.child_scope_subset
    v != true
}
evidence_domain_present if {
    is_object(input.claim)
    "evidence_present" in object.keys(input.claim)
}
evidence_domain_present if {
    is_object(input.claim)
    "evidence_fresh" in object.keys(input.claim)
}
deny contains "CLAIM_EVIDENCE_PRESENT_AND_FRESH" if {
    evidence_domain_present
    object.get(input.claim, "evidence_present", false) != true
}
deny contains "CLAIM_EVIDENCE_PRESENT_AND_FRESH" if {
    evidence_domain_present
    object.get(input.claim, "evidence_fresh", false) != true
}
deny contains "INDEPENDENT_STATUS_REQUIRES_INDEPENDENT_VERIFICATION" if {
    is_object(input.claim)
    input.claim.requested_status == "INDEPENDENT_VALIDATION_ESTABLISHED"
    object.get(input.claim, "verification_class", null) != "INDEPENDENT"
}
deny contains "FLOW_PROVENANCE_KNOWN" if {
    is_object(input.flow)
    v := input.flow.provenance_known
    v != true
}
deny contains "PROTECTED_EGRESS_REQUIRES_COMPOSITION_AUTHORIZATION" if {
    is_object(input.flow)
    input.flow.source_classification in {"CONFIDENTIAL", "RESTRICTED"}
    input.flow.destination_class == "EXTERNAL"
    object.get(input.flow, "composition_authorized", false) != true
}
