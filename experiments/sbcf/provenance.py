"""Local deterministic audit hashing; NOT external independent attestation."""
import hashlib
import json

def canonical_sha256(events: list[dict]) -> str:
    payload = json.dumps(events, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def verify_chain(events: list[dict]) -> bool:
    prev = "0" * 64
    for event in events:
        if set(event) != {"sequence", "previous", "payload", "digest"}:
            return False
        data = {"sequence": event["sequence"], "previous": event["previous"], "payload": event["payload"]}
        if event["previous"] != prev or event["digest"] != canonical_sha256([data]):
            return False
        prev = event["digest"]
    return True

def append_event(events: list[dict], payload: dict) -> list[dict]:
    if not verify_chain(events):
        raise ValueError("existing audit chain invalid")
    previous = events[-1]["digest"] if events else "0" * 64
    data = {"sequence": len(events), "previous": previous, "payload": payload}
    return [*events, {**data, "digest": canonical_sha256([data])}]
