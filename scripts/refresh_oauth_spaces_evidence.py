#!/usr/bin/env python3
"""Refresh current source-bound OAuth/Spaces evidence without touching history.

This command updates only receipts explicitly classified as current. Historical
receipts remain byte-for-byte untouched. It is intentionally write-explicit:
without --write it reports the source/revision values that would be recorded.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import validate_oauth_spaces_receipts as contract

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_DIR = ROOT / "artifacts/receipts"
MANIFEST_PATH = ROOT / "artifacts/oauth-spaces-manifest.json"
SIDECAR_PATH = ROOT / "artifacts/oauth-spaces-manifest.sha256"

CURRENT_BLOCKERS = [
    "PRIVATE_CANARY_RELAY_APPVIEW_NOT_RUN",
    "OAUTH_EXPIRY_GAP",
    "PLC_OPERATOR_INDEPENDENCE_NOT_PROVEN",
]
CURRENT_MANIFEST_STATUS = "BLOCKED_EXTERNAL_APPVIEW_EXPIRY_AND_PLC_INDEPENDENCE_GATES"
CURRENT_RELEASE_BOUND_RECEIPTS = {
    "credentialed-public-oauth.json",
    "live-public-contract-probe.json",
    "radlib-edge-cutover-pending.json",
}
CURRENT_DEPLOYMENT_LINKED_RECEIPTS = CURRENT_RELEASE_BOUND_RECEIPTS | {
    "credentialed-public-spaces.json"
}


def git_head(path: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        raise RuntimeError(f"could not resolve git HEAD for {path}")
    return completed.stdout.strip()


def timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object at {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def build_live_probe_receipt(
    probe: dict[str, Any],
    deployment: dict[str, Any],
    source: str,
    web: str,
    tested_source: str,
    root_revision: str,
    social_revision: str,
    pds_revision: str,
) -> dict[str, Any]:
    """Wrap the full read-only probe in the current receipt contract."""
    metadata = probe.get("metadata", {})
    protected = probe.get("protectedResource", {})
    authorization = probe.get("authorizationServer", {})
    private = probe.get("privateBoundary", {})
    dns = probe.get("lexiconDnsAuthority", {})
    plc = probe.get("plc", {})
    tested_at = str(probe.get("probedAt") or timestamp())
    return {
        "format": "us.edriffles.radlib.live-public-probe/1",
        "status": probe.get("overallStatus", "PUBLIC_CONTRACT_FAILED"),
        "evidenceStatus": "current",
        "secretsIncluded": False,
        "bindings": {
            "deploymentId": deployment["deploymentId"],
            "deploymentImage": deployment["deploymentImage"],
            "deploymentStatus": deployment["deploymentStatus"],
            "environment": "live-public-internet-read-only",
            "origins": [
                "https://social.edriffles.us",
                "https://pds.edriffles.us",
                "https://radlib.edriffles.us",
            ],
            "rootRevision": root_revision,
            "socialRevision": social_revision,
            "pdsRevision": pds_revision,
            "sourceWorkingTreeDigest": source,
            "testedAt": tested_at,
            "testedSourceRevision": tested_source,
            "webArtifactDigest": web,
        },
        "checks": {
            "publicClientMetadata": {
                "contractStatus": metadata.get("contractStatus"),
                "legacyTransitionScopesObserved": metadata.get(
                    "legacyTransitionScopes", []
                ),
                "sourceArtifactStatus": metadata.get("sourceArtifactStatus"),
                "spaceScopeAdvertised": metadata.get("spaceScopeAdvertised"),
                "status": (
                    "PASS"
                    if metadata.get("contractStatus") == "PASS"
                    and metadata.get("sourceArtifactStatus") == "CURRENT"
                    else "FAIL"
                ),
            },
            "protectedResource": protected.get("status"),
            "authorizationServer": authorization.get("status"),
            "didDocuments": "PASS"
            if all(
                item.get("status") == "PASS"
                for item in (probe.get("didDocuments") or {}).values()
            )
            else "FAIL",
            "health": (probe.get("health") or {}).get("status"),
            "privateBoundary": "PASS"
            if all(
                item.get("status") == "PASS"
                for item in (private or {}).values()
            )
            else "FAIL",
            "lexiconDnsAuthority": {
                "agreement": dns.get("agreement"),
                "resolverCount": len(dns.get("resolverResults", {})),
                "status": dns.get("status"),
            },
            "plcEndpoints": {
                "auditShape": (plc.get("audit") or {}).get("status"),
                "dataShape": (plc.get("data") or {}).get("status"),
                "cryptographicHistoryVerification": plc.get(
                    "cryptographicHistoryVerification"
                ),
            },
            "credentialsUsed": probe.get("credentialsUsed"),
            "writesPerformed": probe.get("writesPerformed"),
        },
    }


def deployment_record(path: Path) -> tuple[dict[str, Any], str]:
    record = read_json(path)
    if record.get("secretsIncluded") is not False:
        raise ValueError("deployment record must be secret-free")
    contract.assert_no_secret_keys(record, path.name)
    contract.assert_no_secret_values(record, path.name)
    return record, hashlib.sha256(path.read_bytes()).hexdigest()


def source_revision(
    root_revision: str, social_revision: str, pds_revision: str, source: str
) -> str:
    return (
        f"root:{root_revision};social:{social_revision};pds:{pds_revision};"
        f"working-tree:{source}"
    )


def refresh(
    write: bool,
    deployment_record_path: Path | None = None,
    live_probe_path: Path | None = None,
) -> None:
    root_revision = git_head(ROOT)
    social_revision = git_head(ROOT / "upstream/social-app")
    pds_revision = git_head(ROOT / "upstream/atproto-pds")
    source, input_count = contract.source_digest()
    web = contract.web_artifact_digest()
    tested_source = source_revision(
        root_revision, social_revision, pds_revision, source
    )

    deployment = None
    deployment_record_hash = None
    if deployment_record_path:
        deployment, deployment_record_hash = deployment_record(deployment_record_path)
        deployment_source = deployment.get("source", {})
        if deployment_source.get("workingTreeDigest") != source:
            raise ValueError("deployment record source digest is not current")
        if deployment_source.get("webArtifactDigest") != web:
            raise ValueError("deployment record web artifact digest is not current")
        if live_probe_path is None:
            raise ValueError("a deployed refresh requires the live probe output")

    receipts: dict[str, dict[str, Any]] = {}
    for name in sorted(contract.CURRENT_SOURCE_BOUND_RECEIPTS):
        path = RECEIPT_DIR / name
        if name == "live-public-contract-probe.json" and live_probe_path:
            receipt = build_live_probe_receipt(
                read_json(live_probe_path),
                deployment,
                source,
                web,
                tested_source,
                root_revision,
                social_revision,
                pds_revision,
            )
        else:
            receipt = read_json(path)
        bindings = receipt.get("bindings")
        if not isinstance(bindings, dict):
            raise ValueError(f"current receipt has no bindings object: {name}")
        bindings = copy.deepcopy(bindings)
        bindings.update(
            {
                "rootRevision": root_revision,
                "socialRevision": social_revision,
                "pdsRevision": pds_revision,
                "sourceWorkingTreeDigest": source,
                "testedSourceRevision": tested_source,
            }
        )
        if deployment and name in CURRENT_DEPLOYMENT_LINKED_RECEIPTS:
            bindings["deploymentId"] = deployment["deploymentId"]
        if deployment and name in CURRENT_RELEASE_BOUND_RECEIPTS:
            bindings["deploymentImage"] = deployment["deploymentImage"]
            bindings["deploymentStatus"] = deployment["deploymentStatus"]
        if deployment and name == "radlib-edge-cutover-pending.json":
            bindings["testedAt"] = deployment["verifiedAt"]
        if "webArtifactDigest" in bindings:
            bindings["webArtifactDigest"] = web
        receipt["bindings"] = bindings
        contract.assert_no_secret_keys(receipt, name)
        contract.assert_no_secret_values(receipt, name)
        receipts[name] = receipt

    manifest = read_json(MANIFEST_PATH)
    bindings = manifest.get("bindings")
    if not isinstance(bindings, dict):
        raise ValueError("manifest has no bindings object")
    bindings.update(
        {
            "currentSourceWorkingTreeDigest": source,
            "currentSourceInputCount": input_count,
            "webArtifactDigest": web,
            "rootRevision": root_revision,
            "socialRevision": social_revision,
            "pdsRevision": pds_revision,
        }
    )
    if deployment:
        bindings.update(
            {
                "deploymentId": deployment["deploymentId"],
                "deploymentImage": deployment["deploymentImage"],
                "sourceImage": deployment["sourceImage"],
                "deploymentStatus": deployment["deploymentStatus"],
                "deploymentComponents": copy.deepcopy(deployment["components"]),
                "testedAt": deployment["verifiedAt"],
            }
        )
        manifest["deployment"] = copy.deepcopy(deployment)
        manifest["deployment"]["recordPath"] = (
            deployment_record_path.relative_to(ROOT).as_posix()
        )
        manifest["deployment"]["recordSha256"] = deployment_record_hash
    else:
        bindings.update(
            {
                "deploymentId": None,
                "deploymentImage": "not-deployed-current-worktree",
                "sourceImage": "not-deployed-current-worktree",
                "deploymentStatus": "SOURCE_READY_NOT_DEPLOYED",
            }
        )
    manifest["bindings"] = bindings
    manifest["blockers"] = CURRENT_BLOCKERS
    manifest["status"] = (
        CURRENT_MANIFEST_STATUS if deployment else "SOURCE_READY_EXTERNAL_GATES_PENDING"
    )
    manifest["generatedAt"] = timestamp()

    receipt_hashes = manifest.get("receiptHashes")
    receipt_bindings = manifest.get("receiptBindings")
    if not isinstance(receipt_hashes, dict) or not isinstance(
        receipt_bindings, dict
    ):
        raise ValueError("manifest receipt maps are invalid")
    for path in sorted(RECEIPT_DIR.glob("*.json")):
        name = path.name
        receipt = receipts.get(name)
        if receipt is not None:
            if write:
                write_json(path, receipt)
            receipt_bytes = (json.dumps(receipt, indent=2) + "\n").encode()
            receipt_hashes[name] = hashlib.sha256(receipt_bytes).hexdigest()
            receipt_bindings[name] = copy.deepcopy(receipt["bindings"])
        else:
            receipt_hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()

    manifest["receiptHashes"] = receipt_hashes
    manifest["receiptBindings"] = receipt_bindings
    contract.assert_no_secret_keys(manifest, "manifest")
    contract.assert_no_secret_values(manifest, "manifest")

    if write:
        write_json(MANIFEST_PATH, manifest)
        sidecar = (
            f"{hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()}  "
            "artifacts/oauth-spaces-manifest.json\n"
        )
        SIDECAR_PATH.write_text(sidecar)

    mode = "refreshed" if write else "would refresh"
    print(
        f"{mode} {len(receipts)} current receipts; "
        f"source={source}; inputs={input_count}; web={web}; "
        f"root={root_revision}; social={social_revision}; pds={pds_revision}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write current receipts, manifest, and sidecar",
    )
    parser.add_argument(
        "--deployment-record",
        type=Path,
        help="secret-free JSON record for the deployed Pages, Worker, and PDS",
    )
    parser.add_argument(
        "--live-probe",
        type=Path,
        help="JSON output produced by verify_social_edriffles_live.py --output",
    )
    args = parser.parse_args()
    refresh(args.write, args.deployment_record, args.live_probe)


if __name__ == "__main__":
    main()
