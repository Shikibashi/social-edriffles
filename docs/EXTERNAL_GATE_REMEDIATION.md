# External Gate Remediation

This runbook closes evidence gaps without turning a local fixture into a
production claim. The release manifest remains blocked until a receipt is
captured from the named external target and bound to the tested source,
deployment image, domains, timestamp, and environment.

## Research basis

The design follows the current AT Protocol OAuth requirements: HTTPS client
metadata, authorization-code flow, PKCE S256, PAR, DPoP, issuer and DID
binding, and refresh-token metadata are protocol requirements rather than
project-specific conventions. See the [AT Protocol OAuth specification](https://atproto.com/specs/oauth).

The provider boundaries follow the AT stack model: a PDS hosts account data
and identity, while Relays distribute authenticated repository events and
AppViews materialize application-specific views. A single-PDS application is
valid, but a Relay is a scale and distribution component, not a constitutional
authority. See the [AT Stack guide](https://atproto.com/guides/the-at-stack)
and [sync specification](https://atproto.com/specs/sync).

The PLC boundary uses the ecosystem's read-replica model. PLC histories are
self-authenticating and must be verified from their signed operations; a
replica adds accountability only when its operator is actually separate. See
[PLC read replicas](https://atproto.com/blog/plc-replicas) and the
[go-didplc read-replica implementation](https://github.com/did-method-plc/go-didplc/tree/main/cmd/plc-replica).
For the Relay target, the relevant upstream precedent is the
[Indigo Relay](https://github.com/bluesky-social/indigo/blob/main/cmd/relay/README.md),
which exposes firehose, crawl, status, persistence, and operational logs.

## Batch 1: short-TTL OAuth evidence

The existing PDS provider already owns token expiry, refresh-token rotation,
authorization-code replay handling, and DPoP resource requests. The new
configuration seam passes an optional `PDS_OAUTH_TOKEN_MAX_AGE_MS` through the
existing PDS config into the upstream OAuth provider. It is unset by default;
the example configuration labels it disposable-test-only.

Run this only against a separately disposable PDS and a disposable identity:

```text
PDS_OAUTH_TOKEN_MAX_AGE_MS=5000
RADLIB_CONFIRM_DISPOSABLE_TEST=1
RADLIB_RUN_EXPIRY_REPLAY=1
RADLIB_OAUTH_EXPECTED_TOKEN_MAX_AGE_MS=5000
RADLIB_EXPIRY_WAIT_MAX_MS=30000
RADLIB_PUBLIC_OAUTH_RECEIPT=artifacts/receipts/credentialed-public-oauth.json
```

The guarded walkthrough uses two disposable identities. The first proves an
authorized request before expiry, rejects the saved access credential after
expiry, refreshes successfully, observes refresh rotation, and rejects replay
of the old refresh credential. The second proves authorization-code replay
rejection and that replay invalidates the resulting session. Raw credentials,
codes, verifiers, DPoP keys, cookies, and callback URLs stay in memory and are
never written to the receipt.

The existing non-expiry browser probe remains the default. A short TTL is not a
production security recommendation; it is a bounded timing configuration that
makes the lifecycle observable in a disposable environment.

For a local protocol check, the same runner has an explicitly opt-in loopback
lane. It uses the loopback-native OAuth client metadata convention, starts a
temporary callback listener, and can only target a loopback PDS. It is useful
for validating the source-built image before deployment, but its `local-
disposable` receipt is not eligible for the external release gate:

```sh
RADLIB_ALLOW_LOCAL_DISPOSABLE=1 \
RADLIB_CONFIRM_DISPOSABLE_TEST=1 \
RADLIB_DISPOSABLE_PDS_ORIGIN=http://127.0.0.1:2594 \
RADLIB_DISPOSABLE_HANDLE_DOMAIN=.test \
RADLIB_RUN_EXPIRY_REPLAY=1 \
RADLIB_OAUTH_EXPECTED_TOKEN_MAX_AGE_MS=5000 \
RADLIB_EXPIRY_WAIT_MAX_MS=30000 \
RADLIB_PUBLIC_OAUTH_RECEIPT=/tmp/radlib-local-oauth-expiry.json \
node scripts/credentialed_public_oauth.mjs
```

The local lane deliberately does not relax the production HTTPS client,
redirect, or issuer rules. The external lane still requires the disposable
HTTPS deployment and its fresh credentialed receipt.

When the short-TTL PDS is deployed as a staging subdomain in the existing
`edriffles.us` zone, opt in explicitly instead of sending the walkthrough to
the live PDS. The runner accepts that shape only when all three bindings are
provided:

```sh
RADLIB_ALLOW_EDRIFFLES_SUBDOMAIN_DISPOSABLE=1 \
RADLIB_DISPOSABLE_PDS_ORIGIN=https://pds-oauth-test.edriffles.us \
RADLIB_EXPECTED_OAUTH_ISSUER=https://oauth-oauth-test.edriffles.us \
RADLIB_DISPOSABLE_HANDLE_DOMAIN=.oauth-test.edriffles.us \
RADLIB_CONFIRM_DISPOSABLE_TEST=1
```

These are subdomains of the existing registrable domain; no `radlib.org` or
other new domain is required. The DNS, HTTPS certificate, OAuth issuer, PDS
service configuration, and disposable identity still have to be controlled
and deployed before this becomes external evidence.

## Batch 2: controlled Relay/AppView canary evidence

Provision a disposable PDS, a Relay, and an AppView under operator-controlled
endpoints. The Relay must retain firehose captures, persistence, and logs for
the test window. The AppView must retain query results, materialized storage,
and logs. The operator must be able to export those artifacts after the test.
Do not use a public AppView response as a substitute for these captures: an
HTTP 403 or an empty query is inconclusive when ingestion or access is not
controlled.

Use two distinguishable records:

1. a public control canary that must be observable in the expected public path;
2. a private canary that is directly readable by its authorized owner but must
   not appear in the PDS public CAR/sequencer path, Relay stream/storage/logs,
   or AppView query/storage/logs.

The receipt validator requires capture, storage, and log references for both
downstream services, checks the negative observations explicitly, and records
the target operator identity. It intentionally does not infer operator
independence from those fields; that is a separate gate.

## Batch 3: independent PLC replica evidence

Run the reference-compatible read-replica shape or another documented
compatible implementation under an operator who controls a distinct endpoint,
service identity, signing key, and operational evidence. The primary and
mirror operators must be independently identified; two endpoints controlled by
the same person or organization are redundancy, not independence.

The receipt must include:

- operator IDs, service DIDs, public Ed25519 keys, HTTPS endpoints, and
  independently verifiable control evidence;
- a signed DID-history statement whose digest and Ed25519 signature are checked
  by the local validator;
- verification of genesis-derived DID, previous CIDs, rotation signatures,
  tombstone rules, stale/malformed/invalid-signature fixtures, and primary /
  mirror history agreement;
- any resolver disagreement, including provenance and a user-visible
  reconciliation outcome.

The signed statement covers the history verification result, not a claim that
one resolver is universally correct. The client can therefore expose
disagreement while still requiring cryptographic history validation.

## Evidence promotion rule

Synthetic fixtures under `tests/fixtures/` prove only that the receipt schema,
secret checks, negative checks, and signature verification work. They are
deliberately marked `fixture` and are not included in the release manifest.

The three manifest blockers can change only after the corresponding external
receipt is captured and independently reviewed:

| Blocker | Required external receipt | Current state |
| --- | --- | --- |
| `PRIVATE_CANARY_RELAY_APPVIEW_NOT_RUN` | controlled Relay/AppView captures, storage, logs, and canary scan | CLOSED for the disposable staging target: `artifacts/external-gates/receipts/external-private-canary-current.json` records a fresh HTTPS run with public control and private negative-path checks |
| `OAUTH_EXPIRY_GAP` | short-TTL credentialed browser walkthrough | CLOSED for the disposable staging target: `artifacts/external-gates/receipts/external-oauth-expiry-current.json` records the disposable HTTPS 5-second TTL, stale-token, refresh-rotation, and replay walkthrough |
| `PLC_OPERATOR_INDEPENDENCE_NOT_PROVEN` | independent operator evidence plus signed DID-history receipt | NOT PROVEN: no separate operator identity, service key, endpoint, and signed history receipt has been supplied |

The disposable staging evidence package has status
`BLOCKED_EXTERNAL_PLC_INDEPENDENCE_GATE`: the first two staging gates have
fresh receipts, while PLC operator independence remains unresolved. The
production release manifest is intentionally not rewritten from this staging
package because its current source-bound deployment record still points to a
different deployed image. A production release refresh is therefore a
separate operation after the tested source is actually deployed. The
implementation adds a reproducible path to gather the missing evidence; it
does not fabricate independent-operator evidence.

## Verification commands

From the repository root:

```text
python3 scripts/validate_external_gate_receipts.py
python3 -m unittest tests.test_external_gate_receipts
python3 scripts/validate_contract.py
python3 scripts/validate_oauth_spaces_receipts.py
```

The first two commands validate synthetic receipt behavior. The latter two
continue to enforce the current manifest and its exact blocker set.

After the short-TTL PDS is actually deployed, regenerate the source-bound
bindings with the deployment record and a fresh credential-free live probe:

```text
python3 scripts/refresh_oauth_spaces_evidence.py \
  --deployment-record artifacts/deployment-current.json \
  --live-probe /path/to/fresh-live-probe.json
python3 scripts/validate_oauth_spaces_receipts.py
```

Do not edit the deployment record to make a local candidate appear deployed.
The source-bound digest is expected to differ until the new image and web
artifact are genuinely deployed.
