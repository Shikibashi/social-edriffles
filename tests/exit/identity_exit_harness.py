"""Deterministic identity exit characterization; simulated portions are explicit."""

import json
from typing import Any


def run() -> dict[str, Any]:
    state: dict[str, Any] = {
        "did": "did:plc:example",
        "handle": "alice.example",
        "pds": "A",
        "appview": "X",
        "provider": "feed-x",
        "preferences": {"freshness": 0.8, "topics": ["science"]},
        "oldSession": "revoked",
    }
    for field, value in (("pds", "B"), ("appview", "Y"), ("provider", "feed-y")):
        state[field] = value
    exported: dict[str, Any] = {
        "did": state["did"],
        "preferences": state["preferences"],
    }
    restored: dict[str, Any] = json.loads(json.dumps(exported, sort_keys=True))
    assert (
        restored["did"] == state["did"]
        and restored["preferences"] == state["preferences"]
    )
    assert state["oldSession"] == "revoked"
    return {
        "simulated": True,
        "didContinuous": True,
        "repositoryContinuity": "protocol-dependent",
        "preferencesRestored": True,
        "oldSessionRevoked": True,
        "credentialsExported": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
