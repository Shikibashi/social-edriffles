# Spaces Alpha Integration

Status: `ALPHA_GATED` on `codex/spaces-alpha-integration`.

This branch uses the upstream ATProto `permissioned-data` branch as the PDS
base and carries the fork's protected-account/community policy above the
standard Spaces data plane. It is a disposable alpha test lane, not a
production activation or owner acceptance receipt.

## Pinned sources

| Component | Base | Reviewed checkout | Role |
|---|---|---|---|
| PDS | `bluesky-social/atproto` `permissioned-data` at `89deb9fac20e56fa2a262fe9746ed52bc1095ba` | `d906e959dabcd017b4a0fa840e755d3a5f5d77d8` | Spaces protocol, DPoP credentials, ActorStore data plane, and fork product control API |
| Client | `bluesky-social/social-app` at `1f5c698165c922e707833809902ee959e9824f00` | `fced54453acf1aae2264b7178ba5a74bbe95bf55` | Generated Space adapter, multi-writer fanout, sync boundary, composer, Bulletin-style board, self-contained Communities board creation, and migrated-PDS auth recovery |

The machine-readable copies are `upstream-pins.json` and
`artifacts/upstream-baseline.json`. The root checkout and both submodule
checkouts are pinned branch state; the commits are pushed to the fork remotes,
but nothing in this document authorizes production activation or a moving-head
rebase.

## Boundary

The standard Spaces APIs own private transport and repository data:

- `com.atproto.space.*` for Space-scoped records, blobs, credentials, and
  repository discovery;
- `com.atproto.simplespace.*` for Space creation, policy, and membership;
- the PDS `@atproto/space` implementation for DPoP-bound credentials and
  Space synchronization primitives. The client adapter exposes the matching
  record/blob/repo-discovery/recovery queries, but it is not itself a complete
  multi-PDS sync service.

`org.radlib.private.*` remains only for the higher-level protected-account and
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
Spaces path.

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
Spaces support, not this fork's `org.radlib.private.*` compatibility policy.
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

- root contract and pinned-tree checks, after metadata update;
- social-app web typecheck;
- generated Space Lexicons plus focused social-app permissioned-data and
  Spaces adapter unit tests;
- PDS code generation/build and the existing focused Spaces test files, when
  the local dependency checkout permits them.

Not established by this branch:

- native Hermes/Metro WebCrypto compatibility;
- a server-side private AppView or browser notification service (the client has
  a rebuildable cursor/sink boundary and generated notification wrappers);
- immediate invalidation of already-issued Space credentials after membership
  removal;
- production fielding, deployment, or owner acceptance.

These are explicit follow-up gates. They must not be inferred from a passing
typecheck, fixture, or local PDS build.
