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
    "tests/fixtures/identity-recovery.json",
    "docs/IDENTITY_RECOVERY.md",
    "docs/IDENTITY_RECOVERY_AUTHORITY.md",
    "docs/IDENTITY_RECOVERY_FAILURE_MATRIX.md",
    "docs/IDENTITY_SESSION_AND_KEY_LIFECYCLE.md",
    "tests/test_identity_recovery_contract.py",
    "tests/fixtures/identity-sovereignty-ui.json",
    "docs/IDENTITY_SOVEREIGNTY_UI.md",
    "docs/IDENTITY_UI_AUTHORITY_MAP.md",
    "docs/IDENTITY_UI_ACCESSIBILITY.md",
    "tests/test_identity_sovereignty_ui.py",
    "tests/test_identity_stack_ultra_review.py",
    "docs/IDENTITY_STACK_V1_RELEASE_REVIEW.md",
    "artifacts/identity-stack-v1-ultra-review.json",
    "tests/fixtures/constitutional-stack-authority.json",
    "tests/fixtures/constitutional-stack-capabilities.json",
    "tests/fixtures/constitutional-stack-data-flow.json",
    "tests/fixtures/constitutional-stack-upstream-gaps.json",
    "tests/test_constitutional_stack_integration.py",
    "docs/CONSTITUTIONAL_STACK_V1_INTEGRATION_REVIEW.md",
    "artifacts/constitutional-stack-v1-integration-review.json",
    "tests/fixtures/daily-driver-v1-config.json",
    "tests/test_daily_driver_productization.py",
    "docs/RUNTIME_TOPOLOGY.md",
    "docs/GETTING_STARTED.md",
    "docs/BUILDING.md",
    "docs/DEFAULT_CONFIGURATION.md",
    "docs/LINUX_DAILY_DRIVER.md",
    "docs/DAILY_DRIVER_V1_FEATURE_MATRIX.md",
    "artifacts/daily-driver-v1-release.json",
    "docs/DAILY_DRIVER_V1_RELEASE_REVIEW.md",
    "docs/DEPLOYMENT_ARCHITECTURE.md",
    "docs/DEPLOYMENT_V1.md",
    "docs/SELF_HOSTING_WEB.md",
    "docs/STAGING.md",
    "docs/DEPLOYMENT_TROUBLESHOOTING.md",
    "deploy/static-headers",
    "deploy/static-redirects",
    "artifacts/deployment-v1-manifest.json",
    "tests/fixtures/deployment-v1-config.json",
    "tests/test_deployment_v1.py",
    "docs/DEPLOYMENT_FEATURE_MATRIX.md",
    "docs/DEPLOYMENT_V1_RELEASE_REVIEW.md",
    "docs/UPSTREAM_INVENTORY.md",
    "docs/UPSTREAM_PATCH_SURFACE.md",
    "docs/UPSTREAM_REBASE_PLAYBOOK.md",
    "docs/UPSTREAMABILITY.md",
    "docs/UPSTREAM_REBASE_HARDENING_V1_RELEASE_REVIEW.md",
    "artifacts/upstream-baseline.json",
    "artifacts/upstream-delta-inventory.json",
    "artifacts/upstream-rebase-risk.json",
    "artifacts/upstream-rebase-receipt.json",
    "scripts/check_upstream.py",
    "tests/test_upstream_hardening.py",
    "docs/RELEASE_NOTES_DAILY_DRIVER_V1.md",
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
    recovery = load("tests/fixtures/identity-recovery.json")
    assert recovery["format"] == "org.radical-liberal.identity-recovery"
    assert recovery["secretsInReceipts"] is False
    ui = load("tests/fixtures/identity-sovereignty-ui.json")
    assert ui["format"] == "org.radical-liberal.identity-sovereignty-ui"
    assert ui["privacy"]["secretsRedacted"] is True
    review = load("artifacts/identity-stack-v1-ultra-review.json")
    assert review["verdict"] == "IDENTITY_STACK_V1_RELEASE_READY"
    assert review["severity"]["P1"] == 0
    authority = load("tests/fixtures/constitutional-stack-authority.json")
    capabilities = load("tests/fixtures/constitutional-stack-capabilities.json")
    data_flow = load("tests/fixtures/constitutional-stack-data-flow.json")
    gaps = load("tests/fixtures/constitutional-stack-upstream-gaps.json")
    assert authority["format"] == "org.radical-liberal.constitutional-stack-authority"
    assert "pds-change-does-not-change-appview" in authority["invariants"]
    assert capabilities["vocabulary"] == ["LIVE", "FIXTURE-TESTED", "SIMULATED", "UNSUPPORTED-UPSTREAM", "SKIPPED_ENVIRONMENT"]
    assert "refresh-token-to-personalization" in data_flow["forbidden"]
    assert len(gaps["gaps"]) >= 3
    integration = load("artifacts/constitutional-stack-v1-integration-review.json")
    assert integration["verdict"] == "CONSTITUTIONAL_STACK_V1_RELEASE_READY"
    assert integration["severity"]["P1"] == 0
    daily = load("tests/fixtures/daily-driver-v1-config.json")
    assert daily["format"] == "org.radical-liberal.daily-driver-config"
    assert daily["production"]["localhostDefaults"] is False
    assert daily["production"]["fixtureProviders"] is False
    assert daily["production"]["testCredentials"] is False
    daily_release = load("artifacts/daily-driver-v1-release.json")
    assert daily_release["kind"] == "daily-driver-v1-release"
    assert daily_release["severity"]["P1"] == 0
    deployment = load("artifacts/deployment-v1-manifest.json")
    deployment_config = load("tests/fixtures/deployment-v1-config.json")
    assert deployment["format"] == "org.radical-liberal.deployment-v1"
    assert deployment["secretsIncluded"] is False
    assert deployment_config["production"]["httpsRequired"] is True
    assert deployment_config["production"]["secretBuildVars"] is False
    assert deployment["deploymentStatus"] == "READY-BUT-NOT-EXECUTED"
    baseline = load("artifacts/upstream-baseline.json")
    delta = load("artifacts/upstream-delta-inventory.json")
    receipt = load("artifacts/upstream-rebase-receipt.json")
    assert len(baseline["upstreams"]) == 3
    assert delta["deltas"]
    assert receipt["secretsIncluded"] is False
    print(f"contract validation passed: {len(REQUIRED)} files, {len(blocking['rows'])} blocking rows, {len(feed['cases'])} feed cases")

if __name__ == "__main__":
    main()
