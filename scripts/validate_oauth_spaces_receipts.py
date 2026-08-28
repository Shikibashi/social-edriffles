#!/usr/bin/env python3
"""Fail-closed validation for the secret-free OAuth/Spaces acceptance bundle."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_DIR = ROOT / "artifacts/receipts"
MANIFEST_PATH = ROOT / "artifacts/oauth-spaces-manifest.json"
SIDECAR_PATH = ROOT / "artifacts/oauth-spaces-manifest.sha256"

FORBIDDEN_KEYS = {
    "accessjwt",
    "accesstoken",
    "apikey",
    "authmaterial",
    "authorization",
    "authorizationcode",
    "authorizationheader",
    "bearer",
    "code",
    "codechallenge",
    "codeverifier",
    "clientassertion",
    "clientsecret",
    "credential",
    "credentials",
    "dpop",
    "dpopkey",
    "dpopjwk",
    "dpopproof",
    "oauthsecret",
    "oauthtoken",
    "password",
    "privatekey",
    "privatejwk",
    "pdspassword",
    "refreshtoken",
    "secret",
    "secretvalue",
    "sessiontoken",
    "sessionsecret",
    "token",
    "tokenpayload",
    "tokenvalue",
}

SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"(?i)\b(?:bearer|dpop)\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(
        r"(?i)\b(?:oauth|access|refresh|authorization|client|code|dpop)[_-]?(?:jwt|token|code|secret|assertion|verifier|proof|credential)\s*[:=]\s*[^\s,}]{8,}"
    ),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"-----BEGIN [A-Z0-9 ]+-----"),
    re.compile(r"(?i)\bBasic\s+[A-Za-z0-9+/]{8,}={0,2}"),
)

CURRENT_SOURCE_BOUND_RECEIPTS = {
    "authority-decision.json",
    "local-oauth-spaces-acceptance.json",
    "local-private-canary-scan.json",
    "radlib-edge-cutover-pending.json",
}
CURRENT_CUTOVER_RECEIPT = "radlib-edge-cutover-pending.json"
EXPECTED_MANIFEST_STATUS = "BLOCKED_EXTERNAL_SPACES_APPVIEW_BROWSER_AND_EXPIRY_GATES"
EXPECTED_BLOCKERS = {
    "PUBLIC_CREDENTIALED_SPACES_NOT_RUN",
    "OAUTH_BROWSER_CREDENTIAL_ENTRY_NOT_RUN",
    "INCONCLUSIVE_APPVIEW_403",
    "SPACES_ALPHA_LIMITATIONS",
    "OAUTH_EXPIRY_GAP",
}

EVIDENCE_STATUSES = {
    "alpha-local",
    "blocked-external",
    "current",
    "historical-superseded",
    "inconclusive",
    "policy-decision",
}

JsonObject = dict[str, Any]


def normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> JsonObject:
    value: JsonObject = {}
    for key, child in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def parse_json(text: str, source: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except ValueError as exc:
        raise AssertionError(f"invalid JSON at {source}: {exc}") from exc


def load_json(path: Path) -> Any:
    return parse_json(path.read_text(), str(path))


def as_object(value: Any, source: str) -> JsonObject:
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object at {source}")
    return cast(JsonObject, value)


def as_string_map(value: Any, source: str) -> dict[str, str]:
    obj = as_object(value, source)
    if not all(
        isinstance(key, str) and isinstance(child, str) for key, child in obj.items()
    ):
        raise AssertionError(f"expected string map at {source}")
    return cast(dict[str, str], obj)


def as_object_map(value: Any, source: str) -> dict[str, JsonObject]:
    obj = as_object(value, source)
    return {key: as_object(child, f"{source}.{key}") for key, child in obj.items()}


def source_inputs() -> list[Path]:
    # This digest binds deployable source inputs to a deployment image. The
    # manifest, receipts, validators, and prose documentation are evidence
    # about that binding and must not change the digest after an image is
    # built; otherwise recording the receipt would invalidate the image.
    paths: list[Path] = []
    paths.extend(
        path for path in (ROOT / "upstream/social-app/src").rglob("*") if path.is_file()
    )
    paths.extend(
        ROOT / path
        for path in (
            "upstream/social-app/public/oauth-client-metadata.json",
            "upstream/social-app/app.config.js",
            "upstream/social-app/package.json",
            "upstream/social-app/pnpm-lock.yaml",
            "upstream/social-app/scripts/post-web-build.js",
            "deploy/static-headers",
            "deploy/radlib-edge-proxy/src/index.ts",
            "deploy/radlib-edge-proxy/wrangler.jsonc",
            "deploy/radlib-edge-proxy/worker-configuration.d.ts",
            "upstream/atproto-pds/packages/pds/src/api/index.ts",
            "upstream/atproto-pds/packages/pds/src/api/us/edriffles/radlib/private/index.ts",
            "upstream/atproto-pds/packages/pds/src/well-known.ts",
            "upstream/atproto-pds/packages/pds/src/repo/schemas.ts",
            "upstream/atproto-pds/packages/dev-env/src/service-profile-lexicon.ts",
            "upstream/atproto-pds/packages/pds/src/repo/prepare.ts",
            "upstream/atproto-pds/packages/pds/tests/space/radlib-community-lexicon.test.ts",
            "upstream/atproto-pds/packages/pds/tests/radlib-spaces.test.ts",
            "upstream/atproto-pds/packages/pds/src/lexicons.ts",
            "upstream/atproto-pds/lexicons/us/edriffles/radlib/account.json",
        )
    )
    paths.extend(
        path
        for path in (
            ROOT / "upstream/atproto-pds/lexicons/us/edriffles/radlib/private"
        ).glob("*.json")
        if path.is_file()
    )
    paths.extend(
        path
        for path in (ROOT / "upstream/atproto-pds/packages/pds/src/lexicons").rglob("*")
        if path.is_file()
    )
    return sorted(set(paths), key=lambda path: path.as_posix())


def source_digest() -> tuple[str, int]:
    entries: list[bytes] = []
    for path in source_inputs():
        if not path.is_file():
            raise AssertionError(f"missing source input: {path.relative_to(ROOT)}")
        entries.append(
            path.as_posix().encode()
            + b"\0"
            + hashlib.sha256(path.read_bytes()).hexdigest().encode()
            + b"\n"
        )
    return "sha256:" + hashlib.sha256(b"".join(entries)).hexdigest(), len(entries)


def web_artifact_digest() -> str:
    build = ROOT / "upstream/social-app/web-build"
    entries: list[bytes] = []
    for path in sorted(
        (path for path in build.rglob("*") if path.is_file()),
        key=lambda path: path.as_posix(),
    ):
        entries.append(
            path.as_posix().encode()
            + b"\0"
            + hashlib.sha256(path.read_bytes()).hexdigest().encode()
            + b"\n"
        )
    if not entries:
        raise AssertionError("web artifact is missing")
    return "sha256:" + hashlib.sha256(b"".join(entries)).hexdigest()


def assert_no_secret_keys(value: Any, path: str) -> None:
    if isinstance(value, dict):
        mapping = cast(dict[Any, Any], value)
        for key, child in mapping.items():
            if normalize_key(key) in FORBIDDEN_KEYS:
                raise AssertionError(f"forbidden secret-bearing key at {path}.{key}")
            assert_no_secret_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        children = cast(list[Any], value)
        for index, child in enumerate(children):
            assert_no_secret_keys(child, f"{path}[{index}]")


def assert_no_secret_values(value: Any, path: str) -> None:
    if isinstance(value, dict):
        mapping = cast(dict[Any, Any], value)
        for key, child in mapping.items():
            assert_no_secret_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        children = cast(list[Any], value)
        for index, child in enumerate(children):
            assert_no_secret_values(child, f"{path}[{index}]")
    elif isinstance(value, str):
        for pattern in SENSITIVE_VALUE_PATTERNS:
            if pattern.search(value):
                raise AssertionError(f"secret-like value at {path}")


def assert_secret_policy_is_fail_closed() -> None:
    """Keep the receipt policy itself covered against common bypass shapes."""
    key_fixtures = (
        {"access_token": "opaque-token"},
        {"auth_material": "opaque-auth-material"},
        {"authorization_code": "opaque-code"},
        {"code_verifier": "opaque-verifier"},
        {"dpop_jwk": {"kty": "EC", "d": "opaque-private-value"}},
        {"private_jwk": {"kty": "EC", "d": "opaque-private-value"}},
        {"pds_password": "opaque-password"},
        {"session_secret": "opaque-session-secret"},
        {"token_payload": {"access": "opaque-token"}},
    )
    for fixture in key_fixtures:
        try:
            assert_no_secret_keys(fixture, "fixture")
        except AssertionError:
            continue
        raise AssertionError(f"secret policy accepted adversarial key: {fixture}")

    value_fixtures = (
        "Bearer opaque-bearer-value",
        "authorization_code=opaque-code-value",
        "oauth_token=opaque-oauth-token-value",
        "Authorization: Basic dXNlcjpwYXNz",
        "-----BEGIN PRIVATE KEY-----",
    )
    for fixture in value_fixtures:
        try:
            assert_no_secret_values(fixture, "fixture")
        except AssertionError:
            continue
        raise AssertionError(f"secret policy accepted adversarial value: {fixture}")

    try:
        parse_json(
            '{"access_token":"opaque-token","access_token":"redacted"}',
            "duplicate-key-fixture",
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("JSON parser accepted a duplicate secret-bearing key")


def assert_receipt_binding_matches(
    receipt: JsonObject, manifest_binding: JsonObject, name: str
) -> None:
    receipt_binding = as_object(receipt.get("bindings", {}), f"{name}.bindings")
    receipt_time = receipt_binding.get("testedAt") or receipt.get("timestamp")
    assert receipt_time and manifest_binding["testedAt"] == receipt_time, name
    assert receipt_binding.get("environment") == manifest_binding["environment"], name
    receipt_image = receipt_binding.get("deploymentImage") or receipt_binding.get(
        "sourceImage"
    )
    assert receipt_image and manifest_binding["deploymentImage"] == receipt_image, name
    for revision_key, prefix in (
        ("rootRevision", "root"),
        ("socialRevision", "social"),
        ("pdsRevision", "pds"),
    ):
        revision = receipt_binding.get(revision_key)
        if revision:
            assert (
                f"{prefix}:{revision}" in manifest_binding["testedSourceRevision"]
            ), name


def assert_deployment_image_policy(value: str) -> None:
    assert (
        value.startswith("sha256:")
        or value.startswith("pds:sha256:")
        or value.startswith("cloudflare-pages:")
        or value.startswith("cloudflare-worker:")
        or value.startswith("not-")
    ), value


def validate_manifest(
    manifest: JsonObject, receipt_names: set[str]
) -> tuple[JsonObject, dict[str, str], dict[str, JsonObject]]:
    receipt_hashes = as_string_map(manifest["receiptHashes"], "manifest.receiptHashes")
    receipt_bindings = as_object_map(
        manifest["receiptBindings"], "manifest.receiptBindings"
    )
    manifest_bindings = as_object(manifest["bindings"], "manifest.bindings")
    assert set(receipt_hashes) == receipt_names
    assert set(receipt_bindings) == receipt_names
    assert manifest["format"] == "us.edriffles.radlib.oauth-spaces-manifest/1"
    assert manifest["integritySidecar"] == "artifacts/oauth-spaces-manifest.sha256"
    assert manifest["status"] == EXPECTED_MANIFEST_STATUS
    assert manifest["blockers"]
    assert EXPECTED_BLOCKERS.issubset(set(manifest["blockers"]))
    assert "AUTHORITY_DEFERRED_OUT_OF_SCOPE" not in manifest["deferred"]
    assert manifest_bindings["deploymentStatus"] == (
        "SOCIAL_USER_FACING_CUTOVER_DEPLOYED"
    )
    assert manifest_bindings["origins"] == ["https://social.edriffles.us"]
    assert_deployment_image_policy(manifest_bindings["deploymentImage"])
    assert_deployment_image_policy(manifest_bindings["sourceImage"])
    assert manifest["secretsIncluded"] is False
    assert "AUTHORITY_UNRESOLVED" not in manifest["blockers"]
    assert_secret_policy_is_fail_closed()
    for name, binding in receipt_bindings.items():
        assert "gjcReviewSourceHash" not in binding, name
        assert "gjcReviewPathCount" not in binding, name
    return manifest_bindings, receipt_hashes, receipt_bindings


def validate_cutover_receipt(receipt_bindings: dict[str, JsonObject]) -> None:
    cutover = load_json(RECEIPT_DIR / CURRENT_CUTOVER_RECEIPT)
    cutover = as_object(cutover, CURRENT_CUTOVER_RECEIPT)
    deployment = as_object(
        cutover["deployment"], f"{CURRENT_CUTOVER_RECEIPT}.deployment"
    )
    cutover_bindings = as_object(
        cutover["bindings"], f"{CURRENT_CUTOVER_RECEIPT}.bindings"
    )
    assert cutover["format"] == "us.edriffles.radlib.edge-cutover/1"
    assert cutover["status"] == EXPECTED_MANIFEST_STATUS
    assert deployment["dryRun"] == "passed"
    assert deployment["route"] == "deployed"
    assert deployment["dns"] == "verified"
    assert deployment["pdsPublicHost"] == "reconfigured"
    assert deployment["publicHttpsProbe"] == "passed"
    assert deployment["oauthProviderApiRouting"] == "passed"
    assert deployment["publicPostRoute"] == "passed"
    assert deployment["publicClientMetadata"] == "passed"
    assert deployment["browserOAuthHandoff"] == "passed"
    assert deployment["browserCredentialEntry"] == ("not-run-browser-policy")
    assert cutover_bindings["origins"] == ["https://social.edriffles.us"]
    assert receipt_bindings[CURRENT_CUTOVER_RECEIPT]["deploymentImage"] == (
        cutover_bindings["deploymentImage"]
    )


def validate_receipts(
    manifest_bindings: JsonObject,
    receipt_paths: list[Path],
    receipt_bindings: dict[str, JsonObject],
    receipt_hashes: dict[str, str],
) -> None:
    for path in receipt_paths:
        receipt = as_object(load_json(path), path.name)
        assert receipt.get("secretsIncluded") is False, path.name
        evidence_status = receipt.get("evidenceStatus")
        assert evidence_status in EVIDENCE_STATUSES, path.name
        if path.name in CURRENT_SOURCE_BOUND_RECEIPTS:
            assert evidence_status == "current", path.name
        else:
            assert evidence_status != "current", path.name
        if evidence_status == "historical-superseded":
            assert str(receipt.get("status", "")).startswith("HISTORICAL_"), path.name
        assert_no_secret_keys(receipt, path.name)
        assert_no_secret_values(receipt, path.name)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert receipt_hashes[path.name] == digest, path.name
        binding = receipt_bindings[path.name]
        assert binding["testedAt"]
        assert binding["testedSourceRevision"]
        assert_deployment_image_policy(binding["deploymentImage"])
        assert_receipt_binding_matches(receipt, binding, path.name)
        if path.name in CURRENT_SOURCE_BOUND_RECEIPTS:
            receipt_source_bindings = as_object(
                receipt["bindings"], f"{path.name}.bindings"
            )
            receipt_source = receipt_source_bindings.get("sourceWorkingTreeDigest")
            assert receipt_source == binding.get("sourceWorkingTreeDigest"), path.name
            assert binding.get("sourceWorkingTreeDigest") == receipt_source, path.name
            assert (
                binding.get("sourceWorkingTreeDigest")
                == manifest_bindings["currentSourceWorkingTreeDigest"]
            ), path.name
            receipt_web = receipt_source_bindings.get("webArtifactDigest")
            if receipt_web:
                assert binding.get("webArtifactDigest") == receipt_web, path.name
                assert receipt_web == manifest_bindings["webArtifactDigest"], path.name


def validate_manifest_integrity(
    manifest: JsonObject,
    manifest_bindings: JsonObject,
    receipt_bindings: dict[str, JsonObject],
    receipt_names: set[str],
) -> int:
    assert_no_secret_keys(manifest, "manifest")
    assert_no_secret_values(manifest, "manifest")
    expected_sidecar = (
        f"{hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()}  "
        "artifacts/oauth-spaces-manifest.json"
    )
    assert SIDECAR_PATH.read_text().strip() == expected_sidecar

    expected_source, input_count = source_digest()
    assert manifest_bindings["currentSourceWorkingTreeDigest"] == expected_source
    assert manifest_bindings["currentSourceInputCount"] == input_count
    assert manifest_bindings["webArtifactDigest"] == web_artifact_digest()
    receipt_times = [str(receipt_bindings[name]["testedAt"]) for name in receipt_names]
    assert str(manifest["generatedAt"]) >= max(receipt_times)
    return input_count


def validate_acceptance_receipts() -> None:
    local = load_json(RECEIPT_DIR / "local-oauth-spaces-acceptance.json")
    assert local["format"] == "us.edriffles.radlib.local-oauth-spaces-acceptance/1"
    assert local["checks"]["oauthScopeAndSignupPrompt"]["result"] == (
        "8 suites passed, 52 tests passed"
    )
    assert local["checks"]["credentialedSpaceAuthAndLifecycle"]["result"] == (
        "2 suites passed, 45 tests passed"
    )
    assert local["checks"]["fullBrowserOAuth"]["status"] == "NOT_RUN"
    assert local["checks"]["remoteCredentialedPds"]["status"] == (
        "PASSED_DISPOSABLE_ALPHA_CREDENTIALED_IDENTITY"
    )
    assert local["checks"]["remoteCredentialedSpaces"]["status"] == (
        "PASSED_DISPOSABLE_ALPHA_WITH_EXPLICIT_UNTIL_EXPIRY_LIMITATION"
    )

    deployment = load_json(RECEIPT_DIR / "cloudflare-deploy-attempt.json")
    assert deployment["attempt"]["deploymentCreated"] is False
    assert deployment["attempt"]["dnsChanged"] is False
    assert deployment["attempt"]["apiErrorCodes"] == [10000, 9109]
    assert deployment["status"] == "HISTORICAL_NOT_EXECUTED_INVALID_CLOUDFLARE_TOKEN"
    authority = load_json(RECEIPT_DIR / "authority-decision.json")
    assert authority["format"] == "us.edriffles.radlib.authority-decision/1"
    assert authority["status"] == "PASSED_DNS_AUTHORITY_AND_LEXICON_REPOSITORY"


def main() -> None:
    manifest = as_object(load_json(MANIFEST_PATH), str(MANIFEST_PATH))
    receipt_paths = sorted(RECEIPT_DIR.glob("*.json"))
    receipt_names = {path.name for path in receipt_paths}
    manifest_bindings, receipt_hashes, receipt_bindings = validate_manifest(
        manifest, receipt_names
    )
    validate_cutover_receipt(receipt_bindings)
    validate_receipts(
        manifest_bindings, receipt_paths, receipt_bindings, receipt_hashes
    )
    input_count = validate_manifest_integrity(
        manifest, manifest_bindings, receipt_bindings, receipt_names
    )
    validate_acceptance_receipts()

    print(
        f"OAuth/Spaces receipt validation passed: {len(receipt_paths)} receipts, "
        f"{input_count} source inputs, no secret-bearing keys"
    )


if __name__ == "__main__":
    main()
