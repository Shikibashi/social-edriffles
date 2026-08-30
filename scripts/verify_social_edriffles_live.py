#!/usr/bin/env python3
"""Run a credential-free, read-only probe of the Plumbline public contract.

This probe deliberately does not log in, mint credentials, send authorization
headers, or write to any service. It distinguishes a valid public endpoint from
the more important question of whether the endpoint serves the current local
source artifact. A stale deployment is therefore reported explicitly instead
of being treated as a successful release check.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ORIGIN = "https://plumblines.uk"
PDS_ORIGIN = "https://pds.edriffles.us"
OAUTH_ORIGIN = "https://plumblines.uk"
LEXICON_AUTHORITY_NAME = "_lexicon.radlib.edriffles.us"
LEXICON_AUTHORITY_RESOLVERS = ("1.1.1.1", "8.8.8.8", "9.9.9.9")
AUTHORITY_DID_FALLBACK = "did:plc:cndgd3x3zxqmuv6rm3lsjhjm"
USER_AGENT = "social-edriffles-live-probe/1"
MAX_BODY_BYTES = 2 * 1024 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


OPENER = build_opener(NoRedirect())


@dataclass(frozen=True)
class Response:
    status: int | None
    headers: dict[str, str]
    payload: Any | None
    error: str | None


def fetch_json(url: str, timeout: float) -> Response:
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with OPENER.open(request, timeout=timeout) as response:
            body = response.read(MAX_BODY_BYTES + 1)
            if len(body) > MAX_BODY_BYTES:
                return Response(
                    response.status,
                    selected_headers(response.headers),
                    None,
                    "response exceeds probe size limit",
                )
            try:
                payload = json.loads(body)
            except json.JSONDecodeError as exc:
                return Response(
                    response.status,
                    selected_headers(response.headers),
                    None,
                    f"invalid JSON: {exc.msg}",
                )
            return Response(
                response.status,
                selected_headers(response.headers),
                payload,
                None,
            )
    except HTTPError as exc:
        headers = selected_headers(exc.headers)
        try:
            body = exc.read(MAX_BODY_BYTES + 1)
            payload = json.loads(body) if len(body) <= MAX_BODY_BYTES else None
        except (OSError, json.JSONDecodeError):
            payload = None
        return Response(exc.code, headers, payload, f"HTTP {exc.code}")
    except (OSError, URLError, TimeoutError) as exc:
        return Response(None, {}, None, type(exc).__name__)


def selected_headers(headers: Any) -> dict[str, str]:
    names = (
        "content-type",
        "cache-control",
        "vary",
        "location",
        "www-authenticate",
    )
    return {
        name: str(headers.get(name, ""))
        for name in names
        if headers.get(name) is not None
    }


def response_summary(response: Response) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "httpStatus": response.status,
        "headers": response.headers,
    }
    if response.error:
        summary["error"] = response.error
    if isinstance(response.payload, dict):
        summary["jsonKeys"] = sorted(str(key) for key in response.payload)
    elif isinstance(response.payload, list):
        summary["jsonArrayLength"] = len(response.payload)
    return summary


def is_https_url(value: Any, *, no_port: bool = False) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return (
        parsed.scheme == "https"
        and bool(parsed.hostname)
        and (not no_port or parsed.port is None)
    )


def is_native_callback(value: Any, client_id: Any) -> bool:
    if not isinstance(value, str) or not isinstance(client_id, str):
        return False
    parsed = urlparse(client_id)
    if not parsed.hostname or parsed.scheme != "https":
        return False
    reverse_dns_scheme = ".".join(reversed(parsed.hostname.split(".")))
    return value.startswith(f"{reverse_dns_scheme}:/") and " " not in value


def metadata_probe(timeout: float) -> dict[str, Any]:
    path = ROOT / "upstream/social-app/public/oauth-client-metadata.json"
    expected = json.loads(path.read_text())
    url = f"{PUBLIC_ORIGIN}/oauth-client-metadata.json"
    response = fetch_json(url, timeout)
    live = response.payload if isinstance(response.payload, dict) else {}
    redirect_uris = live.get("redirect_uris")
    grant_types = live.get("grant_types")
    response_types = live.get("response_types")
    scope_values = (
        live.get("scope", "").split()
        if isinstance(live.get("scope"), str)
        else []
    )
    required_contract = {
        "http200": response.status == 200,
        "jsonContentType": "application/json"
        in response.headers.get("content-type", "").lower(),
        "clientId": live.get("client_id") == url,
        "httpsClientIdWithoutPort": is_https_url(live.get("client_id"), no_port=True),
        "authorizationCodeGrant": isinstance(grant_types, list)
        and "authorization_code" in grant_types,
        "refreshGrant": isinstance(grant_types, list)
        and "refresh_token" in grant_types,
        "codeResponse": isinstance(response_types, list) and "code" in response_types,
        "atprotoScope": "atproto" in scope_values,
        "dpopBound": live.get("dpop_bound_access_tokens") is True,
        "webCallback": isinstance(redirect_uris, list)
        and f"{PUBLIC_ORIGIN}/oauth/callback" in redirect_uris,
        "nativeCallback": isinstance(redirect_uris, list)
        and any(
            is_native_callback(item, live.get("client_id"))
            for item in redirect_uris
        ),
    }
    contract_passed = all(required_contract.values())
    matches_local = live == expected
    legacy_scopes = [
        scope
        for scope in scope_values
        if scope in {"transition:generic", "transition:chat.bsky"}
    ]
    return {
        "url": url,
        **response_summary(response),
        "contractStatus": "PASS" if contract_passed else "FAIL",
        "sourceArtifactStatus": "CURRENT" if matches_local else "STALE",
        "requiredContract": required_contract,
        "scopeTokenCount": len(scope_values),
        "legacyTransitionScopes": legacy_scopes,
        "spaceScopeAdvertised": any(
            scope.startswith("space:us.edriffles.radlib.") for scope in scope_values
        ),
        "matchesCheckedInMetadata": matches_local,
    }


def protected_resource_probe(timeout: float) -> dict[str, Any]:
    url = f"{PDS_ORIGIN}/.well-known/oauth-protected-resource"
    response = fetch_json(url, timeout)
    payload = response.payload if isinstance(response.payload, dict) else {}
    auth_servers = payload.get("authorization_servers")
    bearer_methods = payload.get("bearer_methods_supported")
    checks = {
        "http200": response.status == 200,
        "resource": payload.get("resource") == PDS_ORIGIN,
        "oauthIssuer": isinstance(auth_servers, list) and OAUTH_ORIGIN in auth_servers,
        "headerBearer": isinstance(bearer_methods, list) and "header" in bearer_methods,
    }
    return {
        "url": url,
        **response_summary(response),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
    }


def authorization_server_probe(timeout: float) -> dict[str, Any]:
    url = f"{OAUTH_ORIGIN}/.well-known/oauth-authorization-server"
    response = fetch_json(url, timeout)
    payload = response.payload if isinstance(response.payload, dict) else {}
    checks = {
        "http200": response.status == 200,
        "issuer": payload.get("issuer") == OAUTH_ORIGIN,
        "parRequired": payload.get("require_pushed_authorization_requests") is True,
        "parEndpoint": is_https_url(payload.get("pushed_authorization_request_endpoint")),
        "s256": "S256" in (payload.get("code_challenge_methods_supported") or []),
        "authorizationCode": "authorization_code" in (payload.get("grant_types_supported") or []),
        "refreshToken": "refresh_token" in (payload.get("grant_types_supported") or []),
        "atproto": "atproto" in (payload.get("scopes_supported") or []),
    }
    return {
        "url": url,
        **response_summary(response),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "advertisedScopes": payload.get("scopes_supported", []),
    }


def did_probe(timeout: float) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for host in (PDS_ORIGIN, OAUTH_ORIGIN):
        url = f"{host}/.well-known/did.json"
        response = fetch_json(url, timeout)
        payload = response.payload if isinstance(response.payload, dict) else {}
        services = payload.get("service")
        results[host] = {
            "url": url,
            **response_summary(response),
            "status": "PASS"
            if response.status == 200
            and isinstance(payload.get("id"), str)
            and isinstance(services, list)
            and any(
                isinstance(service, dict)
                and service.get("type") == "AtprotoPersonalDataServer"
                and service.get("serviceEndpoint") == OAUTH_ORIGIN
                for service in services
            )
            else "FAIL",
            "did": payload.get("id"),
            "serviceEndpoints": [
                service.get("serviceEndpoint")
                for service in services
                if isinstance(service, dict) and "serviceEndpoint" in service
            ]
            if isinstance(services, list)
            else [],
        }
    return results


def health_probe(timeout: float) -> dict[str, Any]:
    url = f"{PDS_ORIGIN}/xrpc/_health"
    response = fetch_json(url, timeout)
    payload = response.payload if isinstance(response.payload, dict) else {}
    return {
        "url": url,
        **response_summary(response),
        "status": "PASS" if response.status == 200 and "version" in payload else "FAIL",
        "version": payload.get("version"),
    }


def private_boundary_probe(timeout: float) -> dict[str, Any]:
    space = "at://did:plc:cndgd3x3zxqmuv6rm3lsjhjm/space/us.edriffles.radlib.community/probe"
    targets = {
        "listCommunities": (
            f"{PDS_ORIGIN}/xrpc/us.edriffles.radlib.private.listCommunities?"
            + urlencode({"limit": "50"})
        ),
        "getSpace": (
            f"{PDS_ORIGIN}/xrpc/us.edriffles.radlib.private.getSpace?"
            + urlencode({"space": space})
        ),
    }
    results: dict[str, Any] = {}
    for name, url in targets.items():
        response = fetch_json(url, timeout)
        cache_control = response.headers.get("cache-control", "").lower()
        vary = response.headers.get("vary", "").lower()
        checks = {
            "unauthorized": response.status == 401,
            "privateCache": "private" in cache_control,
            "noStore": "no-store" in cache_control,
            "authorizationVary": "authorization" in vary,
            "dpopVary": "dpop" in vary,
        }
        results[name] = {
            "url": url,
            **response_summary(response),
            "status": "PASS" if all(checks.values()) else "FAIL",
            "checks": checks,
        }
    return results


def dig_txt(server: str, timeout: float) -> tuple[str, list[str]]:
    if shutil.which("dig") is None:
        return "NOT_RUN_DIG_UNAVAILABLE", []
    try:
        completed = subprocess.run(
            ["dig", "+short", "+time=3", "+tries=1", f"@{server}", "TXT", LEXICON_AUTHORITY_NAME],
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"NOT_RUN_{type(exc).__name__.upper()}", []
    if completed.returncode != 0:
        return "FAIL_DNS_QUERY", []
    values = [
        line.strip().strip('"')
        for line in completed.stdout.splitlines()
        if line.strip()
    ]
    return ("PASS" if values else "FAIL_EMPTY_DNS_RESPONSE"), values


def dns_authority_probe(timeout: float) -> dict[str, Any]:
    resolver_results: dict[str, Any] = {}
    values: list[str] = []
    for server in LEXICON_AUTHORITY_RESOLVERS:
        status, answers = dig_txt(server, timeout)
        resolver_results[server] = {"status": status, "answers": answers}
        values.extend(answers)
    distinct = sorted(set(values))
    valid = all(re.fullmatch(r"did=did:(?:plc|web):[A-Za-z0-9:._-]+", value) for value in distinct)
    same = len(distinct) == 1
    return {
        "name": LEXICON_AUTHORITY_NAME,
        "status": "PASS" if same and valid else "FAIL",
        "resolverResults": resolver_results,
        "distinctAnswers": distinct,
        "authorityDid": distinct[0].removeprefix("did=") if same and distinct else AUTHORITY_DID_FALLBACK,
        "agreement": same,
    }


def plc_probe(authority_did: str, timeout: float) -> dict[str, Any]:
    encoded = quote(authority_did, safe="")
    data_url = f"https://plc.directory/{encoded}/data"
    audit_url = f"https://plc.directory/{encoded}/log/audit"
    data = fetch_json(data_url, timeout)
    audit = fetch_json(audit_url, timeout)
    data_payload = data.payload if isinstance(data.payload, dict) else {}
    audit_payload = audit.payload if isinstance(audit.payload, list) else []
    data_shape = data.status == 200 and (
        data_payload.get("id") == authority_did
        or data_payload.get("did") == authority_did
        or "rotationKeys" in data_payload
    )
    audit_shape = audit.status == 200 and all(
        isinstance(entry, dict)
        and (
            entry.get("type") in {"plc_operation", "plc_tombstone"}
            or isinstance(entry.get("operation"), dict)
        )
        for entry in audit_payload
    )
    history = [
        entry.get("operation")
        if isinstance(entry, dict) and "operation" in entry
        else entry
        for entry in audit_payload
    ]
    cryptographic_verification = verify_live_plc_history(
        authority_did, history, timeout
    )
    return {
        "authorityDid": authority_did,
        "data": {"url": data_url, **response_summary(data), "status": "PASS" if data_shape else "FAIL"},
        "audit": {
            "url": audit_url,
            **response_summary(audit),
            "status": "PASS" if audit_shape and bool(audit_payload) else "FAIL",
            "operationCount": len(audit_payload),
        },
        "cryptographicHistoryVerification": cryptographic_verification,
    }


def verify_live_plc_history(
    did: str, history: list[Any], timeout: float
) -> dict[str, Any]:
    """Run the checked-in client verifier against the live audit response.

    The live probe is Python for safe response handling, while PLC verification
    remains owned by the client implementation in plc-history.ts. Bundling that
    existing module into a temporary Node process avoids a second verifier with
    potentially different canonical-CBOR or signature semantics.
    """
    node = shutil.which("node")
    bundler = ROOT / "upstream/social-app/node_modules/.bin/esbuild"
    entrypoint = ROOT / "upstream/social-app/src/lib/plc-history.ts"
    if not node or not bundler.is_file():
        return {
            "status": "NOT_RUN_VERIFIER_RUNTIME_UNAVAILABLE",
        }
    with tempfile.TemporaryDirectory(prefix="social-edriffles-plc-") as directory:
        bundle = Path(directory) / "plc-history.mjs"
        build = subprocess.run(
            [
                str(bundler),
                str(entrypoint),
                "--bundle",
                "--platform=node",
                "--format=esm",
                f"--outfile={bundle}",
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout,
        )
        if build.returncode != 0:
            return {"status": "FAIL_VERIFIER_BUILD"}
        verifier = """
import {readFileSync} from 'node:fs'

const {verifyPlcHistory} = await import(process.argv[1])

const input = JSON.parse(readFileSync(0, 'utf8'))
const result = await verifyPlcHistory(input.did, input.history)
process.stdout.write(JSON.stringify({
  status: result.status,
  verifiedOperations: result.verifiedOperations,
  headCid: result.headCid,
}))
"""
        try:
            run = subprocess.run(
                [node, "--input-type=module", "-e", verifier, str(bundle)],
                input=json.dumps({"did": did, "history": history}),
                capture_output=True,
                check=False,
                text=True,
                timeout=timeout,
            )
        except (OSError, subprocess.TimeoutExpired):
            return {"status": "NOT_RUN_VERIFIER_PROCESS_FAILED"}
        if run.returncode != 0:
            return {"status": "FAIL_VERIFIER_PROCESS"}
        try:
            result = json.loads(run.stdout)
        except json.JSONDecodeError:
            return {"status": "FAIL_VERIFIER_OUTPUT"}
        if not isinstance(result, dict):
            return {"status": "FAIL_VERIFIER_OUTPUT"}
        status = result.get("status")
        if status not in {"verified", "tombstoned"}:
            return {
                "status": "FAIL_LIVE_PLC_HISTORY",
                "verifierStatus": status,
                "verifiedOperations": result.get("verifiedOperations"),
            }
        return {
            "status": "PASS",
            "verifierStatus": status,
            "verifiedOperations": result.get("verifiedOperations"),
            "headCid": result.get("headCid"),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument(
        "--allow-stale-source",
        action="store_true",
        help="return zero when public endpoints are valid but do not match local metadata",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="also write the secret-free probe JSON to this local path",
    )
    args = parser.parse_args()

    metadata = metadata_probe(args.timeout)
    protected = protected_resource_probe(args.timeout)
    authorization = authorization_server_probe(args.timeout)
    did = did_probe(args.timeout)
    health = health_probe(args.timeout)
    private = private_boundary_probe(args.timeout)
    dns = dns_authority_probe(args.timeout)
    authority_did = str(dns.get("authorityDid") or AUTHORITY_DID_FALLBACK)
    plc = plc_probe(authority_did, args.timeout)

    hard_statuses = [
        metadata["contractStatus"],
        protected["status"],
        authorization["status"],
        *(item["status"] for item in did.values()),
        health["status"],
        *(item["status"] for item in private.values()),
        dns["status"],
        plc["data"]["status"],
        plc["audit"]["status"],
    ]
    hard_pass = all(status == "PASS" for status in hard_statuses)
    source_current = metadata["sourceArtifactStatus"] == "CURRENT"
    if hard_pass and source_current:
        overall = "PASS_CURRENT_PUBLIC_CONTRACT"
    elif hard_pass:
        overall = "PUBLIC_CONTRACT_VALID_BUT_DEPLOYMENT_STALE"
    else:
        overall = "PUBLIC_CONTRACT_FAILED"

    output = {
        "format": "us.edriffles.radlib.live-public-probe/1",
        "probedAt": __import__("datetime").datetime.now(__import__("datetime").UTC).isoformat().replace("+00:00", "Z"),
        "credentialsUsed": False,
        "writesPerformed": False,
        "origins": {
            "web": PUBLIC_ORIGIN,
            "pds": PDS_ORIGIN,
            "oauth": OAUTH_ORIGIN,
        },
        "overallStatus": overall,
        "metadata": metadata,
        "protectedResource": protected,
        "authorizationServer": authorization,
        "didDocuments": did,
        "health": health,
        "privateBoundary": private,
        "lexiconDnsAuthority": dns,
        "plc": plc,
    }
    serialized = json.dumps(output, indent=2, sort_keys=True) + "\n"
    print(serialized, end="")
    if args.output:
        args.output.write_text(serialized)

    if not hard_pass:
        return 1
    if not source_current and not args.allow_stale_source:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
