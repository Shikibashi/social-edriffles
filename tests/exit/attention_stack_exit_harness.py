"""Deterministic disposable exit-path characterization harness.
Simulates PDS/AppView/provider/algorithm transitions without network or credentials.
"""

import json
from typing import Any


def run() -> dict[str, Any]:
    state: dict[str, Any] = {
        "pds": "A",
        "appview": "X",
        "provider": "provider-a",
        "algorithm": "balanced",
        "preferences": {"freshness": 0.8, "explicitInterests": ["science"]},
        "credential": "never-exported",
    }
    transitions: list[dict[str, Any]] = []
    for key, value in [
        ("algorithm", "news"),
        ("provider", "provider-b"),
        ("appview", "Y"),
        ("pds", "B"),
    ]:
        state[key] = value
        transitions.append(
            {
                key: value,
                "preferencesRetained": state["preferences"]
                == {"freshness": 0.8, "explicitInterests": ["science"]},
            }
        )
    portable = json.dumps({"preferences": state["preferences"]}, sort_keys=True)
    restored: dict[str, Any] = json.loads(portable)["preferences"]
    assert restored == state["preferences"]
    assert state["credential"] == "never-exported"
    return {
        "scenario": "PDS-A/AppView-X/Balanced -> News/provider-B/AppView-Y/PDS-B",
        "transitions": transitions,
        "preferencesRestored": restored,
        "credentialsExported": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
