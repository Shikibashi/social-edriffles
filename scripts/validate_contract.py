#!/usr/bin/env python3
"""Validate the bounded PR-00/PR-01 contract and deterministic fixtures."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "upstream-pins.json",
    "docs/CONSTITUTION.md",
    "docs/BLOCKING_SPEC.md",
    "docs/SERVICE_BOUNDARIES.md",
    "docs/FEED_CONSTITUTION.md",
    "docs/LIVE_CHARACTERIZATION.md",
    "docs/RUNTIME_SLICE.md",
    "tests/fixtures/blocking-matrix.json",
    "tests/fixtures/feed-contract.json",
    "tests/fixtures/attention-contract.json",
    "tests/fixtures/feed-provider-security.json",
    "tests/fixtures/candidate-protocol-replay.json",
    "tests/fixtures/balanced-v1-replay.json",
    "tests/fixtures/attention-sovereignty-ui.json",
    "tests/fixtures/experimental-attention-v1.json",
    "tests/test_attention_stack_release_audit.py",
    "tests/exit/attention_stack_exit_harness.py",
    "docs/ATTENTION_SURFACE_INVENTORY.md",
    "tests/fixtures/experimental-attention-results.json",
    "tests/fixtures/identity-contract.json",
    "tests/fixtures/identity-adversarial.json",
    "tests/exit/identity_exit_harness.py",
    "docs/IDENTITY_CONSTITUTION.md",
    "docs/IDENTITY_AUTHORITY_MODEL.md",
    "docs/IDENTITY_EXIT_AND_MIGRATION.md",
    "docs/IDENTITY_DEPENDENCY_AUDIT.md",
    "tests/test_identity_constitution.py",
    "tests/fixtures/identity-runtime-matrix.json",
    "docs/IDENTITY_RUNTIME.md",
    "docs/IDENTITY_MIGRATION_RUNTIME.md",
    "docs/IDENTITY_MIGRATION_FAILURE_MATRIX.md",
    "tests/test_identity_runtime_contract.py",
]

def load(rel: str):
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"missing required file: {rel}")
    return json.loads(path.read_text()) if path.suffix == ".json" else path.read_text()

def main() -> None:
    for rel in REQUIRED:
        load(rel)
    pins = load("upstream-pins.json")
    assert pins["repositories"]["appviewlite"]["commit"] == "75f78e8e098c05f52821e836832205050c0f539e"
    assert pins["repositories"]["socialApp"]["commit"] == "1f5c698165c922e707833809902ee959e9824f00"
    assert pins["retrievedAt"]

    blocking = load("tests/fixtures/blocking-matrix.json")
    assert blocking["baseline"].endswith("75f78e8e098c05f52821e836832205050c0f539e")
    assert set(blocking["surfaces"]) >= {"posts", "threads", "profiles", "follows", "replies", "mentions", "notifications", "quotes", "feeds"}
    assert {row["viewer"] for row in blocking["rows"]} >= {"A", "B", "C"}
    for surface in blocking["surfaces"]:
        assert any(row["surface"] == surface for row in blocking["rows"]), f"no fixture row for {surface}"

    feed = load("tests/fixtures/feed-contract.json")
    required = {"personalization-sovereignty", "integrity-separation", "viewpoint-neutrality", "explanation-fidelity", "credible-exit"}
    assert required <= set(feed["invariants"])
    assert feed["treatments"] == ["chronological", "engagement", "diversified"]
    assert all(case["id"] for case in feed["cases"])
    assert json.dumps(feed, sort_keys=True) == json.dumps(json.loads(json.dumps(feed)), sort_keys=True)
    attention = load("tests/fixtures/attention-contract.json")
    assert attention["format"] == "org.radical-liberal.attention-constitution"
    assert attention["version"] == 1
    assert len(attention["surfaces"]) == 10
    assert set(attention["explanationScopes"]) == {"public", "audit", "confidential-anti-abuse"}
    assert set(attention["authorityClasses"]) == {"one-shot-advice", "continuous-policy", "local-reversible-filter", "durable-account-mutation"}
    assert {"author-cap", "duplicate-suppression", "exploration-budget", "dogpile-amplification-control"} <= set(attention["concentrationControls"])
    assert set(attention["frozenBoundaries"]) == {"association-constitution", "service-constitution", "portable-personalization-v1"}
    security = load("tests/fixtures/feed-provider-security.json")
    assert security["format"] == "org.radical-liberal.feed-provider-security"
    assert security["version"] == 1
    assert len(security["cases"]) >= 18
    assert security["dataOnly"] is True
    assert {"timeout", "identity-failure", "signature-failure", "hydration-disagreement"} <= set(security["failureClasses"])
    replay = load("tests/fixtures/candidate-protocol-replay.json")
    assert replay["format"] == "org.radical-liberal.candidate-replay"
    assert replay["version"] == 1
    assert replay["batch"]["format"] == "org.radical-liberal.candidate-batch"
    assert replay["portablePersonalization"]["exportLevel"] == "settings"
    assert replay["ranking"]["orderedUris"]
    balanced = load("tests/fixtures/balanced-v1-replay.json")
    assert balanced["format"] == "org.radical-liberal.balanced-replay"
    assert balanced["version"] == 1
    assert len(balanced["candidateSources"]) == 5
    assert "dogpile" in balanced["scenarios"]
    assert balanced["expected"]["deterministic"] is True
    ui = load("tests/fixtures/attention-sovereignty-ui.json")
    assert ui["format"] == "org.radical-liberal.attention-sovereignty-ui"
    assert ui["privacy"]["confidentialIntegrityVisible"] is False
    assert len(ui["accessibility"]) >= 4
    experimental = load("tests/fixtures/experimental-attention-v1.json")
    assert experimental["format"] == "org.radical-liberal.experimental-attention"
    assert len(experimental["modules"]) == 5
    assert experimental["optIn"] is True
    audit = load("artifacts/attention-stack-v1-release-audit.json")
    assert audit["decision"] == "ATTENTION_STACK_V1_RELEASE_READY"
    assert audit["severity"]["P1"] == 0
    identity = load("tests/fixtures/identity-contract.json")
    adversarial = load("tests/fixtures/identity-adversarial.json")
    assert identity["format"] == "org.radical-liberal.identity-constitution"
    assert len(adversarial["cases"]) >= 18
    runtime = load("tests/fixtures/identity-runtime-matrix.json")
    assert runtime["format"] == "org.radical-liberal.identity-runtime"
    assert runtime["cache"]["maxStaleSeconds"] == 3600
    print(f"contract validation passed: {len(REQUIRED)} files, {len(blocking['rows'])} blocking rows, {len(feed['cases'])} feed cases")

if __name__ == "__main__":
    main()
