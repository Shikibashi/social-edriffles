#!/usr/bin/env python3
"""Probe a public PLC mirror without promoting it to an authority.

The command deliberately emits a blocked receipt unless the candidate has
operator evidence that satisfies the external PLC contract. A matching mirror
history proves replication and cryptographic verification, not independent
control or operator-signed attestation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DID = "did:plc:ewvi7nxzyoun6zhxrhs64oiz"
DEFAULT_PRIMARY = "https://plc.directory"
DEFAULT_MIRROR = "https://didplc.directory"
DEFAULT_OPERATOR_DID_URL = "https://vayumandala.com/.well-known/did.json"
DEFAULT_MIRROR_SOFTWARE = "did-method-plc/go-didplc"
DEFAULT_MIRROR_LANDING_PAGE = "https://didplc.directory/"


def timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def fetch_json(url: str) -> tuple[int, Any]:
    request = Request(
        url,
        headers={
            "accept": "application/json",
            "user-agent": "radlib-external-gate-probe/1",
        },
    )
    with urlopen(request, timeout=20) as response:
        return response.status, json.load(response)


def history_for(origin: str, did: str) -> tuple[int, int, list[Any], Any]:
    encoded = quote(did, safe="")
    data_status, data = fetch_json(f"{origin}/{encoded}/data")
    audit_status, audit = fetch_json(f"{origin}/{encoded}/log/audit")
    if not isinstance(audit, list):
        raise ValueError(f"audit response from {origin} is not a list")
    history = [
        item["operation"] if isinstance(item, dict) and "operation" in item else item
        for item in audit
    ]
    return data_status, audit_status, history, data


def history_digest(history: list[Any]) -> str:
    payload = json.dumps(history, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def key_description(document: Any) -> tuple[str | None, str]:
    if not isinstance(document, dict):
        return None, "operator-document-invalid"
    methods = document.get("verificationMethod")
    if not isinstance(methods, list) or not methods:
        return None, "operator-key-not-published"
    first_key: str | None = None
    for method in methods:
        if not isinstance(method, dict):
            continue
        key = method.get("publicKeyMultibase")
        if not isinstance(key, str) or not key:
            continue
        first_key = first_key or key
        if key.startswith("z6Mk"):
            return key, "ed25519"
    if first_key is None:
        return None, "operator-key-not-published"
    return first_key, "not-ed25519"


def verify_history(did: str, history: list[Any]) -> dict[str, Any]:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from verify_social_edriffles_live import verify_live_plc_history

        return verify_live_plc_history(did, history, 30)
    finally:
        if sys.path and sys.path[0] == str(ROOT / "scripts"):
            sys.path.pop(0)


def build_receipt(args: argparse.Namespace) -> dict[str, Any]:
    checked_at = timestamp()
    primary_data_status, primary_audit_status, primary_history, primary_data = history_for(
        args.primary, args.did
    )
    mirror_data_status, mirror_audit_status, mirror_history, mirror_data = history_for(
        args.mirror, args.did
    )
    primary_verification = verify_history(args.did, primary_history)
    mirror_verification = verify_history(args.did, mirror_history)
    primary_digest = history_digest(primary_history)
    mirror_digest = history_digest(mirror_history)

    mirror_health_status = None
    mirror_health: Any = None
    try:
        mirror_health_status, mirror_health = fetch_json(urljoin(args.mirror + "/", "_health"))
    except Exception:
        mirror_health_status = 0

    operator_document_status = 0
    operator_document: Any = None
    try:
        operator_document_status, operator_document = fetch_json(args.operator_did_url)
    except Exception:
        operator_document_status = 0
    operator_key, operator_key_status = key_description(operator_document)
    operator_did = operator_document.get("id") if isinstance(operator_document, dict) else None

    tombstone_observation: dict[str, Any] = {
        "provided": bool(args.tombstone_did),
        "did": args.tombstone_did,
    }
    tombstone_verified = False
    if args.tombstone_did:
        tombstone_primary = history_for(args.primary, args.tombstone_did)
        tombstone_mirror = history_for(args.mirror, args.tombstone_did)
        tombstone_primary_verification = verify_history(
            args.tombstone_did, tombstone_primary[2]
        )
        tombstone_mirror_verification = verify_history(
            args.tombstone_did, tombstone_mirror[2]
        )
        tombstone_primary_digest = history_digest(tombstone_primary[2])
        tombstone_mirror_digest = history_digest(tombstone_mirror[2])
        tombstone_verified = (
            tombstone_primary[0] == 200
            and tombstone_primary[1] == 200
            and tombstone_mirror[0] == 200
            and tombstone_mirror[1] == 200
            and tombstone_primary_verification.get("verifierStatus") == "tombstoned"
            and tombstone_mirror_verification.get("verifierStatus") == "tombstoned"
            and tombstone_primary_digest == tombstone_mirror_digest
        )
        tombstone_observation.update(
            {
                "primaryHistoryDigest": tombstone_primary_digest,
                "mirrorHistoryDigest": tombstone_mirror_digest,
                "primaryVerifierStatus": tombstone_primary_verification.get(
                    "verifierStatus"
                ),
                "mirrorVerifierStatus": tombstone_mirror_verification.get(
                    "verifierStatus"
                ),
                "primaryOperationCount": len(tombstone_primary[2]),
                "mirrorOperationCount": len(tombstone_mirror[2]),
            }
        )

    disagreement_observation: dict[str, Any] = {
        "provided": bool(args.disagreement_did),
        "did": args.disagreement_did,
        "reconciliation": args.reconciliation,
    }
    disagreement_observed = False
    disagreement_visible = False
    if args.disagreement_did:
        disagreement_primary = history_for(args.primary, args.disagreement_did)
        disagreement_mirror = history_for(args.mirror, args.disagreement_did)
        primary_disagreement_digest = history_digest(disagreement_primary[2])
        mirror_disagreement_digest = history_digest(disagreement_mirror[2])
        disagreement_observed = primary_disagreement_digest != mirror_disagreement_digest
        disagreement_visible = disagreement_observed and bool(args.reconciliation)
        disagreement_observation.update(
            {
                "primaryHistoryDigest": primary_disagreement_digest,
                "mirrorHistoryDigest": mirror_disagreement_digest,
                "primaryStatus": [disagreement_primary[0], disagreement_primary[1]],
                "mirrorStatus": [disagreement_mirror[0], disagreement_mirror[1]],
                "observed": disagreement_observed,
                "visible": disagreement_visible,
            }
        )

    histories_agree = primary_digest == mirror_digest
    primary_verified = primary_verification.get("status") == "PASS"
    mirror_verified = mirror_verification.get("status") == "PASS"
    has_ed25519_operator_key = operator_key_status == "ed25519"

    receipt = {
        "format": "us.edriffles.radlib.external-plc-independence/1",
        "evidenceStatus": "blocked-external",
        "secretsIncluded": False,
        "status": "BLOCKED_EXTERNAL_PLC_SIGNED_OPERATOR_STATEMENT",
        "bindings": {
            "deploymentImage": args.deployment_image,
            "environment": "disposable-public-alpha/external-gates/plc-candidate",
            "testedAt": checked_at,
            "testedSourceRevision": args.source_revision,
            "sourceWorkingTreeDigest": args.source_digest,
            "webArtifactDigest": args.web_digest,
        },
        "candidate": {
            "did": args.did,
            "primaryEndpoint": args.primary,
            "mirrorEndpoint": args.mirror,
            "mirrorSoftware": args.mirror_software,
            "mirrorLandingPage": args.mirror_landing_page,
            "operatorIdentityDocument": args.operator_did_url,
            "operatorDid": operator_did,
            "operatorPublicKeyMultibase": operator_key,
            "operatorKeyStatus": operator_key_status,
        },
        "checks": {
            "primaryHistoryFetched": primary_data_status == 200 and primary_audit_status == 200,
            "mirrorHistoryFetched": mirror_data_status == 200 and mirror_audit_status == 200,
            "primaryHistoryCryptographicallyVerified": primary_verified,
            "mirrorHistoryCryptographicallyVerified": mirror_verified,
            "historyAgreement": histories_agree,
            "operationHashesVerified": primary_verified and mirror_verified,
            "previousCidsVerified": primary_verified and mirror_verified,
            "genesisDerivedDid": primary_verified and mirror_verified,
            "rotationSignaturesVerified": primary_verified and mirror_verified,
            "tombstoneRulesVerified": tombstone_verified,
            "operatorIdentityPublished": operator_document_status == 200 and operator_did is not None,
            "separateEndpoint": args.primary != args.mirror,
            "distinctServiceDid": operator_did not in (None, args.did),
            "ed25519PublicKeyPublished": has_ed25519_operator_key,
            "signedDidHistoryReceiptPublished": False,
            "visibleResolverDisagreement": disagreement_visible,
        },
        "observations": {
            "primaryDataStatus": primary_data_status,
            "primaryAuditStatus": primary_audit_status,
            "mirrorDataStatus": mirror_data_status,
            "mirrorAuditStatus": mirror_audit_status,
            "mirrorHealthStatus": mirror_health_status,
            "mirrorHealth": mirror_health,
            "operationCount": len(primary_history),
            "primaryHistoryDigest": primary_digest,
            "mirrorHistoryDigest": mirror_digest,
            "primaryHeadCid": primary_verification.get("headCid"),
            "mirrorHeadCid": mirror_verification.get("headCid"),
            "primaryData": {
                "did": primary_data.get("did") if isinstance(primary_data, dict) else None,
                "serviceCount": len(primary_data.get("services", {}))
                if isinstance(primary_data, dict)
                else None,
            },
            "mirrorData": {
                "did": mirror_data.get("did") if isinstance(mirror_data, dict) else None,
                "serviceCount": len(mirror_data.get("services", {}))
                if isinstance(mirror_data, dict)
                else None,
            },
            "tombstoneEvidence": tombstone_observation,
            "resolverDisagreement": disagreement_observation,
        },
    }
    missing_evidence = [
        "operator-signed-DID-history-statement",
        "Ed25519-operator-public-key",
    ]
    if not tombstone_verified:
        missing_evidence.append("terminal-tombstone-fixture-evidence")
    if not disagreement_visible:
        missing_evidence.append("visible-resolver-disagreement-and-reconciliation")
    receipt["observations"]["missingRequiredEvidence"] = missing_evidence
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--did", default=DEFAULT_DID)
    parser.add_argument("--primary", default=DEFAULT_PRIMARY)
    parser.add_argument("--mirror", default=DEFAULT_MIRROR)
    parser.add_argument("--operator-did-url", default=DEFAULT_OPERATOR_DID_URL)
    parser.add_argument("--mirror-software", default=DEFAULT_MIRROR_SOFTWARE)
    parser.add_argument("--mirror-landing-page", default=DEFAULT_MIRROR_LANDING_PAGE)
    parser.add_argument(
        "--tombstone-did",
        help="fetch and verify a real terminal tombstone history from both endpoints",
    )
    parser.add_argument(
        "--disagreement-did",
        help="compare a DID history from both endpoints for an observable disagreement",
    )
    parser.add_argument(
        "--reconciliation",
        default="",
        help="user-visible reconciliation outcome for the disagreement probe",
    )
    parser.add_argument(
        "--deployment-image",
        default="sha256:62f8c703fd69f55a98e195f6e02f5446198036c99abe95e466e0f1ed757494cb",
    )
    parser.add_argument(
        "--source-revision",
        default="root:016f92eb4a9214ad8df6070733659faa14a00862;social:105a1691ec78c12c9326863199a53a0db0beadf2;pds:9c3d92f04335d624a79acbbf5f346130f00ffbdd;working-tree:sha256:bd712f549b6c60f1e0434e0398c39efde8d73dd80aa14110f8fcd33e07788139",
    )
    parser.add_argument(
        "--source-digest",
        default="sha256:bd712f549b6c60f1e0434e0398c39efde8d73dd80aa14110f8fcd33e07788139",
    )
    parser.add_argument(
        "--web-digest",
        default="sha256:f6c5d440e6091181cf5f831346e3b78fe7af74c3ac99654946a10215c81923b6",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = build_receipt(args)
    rendered = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
