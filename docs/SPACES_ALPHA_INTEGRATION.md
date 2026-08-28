# Spaces Alpha Integration

Status: `ALPHA_GATED / SOURCE_READY / RADLIB.EDRIFFLES.US_CUTOVER_PENDING` on `codex/spaces-alpha-integration`.

This branch uses the upstream ATProto `permissioned-data-alpha` branch as the PDS
base and carries the fork's protected-account/community policy above the
standard Spaces data plane. It is a disposable alpha test lane, not a
production activation or owner acceptance receipt.

## Pinned sources

| Component | Base | Reviewed checkout | Role |
|---|---|---|---|
| PDS | `bluesky-social/atproto` `permissioned-data-alpha` at `4c33457afe96ad2e5d2fe6bd975f094cd6f67328` | `9c3d92f04335d624a79acbbf5f346130f00ffbdd` | Spaces protocol, DPoP credentials, ActorStore data plane, and fork product control API |
| Client | `bluesky-social/social-app` `main` at `c4c999ff4f8f6bf42e752a1b0d39718a6330b68b` | `9fb8bfb623bb09b05acb7533e3d043211d233ba9` | Generated Space adapter, multi-writer fanout, sync boundary, composer, Bulletin-style board, self-contained Communities board creation, resilient deep-link board discovery, migrated-PDS auth recovery, and private bulletin posting |

The machine-readable copies are `upstream-pins.json` and
`artifacts/upstream-baseline.json`. The root checkout and both submodule
checkouts are pinned branch state; the synchronized PDS and client commits are
pushed to their fork branches. Nothing in this document authorizes production
activation, default-branch changes, or a moving-head rebase.

## Boundary

The standard Spaces APIs own private transport and repository data:

- `com.atproto.space.*` for Space-scoped records, blobs, credentials, and
  repository discovery;
- `com.atproto.simplespace.*` for Space creation, policy, and membership;
- the PDS `@atproto/space` implementation for DPoP-bound credentials and
  Space synchronization primitives. The client adapter exposes the matching
  record/blob/repo-discovery/recovery queries, but it is not itself a complete
  multi-PDS sync service.

`us.edriffles.radlib.private.*` remains only for the higher-level protected-account and
community control plane: visibility, follow approval/revocation, community
metadata, discovery, invites, membership policy, and bans. Its SQLite state is
policy state, not the authority for new Space records or blobs. The old custom
record/blob/feed/sync transport is not mounted as a second active data plane;
existing legacy tables are retained only behind an explicitly selected
migration adapter.

## Feature gates

PDS deployments using this slice must set:

```text
PDS_SPACES_ALPHA_ENABLED=true
PDS_PROTECTED_ACCOUNTS_ENABLED=true
PDS_COMMUNITIES_ENABLED=true
```

The client defaults to the standard Space adapter when
`EXPO_PUBLIC_SPACES_ALPHA_ENABLED=1`. The legacy client adapter is disabled
unless `EXPO_PUBLIC_LEGACY_RADLIB_PRIVATE_ENABLED=1` is explicitly set for a
migration-only lane. The PDS control routes do not require
`PDS_LEGACY_RADLIB_PRIVATE_ENABLED`; that flag is not part of the normal
Spaces path. A production web bundle must also set
`EXPO_PUBLIC_SPACES_ALPHA_PRODUCTION_ENABLED=1`; that second setting is an
explicit operator acknowledgement for the requested community-board
deployment and does not change the alpha status or production-readiness gates
below.

## Wave 1/2 hardening evidence

The first two Copernicus waves are verified in the local source-built PDS
checkout:

- Protected access grants fail closed when a remote block collection is
  unavailable, malformed, paginated beyond the configured bound, or exceeds
  the shared five-second lookup deadline. Confirmed blocks still revoke the
  pending/approved state.
- `us.edriffles.radlib.community` is a checked-in `type: "space"` Lexicon with
  `key: "any"` and only `us.edriffles.radlib.private.post` declared. The
  disposable authority DID publishes the checked-in `us.edriffles.radlib.*`
  declarations and the OAuth write boundary rejects an undeclared collection.
  Independent DNS authority is now a named cutover gate at
  `_lexicon.radlib.edriffles.us`; it is not claimed by the local resolver.
- Private `us.edriffles.radlib.private.*` responses set `Cache-Control: private,
  no-store` and vary on `Authorization` and `DPoP`, including service-auth
  fallback failures and successes. The local HTTP header matrix passes, and
  deployed unauthorized probes for both `listCommunities` and `getSpace`
  return the corrected headers through the Cloudflare Tunnel. A credentialed
  deployed probe was not run because no production token was used.

The protocol boundary follows the [official Spaces alpha guidance](https://atproto.com/blog/atproto-spaces-alpha)
and [Permissioned Data proposal 0016](https://github.com/bluesky-social/proposals/blob/main/0016-permissioned-data/README.md).
Neither source makes Spaces confidential or production-ready.

## Reference PDS Docker test lane

The Spaces alpha announcement names the reference PDS image
`ghcr.io/bluesky-social/atproto:pds-spaces-alpha`. The image is intended to be
used with the reference PDS distribution and does not need a new upstream
configuration block for Spaces. This is an alpha compatibility target for
non-production testing, not a production release: schemas may change without
clean migrations, and real accounts must not be migrated to it.

Use a separate test project with test identities and bind it to loopback only.
The named volume below makes test data survive a container restart, but it is
not a migration, backup, or upgrade guarantee:

```yaml
name: spaces-alpha-test

services:
  pds:
    image: ghcr.io/bluesky-social/atproto:pds-spaces-alpha
    restart: "no"
    env_file:
      - .env.test
    ports:
      - "127.0.0.1:2583:3000"
    volumes:
      - spaces-alpha-test-data:/pds
    healthcheck:
      test:
        - CMD
        - node
        - -e
        - >-
          fetch('http://127.0.0.1:3000/xrpc/_health')
          .then((response) => process.exit(response.ok ? 0 : 1))
          .catch(() => process.exit(1))
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 30s

volumes:
  spaces-alpha-test-data:
```

Create `.env.test` from the reference PDS `sample.env`, using disposable
test-only keys and paths. For this fork, add the opt-in flags from the section
above; the upstream image's “no new configuration” statement covers upstream
Spaces support, not this fork's `us.edriffles.radlib.private.*` compatibility
policy.
Do not publish the PDS on `0.0.0.0`, put it behind a public reverse proxy, or
reuse production secrets for this lane.

Before using the test PDS, verify the registry tag and readiness without
pulling over an existing deployment:

```sh
docker manifest inspect ghcr.io/bluesky-social/atproto:pds-spaces-alpha
docker compose --project-name spaces-alpha-test up -d
curl -fsS http://127.0.0.1:2583/xrpc/_health
curl -fsS http://127.0.0.1:2583/xrpc/com.atproto.server.describeServer
docker compose --project-name spaces-alpha-test ps
```

The WebSocket sync probe from the reference PDS documentation is an additional
readiness check when the test environment has a WebSocket client:
`wss://<test-host>/xrpc/com.atproto.sync.subscribeRepos?cursor=0`. A successful
HTTP health response alone does not establish Space membership, credential
issuance, private record writes, or multi-PDS interoperability; those remain
application-level tests.

The current local checkout is intentionally not replaced by that registry
image. It runs a source-built `codex/atproto-pds-spaces-alpha:test` image on
`127.0.0.1:2583` with persistent test volume data, which is the appropriate
lane for exercising this fork's unmerged control-plane changes. Keep the
official alpha image as a separately reproducible upstream compatibility lane.

## Evidence and open gates

Verified in this checkout:

- root contract and pinned-tree checks;
- PDS Lexicon code generation and TypeScript build;
- PDS header, Radlib Spaces, community Lexicon, OAuth, record, and membership
  suites: 149 tests passed;
- formatter and lint checks for the touched PDS/dev-env files.
- Current pushed fork synchronization: PDS `9c3d92f04335d624a79acbbf5f346130f00ffbdd`
  and client `9fb8bfb623bb09b05acb7533e3d043211d233ba9`; both fork branches
  are pushed, while owner acceptance and production gates remain separate.
- Previous pushed fork source: PDS `2a119ba5f15a349d0db63fe46d1d3c854dfb9760`;
  it remains historical evidence for the earlier alpha receipt.
- The prior disposable image and tunnel probe are retained as historical
  evidence. The new single-host route is described in
  `docs/RADLIB_EDRIFFLES_HOST_CUTOVER.md`; its Worker dry run passes, but the
  public route and PDS public-host reconfiguration remain pending.
- Credentialed disposable OAuth protocol flow passed through the official Node
  client with PAR, PKCE S256, DPoP, callback, forced refresh, and revocation;
  the browser UI walkthrough remains unrun because no browser executable is
  available.
- The pre-cutover PDS health, discovery, and unauthorized-header probes remain
  historical evidence; they must be rerun through `https://radlib.edriffles.us`
  after the edge route and PDS host configuration are live.

Not established by this branch:

- a production credentialed header probe, because no production token was used;
- independent DNS publication of `us.edriffles.radlib.*` authority at
  `_lexicon.radlib.edriffles.us`;
- native Hermes/Metro WebCrypto compatibility;
- a server-side private AppView or browser notification service (the client has
  a rebuildable cursor/sink boundary and generated notification wrappers);
- immediate invalidation of already-issued Space credentials after membership
  removal; the disposable credentialed probe confirms that new issuance is
  rejected while an already-issued alpha access remains usable until expiry;
- production fielding or owner acceptance. This remains an alpha/test lane
  until the single-host route is deployed and independently probed.

These are explicit follow-up gates. They must not be inferred from a passing
typecheck, fixture, or local PDS build.
