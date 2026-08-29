#!/usr/bin/env python3
"""Validate the external evidence contracts without manufacturing evidence.

This validator accepts synthetic fixtures so the receipt boundary itself can be
tested. A fixture is never an external gate result: only a receipt captured
from the controlled deployment, with independently supplied bindings, can be
used by release review.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

import validate_oauth_spaces_receipts as contract

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests/fixtures"

JsonObject = dict[str, Any]

CANARY_FORMAT = "us.edriffles.radlib.external-private-canary/1"
OAUTH_FORMAT = "us.edriffles.radlib.external-oauth-expiry/1"
PLC_FORMAT = "us.edriffles.radlib.external-plc-independence/1"

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
BASE64URL_RE = re.compile(r"^[A-Za-z0-9_-]+$")
DID_PLC_RE = re.compile(r"^did:plc:[a-z0-9]{24}$")


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


def as_positive_int(value: Any, source: str, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise AssertionError(f"expected positive integer at {source}")
    if value > maximum:
        raise AssertionError(f"value exceeds bound at {source}")
    return value


def require_sha256(value: Any, source: str) -> str:
    result = as_string(value, source)
    if not SHA256_RE.fullmatch(result):
        raise AssertionError(f"expected sha256 digest at {source}")
    return result


def require_https_url(value: Any, source: str, *, origin_only: bool = False) -> str:
    result = as_string(value, source)
    parsed = urlparse(result)
    if parsed.scheme != "https" or not parsed.hostname:
        raise AssertionError(f"expected HTTPS URL at {source}")
    if parsed.username is not None or parsed.password is not None:
        raise AssertionError(f"userinfo is not allowed at {source}")
    if parsed.fragment:
        raise AssertionError(f"fragment is not allowed at {source}")
    if origin_only and (parsed.path not in ("", "/") or parsed.query):
        raise AssertionError(f"expected an origin URL at {source}")
    return result


def url_origin(value: str) -> tuple[str, str, int | None]:
    parsed = urlparse(value)
    return parsed.scheme, parsed.hostname or "", parsed.port


def require_timestamp(value: Any, source: str) -> str:
    result = as_string(value, source)
    if not result.endswith("Z"):
        raise AssertionError(f"timestamp must be UTC at {source}")
    try:
        parsed = datetime.fromisoformat(result.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AssertionError(f"invalid timestamp at {source}") from exc
    if parsed.tzinfo is None:
        raise AssertionError(f"timestamp must include a timezone at {source}")
    return result


def validate_bindings(receipt: JsonObject, source: str) -> JsonObject:
    bindings = as_object(receipt.get("bindings"), f"{source}.bindings")
    as_string(bindings.get("environment"), f"{source}.bindings.environment")
    require_timestamp(bindings.get("testedAt"), f"{source}.bindings.testedAt")
    as_string(
        bindings.get("testedSourceRevision"),
        f"{source}.bindings.testedSourceRevision",
    )
    require_sha256(
        bindings.get("deploymentImage"), f"{source}.bindings.deploymentImage"
    )
    for key in ("sourceWorkingTreeDigest", "webArtifactDigest"):
        if key in bindings:
            require_sha256(bindings[key], f"{source}.bindings.{key}")
    return bindings


def validate_common(receipt: JsonObject, source: str, expected_format: str) -> None:
    if receipt.get("format") != expected_format:
        raise AssertionError(f"unexpected format at {source}")
    if receipt.get("secretsIncluded") is not False:
        raise AssertionError(f"secret policy is not false at {source}")
    evidence_status = receipt.get("evidenceStatus")
    if evidence_status not in {"fixture", "current", "blocked-external"}:
        raise AssertionError(f"unexpected evidence status at {source}")
    contract.assert_no_secret_keys(receipt, source)
    contract.assert_no_secret_values(receipt, source)
    validate_bindings(receipt, source)


def validate_target(target: Any, source: str) -> None:
    target_obj = as_object(target, source)
    require_https_url(target_obj.get("endpoint"), f"{source}.endpoint", origin_only=True)
    operator = as_object(target_obj.get("operator"), f"{source}.operator")
    as_string(operator.get("operatorId"), f"{source}.operator.operatorId")
    require_https_url(
        operator.get("identityDocument"),
        f"{source}.operator.identityDocument",
    )
    deployment = as_object(target_obj.get("deployment"), f"{source}.deployment")
    require_sha256(deployment.get("imageDigest"), f"{source}.deployment.imageDigest")
    as_string(deployment.get("sourceRevision"), f"{source}.deployment.sourceRevision")
    require_timestamp(deployment.get("capturedAt"), f"{source}.deployment.capturedAt")
    access = as_object(target_obj.get("access"), f"{source}.access")
    for channel in ("capture", "storage", "logs"):
        channel_obj = as_object(access.get(channel), f"{source}.access.{channel}")
        as_string(
            channel_obj.get("accessReference"),
            f"{source}.access.{channel}.accessReference",
        )


def require_checks(
    receipt: JsonObject, expected: dict[str, bool], source: str
) -> JsonObject:
    checks = as_object(receipt.get("checks"), f"{source}.checks")
    for name, expected_value in expected.items():
        actual_value = as_bool(checks.get(name), f"{source}.checks.{name}")
        if actual_value is not expected_value:
            raise AssertionError(f"check did not match at {source}.{name}")
    return checks


def validate_private_canary(receipt: JsonObject, source: str) -> None:
    validate_common(receipt, source, CANARY_FORMAT)
    status = as_string(receipt.get("status"), f"{source}.status")
    if status != "PASSED_EXTERNAL_PRIVATE_CANARY_RELAY_APPVIEW":
        if not status.startswith("BLOCKED_EXTERNAL_PRIVATE_CANARY"):
            raise AssertionError(f"unexpected canary status at {source}")
        return
    if receipt.get("evidenceStatus") == "blocked-external":
        raise AssertionError("blocked canary evidence cannot be a pass")

    canary = as_object(receipt.get("canary"), f"{source}.canary")
    control_id = as_string(canary.get("publicControlId"), f"{source}.canary.publicControlId")
    private_id = as_string(canary.get("privateCanaryId"), f"{source}.canary.privateCanaryId")
    if control_id == private_id:
        raise AssertionError("control and private canaries must differ")
    require_https_url(canary.get("pdsEndpoint"), f"{source}.canary.pdsEndpoint", origin_only=True)

    targets = as_object(receipt.get("targets"), f"{source}.targets")
    validate_target(targets.get("relay"), f"{source}.targets.relay")
    validate_target(targets.get("appView"), f"{source}.targets.appView")
    require_checks(
        receipt,
        {
            "publicControlCanaryObserved": True,
            "privateCanaryDirectPdsRead": True,
            "privateCanaryInPdsPublicCar": False,
            "privateCanaryInPdsSequencer": False,
            "privateCanaryInRelayStream": False,
            "privateCanaryInRelayStorage": False,
            "privateCanaryInRelayLogs": False,
            "privateCanaryInAppViewQuery": False,
            "privateCanaryInAppViewStorage": False,
            "privateCanaryInAppViewLogs": False,
            "canaryBodyIncluded": False,
        },
        source,
    )


def validate_oauth_expiry(receipt: JsonObject, source: str) -> None:
    validate_common(receipt, source, OAUTH_FORMAT)
    status = as_string(receipt.get("status"), f"{source}.status")
    if status != "PASSED_EXTERNAL_OAUTH_SHORT_TTL_EXPIRY_REPLAY":
        if not status.startswith("BLOCKED_EXTERNAL_OAUTH"):
            raise AssertionError(f"unexpected OAuth status at {source}")
        return
    if receipt.get("evidenceStatus") == "blocked-external":
        raise AssertionError("blocked OAuth evidence cannot be a pass")
    target = as_object(receipt.get("target"), f"{source}.target")
    for name in ("authorizationServer", "resourceServer", "clientMetadata"):
        require_https_url(target.get(name), f"{source}.target.{name}")
    require_checks(
        receipt,
        {
            "ttlWithinConfiguredLimit": True,
            "preExpiryAuthorizedRequest": True,
            "staleAccessTokenRejected": True,
            "refreshSucceeded": True,
            "refreshTokenRotated": True,
            "oldRefreshTokenReplayRejected": True,
            "authorizationCodeReplayRejected": True,
            "authorizationCodeReplayRevokedSession": True,
            "revokedOnCleanup": True,
        },
        source,
    )
    timing = as_object(receipt.get("timing"), f"{source}.timing")
    configured = as_positive_int(
        timing.get("configuredTokenMaxAgeMs"),
        f"{source}.timing.configuredTokenMaxAgeMs",
        60_000,
    )
    observed = as_positive_int(
        timing.get("observedExpiresInSeconds"),
        f"{source}.timing.observedExpiresInSeconds",
        60,
    )
    if observed > (configured + 1_999) // 1_000:
        raise AssertionError("observed OAuth TTL exceeds configured bound")
    as_positive_int(timing.get("waitMs"), f"{source}.timing.waitMs", 120_000)


def canonical_json_bytes(value: JsonObject) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def decode_base64url(value: Any, source: str) -> bytes:
    encoded = as_string(value, source)
    if not BASE64URL_RE.fullmatch(encoded):
        raise AssertionError(f"invalid base64url at {source}")
    try:
        return base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
    except ValueError as exc:
        raise AssertionError(f"invalid base64url at {source}") from exc


def validate_operator(operator: Any, source: str) -> JsonObject:
    operator_obj = as_object(operator, source)
    as_string(operator_obj.get("operatorId"), f"{source}.operatorId")
    as_string(operator_obj.get("serviceDid"), f"{source}.serviceDid")
    public_key = decode_base64url(operator_obj.get("publicKey"), f"{source}.publicKey")
    if len(public_key) != 32:
        raise AssertionError(f"expected Ed25519 public key at {source}.publicKey")
    require_https_url(operator_obj.get("endpoint"), f"{source}.endpoint", origin_only=True)
    evidence = operator_obj.get("controlEvidence")
    if not isinstance(evidence, list) or not evidence:
        raise AssertionError(f"control evidence is empty at {source}")
    for index, item in enumerate(evidence):
        evidence_obj = as_object(item, f"{source}.controlEvidence[{index}]")
        reference = evidence_obj.get("evidenceRef")
        if isinstance(reference, str) and reference.startswith("https://"):
            require_https_url(reference, f"{source}.controlEvidence[{index}].evidenceRef")
        else:
            as_string(reference, f"{source}.controlEvidence[{index}].evidenceRef")
        as_string(
            evidence_obj.get("verifiedBy"),
            f"{source}.controlEvidence[{index}].verifiedBy",
        )
        require_timestamp(
            evidence_obj.get("verifiedAt"),
            f"{source}.controlEvidence[{index}].verifiedAt",
        )
    return operator_obj


def validate_plc_independence(receipt: JsonObject, source: str) -> None:
    validate_common(receipt, source, PLC_FORMAT)
    status = as_string(receipt.get("status"), f"{source}.status")
    if status != "PASSED_EXTERNAL_PLC_OPERATOR_INDEPENDENCE":
        if not status.startswith("BLOCKED_EXTERNAL_PLC"):
            raise AssertionError(f"unexpected PLC status at {source}")
        return
    if receipt.get("evidenceStatus") == "blocked-external":
        raise AssertionError("blocked PLC evidence cannot be a pass")

    operators = as_object(receipt.get("operators"), f"{source}.operators")
    primary = validate_operator(operators.get("primary"), f"{source}.operators.primary")
    mirror = validate_operator(operators.get("mirror"), f"{source}.operators.mirror")
    for field in ("operatorId", "serviceDid", "publicKey"):
        if primary[field] == mirror[field]:
            raise AssertionError(f"PLC operators must differ in {field}")
    if url_origin(primary["endpoint"]) == url_origin(mirror["endpoint"]):
        raise AssertionError("PLC operators must use different endpoint origins")

    independence = as_object(receipt.get("independence"), f"{source}.independence")
    if as_bool(independence.get("proven"), f"{source}.independence.proven") is not True:
        raise AssertionError("PLC operator independence is not proven")
    basis = independence.get("basis")
    if not isinstance(basis, list) or len(basis) < 2 or len(set(basis)) != len(basis):
        raise AssertionError("PLC independence needs multiple evidence references")
    for index, item in enumerate(basis):
        require_https_url(item, f"{source}.independence.basis[{index}]")

    history = as_object(
        receipt.get("didHistoryVerification"),
        f"{source}.didHistoryVerification",
    )
    did = as_string(history.get("did"), f"{source}.didHistoryVerification.did")
    if not DID_PLC_RE.fullmatch(did):
        raise AssertionError(f"expected did:plc identifier at {source}.didHistoryVerification.did")
    require_sha256(history.get("historyDigest"), f"{source}.didHistoryVerification.historyDigest")
    as_positive_int(
        history.get("operationCount"),
        f"{source}.didHistoryVerification.operationCount",
        1_000_000,
    )
    for name in (
        "genesisDerivedDid",
        "previousCidsVerified",
        "rotationSignaturesVerified",
        "tombstoneRulesVerified",
        "primaryMirrorAgreement",
        "staleFixtureRejected",
        "malformedFixtureRejected",
        "invalidSignatureRejected",
        "disagreementVisible",
    ):
        if as_bool(history.get(name), f"{source}.didHistoryVerification.{name}") is not True:
            raise AssertionError(f"DID history check did not pass at {source}.{name}")

    disagreement = as_object(receipt.get("resolverDisagreement"), f"{source}.resolverDisagreement")
    if as_bool(disagreement.get("observed"), f"{source}.resolverDisagreement.observed") is not True:
        raise AssertionError("resolver disagreement was not observed")
    if as_bool(disagreement.get("visible"), f"{source}.resolverDisagreement.visible") is not True:
        raise AssertionError("resolver disagreement was not made visible")
    as_string(disagreement.get("reconciliation"), f"{source}.resolverDisagreement.reconciliation")

    signed = as_object(receipt.get("signedReceipt"), f"{source}.signedReceipt")
    signed_by = as_string(signed.get("signedBy"), f"{source}.signedReceipt.signedBy")
    if signed_by != mirror["operatorId"]:
        raise AssertionError("signed PLC receipt is not from the mirror operator")
    if signed.get("signatureAlgorithm") != "Ed25519":
        raise AssertionError("PLC receipt must use Ed25519")
    statement = as_object(signed.get("signedStatement"), f"{source}.signedReceipt.signedStatement")
    for field in ("did", "historyDigest", "operationCount"):
        if statement.get(field) != history.get(field):
            raise AssertionError(f"signed PLC statement is not bound to {field}")
    if statement.get("resolverDisagreementVisible") is not True:
        raise AssertionError("signed PLC statement does not cover visible disagreement")
    payload = canonical_json_bytes(statement)
    digest = "sha256:" + hashlib.sha256(payload).hexdigest()
    if signed.get("signedPayloadSha256") != digest:
        raise AssertionError("signed PLC payload digest mismatch")
    public_key = decode_base64url(signed.get("publicKey"), f"{source}.signedReceipt.publicKey")
    signature = decode_base64url(signed.get("signature"), f"{source}.signedReceipt.signature")
    if public_key != decode_base64url(mirror["publicKey"], f"{source}.operators.mirror.publicKey"):
        raise AssertionError("signed PLC receipt key does not match mirror identity")
    if as_bool(signed.get("signatureVerified"), f"{source}.signedReceipt.signatureVerified") is not True:
        raise AssertionError("signed PLC receipt is not marked verified")
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError as exc:
        raise AssertionError("cryptography is required for PLC signature verification") from exc
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(signature, payload)
    except Exception as exc:
        raise AssertionError("PLC receipt Ed25519 signature verification failed") from exc


def validate_receipt(path: Path) -> None:
    receipt = as_object(contract.load_json(path), str(path))
    source = path.name
    format_name = receipt.get("format")
    if format_name == CANARY_FORMAT:
        validate_private_canary(receipt, source)
    elif format_name == OAUTH_FORMAT:
        validate_oauth_expiry(receipt, source)
    elif format_name == PLC_FORMAT:
        validate_plc_independence(receipt, source)
    else:
        raise AssertionError(f"unsupported external receipt format at {source}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or sorted(FIXTURE_DIR.glob("external-*-pass.json"))
    if not paths:
        raise SystemExit("no external receipt fixtures were found")
    for path in paths:
        validate_receipt(path)
    print(f"external gate receipt validation passed: {len(paths)} receipts")


if __name__ == "__main__":
    main()
