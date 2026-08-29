#!/usr/bin/env python3
"""Validate the disposable external-gate staging manifest and its receipts.

This is deliberately separate from the production release manifest. The
staging PDS, Relay, and AppView are bound to disposable image digests and may
not be substituted for the deployed production image.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts/external-gates/staging-manifest.json"
SIDECAR_PATH = ROOT / "artifacts/external-gates/staging-manifest.sha256"

EXPECTED_FORMAT = "us.edriffles.radlib.external-gate-staging-manifest/1"
EXPECTED_STATUS = "BLOCKED_EXTERNAL_PLC_INDEPENDENCE_GATE"
EXPECTED_BLOCKERS = {"PLC_OPERATOR_INDEPENDENCE_NOT_PROVEN"}
EXPECTED_RECEIPTS = {
    "external-oauth-expiry-current.json",
    "external-private-canary-current.json",
    "external-plc-independence-blocked.json",
}
EXPECTED_SOURCE_DIGEST = (
    "sha256:bd712f549b6c60f1e0434e0398c39efde8d73dd80aa14110f8fcd33e07788139"
)
EXPECTED_WEB_DIGEST = (
    "sha256:f6c5d440e6091181cf5f831346e3b78fe7af74c3ac99654946a10215c81923b6"
)

JsonObject = dict[str, Any]


def as_object(value: Any, source: str) -> JsonObject:
    if not isinstance(value, dict):
        raise AssertionError(f"expected object at {source}")
    return cast(JsonObject, value)


def as_string(value: Any, source: str) -> str:
    if not isinstance(value, str) or not value:
        raise AssertionError(f"expected non-empty string at {source}")
    return value


def as_bool(value: Any, source: str) -> bool:
    if not isinstance(value, bool):
        raise AssertionError(f"expected boolean at {source}")
    return value


def require_https_origin(value: Any, source: str) -> str:
    result = as_string(value, source)
    parsed = urlparse(result)
    if parsed.scheme != "https" or not parsed.hostname:
        raise AssertionError(f"expected HTTPS origin at {source}")
    if parsed.username or parsed.password or parsed.path not in ("", "/"):
        raise AssertionError(f"expected origin without credentials/path at {source}")
    if parsed.query or parsed.fragment:
        raise AssertionError(f"query/fragment is not allowed at {source}")
    return result


def require_sha256(value: Any, source: str) -> str:
    result = as_string(value, source)
    if len(result) != 71 or not result.startswith("sha256:"):
        raise AssertionError(f"expected sha256 digest at {source}")
    int(result[7:], 16)
    return result


def require_timestamp(value: Any, source: str) -> str:
    result = as_string(value, source)
    if not result.endswith("Z"):
        raise AssertionError(f"timestamp must be UTC at {source}")
    try:
        parsed = datetime.fromisoformat(result[:-1] + "+00:00")
    except ValueError as exc:
        raise AssertionError(f"invalid timestamp at {source}") from exc
    if parsed.tzinfo is None:
        raise AssertionError(f"timestamp must include a timezone at {source}")
    return result


def load_json(path: Path) -> JsonObject:
    value = json.loads(path.read_text())
    return as_object(value, str(path))


def validate_manifest(path: Path = MANIFEST_PATH) -> None:
    manifest = load_json(path)

    expected_sidecar = (
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  "
        f"{path.relative_to(ROOT).as_posix()}"
    )
    if SIDECAR_PATH.read_text().strip() != expected_sidecar:
        raise AssertionError("staging manifest sidecar mismatch")

    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import validate_oauth_spaces_receipts as contract

        contract.assert_no_secret_keys(manifest, "external-gate-manifest")
        contract.assert_no_secret_values(manifest, "external-gate-manifest")
    finally:
        if sys.path and sys.path[0] == str(ROOT / "scripts"):
            sys.path.pop(0)

    if manifest.get("format") != EXPECTED_FORMAT:
        raise AssertionError("unexpected external-gate manifest format")
    if manifest.get("evidenceStatus") != "current":
        raise AssertionError("external-gate manifest is not current")
    if manifest.get("secretsIncluded") is not False:
        raise AssertionError("external-gate manifest secret policy is not false")
    if manifest.get("status") != EXPECTED_STATUS:
        raise AssertionError("unexpected external-gate manifest status")
    if set(manifest.get("blockers", [])) != EXPECTED_BLOCKERS:
        raise AssertionError("unexpected external-gate manifest blockers")

    bindings = as_object(manifest.get("bindings"), "manifest.bindings")
    if bindings.get("environment") != "disposable-public-alpha/external-gates":
        raise AssertionError("unexpected staging environment")
    require_timestamp(bindings.get("testedAt"), "manifest.bindings.testedAt")
    if bindings.get("testedSourceRevision", "").find(EXPECTED_SOURCE_DIGEST) < 0:
        raise AssertionError("staging source revision is not bound")
    if bindings.get("sourceWorkingTreeDigest") != EXPECTED_SOURCE_DIGEST:
        raise AssertionError("staging source digest is not bound")
    if bindings.get("webArtifactDigest") != EXPECTED_WEB_DIGEST:
        raise AssertionError("staging web artifact digest is not bound")
    origins = bindings.get("origins")
    if not isinstance(origins, list) or len(origins) != 5:
        raise AssertionError("staging origin inventory is incomplete")
    for index, origin in enumerate(origins):
        require_https_origin(origin, f"manifest.bindings.origins[{index}]")

    ttl = as_object(manifest.get("shortTtlPds"), "manifest.shortTtlPds")
    if ttl.get("tokenMaxAgeMs") != 5000 or ttl.get("inviteRequired") is not False:
        raise AssertionError("short-TTL PDS configuration is not disposable")
    require_https_origin(ttl.get("endpoint"), "manifest.shortTtlPds.endpoint")
    require_https_origin(ttl.get("issuer"), "manifest.shortTtlPds.issuer")
    require_sha256(ttl.get("imageDigest"), "manifest.shortTtlPds.imageDigest")
    if ttl.get("disposableHandleDomain") != ".oauth-test.edriffles.us":
        raise AssertionError("unexpected disposable handle domain")

    config = as_object(manifest.get("testConfiguration"), "manifest.testConfiguration")
    expected_config = {
        "PDS_OAUTH_TOKEN_MAX_AGE_MS": "5000",
        "RADLIB_ALLOW_EDRIFFLES_SUBDOMAIN_DISPOSABLE": "1",
        "RADLIB_DISPOSABLE_PDS_ORIGIN": "https://pds-oauth-test.edriffles.us",
        "RADLIB_EXPECTED_OAUTH_ISSUER": "https://oauth-oauth-test.edriffles.us",
        "RADLIB_DISPOSABLE_HANDLE_DOMAIN": ".oauth-test.edriffles.us",
        "RADLIB_CONFIRM_DISPOSABLE_TEST": "1",
        "RADLIB_RUN_EXPIRY_REPLAY": "1",
        "RADLIB_OAUTH_EXPECTED_TOKEN_MAX_AGE_MS": "5000",
        "RADLIB_EXPIRY_WAIT_MAX_MS": "30000",
    }
    if config != expected_config:
        raise AssertionError("short-TTL test configuration changed")

    targets = as_object(manifest.get("controlledTargets"), "manifest.controlledTargets")
    for name in ("relay", "appView"):
        target = as_object(targets.get(name), f"manifest.controlledTargets.{name}")
        require_https_origin(target.get("endpoint"), f"{name}.endpoint")
        require_sha256(target.get("imageDigest"), f"{name}.imageDigest")
        as_string(target.get("sourceRevision"), f"{name}.sourceRevision")
        for access_name in ("capture", "storage", "logs"):
            as_string(target.get(access_name), f"{name}.{access_name}")

    receipts = as_object(manifest.get("receipts"), "manifest.receipts")
    if set(receipts) != EXPECTED_RECEIPTS:
        raise AssertionError("staging receipt inventory is incomplete")

    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import validate_external_gate_receipts as external

        for name in sorted(EXPECTED_RECEIPTS):
            binding = as_object(receipts.get(name), f"manifest.receipts.{name}")
            receipt_path_value = as_string(binding.get("path"), f"{name}.path")
            receipt_path = (ROOT / receipt_path_value).resolve()
            try:
                receipt_path.relative_to(ROOT)
            except ValueError as exc:
                raise AssertionError(f"staging receipt path escapes repository: {name}") from exc
            if not receipt_path.is_file():
                raise AssertionError(f"missing staging receipt: {receipt_path_value}")
            if hashlib.sha256(receipt_path.read_bytes()).hexdigest() != binding.get("sha256"):
                raise AssertionError(f"staging receipt hash mismatch: {name}")
            external.validate_receipt(receipt_path)
            receipt = load_json(receipt_path)
            receipt_bindings = as_object(receipt.get("bindings"), f"{name}.bindings")
            for field in ("testedAt", "deploymentImage", "environment"):
                if receipt_bindings.get(field) != binding.get(field):
                    raise AssertionError(f"staging receipt binding mismatch: {name}.{field}")
    finally:
        if sys.path and sys.path[0] == str(ROOT / "scripts"):
            sys.path.pop(0)

    operator = as_object(manifest.get("operator"), "manifest.operator")
    as_string(operator.get("operatorId"), "manifest.operator.operatorId")
    if as_bool(operator.get("independenceClaimed"), "manifest.operator.independenceClaimed"):
        raise AssertionError("staging operator must not claim PLC independence")
    if operator.get("independenceStatus") != "not-proven":
        raise AssertionError("staging operator independence status changed")


def main() -> None:
    validate_manifest()
    print(
        f"external-gate staging manifest validation passed: {len(EXPECTED_RECEIPTS)} receipts; "
        "PLC independence remains blocked"
    )


if __name__ == "__main__":
    main()
